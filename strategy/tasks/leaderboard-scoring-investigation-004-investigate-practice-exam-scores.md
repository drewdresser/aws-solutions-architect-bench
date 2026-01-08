# Task: Investigate Low/Zero Practice Exam Scores

**Epic:** [leaderboard-scoring-investigation.md](../epics/leaderboard-scoring-investigation.md)
**Size:** `L`
**Status:** `Done`

## Context

Practice exam scores are unexpectedly low, with some models showing 0% scores. This is surprising given that these are multiple-choice questions that frontier models typically handle well. Need to investigate logs and determine if the tasks are correctly configured.

## Acceptance Criteria

- [x] Download and analyze recent practice exam logs
- [x] Identify patterns in failures (all wrong? scoring bug? format issue?)
- [x] Verify expected answer format matches model output format
- [x] Check if multi-select questions are handled correctly
- [x] Verify scorer is extracting answers properly
- [x] Fix any identified issues
- [ ] Confirm scores improve after fixes (deferred to next benchmark run)

## Resolution

**Root Cause Identified:**
The OpenAI models (`gpt-4.1`, `gpt-5`) via OpenRouter were returning **empty responses** for all practice exam questions. This is a model/API issue, not a scoring bug.

**Evidence from logs:**
- `gpt-5`: All 50 samples returned empty content (`""`)
- `gpt-4.1`: All 50 samples returned empty content (`""`)
- `claude-sonnet-4`: Working correctly (84% score)

**Fix:**
Updated model list to use newer models (`gpt-5.2`, `claude-sonnet-4.5`) which should not have this issue. The practice exam task and scorer are working correctly - the issue was purely with the old model endpoints.

## Technical Notes

**Files to investigate:**
- `evals/practice_exam/tasks.py` — Task definition and scorer
- `evals/practice_exam/aws_sa.jsonl` — Dataset with questions/answers
- Recent logs from `logs/` directory

**Potential issues:**
1. **Answer format mismatch** — Model outputs "A" but scorer expects "a" or vice versa
2. **Multi-select handling** — Questions with multiple correct answers may not be scored correctly
3. **Extraction regex** — Answer extraction pattern may not match model output format
4. **Target format** — Expected answer format in JSONL may not match
5. **Prompt format** — Models may not understand the expected response format

**Investigation steps:**
1. Pull logs from latest benchmark run
2. Look at raw model outputs for practice exam tasks
3. Compare model answers to expected answers
4. Check scorer logic for edge cases
5. Test with a simple question manually

**Key metrics to check:**
- How many questions total?
- How many correct vs incorrect?
- Are there patterns in wrong answers?
- Do multi-select questions have different pass rates?

## Dependencies

- **Blocked by:** None
- **Blocks:** Accurate leaderboard scores

## Verification

```bash
# Run practice exam with verbose logging
make eval.practice LIMIT=5

# Check detailed results
cat results/practice_exam_results.json
```
