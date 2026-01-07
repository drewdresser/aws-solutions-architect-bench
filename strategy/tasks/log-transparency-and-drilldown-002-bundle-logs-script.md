# Task: Create Log Bundling Script

**Epic**: [log-transparency-and-drilldown](../epics/log-transparency-and-drilldown.md)
**Task ID**: 002-bundle-logs-script
**Status**: `Not Started`

## Objective

Create a script that bundles Inspect logs and organizes them for easy linking from the leaderboard.

## Acceptance Criteria

- [ ] Script bundles all logs using `inspect view bundle`
- [ ] Output organized in a predictable structure (by model name or task)
- [ ] Script handles missing logs gracefully
- [ ] Output placed in `docs/logs/` for GitHub Pages deployment
- [ ] Script can be run locally and in CI

## Implementation Notes

### Proposed Script Location

`scripts/bundle_logs.py` or `Makefile` target

### Proposed Output Structure

```
docs/logs/
├── index.html           # Main viewer entry point
├── assets/              # JS/CSS assets
└── logs/                # Individual log files (if separate)
```

### Key Considerations

1. **Model Name Mapping**: May need to map log file names to leaderboard model names
2. **Size Management**: Consider if logs should be filtered or compressed
3. **Incremental Updates**: Should support re-bundling when new logs are added

### Example Implementation

```bash
#!/bin/bash
# scripts/bundle_logs.sh

set -e

LOG_DIR="${LOG_DIR:-logs}"
OUTPUT_DIR="${OUTPUT_DIR:-docs/logs}"

echo "Bundling logs from $LOG_DIR to $OUTPUT_DIR"
uv run inspect view bundle --log-dir "$LOG_DIR" --output-dir "$OUTPUT_DIR" --overwrite

echo "Log bundle complete!"
```

## Dependencies

- Task 001 (explore-inspect-bundle) must be completed to understand output format
