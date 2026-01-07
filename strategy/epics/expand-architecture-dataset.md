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

- [ ] [001-create-generation-script](../tasks/expand-architecture-dataset-001-create-generation-script.md) — Create PEP723 script using OpenAI API to generate items
- [ ] [002-expand-interpretation-items](../tasks/expand-architecture-dataset-002-expand-interpretation-items.md) — Generate 6-8 new diagram interpretation items
- [ ] [003-expand-creation-items](../tasks/expand-architecture-dataset-003-expand-creation-items.md) — Generate 5-6 new diagram creation items
- [ ] [004-add-critique-subtype](../tasks/expand-architecture-dataset-004-add-critique-subtype.md) — Add architecture critique/tradeoff analysis subtype with 3-4 items
- [ ] [005-review-and-tag](../tasks/expand-architecture-dataset-005-review-and-tag.md) — Review, validate, and add consistent tagging to all items

## Status

`In Progress`
