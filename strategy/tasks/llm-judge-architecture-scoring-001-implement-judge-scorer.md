# Task: Implement LLM-as-Judge Scorer Infrastructure

**Epic:** [llm-judge-architecture-scoring.md](../epics/llm-judge-architecture-scoring.md)
**Size:** `M`
**Status:** `Done`

## Context

The current architecture scorer in `evals/architecture_design/tasks.py` uses keyword heuristics (checking if expected words appear in responses). This is brittle and easy to game. We need to implement an LLM-as-judge scorer that can evaluate nuanced architectural reasoning using a separate model call.

## Acceptance Criteria

- [ ] Create `llm_judge_scorer()` function that calls a judge model to evaluate responses
- [ ] Judge scorer accepts a rubric prompt and response to evaluate
- [ ] Scorer returns structured scores (accuracy, completeness, quality) like the current scorer
- [ ] Add configuration for judge model (default to a capable model like GPT-4o or Claude)
- [ ] Add fallback to deterministic checks if judge call fails
- [ ] Integrate with Inspect AI's scorer interface

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/tasks.py` — Add new `llm_judge_scorer()` alongside existing scorer
- `evals/architecture_design/judge_prompts.py` — New file for rubric prompts (task 002)

**Approach:**
1. Create a generic `call_judge()` helper that sends a prompt to a judge model
2. Build `llm_judge_scorer()` that constructs the judge prompt with:
   - The original task/question
   - The expected answer/rubric criteria
   - The model's response to evaluate
3. Parse the judge's structured output (JSON with scores and reasoning)
4. Map judge output to Score object with metadata

**Judge Prompt Template:**
```
You are evaluating an architecture response. Score from 0.0 to 1.0 on:
- accuracy: How well does the response match the expected answer?
- completeness: Does it cover all required elements?
- quality: Is the reasoning sound and well-explained?

Task: {task_description}
Expected Answer: {expected}
Model Response: {response}

Return JSON: {"accuracy": X.X, "completeness": X.X, "quality": X.X, "reasoning": "..."}
```

**Gotchas:**
- Judge model must be different from model being evaluated (or use self-consistency)
- Handle rate limits and errors gracefully
- Parse JSON carefully — LLMs sometimes add extra text
- Consider cost — judge calls add overhead per sample

## Dependencies

- **Blocked by:** None
- **Blocks:** 002 (needs scorer infrastructure), 003 (needs scorer for anti-gaming)

## Verification

```bash
# Run architecture eval with new scorer
uv run inspect eval evals/architecture_design/tasks.py -T architecture_design --scorer llm_judge

# Check that scores are returned
uv run pytest tests/test_llm_judge_scorer.py -v
```
