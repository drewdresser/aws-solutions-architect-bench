# Task: Create CDK Item Generation Script

**Epic:** [expand-cdk-dataset.md](../epics/expand-cdk-dataset.md)
**Size:** `M`
**Status:** `Done`

## Context

Following the pattern established by `generate_arch_items.py` and `generate_mcq_items.py`, create a script to generate new CDK synthesis prompts using OpenAI/OpenRouter API. This enables scalable dataset expansion with consistent quality.

## Acceptance Criteria

- [x] Script created at `scripts/generate_cdk_items.py`
- [x] Uses PEP723 inline script metadata (like existing generators)
- [x] Supports CLI arguments: `--domain`, `--difficulty`, `--count`, `--output`
- [x] Generates items with enhanced metadata schema (see technical notes)
- [x] Validates output against Pydantic schema before writing
- [x] Appends to JSONL file (doesn't overwrite existing items)
- [x] Uses OpenRouter API (OPENROUTER_API_KEY from .env)
- [x] Includes dry-run mode for preview

## Technical Notes

**Target File:**
- `scripts/generate_cdk_items.py`

**Reference Files:**
- `scripts/generate_arch_items.py` — Pattern to follow
- `scripts/generate_mcq_items.py` — CLI argument patterns
- `evals/cdk_synth/cdk_synth.jsonl` — Current dataset format

**Current CDK Item Schema:**
```json
{
  "id": 0,
  "input": "...",
  "target": null,
  "metadata": {
    "skill": "networking"
  }
}
```

**Enhanced Schema (new items):**
```json
{
  "id": "cdk_001",
  "input": "...",
  "target": null,
  "metadata": {
    "difficulty": "intermediate",
    "domains": ["networking", "security"],
    "aws_services": ["VPC", "SecurityGroup", "NATGateway"],
    "cdk_constructs": ["Vpc", "SubnetType", "NatGateway"],
    "pattern": "three_tier_architecture"
  }
}
```

**Domain Categories:**
- networking, security, serverless, containers, database
- analytics, ml, edge, observability, cost_optimization
- ci_cd, multi_account, event_driven, high_availability
- orchestration, storage, global

**Difficulty Levels:**
- `beginner`: Single service, simple patterns (S3 bucket, Lambda function)
- `intermediate`: 2-4 services, common patterns (API + Lambda + DynamoDB)
- `advanced`: 5+ services, complex patterns (EKS cluster, multi-region)

**System Prompt Guidance:**
```
You are an expert AWS Solutions Architect creating CDK synthesis evaluation items.
Generate prompts that:
1. Explicitly specify Python and AWS CDK v2 (aws-cdk-lib)
2. Request "a complete CDK app that can be synthesized"
3. Have clear, unambiguous requirements
4. Cover realistic infrastructure patterns
5. Include enough detail for deterministic evaluation
```

**Approach:**
1. Copy structure from `generate_arch_items.py`
2. Define CDKItem and CDKMetadata Pydantic models
3. Create domain-specific generation prompts
4. Implement ID generation (cdk_XXX format)
5. Add validation that generated items are synthesizable

**Gotchas:**
- Generated prompts must be specific enough that `cdk synth` success/failure is meaningful
- Avoid prompts that require external resources (databases, existing VPCs)
- Include version requirements (CDK v2) in generated prompts
- Balance complexity with synthesizability

## Dependencies

- **Blocked by:** None
- **Blocks:** Tasks 002, 003

## Verification

```bash
# Test script help
uv run scripts/generate_cdk_items.py --help

# Generate 1 item in dry-run mode
uv run scripts/generate_cdk_items.py --domain networking --difficulty intermediate --count 1 --dry-run

# Generate and append to dataset
uv run scripts/generate_cdk_items.py --domain serverless --difficulty beginner --count 2
```
