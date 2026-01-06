# Task: Document Reproducibility Tolerance

**Epic:** [reproducibility-and-ci.md](../epics/reproducibility-and-ci.md)
**Size:** `S`
**Status:** `Done`

## Context

The OKR mentions "within a defined tolerance (e.g., ±X%)". We need to document what variance is expected between runs due to LLM non-determinism and establish acceptable bounds.

## Acceptance Criteria

- [ ] Reproducibility tolerance documented in docs/SCORING.md
- [ ] Explanation of why scores vary (LLM temperature, non-determinism)
- [ ] Recommended settings for maximum reproducibility (temperature=0 if supported)
- [ ] Expected variance range stated (e.g., "±5% for MCQ, ±10% for architecture")

## Technical Notes

**Relevant Files:**
- `docs/SCORING.md` — Add reproducibility section

**Content to add:**
```markdown
## Reproducibility

### Expected Variance

Due to LLM non-determinism, scores may vary between runs:
- **Practice Exam (MCQ)**: ±2-5% (discrete answers, low variance)
- **Architecture Design**: ±5-10% (rubric scoring, moderate variance)
- **CDK Synthesis**: ±5% (binary pass/fail, but extraction varies)

### Maximizing Reproducibility

- Use `temperature=0` when supported by the model
- Run full dataset (no `--limit`) for stable averages
- Use same model version (pin to specific model IDs)

### Tolerance for Leaderboard

A fresh run is considered reproducible if overall scores are within ±5% of published leaderboard values.
```

**Gotchas:**
- Different models have different variance characteristics
- Actual variance should be measured empirically over time

## Dependencies

- **Blocked by:** None
- **Blocks:** None

## Verification

```bash
# Run benchmark twice and compare scores
# Verify variance is within documented tolerance
```
