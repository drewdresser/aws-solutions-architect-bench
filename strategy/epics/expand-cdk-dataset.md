# Epic: Expand CDK Dataset

## User Value

A larger CDK dataset with domain-tagged prompts provides more comprehensive IaC evaluation, covering the breadth of AWS infrastructure patterns and enabling meaningful CDK capability comparisons.

## Success Criteria

- [x] CDK track grown from 20 to at least 40 prompts
- [x] Prompts tagged by domain (networking, serverless, security, data, etc.)
- [x] Documented "prompt contract" specifying expected output format
- [x] Reduced ambiguity in prompt requirements
- [x] Coverage of common CDK patterns (VPC, Lambda, API Gateway, DynamoDB, etc.)

## Technical Approach

Add new prompts to `evals/cdk_synth/cdk_synth.jsonl`. Define clear prompt contract (what inputs are given, what outputs are expected). Tag prompts by AWS domain. Ensure prompts have unambiguous requirements that can be verified by `cdk synth`.

## OKR Alignment

- **Objective**: O3 — Expand task coverage and stabilize category scores
- **Key Result**: KR3 — Grow CDK track from ~20 to at least [N] prompts with tagging

## Dependencies

- **Depends on**: cdk-eval-reliability (fix scoring before expanding)
- **Blocks**: category-score-reporting (need enough data for stable scores)
- **Priority**: `Low`

## Tasks

- [x] [001-create-generation-script](../tasks/expand-cdk-dataset-001-create-generation-script.md) — Create CDK item generation script (M)
- [x] [002-expand-beginner-items](../tasks/expand-cdk-dataset-002-expand-beginner-items.md) — Generate 10 beginner-level items (M)
- [x] [003-expand-advanced-items](../tasks/expand-cdk-dataset-003-expand-advanced-items.md) — Generate 10 advanced-level items (M)
- [x] [004-add-metadata-to-existing](../tasks/expand-cdk-dataset-004-add-metadata-to-existing.md) — Add metadata to existing 20 items (S)
- [x] [005-review-and-document](../tasks/expand-cdk-dataset-005-review-and-document.md) — Review dataset and document prompt contract (S)

## Status

`Done`
