# Task: Expand Diagram Interpretation Items

**Epic:** [expand-architecture-dataset.md](../epics/expand-architecture-dataset.md)
**Size:** `M`
**Status:** `Done`

## Context

The dataset currently has only 5 diagram interpretation items (one per subtype). To achieve meaningful coverage and score stability, we need to expand each subtype to have 2-3 items across different difficulty levels and AWS service domains.

## Acceptance Criteria

- [ ] Generate 6-8 new diagram interpretation items using the generation script
- [ ] Coverage across all 5 subtypes: service_identification (2), data_flow_analysis (2), security_assessment (2), scalability_analysis (2), cost_optimization (2)
- [ ] Balanced difficulty: at least 2 beginner, 3 intermediate, 2 advanced
- [ ] Diverse AWS services covered (beyond EC2/RDS/Lambda):
  - [ ] At least 1 item featuring data/analytics (Kinesis, Redshift, Athena)
  - [ ] At least 1 item featuring ML services (SageMaker, Bedrock)
  - [ ] At least 1 item featuring container services (ECS, EKS, Fargate)
  - [ ] At least 1 item featuring networking (Transit Gateway, PrivateLink)
- [ ] Each item has realistic expected answers and scoring criteria
- [ ] Items pass schema validation

## Technical Notes

**Relevant Files:**
- `scripts/generate_arch_items.py` — Generation script from Task 001
- `evals/architecture_design/architecture_interpretation.jsonl` — Append to this file

**Target Item Breakdown:**

| Subtype | Current | Add | Total | Notes |
|---------|---------|-----|-------|-------|
| service_identification | 1 | 2 | 3 | Add data/analytics, ML scenarios |
| data_flow_analysis | 1 | 2 | 3 | Add event-driven, streaming scenarios |
| security_assessment | 1 | 2 | 3 | Add Zero Trust, compliance scenarios |
| scalability_analysis | 1 | 2 | 3 | Add container, multi-region scenarios |
| cost_optimization | 1 | 1-2 | 2-3 | Add FinOps, multi-account scenarios |

**Example Generation Commands:**
```bash
# Generate intermediate data analytics service identification
uv run scripts/generate_arch_items.py \
  --subtype service_identification \
  --difficulty intermediate \
  --domain "data analytics with Kinesis, Glue, and Redshift" \
  --count 1

# Generate advanced container scalability analysis
uv run scripts/generate_arch_items.py \
  --subtype scalability_analysis \
  --difficulty advanced \
  --domain "EKS with Karpenter auto-scaling" \
  --count 1
```

**Approach:**
1. Run generation script for each target combination
2. Review generated items for quality and realism
3. Adjust expected answers if needed
4. Assign sequential IDs (arch_010 through arch_017)
5. Append to JSONL file

**Gotchas:**
- diagram_path fields are placeholders (no actual images)
- Review scoring_criteria weights for balance
- Ensure expected answers are comprehensive but not excessive
- Check for duplicated concepts with existing items

## Dependencies

- **Blocked by:** Task 001 (create-generation-script)
- **Blocks:** Task 005 (review-and-tag)

## Verification

```bash
# Count interpretation items
grep '"type": "diagram_interpretation"' evals/architecture_design/architecture_interpretation.jsonl | wc -l
# Should be 11-13 (5 existing + 6-8 new)

# Validate JSONL
python -c "import json; lines=[json.loads(l) for l in open('evals/architecture_design/architecture_interpretation.jsonl')]; print(f'{len(lines)} items')"

# Check subtype distribution
grep -o '"subtype": "[^"]*"' evals/architecture_design/architecture_interpretation.jsonl | sort | uniq -c
```
