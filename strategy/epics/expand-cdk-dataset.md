# Epic: Expand CDK Dataset

## User Value

A larger CDK dataset with domain-tagged prompts provides more comprehensive IaC evaluation, covering the breadth of AWS infrastructure patterns and enabling meaningful CDK capability comparisons.

## Success Criteria

- [ ] CDK track grown from 20 to at least 40 prompts
- [ ] Prompts tagged by domain (networking, serverless, security, data, etc.)
- [ ] Documented "prompt contract" specifying expected output format
- [ ] Reduced ambiguity in prompt requirements
- [ ] Coverage of common CDK patterns (VPC, Lambda, API Gateway, DynamoDB, etc.)

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

<!-- Tasks will be created just-in-time when work begins -->
- [ ] _Tasks to be defined when epic starts_

## Status

`Not Started`
