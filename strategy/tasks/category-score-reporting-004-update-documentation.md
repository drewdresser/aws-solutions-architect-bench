# Task: Update Scoring Documentation

**Epic:** [category-score-reporting.md](../epics/category-score-reporting.md)
**Size:** `S`
**Status:** `Done`

## Context

With enhanced category reporting, the scoring documentation needs updates to explain the new metadata fields, confidence notes, and how users should interpret per-category scores.

## Acceptance Criteria

- [x] `docs/SCORING.md` updated with category metadata explanation
- [x] Confidence/variance methodology documented
- [x] Per-category scoring details enhanced
- [x] JSON schema changes documented
- [x] README links to scoring docs (if not already)

## Technical Notes

**Target Files:**
- `docs/SCORING.md` — Main scoring documentation
- `docs/ARCHITECTURE_SCORING.md` — Architecture-specific details (may need updates)
- `README.md` — Ensure links to scoring docs

**Sections to Add/Update in SCORING.md:**

```markdown
## Category Score Details

### Practice Exam (34%)
- **What it measures**: AWS certification-style knowledge
- **Scoring**: Binary (correct/incorrect)
- **Sample size**: 50 questions
- **Expected variance**: ±5%

### Architecture Design (33%)
- **What it measures**: Architectural reasoning and diagram interpretation
- **Scoring**: Rubric-based (accuracy, completeness, quality)
- **Sample size**: 28 tasks
- **Expected variance**: ±10% (LLM judge non-determinism)

### CDK Synthesis (33%)
- **What it measures**: Infrastructure-as-code generation
- **Scoring**: Binary (synth succeeds/fails)
- **Sample size**: 40 prompts
- **Expected variance**: ±5%

## Understanding Score Variance

Scores may vary between runs due to:
1. **LLM non-determinism**: Models may give different responses
2. **API routing**: Provider may route to different model instances
3. **Judge variance**: Architecture scoring uses LLM-as-judge

### Interpreting Close Scores

When models score within 5% of each other:
- Consider them **statistically equivalent**
- Focus on category-level differences for insights
- Re-run benchmark for validation if needed

## JSON Schema

The leaderboard JSON includes category metadata:

```json
{
  "_metadata": {
    "categories": {
      "practice_exam": {
        "name": "Practice Exam",
        "description": "...",
        "weight": 0.34,
        "sample_count": 50,
        "confidence": "high",
        "margin": "±5%"
      }
    }
  }
}
```
```

**Approach:**
1. Review current SCORING.md content
2. Add category details section
3. Add variance/confidence explanation
4. Add JSON schema documentation
5. Cross-reference from README if needed

**Gotchas:**
- Keep documentation accessible to non-technical readers
- Don't over-promise precision
- Include examples of how to interpret scores

## Dependencies

- **Blocked by:** Tasks 001, 003 (document what was implemented)
- **Blocks:** None (final documentation task)

## Verification

```bash
# Check documentation exists and has new sections
grep -E "Category Score|Variance|Confidence" docs/SCORING.md

# Verify links work
grep -l "SCORING.md" README.md docs/*.md
```
