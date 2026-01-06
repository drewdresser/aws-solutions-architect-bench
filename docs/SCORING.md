# SA Bench Scoring Methodology

This document describes how SA Bench computes scores for the leaderboard.

## Categories

SA Bench evaluates models across three categories, each measuring a different aspect of Solutions Architect capability.

### Practice Exam (MCQ)

- **What it measures**: AWS certification-style knowledge—service selection, best practices, and architectural decision-making in a multiple-choice format
- **Dataset**: `evals/practice_exam/aws_sa.jsonl`
- **Scoring**: Binary (1.0 if correct, 0.0 if incorrect)
- **Metric**: `choice` scorer from Inspect AI
- **Weight**: 34%

### Architecture Design

- **What it measures**: Architectural reasoning, diagram understanding, data flow analysis, security assessment, and scalability analysis
- **Dataset**: `evals/architecture_design/architecture_interpretation.jsonl`
- **Scoring**: Rubric-based score in [0, 1] combining accuracy, completeness, and quality dimensions
- **Metric**: Custom `architecture_scorer`
- **Weight**: 33%

### CDK Synthesis

- **What it measures**: Infrastructure-as-code generation—ability to produce valid AWS CDK Python code that synthesizes without errors
- **Dataset**: `evals/cdk_synth/cdk_synth.jsonl`
- **Scoring**: Binary (1.0 if `cdk synth` succeeds, 0.0 if it fails)
- **Metric**: `cdk_verify` scorer
- **Weight**: 33%

## Overall Score Formula

The overall score is a weighted average of category scores:

```
overall = (practice_exam × 0.34) + (architecture_design × 0.33) + (cdk_synth × 0.33)
```

### Properties

- **Range**: 0.0 to 1.0
- **Perfect score**: A model scoring 1.0 in all categories receives an overall of 1.0
- **Missing categories**: Treated as 0.0 (penalizes incomplete runs)
- **Equal weighting**: All three categories contribute roughly equally, reflecting that SA work requires knowledge, reasoning, and implementation skills

## Per-Category Calculation

### Practice Exam & CDK

For binary pass/fail tasks:

```
category_score = correct_count / total_count
```

### Architecture Design

For rubric-scored tasks:

```
category_score = mean(sample_scores)
```

Where each sample score is the average of accuracy, completeness, and quality dimensions.

## Interpretation Notes

1. **Scores are not percentages**: While scores range from 0-1, they represent accuracy within each category's specific methodology
2. **Category scores are comparable**: A 0.7 in Practice Exam represents similar mastery as 0.7 in Architecture Design
3. **Overall is a summary**: Use category scores for detailed capability analysis
4. **CDK reliability**: The CDK track has known reliability issues being addressed; 0% scores may reflect evaluation bugs rather than model capability

## Technical Implementation

- **Registry**: `scripts/task_registry.py` defines weights and scoring configuration
- **Aggregation**: `scripts/aggregate_multi.py` computes leaderboard from Inspect logs
- **Tests**: `tests/test_task_registry.py` enforces weight normalization
- **Validation**: Weights are tested to sum to exactly 1.0

## Changelog

- **2026-01-05**: Normalized weights to sum to 1.0 (was 1.6). Equal weighting: 0.34/0.33/0.33.
