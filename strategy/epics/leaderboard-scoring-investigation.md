# Epic: Leaderboard Scoring Investigation

## User Value

Accurate, trustworthy benchmark scores on current frontier models that users can rely on for model selection decisions. The leaderboard should work correctly and provide meaningful, interpretable results.

## Success Criteria

- [x] Models updated to latest versions (gpt-5.2, claude-sonnet-4.5)
- [x] Log viewer shows only logs for the selected model (bug fix)
- [x] Architecture tasks with images load and display correctly
- [x] Practice exam scores investigated and issues resolved
- [ ] All task types producing meaningful, non-zero scores (pending next run)
- [ ] Fresh benchmark run with verified results (pending)

## Technical Approach

1. Update model configuration to use latest frontier models
2. Debug log viewer filtering to show only selected model's logs
3. Investigate architecture dataset to ensure images are properly embedded/referenced
4. Analyze practice exam logs to understand why scores are 0% and fix underlying issues

## OKR Alignment

- **Objective**: O1 — Build a trustworthy, reproducible evaluation framework
- **Key Result**: KR2 — Publish live leaderboard with accurate scores

## Dependencies

- **Depends on**: public-leaderboard-and-release (leaderboard must exist)
- **Blocks**: credibility-and-distribution (need accurate scores before promoting)
- **Priority**: `High`

## Tasks

- [x] [001-update-models](../tasks/leaderboard-scoring-investigation-001-update-models.md) — Update to latest frontier models (`S`)
- [x] [002-fix-log-viewer-filtering](../tasks/leaderboard-scoring-investigation-002-fix-log-viewer-filtering.md) — Fix log viewer to show only selected model (`M`)
- [x] [003-investigate-architecture-images](../tasks/leaderboard-scoring-investigation-003-investigate-architecture-images.md) — Investigate missing images in architecture tasks (`M`)
- [x] [004-investigate-practice-exam-scores](../tasks/leaderboard-scoring-investigation-004-investigate-practice-exam-scores.md) — Investigate low/zero practice exam scores (`L`)

## Status

`Done`
