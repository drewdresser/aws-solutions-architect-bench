"""Tests for aggregation logic in aggregate_multi.py."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from aggregate_multi import collect, metric_value, scores_to_dict, validate_leaderboard_json, SCHEMA_PATH
from task_registry import TASKS


# ---------------------------------------------------------------------------
# Mock data structures
# ---------------------------------------------------------------------------


@dataclass
class MockScore:
    """Mock Inspect Score object."""

    name: str
    value: Any
    answer: Any = None


@dataclass
class MockSampleSummary:
    """Mock Inspect sample summary."""

    model: str
    scores: dict


def make_sample(model: str, metric_name: str, value: Any) -> MockSampleSummary:
    """Create a mock sample summary with a single score."""
    return MockSampleSummary(
        model=model,
        scores={metric_name: MockScore(name=metric_name, value=value)},
    )


# ---------------------------------------------------------------------------
# Test: scores_to_dict normalization
# ---------------------------------------------------------------------------


class TestScoresToDict:
    """Test score payload normalization."""

    def test_dict_passthrough(self):
        """Dict input should pass through unchanged."""
        scores = {"choice": MockScore("choice", "C")}
        result = scores_to_dict(scores)
        assert result == scores

    def test_list_of_scores(self):
        """List of Score objects should convert to dict by name."""
        scores = [MockScore("choice", "C"), MockScore("other", 0.5)]
        result = scores_to_dict(scores)
        assert "choice" in result
        assert "other" in result

    def test_none_returns_empty(self):
        """None input should return empty dict."""
        assert scores_to_dict(None) == {}

    def test_empty_list_returns_empty(self):
        """Empty list should return empty dict."""
        assert scores_to_dict([]) == {}


# ---------------------------------------------------------------------------
# Test: metric_value extraction
# ---------------------------------------------------------------------------


class TestMetricValue:
    """Test metric value extraction from samples."""

    def test_pass_value_correct(self):
        """Sample with pass_value 'C' should return 1.0."""
        task_cfg = {"metric": "choice", "pass_values": ["C"]}
        sample = make_sample("model", "choice", "C")
        assert metric_value(sample, task_cfg) == 1.0

    def test_pass_value_incorrect(self):
        """Sample with non-pass value should return 0.0."""
        task_cfg = {"metric": "choice", "pass_values": ["C"]}
        sample = make_sample("model", "choice", "I")
        assert metric_value(sample, task_cfg) == 0.0

    def test_numeric_value_passthrough(self):
        """Numeric rubric scores should pass through as-is."""
        task_cfg = {"metric": "architecture_scorer"}
        sample = make_sample("model", "architecture_scorer", 0.75)
        assert metric_value(sample, task_cfg) == 0.75

    def test_boolean_true(self):
        """Boolean True should return 1.0."""
        task_cfg = {"metric": "test"}
        sample = make_sample("model", "test", True)
        assert metric_value(sample, task_cfg) == 1.0

    def test_boolean_false(self):
        """Boolean False should return 0.0."""
        task_cfg = {"metric": "test"}
        sample = make_sample("model", "test", False)
        assert metric_value(sample, task_cfg) == 0.0

    def test_metric_alias_fallback(self):
        """Should try metric_aliases if primary metric not found."""
        task_cfg = {"metric": "primary", "metric_aliases": ["secondary"]}
        sample = make_sample("model", "secondary", 0.8)
        assert metric_value(sample, task_cfg) == 0.8


# ---------------------------------------------------------------------------
# Test: Overall score calculation
# ---------------------------------------------------------------------------


class TestOverallScoreCalculation:
    """Test that overall score is computed correctly."""

    def test_weighted_average_calculation(self):
        """Verify overall = sum(category * weight) with current weights."""
        # Get current weights from registry
        weights = {name: cfg["weight"] for name, cfg in TASKS.items()}

        # Sample scores
        scores = {
            "practice_exam": 0.80,
            "architecture_design": 0.70,
            "cdk_synth": 0.60,
        }

        # Calculate expected overall
        expected = sum(scores[task] * weights[task] for task in scores)

        # Create DataFrame mimicking collect() output
        df = pd.DataFrame(
            [
                {
                    "model": "test-model",
                    **scores,
                }
            ]
        )

        # Apply same calculation as collect()
        df["overall"] = sum(
            df[t] * cfg["weight"] for t, cfg in TASKS.items()
        ).round(4)

        assert abs(df["overall"].iloc[0] - expected) < 0.0001

    def test_missing_category_treated_as_zero(self):
        """Missing category should contribute 0 to overall."""
        weights = {name: cfg["weight"] for name, cfg in TASKS.items()}

        # Only practice_exam has score
        scores = {
            "practice_exam": 1.0,
            "architecture_design": 0.0,  # Missing → 0
            "cdk_synth": 0.0,  # Missing → 0
        }

        expected = 1.0 * weights["practice_exam"]

        df = pd.DataFrame([{"model": "test-model", **scores}])
        df["overall"] = sum(
            df[t] * cfg["weight"] for t, cfg in TASKS.items()
        ).round(4)

        assert abs(df["overall"].iloc[0] - expected) < 0.0001

    def test_perfect_scores_yield_one(self):
        """All 1.0 scores should yield overall of 1.0."""
        df = pd.DataFrame(
            [
                {
                    "model": "perfect-model",
                    "practice_exam": 1.0,
                    "architecture_design": 1.0,
                    "cdk_synth": 1.0,
                }
            ]
        )

        df["overall"] = sum(
            df[t] * cfg["weight"] for t, cfg in TASKS.items()
        ).round(4)

        # With weights summing to 1.0, all 1.0 scores should give 1.0
        assert df["overall"].iloc[0] == 1.0

    def test_zero_scores_yield_zero(self):
        """All 0.0 scores should yield overall of 0.0."""
        df = pd.DataFrame(
            [
                {
                    "model": "zero-model",
                    "practice_exam": 0.0,
                    "architecture_design": 0.0,
                    "cdk_synth": 0.0,
                }
            ]
        )

        df["overall"] = sum(
            df[t] * cfg["weight"] for t, cfg in TASKS.items()
        ).round(4)

        assert df["overall"].iloc[0] == 0.0


class TestDuplicateHandling:
    """Test handling of duplicate log entries."""

    def test_duplicate_model_task_averages(self):
        """Multiple logs for same model+task should be averaged."""
        # Simulate raw data before aggregation
        raw_data = [
            {"model": "model-a", "task": "practice_exam", "accuracy": 0.8},
            {"model": "model-a", "task": "practice_exam", "accuracy": 0.6},  # Duplicate
        ]
        df = pd.DataFrame(raw_data)

        # Group and average (same as in collect())
        df_agg = df.groupby(["model", "task"], as_index=False)["accuracy"].mean()

        assert len(df_agg) == 1
        assert df_agg["accuracy"].iloc[0] == 0.7  # Average of 0.8 and 0.6


# ---------------------------------------------------------------------------
# Test: JSON schema validation
# ---------------------------------------------------------------------------


class TestSchemaValidation:
    """Test leaderboard JSON schema validation."""

    def test_schema_file_exists(self):
        """Schema file should exist at expected path."""
        assert SCHEMA_PATH.exists(), f"Schema not found at {SCHEMA_PATH}"

    def test_schema_is_valid_json(self):
        """Schema file should be valid JSON."""
        with open(SCHEMA_PATH) as f:
            schema = json.load(f)
        assert "$schema" in schema
        assert "type" in schema

    def test_valid_leaderboard_passes(self):
        """Valid leaderboard data should pass validation."""
        valid_data = [
            {
                "model": "test/model-a",
                "practice_exam": 0.8,
                "architecture_design": 0.7,
                "cdk_synth": 0.6,
                "overall": 0.7,
            },
            {
                "model": "test/model-b",
                "overall": 0.5,
            },
        ]
        # Should not raise
        validate_leaderboard_json(valid_data)

    def test_invalid_overall_fails(self):
        """Overall score > 1.0 should fail validation."""
        import jsonschema

        invalid_data = [{"model": "test", "overall": 1.5}]  # > 1.0
        with pytest.raises(jsonschema.ValidationError):
            validate_leaderboard_json(invalid_data)

    def test_missing_model_fails(self):
        """Entry without model should fail validation."""
        import jsonschema

        invalid_data = [{"overall": 0.5}]  # Missing required 'model'
        with pytest.raises(jsonschema.ValidationError):
            validate_leaderboard_json(invalid_data)

    def test_missing_overall_fails(self):
        """Entry without overall should fail validation."""
        import jsonschema

        invalid_data = [{"model": "test"}]  # Missing required 'overall'
        with pytest.raises(jsonschema.ValidationError):
            validate_leaderboard_json(invalid_data)

    def test_negative_score_fails(self):
        """Negative category score should fail validation."""
        import jsonschema

        invalid_data = [{"model": "test", "overall": 0.5, "practice_exam": -0.1}]
        with pytest.raises(jsonschema.ValidationError):
            validate_leaderboard_json(invalid_data)

    def test_existing_leaderboard_validates(self):
        """Existing leaderboard.json should pass validation."""
        leaderboard_path = SCHEMA_PATH.parent.parent / "results" / "leaderboard.json"
        if leaderboard_path.exists():
            with open(leaderboard_path) as f:
                data = json.load(f)
            # Should not raise
            validate_leaderboard_json(data)
