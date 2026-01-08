#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "openai>=1.0",
#   "pydantic>=2.0",
#   "python-dotenv>=1.0",
# ]
# ///
"""
Generate CDK synthesis evaluation items using OpenAI API (via OpenRouter).

Usage:
    uv run scripts/generate_cdk_items.py --difficulty beginner --domain serverless --count 2
    uv run scripts/generate_cdk_items.py --difficulty advanced --domain containers --count 1
    uv run scripts/generate_cdk_items.py --help
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field

# Load environment variables
load_dotenv()

# === Constants ===

DOMAINS = [
    "networking",
    "security",
    "serverless",
    "containers",
    "database",
    "analytics",
    "ml",
    "edge",
    "observability",
    "cost_optimization",
    "ci_cd",
    "multi_account",
    "event_driven",
    "high_availability",
    "orchestration",
    "storage",
    "global",
    "identity",
    "messaging",
]

DIFFICULTIES = ["beginner", "intermediate", "advanced"]

DEFAULT_OUTPUT_FILE = "evals/cdk_synth/cdk_synth.jsonl"


# === Pydantic Models for Schema Validation ===


class CDKMetadata(BaseModel):
    """Metadata for CDK items."""

    model_config = ConfigDict(extra="allow")

    difficulty: Literal["beginner", "intermediate", "advanced"]
    domains: list[str] = Field(min_length=1)
    aws_services: list[str] = Field(min_length=1)
    cdk_constructs: list[str] = Field(default_factory=list)
    pattern: str | None = None
    skill: str | None = None  # Legacy field for backwards compatibility


class CDKItem(BaseModel):
    """Schema for CDK synthesis items."""

    id: str = Field(pattern=r"^cdk_\d{3}$")
    input: str = Field(min_length=50)
    target: None = None  # CDK items always have null target
    metadata: CDKMetadata


# === Generation Prompts ===

SYSTEM_PROMPT = """You are an expert AWS Solutions Architect creating CDK synthesis evaluation items for an LLM benchmark.

Generate realistic, technically accurate CDK prompts that:
1. Explicitly specify Python and AWS CDK v2 (aws-cdk-lib)
2. Request "a complete CDK app that can be synthesized"
3. Have clear, unambiguous requirements
4. Cover realistic infrastructure patterns
5. Include enough detail for deterministic evaluation
6. Do NOT require external resources (existing VPCs, databases, etc.)

Each prompt should be self-contained and synthesizable without external dependencies."""


def get_generation_prompt(difficulty: str, domain: str) -> str:
    """Get prompt for generating CDK items."""

    difficulty_guidance = {
        "beginner": """Generate a BEGINNER level CDK item:
- Single service or simple 2-service pattern
- Basic configuration options
- Common, well-documented patterns
- Examples: S3 bucket with versioning, simple Lambda function, basic DynamoDB table

Keep the prompt straightforward but include enough detail that the solution is unambiguous.""",
        "intermediate": """Generate an INTERMEDIATE level CDK item:
- 2-4 AWS services working together
- Common architectural patterns
- Include cross-service integrations
- Examples: API Gateway + Lambda + DynamoDB, VPC with NAT Gateway, ECS Fargate service

The prompt should describe a realistic use case with clear requirements.""",
        "advanced": """Generate an ADVANCED level CDK item:
- 5+ AWS services in a complex architecture
- Enterprise-grade patterns
- Include security, HA, or DR considerations
- Examples: Multi-AZ deployment with auto-scaling, event-driven pipeline, blue-green deployment

The prompt should describe a sophisticated scenario but remain synthesizable.""",
    }

    domain_examples = {
        "networking": "VPC, Subnets, NAT Gateway, Transit Gateway, PrivateLink, Security Groups",
        "security": "KMS, Secrets Manager, WAF, Security Hub, GuardDuty, IAM roles/policies",
        "serverless": "Lambda, API Gateway, EventBridge, Step Functions, SQS, SNS",
        "containers": "ECS, Fargate, ECR, EKS, App Runner, ALB",
        "database": "RDS, Aurora, DynamoDB, ElastiCache, DocumentDB, Neptune",
        "analytics": "S3, Glue, Athena, Kinesis, QuickSight, Lake Formation",
        "ml": "SageMaker, Comprehend, Rekognition, Textract, Bedrock",
        "edge": "CloudFront, Lambda@Edge, Global Accelerator, Route 53",
        "observability": "CloudWatch, CloudTrail, X-Ray, OpenSearch, Config",
        "cost_optimization": "Budgets, Cost Explorer, Savings Plans, spot instances",
        "ci_cd": "CodePipeline, CodeBuild, CodeDeploy, CodeCommit, Artifact",
        "multi_account": "Organizations, Control Tower, RAM, Transit Gateway",
        "event_driven": "EventBridge, SQS, SNS, Kinesis, Lambda triggers",
        "high_availability": "Multi-AZ, Auto Scaling, Route 53 failover, Global Tables",
        "orchestration": "Step Functions, Batch, ECS tasks, EventBridge Scheduler",
        "storage": "S3, EFS, FSx, Storage Gateway, Backup",
        "global": "Global Tables, CloudFront, Route 53 geolocation, multi-region",
        "identity": "Cognito, IAM Identity Center, Directory Service",
        "messaging": "SQS, SNS, EventBridge, MQ, MSK",
    }

    domain_hint = domain_examples.get(domain, domain)

    return f"""Generate a CDK synthesis evaluation item.

Difficulty: {difficulty}
Domain: {domain}
Related services: {domain_hint}

{difficulty_guidance[difficulty]}

IMPORTANT REQUIREMENTS FOR THE PROMPT:
1. The prompt MUST start with "Write a Python AWS CDK v2 app" or similar
2. The prompt MUST include "Use AWS CDK v2 (aws-cdk-lib)"
3. The prompt MUST end with "Emit a complete CDK app that can be synthesized."
4. The prompt should specify what resources to create
5. Do NOT include requirements that need external resources

Generate a JSON object with these fields:
- id: Use "cdk_000" as placeholder (will be reassigned)
- input: The complete prompt for the model (50+ chars, must follow requirements above)
- target: null
- metadata:
  - difficulty: "{difficulty}"
  - domains: Array of domain tags from {DOMAINS[:10]}... (1-3 domains)
  - aws_services: Array of AWS service names (e.g., "VPC", "Lambda", "S3")
  - cdk_constructs: Array of CDK construct names (e.g., "Vpc", "Function", "Bucket")
  - pattern: Optional pattern name (e.g., "three_tier", "event_driven", "data_lake")

Generate a complete, valid JSON object."""


# === Item Generation ===


def generate_item(
    client: OpenAI,
    difficulty: str,
    domain: str,
    model: str = "openai/gpt-4o",
) -> dict:
    """Generate a single CDK item using OpenAI."""
    user_prompt = get_generation_prompt(difficulty, domain)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from API")

        return json.loads(content)
    except Exception as e:
        print(f"  API Error: {e}", file=sys.stderr)
        raise


def validate_item(item: dict) -> tuple[bool, str | None]:
    """Validate an item against its schema."""
    try:
        CDKItem(**item)
        return True, None
    except Exception as e:
        return False, str(e)


def get_next_id(output_file: Path) -> int:
    """Get the next available ID number."""
    if not output_file.exists():
        return 20  # Start at cdk_020 (after existing 0-19)

    existing_ids = []
    for line in output_file.read_text().strip().split("\n"):
        if line:
            item = json.loads(line)
            id_val = item.get("id")
            if isinstance(id_val, int):
                existing_ids.append(id_val)
            elif isinstance(id_val, str) and id_val.startswith("cdk_"):
                existing_ids.append(int(id_val.replace("cdk_", "")))

    return max(existing_ids) + 1 if existing_ids else 20


def main():
    parser = argparse.ArgumentParser(
        description="Generate CDK synthesis evaluation items using OpenAI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 2 beginner serverless items
  uv run scripts/generate_cdk_items.py --difficulty beginner --domain serverless --count 2

  # Generate advanced containers item
  uv run scripts/generate_cdk_items.py --difficulty advanced --domain containers

  # Dry run to preview without saving
  uv run scripts/generate_cdk_items.py --difficulty intermediate --domain database --dry-run
        """,
    )

    parser.add_argument(
        "--difficulty",
        required=True,
        choices=DIFFICULTIES,
        help="Difficulty level",
    )
    parser.add_argument(
        "--domain",
        required=True,
        choices=DOMAINS,
        help="Domain/skill area",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of items to generate (default: 1)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output JSONL file (default: {DEFAULT_OUTPUT_FILE})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated items without saving",
    )
    parser.add_argument(
        "--model",
        default="openai/gpt-4o",
        help="Model to use via OpenRouter (default: openai/gpt-4o)",
    )

    args = parser.parse_args()

    # Initialize OpenAI client (via OpenRouter)
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            "Error: Set OPENROUTER_API_KEY or OPENAI_API_KEY environment variable",
            file=sys.stderr,
        )
        sys.exit(1)

    # Use OpenRouter if OPENROUTER_API_KEY is set
    if os.environ.get("OPENROUTER_API_KEY"):
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
    else:
        client = OpenAI(api_key=api_key)

    output_path = Path(args.output)
    next_id = get_next_id(output_path)

    generated_items = []
    for i in range(args.count):
        print(f"Generating item {i + 1}/{args.count}...", file=sys.stderr)

        try:
            item = generate_item(
                client=client,
                difficulty=args.difficulty,
                domain=args.domain,
                model=args.model,
            )

            # Assign proper ID
            item["id"] = f"cdk_{next_id + i:03d}"

            # Ensure target is null
            item["target"] = None

            # Add legacy skill field for backwards compatibility
            if "metadata" in item and "skill" not in item["metadata"]:
                item["metadata"]["skill"] = args.domain

            # Validate
            valid, error = validate_item(item)
            if not valid:
                print(f"  Warning: Validation failed: {error}", file=sys.stderr)
                print(f"  Item: {json.dumps(item, indent=2)}", file=sys.stderr)
                continue

            generated_items.append(item)
            print(f"  Generated: {item['id']}", file=sys.stderr)

        except Exception as e:
            print(f"  Error generating item: {e}", file=sys.stderr)
            continue

    if not generated_items:
        print("No valid items generated.", file=sys.stderr)
        sys.exit(1)

    # Output results
    if args.dry_run:
        print("\n=== Dry Run - Generated Items ===\n")
        for item in generated_items:
            print(json.dumps(item, indent=2))
            print()
    else:
        # Append to output file
        with open(output_path, "a") as f:
            for item in generated_items:
                f.write(json.dumps(item) + "\n")
        print(
            f"\nAppended {len(generated_items)} items to {output_path}", file=sys.stderr
        )

    # Print summary
    print(f"\nGenerated {len(generated_items)} item(s):", file=sys.stderr)
    for item in generated_items:
        print(
            f"  - {item['id']}: {args.domain} ({item['metadata']['difficulty']})",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
