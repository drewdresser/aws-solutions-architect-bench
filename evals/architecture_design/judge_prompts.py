"""
Rubric prompts for LLM-as-judge architecture scoring.

Each rubric provides structured guidance for evaluating architecture responses
across three dimensions: accuracy, completeness, and quality.
"""

from typing import Dict, List, Any

# Base judge system prompt
JUDGE_SYSTEM_PROMPT = """You are an expert AWS Solutions Architect evaluator. Your task is to score architecture responses on three dimensions:

1. **accuracy** (0.0-1.0): How well does the response match the expected answer and AWS best practices?
2. **completeness** (0.0-1.0): Does it cover all required elements thoroughly?
3. **quality** (0.0-1.0): Is the reasoning sound, well-structured, and professionally presented?

Be objective and consistent. Provide a brief reasoning for each score.

IMPORTANT: Return ONLY valid JSON in this exact format:
{
  "accuracy": 0.X,
  "completeness": 0.X,
  "quality": 0.X,
  "reasoning": "Brief explanation of scores"
}"""


# Rubric prompts keyed by (type, subtype)
RUBRIC_PROMPTS: Dict[tuple, str] = {
    # === DIAGRAM INTERPRETATION SUBTYPES ===
    ("diagram_interpretation", "service_identification"): """
## Task Type: Service Identification
The model was shown an AWS architecture diagram and asked to identify services and their roles.

## Expected Services
{expected_services}

## Scoring Guidance

### Accuracy (0.0-1.0)
- **0.9-1.0**: All services correctly identified with proper AWS naming (e.g., "Amazon EC2" not just "EC2")
- **0.7-0.89**: Most services identified correctly, minor naming variations acceptable
- **0.5-0.69**: Core services identified but several missing or misnamed
- **0.3-0.49**: Only obvious services identified, significant gaps
- **0.0-0.29**: Major services missing or incorrectly identified

### Completeness (0.0-1.0)
- **0.9-1.0**: Each service's role clearly explained with architectural context
- **0.7-0.89**: Roles explained for most services, some could be more detailed
- **0.5-0.69**: Basic roles mentioned but lacking depth
- **0.3-0.49**: Roles vague or missing for multiple services
- **0.0-0.29**: No meaningful role explanations provided

### Quality (0.0-1.0)
- **0.9-1.0**: Well-organized, uses proper terminology, shows deep AWS knowledge
- **0.7-0.89**: Clear structure, appropriate terminology
- **0.5-0.69**: Adequate but could be better organized
- **0.3-0.49**: Disorganized or uses incorrect terminology
- **0.0-0.29**: Poor structure, significant terminology errors

## Response to Evaluate
{response}
""",

    ("diagram_interpretation", "data_flow_analysis"): """
## Task Type: Data Flow Analysis
The model was asked to trace data flow through an AWS architecture.

## Expected Flow Steps
{expected_flow}

## Scoring Guidance

### Accuracy (0.0-1.0)
- **0.9-1.0**: Flow correctly traces all steps in proper sequence
- **0.7-0.89**: Flow mostly correct, minor sequencing issues
- **0.5-0.69**: Major steps present but some missing or out of order
- **0.3-0.49**: Significant flow errors or missing steps
- **0.0-0.29**: Flow fundamentally incorrect

### Completeness (0.0-1.0)
- **0.9-1.0**: All data transformation and processing steps explained
- **0.7-0.89**: Most steps explained, some detail missing
- **0.5-0.69**: Basic flow described, lacks detail
- **0.3-0.49**: Many steps unexplained
- **0.0-0.29**: Minimal or no explanation of flow

### Quality (0.0-1.0)
- **0.9-1.0**: Uses flow indicators (first, then, next), shows understanding of async/sync patterns
- **0.7-0.89**: Clear sequential explanation
- **0.5-0.69**: Understandable but could be clearer
- **0.3-0.49**: Confusing or hard to follow
- **0.0-0.29**: Incomprehensible flow description

## Response to Evaluate
{response}
""",

    ("diagram_interpretation", "security_assessment"): """
## Task Type: Security Assessment
The model was asked to analyze security components and suggest improvements.

## Expected Security Components
{expected_security_components}

## Expected Improvements
{potential_improvements}

## Scoring Guidance

### Accuracy (0.0-1.0)
- **0.9-1.0**: Correctly identifies all security controls with proper descriptions
- **0.7-0.89**: Most security controls identified correctly
- **0.5-0.69**: Core controls identified, some missed
- **0.3-0.49**: Several controls missed or misidentified
- **0.0-0.29**: Fails to identify basic security controls

### Completeness (0.0-1.0)
- **0.9-1.0**: Identifies existing controls AND provides relevant improvement suggestions
- **0.7-0.89**: Good coverage of controls, some improvement suggestions
- **0.5-0.69**: Partial coverage, limited improvements suggested
- **0.3-0.49**: Missing many controls or improvements
- **0.0-0.29**: Minimal security analysis

### Quality (0.0-1.0)
- **0.9-1.0**: References AWS security best practices, Shared Responsibility Model, defense in depth
- **0.7-0.89**: Shows solid security understanding
- **0.5-0.69**: Basic security awareness
- **0.3-0.49**: Superficial security understanding
- **0.0-0.29**: Poor security reasoning

## Response to Evaluate
{response}
""",

    ("diagram_interpretation", "scalability_analysis"): """
## Task Type: Scalability Analysis
The model was asked to evaluate scaling mechanisms and potential bottlenecks.

## Expected Scaling Mechanisms
{expected_scaling_mechanisms}

## Potential Bottlenecks
{potential_bottlenecks}

## Scoring Guidance

### Accuracy (0.0-1.0)
- **0.9-1.0**: Correctly identifies all scaling mechanisms with proper AWS terminology
- **0.7-0.89**: Most mechanisms identified, minor gaps
- **0.5-0.69**: Core mechanisms found, some missed
- **0.3-0.49**: Limited mechanism identification
- **0.0-0.29**: Fails to identify basic scaling patterns

### Completeness (0.0-1.0)
- **0.9-1.0**: Identifies mechanisms AND bottlenecks with mitigation strategies
- **0.7-0.89**: Good coverage of mechanisms and bottlenecks
- **0.5-0.69**: Partial analysis
- **0.3-0.49**: Missing significant elements
- **0.0-0.29**: Incomplete analysis

### Quality (0.0-1.0)
- **0.9-1.0**: Demonstrates understanding of horizontal vs vertical scaling, discusses limits
- **0.7-0.89**: Shows scaling knowledge
- **0.5-0.69**: Basic scalability understanding
- **0.3-0.49**: Limited scaling insight
- **0.0-0.29**: Poor scalability reasoning

## Response to Evaluate
{response}
""",

    ("diagram_interpretation", "cost_optimization"): """
## Task Type: Cost Optimization Analysis
The model was asked to identify cost factors and optimization opportunities.

## Cost Optimization Opportunities
{cost_optimization_opportunities}

## Cost Factors
{cost_factors}

## Scoring Guidance

### Accuracy (0.0-1.0)
- **0.9-1.0**: Correctly identifies all cost drivers and optimization opportunities
- **0.7-0.89**: Most cost factors correctly identified
- **0.5-0.69**: Core costs identified, some missed
- **0.3-0.49**: Limited cost identification
- **0.0-0.29**: Misses major cost factors

### Completeness (0.0-1.0)
- **0.9-1.0**: Identifies costs AND provides actionable optimization strategies
- **0.7-0.89**: Good coverage with some optimization suggestions
- **0.5-0.69**: Partial coverage
- **0.3-0.49**: Missing many elements
- **0.0-0.29**: Incomplete analysis

### Quality (0.0-1.0)
- **0.9-1.0**: Mentions pricing models (Reserved, Spot), data transfer costs, right-sizing
- **0.7-0.89**: Shows AWS pricing understanding
- **0.5-0.69**: Basic cost awareness
- **0.3-0.49**: Limited cost optimization insight
- **0.0-0.29**: Poor cost reasoning

## Response to Evaluate
{response}
""",

    # === DIAGRAM CREATION SUBTYPES ===
    ("diagram_creation", "requirements_to_architecture"): """
## Task Type: Requirements to Architecture Design
The model was given requirements and asked to design an AWS architecture.

## Expected Components
{expected_components}

## Architectural Principles
{architectural_principles}

## Scoring Guidance

### Accuracy (0.0-1.0)
- **0.9-1.0**: Design includes all expected components with appropriate AWS services
- **0.7-0.89**: Most components present with suitable services
- **0.5-0.69**: Core components present, some gaps
- **0.3-0.49**: Missing several required components
- **0.0-0.29**: Design doesn't meet requirements

### Completeness (0.0-1.0)
- **0.9-1.0**: All requirements addressed with clear justification
- **0.7-0.89**: Most requirements covered
- **0.5-0.69**: Partial requirements coverage
- **0.3-0.49**: Many requirements missed
- **0.0-0.29**: Requirements largely unaddressed

### Quality (0.0-1.0)
- **0.9-1.0**: Follows Well-Architected Framework principles, explains trade-offs
- **0.7-0.89**: Good architectural reasoning
- **0.5-0.69**: Adequate design explanation
- **0.3-0.49**: Limited design justification
- **0.0-0.29**: Poor architectural reasoning

## Response to Evaluate
{response}
""",

    ("diagram_creation", "pattern_implementation"): """
## Task Type: Architectural Pattern Implementation
The model was asked to implement a specific architectural pattern.

## Pattern to Implement
{pattern}

## Constraints
{constraints}

## Expected Pattern Elements
{expected_pattern_elements}

## Pattern Benefits
{pattern_benefits}

## Scoring Guidance

### Accuracy (0.0-1.0)
- **0.9-1.0**: Pattern correctly implemented with all expected elements
- **0.7-0.89**: Pattern mostly correct, minor deviations
- **0.5-0.69**: Pattern recognizable but incomplete
- **0.3-0.49**: Pattern partially implemented
- **0.0-0.29**: Pattern fundamentally incorrect

### Completeness (0.0-1.0)
- **0.9-1.0**: All pattern elements present, constraints satisfied, benefits explained
- **0.7-0.89**: Most elements present
- **0.5-0.69**: Core elements present
- **0.3-0.49**: Missing key elements
- **0.0-0.29**: Incomplete implementation

### Quality (0.0-1.0)
- **0.9-1.0**: Shows deep pattern understanding, explains why pattern fits use case
- **0.7-0.89**: Good pattern application
- **0.5-0.69**: Adequate pattern usage
- **0.3-0.49**: Limited pattern understanding
- **0.0-0.29**: Poor pattern application

## Response to Evaluate
{response}
""",

    ("diagram_creation", "problem_solving"): """
## Task Type: Problem Solving / Migration Architecture
The model was asked to solve an architectural problem (often migration).

## Problem Statement
{problem}

## Constraints
{constraints}

## Expected Solution Elements
{expected_solution_elements}

## Migration Phases (if applicable)
{migration_phases}

## Scoring Guidance

### Accuracy (0.0-1.0)
- **0.9-1.0**: Solution addresses problem with all expected elements, constraints satisfied
- **0.7-0.89**: Solution mostly addresses problem
- **0.5-0.69**: Core problem addressed, some constraints missed
- **0.3-0.49**: Partial solution
- **0.0-0.29**: Solution doesn't address problem

### Completeness (0.0-1.0)
- **0.9-1.0**: All solution elements present with clear phases/steps
- **0.7-0.89**: Most elements present
- **0.5-0.69**: Core elements present
- **0.3-0.49**: Missing key elements
- **0.0-0.29**: Incomplete solution

### Quality (0.0-1.0)
- **0.9-1.0**: Shows migration best practices, risk mitigation, rollback strategy
- **0.7-0.89**: Good problem-solving approach
- **0.5-0.69**: Adequate solution
- **0.3-0.49**: Limited problem-solving
- **0.0-0.29**: Poor solution quality

## Response to Evaluate
{response}
""",
}


# Hidden criteria for anti-gaming (not exposed in public docs)
HIDDEN_CRITERIA: Dict[str, List[str]] = {
    "service_identification": [
        "Distinguishes between similar services (ALB vs NLB, Aurora vs RDS)",
        "Acknowledges service relationships (EC2 requires VPC)",
        "Uses official AWS naming conventions",
    ],
    "data_flow_analysis": [
        "Considers synchronous vs asynchronous patterns",
        "Mentions error handling in flow",
        "Discusses data transformation at each step",
    ],
    "security_assessment": [
        "References Shared Responsibility Model concepts",
        "Distinguishes data-at-rest vs data-in-transit encryption",
        "Considers IAM and resource-based policies",
    ],
    "scalability_analysis": [
        "Mentions service limits and quotas",
        "Discusses regional vs global scaling",
        "Considers data layer scaling separately from compute",
    ],
    "cost_optimization": [
        "Mentions specific pricing models (Reserved, Savings Plans, Spot)",
        "Considers data transfer costs between AZs/regions",
        "Discusses compute vs storage cost trade-offs",
    ],
    "requirements_to_architecture": [
        "Addresses non-functional requirements (latency, availability targets)",
        "Considers operational aspects (monitoring, logging)",
        "Discusses failure modes and recovery",
    ],
    "pattern_implementation": [
        "Explains why the pattern fits the constraints",
        "Discusses pattern trade-offs",
        "Considers pattern evolution/extensibility",
    ],
    "problem_solving": [
        "Addresses risk mitigation",
        "Includes rollback strategy",
        "Considers testing/validation approach",
    ],
}


def get_rubric_prompt(eval_type: str, subtype: str) -> str | None:
    """Get the rubric prompt for a given evaluation type and subtype."""
    return RUBRIC_PROMPTS.get((eval_type, subtype))


def get_hidden_criteria(subtype: str) -> List[str]:
    """Get hidden anti-gaming criteria for a subtype."""
    return HIDDEN_CRITERIA.get(subtype, [])


def format_rubric_prompt(
    eval_type: str,
    subtype: str,
    response: str,
    eval_data: Dict[str, Any],
) -> str | None:
    """Format a rubric prompt with response and evaluation data."""
    template = get_rubric_prompt(eval_type, subtype)
    if not template:
        return None

    # Build format kwargs from eval_data
    format_kwargs = {"response": response}

    # Add all list/string fields from eval_data
    for key, value in eval_data.items():
        if isinstance(value, list):
            if value and isinstance(value[0], dict):
                # Format list of dicts (like expected_services)
                formatted = "\n".join(
                    f"- {item.get('service', item)}: {item.get('role', '')}"
                    for item in value
                )
            else:
                # Format simple list
                formatted = "\n".join(f"- {item}" for item in value)
            format_kwargs[key] = formatted
        elif isinstance(value, str):
            format_kwargs[key] = value
        else:
            format_kwargs[key] = str(value) if value else "N/A"

    # Fill in any missing placeholders with N/A
    import re
    placeholders = re.findall(r'\{(\w+)\}', template)
    for ph in placeholders:
        if ph not in format_kwargs:
            format_kwargs[ph] = "N/A"

    return template.format(**format_kwargs)


def get_all_subtypes() -> List[tuple]:
    """Return all supported (type, subtype) pairs."""
    return list(RUBRIC_PROMPTS.keys())
