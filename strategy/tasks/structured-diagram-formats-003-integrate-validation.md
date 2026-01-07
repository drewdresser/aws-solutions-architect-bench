# Task: Integrate Validation into Scorer Pipeline

**Epic:** [structured-diagram-formats-and-validation.md](../epics/structured-diagram-formats-and-validation.md)
**Size:** `M`
**Status:** `Done`

## Context

With parsers in place, we need to integrate structural validation into the architecture scoring pipeline. Responses that fail to parse should receive reduced scores, while valid structured outputs get a validation bonus.

## Acceptance Criteria

- [ ] Add `validate_structured_output()` function that detects and validates format
- [ ] Integrate validation into `llm_judge_scorer()` as a pre-check
- [ ] Validation result affects final score (bonus for valid, penalty for invalid when format required)
- [ ] Track validation results in score metadata
- [ ] Update scoring to handle new `output_format` field in dataset items
- [ ] Add tests for scoring with validation

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/tasks.py` — Integrate validation into scorer
- `evals/architecture_design/diagram_validators.py` — Import validators
- `tests/test_llm_judge_scorer.py` — Add validation integration tests

**Approach:**
1. Create `validate_structured_output(response, required_format)` dispatcher
2. In scorer, check if dataset item specifies `output_format`
3. If format specified, run validation before LLM judging
4. Apply score modifier based on validation result:
   - Valid + parseable: +5% bonus to quality score
   - Invalid when required: -20% penalty to overall score
   - No format required: no modifier

**Score Modification Logic:**
```python
def apply_validation_modifier(scores, validation_result, format_required):
    if not format_required:
        return scores  # No modification

    if validation_result.is_valid:
        scores['quality'] = min(1.0, scores['quality'] * 1.05)  # 5% bonus
    else:
        # Apply penalty to all dimensions
        penalty = 0.8  # 20% reduction
        scores = {k: v * penalty for k, v in scores.items()}

    return scores
```

**Metadata to Track:**
- `validation_attempted`: bool
- `validation_format`: str (mermaid/plantuml/json/none)
- `validation_passed`: bool
- `validation_error`: str | None

**Gotchas:**
- Don't penalize interpretation tasks (only creation tasks have format requirements)
- Handle cases where model doesn't produce the requested format at all
- Validation should be lenient — focus on parseability, not perfection

## Dependencies

- **Blocked by:** 001, 002 (needs parsers)
- **Blocks:** 004 (dataset needs scorer support first)

## Verification

```bash
uv run pytest tests/test_llm_judge_scorer.py -v -k validation
```
