# Task: Expand Associate-Level Questions

**Epic:** [expand-mcq-dataset.md](../epics/expand-mcq-dataset.md)
**Size:** `M`
**Status:** `Done`

## Context

The dataset currently has 10 Associate-level questions across 10 domains. To reach 50+ total questions with balanced coverage, we need approximately 15 more Associate questions covering underrepresented and missing domains.

## Acceptance Criteria

- [ ] Generate 15 new SA Associate-level questions using the generation script
- [ ] Coverage across missing/underrepresented domains:
  - [ ] compliance (2 questions) — GuardDuty, Security Hub, AWS Config compliance
  - [ ] data_analytics (2 questions) — Athena, QuickSight, Glue
  - [ ] disaster_recovery (2 questions) — Backup strategies, RTO/RPO
  - [ ] migration (2 questions) — DMS, Snow family, migration strategies
  - [ ] monitoring (2 questions) — CloudWatch, X-Ray, EventBridge
  - [ ] management (1 question) — Cost Explorer, Budgets, Trusted Advisor
  - [ ] Additional networking (2 questions) — VPC peering, Transit Gateway
  - [ ] Additional storage (2 questions) — EFS, FSx, Storage Gateway
- [ ] Mix of single-select (10) and multi-select (5) questions
- [ ] Questions pass schema validation
- [ ] Questions are technically accurate per AWS best practices

## Technical Notes

**Relevant Files:**
- `scripts/generate_mcq_items.py` — Generation script from Task 001
- `evals/practice_exam/aws_sa.jsonl` — Append to this file

**Target Coverage Breakdown:**

| Domain | Current Associate | Add | Total |
|--------|-------------------|-----|-------|
| networking | 2 | 2 | 4 |
| storage | 1 | 2 | 3 |
| compliance | 0 | 2 | 2 |
| data_analytics | 0 | 2 | 2 |
| disaster_recovery | 0 | 2 | 2 |
| migration | 0 | 2 | 2 |
| monitoring | 0 | 2 | 2 |
| management | 0 | 1 | 1 |

**Example Generation Commands:**
```bash
# Generate Associate networking question
uv run scripts/generate_mcq_items.py \
  --domain networking \
  --difficulty sa_associate \
  --topic "VPC Transit Gateway and VPC peering" \
  --count 1

# Generate Associate data analytics (multi-select)
uv run scripts/generate_mcq_items.py \
  --domain data_analytics \
  --difficulty sa_associate \
  --topic "Amazon Athena and S3 data lakes" \
  --multi-select \
  --count 1
```

**Approach:**
1. Run generation script for each domain/topic combination
2. Review generated questions for technical accuracy
3. Ensure question difficulty matches Associate level (foundational, less complex scenarios)
4. Append to JSONL file

**Gotchas:**
- Associate questions should focus on single-service scenarios or basic integrations
- Avoid overly complex multi-service architectures (save for Pro level)
- Ensure answers align with current AWS best practices
- Check for duplicate concepts with existing questions

## Dependencies

- **Blocked by:** Task 001 (create-generation-script)
- **Blocks:** Task 005 (review-and-tag)

## Verification

```bash
# Count Associate questions
grep '"difficulty": "sa_associate"' evals/practice_exam/aws_sa.jsonl | wc -l
# Should be 25 (10 existing + 15 new)

# Validate JSONL
python -c "import json; lines=[json.loads(l) for l in open('evals/practice_exam/aws_sa.jsonl')]; print(f'{len(lines)} items')"

# Check domain distribution for Associate
grep -o '"difficulty": "sa_associate"' evals/practice_exam/aws_sa.jsonl -A1 | grep domain | sort | uniq -c
```
