# Task: Create Rubric Prompts for Each Architecture Subtype

**Epic:** [llm-judge-architecture-scoring.md](../epics/llm-judge-architecture-scoring.md)
**Size:** `M`
**Status:** `Done`

## Context

Each architecture task subtype (service_identification, data_flow_analysis, security_assessment, etc.) needs a tailored rubric prompt that guides the LLM judge to evaluate responses correctly. Generic prompts lead to inconsistent scoring; subtype-specific prompts improve reliability.

## Acceptance Criteria

- [ ] Create rubric prompts for all interpretation subtypes:
  - `service_identification` — Score on service name accuracy, role explanation
  - `data_flow_analysis` — Score on flow sequence, component understanding
  - `security_assessment` — Score on security control identification, improvement suggestions
  - `scalability_analysis` — Score on scaling mechanism knowledge, bottleneck awareness
  - `cost_optimization` — Score on cost factor understanding, optimization opportunities
- [ ] Create rubric prompts for all creation subtypes:
  - `requirements_to_architecture` — Score on requirement coverage, component selection
  - `pattern_implementation` — Score on pattern fidelity, AWS service choices
  - `problem_solving` — Score on solution completeness, migration strategy
- [ ] Each rubric includes explicit scoring criteria with weights
- [ ] Prompts stored in `evals/architecture_design/judge_prompts.py`

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/judge_prompts.py` — New file for rubric prompts
- `evals/architecture_design/tasks.py` — Import and use rubrics in judge scorer

**Approach:**
1. Create a `RUBRIC_PROMPTS` dictionary keyed by `(type, subtype)`
2. Each rubric is a detailed prompt that:
   - Explains what the task is testing
   - Lists specific criteria to evaluate
   - Provides scoring guidance (what's a 0.8 vs 0.5 vs 0.2)
   - Includes anti-gaming hints (see task 003)
3. Add `get_rubric_prompt(eval_type, subtype)` helper function

**Example Rubric Structure:**
```python
RUBRIC_PROMPTS = {
    ("diagram_interpretation", "service_identification"): """
You are evaluating an AWS architecture service identification response.

## Task Context
The model was shown an architecture diagram and asked to identify AWS services and their roles.

## Expected Services
{expected_services}

## Scoring Criteria
- **accuracy** (0.0-1.0): Did the model correctly identify the services present?
  - 1.0: All services correctly named with proper AWS naming
  - 0.5: Most services identified, some naming issues
  - 0.0: Major services missing or misidentified

- **completeness** (0.0-1.0): Did the model explain each service's role?
  - 1.0: Clear explanation of each service's purpose in the architecture
  - 0.5: Roles mentioned but vague or incomplete
  - 0.0: No role explanations provided

- **quality** (0.0-1.0): Is the response well-structured and professional?
  - 1.0: Clear organization, proper terminology, insightful observations
  - 0.5: Adequate structure, basic terminology
  - 0.0: Disorganized, incorrect terminology, no insight

## Response to Evaluate
{response}

Return JSON with scores and brief reasoning for each dimension.
""",
    # ... more subtypes
}
```

**Gotchas:**
- Keep prompts concise but complete — long prompts increase judge cost
- Include examples of good vs bad responses where helpful
- Avoid overly strict criteria that penalize valid alternative answers
- Test rubrics on known good/bad responses before deployment

## Dependencies

- **Blocked by:** 001 (needs scorer infrastructure to test)
- **Blocks:** 004 (rubrics needed for calibration testing)

## Verification

```bash
# Check all subtypes have rubrics
python -c "from evals.architecture_design.judge_prompts import RUBRIC_PROMPTS; print(len(RUBRIC_PROMPTS))"

# Manual test: Run judge on sample response
uv run python -c "
from evals.architecture_design.judge_prompts import get_rubric_prompt
print(get_rubric_prompt('diagram_interpretation', 'service_identification'))
"
```
