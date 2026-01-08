# Task: Explore Inspect Bundle Command

**Epic**: [log-transparency-and-drilldown](../epics/log-transparency-and-drilldown.md)
**Task ID**: 001-explore-inspect-bundle
**Status**: `Done`

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

## Findings (2026-01-07)

### Bundle Output Structure

```
test-bundle/
├── index.html          # Entry point (single-page React app)
├── robots.txt          # SEO file
├── assets/
│   ├── index.js        # ~9.7MB bundled React viewer
│   ├── index.css       # ~956KB styles
│   └── favicon.svg     # Icon
└── logs/
    ├── listing.json    # Metadata about all logs
    └── *.eval          # Individual log files (ZIP format)
```

### Key Findings

1. **Size**: ~10MB fixed overhead for assets, plus individual log files (~9KB per eval)
2. **Static Hosting**: Works as static files - no server required
3. **listing.json**: Contains metadata for each log including:
   - `model`: Model name (e.g., "openrouter/anthropic/claude-sonnet-4")
   - `task`: Task name
   - `status`: success/error
   - `primary_metric`: Score information
   - `started_at`/`completed_at`: Timestamps
4. **Log Format**: `.eval` files are ZIP archives containing JSON data
5. **Viewer**: React-based single-page app that loads logs dynamically

### Linking Strategy

The `listing.json` provides all metadata needed to:
1. Map model names from leaderboard to log files
2. Show log availability before linking
3. Link directly to the viewer (URL fragment or query param for specific log)

### Recommendations

1. **Single Bundle**: Use one bundled viewer at `docs/logs/` with all logs
2. **Model Mapping**: Parse `listing.json` to create model → log URL mapping
3. **Size Management**: 10MB is acceptable for GitHub Pages (1GB limit)
4. **CI Integration**: Bundle after each benchmark run before deployment
