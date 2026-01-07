# Task: Add Tests for Weight Normalization

**Epic:** [scoring-and-aggregation-hardening.md](../epics/scoring-and-aggregation-hardening.md)
**Size:** `S`
**Status:** `Done`

## Context

The weight normalization fix needs a regression test to prevent future breakage. This test enforces the success criterion "Weights sum to exactly 1.0 (enforced by test)".

## Acceptance Criteria

- [ ] Test file `tests/test_task_registry.py` created
- [ ] Test `test_weights_sum_to_one()` asserts weights sum to 1.0
- [ ] Test `test_all_weights_positive()` ensures no negative weights
- [ ] Test `test_all_tasks_have_required_fields()` validates registry structure
- [ ] All tests pass

## Technical Notes

**Relevant Files:**
- `tests/test_task_registry.py` — New file
- `scripts/task_registry.py` — Module under test

**Approach:**
```python
import pytest
from scripts.task_registry import TASKS

def test_weights_sum_to_one():
    total = sum(cfg["weight"] for cfg in TASKS.values())
    assert abs(total - 1.0) < 0.0001, f"Weights sum to {total}, expected 1.0"

def test_all_weights_positive():
    for name, cfg in TASKS.items():
        assert cfg["weight"] > 0, f"Task {name} has non-positive weight"

def test_all_tasks_have_required_fields():
    required = {"patterns", "metric", "weight"}
    for name, cfg in TASKS.items():
        missing = required - set(cfg.keys())
        assert not missing, f"Task {name} missing fields: {missing}"
```

**Gotchas:**
- Use `abs(total - 1.0) < epsilon` for float comparison, not `== 1.0`

## Dependencies

- **Blocked by:** 001 (fix weights first), 002 (need pytest)
- **Blocks:** None

## Verification

```bash
uv run pytest tests/test_task_registry.py -v
```
