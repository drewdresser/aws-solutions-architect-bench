# Epic: LLM-as-Judge Architecture Scoring

## User Value

Architecture tasks are scored by an LLM judge with transparent rubrics, moving beyond keyword heuristics to evaluate nuanced architectural reasoning—making scores more meaningful and harder to game.

## Success Criteria

- [ ] LLM-as-judge scorer implemented for architecture track
- [ ] Published rubric document explaining scoring criteria
- [ ] At least one anti-gaming mechanism implemented (e.g., hidden test points, schema validation, adversarial checks)
- [ ] Judge agreement rate measured on sanity set (target: >=80% consistency)
- [ ] Fallback to deterministic checks where applicable (e.g., service names present)

## Technical Approach

Replace keyword-based `score_*` functions in `evals/architecture_design/tasks.py` with LLM-as-judge calls. Create explicit rubric prompts for each subtype (service identification, data flow, security, etc.). Implement multi-judge self-consistency or hidden criteria to reduce gaming. Add calibration test set to measure judge reliability.

## OKR Alignment

- **Objective**: O2 — Make scoring robust and aligned with SA Bench's long-term vision
- **Key Result**: KR1 — Implement LLM-as-judge scoring with rubrics and anti-gaming
- **Key Result**: KR2 — Establish scorer quality checks

## Dependencies

- **Depends on**: None (can start independently)
- **Blocks**: structured-diagram-formats-and-validation (LLM judge can enforce structure)
- **Priority**: `High`

## Tasks

- [x] [001-implement-judge-scorer](../tasks/llm-judge-architecture-scoring-001-implement-judge-scorer.md) — LLM-as-judge scorer infrastructure
- [x] [002-create-rubric-prompts](../tasks/llm-judge-architecture-scoring-002-create-rubric-prompts.md) — Subtype-specific rubric prompts
- [x] [003-add-anti-gaming](../tasks/llm-judge-architecture-scoring-003-add-anti-gaming.md) — Anti-gaming mechanisms
- [x] [004-calibration-tests](../tasks/llm-judge-architecture-scoring-004-calibration-tests.md) — Calibration set and agreement measurement
- [x] [005-publish-rubric-docs](../tasks/llm-judge-architecture-scoring-005-publish-rubric-docs.md) — Public rubric documentation

## Status

`Done`
