# Task: Generate Advanced-Level CDK Items

**Epic:** [expand-cdk-dataset.md](../epics/expand-cdk-dataset.md)
**Size:** `M`
**Status:** `Done`

## Context

While most current items are intermediate, the dataset lacks truly complex enterprise patterns. Adding advanced items tests sophisticated CDK capabilities and differentiates strong models from average performers.

## Acceptance Criteria

- [x] 10 new advanced-level CDK items added to dataset
- [x] Items cover complex multi-service architectures (5+ services)
- [x] Each item tagged with domains, aws_services, difficulty
- [x] Patterns include: multi-region, compliance, DR, complex networking
- [x] Items are validated to synthesize successfully (spot-check 2-3)

## Technical Notes

**Target File:**
- `evals/cdk_synth/cdk_synth.jsonl`

**Advanced Pattern Examples:**

1. **Multi-Region Active-Active**
   - DynamoDB Global Tables
   - Route 53 latency-based routing
   - Lambda in multiple regions

2. **Zero-Trust Network Architecture**
   - VPC with private subnets only
   - PrivateLink endpoints for AWS services
   - Network Firewall

3. **Compliance-Ready Data Lake**
   - S3 with encryption, versioning, object lock
   - Macie for data classification
   - CloudTrail + Config for auditing

4. **Blue-Green ECS Deployment**
   - ECS Fargate service
   - CodeDeploy integration
   - ALB with target group switching

5. **Serverless Event Mesh**
   - EventBridge with multiple rules
   - Cross-account event patterns
   - Lambda destinations

6. **Resilient API Platform**
   - API Gateway with WAF
   - Lambda with reserved concurrency
   - DynamoDB with DAX caching

7. **ML Inference Pipeline**
   - SageMaker endpoint
   - API Gateway integration
   - CloudWatch custom metrics

8. **Multi-Account Landing Zone Pattern**
   - Control Tower concepts
   - Cross-account IAM roles
   - Centralized logging

9. **Kubernetes-Native Architecture**
   - EKS with managed node groups
   - AWS Load Balancer Controller
   - Secrets Manager CSI driver

10. **Real-Time Analytics Pipeline**
    - Kinesis Data Streams
    - Lambda for processing
    - OpenSearch for storage
    - Kinesis Firehose for delivery

**Generation Commands:**
```bash
uv run scripts/generate_cdk_items.py --difficulty advanced --domain multi_region --count 2
uv run scripts/generate_cdk_items.py --difficulty advanced --domain security --count 2
uv run scripts/generate_cdk_items.py --difficulty advanced --domain containers --count 2
uv run scripts/generate_cdk_items.py --difficulty advanced --domain analytics --count 2
uv run scripts/generate_cdk_items.py --difficulty advanced --domain serverless --count 2
```

**Quality Checks:**
- Prompt describes complex but synthesizable architecture
- Clear component relationships specified
- No runtime dependencies (existing DBs, etc.)
- Reasonable scope (synthesizable in 60 seconds)

**Gotchas:**
- Advanced doesn't mean impossible — must still synthesize
- Avoid patterns requiring account-specific resources
- Some advanced patterns may need simplified versions
- Test that synthesis completes within timeout (60s)

## Dependencies

- **Blocked by:** Task 001 (generation script)
- **Blocks:** Task 005

## Verification

```bash
# Count items after adding
wc -l evals/cdk_synth/cdk_synth.jsonl
# Should show 40 (30 after task 002 + 10 new)

# Check difficulty distribution
cat evals/cdk_synth/cdk_synth.jsonl | jq -r '.metadata.difficulty' | sort | uniq -c
```
