"""Tests for task registry configuration."""

import pytest

from task_registry import TASKS


class TestWeightNormalization:
    """Verify task weights are properly configured."""

    def test_weights_sum_to_one(self):
        """Weights must sum to exactly 1.0 for proper weighted averaging."""
        total = sum(cfg["weight"] for cfg in TASKS.values())
        assert abs(total - 1.0) < 0.0001, f"Weights sum to {total}, expected 1.0"

    def test_all_weights_positive(self):
        """All weights must be positive."""
        for name, cfg in TASKS.items():
            assert cfg["weight"] > 0, f"Task {name} has non-positive weight: {cfg['weight']}"

    def test_all_weights_at_most_one(self):
        """No single weight should exceed 1.0."""
        for name, cfg in TASKS.items():
            assert cfg["weight"] <= 1.0, f"Task {name} has weight > 1.0: {cfg['weight']}"


class TestTaskRegistryStructure:
    """Verify task registry has required fields."""

    REQUIRED_FIELDS = {"patterns", "metric", "weight"}

    def test_all_tasks_have_required_fields(self):
        """Every task must have patterns, metric, and weight."""
        for name, cfg in TASKS.items():
            missing = self.REQUIRED_FIELDS - set(cfg.keys())
            assert not missing, f"Task {name} missing required fields: {missing}"

    def test_patterns_are_non_empty_lists(self):
        """Patterns must be non-empty lists for log detection."""
        for name, cfg in TASKS.items():
            patterns = cfg.get("patterns", [])
            assert isinstance(patterns, list), f"Task {name} patterns is not a list"
            assert len(patterns) > 0, f"Task {name} has empty patterns list"

    def test_metric_is_string(self):
        """Metric must be a string identifier."""
        for name, cfg in TASKS.items():
            assert isinstance(cfg["metric"], str), f"Task {name} metric is not a string"
            assert len(cfg["metric"]) > 0, f"Task {name} has empty metric"

    def test_pass_values_when_present_is_list(self):
        """If pass_values is specified, it must be a list."""
        for name, cfg in TASKS.items():
            if "pass_values" in cfg:
                assert isinstance(cfg["pass_values"], list), (
                    f"Task {name} pass_values is not a list"
                )


class TestExpectedTasks:
    """Verify expected evaluation tracks exist."""

    EXPECTED_TASKS = ["practice_exam", "architecture_design", "cdk_synth"]

    def test_expected_tasks_exist(self):
        """All expected evaluation tracks must be registered."""
        for task_name in self.EXPECTED_TASKS:
            assert task_name in TASKS, f"Expected task {task_name} not in registry"

    def test_no_unexpected_tasks(self):
        """Registry should only contain expected tasks (update test if adding new tracks)."""
        unexpected = set(TASKS.keys()) - set(self.EXPECTED_TASKS)
        assert not unexpected, f"Unexpected tasks in registry: {unexpected}"
