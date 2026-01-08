# Task: Update to Latest Frontier Models

**Epic:** [leaderboard-scoring-investigation.md](../epics/leaderboard-scoring-investigation.md)
**Size:** `S`
**Status:** `Done`

## Context

The current model list includes older models (gpt-4.1, gpt-5) that should be replaced with the latest frontier models to ensure the benchmark reflects current capabilities.

## Acceptance Criteria

- [x] Remove `openrouter/openai/gpt-4.1` from model list
- [x] Remove `openrouter/openai/gpt-5` from model list
- [x] Add `openrouter/openai/gpt-5.2` to model list
- [x] Add `openrouter/anthropic/claude-sonnet-4.5` to model list
- [x] Verify models work with a quick test run
- [ ] Update any documentation referencing old models (N/A - no docs to update)

## Technical Notes

**Files to modify:**
- `Makefile` — Update the `MODELS` variable

**Current models:**
```makefile
MODELS ?= openrouter/anthropic/claude-sonnet-4,openrouter/openai/gpt-4.1,openrouter/openai/gpt-5
```

**Target models:**
```makefile
MODELS ?= openrouter/anthropic/claude-sonnet-4,openrouter/anthropic/claude-sonnet-4.5,openrouter/openai/gpt-5.2
```

## Dependencies

- **Blocked by:** None
- **Blocks:** Fresh benchmark run

## Verification

```bash
# Quick test with new models
make eval.practice LIMIT=1
```
