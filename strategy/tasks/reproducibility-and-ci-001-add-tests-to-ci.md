# Task: Add Tests to CI Workflow

**Epic:** [reproducibility-and-ci.md](../epics/reproducibility-and-ci.md)
**Size:** `S`
**Status:** `Done`

## Context

Tests exist but aren't run in CI. Adding a test step ensures code quality is validated on every nightly run and catches regressions before they affect leaderboard results.

## Acceptance Criteria

- [ ] CI workflow runs `make test` before benchmark
- [ ] CI fails if tests fail (benchmark doesn't run with broken code)
- [ ] Test results shown in job summary

## Technical Notes

**Relevant Files:**
- `.github/workflows/bench.yaml` — Add test step

**Approach:**
Add a "Run tests" step after "Sync Python deps" and before "Nightly bench run". Use `make test` for consistency with local development.

```yaml
- name: Run tests
  run: make test
```

**Gotchas:**
- Tests should run before benchmark to fail fast
- Consider whether to continue benchmark on test failure (probably not)

## Dependencies

- **Blocked by:** None
- **Blocks:** None

## Verification

```bash
# Trigger workflow manually and verify tests run
gh workflow run bench.yaml
gh run list --workflow=bench.yaml --limit=1
```
