"""Tests for diagram validators."""

import pytest
from evals.architecture_design.diagram_validators import (
    validate_mermaid,
    validate_plantuml,
    validate_architecture_json,
    validate_structured_output,
    extract_code_block,
    detect_format,
    check_required_components,
    ValidationResult,
)


class TestCodeBlockExtraction:
    """Test code block extraction utilities."""

    def test_extract_mermaid_block(self):
        """Extract Mermaid code from fenced block."""
        text = """Here is the diagram:

```mermaid
flowchart TD
    A[Start] --> B[End]
```

That's the architecture."""
        code = extract_code_block(text, "mermaid")
        assert code is not None
        assert "flowchart TD" in code
        assert "A[Start]" in code

    def test_extract_json_block(self):
        """Extract JSON code from fenced block."""
        text = '```json\n{"architecture": {"components": []}}\n```'
        code = extract_code_block(text, "json")
        assert code is not None
        assert '"architecture"' in code

    def test_extract_any_block(self):
        """Extract code without specifying language."""
        text = "```python\nprint('hello')\n```"
        code = extract_code_block(text, None)
        assert code is not None
        assert "print" in code

    def test_extract_largest_block(self):
        """When multiple blocks, return the largest."""
        text = """```mermaid
A
```

```mermaid
flowchart TD
    A[Start] --> B[Process] --> C[End]
```"""
        code = extract_code_block(text, "mermaid")
        assert "flowchart TD" in code

    def test_no_block_returns_none(self):
        """Return None when no code block found."""
        text = "Just plain text without code blocks."
        code = extract_code_block(text, "mermaid")
        assert code is None


class TestFormatDetection:
    """Test automatic format detection."""

    def test_detect_mermaid_code_block(self):
        """Detect Mermaid from code block."""
        text = "```mermaid\nflowchart TD\n```"
        assert detect_format(text) == "mermaid"

    def test_detect_mermaid_keywords(self):
        """Detect Mermaid from keywords without code block."""
        text = "flowchart TD\n    A --> B"
        assert detect_format(text) == "mermaid"

    def test_detect_plantuml_code_block(self):
        """Detect PlantUML from code block."""
        text = "```plantuml\n@startuml\n@enduml\n```"
        assert detect_format(text) == "plantuml"

    def test_detect_plantuml_startuml(self):
        """Detect PlantUML from @startuml without code block."""
        text = "@startuml\ncomponent A\n@enduml"
        assert detect_format(text) == "plantuml"

    def test_detect_json_architecture(self):
        """Detect JSON architecture format."""
        text = '```json\n{"architecture": {}}\n```'
        assert detect_format(text) == "json"

    def test_detect_unknown(self):
        """Return None for unknown format."""
        text = "Just plain text about architecture."
        assert detect_format(text) is None


class TestMermaidValidation:
    """Test Mermaid diagram validation."""

    def test_valid_flowchart(self):
        """Valid Mermaid flowchart passes validation."""
        text = """```mermaid
flowchart TD
    ALB[Application Load Balancer]
    EC2[EC2 Instances]
    RDS[(Database)]

    ALB --> EC2
    EC2 --> RDS
```"""
        result = validate_mermaid(text)
        assert result.is_valid
        assert result.format_detected == "mermaid"
        assert result.error_message is None

    def test_valid_graph_lr(self):
        """Valid graph with LR direction."""
        text = """```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
```"""
        result = validate_mermaid(text)
        assert result.is_valid

    def test_missing_diagram_type(self):
        """Fail when missing diagram type declaration."""
        text = """```mermaid
    A[Start] --> B[End]
```"""
        result = validate_mermaid(text)
        assert not result.is_valid
        assert "diagram type" in result.error_message.lower()

    def test_unbalanced_brackets(self):
        """Fail on unbalanced brackets."""
        text = """```mermaid
flowchart TD
    A[Start --> B[End]
```"""
        result = validate_mermaid(text)
        assert not result.is_valid
        assert "bracket" in result.error_message.lower()

    def test_no_edges(self):
        """Fail when no edges/connections defined."""
        text = """```mermaid
flowchart TD
    A[Start]
    B[End]
```"""
        result = validate_mermaid(text)
        assert not result.is_valid
        assert "edge" in result.error_message.lower() or "connection" in result.error_message.lower()

    def test_too_few_nodes(self):
        """Fail when fewer than 2 nodes."""
        text = """```mermaid
flowchart TD
    A[Only One Node]
    A --> A
```"""
        result = validate_mermaid(text)
        assert not result.is_valid
        assert "node" in result.error_message.lower()

    def test_without_code_block(self):
        """Validate Mermaid without code block wrapper."""
        text = """flowchart TD
    A[Start] --> B[End]
"""
        result = validate_mermaid(text)
        assert result.is_valid

    def test_sequence_diagram(self):
        """Valid sequence diagram with ->> syntax."""
        text = """```mermaid
sequenceDiagram
    Client->>Server: Request
    Server->>Client: Response
```"""
        result = validate_mermaid(text)
        assert result.is_valid
        assert result.format_detected == "mermaid"


class TestPlantUMLValidation:
    """Test PlantUML diagram validation."""

    def test_valid_component_diagram(self):
        """Valid PlantUML component diagram."""
        text = """```plantuml
@startuml
[Web Server] --> [Application Server]
[Application Server] --> [Database]
@enduml
```"""
        result = validate_plantuml(text)
        assert result.is_valid
        assert result.format_detected == "plantuml"

    def test_valid_with_actors(self):
        """Valid diagram with actors."""
        text = """```plantuml
@startuml
actor User
User --> [Web App]
[Web App] --> [API]
@enduml
```"""
        result = validate_plantuml(text)
        assert result.is_valid

    def test_missing_startuml(self):
        """Fail when missing @startuml."""
        text = """```plantuml
[Component A] --> [Component B]
@enduml
```"""
        result = validate_plantuml(text)
        assert not result.is_valid
        assert "@startuml" in result.error_message

    def test_missing_enduml(self):
        """Fail when missing @enduml."""
        text = """```plantuml
@startuml
[Component A] --> [Component B]
```"""
        result = validate_plantuml(text)
        assert not result.is_valid
        assert "@enduml" in result.error_message

    def test_no_components(self):
        """Fail when no components defined."""
        text = """```plantuml
@startuml
' Just a comment
@enduml
```"""
        result = validate_plantuml(text)
        assert not result.is_valid
        assert "component" in result.error_message.lower()

    def test_no_relationships(self):
        """Fail when no relationships defined."""
        text = """```plantuml
@startuml
[Component A]
[Component B]
@enduml
```"""
        result = validate_plantuml(text)
        assert not result.is_valid
        assert "relationship" in result.error_message.lower()

    def test_without_code_block(self):
        """Validate PlantUML without code block wrapper."""
        text = """@startuml
[A] --> [B]
@enduml"""
        result = validate_plantuml(text)
        assert result.is_valid


class TestJSONValidation:
    """Test JSON architecture validation."""

    def test_valid_architecture(self):
        """Valid JSON architecture passes validation."""
        text = '''```json
{
  "architecture": {
    "name": "Web App",
    "components": [
      {"id": "alb", "type": "load_balancer", "aws_service": "ALB"},
      {"id": "ec2", "type": "compute", "aws_service": "EC2"},
      {"id": "rds", "type": "database", "aws_service": "RDS"}
    ],
    "relationships": [
      {"from": "alb", "to": "ec2", "type": "routes_to"},
      {"from": "ec2", "to": "rds", "type": "queries"}
    ]
  }
}
```'''
        result = validate_architecture_json(text)
        assert result.is_valid
        assert result.format_detected == "json"

    def test_missing_architecture_key(self):
        """Fail when missing 'architecture' key."""
        text = '''```json
{
  "components": []
}
```'''
        result = validate_architecture_json(text)
        assert not result.is_valid
        assert "architecture" in result.error_message.lower()

    def test_missing_components(self):
        """Fail when missing 'components' array."""
        text = '''```json
{
  "architecture": {
    "name": "Test"
  }
}
```'''
        result = validate_architecture_json(text)
        assert not result.is_valid

    def test_invalid_json_syntax(self):
        """Fail on invalid JSON syntax."""
        text = '''```json
{
  "architecture": {
    components: []  // Missing quotes
  }
}
```'''
        result = validate_architecture_json(text)
        assert not result.is_valid
        assert "syntax" in result.error_message.lower()

    def test_component_missing_id(self):
        """Fail when component missing required 'id' field."""
        text = '''```json
{
  "architecture": {
    "components": [
      {"type": "compute"}
    ]
  }
}
```'''
        result = validate_architecture_json(text)
        assert not result.is_valid

    def test_too_few_components(self):
        """Fail when fewer than 2 components."""
        text = '''```json
{
  "architecture": {
    "components": [
      {"id": "single", "type": "compute"}
    ]
  }
}
```'''
        result = validate_architecture_json(text)
        assert not result.is_valid
        assert "2 component" in result.error_message.lower()


class TestUnifiedValidation:
    """Test unified validation interface."""

    def test_auto_detect_mermaid(self):
        """Auto-detect and validate Mermaid."""
        text = """```mermaid
flowchart TD
    A[Start] --> B[End]
```"""
        result = validate_structured_output(text)
        assert result.is_valid
        assert result.format_detected == "mermaid"

    def test_auto_detect_plantuml(self):
        """Auto-detect and validate PlantUML."""
        text = """@startuml
[A] --> [B]
@enduml"""
        result = validate_structured_output(text)
        assert result.is_valid
        assert result.format_detected == "plantuml"

    def test_required_format_mismatch(self):
        """Fail when required format doesn't match content."""
        text = """```mermaid
flowchart TD
    A --> B
```"""
        result = validate_structured_output(text, required_format="plantuml")
        assert not result.is_valid

    def test_empty_response(self):
        """Fail on empty response."""
        result = validate_structured_output("")
        assert not result.is_valid
        assert "empty" in result.error_message.lower()

    def test_no_format_detected(self):
        """Fail when no format detected."""
        result = validate_structured_output("Just plain text about architecture.")
        assert not result.is_valid
        assert "no structured format" in result.error_message.lower()


class TestComponentChecking:
    """Test required component checking."""

    def test_all_components_present(self):
        """All required components found."""
        result = ValidationResult(
            is_valid=True,
            format_detected="mermaid",
            extracted_content="ALB --> EC2 --> RDS",
        )
        all_present, missing = check_required_components(result, ["ALB", "EC2", "RDS"])
        assert all_present
        assert missing == []

    def test_some_components_missing(self):
        """Report missing components."""
        result = ValidationResult(
            is_valid=True,
            format_detected="mermaid",
            extracted_content="ALB --> EC2",
        )
        all_present, missing = check_required_components(result, ["ALB", "EC2", "RDS", "CloudFront"])
        assert not all_present
        assert "RDS" in missing
        assert "CloudFront" in missing

    def test_case_insensitive(self):
        """Component check is case-insensitive."""
        result = ValidationResult(
            is_valid=True,
            format_detected="mermaid",
            extracted_content="alb --> ec2",
        )
        all_present, missing = check_required_components(result, ["ALB", "EC2"])
        assert all_present

    def test_invalid_result_returns_all_missing(self):
        """Invalid validation result returns all components as missing."""
        result = ValidationResult(
            is_valid=False,
            format_detected=None,
            error_message="Some error",
        )
        all_present, missing = check_required_components(result, ["A", "B", "C"])
        assert not all_present
        assert missing == ["A", "B", "C"]
