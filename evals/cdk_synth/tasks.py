from pathlib import Path
import textwrap
import json
import uuid
import re
import logging
import os
import subprocess
import tempfile
from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset, FieldSpec
from inspect_ai.solver import chain_of_thought, generate, self_critique
from inspect_ai.scorer import CORRECT, INCORRECT, Score, scorer, mean
from inspect_ai.util import sandbox, ExecResult
from inspect_ai.model import GenerateConfig

logger = logging.getLogger(__name__)

VERIFY_TIMEOUT = 60  # seconds

# Code extraction patterns in order of specificity
CODE_PATTERNS = [
    (r"```python\n(.*?)```", "python-fenced"),
    (r"```py\n(.*?)```", "py-fenced"),
    (r"```Python\n(.*?)```", "Python-fenced"),
    (r"```\n(.*?)```", "untagged-fenced"),
]


def _extract_code(raw: str) -> str:
    """Extract Python source from model output.

    Tries multiple code block patterns in order of specificity:
    1. ```python ... ``` (most common)
    2. ```py ... ``` (alternative)
    3. ```Python ... ``` (capitalized)
    4. ``` ... ``` (untagged)
    5. Fallback: remove ANSWER: lines and return cleaned text

    Returns:
        Extracted and dedented Python code
    """
    # Try each pattern in order
    for pattern, pattern_name in CODE_PATTERNS:
        matches = list(re.finditer(pattern, raw, re.DOTALL | re.IGNORECASE))
        if matches:
            # If multiple matches, take the largest one (most likely to be the full code)
            best_match = max(matches, key=lambda m: len(m.group(1)))
            code = textwrap.dedent(best_match.group(1)).strip()
            logger.debug(f"Code extracted via {pattern_name} pattern ({len(code)} chars, {len(matches)} matches)")
            return code

    # Fallback: remove ANSWER: lines and return cleaned text
    logger.warning("No code block found, using fallback extraction")
    cleaned = re.sub(r"^ANSWER:.*$", "", raw, flags=re.IGNORECASE | re.MULTILINE)
    return textwrap.dedent(cleaned).strip()


def _write_project(src_code: str, workdir: Path) -> None:
    """Create a minimal CDK project inside *workdir*."""
    # (workdir / "requirements.txt").write_text("aws-cdk-lib>=2.0.0\nconstructs\n")
    (workdir / "cdk.json").write_text(json.dumps({"app": "python app.py"}))
    (workdir / "app.py").write_text(src_code)


def _run_cdk_local(tmp_path: Path) -> tuple[bool, str]:
    """Run cdk synth locally using subprocess (no Docker).

    Returns:
        Tuple of (success: bool, stderr: str)
    """
    env = {
        **os.environ,
        "CDK_DEFAULT_ACCOUNT": "123456789012",
        "CDK_DEFAULT_REGION": "us-east-1",
    }

    try:
        logger.debug(f"Running cdk synth locally in {tmp_path}")
        result = subprocess.run(
            ["cdk", "synth"],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
            timeout=VERIFY_TIMEOUT,
            env=env,
        )
        logger.debug(f"cdk synth returned {result.returncode}")
        if result.returncode != 0:
            logger.debug(f"stderr: {result.stderr[:500]}")
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        logger.warning(f"cdk synth timed out after {VERIFY_TIMEOUT}s")
        return False, "cdk synth timed-out"
    except FileNotFoundError:
        logger.error("cdk command not found - install with: npm install -g aws-cdk")
        return False, "cdk command not found - install with: npm install -g aws-cdk"


def _run_cfn_lint_local(tmp_path: Path) -> tuple[bool, str]:
    """Run cfn-lint locally using subprocess.

    Returns:
        Tuple of (success: bool, stderr: str)
    """
    template_glob = tmp_path / "cdk.out" / "*.template.json"
    templates = list((tmp_path / "cdk.out").glob("*.template.json"))

    if not templates:
        logger.debug("No CloudFormation templates found to lint")
        return True, ""

    try:
        result = subprocess.run(
            ["cfn-lint"] + [str(t) for t in templates],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0, result.stderr
    except FileNotFoundError:
        logger.debug("cfn-lint not installed, skipping lint check")
        return True, ""  # Don't fail if cfn-lint not installed
    except subprocess.TimeoutExpired:
        return False, "cfn-lint timed-out"


@scorer(metrics=[mean()])
def cdk_verify_local():
    """CDK verification scorer using local subprocess execution.

    This scorer runs cdk synth directly on the host machine without Docker,
    making it more reliable in CI environments where Docker-in-Docker is problematic.

    Requires: npm install -g aws-cdk && pip install cfn-lint (optional)
    """
    async def score(state, target):
        # 1. Extract code from model output
        code_raw = state.output.completion
        src = _extract_code(code_raw)
        logger.debug(f"Extracted {len(src)} chars of code")

        # 2. Create temporary project directory
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            _write_project(src, tmp_path)
            logger.debug(f"Created CDK project in {tmp_path}")

            # 3. Run cdk synth
            success, stderr = _run_cdk_local(tmp_path)

            # 4. Optional cfn-lint if synth succeeded
            if success:
                lint_success, lint_stderr = _run_cfn_lint_local(tmp_path)
                if not lint_success:
                    success = False
                    stderr = lint_stderr

        explanation = (
            "cdk synth passed ✅" if success else f"❌ {stderr[:200]}"
        )
        return Score(
            value=CORRECT if success else INCORRECT,
            answer="synth-result",
            explanation=explanation,
        )

    return score


@scorer(metrics=[mean()])
def cdk_verify():
    """CDK verification scorer using Docker sandbox.

    Note: This may fail in CI environments. Set CDK_EVAL_MODE=local to use
    subprocess-based execution instead.
    """
    async def score(state, target):
        # 1. grab code
        code_raw = state.output.completion
        src = _extract_code(code_raw)
        logger.debug(f"Extracted {len(src)} chars of code for Docker sandbox evaluation")

        # 2. host tmp dir that is mounted in the container
        tmp = Path("/tmp") / str(uuid.uuid4())
        tmp.mkdir(parents=True, exist_ok=True)
        _write_project(src, tmp)
        logger.debug(f"Created CDK project in {tmp}")

        # 3. run synth inside the container
        try:
            logger.debug("Starting Docker sandbox execution...")
            result = await sandbox().exec(
                cmd=["bash", "-c", "cdk synth"],
                cwd=str(tmp),
                timeout=VERIFY_TIMEOUT,
            )
            logger.debug(f"Docker sandbox returned: success={result.success}")
        except TimeoutError:
            logger.warning(f"Docker sandbox timed out after {VERIFY_TIMEOUT}s")
            result = ExecResult(False, 1, "", "cdk synth timed-out")
        except Exception as e:
            logger.error(f"Docker sandbox failed with exception: {e}")
            result = ExecResult(False, 1, "", f"sandbox error: {str(e)[:100]}")

        # 4. optional cfn-lint
        if result.success:
            try:
                lint = await sandbox().exec(
                    cmd=["cfn-lint", "cdk.out/**/*.template.json"],
                    cwd=str(tmp),
                )
                result = lint if not lint.success else result
            except Exception as e:
                logger.debug(f"cfn-lint skipped due to error: {e}")

        explanation = (
            "cdk synth passed ✅" if result.success else f"❌ {result.stderr[:200]}"
        )
        return Score(
            value=CORRECT if result.success else INCORRECT,
            answer="synth-result",
            explanation=explanation,
        )

    return score


def _get_dataset():
    """Load the CDK synth dataset."""
    return json_dataset(
        "cdk_synth.jsonl",
        sample_fields=FieldSpec(input="input", target="target"),
        shuffle=True,
        auto_id=True,
    )


def _get_solver():
    """Configure the solver chain with robust API handling."""
    generate_config = GenerateConfig(
        max_retries=5,  # Retry failed API calls up to 5 times
        timeout=180,  # Increase timeout to 3 minutes
    )
    return [
        chain_of_thought(),
        generate(config=generate_config),
        self_critique(),
    ]


@task
def aws_cdk_synth():
    """CDK synthesis task using Docker sandbox.

    This is the original Docker-based evaluation. May fail in CI environments.
    For CI, use aws_cdk_synth_local() instead.
    """
    return Task(
        dataset=_get_dataset(),
        solver=_get_solver(),
        scorer=cdk_verify(),
        sandbox=("docker", (Path(__file__).parent / "compose.yaml").as_posix()),
    )


@task
def aws_cdk_synth_local():
    """CDK synthesis task using local subprocess execution.

    This variant runs cdk synth directly without Docker, making it more reliable
    in CI environments where Docker-in-Docker is problematic.

    Requires:
        - Node.js and npm install -g aws-cdk
        - pip install cfn-lint (optional, for linting)
    """
    logger.info("Using local execution mode (no Docker sandbox)")
    return Task(
        dataset=_get_dataset(),
        solver=_get_solver(),
        scorer=cdk_verify_local(),
        # No sandbox - runs directly on host
    )
