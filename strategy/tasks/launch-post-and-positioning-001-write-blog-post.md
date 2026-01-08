# Task: Write Launch Blog Post

**Epic:** [launch-post-and-positioning.md](../epics/launch-post-and-positioning.md)
**Size:** `L`
**Status:** `Done`

## Context

The primary deliverable of this epic is a compelling public write-up that explains SA Bench to practitioners and researchers. This post will serve as the canonical reference for what SA Bench measures and why it matters.

## Acceptance Criteria

- [x] Blog post written in markdown format at `docs/LAUNCH_POST.md`
- [x] Covers all required sections (see structure below)
- [x] Includes at least 3 example tasks with sample prompts and responses
- [x] Shows at least 2 failure cases demonstrating what models get wrong
- [x] Clear "AI is changing SA work" narrative throughout
- [x] Accessible to both technical and non-technical audiences
- [x] Word count: 1500-2500 words (substantial but not overwhelming)

## Technical Notes

**Target File:**
- `docs/LAUNCH_POST.md` — Main blog post content

**Recommended Structure:**
```markdown
# SA Bench: Measuring AI on Solutions Architect Work

## The Problem
- LLMs are increasingly used for SA work
- No way to measure/compare their capabilities
- Anecdotes aren't enough

## What SA Bench Measures
- Three categories: Practice Exam, Architecture Design, CDK Synthesis
- Explain each briefly with example tasks
- Why these categories matter for real SA work

## Methodology
- How scoring works (brief, link to SCORING.md for details)
- LLM-as-judge for architecture tasks
- Why we chose structured outputs

## Example Tasks and Results
- Show 3 representative tasks (one per category)
- Include actual prompt and response snippets
- Show what "good" vs "bad" looks like

## What Models Get Wrong (Failure Cases)
- Architecture: Missing security considerations
- CDK: Syntax errors, wrong constructs
- MCQ: Plausible but incorrect reasoning

## Current Leaderboard Highlights
- Top performers and why
- Interesting patterns (e.g., model X good at MCQ but weak at CDK)

## Limitations and Future Work
- Dataset size constraints
- Structured output requirements
- Plans for expansion

## How to Run It Yourself
- Link to README
- One-command quickstart

## The Bigger Picture
- AI is changing SA work
- This benchmark helps understand where we are
- Call to action: try it, contribute, cite it
```

**Source Material:**
- `docs/SCORING.md` — Scoring methodology
- `docs/ARCHITECTURE_SCORING.md` — LLM-as-judge approach
- `evals/*/` — Example tasks and datasets
- `docs/leaderboard.json` — Current results

**Approach:**
1. Draft outline following recommended structure
2. Pull real examples from datasets
3. Generate sample model responses for illustration
4. Write in conversational but technical style
5. Review for accessibility to non-AWS-experts

**Gotchas:**
- Don't be too promotional — focus on methodology and utility
- Include limitations honestly (builds credibility)
- Make sure example prompts/responses are representative, not cherry-picked
- Avoid jargon without explanation

## Dependencies

- **Blocked by:** None
- **Blocks:** Tasks 002, 003, 004

## Verification

```bash
# Check file exists and has content
wc -w docs/LAUNCH_POST.md
# Should be 1500-2500 words

# Check all required sections present
grep -E "^##" docs/LAUNCH_POST.md
# Should show all major sections
```
