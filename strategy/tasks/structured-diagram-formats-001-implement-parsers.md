# Task: Implement Mermaid and PlantUML Parsers

**Epic:** [structured-diagram-formats-and-validation.md](../epics/structured-diagram-formats-and-validation.md)
**Size:** `M`
**Status:** `Done`

## Context

To validate structured diagram outputs, we need parsers that can verify Mermaid and PlantUML syntax is correct. These parsers will be used by the scorer to add a structural validation component to architecture scoring.

## Acceptance Criteria

- [ ] Create `validate_mermaid()` function that checks Mermaid syntax validity
- [ ] Create `validate_plantuml()` function that checks PlantUML syntax validity
- [ ] Both functions return `(is_valid: bool, error_message: str | None)`
- [ ] Extract diagram code from fenced code blocks (```mermaid, ```plantuml)
- [ ] Handle common syntax errors gracefully
- [ ] Add unit tests for valid and invalid diagrams

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/diagram_validators.py` — New file for validators
- `tests/test_diagram_validators.py` — New test file

**Approach:**
1. For Mermaid: Use regex to validate basic structure (graph/flowchart declarations, node definitions, edges)
2. For PlantUML: Validate @startuml/@enduml wrapper and basic component syntax
3. Consider using external tools if available (mermaid-cli, plantuml.jar) but don't require them
4. Focus on structural validation, not semantic correctness

**Mermaid Validation Points:**
- Must start with diagram type (graph, flowchart, sequenceDiagram, etc.)
- Node definitions match `id[label]` or `id((label))` patterns
- Edges match `-->`, `---`, `-.->` patterns
- Balanced brackets and quotes

**PlantUML Validation Points:**
- Must have @startuml and @enduml delimiters
- Component definitions match `[name]`, `(name)`, `database name` patterns
- Relationships match `-->`, `..>`, `--` patterns

**Gotchas:**
- Don't be too strict — focus on parseable, not perfect
- Handle multiline code blocks
- Some models may add explanation text around the diagram

## Dependencies

- **Blocked by:** None
- **Blocks:** 003 (needs validators for scorer integration)

## Verification

```bash
uv run pytest tests/test_diagram_validators.py -v
```
