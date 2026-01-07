# Epic: Public Leaderboard and Release

## User Value

A public, stable URL where practitioners and researchers can view current benchmark results and understand how scores are computed, making SA Bench cite-worthy and usable.

## Success Criteria

- [ ] Leaderboard hosted at stable public URL (GitHub Pages)
- [ ] "How scores are computed" documentation visible on leaderboard page
- [ ] v0.1 release tag created with release notes
- [ ] Leaderboard displays category-level scores (not just overall)
- [ ] Mobile-responsive leaderboard design
- [ ] Last-updated timestamp visible on leaderboard

## Technical Approach

Enhance `docs/index.html` to show methodology and category breakdowns. Set up GitHub Pages deployment in CI. Create release automation or documented release process. Add metadata (timestamp, run info) to leaderboard JSON.

## OKR Alignment

- **Objective**: O1 — Ship SA Bench v0.1 as a credible, reproducible public benchmark
- **Key Result**: KR2 — Host leaderboard publicly with stable URL and documentation

## Dependencies

- **Depends on**: scoring-and-aggregation-hardening, reproducibility-and-ci
- **Blocks**: launch-post-and-positioning (need something to launch)
- **Priority**: `High`

## Tasks

- [x] [001-add-timestamp-metadata](../tasks/public-leaderboard-and-release-001-add-timestamp-metadata.md) — Add generated_at timestamp to leaderboard JSON
- [x] [002-enhance-leaderboard-ui](../tasks/public-leaderboard-and-release-002-enhance-leaderboard-ui.md) — Category score highlighting and mobile support
- [x] [003-expand-methodology-section](../tasks/public-leaderboard-and-release-003-expand-methodology-section.md) — Detailed methodology on leaderboard page
- [ ] [004-create-v01-release](../tasks/public-leaderboard-and-release-004-create-v01-release.md) — Create Git tag and GitHub Release
- [x] [005-verify-github-pages-url](../tasks/public-leaderboard-and-release-005-verify-github-pages-url.md) — Verify deployment and document URL

## Status

`In Progress`
