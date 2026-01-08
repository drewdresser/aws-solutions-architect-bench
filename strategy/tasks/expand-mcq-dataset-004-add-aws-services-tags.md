# Task: Add AWS Services Tags to Questions

**Epic:** [expand-mcq-dataset.md](../epics/expand-mcq-dataset.md)
**Size:** `S`
**Status:** `Todo`

## Context

To align with the architecture dataset and enable more granular analysis, we should add `aws_services` tags to each MCQ item. This will allow analysis of which specific AWS services are covered and identify gaps in service coverage.

## Acceptance Criteria

- [ ] Add `aws_services` array to metadata for all existing 20 questions
- [ ] Ensure all new questions (from Tasks 002-003) include `aws_services` tags
- [ ] Each question lists all AWS services mentioned in the question AND answer choices
- [ ] Use official AWS service names (e.g., "Amazon EC2" not "EC2")
- [ ] Update generation script to automatically include aws_services tags

## Technical Notes

**Relevant Files:**
- `evals/practice_exam/aws_sa.jsonl` — Update existing items
- `scripts/generate_mcq_items.py` — Ensure it generates aws_services tags

**Updated Schema:**
```json
{
  "input": "Question text...",
  "choices": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "target": "A",
  "metadata": {
    "difficulty": "sa_associate",
    "domain": "networking",
    "aws_services": ["Amazon VPC", "NAT Gateway", "Amazon EC2"]
  }
}
```

**Service Extraction Approach:**
For existing questions, extract services mentioned in:
1. The question text (input field)
2. All answer choices
3. The target answer context

**Example Service Tags:**
- Question about NAT Gateway: `["Amazon VPC", "NAT Gateway", "Amazon EC2"]`
- Question about S3 CORS: `["Amazon S3", "Amazon API Gateway"]`
- Question about Aurora read replicas: `["Amazon Aurora", "Amazon RDS"]`

**Approach:**
1. Write a utility script or manually tag existing 20 questions
2. Update generate_mcq_items.py to include aws_services extraction
3. Verify all items have the new field

**Gotchas:**
- Use official AWS naming (Amazon S3, not S3; AWS Lambda, not Lambda)
- Include services from wrong answer choices too (they're still relevant to the question)
- Some services have multiple valid names (ELB vs Elastic Load Balancing) — standardize

## Dependencies

- **Blocked by:** None (can start in parallel with Tasks 002-003)
- **Blocks:** Task 005 (review-and-tag)

## Verification

```bash
# Check all items have aws_services
python -c "
import json
items = [json.loads(l) for l in open('evals/practice_exam/aws_sa.jsonl')]
missing = [i for i in items if 'aws_services' not in i.get('metadata', {})]
print(f'Items missing aws_services: {len(missing)}')
"

# Count unique services
python -c "
import json
items = [json.loads(l) for l in open('evals/practice_exam/aws_sa.jsonl')]
services = set()
for item in items:
    services.update(item.get('metadata', {}).get('aws_services', []))
print(f'Unique AWS services: {len(services)}')
print(sorted(services))
"
```
