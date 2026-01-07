# Task: Review, Validate, and Tag All Items

**Epic:** [expand-architecture-dataset.md](../epics/expand-architecture-dataset.md)
**Size:** `S`
**Status:** `Done`

## Context

After generating new items, we need to review them for quality, ensure schema compliance, add consistent tagging, and verify the dataset meets the epic's success criteria.

## Acceptance Criteria

- [ ] All items pass JSON schema validation
- [ ] Total item count is 20+ (target: 22-24)
- [ ] Each item has consistent tagging:
  - [ ] `difficulty` field present (beginner/intermediate/advanced)
  - [ ] `aws_services` array added listing all AWS services mentioned
  - [ ] `domains` array added (networking/compute/storage/database/analytics/ml/security/serverless)
- [ ] Balance verification:
  - [ ] Diagram interpretation: ~13 items
  - [ ] Diagram creation: ~10 items
  - [ ] Difficulty distribution: ~6 beginner, ~10 intermediate, ~6 advanced
- [ ] No duplicate scenarios or near-duplicate content
- [ ] Expected answers are realistic and comprehensive
- [ ] Scoring criteria weights sum to 1.0 for each item

## Technical Notes

**Relevant Files:**
- `evals/architecture_design/architecture_interpretation.jsonl` — Full dataset
- `schemas/` — May need JSON schema for validation

**New Tags to Add:**
```json
{
  "aws_services": ["Amazon EC2", "Amazon RDS", "Elastic Load Balancer"],
  "domains": ["compute", "database", "networking"]
}
```

**Domain Categories:**
- `compute`: EC2, Lambda, ECS, EKS, Fargate, Batch
- `storage`: S3, EBS, EFS, FSx
- `database`: RDS, DynamoDB, Aurora, ElastiCache, Redshift
- `networking`: VPC, ALB/NLB, CloudFront, Route 53, API Gateway, Transit Gateway
- `analytics`: Kinesis, Glue, Athena, EMR, QuickSight
- `ml`: SageMaker, Bedrock, Rekognition, Comprehend
- `security`: IAM, WAF, Shield, KMS, Secrets Manager, GuardDuty
- `serverless`: Lambda, API Gateway, Step Functions, EventBridge, SNS, SQS

**Approach:**
1. Run validation script on full dataset
2. Add missing tags programmatically where possible
3. Manual review of each generated item for quality
4. Fix any issues found
5. Generate final statistics

**Validation Script Snippet:**
```python
import json
from pathlib import Path

dataset = Path("evals/architecture_design/architecture_interpretation.jsonl")
items = [json.loads(line) for line in dataset.read_text().strip().split("\n")]

# Check required fields
required = ["id", "type", "subtype", "difficulty", "input", "target", "scoring_criteria"]
for item in items:
    missing = [f for f in required if f not in item]
    if missing:
        print(f"{item['id']}: missing {missing}")

# Check scoring criteria sum
for item in items:
    total = sum(item["scoring_criteria"].values())
    if abs(total - 1.0) > 0.01:
        print(f"{item['id']}: scoring_criteria sum = {total}")

# Distribution stats
from collections import Counter
print("\nType distribution:", Counter(i["type"] for i in items))
print("Subtype distribution:", Counter(i["subtype"] for i in items))
print("Difficulty distribution:", Counter(i["difficulty"] for i in items))
```

**Gotchas:**
- Don't modify existing items unless fixing bugs
- Preserve original IDs
- Be consistent with AWS service naming (use official names)

## Dependencies

- **Blocked by:** Tasks 002, 003, 004 (all generation tasks)
- **Blocks:** None (final task)

## Verification

```bash
# Final item count
wc -l evals/architecture_design/architecture_interpretation.jsonl
# Should be 20+

# Run validation
uv run python -c "
import json
items = [json.loads(l) for l in open('evals/architecture_design/architecture_interpretation.jsonl')]
print(f'Total items: {len(items)}')
print(f'Types: {set(i[\"type\"] for i in items)}')
print(f'All have aws_services: {all(\"aws_services\" in i for i in items)}')
print(f'All have domains: {all(\"domains\" in i for i in items)}')
"

# Run the architecture eval to verify items work
uv run inspect eval evals/architecture_design/tasks.py --limit 3 --model openai/gpt-4o-mini
```
