# Task: Verify and Document GitHub Pages URL

**Epic:** [public-leaderboard-and-release.md](../epics/public-leaderboard-and-release.md)
**Size:** `S`
**Status:** `Done`

## Context

The CI workflow deploys to GitHub Pages, but we need to verify the deployment is working and document the stable URL. The leaderboard URL should be easily findable in the README and consistently linked throughout docs.

## Acceptance Criteria

- [ ] GitHub Pages is enabled in repository settings (if not already)
- [ ] Leaderboard is accessible at stable URL (e.g., `https://drewdresser.github.io/aws-sa-bench/`)
- [ ] README has prominent link to leaderboard URL near the top
- [ ] All internal docs link to the correct URL (check SCORING.md, index.html)
- [ ] URL is tested after a CI run to confirm deployment works

## Technical Notes

**Relevant Files:**
- `README.md` — Add/update leaderboard URL
- `docs/index.html` — Verify links are correct
- `.github/workflows/bench.yaml` — Verify deployment job

**Approach:**
1. Check GitHub repo Settings → Pages to confirm source and URL
2. Trigger a workflow run (or wait for nightly) and verify deployment
3. Update README with prominent leaderboard link
4. Search codebase for any incorrect URLs and fix

**Where to Add URL in README:**
```markdown
# AWS Solutions Architect Bench

**[📊 View Leaderboard](https://drewdresser.github.io/aws-sa-bench/)** | [Scoring Methodology](docs/SCORING.md) | [GitHub](...)
```

**Gotchas:**
- GitHub Pages URL is case-sensitive and based on repo name
- If using custom domain in future, update all references
- Ensure `index.html` is copied to site root (already in CI workflow)

## Dependencies

- **Blocked by:** None
- **Blocks:** 004 (release notes should link to verified URL)

## Verification

```bash
# Check if GitHub Pages is live
curl -sI https://drewdresser.github.io/aws-sa-bench/ | grep HTTP

# Verify leaderboard.json loads
curl -s https://drewdresser.github.io/aws-sa-bench/leaderboard.json | jq '.[0].model'

# Check README has the link
grep -q "github.io/aws-sa-bench" README.md && echo "URL found in README"
```
