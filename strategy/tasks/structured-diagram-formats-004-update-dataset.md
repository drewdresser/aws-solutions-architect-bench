# Task: Update Dataset Items with Format Requirements

**Epic:** [structured-diagram-formats-and-validation.md](../epics/structured-diagram-formats-and-validation.md)
**Size:** `S`
**Status:** `Done`

## Context

With validation infrastructure in place, we need to update the diagram creation tasks in the dataset to specify required output formats. This tells models what format to produce and enables validation scoring.

## Acceptance Criteria

- [ ] Add `output_format` field to diagram_creation tasks (arch_006, arch_007, arch_008)
- [ ] Update task prompts to explicitly request the format
- [ ] Add `expected_components` for JSON validation (component IDs to check)
- [ ] Keep interpretation tasks unchanged (no format requirement)
- [ ] Create one new diagram creation task that requires Mermaid output

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/architecture_interpretation.jsonl` — Update dataset

**Format Options:**
- `"output_format": "mermaid"` — Require Mermaid flowchart/diagram
- `"output_format": "plantuml"` — Require PlantUML diagram
- `"output_format": "json"` — Require JSON architecture description
- `"output_format": null` — No specific format required (default)

**Updated arch_006 Example:**
```json
{
  "id": "arch_006",
  "type": "diagram_creation",
  "subtype": "requirements_to_architecture",
  "output_format": "mermaid",
  "input": "Design a highly available web application architecture... Output your architecture as a Mermaid flowchart diagram.",
  "expected_components": ["ALB", "EC2", "RDS", "CloudFront"],
  ...
}
```

**Prompt Additions by Format:**
- Mermaid: "Output your architecture as a Mermaid flowchart diagram using ```mermaid code blocks."
- PlantUML: "Output your architecture as a PlantUML component diagram using ```plantuml code blocks."
- JSON: "Output your architecture as a JSON object following the architecture schema, using ```json code blocks."

**Gotchas:**
- Keep existing scoring criteria — format is additive
- Don't change task difficulty or expected components
- Ensure prompt clearly communicates format requirement

## Dependencies

- **Blocked by:** 003 (scorer must support format validation)
- **Blocks:** None

## Verification

```bash
# Verify dataset is valid JSON
python -c "import json; [json.loads(l) for l in open('evals/architecture_design/architecture_interpretation.jsonl')]"

# Check format field present
grep -c "output_format" evals/architecture_design/architecture_interpretation.jsonl
```
