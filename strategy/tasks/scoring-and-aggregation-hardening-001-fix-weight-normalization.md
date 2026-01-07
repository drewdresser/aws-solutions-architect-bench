# Task: Fix Weight Normalization in Task Registry

**Epic:** [scoring-and-aggregation-hardening.md](../epics/scoring-and-aggregation-hardening.md)
**Size:** `S`
**Status:** `Done`

## Context

The task registry defines weights that sum to 1.6 (0.4 + 0.6 + 0.6), not 1.0. This means the "overall" score is not a proper weighted average—it's inflated when all categories have data. This is the core bug this epic addresses.

## Acceptance Criteria

- [ ] Weights in `scripts/task_registry.py` sum to exactly 1.0
- [ ] Weight values are documented with rationale (why each category has its weight)
- [ ] Add a comment block explaining the weight scheme

## Technical Notes

**Relevant Files:**
- `scripts/task_registry.py` — Contains TASKS dict with weights

**Approach:**
Decide on proper weight distribution (e.g., 0.33/0.33/0.34 for equal, or weighted by importance). Update the values. Add inline documentation explaining the rationale.

**Current state:**
```python
"practice_exam": {"weight": 0.4},      # MCQ
"architecture_design": {"weight": 0.6}, # Architecture
"cdk_synth": {"weight": 0.6},          # CDK
# Total: 1.6 (BUG)
```

**Gotchas:**
- Consider whether CDK should have reduced weight given its 0% pass rate issue
- May want to discuss weight rationale with stakeholders before finalizing

## Dependencies

- **Blocked by:** None
- **Blocks:** 002 (tests should verify the fix)

## Verification

```bash
# After fix, this should show weights summing to 1.0
python -c "from scripts.task_registry import TASKS; print(sum(t['weight'] for t in TASKS.values()))"
```
