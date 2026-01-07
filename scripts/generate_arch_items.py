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
Generate architecture evaluation items using OpenAI API (via OpenRouter).

Usage:
    uv run scripts/generate_arch_items.py --subtype service_identification --difficulty intermediate --count 2
    uv run scripts/generate_arch_items.py --subtype pattern_implementation --difficulty advanced --output-format plantuml --count 1
    uv run scripts/generate_arch_items.py --help
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Load environment variables
load_dotenv()

# === Constants ===

DIAGRAM_INTERPRETATION_SUBTYPES = [
    "service_identification",
    "data_flow_analysis",
    "security_assessment",
    "scalability_analysis",
    "cost_optimization",
    "architecture_critique",  # New subtype from Task 004
]

DIAGRAM_CREATION_SUBTYPES = [
    "requirements_to_architecture",
    "pattern_implementation",
    "problem_solving",
]

ALL_SUBTYPES = DIAGRAM_INTERPRETATION_SUBTYPES + DIAGRAM_CREATION_SUBTYPES

DIFFICULTIES = ["beginner", "intermediate", "advanced"]
OUTPUT_FORMATS = ["mermaid", "plantuml", "json"]

DEFAULT_OUTPUT_FILE = "evals/architecture_design/architecture_interpretation.jsonl"


# === Pydantic Models for Schema Validation ===


class ScoringCriteria(BaseModel):
    """Base scoring criteria - weights must sum to 1.0."""

    model_config = ConfigDict(extra="allow")


class ExpectedService(BaseModel):
    """Service with role description."""

    service: str
    role: str


class BaseArchItem(BaseModel):
    """Base fields common to all architecture items."""

    id: str = Field(pattern=r"^arch_\d{3}$")
    difficulty: Literal["beginner", "intermediate", "advanced"]
    input: str = Field(min_length=20)
    target: str = Field(min_length=50)
    scoring_criteria: dict[str, float]
    aws_services: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)

    @field_validator("scoring_criteria")
    @classmethod
    def validate_scoring_weights(cls, v: dict[str, float]) -> dict[str, float]:
        total = sum(v.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"scoring_criteria must sum to 1.0, got {total}")
        return v


class DiagramInterpretationItem(BaseArchItem):
    """Schema for diagram interpretation items."""

    type: Literal["diagram_interpretation"] = "diagram_interpretation"
    subtype: Literal[
        "service_identification",
        "data_flow_analysis",
        "security_assessment",
        "scalability_analysis",
        "cost_optimization",
        "architecture_critique",
    ]
    diagram_path: str = Field(pattern=r"^diagrams/")

    # Subtype-specific fields (optional based on subtype)
    expected_services: list[ExpectedService] | None = None
    expected_flow: list[str] | None = None
    expected_security_components: list[str] | None = None
    potential_improvements: list[str] | None = None
    expected_scaling_mechanisms: list[str] | None = None
    potential_bottlenecks: list[str] | None = None
    scaling_benefits: list[str] | None = None
    cost_optimization_opportunities: list[str] | None = None
    cost_factors: list[str] | None = None
    # Architecture critique fields
    expected_issues: list[str] | None = None
    expected_improvements: list[str] | None = None
    tradeoffs_to_discuss: list[str] | None = None
    waf_pillars_relevant: list[str] | None = None


class DiagramCreationItem(BaseArchItem):
    """Schema for diagram creation items."""

    type: Literal["diagram_creation"] = "diagram_creation"
    subtype: Literal[
        "requirements_to_architecture",
        "pattern_implementation",
        "problem_solving",
    ]
    output_format: Literal["mermaid", "plantuml", "json"]

    # Subtype-specific fields (optional based on subtype)
    requirements: str | None = None
    expected_components: list[str] | None = None
    architectural_principles: list[str] | None = None
    pattern: str | None = None
    constraints: list[str] | None = None
    expected_pattern_elements: list[str] | None = None
    pattern_benefits: list[str] | None = None
    problem: str | None = None
    expected_solution_elements: list[str] | None = None
    migration_phases: list[str] | None = None


# === Generation Prompts ===

SYSTEM_PROMPT = """You are an expert AWS Solutions Architect creating evaluation items for an LLM benchmark.

Generate realistic, technically accurate AWS architecture evaluation items. Each item should:
1. Use correct AWS service names (e.g., "Amazon EC2" not just "EC2")
2. Reflect real-world architectural scenarios
3. Cover diverse AWS services beyond basic EC2/RDS/Lambda
4. Have appropriately calibrated difficulty
5. Include comprehensive expected answers

Be specific with AWS terminology and ensure scenarios are technically sound."""


def get_interpretation_prompt(subtype: str, difficulty: str, domain: str | None) -> str:
    """Get prompt for generating diagram interpretation items."""
    domain_hint = f"\n\nFocus area: {domain}" if domain else ""

    subtype_guidance = {
        "service_identification": """Generate an item where the model must identify AWS services and their roles.
Include expected_services as array of {service, role} objects.
scoring_criteria should have: service_accuracy, role_explanation, completeness (summing to 1.0).""",
        "data_flow_analysis": """Generate an item where the model must trace data flow through the architecture.
Include expected_flow as array of flow step strings.
scoring_criteria should have: flow_accuracy, component_understanding, completeness (summing to 1.0).""",
        "security_assessment": """Generate an item where the model must analyze security and suggest improvements.
Include expected_security_components and potential_improvements as arrays.
scoring_criteria should have: security_identification, vulnerability_assessment, improvement_suggestions (summing to 1.0).""",
        "scalability_analysis": """Generate an item where the model must evaluate scaling mechanisms and bottlenecks.
Include expected_scaling_mechanisms, potential_bottlenecks, and scaling_benefits as arrays.
scoring_criteria should have: scaling_mechanism_identification, bottleneck_analysis, scalability_understanding (summing to 1.0).""",
        "cost_optimization": """Generate an item where the model must identify cost factors and optimization opportunities.
Include cost_optimization_opportunities and cost_factors as arrays.
scoring_criteria should have: cost_opportunity_identification, cost_factor_understanding, optimization_feasibility (summing to 1.0).""",
        "architecture_critique": """Generate an item where the model must review an architecture for issues and suggest improvements.
Include expected_issues, expected_improvements, tradeoffs_to_discuss, and waf_pillars_relevant arrays.
scoring_criteria should have: issue_identification, improvement_quality, tradeoff_analysis (summing to 1.0).
waf_pillars_relevant should include relevant Well-Architected Framework pillars: operational_excellence, security, reliability, performance_efficiency, cost_optimization, sustainability.""",
    }

    difficulty_guidance = {
        "beginner": "Simple architecture with 3-5 services. Focus on common patterns.",
        "intermediate": "Moderate complexity with 5-8 services. Include some advanced patterns.",
        "advanced": "Complex multi-service architecture with 8+ services. Include edge cases and nuanced trade-offs.",
    }

    return f"""Generate a diagram interpretation evaluation item.

Type: diagram_interpretation
Subtype: {subtype}
Difficulty: {difficulty}

{subtype_guidance[subtype]}

Difficulty guidance: {difficulty_guidance[difficulty]}
{domain_hint}

Required fields:
- id: Use "arch_XXX" format (will be assigned later, use arch_000 as placeholder)
- type: "diagram_interpretation"
- subtype: "{subtype}"
- difficulty: "{difficulty}"
- diagram_path: "diagrams/{difficulty}/[descriptive_name].png"
- input: The question/task for the model (20+ chars)
- target: The expected answer summary (50+ chars)
- scoring_criteria: Dict with weights summing to 1.0
- aws_services: Array of AWS service names mentioned in the scenario
- domains: Array from [compute, storage, database, networking, analytics, ml, security, serverless]

Generate a complete, valid JSON object."""


def get_creation_prompt(
    subtype: str, difficulty: str, output_format: str, scenario: str | None
) -> str:
    """Get prompt for generating diagram creation items."""
    scenario_hint = f"\n\nScenario focus: {scenario}" if scenario else ""

    subtype_guidance = {
        "requirements_to_architecture": """Generate an item where the model must design an architecture from requirements.
Include requirements string, expected_components array, and architectural_principles array.
scoring_criteria should have: requirement_adherence, component_selection, architectural_soundness (summing to 1.0).""",
        "pattern_implementation": """Generate an item where the model must implement a specific architectural pattern.
Include pattern string, constraints array, expected_pattern_elements array, and pattern_benefits array.
scoring_criteria should have: pattern_compliance, serverless_usage (or similar), fault_tolerance (summing to 1.0).""",
        "problem_solving": """Generate an item where the model must solve an architectural problem (often migration).
Include problem string, constraints array, expected_solution_elements array, and migration_phases array if applicable.
scoring_criteria should have: migration_strategy (or problem_strategy), downtime_minimization, risk_mitigation (summing to 1.0).""",
    }

    format_instruction = {
        "mermaid": "Output your architecture as a Mermaid flowchart diagram using ```mermaid code blocks.",
        "plantuml": "Output your architecture as a PlantUML component diagram using ```plantuml code blocks.",
        "json": "Output your architecture as a JSON object with 'architecture' containing 'components' (array with id, type, aws_service) and 'relationships' (array with from, to, type) using ```json code blocks.",
    }

    difficulty_guidance = {
        "beginner": "Simple requirements with 3-5 components. Clear, straightforward design.",
        "intermediate": "Moderate complexity with 5-8 components. Include HA and scaling considerations.",
        "advanced": "Complex requirements with 8+ components. Include DR, multi-region, or migration scenarios.",
    }

    return f"""Generate a diagram creation evaluation item.

Type: diagram_creation
Subtype: {subtype}
Difficulty: {difficulty}
Output format: {output_format}

{subtype_guidance[subtype]}

The input prompt MUST end with: "{format_instruction[output_format]}"

Difficulty guidance: {difficulty_guidance[difficulty]}
{scenario_hint}

Required fields:
- id: Use "arch_XXX" format (will be assigned later, use arch_000 as placeholder)
- type: "diagram_creation"
- subtype: "{subtype}"
- difficulty: "{difficulty}"
- output_format: "{output_format}"
- input: The requirements/problem for the model (include format instruction at end)
- target: The expected answer summary (50+ chars)
- scoring_criteria: Dict with weights summing to 1.0
- aws_services: Array of AWS service names expected in the solution
- domains: Array from [compute, storage, database, networking, analytics, ml, security, serverless]

Generate a complete, valid JSON object."""


# === Item Generation ===


def generate_item(
    client: OpenAI,
    subtype: str,
    difficulty: str,
    output_format: str | None = None,
    domain: str | None = None,
    scenario: str | None = None,
    model: str = "gpt-4o",
) -> dict:
    """Generate a single architecture item using OpenAI."""
    is_interpretation = subtype in DIAGRAM_INTERPRETATION_SUBTYPES

    if is_interpretation:
        user_prompt = get_interpretation_prompt(subtype, difficulty, domain)
    else:
        if not output_format:
            output_format = "mermaid"  # Default
        user_prompt = get_creation_prompt(subtype, difficulty, output_format, scenario)

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
        item_type = item.get("type")
        if item_type == "diagram_interpretation":
            DiagramInterpretationItem(**item)
        elif item_type == "diagram_creation":
            DiagramCreationItem(**item)
        else:
            return False, f"Unknown type: {item_type}"
        return True, None
    except Exception as e:
        return False, str(e)


def get_next_id(output_file: Path) -> int:
    """Get the next available ID number."""
    if not output_file.exists():
        return 10  # Start at arch_010

    existing_ids = []
    for line in output_file.read_text().strip().split("\n"):
        if line:
            item = json.loads(line)
            id_str = item.get("id", "arch_000")
            id_num = int(id_str.replace("arch_", ""))
            existing_ids.append(id_num)

    return max(existing_ids) + 1 if existing_ids else 10


def main():
    parser = argparse.ArgumentParser(
        description="Generate architecture evaluation items using OpenAI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 2 intermediate service identification items
  uv run scripts/generate_arch_items.py --subtype service_identification --difficulty intermediate --count 2

  # Generate advanced pattern implementation with PlantUML output
  uv run scripts/generate_arch_items.py --subtype pattern_implementation --difficulty advanced --output-format plantuml

  # Generate with specific domain focus
  uv run scripts/generate_arch_items.py --subtype scalability_analysis --difficulty intermediate --domain "EKS with Karpenter"

  # Dry run to preview without saving
  uv run scripts/generate_arch_items.py --subtype service_identification --difficulty beginner --dry-run
        """,
    )

    parser.add_argument(
        "--subtype",
        required=True,
        choices=ALL_SUBTYPES,
        help="Item subtype to generate",
    )
    parser.add_argument(
        "--difficulty",
        required=True,
        choices=DIFFICULTIES,
        help="Difficulty level",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of items to generate (default: 1)",
    )
    parser.add_argument(
        "--output-format",
        choices=OUTPUT_FORMATS,
        help="Output format for diagram creation items (default: mermaid)",
    )
    parser.add_argument(
        "--domain",
        help="Optional domain focus (e.g., 'data analytics', 'EKS', 'ML services')",
    )
    parser.add_argument(
        "--scenario",
        help="Optional scenario focus for creation items",
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

    # Validate output format requirement
    if args.subtype in DIAGRAM_CREATION_SUBTYPES and not args.output_format:
        args.output_format = "mermaid"
        print(f"Note: Using default output_format 'mermaid' for diagram creation item")

    # Initialize OpenAI client (via OpenRouter)
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set OPENROUTER_API_KEY or OPENAI_API_KEY environment variable", file=sys.stderr)
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
                subtype=args.subtype,
                difficulty=args.difficulty,
                output_format=args.output_format,
                domain=args.domain,
                scenario=args.scenario,
                model=args.model,
            )

            # Assign proper ID
            item["id"] = f"arch_{next_id + i:03d}"

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
        print(f"  - {item['id']}: {item['subtype']} ({item['difficulty']})", file=sys.stderr)


if __name__ == "__main__":
    main()
