# Epic: Scoring and Aggregation Hardening

## User Value

Ensures leaderboard scores are mathematically correct and trustworthy, so users can confidently compare model performance without questioning the validity of the numbers.

## Success Criteria

- [ ] Weights across all categories sum to exactly 1.0 (enforced by test)
- [ ] Per-category scores match documented calculation methods
- [ ] Overall score formula is documented and matches implementation
- [ ] Test suite validates aggregation correctness on sample data
- [ ] `leaderboard.json` schema is documented and validated

## Technical Approach

Audit `scripts/aggregate_multi.py` and related aggregation code. Add unit tests that verify weight normalization and score calculation. Document the scoring formula in a visible location (README or dedicated doc). Add JSON schema validation for leaderboard output.

## OKR Alignment

- **Objective**: O1 — Ship SA Bench v0.1 as a credible, reproducible public benchmark
- **Key Result**: KR4 — Fix benchmark aggregation correctness

## Dependencies

- **Depends on**: None
- **Blocks**: public-leaderboard-and-release (scores must be correct before public launch)
- **Priority**: `High`

## Tasks

<!-- Tasks will be created just-in-time when work begins -->
- [ ] _Tasks to be defined when epic starts_

## Status

`Not Started`
