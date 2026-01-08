# Task: Expand Professional-Level Questions

**Epic:** [expand-mcq-dataset.md](../epics/expand-mcq-dataset.md)
**Size:** `M`
**Status:** `Done`

## Context

The dataset currently has 10 Professional-level questions. To reach 50+ total questions with balanced coverage, we need approximately 15 more Pro questions covering advanced scenarios, multi-service architectures, and complex decision-making.

## Acceptance Criteria

- [ ] Generate 15 new SA Professional-level questions using the generation script
- [ ] Coverage across advanced domains and scenarios:
  - [ ] disaster_recovery (2 questions) — Multi-region DR, pilot light, warm standby
  - [ ] compliance (2 questions) — Multi-account compliance, audit trails
  - [ ] integration (2 questions) — Complex API patterns, service mesh
  - [ ] ml_ai (2 questions) — SageMaker pipelines, Bedrock integration
  - [ ] data_analytics (2 questions) — Data lake architecture, streaming analytics
  - [ ] Additional security (2 questions) — Cross-account access, advanced IAM
  - [ ] Additional serverless (1 question) — Complex event-driven patterns
  - [ ] Additional architecture (2 questions) — Cost optimization at scale, hybrid architectures
- [ ] Mix of single-select (8) and multi-select (7) questions
- [ ] Questions pass schema validation
- [ ] Questions involve complex, multi-service scenarios typical of Pro exam

## Technical Notes

**Relevant Files:**
- `scripts/generate_mcq_items.py` — Generation script from Task 001
- `evals/practice_exam/aws_sa.jsonl` — Append to this file

**Target Coverage Breakdown:**

| Domain | Current Pro | Add | Total |
|--------|-------------|-----|-------|
| disaster_recovery | 0 | 2 | 2 |
| compliance | 0 | 2 | 2 |
| integration | 0 | 2 | 2 |
| ml_ai | 0 | 2 | 2 |
| data_analytics | 0 | 2 | 2 |
| security | 1 | 2 | 3 |
| serverless | 1 | 1 | 2 |
| architecture | 1 | 2 | 3 |

**Professional Question Characteristics:**
- Multi-service integration scenarios
- Trade-off analysis between multiple valid approaches
- Cost optimization at enterprise scale
- Security and compliance in complex environments
- Disaster recovery with specific RTO/RPO requirements
- Cross-account and cross-region architectures

**Example Generation Commands:**
```bash
# Generate Pro disaster recovery question
uv run scripts/generate_mcq_items.py \
  --domain disaster_recovery \
  --difficulty sa_pro \
  --topic "Multi-region active-active disaster recovery with RPO < 1 minute" \
  --count 1

# Generate Pro ML question (multi-select)
uv run scripts/generate_mcq_items.py \
  --domain ml_ai \
  --difficulty sa_pro \
  --topic "SageMaker MLOps pipeline with model monitoring" \
  --multi-select \
  --count 1
```

**Approach:**
1. Run generation script for each domain/topic combination
2. Review generated questions for technical accuracy and appropriate complexity
3. Ensure questions reflect real Pro exam complexity
4. Append to JSONL file

**Gotchas:**
- Pro questions should involve multiple AWS services working together
- Scenarios should include constraints (cost, latency, compliance requirements)
- Multi-select questions should have 5-6 choices with 2-3 correct answers
- Avoid questions that could be solved with basic knowledge

## Dependencies

- **Blocked by:** Task 001 (create-generation-script)
- **Blocks:** Task 005 (review-and-tag)

## Verification

```bash
# Count Professional questions
grep '"difficulty": "sa_pro"' evals/practice_exam/aws_sa.jsonl | wc -l
# Should be 25 (10 existing + 15 new)

# Validate JSONL
python -c "import json; lines=[json.loads(l) for l in open('evals/practice_exam/aws_sa.jsonl')]; print(f'{len(lines)} items')"

# Check domain distribution for Pro
grep -o '"difficulty": "sa_pro"' evals/practice_exam/aws_sa.jsonl -A1 | grep domain | sort | uniq -c
```
