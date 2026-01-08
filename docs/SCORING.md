# SA Bench Scoring Methodology

This document describes how SA Bench computes scores for the leaderboard.

## Categories

SA Bench evaluates models across three categories, each measuring a different aspect of Solutions Architect capability.

### Practice Exam (MCQ)

| Property | Value |
|----------|-------|
| **What it measures** | AWS certification-style knowledge—service selection, best practices, and architectural decision-making |
| **Dataset** | `evals/practice_exam/aws_sa.jsonl` |
| **Sample count** | 50 questions |
| **Scoring** | Binary (1.0 if correct, 0.0 if incorrect) |
| **Metric** | `choice` scorer from Inspect AI |
| **Weight** | 34% |
| **Confidence** | High |
| **Expected variance** | ±5% |

### Architecture Design

| Property | Value |
|----------|-------|
| **What it measures** | Architectural reasoning, diagram understanding, data flow analysis, security assessment, and scalability analysis |
| **Dataset** | `evals/architecture_design/architecture_interpretation.jsonl` |
| **Sample count** | 28 tasks |
| **Scoring** | Rubric-based score in [0, 1] combining accuracy, completeness, and quality dimensions |
| **Metric** | `architecture_scorer` (heuristic) or `llm_judge_scorer` (LLM-as-judge) |
| **Weight** | 33% |
| **Confidence** | Medium |
| **Expected variance** | ±10% |

- **Detailed rubrics**: See [ARCHITECTURE_SCORING.md](ARCHITECTURE_SCORING.md) for LLM judge rubrics and anti-gaming mechanisms
- **Structured outputs**: See [STRUCTURED_OUTPUTS.md](STRUCTURED_OUTPUTS.md) for diagram format validation (Mermaid, PlantUML, JSON)

### CDK Synthesis

| Property | Value |
|----------|-------|
| **What it measures** | Infrastructure-as-code generation—ability to produce valid AWS CDK Python code that synthesizes without errors |
| **Dataset** | `evals/cdk_synth/cdk_synth.jsonl` |
| **Sample count** | 40 prompts |
| **Scoring** | Binary (1.0 if `cdk synth` succeeds, 0.0 if it fails) |
| **Metric** | `cdk_verify` or `cdk_verify_local` scorer |
| **Weight** | 33% |
| **Confidence** | High |
| **Expected variance** | ±5% |

- **Known issues**: See [CDK_FAILURE_MODES.md](CDK_FAILURE_MODES.md) for extraction, synthesis, and environment failure documentation
- **Prompt contract**: See [CDK_PROMPT_CONTRACT.md](CDK_PROMPT_CONTRACT.md) for input/output format specification

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

## Understanding Score Confidence

### Confidence Levels

| Level | Meaning | Example Categories |
|-------|---------|-------------------|
| **High** | Scores are reliable within ±5%. Small sample variance. | Practice Exam, CDK Synthesis |
| **Medium** | Scores may vary ±10%. LLM judge introduces additional variance. | Architecture Design |
| **Low** | Scores may vary significantly. Use for directional comparison only. | (none currently) |

### Interpreting Close Scores

When comparing models:
- **Within 5%**: Consider them statistically equivalent
- **5-10% difference**: Likely meaningful for high-confidence categories
- **>10% difference**: Definite capability difference

### Factors Affecting Variance

1. **LLM non-determinism**: Models may give different responses to the same prompt
2. **API routing**: OpenRouter may route to different model instances
3. **LLM judge variance**: Architecture scoring uses LLM-as-judge which adds variance
4. **Prompt caching**: Cached vs. fresh prompts may produce different outputs

## Technical Implementation

- **Registry**: `scripts/task_registry.py` defines weights and scoring configuration
- **Aggregation**: `scripts/aggregate_multi.py` computes leaderboard from Inspect logs
- **Tests**: `tests/test_task_registry.py` enforces weight normalization
- **Validation**: Weights are tested to sum to exactly 1.0

## Reproducibility

### Expected Variance

Due to LLM non-determinism, scores may vary between runs:

| Category | Expected Variance | Reason |
|----------|-------------------|--------|
| **Practice Exam (MCQ)** | ±2-5% | Discrete answers, low variance |
| **Architecture Design** | ±5-10% | Rubric scoring, moderate variance |
| **CDK Synthesis** | ±5% | Binary pass/fail, but extraction varies |
| **Overall** | ±5% | Aggregated variance |

### Maximizing Reproducibility

For the most consistent results:

1. **Use `temperature=0`** when supported by the model provider
2. **Run full dataset** (avoid `--limit` flags) for stable averages
3. **Pin model versions** when possible (some providers update models)
4. **Use identical environment** (same Python version, dependencies)

### Tolerance for Leaderboard

A fresh benchmark run is considered **reproducible** if overall scores fall within **±5%** of published leaderboard values.

For example, if a model shows 72% overall on the leaderboard:
- Scores between 67-77% are within expected variance
- Scores outside this range may indicate configuration differences

### Factors Affecting Variance

- **Model updates**: Providers may update models without version changes
- **API routing**: OpenRouter may route to different model instances
- **Temperature**: Even at `temperature=0`, some models have residual randomness
- **Prompt caching**: Cached vs. fresh prompts may produce different outputs

## JSON Schema

The leaderboard JSON includes category metadata for programmatic access:

```json
{
  "_metadata": {
    "generated_at": "2026-01-07T00:00:00Z",
    "run_id": "local-20260107-000000",
    "model_count": 5,
    "categories": {
      "practice_exam": {
        "name": "Practice Exam",
        "description": "AWS certification-style MCQ questions...",
        "weight": 0.34,
        "sample_count": 50,
        "scoring": "binary",
        "confidence": "high",
        "margin": "±5%"
      }
    }
  },
  "models": [
    { "model": "...", "practice_exam": 0.85, "overall": 0.34 }
  ]
}
```

### Schema Fields

| Field | Type | Description |
|-------|------|-------------|
| `_metadata.generated_at` | ISO 8601 | Timestamp of leaderboard generation |
| `_metadata.run_id` | string | GitHub run ID or local identifier |
| `_metadata.model_count` | integer | Number of models evaluated |
| `_metadata.categories` | object | Per-category metadata (see below) |
| `models` | array | Model scores |

### Category Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable category name |
| `description` | string | What the category measures |
| `weight` | number | Weight in overall score (0-1) |
| `sample_count` | integer | Number of items in dataset |
| `scoring` | string | "binary" or "rubric" |
| `confidence` | string | "high", "medium", or "low" |
| `margin` | string | Expected variance (e.g., "±5%") |

Full schema: `schemas/leaderboard.schema.json`

## Changelog

- **2026-01-07**: Added category metadata to JSON schema (sample_count, confidence, margin)
- **2026-01-07**: Added score confidence documentation
- **2026-01-05**: Added reproducibility documentation
- **2026-01-05**: Normalized weights to sum to 1.0 (was 1.6). Equal weighting: 0.34/0.33/0.33.
