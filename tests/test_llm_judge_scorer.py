"""Tests for the LLM-as-judge architecture scorer."""

import pytest
from evals.architecture_design.tasks import (
    _parse_judge_response,
    _check_anti_gaming,
    _apply_deterministic_checks,
)
from evals.architecture_design.judge_prompts import (
    get_rubric_prompt,
    format_rubric_prompt,
    get_hidden_criteria,
    get_all_subtypes,
)


class TestJudgeResponseParsing:
    """Test JSON parsing from judge responses."""

    def test_parse_valid_json(self):
        """Parse a well-formed JSON response."""
        response = '{"accuracy": 0.85, "completeness": 0.7, "quality": 0.9, "reasoning": "Good response"}'
        result = _parse_judge_response(response)
        assert result["accuracy"] == 0.85
        assert result["completeness"] == 0.7
        assert result["quality"] == 0.9
        assert result["reasoning"] == "Good response"

    def test_parse_json_with_preamble(self):
        """Parse JSON when judge adds text before it."""
        response = 'Here is my evaluation:\n{"accuracy": 0.6, "completeness": 0.8, "quality": 0.7, "reasoning": "test"}'
        result = _parse_judge_response(response)
        assert result["accuracy"] == 0.6
        assert result["completeness"] == 0.8

    def test_parse_malformed_json_extracts_scores(self):
        """Extract scores from malformed JSON-like text."""
        response = '"accuracy": 0.5, "completeness": 0.6, "quality": 0.7 blah blah'
        result = _parse_judge_response(response)
        assert result["accuracy"] == 0.5
        assert result["completeness"] == 0.6
        assert result["quality"] == 0.7

    def test_parse_completely_invalid_returns_defaults(self):
        """Return default scores for completely unparseable responses."""
        response = "I cannot evaluate this response."
        result = _parse_judge_response(response)
        assert result["accuracy"] == 0.5
        assert result["completeness"] == 0.5
        assert result["quality"] == 0.5


class TestAntiGaming:
    """Test anti-gaming mechanisms."""

    def test_short_response_penalty(self):
        """Very short responses should be penalized."""
        short_response = "EC2, RDS, ELB"  # ~3 words
        factor = _check_anti_gaming(short_response, "service_identification")
        assert factor < 1.0, "Short responses should have penalty < 1.0"

    def test_normal_response_no_penalty(self):
        """Normal length responses should not be penalized."""
        normal_response = " ".join(["word"] * 200)
        factor = _check_anti_gaming(normal_response, "service_identification")
        assert factor >= 0.9, "Normal responses should have factor >= 0.9"

    def test_hidden_criteria_bonus(self):
        """Responses meeting hidden criteria should get bonus."""
        # For service_identification, hidden criteria include distinguishing similar services
        # Response needs to be long enough to avoid short-response penalty
        response = """
        The architecture shows Amazon EC2 instances for compute workloads.
        Note that an Application Load Balancer (ALB) is used instead of a Network Load Balancer (NLB)
        because this is HTTP/HTTPS traffic requiring layer 7 routing capabilities.
        EC2 instances are deployed within a VPC for network isolation and security.
        The VPC contains both public and private subnets for proper network segmentation.
        Amazon RDS provides the database tier with Multi-AZ deployment for high availability.
        Auto Scaling Groups automatically adjust EC2 capacity based on demand.
        """ + " ".join(["additional context"] * 10)  # Ensure minimum word count
        factor = _check_anti_gaming(response, "service_identification")
        # Should get some bonus for mentioning ALB vs NLB distinction and VPC relationship
        assert factor > 0.95, f"Response meeting hidden criteria should get bonus, got {factor}"

    def test_repetitive_content_penalty(self):
        """Long repetitive responses should be penalized."""
        # Create a repetitive response
        sentence = "This is a repeated sentence about AWS services. "
        response = sentence * 100  # Very repetitive
        factor = _check_anti_gaming(response, "service_identification")
        assert factor <= 1.0, "Repetitive content should not exceed 1.0"


class TestRubricPrompts:
    """Test rubric prompt functionality."""

    def test_all_subtypes_have_rubrics(self):
        """Every subtype should have a corresponding rubric."""
        all_subtypes = get_all_subtypes()
        assert len(all_subtypes) >= 8, "Should have rubrics for at least 8 subtypes"

        for eval_type, subtype in all_subtypes:
            rubric = get_rubric_prompt(eval_type, subtype)
            assert rubric is not None, f"Missing rubric for {eval_type}/{subtype}"
            assert len(rubric) > 100, f"Rubric too short for {eval_type}/{subtype}"

    def test_rubric_format_service_identification(self):
        """Service identification rubric should format correctly."""
        eval_data = {
            "expected_services": [
                {"service": "Amazon EC2", "role": "Compute"},
                {"service": "Amazon RDS", "role": "Database"},
            ]
        }
        response = "The architecture uses EC2 for compute and RDS for data storage."

        formatted = format_rubric_prompt(
            "diagram_interpretation", "service_identification", response, eval_data
        )

        assert formatted is not None
        assert "Amazon EC2" in formatted
        assert "Amazon RDS" in formatted
        assert response in formatted
        assert "Scoring Guidance" in formatted

    def test_rubric_format_handles_missing_fields(self):
        """Formatting should handle missing fields gracefully."""
        eval_data = {}  # Empty eval data
        response = "Some response"

        formatted = format_rubric_prompt(
            "diagram_interpretation", "service_identification", response, eval_data
        )

        assert formatted is not None
        assert response in formatted
        # Should have N/A or empty for missing fields

    def test_unknown_subtype_returns_none(self):
        """Unknown subtypes should return None."""
        rubric = get_rubric_prompt("unknown_type", "unknown_subtype")
        assert rubric is None


class TestHiddenCriteria:
    """Test hidden criteria functionality."""

    def test_service_identification_has_hidden_criteria(self):
        """Service identification should have hidden criteria."""
        criteria = get_hidden_criteria("service_identification")
        assert len(criteria) > 0
        # Check for expected criteria about distinguishing similar services
        criteria_text = " ".join(criteria).lower()
        assert "alb" in criteria_text or "nlb" in criteria_text or "distinguish" in criteria_text

    def test_security_assessment_has_hidden_criteria(self):
        """Security assessment should have hidden criteria."""
        criteria = get_hidden_criteria("security_assessment")
        assert len(criteria) > 0
        criteria_text = " ".join(criteria).lower()
        assert "responsibility" in criteria_text or "iam" in criteria_text

    def test_unknown_subtype_returns_empty(self):
        """Unknown subtypes should return empty list."""
        criteria = get_hidden_criteria("unknown_subtype")
        assert criteria == []


class TestDeterministicChecks:
    """Test deterministic scoring fallback."""

    def test_service_identification_deterministic(self):
        """Deterministic check should score service identification."""
        eval_data = {
            "type": "diagram_interpretation",
            "subtype": "service_identification",
            "expected_services": [
                {"service": "Amazon EC2", "role": "compute servers"},
                {"service": "Amazon RDS", "role": "database storage"},
            ],
        }
        response = "The architecture uses Amazon EC2 for compute servers and Amazon RDS for database."

        accuracy, completeness, quality = _apply_deterministic_checks(
            response, eval_data, "service_identification"
        )

        assert accuracy > 0.5, "Should find services"
        assert completeness > 0.5, "Should find roles"
        assert quality > 0, "Should have some quality score"

    def test_data_flow_deterministic(self):
        """Deterministic check should score data flow."""
        eval_data = {
            "type": "diagram_interpretation",
            "subtype": "data_flow_analysis",
            "expected_flow": [
                "User sends request to Load Balancer",
                "Load Balancer forwards to EC2",
            ],
        }
        response = "First, the user sends a request. Then the load balancer forwards it to EC2 instances."

        accuracy, completeness, quality = _apply_deterministic_checks(
            response, eval_data, "data_flow_analysis"
        )

        assert accuracy > 0, "Should match flow steps"
        assert completeness > 0, "Should have flow indicators"

    def test_unknown_type_returns_moderate_scores(self):
        """Unknown types should return moderate default scores."""
        eval_data = {"type": "unknown_type"}
        response = "Some response"

        accuracy, completeness, quality = _apply_deterministic_checks(
            response, eval_data, "unknown_subtype"
        )

        assert accuracy == 0.5
        assert completeness == 0.5
        assert quality == 0.5
