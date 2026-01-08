# Epic: Category Score Reporting

## User Value

Leaderboard displays per-category scores (MCQ, CDK, Architecture) with clear definitions, enabling users to understand model strengths/weaknesses and make informed comparisons for specific SA tasks.

## Success Criteria

- [x] Per-category scores displayed as first-class output on leaderboard
- [x] Each category has clear definition of what it measures
- [x] Variance estimates or confidence notes included (if feasible)
- [x] Category breakdown visible in both JSON and HTML outputs
- [x] Documentation explains category weights and calculation

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

- [x] [001-enhance-json-schema](../tasks/category-score-reporting-001-enhance-json-schema.md) — Add category metadata to leaderboard JSON (S)
- [x] [002-enhance-ui-display](../tasks/category-score-reporting-002-enhance-ui-display.md) — Enhance UI with tooltips and weight badges (M)
- [x] [003-add-confidence-notes](../tasks/category-score-reporting-003-add-confidence-notes.md) — Add confidence/variance notes (M)
- [x] [004-update-documentation](../tasks/category-score-reporting-004-update-documentation.md) — Update scoring documentation (S)

## Status

`Done`
