# Task: Fix Log Viewer to Show Only Selected Model

**Epic:** [leaderboard-scoring-investigation.md](../epics/leaderboard-scoring-investigation.md)
**Size:** `M`
**Status:** `Not Started`

## Context

When clicking on a model name in the leaderboard to view its logs, the log viewer currently shows logs from all models instead of filtering to show only the selected model's logs. This makes it difficult to inspect a specific model's performance.

## Acceptance Criteria

- [ ] Clicking a model name shows only that model's logs
- [ ] Log list is filtered by model name/ID
- [ ] Back button or breadcrumb to return to full leaderboard
- [ ] Model name clearly displayed in log viewer header
- [ ] Works correctly for all models in the leaderboard

## Technical Notes

**Files to investigate:**
- `docs/index.html` — Leaderboard UI with model links
- `scripts/bundle_logs.sh` — Log bundling script
- `docs/logs/` — Bundled log structure

**Possible causes:**
1. Log bundling doesn't separate by model
2. Frontend filtering not implemented
3. URL parameters not being used to filter

**Approach:**
1. Check how logs are currently bundled (by model? by run?)
2. Verify the link URL contains model identifier
3. Add frontend JavaScript to filter logs by model
4. Or restructure log bundles to be per-model

## Dependencies

- **Blocked by:** None
- **Blocks:** None (UX improvement)

## Verification

```bash
# After fix, click on a model in the leaderboard
# Should only see logs from that model
```
