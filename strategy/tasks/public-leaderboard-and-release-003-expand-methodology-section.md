# Task: Expand Methodology Section on Leaderboard Page

**Epic:** [public-leaderboard-and-release.md](../epics/public-leaderboard-and-release.md)
**Size:** `S`
**Status:** `Done`

## Context

The leaderboard page has a brief methodology section, but visitors need more context to understand and trust the scores. This task expands the on-page documentation to answer common questions without requiring users to click through to GitHub.

## Acceptance Criteria

- [ ] Methodology section explains what each category measures (1-2 sentences each)
- [ ] Overall score formula is shown explicitly (e.g., "Overall = 0.34×MCQ + 0.33×Arch + 0.33×CDK")
- [ ] Reproducibility note explains expected ±5% variance between runs
- [ ] Links to full docs remain (SCORING.md, CDK_FAILURE_MODES.md, GitHub repo)
- [ ] Section is collapsible or uses tabs to avoid overwhelming the page
- [ ] Meta tags added for social sharing (og:title, og:description, og:image)

## Technical Notes

**Relevant Files:**
- `docs/index.html` — Add expanded methodology content

**Approach:**
1. Expand the existing `.methodology` div with more detail
2. Use Bulma's `collapsible` or `tabs` component to organize content
3. Add sections: "What We Measure", "How Scores Work", "Reproducibility"
4. Add Open Graph meta tags for better social sharing

**Content Outline:**
```
What We Measure
├── Practice Exam (34%): AWS certification-style MCQ covering...
├── Architecture Design (33%): Diagram understanding and reasoning...
└── CDK Synthesis (33%): Infrastructure-as-code generation...

How Scores Work
├── Formula: Overall = 0.34×practice_exam + 0.33×architecture + 0.33×cdk
├── Range: 0-100% (shown as percentages)
└── Per-category: Each category is scored independently

Reproducibility
├── Expected variance: ±5% between runs
├── Factors: Model updates, temperature, API routing
└── How to reproduce: [link to README]
```

**Gotchas:**
- Keep content scannable (bullets, not walls of text)
- Don't duplicate SCORING.md entirely — link to it for full details
- Test that collapsible components work without JS if possible

## Dependencies

- **Blocked by:** None
- **Blocks:** None

## Verification

```bash
# Open page and verify methodology section
open docs/index.html
# Check meta tags
curl -s docs/index.html | grep -E '<meta property="og:'
```
