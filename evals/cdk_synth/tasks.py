from pathlib import Path
import textwrap
import json
import uuid
import re
from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset, FieldSpec
from inspect_ai.solver import chain_of_thought, generate, self_critique
from inspect_ai.scorer import CORRECT, INCORRECT, Score, scorer, mean
from inspect_ai.util import sandbox, ExecResult
from inspect_ai.model import GenerateConfig

VERIFY_TIMEOUT = 60  # seconds

CODE_RE = re.compile(r"```python\n(.*?)```", re.DOTALL | re.IGNORECASE)


def _extract_code(raw: str) -> str:
    """Return just the python source from the model output."""
    if m := CODE_RE.search(raw):
        return textwrap.dedent(m.group(1))
    # fallback: remove lines that start with ANSWER: and dedent
    cleaned = re.sub(r"^ANSWER:.*$", "", raw, flags=re.IGNORECASE | re.MULTILINE)
    return textwrap.dedent(cleaned).strip()


def _write_project(src_code: str, workdir: Path) -> None:
    """Create a minimal CDK project inside *workdir*."""
    # (workdir / "requirements.txt").write_text("aws-cdk-lib>=2.0.0\nconstructs\n")
    (workdir / "cdk.json").write_text(json.dumps({"app": "python app.py"}))
    (workdir / "app.py").write_text(src_code)


@scorer(metrics=[mean()])
def cdk_verify():
    async def score(state, target):
        # 1. grab code
        code_raw = state.output.completion
        src = _extract_code(code_raw)

        # 2. host tmp dir that is mounted in the container
        tmp = Path("/tmp") / str(uuid.uuid4())
        tmp.mkdir(parents=True, exist_ok=True)
        _write_project(src, tmp)

        # 3. run synth inside the container
        try:
            result = await sandbox().exec(
                cmd=["bash", "-c", "cdk synth"],
                cwd=str(tmp),
                timeout=VERIFY_TIMEOUT,
            )
        except TimeoutError:
            result = ExecResult(False, 1, "", "cdk synth timed-out")

        # 4. optional cfn-lint
        if result.success:
            lint = await sandbox().exec(
                cmd=["cfn-lint", "cdk.out/**/*.template.json"],
                cwd=str(tmp),
            )
            result = lint if not lint.success else result

        explanation = (
            "cdk synth passed ✅" if result.success else f"❌ {result.stderr[:200]}"
        )
        return Score(
            value=CORRECT if result.success else INCORRECT,
            answer="synth-result",
            explanation=explanation,
        )

    return score


@task
def aws_cdk_synth():
    dataset = json_dataset(
        "cdk_synth.jsonl",
        sample_fields=FieldSpec(input="input", target="target"),
        shuffle=True,
        auto_id=True,
    )

    # Configure more robust API handling
    generate_config = GenerateConfig(
        max_retries=5,  # Retry failed API calls up to 5 times
        timeout=180,  # Increase timeout to 3 minutes
    )

    return Task(
        dataset=dataset,
        solver=[
            chain_of_thought(),
            generate(config=generate_config),
            self_critique(),  # Keep self_critique simple - retry config will be inherited
        ],
        scorer=cdk_verify(),
        sandbox=("docker", (Path(__file__).parent / "compose.yaml").as_posix()),
    )
