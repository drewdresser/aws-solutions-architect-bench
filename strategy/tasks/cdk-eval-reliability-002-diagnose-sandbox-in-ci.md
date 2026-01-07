# Task: Diagnose Docker Sandbox Execution in CI

**Epic:** [cdk-eval-reliability.md](../epics/cdk-eval-reliability.md)
**Size:** `M`
**Status:** `Done`

## Context

Even when the correct task file is used, the CDK eval may fail in GitHub Actions due to Docker sandbox issues. The scorer uses `sandbox().exec()` which depends on Docker compose starting a container with `/tmp` mounted.

## Acceptance Criteria

- [ ] Document whether Docker is available in GitHub Actions runner
- [ ] Verify compose.yaml works in CI environment
- [ ] Add diagnostic logging to identify where sandbox execution fails
- [ ] Either fix sandbox execution OR implement a non-Docker fallback

## Technical Notes

**Relevant Files:**
- `evals/cdk_synth/tasks.py` — Uses `sandbox=("docker", ...)` configuration
- `evals/cdk_synth/compose.yaml` — Mounts `/tmp:/tmp`, uses `network_mode: none`
- `.github/workflows/bench.yaml` — CI environment

**Current sandbox flow:**
1. Model generates CDK code
2. Scorer extracts code via regex
3. Scorer writes code to `/tmp/<uuid>/app.py` on HOST
4. Scorer calls `sandbox().exec(["bash", "-c", "cdk synth"], cwd=str(tmp))`
5. Docker container executes command with `/tmp` mounted

**Potential CI issues:**
- Docker may not be pre-installed or configured
- `/tmp` path may differ between host and container in CI
- Container may timeout or fail to start
- Memory limits (2GB) may be insufficient

**Approach:**
1. Add verbose logging to sandbox execution
2. Test with `workflow_dispatch` trigger to debug interactively
3. Consider switching to local execution (no sandbox) if Docker unreliable in CI

**Alternative: Local execution scorer**
```python
# Instead of sandbox().exec(), use subprocess directly
import subprocess
result = subprocess.run(["cdk", "synth"], cwd=str(tmp), capture_output=True, timeout=60)
```

This requires CDK to be installed in the CI environment but avoids Docker-in-Docker issues.

**Gotchas:**
- GitHub Actions runners have Docker but may have different defaults
- The `network_mode: none` may cause issues
- Inspect AI's sandbox API may have CI-specific configurations we're not using

## Dependencies

- **Blocked by:** 001 (need working task file first)
- **Blocks:** None

## Verification

```bash
# Trigger manual workflow run
gh workflow run bench.yaml

# Check workflow logs for Docker/sandbox errors
gh run view --log

# Test locally with same commands CI uses
make bench.daily LIMIT=1
```
