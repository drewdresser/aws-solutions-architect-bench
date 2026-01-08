# Task: Update README for Launch

**Epic:** [launch-post-and-positioning.md](../epics/launch-post-and-positioning.md)
**Size:** `M`
**Status:** `Done`

## Context

The README.md is the first thing visitors see on GitHub. It needs to be polished for launch, with clear value proposition, quick start instructions, and links to documentation and the live leaderboard.

## Acceptance Criteria

- [x] README has compelling opening that explains what SA Bench is and why it matters
- [x] Includes badge linking to live leaderboard
- [x] Quick start section with one-command run instructions
- [x] Clear explanation of three evaluation categories
- [x] Links to detailed documentation (SCORING.md, ARCHITECTURE_SCORING.md, etc.)
- [x] Link to launch blog post (once published)
- [x] Includes sample leaderboard results or screenshot
- [x] License and contribution sections present

## Technical Notes

**Target File:**
- `README.md` — Project root

**Recommended Structure:**
```markdown
# SA Bench 🏗️

> Measuring LLM performance on AWS Solutions Architect tasks

[![Leaderboard](https://img.shields.io/badge/Leaderboard-Live-brightgreen)](https://drewdresser.github.io/aws-solutions-architect-bench/)

## What is SA Bench?
[2-3 sentences explaining the benchmark and its purpose]

## Why It Matters
[Brief explanation of AI + SA work narrative]

## Current Leaderboard
[Table or link to live leaderboard]

## Evaluation Categories
### Practice Exam (34%)
[Brief description]

### Architecture Design (33%)
[Brief description]

### CDK Synthesis (33%)
[Brief description]

## Quick Start
```bash
# Clone and run
git clone ...
make bench
```

## Documentation
- [Scoring Methodology](docs/SCORING.md)
- [Architecture Scoring](docs/ARCHITECTURE_SCORING.md)
- [Structured Outputs](docs/STRUCTURED_OUTPUTS.md)
- [CDK Failure Modes](docs/CDK_FAILURE_MODES.md)

## Contributing
[Brief contribution guide or link to CONTRIBUTING.md]

## License
[License info]

## Citation
[How to cite SA Bench in papers/posts]
```

**Existing README Analysis:**
- Current README exists (8,215 bytes)
- Has basic structure but may need polish for launch
- Should review and update sections as needed

**Approach:**
1. Review current README content
2. Update opening to be more compelling
3. Add leaderboard badge
4. Ensure quick start is current and works
5. Add citation section for academic use
6. Link to launch blog post

**Gotchas:**
- Quick start instructions must actually work (test them!)
- Don't over-promise on accuracy or coverage
- Keep it concise — link to docs for details

## Dependencies

- **Blocked by:** Task 001 (need blog post to link to)
- **Blocks:** None

## Verification

```bash
# Check README exists and has key sections
grep -E "Quick Start|Leaderboard|Categories|Documentation" README.md

# Test quick start instructions actually work
make bench --dry-run  # or similar verification
```
