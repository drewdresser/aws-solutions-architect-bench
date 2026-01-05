# Epic: Reproducibility and CI

## User Value

Anyone can clone the repo and reproduce leaderboard scores on their own machine, building trust in the benchmark's credibility and enabling external validation.

## Success Criteria

- [ ] "One-command run" documented and tested (e.g., `make bench` or similar)
- [ ] Fresh clone produces scores within documented tolerance (e.g., ±X%)
- [ ] CI workflow runs nightly and updates leaderboard artifacts
- [ ] Environment setup documented (Python version, dependencies, API keys)
- [ ] Reproducibility tested on clean Ubuntu environment (CI validates this)

## Technical Approach

Enhance existing `.github/workflows/bench.yaml` to be more robust. Add a documented "quickstart" section to README. Ensure `uv sync` and environment setup are idempotent. Consider adding a reproducibility test that compares scores across runs.

## OKR Alignment

- **Objective**: O1 — Ship SA Bench v0.1 as a credible, reproducible public benchmark
- **Key Result**: KR1 — Publish a public benchmark release with "one-command run" path
- **Key Result**: KR3 — Add CI automation for repeatable runs

## Dependencies

- **Depends on**: scoring-and-aggregation-hardening (CI should produce correct scores)
- **Blocks**: public-leaderboard-and-release (reproducibility needed before launch)
- **Priority**: `High`

## Tasks

<!-- Tasks will be created just-in-time when work begins -->
- [ ] _Tasks to be defined when epic starts_

## Status

`Not Started`
