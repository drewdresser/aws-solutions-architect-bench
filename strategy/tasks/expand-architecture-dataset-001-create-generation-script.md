# Task: Create OpenAI-Powered Item Generation Script

**Epic:** [expand-architecture-dataset.md](../epics/expand-architecture-dataset.md)
**Size:** `M`
**Status:** `Done`

## Context

To efficiently expand the architecture dataset from 9 to 20+ items, we'll create a PEP723-powered Python script that uses the OpenAI API to generate new evaluation items. This script will ensure consistency with the existing dataset schema and enable rapid, high-quality item creation.

## Acceptance Criteria

- [ ] Script uses PEP723 inline metadata for dependencies (openai, pydantic)
- [ ] Script can be run with `uv run scripts/generate_arch_items.py`
- [ ] Generates items matching the exact JSONL schema of existing items
- [ ] Supports all 8 subtypes: service_identification, data_flow_analysis, security_assessment, scalability_analysis, cost_optimization, requirements_to_architecture, pattern_implementation, problem_solving
- [ ] Accepts CLI arguments for: subtype, difficulty, count, output file
- [ ] Uses structured outputs (JSON mode) to ensure valid schema
- [ ] Includes validation that generated items match expected schema
- [ ] Generates unique IDs following arch_XXX pattern

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/architecture_interpretation.jsonl` — Target schema to match
- `evals/architecture_design/judge_prompts.py` — Contains field definitions per subtype
- `scripts/` — Location for new script

**Schema Reference (by type):**

```python
# diagram_interpretation items need:
{
  "id": "arch_XXX",
  "type": "diagram_interpretation",
  "subtype": "service_identification|data_flow_analysis|security_assessment|scalability_analysis|cost_optimization",
  "difficulty": "beginner|intermediate|advanced",
  "diagram_path": "diagrams/{difficulty}/{name}.png",
  "input": "...",
  "target": "...",
  # Plus subtype-specific fields like expected_services, expected_flow, etc.
  "scoring_criteria": {...}
}

# diagram_creation items need:
{
  "id": "arch_XXX",
  "type": "diagram_creation",
  "subtype": "requirements_to_architecture|pattern_implementation|problem_solving",
  "difficulty": "beginner|intermediate|advanced",
  "output_format": "mermaid|plantuml|json",
  "input": "...",
  "target": "...",
  # Plus subtype-specific fields
  "scoring_criteria": {...}
}
```

**Approach:**
1. Use PEP723 script metadata for zero-config execution
2. Define Pydantic models matching the schema
3. Create prompts that generate items with proper AWS depth
4. Use OpenAI's JSON mode for reliable structured output
5. Validate and dedupe before appending to dataset

**Example Script Header:**
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "openai>=1.0",
#   "pydantic>=2.0",
# ]
# ///
```

**Gotchas:**
- Diagram paths should be placeholders (actual diagrams don't exist)
- Generated items need human review before final inclusion
- Model should use real AWS service names and realistic scenarios
- Avoid duplicating scenarios already in the dataset

## Dependencies

- **Blocked by:** None
- **Blocks:** Tasks 002-005 (generation tasks use this script)

## Verification

```bash
# Script runs without errors
uv run scripts/generate_arch_items.py --help

# Generates valid item
uv run scripts/generate_arch_items.py --subtype service_identification --difficulty intermediate --count 1 --dry-run

# Validate output schema
python -c "import json; [json.loads(l) for l in open('test_output.jsonl')]"
```
