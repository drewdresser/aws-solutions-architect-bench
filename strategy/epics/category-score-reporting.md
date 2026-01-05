# Epic: Category Score Reporting

## User Value

Leaderboard displays per-category scores (MCQ, CDK, Architecture) with clear definitions, enabling users to understand model strengths/weaknesses and make informed comparisons for specific SA tasks.

## Success Criteria

- [ ] Per-category scores displayed as first-class output on leaderboard
- [ ] Each category has clear definition of what it measures
- [ ] Variance estimates or confidence notes included (if feasible)
- [ ] Category breakdown visible in both JSON and HTML outputs
- [ ] Documentation explains category weights and calculation

## Technical Approach

Enhance `scripts/aggregate_multi.py` to output per-category breakdowns. Update `docs/index.html` to display category scores prominently. Add category descriptions to leaderboard UI. Consider adding confidence intervals based on sample size.

## OKR Alignment

- **Objective**: O3 — Expand task coverage and stabilize category scores
- **Key Result**: KR4 — Publish category-level score reporting as first-class output

## Dependencies

- **Depends on**: expand-mcq-dataset, expand-architecture-dataset, expand-cdk-dataset (need enough items per category)
- **Blocks**: None
- **Priority**: `Medium`

## Tasks

<!-- Tasks will be created just-in-time when work begins -->
- [ ] _Tasks to be defined when epic starts_

## Status

`Not Started`
