# Epic: Structured Diagram Formats and Validation

## User Value

Diagram generation tasks produce outputs in standardized formats (Mermaid/PlantUML/JSON) that can be automatically validated, making scores more objective and enabling visual rendering of generated architectures.

## Success Criteria

- [x] Diagram generation tasks specify required output format (Mermaid, PlantUML, or JSON schema)
- [x] Automatic structural validation: output parses correctly
- [x] Required nodes/edges validation: key components present
- [x] Documentation of accepted formats and validation rules
- [x] Sample valid/invalid outputs for each format

## Technical Approach

Update architecture dataset items to specify output format requirements. Implement parsers for Mermaid and PlantUML syntax validation. Create JSON schemas for structured architecture descriptions. Add validation step in scorer that checks parseability before LLM judging.

## OKR Alignment

- **Objective**: O2 — Make scoring robust and aligned with SA Bench's long-term vision
- **Key Result**: KR3 — Standardize output formats and add automatic structural validation

## Dependencies

- **Depends on**: llm-judge-architecture-scoring (works together with LLM judge)
- **Blocks**: expand-architecture-dataset (new items should use standardized formats)
- **Priority**: `Medium`

## Tasks

- [x] [001-implement-parsers](../tasks/structured-diagram-formats-001-implement-parsers.md) — Mermaid and PlantUML validators
- [x] [002-create-json-schema](../tasks/structured-diagram-formats-002-create-json-schema.md) — JSON schema for architecture descriptions
- [x] [003-integrate-validation](../tasks/structured-diagram-formats-003-integrate-validation.md) — Validation in scorer pipeline
- [x] [004-update-dataset](../tasks/structured-diagram-formats-004-update-dataset.md) — Add format requirements to dataset items
- [x] [005-create-documentation](../tasks/structured-diagram-formats-005-create-documentation.md) — Documentation and examples

## Status

`Done`
