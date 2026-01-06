# Epic: Reproducibility and CI

## User Value

Anyone can clone the repo and reproduce leaderboard scores on their own machine, building trust in the benchmark's credibility and enabling external validation.

## Success Criteria

- [x] "One-command run" documented and tested (e.g., `make bench` or similar)
- [x] Fresh clone produces scores within documented tolerance (e.g., ±5%)
- [x] CI workflow runs nightly and updates leaderboard artifacts
- [x] Environment setup documented (Python version, dependencies, API keys)
- [x] Reproducibility tested on clean Ubuntu environment (CI validates this)

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

- [x] [001-add-tests-to-ci](../tasks/reproducibility-and-ci-001-add-tests-to-ci.md)
- [x] [002-fix-static-site-html](../tasks/reproducibility-and-ci-002-fix-static-site-html.md)
- [x] [003-add-github-pages-deployment](../tasks/reproducibility-and-ci-003-add-github-pages-deployment.md)
- [x] [004-document-quickstart](../tasks/reproducibility-and-ci-004-document-quickstart.md)
- [x] [005-document-reproducibility-tolerance](../tasks/reproducibility-and-ci-005-document-reproducibility-tolerance.md)

## Status

`Done`
