# Task: Investigate Low/Zero Practice Exam Scores

**Epic:** [leaderboard-scoring-investigation.md](../epics/leaderboard-scoring-investigation.md)
**Size:** `L`
**Status:** `Not Started`

## Context

Practice exam scores are unexpectedly low, with some models showing 0% scores. This is surprising given that these are multiple-choice questions that frontier models typically handle well. Need to investigate logs and determine if the tasks are correctly configured.

## Acceptance Criteria

- [ ] Download and analyze recent practice exam logs
- [ ] Identify patterns in failures (all wrong? scoring bug? format issue?)
- [ ] Verify expected answer format matches model output format
- [ ] Check if multi-select questions are handled correctly
- [ ] Verify scorer is extracting answers properly
- [ ] Fix any identified issues
- [ ] Confirm scores improve after fixes

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
