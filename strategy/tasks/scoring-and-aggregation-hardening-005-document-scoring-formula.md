# Task: Document Scoring Formula

**Epic:** [scoring-and-aggregation-hardening.md](../epics/scoring-and-aggregation-hardening.md)
**Size:** `S`
**Status:** `Done`

## Context

The scoring methodology is not documented anywhere. Users and contributors need to understand how scores are computed to trust the leaderboard. This enforces "Overall score formula is documented and matches implementation".

## Acceptance Criteria

- [ ] `docs/SCORING.md` created with complete methodology documentation
- [ ] Documents each category and what it measures
- [ ] Documents per-category score calculation (accuracy formula)
- [ ] Documents overall score formula (weighted average)
- [ ] Documents weight rationale
- [ ] Link to SCORING.md added to README.md

## Technical Notes

**Relevant Files:**
- `docs/SCORING.md` — New file
- `README.md` — Add link to scoring docs

**Content outline:**
```markdown
# SA Bench Scoring Methodology

## Categories

### Practice Exam (MCQ)
- **What it measures**: AWS certification-style knowledge
- **Scoring**: % correct (1.0 if answer matches, 0.0 otherwise)
- **Weight**: X%

### Architecture Design
- **What it measures**: Architectural reasoning and diagram understanding
- **Scoring**: Rubric-based score in [0,1] from architecture_scorer
- **Weight**: Y%

### CDK Synthesis
- **What it measures**: Infrastructure-as-code generation
- **Scoring**: Pass/fail based on `cdk synth` success
- **Weight**: Z%

## Overall Score

overall = (practice_exam × 0.X) + (architecture_design × 0.Y) + (cdk_synth × 0.Z)

## Interpretation Notes
- Scores range from 0.0 to 1.0
- Missing categories treated as 0
- [Any other important notes]
```

**Gotchas:**
- Keep in sync with actual implementation
- Consider adding examples

## Dependencies

- **Blocked by:** 001 (need final weights to document)
- **Blocks:** None

## Verification

```bash
# Check file exists and has content
test -f docs/SCORING.md && wc -l docs/SCORING.md

# Check README links to it
grep -q "SCORING.md" README.md
```
