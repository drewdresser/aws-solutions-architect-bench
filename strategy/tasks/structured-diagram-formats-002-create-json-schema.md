# Task: Create JSON Schema for Architecture Descriptions

**Epic:** [structured-diagram-formats-and-validation.md](../epics/structured-diagram-formats-and-validation.md)
**Size:** `M`
**Status:** `Done`

## Context

As an alternative to visual diagram formats, we need a JSON schema that captures architecture descriptions in a structured, machine-parseable format. This enables deterministic validation of required components and relationships.

## Acceptance Criteria

- [ ] Create JSON schema for architecture descriptions
- [ ] Schema captures: services/components, relationships/edges, metadata
- [ ] Create `validate_architecture_json()` function using jsonschema library
- [ ] Function extracts JSON from code blocks and validates against schema
- [ ] Schema is flexible enough for different architecture types
- [ ] Add unit tests for valid and invalid JSON architectures

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/schemas/architecture.json` — JSON schema file
- `evals/architecture_design/diagram_validators.py` — Add JSON validation function
- `tests/test_diagram_validators.py` — Add JSON validation tests

**JSON Schema Structure:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["architecture"],
  "properties": {
    "architecture": {
      "type": "object",
      "required": ["name", "components"],
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" },
        "components": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "type"],
            "properties": {
              "id": { "type": "string" },
              "type": { "type": "string" },
              "name": { "type": "string" },
              "aws_service": { "type": "string" },
              "properties": { "type": "object" }
            }
          }
        },
        "relationships": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["from", "to"],
            "properties": {
              "from": { "type": "string" },
              "to": { "type": "string" },
              "type": { "type": "string" },
              "description": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

**Example Valid Architecture:**
```json
{
  "architecture": {
    "name": "Three-Tier Web Application",
    "components": [
      {"id": "alb", "type": "load_balancer", "aws_service": "ALB"},
      {"id": "web", "type": "compute", "aws_service": "EC2"},
      {"id": "db", "type": "database", "aws_service": "RDS"}
    ],
    "relationships": [
      {"from": "alb", "to": "web", "type": "routes_to"},
      {"from": "web", "to": "db", "type": "queries"}
    ]
  }
}
```

**Gotchas:**
- Schema should be flexible — don't over-constrain
- Allow additional properties for extensibility
- Handle JSON extraction from markdown code blocks

## Dependencies

- **Blocked by:** None (can parallelize with 001)
- **Blocks:** 003 (needs validators for scorer integration)

## Verification

```bash
uv run pytest tests/test_diagram_validators.py::TestJSONValidation -v
```
