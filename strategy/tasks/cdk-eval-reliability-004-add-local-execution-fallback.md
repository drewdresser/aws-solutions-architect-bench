# Task: Add Local Execution Fallback for CI

**Epic:** [cdk-eval-reliability.md](../epics/cdk-eval-reliability.md)
**Size:** `L`
**Status:** `Todo`

## Context

Per user feedback, CDK eval works locally but fails in GitHub Actions. The Docker sandbox approach may be unreliable in CI. Adding a local execution fallback (using subprocess instead of Docker) would improve CI reliability.

## Acceptance Criteria

- [ ] New scorer variant that uses subprocess instead of Docker sandbox
- [ ] CI workflow installs CDK dependencies (Node.js, aws-cdk, aws-cdk-lib)
- [ ] Fallback triggered automatically when sandbox fails OR via environment variable
- [ ] Same scoring logic (cdk synth + optional cfn-lint) preserved
- [ ] Performance acceptable (local may be faster than Docker startup)

## Technical Notes

**Relevant Files:**
- `evals/cdk_synth/tasks.py` — Current sandbox-based scorer
- `.github/workflows/bench.yaml` — CI environment setup

**Approach:**
Create a new scorer `cdk_verify_local()` that uses subprocess:

```python
import subprocess
import tempfile

@scorer(metrics=[mean()])
def cdk_verify_local():
    async def score(state, target):
        code_raw = state.output.completion
        src = _extract_code(code_raw)

        # Use tempfile for cross-platform compatibility
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            _write_project(src, tmp_path)

            try:
                result = subprocess.run(
                    ["cdk", "synth"],
                    cwd=str(tmp_path),
                    capture_output=True,
                    text=True,
                    timeout=VERIFY_TIMEOUT,
                    env={**os.environ, "CDK_DEFAULT_ACCOUNT": "123456789012", "CDK_DEFAULT_REGION": "us-east-1"}
                )
                success = result.returncode == 0
                stderr = result.stderr
            except subprocess.TimeoutExpired:
                success = False
                stderr = "cdk synth timed-out"
            except FileNotFoundError:
                success = False
                stderr = "cdk command not found - install with: npm install -g aws-cdk"

        # ... rest of scoring logic
    return score
```

**CI setup additions:**
```yaml
- name: Install CDK for local execution
  run: |
    npm install -g aws-cdk
    pip install aws-cdk-lib constructs cfn-lint
```

**Task variant selection:**
- `tasks.py` — Uses Docker sandbox (original)
- `tasks_local.py` — Uses subprocess (new, CI-friendly)
- Or: single file with env var `CDK_EVAL_MODE=local|docker`

**Gotchas:**
- Need to set CDK environment variables (account/region) for synth to work
- cfn-lint must also be installed locally
- tempfile cleanup is automatic with context manager
- Windows compatibility if anyone runs locally on Windows

## Dependencies

- **Blocked by:** 001 (need working task structure)
- **Blocks:** None

## Verification

```bash
# Test locally without Docker
CDK_EVAL_MODE=local make eval.cdk LIMIT=2

# Verify CI has required tools
gh workflow run bench.yaml
# Check logs for CDK execution
```
