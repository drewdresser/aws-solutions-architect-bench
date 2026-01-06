# Task: Fix Static Site HTML in CI

**Epic:** [reproducibility-and-ci.md](../epics/reproducibility-and-ci.md)
**Size:** `S`
**Status:** `Done`

## Context

The inline HTML in the CI workflow for the static site is truncated/incomplete. The JavaScript for loading and rendering the CSV is cut off, which would cause the deployed leaderboard page to not work properly.

## Acceptance Criteria

- [ ] Static site HTML is complete and valid
- [ ] JavaScript properly loads and renders leaderboard.csv
- [ ] Table is sortable by clicking headers
- [ ] Page displays "last updated" timestamp
- [ ] Move HTML to a separate template file for maintainability

## Technical Notes

**Relevant Files:**
- `.github/workflows/bench.yaml` — Current inline HTML (truncated)
- `docs/index.html` — Existing leaderboard template (could use this instead)

**Approach:**
Option 1: Fix the inline HTML heredoc in the workflow
Option 2: Use the existing `docs/index.html` as the template and copy it

Recommend Option 2 - use existing `docs/index.html` which already works. Modify CI to copy it instead of generating inline.

**Gotchas:**
- Heredoc in YAML can be tricky with special characters
- Need to ensure leaderboard.json path is correct for the deployed site

## Dependencies

- **Blocked by:** None
- **Blocks:** 003 (need working site before deploying)

## Verification

```bash
# Build site locally and test
mkdir -p site && cp docs/index.html site/ && cp results/leaderboard.json site/
# Open site/index.html in browser
```
