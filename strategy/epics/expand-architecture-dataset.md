# Epic: Expand Architecture Dataset

## User Value

A larger architecture dataset with diverse task types provides more comprehensive evaluation of model architectural reasoning, with enough items for statistically meaningful category scores.

## Success Criteria

- [ ] Architecture track grown from 8 to at least 20 items
- [ ] Balanced coverage: diagram understanding, diagram generation, critique/tradeoff analysis
- [ ] Items tagged by subtype and complexity
- [ ] Diverse AWS service coverage (not just EC2/S3/Lambda)
- [ ] Include multi-service integration scenarios

## Technical Approach

Add new items to `evals/architecture_design/architecture_interpretation.jsonl`. Create additional diagrams or textual architecture descriptions. Balance across subtypes. Ensure new items align with structured format requirements (if structured-diagram-formats epic is complete).

## OKR Alignment

- **Objective**: O3 — Expand task coverage and stabilize category scores
- **Key Result**: KR2 — Grow Architecture track from ~8 to at least [N] items

## Dependencies

- **Depends on**: structured-diagram-formats-and-validation (new items should use standard formats)
- **Blocks**: category-score-reporting (need enough data for stable scores)
- **Priority**: `Medium`

## Tasks

<!-- Tasks will be created just-in-time when work begins -->
- [ ] _Tasks to be defined when epic starts_

## Status

`Not Started`
