"""
Validators for structured diagram output formats.

Provides validation for Mermaid, PlantUML, and JSON architecture descriptions.
Used by the LLM judge scorer to add structural validation to architecture scoring.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jsonschema


@dataclass
class ValidationResult:
    """Result of validating a structured diagram output."""

    is_valid: bool
    format_detected: str | None  # "mermaid", "plantuml", "json", or None
    error_message: str | None = None
    extracted_content: str | None = None


# =============================================================================
# Code Block Extraction
# =============================================================================


def extract_code_block(text: str, language: str | None = None) -> str | None:
    """
    Extract code from fenced code blocks.

    Args:
        text: The full response text
        language: Optional language tag to match (e.g., "mermaid", "json")

    Returns:
        Extracted code content, or None if no matching block found
    """
    if language:
        # Match specific language tag
        pattern = rf"```{language}\s*\n(.*?)```"
    else:
        # Match any code block
        pattern = r"```(?:\w+)?\s*\n(.*?)```"

    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
    if matches:
        # Return the largest code block (most likely to be the main content)
        return max(matches, key=len).strip()
    return None


def detect_format(text: str) -> str | None:
    """
    Detect the diagram format in the text.

    Returns: "mermaid", "plantuml", "json", or None
    """
    text_lower = text.lower()

    # Check for explicit code blocks
    if "```mermaid" in text_lower:
        return "mermaid"
    if "```plantuml" in text_lower:
        return "plantuml"
    if "```json" in text_lower and '"architecture"' in text:
        return "json"

    # Check for format indicators without code blocks
    if "@startuml" in text_lower:
        return "plantuml"
    if re.search(r"\b(flowchart|graph|sequenceDiagram|classDiagram)\s+(TD|TB|LR|RL|BT)?\b", text):
        return "mermaid"
    if '{"architecture"' in text or '"architecture":' in text:
        return "json"

    return None


# =============================================================================
# Mermaid Validation
# =============================================================================

# Valid Mermaid diagram types
MERMAID_DIAGRAM_TYPES = [
    "flowchart",
    "graph",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "erDiagram",
    "journey",
    "gantt",
    "pie",
    "quadrantChart",
    "requirementDiagram",
    "gitGraph",
    "mindmap",
    "timeline",
    "C4Context",
    "C4Container",
    "C4Component",
    "C4Dynamic",
    "C4Deployment",
]

# Mermaid direction keywords
MERMAID_DIRECTIONS = ["TD", "TB", "BT", "LR", "RL"]


def validate_mermaid(text: str) -> ValidationResult:
    """
    Validate Mermaid diagram syntax.

    Checks for:
    - Valid diagram type declaration
    - Basic node definition syntax
    - Edge syntax validity
    - Balanced brackets

    Returns:
        ValidationResult with is_valid, error_message, and extracted_content
    """
    # Extract Mermaid code block
    code = extract_code_block(text, "mermaid")
    if not code:
        # Try to find Mermaid content without code block
        code = text
        # Check if it looks like Mermaid at all
        if not re.search(r"\b(flowchart|graph)\b", code, re.IGNORECASE):
            return ValidationResult(
                is_valid=False,
                format_detected="mermaid",
                error_message="No Mermaid diagram found. Use ```mermaid code block.",
                extracted_content=None,
            )

    code = code.strip()
    lines = code.split("\n")

    # Check for diagram type declaration
    first_line = lines[0].strip() if lines else ""
    diagram_type_found = False

    for dtype in MERMAID_DIAGRAM_TYPES:
        if first_line.lower().startswith(dtype.lower()):
            diagram_type_found = True
            break

    if not diagram_type_found:
        return ValidationResult(
            is_valid=False,
            format_detected="mermaid",
            error_message=f"Invalid diagram type. Must start with one of: {', '.join(MERMAID_DIAGRAM_TYPES[:5])}...",
            extracted_content=code,
        )

    # Check for balanced brackets
    brackets = {"[": "]", "(": ")", "{": "}", "[[": "]]", "((": "))"}
    bracket_stack = []

    for line in lines[1:]:  # Skip diagram declaration
        # Skip comments
        if line.strip().startswith("%%"):
            continue

        for char in line:
            if char in "[({":
                bracket_stack.append(char)
            elif char in "])}":
                if not bracket_stack:
                    return ValidationResult(
                        is_valid=False,
                        format_detected="mermaid",
                        error_message=f"Unbalanced bracket: unexpected '{char}'",
                        extracted_content=code,
                    )
                bracket_stack.pop()

    if bracket_stack:
        return ValidationResult(
            is_valid=False,
            format_detected="mermaid",
            error_message=f"Unbalanced brackets: unclosed '{bracket_stack[-1]}'",
            extracted_content=code,
        )

    # Check for at least one edge (connection between nodes)
    edge_patterns = [
        r"--\>",  # Arrow
        r"-\.-\>",  # Dotted arrow
        r"==\>",  # Thick arrow
        r"---",  # Line
        r"-\.-",  # Dotted line
        r"===",  # Thick line
        r"->>\+?",  # Sequence diagram arrow
        r"-->>",  # Sequence diagram async
        r"-x",  # Sequence diagram cross
    ]
    has_edges = any(re.search(pattern, code) for pattern in edge_patterns)

    if not has_edges:
        return ValidationResult(
            is_valid=False,
            format_detected="mermaid",
            error_message="No edges/connections found. Diagram should show relationships between components.",
            extracted_content=code,
        )

    # Check for at least two nodes
    # Node patterns: id[label], id((label)), id{label}, id>label], etc.
    # Also extract node IDs from edges like A --> B or sequence diagrams like Client->>Server
    node_pattern = r"(\w+)[\[\(\{<]"
    edge_node_pattern = r"(\w+)\s*(?:--\>|---|-\.-\>|==\>|->>|-->>)"
    edge_target_pattern = r"(?:--\>|---|-\.-\>|==\>|->>|-->>)\s*(\w+)"

    nodes = set()
    for line in lines[1:]:
        line_stripped = line.strip()
        # Find nodes with explicit definitions
        for match in re.finditer(node_pattern, line_stripped):
            nodes.add(match.group(1))
        # Find nodes from edge sources
        for match in re.finditer(edge_node_pattern, line_stripped):
            nodes.add(match.group(1))
        # Find nodes from edge targets
        for match in re.finditer(edge_target_pattern, line_stripped):
            nodes.add(match.group(1))

    if len(nodes) < 2:
        return ValidationResult(
            is_valid=False,
            format_detected="mermaid",
            error_message="Diagram should have at least 2 defined nodes.",
            extracted_content=code,
        )

    return ValidationResult(
        is_valid=True,
        format_detected="mermaid",
        error_message=None,
        extracted_content=code,
    )


# =============================================================================
# PlantUML Validation
# =============================================================================


def validate_plantuml(text: str) -> ValidationResult:
    """
    Validate PlantUML diagram syntax.

    Checks for:
    - @startuml and @enduml delimiters
    - Basic component/node definitions
    - Relationship syntax

    Returns:
        ValidationResult with is_valid, error_message, and extracted_content
    """
    # Extract PlantUML code block
    code = extract_code_block(text, "plantuml")
    if not code:
        # Try to find PlantUML content without code block
        if "@startuml" in text.lower():
            # Extract between @startuml and @enduml
            match = re.search(r"@startuml(.*?)@enduml", text, re.DOTALL | re.IGNORECASE)
            if match:
                code = "@startuml" + match.group(1) + "@enduml"
            else:
                code = text
        else:
            return ValidationResult(
                is_valid=False,
                format_detected="plantuml",
                error_message="No PlantUML diagram found. Use ```plantuml code block with @startuml/@enduml.",
                extracted_content=None,
            )

    code = code.strip()
    code_lower = code.lower()

    # Check for @startuml
    if "@startuml" not in code_lower:
        return ValidationResult(
            is_valid=False,
            format_detected="plantuml",
            error_message="Missing @startuml declaration.",
            extracted_content=code,
        )

    # Check for @enduml
    if "@enduml" not in code_lower:
        return ValidationResult(
            is_valid=False,
            format_detected="plantuml",
            error_message="Missing @enduml declaration.",
            extracted_content=code,
        )

    # Check that @startuml comes before @enduml
    start_pos = code_lower.find("@startuml")
    end_pos = code_lower.find("@enduml")
    if start_pos > end_pos:
        return ValidationResult(
            is_valid=False,
            format_detected="plantuml",
            error_message="@startuml must come before @enduml.",
            extracted_content=code,
        )

    # Extract content between delimiters
    content = code[start_pos + len("@startuml") : end_pos].strip()
    lines = content.split("\n")

    # Check for components or actors
    component_patterns = [
        r"^\s*\[.+\]",  # [Component]
        r"^\s*\(.+\)",  # (Actor)
        r"^\s*actor\s+",  # actor Name
        r"^\s*component\s+",  # component Name
        r"^\s*database\s+",  # database Name
        r"^\s*node\s+",  # node Name
        r"^\s*cloud\s+",  # cloud Name
        r"^\s*package\s+",  # package Name
        r"^\s*rectangle\s+",  # rectangle Name
        r"^\s*interface\s+",  # interface Name
        r"^\s*class\s+",  # class Name
    ]

    has_components = False
    for line in lines:
        if any(re.match(pattern, line, re.IGNORECASE) for pattern in component_patterns):
            has_components = True
            break

    if not has_components:
        return ValidationResult(
            is_valid=False,
            format_detected="plantuml",
            error_message="No components found. Define components using [Name], (Name), or 'component Name' syntax.",
            extracted_content=code,
        )

    # Check for relationships
    relationship_patterns = [
        r"--\>",  # Arrow
        r"\.\.\>",  # Dotted arrow
        r"--",  # Line
        r"\.\.",  # Dotted line
        r"<--",  # Reverse arrow
        r"<\.\.",  # Reverse dotted arrow
    ]

    has_relationships = any(re.search(pattern, content) for pattern in relationship_patterns)

    if not has_relationships:
        return ValidationResult(
            is_valid=False,
            format_detected="plantuml",
            error_message="No relationships found. Connect components using --> or -- syntax.",
            extracted_content=code,
        )

    return ValidationResult(
        is_valid=True,
        format_detected="plantuml",
        error_message=None,
        extracted_content=code,
    )


# =============================================================================
# JSON Architecture Validation
# =============================================================================

# JSON Schema for architecture descriptions
ARCHITECTURE_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["architecture"],
    "properties": {
        "architecture": {
            "type": "object",
            "required": ["components"],
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "components": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["id", "type"],
                        "properties": {
                            "id": {"type": "string"},
                            "type": {"type": "string"},
                            "name": {"type": "string"},
                            "aws_service": {"type": "string"},
                            "description": {"type": "string"},
                            "properties": {"type": "object"},
                        },
                    },
                },
                "relationships": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["from", "to"],
                        "properties": {
                            "from": {"type": "string"},
                            "to": {"type": "string"},
                            "type": {"type": "string"},
                            "description": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
}


def validate_architecture_json(text: str) -> ValidationResult:
    """
    Validate JSON architecture description against schema.

    Checks for:
    - Valid JSON syntax
    - Conforms to architecture schema
    - Has required components array
    - Components have id and type

    Returns:
        ValidationResult with is_valid, error_message, and extracted_content
    """
    # Extract JSON code block
    code = extract_code_block(text, "json")
    if not code:
        # Try to find JSON object in text
        json_match = re.search(r'\{[^{}]*"architecture"[^{}]*\{.*\}[^{}]*\}', text, re.DOTALL)
        if json_match:
            code = json_match.group()
        else:
            return ValidationResult(
                is_valid=False,
                format_detected="json",
                error_message="No JSON architecture found. Use ```json code block with {\"architecture\": ...}.",
                extracted_content=None,
            )

    code = code.strip()

    # Try to parse JSON
    try:
        data = json.loads(code)
    except json.JSONDecodeError as e:
        return ValidationResult(
            is_valid=False,
            format_detected="json",
            error_message=f"Invalid JSON syntax: {e.msg} at line {e.lineno}",
            extracted_content=code,
        )

    # Validate against schema
    try:
        jsonschema.validate(data, ARCHITECTURE_SCHEMA)
    except jsonschema.ValidationError as e:
        # Simplify the error message
        path = " -> ".join(str(p) for p in e.absolute_path) if e.absolute_path else "root"
        return ValidationResult(
            is_valid=False,
            format_detected="json",
            error_message=f"Schema validation failed at '{path}': {e.message}",
            extracted_content=code,
        )

    # Additional semantic checks
    components = data.get("architecture", {}).get("components", [])
    if len(components) < 2:
        return ValidationResult(
            is_valid=False,
            format_detected="json",
            error_message="Architecture should have at least 2 components.",
            extracted_content=code,
        )

    # Check for relationships (optional but recommended)
    relationships = data.get("architecture", {}).get("relationships", [])
    if not relationships:
        # Warning but not invalid
        pass

    return ValidationResult(
        is_valid=True,
        format_detected="json",
        error_message=None,
        extracted_content=code,
    )


# =============================================================================
# Unified Validation Interface
# =============================================================================


def validate_structured_output(
    text: str, required_format: str | None = None
) -> ValidationResult:
    """
    Validate structured diagram output.

    Args:
        text: The response text to validate
        required_format: Required format ("mermaid", "plantuml", "json") or None to auto-detect

    Returns:
        ValidationResult with is_valid, format_detected, error_message, and extracted_content
    """
    if not text or not text.strip():
        return ValidationResult(
            is_valid=False,
            format_detected=None,
            error_message="Empty response",
            extracted_content=None,
        )

    # Determine format to validate
    if required_format:
        format_to_validate = required_format.lower()
    else:
        format_to_validate = detect_format(text)

    if not format_to_validate:
        return ValidationResult(
            is_valid=False,
            format_detected=None,
            error_message="No structured format detected. Use Mermaid, PlantUML, or JSON.",
            extracted_content=None,
        )

    # Validate based on format
    if format_to_validate == "mermaid":
        return validate_mermaid(text)
    elif format_to_validate == "plantuml":
        return validate_plantuml(text)
    elif format_to_validate == "json":
        return validate_architecture_json(text)
    else:
        return ValidationResult(
            is_valid=False,
            format_detected=None,
            error_message=f"Unknown format: {format_to_validate}. Use 'mermaid', 'plantuml', or 'json'.",
            extracted_content=None,
        )


def check_required_components(
    validation_result: ValidationResult, expected_components: list[str]
) -> tuple[bool, list[str]]:
    """
    Check if required components are present in validated output.

    Args:
        validation_result: Result from validate_structured_output
        expected_components: List of component IDs/names that should be present

    Returns:
        Tuple of (all_present: bool, missing_components: list[str])
    """
    if not validation_result.is_valid or not validation_result.extracted_content:
        return False, expected_components

    content_lower = validation_result.extracted_content.lower()
    missing = []

    for component in expected_components:
        # Check for component name (case-insensitive)
        if component.lower() not in content_lower:
            missing.append(component)

    return len(missing) == 0, missing
