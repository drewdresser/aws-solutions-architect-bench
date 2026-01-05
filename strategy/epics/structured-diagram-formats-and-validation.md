# Epic: Structured Diagram Formats and Validation

## User Value

Diagram generation tasks produce outputs in standardized formats (Mermaid/PlantUML/JSON) that can be automatically validated, making scores more objective and enabling visual rendering of generated architectures.

## Success Criteria

- [ ] Diagram generation tasks specify required output format (Mermaid, PlantUML, or JSON schema)
- [ ] Automatic structural validation: output parses correctly
- [ ] Required nodes/edges validation: key components present
- [ ] Documentation of accepted formats and validation rules
- [ ] Sample valid/invalid outputs for each format

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

<!-- Tasks will be created just-in-time when work begins -->
- [ ] _Tasks to be defined when epic starts_

## Status

`Not Started`
