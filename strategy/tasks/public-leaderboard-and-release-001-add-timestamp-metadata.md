# Task: Add Last-Updated Timestamp to Leaderboard

**Epic:** [public-leaderboard-and-release.md](../epics/public-leaderboard-and-release.md)
**Size:** `S`
**Status:** `Done`

## Context

The leaderboard page currently shows a static "Updated from nightly CI" message. To build credibility and trust, users need to see the actual date/time when scores were generated. This requires adding metadata to `leaderboard.json` during aggregation and displaying it in the UI.

## Acceptance Criteria

- [ ] `leaderboard.json` includes `_metadata` object with `generated_at` ISO timestamp
- [ ] `leaderboard.json` includes `_metadata.run_id` (GitHub run ID if available, or local timestamp)
- [ ] `docs/index.html` displays the timestamp in human-readable format
- [ ] Timestamp updates correctly on each CI run
- [ ] Schema validation allows the new metadata field

## Technical Notes

**Relevant Files:**
- `scripts/aggregate_multi.py` — Add metadata to JSON output
- `docs/index.html` — Display timestamp from JSON
- `schemas/leaderboard.schema.json` — Update schema to allow metadata

**Approach:**
1. Modify `aggregate_multi.py` to wrap output in `{ "_metadata": {...}, "models": [...] }` OR add metadata as special entry
2. Include `generated_at`, `run_id` (from env var `GITHUB_RUN_ID` or generate locally)
3. Update `index.html` JS to extract and display timestamp
4. Update schema to accept the new structure (or use `additionalProperties: true`)

**Gotchas:**
- Don't break existing consumers expecting a flat array — consider backwards compatibility
- Alternative: Keep array but add metadata to each row, or use separate metadata file
- Time zones: Use ISO 8601 format with UTC

## Dependencies

- **Blocked by:** None
- **Blocks:** None (but 002 will use this timestamp)

## Verification

```bash
# Generate leaderboard and check for metadata
make board.json
cat results/leaderboard.json | jq '._metadata'
# Should show: { "generated_at": "2026-01-...", "run_id": "..." }
```
