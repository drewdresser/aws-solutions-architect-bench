# Epic: Log Transparency and Drilldown

## User Value

Users viewing the leaderboard can click on a model to see detailed evaluation logs, understanding exactly how scores were computed, what questions were asked, and how the model responded. This increases trust in the benchmark and helps researchers debug and understand model behavior.

## Success Criteria

- [x] Detailed logs viewable by clicking on model names in the leaderboard
- [x] Logs hosted as static files on GitHub Pages (no server required)
- [x] Per-model log pages show all eval samples with questions, responses, and scores
- [x] Log viewer works across all three categories (Practice Exam, Architecture, CDK)
- [x] CI pipeline automatically bundles and deploys logs alongside leaderboard

## Technical Approach

Leverage Inspect AI's built-in `inspect view bundle` command to generate static HTML log viewers. The approach:

1. **Log Bundling**: Run `inspect view bundle --log-dir logs --output-dir docs/logs` to generate static HTML files for each evaluation log
2. **Leaderboard Integration**: Modify `docs/index.html` to make model names clickable, linking to their corresponding log viewer pages
3. **CI Integration**: Update the GitHub Actions workflow to bundle logs and deploy them alongside the leaderboard
4. **Organization**: Structure logs by model name for easy linking (e.g., `docs/logs/{model-name}/index.html`)

### Key Commands

```bash
# Bundle all logs into static HTML files
uv run inspect view bundle --log-dir logs --output-dir docs/logs --overwrite

# The bundled output can be served statically via GitHub Pages
```

### Alternative Considerations

If `inspect view bundle` doesn't meet all needs, we could:
- Extract key data from logs and build a custom React/HTML viewer
- Use the JSON export from `inspect log dump` and build a lightweight viewer

## OKR Alignment

- **Objective**: O1 — Ship SA Bench v0.1 as a credible, reproducible public benchmark
- **Key Result**: KR2 — Host leaderboard publicly with stable URL and documentation (enhancement)
- **Objective**: O4 — Earn credible public attention for the leaderboard
- **Key Result**: Transparency builds trust and credibility

## Dependencies

- **Depends on**: public-leaderboard-and-release (need leaderboard infrastructure)
- **Blocks**: None (enhances credibility-and-distribution)
- **Priority**: `Medium`

## Tasks

- [x] [001-explore-inspect-bundle](../tasks/log-transparency-and-drilldown-001-explore-inspect-bundle.md) — Test `inspect view bundle` and understand output structure
- [x] [002-bundle-logs-script](../tasks/log-transparency-and-drilldown-002-bundle-logs-script.md) — Create script to organize bundled logs by model
- [x] [003-add-leaderboard-links](../tasks/log-transparency-and-drilldown-003-add-leaderboard-links.md) — Make model names clickable in leaderboard UI
- [x] [004-ci-log-deployment](../tasks/log-transparency-and-drilldown-004-ci-log-deployment.md) — Update CI to bundle and deploy logs with leaderboard

## Status

`Done`
