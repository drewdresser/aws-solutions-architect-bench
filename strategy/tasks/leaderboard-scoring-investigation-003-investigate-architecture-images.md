# Task: Investigate Missing Images in Architecture Tasks

**Epic:** [leaderboard-scoring-investigation.md](../epics/leaderboard-scoring-investigation.md)
**Size:** `M`
**Status:** `Done`

## Context

Some architecture tasks are expected to include images (architecture diagrams) but the images are not being loaded or displayed during evaluation. This could cause models to fail tasks that require visual interpretation.

## Acceptance Criteria

- [x] Identify which architecture tasks should have images
- [x] Verify images exist in the expected locations
- [x] Check how images are loaded/embedded in prompts
- [x] Fix any broken image references or loading issues
- [x] Verify images are correctly passed to multimodal models
- [ ] Test with a model that supports vision (deferred to next benchmark run)

## Resolution

**Findings:**
- 28 total architecture items
- 10 items have no diagram (diagram_creation tasks - expected)
- 5 items have existing images (working correctly)
- 13 items reference images that don't exist (broken)

**Fix Applied:**
Updated `evals/architecture_design/tasks.py` to:
1. Validate image paths during dataset loading
2. Skip items where referenced images don't exist
3. Log warnings for skipped items
4. Dataset now correctly loads 15 items (10 no-image + 5 with images)

**Future Work:**
- Create the 13 missing diagram images
- Or rewrite those items to not require images

## Technical Notes

**Files to investigate:**
- `evals/architecture_design/architecture_interpretation.jsonl` — Dataset with image references
- `evals/architecture_design/diagrams/` — Image files
- `evals/architecture_design/tasks.py` — Task loading logic

**Potential issues:**
1. Image paths incorrect or relative vs absolute
2. Base64 encoding not working
3. Images not being passed to model API correctly
4. JSONL entries missing image field
5. inspect-ai not handling images properly

**Investigation steps:**
1. Load a sample from architecture_interpretation.jsonl
2. Check if image field exists and path is valid
3. Trace code path for image loading in tasks.py
4. Check inspect-ai logs for image-related errors
5. Test with a known multimodal model

## Dependencies

- **Blocked by:** None
- **Blocks:** Accurate architecture scores

## Verification

```bash
# Run single architecture task with debug logging
INSPECT_LOG_LEVEL=debug make eval.arch LIMIT=1

# Check logs for image-related entries
```
