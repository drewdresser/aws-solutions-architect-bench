# Task: Add Architecture Critique/Tradeoff Subtype

**Epic:** [expand-architecture-dataset.md](../epics/expand-architecture-dataset.md)
**Size:** `M`
**Status:** `Done`

## Context

The epic mentions "critique/tradeoff analysis" as an optional but valuable task type. This tests a different skill than identification or creation: evaluating existing architectures, identifying weaknesses, and suggesting improvements with trade-off analysis. This is a core SA skill.

## Acceptance Criteria

- [ ] Add new subtype "architecture_critique" to the evaluation framework
- [ ] Create rubric prompt for the new subtype in `judge_prompts.py`
- [ ] Add hidden criteria for anti-gaming
- [ ] Generate 3-4 architecture critique items covering:
  - [ ] Well-Architected Framework pillar violations
  - [ ] Anti-pattern identification
  - [ ] Trade-off analysis (cost vs. performance, availability vs. complexity)
  - [ ] Improvement recommendations
- [ ] Items span beginner to advanced difficulty
- [ ] Each item includes expected critiques and improvement suggestions

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/judge_prompts.py` — Add new rubric
- `evals/architecture_design/architecture_interpretation.jsonl` — Add new items
- `scripts/generate_arch_items.py` — Extend to support new subtype

**New Schema for Critique Items:**
```json
{
  "id": "arch_XXX",
  "type": "diagram_interpretation",
  "subtype": "architecture_critique",
  "difficulty": "beginner|intermediate|advanced",
  "diagram_path": "diagrams/{difficulty}/{name}.png",
  "input": "Review this architecture and identify issues, anti-patterns, and suggest improvements...",
  "target": "...",
  "expected_issues": ["Single point of failure in...", "No encryption at rest..."],
  "expected_improvements": ["Add Multi-AZ for RDS...", "Implement WAF..."],
  "tradeoffs_to_discuss": ["Cost of Multi-AZ vs availability", "Complexity of adding caching"],
  "waf_pillars_relevant": ["reliability", "security", "cost_optimization"],
  "scoring_criteria": {
    "issue_identification": 0.3,
    "improvement_quality": 0.4,
    "tradeoff_analysis": 0.3
  }
}
```

**New Rubric Prompt (add to judge_prompts.py):**
```python
("diagram_interpretation", "architecture_critique"): """
## Task Type: Architecture Critique / Tradeoff Analysis
The model was asked to review an architecture and identify issues and improvements.

## Expected Issues
{expected_issues}

## Expected Improvements
{expected_improvements}

## Tradeoffs to Discuss
{tradeoffs_to_discuss}

## Relevant Well-Architected Pillars
{waf_pillars_relevant}

## Scoring Guidance

### Accuracy (0.0-1.0)
- **0.9-1.0**: Correctly identifies all major issues with proper terminology
- **0.7-0.89**: Most issues identified, minor gaps
- **0.5-0.69**: Core issues found, some missed
- **0.3-0.49**: Limited issue identification
- **0.0-0.29**: Misses critical issues

### Completeness (0.0-1.0)
- **0.9-1.0**: Issues, improvements, AND trade-offs all addressed thoroughly
- **0.7-0.89**: Good coverage across all three areas
- **0.5-0.69**: Partial coverage
- **0.3-0.49**: Missing significant areas
- **0.0-0.29**: Incomplete analysis

### Quality (0.0-1.0)
- **0.9-1.0**: References Well-Architected Framework, explains WHY changes help
- **0.7-0.89**: Good reasoning for recommendations
- **0.5-0.69**: Adequate explanations
- **0.3-0.49**: Superficial reasoning
- **0.0-0.29**: Poor justification

## Response to Evaluate
{response}
"""
```

**Hidden Criteria:**
```python
"architecture_critique": [
    "References specific Well-Architected Framework pillars",
    "Quantifies trade-offs (cost estimates, latency impact)",
    "Prioritizes improvements by impact",
]
```

**Approach:**
1. Update `judge_prompts.py` with new rubric and hidden criteria
2. Update generation script to support new subtype
3. Generate 3-4 items with diverse critique scenarios
4. Review and assign IDs

**Example Critique Scenarios:**
- Beginner: Simple web app missing basic security (no HTTPS, no WAF)
- Intermediate: Over-engineered startup architecture (cost vs. needs)
- Advanced: Production system with subtle reliability issues

## Dependencies

- **Blocked by:** Task 001 (create-generation-script)
- **Blocks:** Task 005 (review-and-tag)

## Verification

```bash
# Check rubric was added
grep "architecture_critique" evals/architecture_design/judge_prompts.py

# Count critique items
grep '"subtype": "architecture_critique"' evals/architecture_design/architecture_interpretation.jsonl | wc -l
# Should be 3-4

# Run scorer on a sample to verify rubric works
uv run pytest tests/test_llm_judge_scorer.py -k critique -v
```
