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
Generate AWS Solutions Architect MCQ items using OpenAI API (via OpenRouter).

Usage:
    uv run scripts/generate_mcq_items.py --domain networking --difficulty sa_associate --count 2
    uv run scripts/generate_mcq_items.py --domain security --difficulty sa_pro --multi-select --count 1
    uv run scripts/generate_mcq_items.py --help
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator

# Load environment variables
load_dotenv()

# === Constants ===

DOMAINS = [
    # Original domains
    "compute",
    "storage",
    "networking",
    "security",
    "database",
    "serverless",
    "messaging",
    "high_availability",
    "scaling",
    "cost",
    "cost_management",
    "iam",
    "operations",
    "big_data",
    "architecture",
    "global_architecture",
    "modernization",
    # New domains
    "compliance",
    "data_analytics",
    "disaster_recovery",
    "integration",
    "migration",
    "ml_ai",
    "monitoring",
    "management",
]

DIFFICULTIES = ["sa_associate", "sa_pro"]

DEFAULT_OUTPUT_FILE = "evals/practice_exam/aws_sa.jsonl"


# === Pydantic Models for Schema Validation ===


class MCQMetadata(BaseModel):
    """Metadata for MCQ items."""

    difficulty: Literal["sa_associate", "sa_pro"]
    domain: str
    aws_services: list[str] = Field(default_factory=list)


class MCQItem(BaseModel):
    """Schema for MCQ items."""

    input: str = Field(min_length=50, description="Question text")
    choices: list[str] = Field(min_length=4, max_length=6)
    target: str | list[str]
    metadata: MCQMetadata

    @field_validator("choices")
    @classmethod
    def validate_choices(cls, v: list[str]) -> list[str]:
        # Ensure choices have letter prefixes
        for i, choice in enumerate(v):
            expected_prefix = f"{chr(65 + i)}."  # A., B., C., etc.
            if not choice.startswith(expected_prefix):
                # Try to fix if missing prefix
                if not choice[0:2].endswith("."):
                    v[i] = f"{expected_prefix} {choice}"
        return v

    @field_validator("target")
    @classmethod
    def validate_target(cls, v: str | list[str]) -> str | list[str]:
        valid_letters = ["A", "B", "C", "D", "E", "F"]
        if isinstance(v, list):
            for letter in v:
                if letter not in valid_letters:
                    raise ValueError(f"Invalid target letter: {letter}")
        else:
            if v not in valid_letters:
                raise ValueError(f"Invalid target letter: {v}")
        return v


# === Generation Prompts ===

SYSTEM_PROMPT = """You are an expert AWS Solutions Architect exam question writer. Create realistic, technically accurate AWS certification-style questions.

Your questions should:
1. Use correct AWS service names and terminology
2. Present realistic enterprise scenarios
3. Have clear, unambiguous correct answers
4. Include plausible but incorrect distractors
5. Follow the style of official AWS certification exams
6. Test understanding of AWS best practices and Well-Architected Framework principles

For SA Associate questions:
- Focus on single-service or basic multi-service scenarios
- Test foundational AWS knowledge
- Keep scenarios straightforward

For SA Professional questions:
- Focus on complex, multi-service architectures
- Include constraints (cost, latency, compliance, RTO/RPO)
- Test advanced decision-making and trade-off analysis
- Present enterprise-scale scenarios"""


def get_mcq_prompt(
    domain: str,
    difficulty: str,
    multi_select: bool,
    topic: str | None = None,
) -> str:
    """Get prompt for generating MCQ items."""
    topic_hint = f"\n\nSpecific topic focus: {topic}" if topic else ""

    difficulty_guidance = {
        "sa_associate": """
Associate-level guidance:
- Focus on foundational AWS knowledge
- Single-service or basic integrations
- Straightforward scenarios
- Test understanding of when to use specific services
- 4 answer choices""",
        "sa_pro": """
Professional-level guidance:
- Complex multi-service architectures
- Enterprise-scale scenarios with constraints
- Trade-off analysis between multiple valid approaches
- Include specific requirements (cost, latency, compliance, RTO/RPO)
- May have 4-5 answer choices
- Test advanced architectural decision-making""",
    }

    if multi_select:
        selection_guidance = """
Multi-select question requirements:
- Include "(Select TWO.)" or "(Select THREE.)" at the end of the question
- Provide 5-6 answer choices
- Have exactly 2-3 correct answers
- target field should be an array like ["A", "B"] or ["A", "C", "E"]"""
    else:
        selection_guidance = """
Single-select question requirements:
- One clearly correct answer
- 4 answer choices (A, B, C, D)
- target field should be a single letter like "A" or "C" """

    return f"""Generate an AWS Solutions Architect certification-style multiple choice question.

Domain: {domain}
Difficulty: {difficulty}
{difficulty_guidance[difficulty]}
{selection_guidance}
{topic_hint}

Required JSON structure:
{{
  "input": "Full question text including any selection instructions like (Select TWO.)",
  "choices": ["A. First option", "B. Second option", "C. Third option", "D. Fourth option"],
  "target": "B" or ["A", "C"] for multi-select,
  "metadata": {{
    "difficulty": "{difficulty}",
    "domain": "{domain}",
    "aws_services": ["Amazon EC2", "Amazon S3", ...]  // List all AWS services mentioned
  }}
}}

Important:
- Each choice MUST start with its letter prefix (A., B., C., D., E., F.)
- aws_services should list the official AWS service names mentioned in the question
- Question must be technically accurate per current AWS best practices
- Distractors should be plausible but clearly incorrect to an expert

Generate a complete, valid JSON object."""


# === Item Generation ===


def generate_item(
    client: OpenAI,
    domain: str,
    difficulty: str,
    multi_select: bool = False,
    topic: str | None = None,
    model: str = "openai/gpt-4o",
) -> dict:
    """Generate a single MCQ item using OpenAI."""
    user_prompt = get_mcq_prompt(domain, difficulty, multi_select, topic)

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
        MCQItem(**item)
        return True, None
    except Exception as e:
        return False, str(e)


def get_item_count(output_file: Path) -> int:
    """Get the current number of items in the file."""
    if not output_file.exists():
        return 0

    count = 0
    for line in output_file.read_text().strip().split("\n"):
        if line:
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Generate AWS SA MCQ items using OpenAI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 2 Associate networking questions
  uv run scripts/generate_mcq_items.py --domain networking --difficulty sa_associate --count 2

  # Generate a Pro security question (multi-select)
  uv run scripts/generate_mcq_items.py --domain security --difficulty sa_pro --multi-select

  # Generate with specific topic focus
  uv run scripts/generate_mcq_items.py --domain disaster_recovery --difficulty sa_pro --topic "Multi-region active-active with RPO < 1 minute"

  # Dry run to preview without saving
  uv run scripts/generate_mcq_items.py --domain compute --difficulty sa_associate --dry-run
        """,
    )

    parser.add_argument(
        "--domain",
        required=True,
        choices=DOMAINS,
        help="AWS domain for the question",
    )
    parser.add_argument(
        "--difficulty",
        required=True,
        choices=DIFFICULTIES,
        help="Difficulty level (sa_associate or sa_pro)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of items to generate (default: 1)",
    )
    parser.add_argument(
        "--multi-select",
        action="store_true",
        help="Generate multi-select questions (Select TWO/THREE)",
    )
    parser.add_argument(
        "--topic",
        help="Optional specific topic focus for the question",
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
    current_count = get_item_count(output_path)

    generated_items = []
    for i in range(args.count):
        print(f"Generating item {i + 1}/{args.count}...", file=sys.stderr)

        try:
            item = generate_item(
                client=client,
                domain=args.domain,
                difficulty=args.difficulty,
                multi_select=args.multi_select,
                topic=args.topic,
                model=args.model,
            )

            # Validate
            valid, error = validate_item(item)
            if not valid:
                print(f"  Warning: Validation failed: {error}", file=sys.stderr)
                print(f"  Item: {json.dumps(item, indent=2)}", file=sys.stderr)
                continue

            generated_items.append(item)
            q_type = "multi-select" if args.multi_select else "single-select"
            print(
                f"  Generated: {args.domain}/{args.difficulty} ({q_type})",
                file=sys.stderr,
            )

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
            f"\nAppended {len(generated_items)} items to {output_path}",
            file=sys.stderr,
        )
        print(f"Total items now: {current_count + len(generated_items)}", file=sys.stderr)

    # Print summary
    print(f"\nGenerated {len(generated_items)} item(s):", file=sys.stderr)
    for item in generated_items:
        target = item["target"]
        q_type = "multi" if isinstance(target, list) else "single"
        print(
            f"  - {item['metadata']['domain']}/{item['metadata']['difficulty']} ({q_type})",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
