# Task: CI Integration for Log Deployment

**Epic**: [log-transparency-and-drilldown](../epics/log-transparency-and-drilldown.md)
**Task ID**: 004-ci-log-deployment
**Status**: `Not Started`

## Objective

Update the GitHub Actions CI workflow to automatically bundle and deploy evaluation logs alongside the leaderboard.

## Acceptance Criteria

- [ ] CI workflow bundles logs when leaderboard is updated
- [ ] Bundled logs deployed to GitHub Pages with leaderboard
- [ ] CI handles missing logs gracefully (doesn't fail if no logs)
- [ ] Deployment is atomic (logs and leaderboard update together)
- [ ] Logs are available at predictable URL (e.g., `https://drewdresser.github.io/aws-solutions-architect-bench/logs/`)

## Implementation Notes

### Files to Modify

- `.github/workflows/deploy.yml` (or equivalent)
- Potentially `Makefile` if used for build orchestration

### Proposed Workflow Changes

```yaml
jobs:
  deploy:
    steps:
      # ... existing steps ...

      - name: Bundle evaluation logs
        run: |
          if [ -d "logs" ] && [ "$(ls -A logs 2>/dev/null)" ]; then
            uv run inspect view bundle --log-dir logs --output-dir docs/logs --overwrite
            echo "Logs bundled successfully"
          else
            echo "No logs found, skipping bundle"
          fi

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

### Considerations

1. **Log Storage**: Where do logs come from in CI?
   - Option A: Logs checked into repo (simple but large)
   - Option B: Logs stored in artifacts from eval runs
   - Option C: Logs fetched from separate storage (S3, etc.)

2. **Size Limits**: GitHub Pages has size limits; may need to manage log retention

3. **Privacy**: Ensure no sensitive data in logs (API keys, etc.)

## Dependencies

- Tasks 001-003 must be completed
- Need to decide on log storage strategy
