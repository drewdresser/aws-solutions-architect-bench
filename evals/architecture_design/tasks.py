"""
AWS Solutions Architect Architecture Design Evaluation Tasks

This module defines evaluation tasks for testing AI model capabilities on AWS architecture
design, including diagram interpretation and creation tasks.
"""

import base64
import json
import mimetypes
from pathlib import Path
from typing import Dict

from inspect_ai import Task, task
from inspect_ai.dataset import Dataset, MemoryDataset, Sample
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, ContentImage, ContentText
from inspect_ai.scorer import Score, Scorer, Target, mean, metric, scorer
from inspect_ai.solver import Generate, Solver, TaskState, generate, solver


# System prompts for different evaluation types
ARCHITECTURE_SYSTEM_PROMPT = """You are an expert AWS Solutions Architect with deep knowledge of AWS services, architectural patterns, and best practices. You have extensive experience in:

- Designing scalable, secure, and cost-effective cloud architectures
- Analyzing architecture diagrams and identifying components
- Understanding data flows and service interactions
- Implementing AWS Well-Architected Framework principles
- Optimizing architectures for performance, security, and cost

When analyzing architecture diagrams:
1. Carefully examine all components and their relationships
2. Identify AWS services by their standard icons and labels
3. Consider the architectural patterns being implemented
4. Think about data flow, security, scalability, and cost implications
5. Provide detailed explanations for your analysis

When creating architecture designs:
1. Start by understanding the requirements thoroughly
2. Consider all architectural pillars: operational excellence, security, reliability, performance efficiency, and cost optimization
3. Select appropriate AWS services for each component
4. Design for scalability, availability, and fault tolerance
5. Explain your design decisions and trade-offs

Be precise, thorough, and practical in your responses."""

DIAGRAM_INTERPRETATION_PROMPT = """You are analyzing an AWS architecture diagram. Please provide a comprehensive analysis based on the specific question asked. 

When identifying services:
- Use official AWS service names (e.g., "Amazon EC2", "Amazon RDS", "Elastic Load Balancer")
- Explain the role and purpose of each service in the architecture
- Consider how services interact with each other

When analyzing data flow:
- Trace the complete path from source to destination
- Explain what happens at each step
- Identify any transformation or processing that occurs

When assessing security:
- Identify security controls and mechanisms
- Point out potential vulnerabilities or areas for improvement
- Consider network security, data protection, and access controls

When evaluating scalability:
- Identify auto-scaling mechanisms
- Point out potential bottlenecks
- Consider both horizontal and vertical scaling options

When analyzing costs:
- Consider all cost factors (compute, storage, data transfer, etc.)
- Identify optimization opportunities
- Think about usage patterns and pricing models"""

DIAGRAM_CREATION_PROMPT = """You are designing an AWS architecture based on the given requirements. Please create a detailed architectural design that addresses all specified requirements and constraints.

Your response should include:
1. **Architecture Overview**: High-level description of the solution
2. **Component Selection**: List of AWS services and their roles
3. **Architecture Diagram Description**: Detailed description of how components connect
4. **Design Rationale**: Explanation of key design decisions
5. **Scalability Considerations**: How the architecture handles growth
6. **Security Measures**: Security controls and best practices implemented
7. **Cost Optimization**: Strategies to minimize costs while meeting requirements
8. **Operational Considerations**: Monitoring, logging, and maintenance aspects

Format your response clearly with these sections. Be specific about AWS services, configurations, and architectural patterns used."""


def load_architecture_dataset(file_path: str) -> Dataset:
    """Load architecture dataset with full metadata preserved."""
    import json

    samples = []
    file_path_obj = Path(__file__).parent / file_path

    with open(file_path_obj, "r") as f:
        for line in f:
            data = json.loads(line.strip())

            # Create sample with input/target fields and preserve metadata
            sample = Sample(
                input=data.get("input", ""),
                target=data.get("target", ""),
                metadata=data,  # Store the full original data
            )
            samples.append(sample)

    return MemoryDataset(samples)


# Custom metrics for architecture evaluation
@metric
def architecture_accuracy_metric():
    """Average accuracy component extracted from score metadata."""

    def metric_fn(scores):
        if not scores:
            return 0.0
        values = [
            score.metadata.get("accuracy", 0.0)
            for score in scores
            if getattr(score, "metadata", None)
        ]
        return sum(values) / len(values) if values else 0.0

    return metric_fn


@metric
def architecture_completeness_metric():
    """Average completeness component extracted from score metadata."""

    def metric_fn(scores):
        if not scores:
            return 0.0
        values = [
            score.metadata.get("completeness", 0.0)
            for score in scores
            if getattr(score, "metadata", None)
        ]
        return sum(values) / len(values) if values else 0.0

    return metric_fn


@metric
def architecture_quality_metric():
    """Average quality component extracted from score metadata."""

    def metric_fn(scores):
        if not scores:
            return 0.0
        values = [
            score.metadata.get("quality", 0.0)
            for score in scores
            if getattr(score, "metadata", None)
        ]
        return sum(values) / len(values) if values else 0.0

    return metric_fn


def _get_sample_metadata(state: TaskState) -> Dict:
    """Return metadata attached to the current sample for prompting and scoring."""

    sample = getattr(state, "sample", None)
    if sample and getattr(sample, "metadata", None):
        return sample.metadata

    if getattr(state, "metadata", None):
        return state.metadata

    return {}


def _image_content_for_path(diagram_path: str) -> ContentImage | None:
    """Return base64-encoded image content for the provided diagram path."""

    if not diagram_path:
        return None

    image_file = (Path(__file__).parent / diagram_path).resolve()
    if not image_file.exists() or not image_file.is_file():
        return None

    mime_type, _ = mimetypes.guess_type(image_file.name)
    if mime_type is None:
        mime_type = "image/png"

    encoded = base64.b64encode(image_file.read_bytes()).decode("ascii")
    data_uri = f"data:{mime_type};base64,{encoded}"
    return ContentImage(image=data_uri)


@scorer(
    metrics=[
        mean(),
        architecture_accuracy_metric(),
        architecture_completeness_metric(),
        architecture_quality_metric(),
    ]
)
def architecture_scorer() -> Scorer:
    """Custom scorer for architecture evaluation tasks."""

    async def score(state: TaskState, target: Target) -> Score:
        """Score architecture evaluation responses."""

        # Get the sample data for scoring - should now be in state.metadata from our custom dataset
        eval_data = _get_sample_metadata(state)

        response = state.output.completion if state.output else ""

        # Initialize scores
        accuracy_score = 0.0
        completeness_score = 0.0
        quality_score = 0.0

        eval_type = eval_data.get("type", "")
        subtype = eval_data.get("subtype", "")

        if eval_type == "diagram_interpretation":
            accuracy_score, completeness_score, quality_score = score_interpretation(
                response, eval_data, subtype
            )
        elif eval_type == "diagram_creation":
            accuracy_score, completeness_score, quality_score = score_creation(
                response, eval_data, subtype
            )

        # Calculate overall score
        overall_score = (accuracy_score + completeness_score + quality_score) / 3

        return Score(
            value=overall_score,
            metadata={
                "accuracy": accuracy_score,
                "completeness": completeness_score,
                "quality": quality_score,
                "type": eval_type,
                "subtype": subtype,
            },
        )

    return score


def score_interpretation(
    response: str, eval_data: Dict, subtype: str
) -> tuple[float, float, float]:
    """Score diagram interpretation tasks."""

    response_lower = response.lower()

    if subtype == "service_identification":
        return score_service_identification(response, response_lower, eval_data)
    elif subtype == "data_flow_analysis":
        return score_data_flow_analysis(response, response_lower, eval_data)
    elif subtype == "security_assessment":
        return score_security_assessment(response, response_lower, eval_data)
    elif subtype == "scalability_analysis":
        return score_scalability_analysis(response, response_lower, eval_data)
    elif subtype == "cost_optimization":
        return score_cost_optimization(response, response_lower, eval_data)

    return 0.5, 0.5, 0.5  # Default moderate score


def score_service_identification(
    response: str, response_lower: str, eval_data: Dict
) -> tuple[float, float, float]:
    """Score service identification tasks."""

    expected_services = eval_data.get("expected_services", [])

    # Check for service mentions
    services_found = 0
    roles_explained = 0

    for service_info in expected_services:
        service_name = service_info["service"].lower()
        service_role = service_info["role"].lower()

        # Check if service is mentioned
        if service_name in response_lower or any(
            word in response_lower for word in service_name.split()
        ):
            services_found += 1

            # Check if role is explained (basic keyword matching)
            role_keywords = service_role.split()
            if any(keyword in response_lower for keyword in role_keywords):
                roles_explained += 1

    accuracy = services_found / len(expected_services) if expected_services else 0
    completeness = roles_explained / len(expected_services) if expected_services else 0

    # Quality based on response length and structure
    quality = min(1.0, len(response.split()) / 100)  # Reward detailed responses

    return accuracy, completeness, quality


def score_data_flow_analysis(
    response: str, response_lower: str, eval_data: Dict
) -> tuple[float, float, float]:
    """Score data flow analysis tasks."""

    expected_flow = eval_data.get("expected_flow", [])

    # Check for flow step mentions
    steps_found = 0
    for step in expected_flow:
        step_keywords = step.lower().split()
        if any(
            keyword in response_lower for keyword in step_keywords[:3]
        ):  # Check first 3 words
            steps_found += 1

    accuracy = steps_found / len(expected_flow) if expected_flow else 0

    # Check for flow indicators (sequential words)
    flow_indicators = ["first", "then", "next", "after", "finally", "step", "->", "→"]
    flow_structure = sum(
        1 for indicator in flow_indicators if indicator in response_lower
    )
    completeness = min(1.0, flow_structure / 5)  # Normalize to 0-1

    # Quality based on explanation depth
    quality = min(1.0, len(response.split()) / 150)

    return accuracy, completeness, quality


def score_security_assessment(
    response: str, response_lower: str, eval_data: Dict
) -> tuple[float, float, float]:
    """Score security assessment tasks."""

    security_components = eval_data.get("expected_security_components", [])
    improvements = eval_data.get("potential_improvements", [])

    # Check for security component identification
    components_found = 0
    for component in security_components:
        if component.lower() in response_lower:
            components_found += 1

    # Check for improvement suggestions
    improvements_found = 0
    for improvement in improvements:
        improvement_keywords = improvement.lower().split()
        if any(keyword in response_lower for keyword in improvement_keywords[:2]):
            improvements_found += 1

    accuracy = components_found / len(security_components) if security_components else 0
    completeness = improvements_found / len(improvements) if improvements else 0

    # Quality based on security depth
    security_keywords = [
        "security",
        "vulnerability",
        "threat",
        "risk",
        "protection",
        "encryption",
    ]
    security_depth = sum(
        1 for keyword in security_keywords if keyword in response_lower
    )
    quality = min(1.0, security_depth / 5)

    return accuracy, completeness, quality


def score_scalability_analysis(
    response: str, response_lower: str, eval_data: Dict
) -> tuple[float, float, float]:
    """Score scalability analysis tasks."""

    scaling_mechanisms = eval_data.get("expected_scaling_mechanisms", [])
    bottlenecks = eval_data.get("potential_bottlenecks", [])

    # Check for scaling mechanism identification
    mechanisms_found = 0
    for mechanism in scaling_mechanisms:
        if mechanism.lower() in response_lower:
            mechanisms_found += 1

    # Check for bottleneck identification
    bottlenecks_found = 0
    for bottleneck in bottlenecks:
        bottleneck_keywords = bottleneck.lower().split()
        if any(keyword in response_lower for keyword in bottleneck_keywords[:2]):
            bottlenecks_found += 1

    accuracy = mechanisms_found / len(scaling_mechanisms) if scaling_mechanisms else 0
    completeness = bottlenecks_found / len(bottlenecks) if bottlenecks else 0

    # Quality based on scalability understanding
    scalability_keywords = [
        "scale",
        "scaling",
        "bottleneck",
        "capacity",
        "performance",
        "throughput",
    ]
    scalability_depth = sum(
        1 for keyword in scalability_keywords if keyword in response_lower
    )
    quality = min(1.0, scalability_depth / 4)

    return accuracy, completeness, quality


def score_cost_optimization(
    response: str, response_lower: str, eval_data: Dict
) -> tuple[float, float, float]:
    """Score cost optimization tasks."""

    opportunities = eval_data.get("cost_optimization_opportunities", [])
    cost_factors = eval_data.get("cost_factors", [])

    # Check for optimization opportunities
    opportunities_found = 0
    for opportunity in opportunities:
        opportunity_keywords = opportunity.lower().split()
        if any(keyword in response_lower for keyword in opportunity_keywords[:2]):
            opportunities_found += 1

    # Check for cost factor understanding
    factors_found = 0
    for factor in cost_factors:
        if factor.lower() in response_lower:
            factors_found += 1

    accuracy = opportunities_found / len(opportunities) if opportunities else 0
    completeness = factors_found / len(cost_factors) if cost_factors else 0

    # Quality based on cost understanding
    cost_keywords = [
        "cost",
        "pricing",
        "optimization",
        "savings",
        "budget",
        "reserved",
        "spot",
    ]
    cost_depth = sum(1 for keyword in cost_keywords if keyword in response_lower)
    quality = min(1.0, cost_depth / 5)

    return accuracy, completeness, quality


def score_creation(
    response: str, eval_data: Dict, subtype: str
) -> tuple[float, float, float]:
    """Score diagram creation tasks."""

    response_lower = response.lower()

    if subtype == "requirements_to_architecture":
        return score_requirements_architecture(response, response_lower, eval_data)
    elif subtype == "pattern_implementation":
        return score_pattern_implementation(response, response_lower, eval_data)
    elif subtype == "problem_solving":
        return score_problem_solving(response, response_lower, eval_data)

    return 0.5, 0.5, 0.5  # Default moderate score


def score_requirements_architecture(
    response: str, response_lower: str, eval_data: Dict
) -> tuple[float, float, float]:
    """Score requirements to architecture tasks."""

    expected_components = eval_data.get("expected_components", [])
    principles = eval_data.get("architectural_principles", [])

    # Check for component mentions
    components_found = 0
    for component in expected_components:
        if component.lower() in response_lower:
            components_found += 1

    # Check for architectural principles
    principles_found = 0
    for principle in principles:
        principle_keywords = principle.lower().split()
        if any(keyword in response_lower for keyword in principle_keywords):
            principles_found += 1

    accuracy = components_found / len(expected_components) if expected_components else 0
    completeness = principles_found / len(principles) if principles else 0

    # Quality based on architectural depth
    arch_keywords = [
        "architecture",
        "design",
        "scalable",
        "available",
        "secure",
        "resilient",
    ]
    arch_depth = sum(1 for keyword in arch_keywords if keyword in response_lower)
    quality = min(1.0, arch_depth / 4)

    return accuracy, completeness, quality


def score_pattern_implementation(
    response: str, response_lower: str, eval_data: Dict
) -> tuple[float, float, float]:
    """Score pattern implementation tasks."""

    pattern_elements = eval_data.get("expected_pattern_elements", [])
    benefits = eval_data.get("pattern_benefits", [])

    # Check for pattern elements
    elements_found = 0
    for element in pattern_elements:
        if element.lower() in response_lower:
            elements_found += 1

    # Check for pattern benefits understanding
    benefits_found = 0
    for benefit in benefits:
        benefit_keywords = benefit.lower().split()
        if any(keyword in response_lower for keyword in benefit_keywords):
            benefits_found += 1

    accuracy = elements_found / len(pattern_elements) if pattern_elements else 0
    completeness = benefits_found / len(benefits) if benefits else 0

    # Quality based on pattern understanding
    pattern_keywords = ["pattern", "microservices", "event", "serverless", "decoupled"]
    pattern_depth = sum(1 for keyword in pattern_keywords if keyword in response_lower)
    quality = min(1.0, pattern_depth / 3)

    return accuracy, completeness, quality


def score_problem_solving(
    response: str, response_lower: str, eval_data: Dict
) -> tuple[float, float, float]:
    """Score problem solving tasks."""

    solution_elements = eval_data.get("expected_solution_elements", [])
    phases = eval_data.get("migration_phases", [])

    # Check for solution elements
    elements_found = 0
    for element in solution_elements:
        element_keywords = element.lower().split()
        if any(keyword in response_lower for keyword in element_keywords[:2]):
            elements_found += 1

    # Check for migration phases (if applicable)
    phases_found = 0
    if phases:
        for phase in phases:
            phase_keywords = phase.lower().split()
            if any(keyword in response_lower for keyword in phase_keywords):
                phases_found += 1

    accuracy = elements_found / len(solution_elements) if solution_elements else 0
    completeness = (
        phases_found / len(phases) if phases else 1.0
    )  # Full score if no phases expected

    # Quality based on solution depth
    solution_keywords = [
        "solution",
        "strategy",
        "migration",
        "approach",
        "implementation",
    ]
    solution_depth = sum(
        1 for keyword in solution_keywords if keyword in response_lower
    )
    quality = min(1.0, solution_depth / 3)

    return accuracy, completeness, quality


@solver
def architecture_solver() -> Solver:
    """Solver for architecture evaluation tasks."""

    async def solve(state: TaskState, _generate: Generate) -> TaskState:
        """Solve architecture evaluation tasks."""

        # Get the evaluation data from metadata (preserved from our custom dataset)
        eval_data = _get_sample_metadata(state)

        eval_type = eval_data.get("type", "")
        diagram_path = eval_data.get("diagram_path", "")
        question = state.input  # The input field extracted by our custom dataset

        # Prepare the prompt based on evaluation type
        content_parts: list[ContentText | ContentImage]

        if eval_type == "diagram_interpretation":
            system_prompt = (
                ARCHITECTURE_SYSTEM_PROMPT + "\n\n" + DIAGRAM_INTERPRETATION_PROMPT
            )

            image_content = _image_content_for_path(diagram_path)
            if image_content is not None:
                content_parts = [
                    ContentText(
                        text="Please analyze the following AWS architecture diagram and answer the question."
                    ),
                    image_content,
                    ContentText(text=f"Question: {question}"),
                ]
            else:
                content_parts = [
                    ContentText(
                        text=(
                            "Diagram unavailable; analyze using the provided description "
                            f"(original path: {diagram_path or 'n/a'})."
                        )
                    ),
                    ContentText(text=f"Question: {question}"),
                ]

        elif eval_type == "diagram_creation":
            system_prompt = (
                ARCHITECTURE_SYSTEM_PROMPT + "\n\n" + DIAGRAM_CREATION_PROMPT
            )

            requirements = eval_data.get("requirements", "")
            pattern = eval_data.get("pattern", "")
            problem = eval_data.get("problem", "")
            constraints = eval_data.get("constraints", [])

            if requirements:
                prompt_text = (
                    "Requirements:\n"
                    f"{requirements}\n\nPlease design an AWS architecture that meets these requirements."
                )
            elif pattern:
                constraint_text = (
                    "\n".join([f"- {c}" for c in constraints]) if constraints else ""
                )
                prompt_text = (
                    "Pattern to implement: "
                    f"{pattern}\n\nConstraints:\n{constraint_text}\n\n"
                    "Please design an AWS architecture implementing this pattern with the given constraints."
                )
            elif problem:
                constraint_text = (
                    "\n".join([f"- {c}" for c in constraints]) if constraints else ""
                )
                prompt_text = (
                    "Problem: "
                    f"{problem}\n\nConstraints:\n{constraint_text}\n\n"
                    "Please design a solution architecture addressing this problem within the given constraints."
                )
            else:
                prompt_text = question

            content_parts = [ContentText(text=prompt_text)]
        else:
            system_prompt = ARCHITECTURE_SYSTEM_PROMPT
            content_parts = [ContentText(text=question)]

        # Update the state with the prepared messages
        state.messages = [
            ChatMessageSystem(content=system_prompt),
            ChatMessageUser(content=content_parts if len(content_parts) > 1 else content_parts[0].text),
        ]

        # Store evaluation data in metadata for scoring
        state.metadata = eval_data

        return state

    return solve


@task
def architecture_interpretation() -> Task:
    """Task for architecture diagram interpretation evaluations."""

    return Task(
        dataset=load_architecture_dataset("architecture_interpretation.jsonl"),
        plan=[architecture_solver(), generate()],
        scorer=architecture_scorer(),
    )


@task
def architecture_design() -> Task:
    """Combined task for all architecture design evaluations."""

    return Task(
        dataset=load_architecture_dataset("architecture_interpretation.jsonl"),
        plan=[architecture_solver(), generate()],
        scorer=architecture_scorer(),
    )


# Export tasks
__all__ = ["architecture_interpretation", "architecture_design"]
