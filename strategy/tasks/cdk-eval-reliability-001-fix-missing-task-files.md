# Task: Fix Missing CDK Task Files

**Epic:** [cdk-eval-reliability.md](../epics/cdk-eval-reliability.md)
**Size:** `S`
**Status:** `Done`

## Context

The Makefile references `tasks_no_critique.py` and `tasks_robust.py` which don't exist, causing `make bench.daily` to silently fail for CDK evals. This is why CDK scores are 0% - the eval never runs.

## Acceptance Criteria

- [x] Either create the missing task files OR update Makefile to use existing `tasks.py`
- [x] `make bench.daily --dry-run` shows valid file paths
- [x] CDK task can be imported without errors: `uv run python -c "from evals.cdk_synth.tasks import aws_cdk_synth"`
- [x] CI workflow produces non-zero scores for all three eval tracks (verified in run 20753351490)

## Technical Notes

**Relevant Files:**
- `Makefile` — Line 24: `CDK_TASK ?= evals/cdk_synth/tasks_no_critique.py` (doesn't exist)
- `Makefile` — Line 96: `bench.daily` uses `tasks_robust.py` (doesn't exist)
- `evals/cdk_synth/tasks.py` — Only task file that exists
- `evals/cdk_synth/README.md` — Documents three variants that should exist

**Approach:**
Option A (Simpler): Update Makefile to use `tasks.py` as the default
Option B (Per README): Create `tasks_no_critique.py` and `tasks_robust.py` as described in README.md

Recommend Option A first to unblock, then Option B if robust error handling is needed.

**Gotchas:**
- The README describes API error handling variants that may be valuable for CI reliability
- Inspect AI may fail silently when task file doesn't exist

## Dependencies

- **Blocked by:** None
- **Blocks:** All other CDK tasks (nothing works until this is fixed)

## Verification

```bash
# Verify task file exists
ls evals/cdk_synth/$(grep CDK_TASK Makefile | head -1 | cut -d= -f2 | tr -d ' ')

# Verify import works
uv run python -c "from evals.cdk_synth.tasks import aws_cdk_synth; print('OK')"

# Dry run should show valid paths
make bench.daily --dry-run
```
