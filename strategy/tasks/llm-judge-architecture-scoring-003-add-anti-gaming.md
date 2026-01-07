# Task: Add Anti-Gaming Mechanisms to LLM Judge

**Epic:** [llm-judge-architecture-scoring.md](../epics/llm-judge-architecture-scoring.md)
**Size:** `M`
**Status:** `Done`

## Context

LLM-as-judge scoring can be gamed if models learn to produce responses that "look good" to judges without actually being correct. We need mechanisms to make gaming harder: hidden test points, multi-judge consistency, and adversarial checks.

## Acceptance Criteria

- [ ] Implement at least one anti-gaming mechanism:
  - **Option A: Hidden Test Points** — Add criteria not visible in the public rubric
  - **Option B: Schema Validation** — Require structured output that can be deterministically validated
  - **Option C: Multi-Judge Consistency** — Run multiple judge prompts and aggregate scores
  - **Option D: Adversarial Checks** — Test for keyword stuffing, verbose padding, etc.
- [ ] Document which mechanism(s) are implemented
- [ ] Anti-gaming reduces score inflation from "gaming" responses vs legitimate answers
- [ ] Mechanism doesn't unfairly penalize valid alternative approaches

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/tasks.py` — Add anti-gaming to judge scorer
- `evals/architecture_design/judge_prompts.py` — Hidden criteria in prompts
- `docs/SCORING.md` — Document anti-gaming approach

**Recommended Approach: Hidden Test Points + Deterministic Fallback**

1. **Hidden Test Points**: Add criteria to judge prompts that aren't in the public rubric
   - Check for specific AWS best practices not mentioned in expected answer
   - Verify response doesn't contradict fundamental AWS concepts
   - Score on coherence between different parts of the answer

2. **Deterministic Fallback**: Combine LLM judge with keyword checks
   - If judge gives high score but response lacks expected keywords → penalize
   - If response mentions correct services but judge is skeptical → trust keywords partially
   - Weight: 70% LLM judge + 30% deterministic checks

3. **Adversarial Detection**: Flag suspicious patterns
   - Very long responses with repetitive content → quality penalty
   - Generic AWS buzzword salad without specifics → completeness penalty
   - Response structure doesn't match question type → accuracy penalty

**Example Hidden Criteria:**
```python
HIDDEN_CRITERIA = {
    "service_identification": [
        "Correctly distinguishes between similar services (e.g., ALB vs NLB)",
        "Mentions service tiers or editions where relevant (e.g., RDS engine type)",
        "Acknowledges relationships between services (e.g., EC2 needs VPC)",
    ],
    "security_assessment": [
        "References AWS Shared Responsibility Model concepts",
        "Considers data-at-rest vs data-in-transit separately",
        "Mentions IAM or resource-based policies",
    ],
}
```

**Gotchas:**
- Hidden criteria must be fair — they should reward expertise, not trick responses
- Multi-judge is expensive (2-3x cost) — consider only for final scoring runs
- Adversarial checks can have false positives — tune thresholds carefully
- Document anti-gaming publicly at high level, but keep specifics private

## Dependencies

- **Blocked by:** 001 (needs judge infrastructure), 002 (needs base rubrics)
- **Blocks:** None

## Verification

```bash
# Test with known gaming attempt
uv run python -c "
# Create a gaming response (verbose, keyword-heavy but wrong)
gaming_response = '''
AWS services include Amazon EC2, Amazon RDS, Elastic Load Balancer...
[repeat buzzwords without actual analysis]
'''
# Should score lower than legitimate response
"

# Run scorer on calibration set
uv run pytest tests/test_anti_gaming.py -v
```
