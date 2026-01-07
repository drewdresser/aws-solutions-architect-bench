# Task: Explore Inspect Bundle Command

**Epic**: [log-transparency-and-drilldown](../epics/log-transparency-and-drilldown.md)
**Task ID**: 001-explore-inspect-bundle
**Status**: `Not Started`

## Objective

Understand how `inspect view bundle` works and what output it generates, to determine if it meets our needs for static log viewing.

## Acceptance Criteria

- [ ] Document what files `inspect view bundle` generates
- [ ] Confirm bundled output works as static HTML (no server required)
- [ ] Identify any limitations (file size, interactivity, customization)
- [ ] Test with logs from all three categories (Practice Exam, Architecture, CDK)
- [ ] Document folder structure and naming conventions of output

## Implementation Notes

### Commands to Test

```bash
# List available logs
uv run inspect log list --log-dir logs

# Bundle all logs
uv run inspect view bundle --log-dir logs --output-dir test-bundle --overwrite

# Examine output structure
ls -la test-bundle/
```

### Questions to Answer

1. Does the bundle include all log details (prompts, responses, scores)?
2. Can we link directly to a specific model's logs?
3. What is the approximate size of bundled output?
4. Does it work offline / as static files?

## Dependencies

- Requires eval logs to exist in `logs/` directory

## Notes

If `inspect view bundle` doesn't meet all requirements, document gaps and consider alternative approaches (custom viewer, JSON extraction).
