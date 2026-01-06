# Task: Add GitHub Pages Deployment

**Epic:** [reproducibility-and-ci.md](../epics/reproducibility-and-ci.md)
**Size:** `M`
**Status:** `Done`

## Context

The CI builds a static site but doesn't deploy it to GitHub Pages. Adding deployment makes the leaderboard publicly accessible at a stable URL.

## Acceptance Criteria

- [ ] CI deploys site to GitHub Pages after successful benchmark
- [ ] Leaderboard accessible at `https://<user>.github.io/<repo>/`
- [ ] Deployment only happens on successful runs (not on failure)
- [ ] Site includes leaderboard.json, leaderboard.csv, and index.html

## Technical Notes

**Relevant Files:**
- `.github/workflows/bench.yaml` — Add deployment steps

**Approach:**
Add GitHub Pages deployment using the official actions:

```yaml
- name: Setup Pages
  uses: actions/configure-pages@v4

- name: Upload Pages artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: site

- name: Deploy to GitHub Pages
  id: deployment
  uses: actions/deploy-pages@v4
```

Also need to ensure the repository has Pages enabled with "GitHub Actions" as the source.

**Gotchas:**
- Requires `pages: write` and `id-token: write` permissions (already present)
- May need to configure repository settings to enable Pages from Actions
- Should only deploy on main branch and successful runs

## Dependencies

- **Blocked by:** 002 (need working static site)
- **Blocks:** None

## Verification

```bash
# After workflow runs, check Pages URL
curl -I https://drewdresser.github.io/aws-sa-bench/
```
