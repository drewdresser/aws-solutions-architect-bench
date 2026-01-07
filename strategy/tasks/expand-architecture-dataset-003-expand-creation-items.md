# Task: Expand Diagram Creation Items

**Epic:** [expand-architecture-dataset.md](../epics/expand-architecture-dataset.md)
**Size:** `M`
**Status:** `Todo`

## Context

The dataset has 4 diagram creation items covering 3 subtypes. We need more variety in requirements, patterns, and problem scenarios to test model architectural design capabilities more thoroughly.

## Acceptance Criteria

- [ ] Generate 5-6 new diagram creation items using the generation script
- [ ] Coverage across all 3 subtypes:
  - requirements_to_architecture: add 2 (currently 2, target 4)
  - pattern_implementation: add 2 (currently 1, target 3)
  - problem_solving: add 2 (currently 1, target 3)
- [ ] Balanced output formats: mermaid, plantuml, json (roughly equal)
- [ ] Balanced difficulty: 1-2 beginner, 2-3 intermediate, 1-2 advanced
- [ ] Diverse architectural patterns:
  - [ ] CQRS/Event Sourcing
  - [ ] Multi-region active-active
  - [ ] Data lake architecture
  - [ ] Real-time streaming
  - [ ] Disaster recovery
- [ ] Each item includes realistic constraints and expected components
- [ ] Items pass schema validation

## Technical Notes

**Relevant Files:**
- `scripts/generate_arch_items.py` — Generation script from Task 001
- `evals/architecture_design/architecture_interpretation.jsonl` — Append to this file

**Target Item Breakdown:**

| Subtype | Current | Add | Total | Scenarios to Add |
|---------|---------|-----|-------|------------------|
| requirements_to_architecture | 2 | 2 | 4 | Real-time analytics, Multi-tenant SaaS |
| pattern_implementation | 1 | 2 | 3 | CQRS, Saga pattern |
| problem_solving | 1 | 2 | 3 | DR setup, Performance optimization |

**Output Format Distribution:**
- Mermaid: 2-3 items (flowcharts, sequence diagrams)
- PlantUML: 2 items (component diagrams)
- JSON: 1-2 items (structured architecture definitions)

**Example Generation Commands:**
```bash
# Generate intermediate CQRS pattern implementation (PlantUML)
uv run scripts/generate_arch_items.py \
  --subtype pattern_implementation \
  --difficulty intermediate \
  --output-format plantuml \
  --pattern "CQRS with EventBridge and DynamoDB streams" \
  --count 1

# Generate advanced DR problem solving (JSON)
uv run scripts/generate_arch_items.py \
  --subtype problem_solving \
  --difficulty advanced \
  --output-format json \
  --scenario "Design disaster recovery for critical financial application" \
  --count 1
```

**Approach:**
1. Run generation script for each target combination
2. Review constraints and expected components for realism
3. Ensure output format instructions are clear in the input
4. Assign sequential IDs (arch_018 through arch_023)
5. Append to JSONL file

**Gotchas:**
- Creation items require output_format field specifying mermaid/plantuml/json
- Input must include clear instructions for output format
- Expected components should be AWS-specific service names
- Patterns must be recognizable architectural patterns

## Dependencies

- **Blocked by:** Task 001 (create-generation-script)
- **Blocks:** Task 005 (review-and-tag)

## Verification

```bash
# Count creation items
grep '"type": "diagram_creation"' evals/architecture_design/architecture_interpretation.jsonl | wc -l
# Should be 9-10 (4 existing + 5-6 new)

# Check output format distribution
grep -o '"output_format": "[^"]*"' evals/architecture_design/architecture_interpretation.jsonl | sort | uniq -c

# Total items should be 20+
wc -l evals/architecture_design/architecture_interpretation.jsonl
```
