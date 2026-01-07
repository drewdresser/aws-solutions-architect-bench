# Task: Create v0.1 Release with Release Notes

**Epic:** [public-leaderboard-and-release.md](../epics/public-leaderboard-and-release.md)
**Size:** `S`
**Status:** `Todo`

## Context

To make SA Bench citable and referenceable, we need a formal v0.1 release tag with release notes documenting what's included. This signals that the benchmark is ready for public use and provides a stable reference point.

## Acceptance Criteria

- [ ] Git tag `v0.1.0` created and pushed
- [ ] GitHub Release created from tag with release notes
- [ ] Release notes include: what's included, how to run, known limitations
- [ ] Release notes link to leaderboard URL and documentation
- [ ] README badge or link points to latest release

## Technical Notes

**Relevant Files:**
- None to create — this is a GitHub release process
- `README.md` — Add release badge/link after release

**Approach:**
1. Write release notes covering:
   - What's new in v0.1 (initial public release)
   - Three evaluation tracks (MCQ, Architecture, CDK)
   - Reproducibility instructions
   - Known limitations (CDK failure modes, scoring caveats)
   - Links to docs and leaderboard
2. Create tag: `git tag -a v0.1.0 -m "Initial public release"`
3. Push tag: `git push origin v0.1.0`
4. Create GitHub Release via UI or `gh release create`

**Release Notes Template:**
```markdown
## SA Bench v0.1.0 — Initial Public Release

### What's Included
- **Practice Exam Track**: AWS certification-style MCQ (34% weight)
- **Architecture Design Track**: Diagram understanding and reasoning (33% weight)
- **CDK Synthesis Track**: Infrastructure-as-code generation (33% weight)

### Leaderboard
View current results: [SA Bench Leaderboard](https://drewdresser.github.io/aws-sa-bench/)

### Quick Start
\`\`\`bash
git clone https://github.com/drewdresser/aws-sa-bench
cd aws-sa-bench && uv sync
cp .env.example .env  # Add OPENROUTER_API_KEY
make bench && make board.json
\`\`\`

### Documentation
- [Scoring Methodology](docs/SCORING.md)
- [CDK Failure Modes](docs/CDK_FAILURE_MODES.md)
- [Full README](README.md)

### Known Limitations
- CDK track may show 0% for some models due to extraction issues
- Scores vary ±5% between runs (expected LLM non-determinism)
- Architecture scoring uses heuristic rubrics (LLM-as-judge coming in v0.2)
```

**Gotchas:**
- Ensure all tests pass before tagging (`make test`)
- Consider whether to include a sample `leaderboard.json` in release assets
- Semantic versioning: v0.1.0 indicates early/experimental status

## Dependencies

- **Blocked by:** 001, 002, 003 (complete UI improvements before release)
- **Blocks:** launch-post-and-positioning epic (needs something to launch)

## Verification

```bash
# Check tag exists
git tag | grep v0.1.0

# Check release on GitHub
gh release view v0.1.0

# Verify release notes are accessible
curl -s https://api.github.com/repos/drewdresser/aws-sa-bench/releases/tags/v0.1.0 | jq '.body'
```
