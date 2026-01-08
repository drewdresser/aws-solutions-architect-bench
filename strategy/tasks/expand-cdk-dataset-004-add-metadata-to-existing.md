# Task: Add Metadata to Existing CDK Items

**Epic:** [expand-cdk-dataset.md](../epics/expand-cdk-dataset.md)
**Size:** `S`
**Status:** `Done`

## Context

The existing 20 CDK items only have a `skill` field in metadata. To enable domain analysis and consistent reporting, add enhanced metadata (difficulty, domains array, aws_services) to all existing items.

## Acceptance Criteria

- [x] All 20 existing items have `difficulty` field added
- [x] All items have `domains` array (can include multiple domains)
- [x] All items have `aws_services` array listing services used
- [x] Original `skill` field preserved for backwards compatibility
- [x] Items validated (JSON syntax correct after editing)

## Technical Notes

**Target File:**
- `evals/cdk_synth/cdk_synth.jsonl`

**Current Format (item 0 example):**
```json
{
  "id": 0,
  "input": "Write a Python AWS CDK v2 app...",
  "target": null,
  "metadata": {
    "skill": "networking"
  }
}
```

**Enhanced Format:**
```json
{
  "id": 0,
  "input": "Write a Python AWS CDK v2 app...",
  "target": null,
  "metadata": {
    "skill": "networking",
    "difficulty": "intermediate",
    "domains": ["networking", "security"],
    "aws_services": ["VPC", "Subnet", "NATGateway", "SecurityGroup", "SSMParameter"]
  }
}
```

**Existing Items to Enhance (by skill/domain):**

| ID | Skill | Likely Difficulty | Key Services |
|----|-------|-------------------|--------------|
| 0 | networking | intermediate | VPC, Subnet, NAT |
| 1 | edge | intermediate | CloudFront, Lambda@Edge |
| 2 | security | intermediate | S3, KMS, Config |
| 3 | serverless | intermediate | API Gateway, Lambda |
| 4 | database | intermediate | Aurora, Secrets Manager |
| 5 | containers | intermediate | ECS, ALB, ECR |
| 6 | multi-account | advanced | Organizations, Transit Gateway |
| 7 | observability | intermediate | CloudTrail, CloudWatch |
| 8 | cost-optimization | intermediate | Budgets, SNS |
| 9 | ci/cd | intermediate | CodePipeline, CodeBuild |
| 10 | ml | advanced | SageMaker |
| 11 | event-driven | intermediate | SQS, Lambda, DynamoDB |
| 12 | high-availability | intermediate | RDS Multi-AZ |
| 13 | analytics | intermediate | S3, Glue, Athena |
| 14 | global-data | intermediate | DynamoDB Global Tables |
| 15 | kubernetes | advanced | EKS, Fargate |
| 16 | orchestration | intermediate | Step Functions |
| 17-19 | various | intermediate | (review actual content) |

**Approach:**
1. Read each item and analyze the prompt
2. Determine difficulty based on complexity
3. Extract AWS services mentioned
4. Assign multiple domains where applicable
5. Update metadata in-place

**Gotchas:**
- Preserve exact input text (no modifications)
- Keep `skill` field for backwards compatibility
- Validate JSON after each edit
- Use consistent service naming (e.g., "Lambda" not "AWS Lambda")

## Dependencies

- **Blocked by:** None (can run in parallel with other tasks)
- **Blocks:** Task 005

## Verification

```bash
# Validate all items have required fields
cat evals/cdk_synth/cdk_synth.jsonl | jq -e '.metadata | has("difficulty") and has("domains") and has("aws_services")' | grep -c true
# Should output 20

# Check JSON is valid
cat evals/cdk_synth/cdk_synth.jsonl | jq . > /dev/null && echo "Valid JSON"

# Show metadata summary
cat evals/cdk_synth/cdk_synth.jsonl | jq -r '.metadata.difficulty' | sort | uniq -c
```
