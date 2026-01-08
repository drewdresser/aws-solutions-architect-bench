# Task: Generate Beginner-Level CDK Items

**Epic:** [expand-cdk-dataset.md](../epics/expand-cdk-dataset.md)
**Size:** `M`
**Status:** `Done`

## Context

The current CDK dataset has 20 items, all at intermediate/advanced difficulty. Adding beginner-level items provides a foundation for measuring basic CDK competency and creates a difficulty gradient for more meaningful evaluation.

## Acceptance Criteria

- [x] 10 new beginner-level CDK items added to dataset
- [x] Items cover single-service or simple 2-service patterns
- [x] Each item tagged with domains, aws_services, difficulty
- [x] Items are validated to synthesize successfully (at least manually spot-check 3)
- [x] Coverage includes: S3, Lambda, DynamoDB, SNS, SQS, API Gateway basics

## Technical Notes

**Target File:**
- `evals/cdk_synth/cdk_synth.jsonl`

**Beginner Pattern Examples:**

1. **S3 Static Website**
   - S3 bucket with website hosting enabled
   - Bucket policy for public read

2. **Simple Lambda Function**
   - Lambda function with inline code
   - Basic IAM execution role

3. **DynamoDB Table**
   - Single table with partition key
   - On-demand billing mode

4. **SNS Topic with Email**
   - SNS topic
   - Email subscription

5. **SQS Queue**
   - Standard queue with basic configuration
   - Dead letter queue

6. **Lambda + API Gateway**
   - REST API with single endpoint
   - Lambda integration

7. **S3 + Lambda Trigger**
   - S3 bucket with event notification
   - Lambda function for processing

8. **CloudWatch Alarm**
   - Basic metric alarm
   - SNS notification

9. **IAM Role and Policy**
   - Custom IAM role
   - Inline or managed policy

10. **Secrets Manager Secret**
    - Secret with rotation disabled
    - Basic access policy

**Generation Commands:**
```bash
# Generate 2-3 items per batch, review, then continue
uv run scripts/generate_cdk_items.py --difficulty beginner --domain storage --count 2
uv run scripts/generate_cdk_items.py --difficulty beginner --domain serverless --count 3
uv run scripts/generate_cdk_items.py --difficulty beginner --domain database --count 2
uv run scripts/generate_cdk_items.py --difficulty beginner --domain messaging --count 2
uv run scripts/generate_cdk_items.py --difficulty beginner --domain security --count 1
```

**Quality Checks:**
- Prompt clearly specifies single or simple pattern
- No dependencies on existing resources
- Synthesizable without external context
- Clear success criteria in prompt

**Gotchas:**
- "Beginner" doesn't mean trivial — should still be useful CDK patterns
- Avoid prompts that are too simple (e.g., just "create a bucket")
- Include enough context for deterministic evaluation
- Verify prompts synthesize before committing

## Dependencies

- **Blocked by:** Task 001 (generation script)
- **Blocks:** Task 005

## Verification

```bash
# Count items after adding
wc -l evals/cdk_synth/cdk_synth.jsonl
# Should show 30 (20 existing + 10 new)

# Spot-check synthesis of new items
# Extract last few items and test manually
tail -3 evals/cdk_synth/cdk_synth.jsonl | jq -r '.input'
```
