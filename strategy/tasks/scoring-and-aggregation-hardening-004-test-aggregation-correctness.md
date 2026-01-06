# Task: Add Tests for Aggregation Correctness

**Epic:** [scoring-and-aggregation-hardening.md](../epics/scoring-and-aggregation-hardening.md)
**Size:** `M`
**Status:** `Todo`

## Context

The aggregation logic in `aggregate_multi.py` needs tests to verify that per-category scores and overall scores are calculated correctly. This enforces "Test suite validates aggregation correctness on sample data".

## Acceptance Criteria

- [ ] Test file `tests/test_aggregate_multi.py` created
- [ ] Test with mock sample data verifies per-category accuracy calculation
- [ ] Test verifies overall score = weighted sum of category scores
- [ ] Test verifies handling of missing categories (fillna(0))
- [ ] Test verifies duplicate log handling (mean aggregation)
- [ ] All tests pass

## Technical Notes

**Relevant Files:**
- `tests/test_aggregate_multi.py` — New file
- `scripts/aggregate_multi.py` — Module under test

**Approach:**
Create mock data structures that mimic Inspect log sample summaries. Test the `metric_value()` function directly with various score formats. Test `collect()` with a list of mock log paths (may need to mock file reading).

**Key functions to test:**
- `metric_value(sample, task_cfg)` — Core scoring logic
- `summarise_log(path)` — Per-log summarization (needs mocking)
- `collect(files)` — Full aggregation pipeline

**Test cases:**
1. Simple case: 3 models, 3 tasks, all scores present
2. Missing category: model has no CDK scores → should be 0
3. Duplicate logs: same model+task appears twice → should average
4. Edge case: all zeros
5. Edge case: all perfect scores

**Gotchas:**
- May need to mock `read_eval_log_sample_summaries` from inspect_ai
- Consider using pytest fixtures for reusable mock data

## Dependencies

- **Blocked by:** 001 (need correct weights), 002 (need pytest)
- **Blocks:** None

## Verification

```bash
uv run pytest tests/test_aggregate_multi.py -v
```
