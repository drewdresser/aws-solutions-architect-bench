# Task: Add Confidence Notes to Leaderboard

**Epic:** [category-score-reporting.md](../epics/category-score-reporting.md)
**Size:** `M`
**Status:** `Done`

## Context

Users need to understand the reliability of scores. While computing true confidence intervals requires multiple runs, we can provide useful confidence notes based on sample size and scoring method. This helps users interpret close scores correctly.

## Acceptance Criteria

- [x] Per-category confidence notes added to JSON metadata
- [x] UI displays confidence indication (e.g., "±2%" or "High/Medium/Low")
- [x] Methodology section explains confidence calculation
- [x] Documentation updated with confidence methodology

## Technical Notes

**Target Files:**
- `scripts/aggregate_multi.py` — Add confidence metadata
- `docs/index.html` — Display confidence notes
- `docs/SCORING.md` — Document methodology

**Confidence Calculation Approach:**

For binary scoring (MCQ, CDK), use binomial proportion confidence interval:
```python
# Standard error for proportion
se = sqrt(p * (1-p) / n)
# 95% CI margin of error
margin = 1.96 * se

# Example: 80% accuracy on 50 items
# se = sqrt(0.8 * 0.2 / 50) = 0.057
# margin = 1.96 * 0.057 = ±11%
```

For rubric scoring (Architecture), variance is higher due to:
- LLM judge non-determinism
- Subjective criteria interpretation

Simplified approach (avoid complex stats):
```json
{
  "practice_exam": {
    "confidence": "high",
    "margin": "±5%",
    "note": "Binary scoring on 50 items"
  },
  "architecture_design": {
    "confidence": "medium",
    "margin": "±10%",
    "note": "Rubric-based scoring with LLM judge"
  },
  "cdk_synth": {
    "confidence": "high",
    "margin": "±5%",
    "note": "Binary pass/fail on 40 items"
  }
}
```

**UI Display Options:**

Option A: Margin in score cells
```
85.0% ±5%
```

Option B: Confidence badge on header
```
Practice Exam [High Confidence]
```

Option C: Tooltip only (less cluttered)
```
(hover) "Scores typically vary ±5% between runs"
```

**Recommended: Option C** (tooltips) with Option A available for detail view

**Approach:**
1. Add `confidence` field to category metadata in aggregate_multi.py
2. Calculate simple margin based on sample size and scoring type
3. Update UI to show confidence in tooltips
4. Add footnote explaining what confidence means
5. Update SCORING.md with confidence methodology

**Gotchas:**
- Don't overclaim precision — these are estimates, not rigorous CIs
- Make clear this is expected variance, not statistical confidence
- Keep terminology accessible (avoid "confidence interval" jargon)

## Dependencies

- **Blocked by:** Task 001 (builds on category metadata)
- **Blocks:** None

## Verification

```bash
# Check confidence in JSON
make board.json
cat results/leaderboard.json | jq '._metadata.categories.practice_exam.confidence'

# Manual: verify tooltips show confidence info
python -m http.server 8000 --directory docs
```
