#!/usr/bin/env python3
"""
Measure LLM judge agreement against calibration ground truth.

This script runs the LLM judge on calibration responses and measures:
- Agreement rate (% within tolerance of ground truth)
- Mean absolute error per dimension
- Self-consistency (variance across multiple runs)
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from statistics import mean, stdev

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evals.architecture_design.tasks import (
    _call_judge,
    _parse_judge_response,
    DEFAULT_JUDGE_MODEL,
)
from evals.architecture_design.judge_prompts import format_rubric_prompt
from inspect_ai.model import get_model, GenerateConfig


# Configuration
TOLERANCE = 0.15  # Agreement threshold
NUM_RUNS = 3  # Number of judge runs for consistency check
CALIBRATION_FILE = Path(__file__).parent.parent / "evals/architecture_design/calibration/responses.jsonl"


def load_calibration_data():
    """Load calibration responses with ground truth."""
    samples = []
    with open(CALIBRATION_FILE, "r") as f:
        for line in f:
            if line.strip():
                samples.append(json.loads(line))
    return samples


async def run_judge_on_sample(judge_model, sample):
    """Run the judge on a single calibration sample."""
    rubric_prompt = format_rubric_prompt(
        sample["type"],
        sample["subtype"],
        sample["model_response"],
        sample,
    )

    if not rubric_prompt:
        return None

    result = await _call_judge(judge_model, rubric_prompt)
    return result


async def measure_agreement():
    """Run agreement measurement against calibration set."""
    print(f"Loading calibration data from {CALIBRATION_FILE}")
    samples = load_calibration_data()
    print(f"Loaded {len(samples)} calibration samples")

    # Initialize judge model
    judge_model_name = os.environ.get("ARCHITECTURE_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)
    print(f"Using judge model: {judge_model_name}")
    judge_model = get_model(judge_model_name)

    # Track results
    all_results = []
    dimension_errors = {"accuracy": [], "completeness": [], "quality": []}

    for sample in samples:
        sample_id = sample["id"]
        ground_truth = sample["ground_truth"]
        quality_tier = sample.get("quality_tier", "unknown")

        print(f"\nProcessing {sample_id} ({quality_tier} tier)...")

        # Run judge multiple times for consistency
        sample_scores = []
        for run in range(NUM_RUNS):
            result = await run_judge_on_sample(judge_model, sample)
            if result:
                sample_scores.append(result)

        if not sample_scores:
            print(f"  ⚠ Failed to get judge scores for {sample_id}")
            continue

        # Calculate average scores across runs
        avg_scores = {
            "accuracy": mean([s.get("accuracy", 0.5) for s in sample_scores]),
            "completeness": mean([s.get("completeness", 0.5) for s in sample_scores]),
            "quality": mean([s.get("quality", 0.5) for s in sample_scores]),
        }

        # Calculate self-consistency (std dev across runs)
        consistency = {
            "accuracy": stdev([s.get("accuracy", 0.5) for s in sample_scores]) if len(sample_scores) > 1 else 0,
            "completeness": stdev([s.get("completeness", 0.5) for s in sample_scores]) if len(sample_scores) > 1 else 0,
            "quality": stdev([s.get("quality", 0.5) for s in sample_scores]) if len(sample_scores) > 1 else 0,
        }

        # Calculate errors from ground truth
        errors = {
            "accuracy": abs(avg_scores["accuracy"] - ground_truth["accuracy"]),
            "completeness": abs(avg_scores["completeness"] - ground_truth["completeness"]),
            "quality": abs(avg_scores["quality"] - ground_truth["quality"]),
        }

        # Check agreement (within tolerance)
        within_tolerance = all(e <= TOLERANCE for e in errors.values())

        # Print sample result
        print(f"  Ground Truth: A={ground_truth['accuracy']:.2f} C={ground_truth['completeness']:.2f} Q={ground_truth['quality']:.2f}")
        print(f"  Judge Avg:    A={avg_scores['accuracy']:.2f} C={avg_scores['completeness']:.2f} Q={avg_scores['quality']:.2f}")
        print(f"  Errors:       A={errors['accuracy']:.2f} C={errors['completeness']:.2f} Q={errors['quality']:.2f}")
        print(f"  Consistency:  A={consistency['accuracy']:.2f} C={consistency['completeness']:.2f} Q={consistency['quality']:.2f}")
        print(f"  Agreement:    {'✓' if within_tolerance else '✗'} (tolerance={TOLERANCE})")

        # Track for summary
        all_results.append({
            "id": sample_id,
            "tier": quality_tier,
            "ground_truth": ground_truth,
            "judge_scores": avg_scores,
            "errors": errors,
            "consistency": consistency,
            "within_tolerance": within_tolerance,
        })

        for dim in dimension_errors:
            dimension_errors[dim].append(errors[dim])

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    agreement_count = sum(1 for r in all_results if r["within_tolerance"])
    agreement_rate = agreement_count / len(all_results) * 100 if all_results else 0

    print(f"\nAgreement Rate: {agreement_rate:.1f}% ({agreement_count}/{len(all_results)})")
    print(f"Target: ≥80%")
    print(f"Status: {'✓ PASS' if agreement_rate >= 80 else '✗ FAIL'}")

    print(f"\nMean Absolute Error by Dimension:")
    for dim, errors in dimension_errors.items():
        mae = mean(errors) if errors else 0
        print(f"  {dim}: {mae:.3f}")

    print(f"\nSelf-Consistency (std dev across {NUM_RUNS} runs):")
    avg_consistency = {
        dim: mean([r["consistency"][dim] for r in all_results])
        for dim in ["accuracy", "completeness", "quality"]
    }
    for dim, std in avg_consistency.items():
        print(f"  {dim}: {std:.3f}")

    print(f"\nBy Quality Tier:")
    for tier in ["excellent", "good", "poor"]:
        tier_results = [r for r in all_results if r["tier"] == tier]
        if tier_results:
            tier_agreement = sum(1 for r in tier_results if r["within_tolerance"]) / len(tier_results) * 100
            print(f"  {tier}: {tier_agreement:.1f}% agreement ({len(tier_results)} samples)")

    return agreement_rate >= 80


if __name__ == "__main__":
    success = asyncio.run(measure_agreement())
    sys.exit(0 if success else 1)
