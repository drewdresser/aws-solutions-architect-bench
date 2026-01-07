# Task: Create Published Rubric Documentation

**Epic:** [llm-judge-architecture-scoring.md](../epics/llm-judge-architecture-scoring.md)
**Size:** `S`
**Status:** `Done`

## Context

For SA Bench to be credible and transparent, we need public documentation explaining how architecture responses are scored. This helps users understand what the benchmark measures and builds trust in the scores.

## Acceptance Criteria

- [ ] Create `docs/ARCHITECTURE_SCORING.md` with rubric documentation
- [ ] Document what each dimension (accuracy, completeness, quality) measures
- [ ] Explain scoring approach at high level (LLM-as-judge with rubrics)
- [ ] Provide examples of good vs poor responses for 1-2 subtypes
- [ ] Note expected score variance and what affects it
- [ ] Link from main SCORING.md and leaderboard methodology section

## Technical Notes

**Relevant Files:**
- `docs/ARCHITECTURE_SCORING.md` — New file with rubric documentation
- `docs/SCORING.md` — Add link to architecture-specific docs
- `docs/index.html` — Update methodology section to mention LLM judge

**Document Structure:**
```markdown
# Architecture Scoring Rubric

## Overview
Architecture tasks are scored using an LLM-as-judge approach with transparent rubrics...

## Scoring Dimensions

### Accuracy (0-100%)
How well the response matches the expected answer...
- **High (80-100%)**: Correct service identification, proper AWS naming...
- **Medium (50-79%)**: Most elements correct, some gaps...
- **Low (0-49%)**: Major errors or omissions...

### Completeness (0-100%)
Coverage of all required elements...

### Quality (0-100%)
Reasoning depth and professional presentation...

## Task Subtypes

### Service Identification
**What it tests**: Ability to recognize AWS services from diagrams...
**Good response example**: ...
**Poor response example**: ...

### Data Flow Analysis
...

## Anti-Gaming Measures
The judge uses additional criteria not detailed here to prevent gaming...

## Expected Variance
Architecture scores may vary ±10% between runs due to LLM judge non-determinism...

## Calibration
The judge has been calibrated against human-scored responses with 80%+ agreement...
```

**Gotchas:**
- Don't expose hidden anti-gaming criteria in public docs
- Examples should be realistic but not from the actual eval set
- Keep language accessible — this is for users, not just developers
- Update if rubrics change significantly

## Dependencies

- **Blocked by:** 002 (need rubrics), 004 (need calibration results)
- **Blocks:** None (but should complete before major release)

## Verification

```bash
# Check file exists and has content
test -s docs/ARCHITECTURE_SCORING.md && echo "Rubric docs exist"

# Check links from SCORING.md
grep -q "ARCHITECTURE_SCORING" docs/SCORING.md && echo "Link added"

# Verify examples are present
grep -c "example" docs/ARCHITECTURE_SCORING.md
```
