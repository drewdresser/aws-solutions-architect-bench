# CDK Synthesis Prompt Contract

This document specifies the format and expectations for CDK synthesis evaluation items in SA Bench.

## Overview

CDK synthesis evaluations test whether models can generate valid AWS CDK code that successfully compiles into CloudFormation templates. This is a binary evaluation: either `cdk synth` succeeds or it fails.

## Input Format

### Prompt Structure

Each CDK prompt follows a consistent structure:

1. **Language specification**: Explicitly mentions Python
2. **Framework version**: Specifies AWS CDK v2 (aws-cdk-lib)
3. **Requirements**: Describes what infrastructure to create
4. **Output expectation**: Requests "a complete CDK app that can be synthesized"

### Example Prompts

**Beginner:**
```
Write a Python AWS CDK v2 app to create an S3 bucket with versioning enabled.
Use AWS CDK v2 (aws-cdk-lib). The bucket should have public access blocked and
server-side encryption enabled using AES-256. Emit a complete CDK app that can
be synthesized.
```

**Intermediate:**
```
Using CDK (Python), build an event-driven architecture where an SQS queue triggers
a Lambda function that writes records to DynamoDB with on-demand capacity and
point-in-time recovery. Use AWS CDK v2. Emit a complete CDK app that can be synthesized.
```

**Advanced:**
```
Write a Python AWS CDK v2 app to deploy a highly available, enterprise-grade
containerized application using the following components: [detailed multi-service
architecture requirements]. Use AWS CDK v2 (aws-cdk-lib). Emit a complete CDK app
that can be synthesized.
```

## Expected Output

Model responses should include:

### Required Elements

1. **Imports**: All necessary CDK and construct library imports
2. **Stack class**: A class inheriting from `Stack`
3. **App instantiation**: `App()` object creation
4. **Stack instantiation**: Stack added to the app
5. **Synthesis call**: `app.synth()` at the end

### Minimal Valid Structure

```python
from aws_cdk import App, Stack
from constructs import Construct

class MyStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Resources defined here

app = App()
MyStack(app, "MyStack")
app.synth()
```

### Code Format

- Code should be extractable from markdown code blocks
- Multiple code blocks are acceptable (will be concatenated)
- Explanatory text outside code blocks is ignored during evaluation

## Evaluation Criteria

### Pass Condition

The evaluation passes if and only if:
1. Python code can be extracted from the response
2. The code can be written to `app.py`
3. `cdk synth` exits with code 0
4. Valid CloudFormation template is produced

### Fail Conditions

The evaluation fails if any of the following occur:
- No Python code found in response
- Import errors (missing or incorrect imports)
- Syntax errors (invalid Python)
- CDK construct errors (invalid properties, missing required fields)
- Missing App/Stack structure
- Runtime errors during synthesis

### No Partial Credit

CDK evaluation is binary. A response that is "90% correct" but has one import error still fails. This reflects real-world behavior: CDK code either synthesizes or it doesn't.

## Metadata Schema

Each evaluation item includes structured metadata:

```json
{
  "id": "cdk_XXX",
  "input": "Write a Python AWS CDK v2 app...",
  "target": null,
  "metadata": {
    "difficulty": "beginner|intermediate|advanced",
    "domains": ["networking", "security", ...],
    "aws_services": ["VPC", "Lambda", ...],
    "cdk_constructs": ["Vpc", "Function", ...],
    "pattern": "optional_pattern_name",
    "skill": "legacy_domain_tag"
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (integer for legacy items, `cdk_XXX` for new) |
| `input` | string | The prompt presented to the model |
| `target` | null | Always null for CDK items (evaluation is synthesis-based) |
| `difficulty` | string | `beginner`, `intermediate`, or `advanced` |
| `domains` | array | Primary domain categories (1-3 domains) |
| `aws_services` | array | AWS services used in the solution |
| `cdk_constructs` | array | CDK construct names expected (new items only) |
| `pattern` | string | Optional architectural pattern name |
| `skill` | string | Legacy domain tag for backwards compatibility |

## Difficulty Levels

### Beginner
- **Scope**: Single service or simple 2-service pattern
- **Complexity**: Basic configuration options
- **Examples**: S3 bucket, Lambda function, DynamoDB table
- **Expected constructs**: 1-3

### Intermediate
- **Scope**: 2-4 AWS services working together
- **Complexity**: Cross-service integrations, common patterns
- **Examples**: API Gateway + Lambda + DynamoDB, VPC with NAT Gateway
- **Expected constructs**: 3-8

### Advanced
- **Scope**: 5+ AWS services in complex architecture
- **Complexity**: Enterprise patterns, HA/DR, security hardening
- **Examples**: Multi-AZ ECS deployment, event-driven pipeline, data lake
- **Expected constructs**: 8+

## Domain Categories

| Domain | Description | Example Services |
|--------|-------------|------------------|
| `networking` | VPC, subnets, routing | VPC, NAT Gateway, Transit Gateway |
| `security` | Encryption, access control | KMS, WAF, GuardDuty |
| `serverless` | Functions, managed compute | Lambda, API Gateway, Step Functions |
| `containers` | Container orchestration | ECS, EKS, Fargate |
| `database` | Data storage | RDS, DynamoDB, Aurora |
| `analytics` | Data processing | Glue, Athena, Kinesis |
| `ml` | Machine learning | SageMaker |
| `edge` | Content delivery | CloudFront, Lambda@Edge |
| `observability` | Monitoring, logging | CloudWatch, CloudTrail |
| `cost_optimization` | Cost management | Budgets |
| `ci_cd` | Deployment pipelines | CodePipeline, CodeBuild |
| `multi_account` | Organization patterns | Organizations, SCPs |
| `event_driven` | Event processing | EventBridge, SQS, SNS |
| `high_availability` | Resilience patterns | Multi-AZ, Auto Scaling |
| `orchestration` | Workflow management | Step Functions |
| `storage` | Object/file storage | S3, EFS |
| `global` | Multi-region patterns | Global Tables, Route 53 |
| `identity` | Authentication | Cognito, IAM |
| `messaging` | Message queuing | SQS, SNS, MQ |

## Dataset Statistics

As of the current version:

| Metric | Value |
|--------|-------|
| Total items | 40 |
| Beginner items | 10 |
| Intermediate items | 17 |
| Advanced items | 13 |
| Unique domains | 19 |
| Unique AWS services | 53 |

## Common Failure Patterns

See [CDK_FAILURE_MODES.md](CDK_FAILURE_MODES.md) for detailed analysis of why models fail CDK synthesis, including:

1. **Missing boilerplate**: App/Stack structure omitted
2. **Import errors**: Wrong module paths or missing imports
3. **Invalid construct properties**: Using non-existent or deprecated options
4. **Extraction failures**: Code buried in explanation

## Adding New Items

When adding new items to the dataset:

1. Use `scripts/generate_cdk_items.py` or follow the schema manually
2. Ensure prompt explicitly mentions Python and CDK v2
3. End prompt with "Emit a complete CDK app that can be synthesized."
4. Include all required metadata fields
5. Spot-check that a correct solution actually synthesizes
6. Tag with appropriate difficulty, domains, and services
