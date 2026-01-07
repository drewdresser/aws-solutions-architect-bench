# Task: Create Calibration Test Set and Measure Judge Agreement

**Epic:** [llm-judge-architecture-scoring.md](../epics/llm-judge-architecture-scoring.md)
**Size:** `M`
**Status:** `Done`

## Context

Before deploying LLM-as-judge scoring, we need to validate that the judge produces consistent, reasonable scores. A calibration test set with known-quality responses lets us measure judge reliability and tune prompts until we hit our target agreement rate (>=80%).

## Acceptance Criteria

- [ ] Create calibration dataset with 10-15 sample responses of varying quality
- [ ] Each sample has a "ground truth" score assigned by human review
- [ ] Run judge on calibration set and measure agreement with ground truth
- [ ] Agreement rate >= 80% (within 0.15 of ground truth on each dimension)
- [ ] Document calibration methodology and results
- [ ] Add CI check to run calibration on judge prompt changes

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/calibration/` — New directory for calibration data
- `evals/architecture_design/calibration/responses.jsonl` — Sample responses with ground truth
- `tests/test_judge_calibration.py` — Tests that measure agreement rate
- `docs/SCORING.md` — Document calibration results

**Approach:**

1. **Create Calibration Responses**: For 3-4 subtypes, create:
   - 1 excellent response (target: 0.9+ on all dimensions)
   - 1-2 good responses (target: 0.7-0.85)
   - 1 mediocre response (target: 0.4-0.6)
   - 1 poor response (target: 0.1-0.3)

2. **Ground Truth Assignment**: Manually score each response, documenting reasoning

3. **Agreement Measurement**:
   - Run judge 3 times per sample (measure self-consistency)
   - Compare average judge score to ground truth
   - Report: mean absolute error, correlation, % within tolerance

4. **Tuning Loop**: If agreement < 80%, adjust rubric prompts and re-test

**Calibration Data Format:**
```json
{
  "id": "cal_001",
  "type": "diagram_interpretation",
  "subtype": "service_identification",
  "task_input": "Identify all AWS services in this three-tier architecture...",
  "expected_answer": "EC2, RDS, ELB, VPC, Auto Scaling...",
  "model_response": "The architecture shows Amazon EC2 instances serving as web servers...",
  "ground_truth": {
    "accuracy": 0.85,
    "completeness": 0.80,
    "quality": 0.75,
    "reasoning": "Identified 4/5 services, good role explanations, slightly verbose"
  },
  "quality_tier": "good"
}
```

**Agreement Metrics:**
- **Absolute Agreement**: Judge within ±0.15 of ground truth
- **Ranking Agreement**: Judge correctly orders responses by quality
- **Self-Consistency**: Multiple judge runs produce similar scores (std < 0.1)

**Gotchas:**
- Ground truth is subjective — document reasoning for each score
- Run calibration multiple times to account for judge variance
- Different judge models may need different rubric tuning
- Keep calibration set separate from main eval set

## Dependencies

- **Blocked by:** 001 (needs scorer), 002 (needs rubrics)
- **Blocks:** 005 (need passing calibration before publishing rubrics)

## Verification

```bash
# Run calibration tests
uv run pytest tests/test_judge_calibration.py -v

# Check agreement rate
uv run python scripts/measure_judge_agreement.py

# Output should show:
# Agreement Rate: 82% (target: 80%)
# Mean Absolute Error: 0.12
# Self-Consistency (std): 0.08
```
