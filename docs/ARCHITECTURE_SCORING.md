# Architecture Scoring Rubric

This document explains how architecture evaluation responses are scored in SA Bench.

## Overview

Architecture tasks are scored using an **LLM-as-judge approach** with transparent rubrics. A judge model evaluates each response across three dimensions, combining nuanced reasoning assessment with deterministic checks.

## Scoring Dimensions

Every architecture response is scored on three dimensions, each ranging from 0% to 100%:

### Accuracy (0-100%)

How well the response matches the expected answer and demonstrates correct AWS knowledge.

| Score Range | Description |
|-------------|-------------|
| **90-100%** | All key elements correctly identified with proper AWS naming and accurate technical details |
| **70-89%** | Most elements correct, minor gaps or naming variations |
| **50-69%** | Core elements present but with notable omissions |
| **30-49%** | Several errors or major omissions |
| **0-29%** | Fundamental errors or missing most expected content |

### Completeness (0-100%)

Whether all required elements are covered thoroughly.

| Score Range | Description |
|-------------|-------------|
| **90-100%** | All expected elements addressed with detailed explanations |
| **70-89%** | Most elements covered with adequate depth |
| **50-69%** | Partial coverage, some elements superficial |
| **30-49%** | Many elements missing or barely mentioned |
| **0-29%** | Minimal coverage of expected content |

### Quality (0-100%)

Reasoning depth, structure, and professional presentation.

| Score Range | Description |
|-------------|-------------|
| **90-100%** | Well-organized, uses proper terminology, shows deep AWS expertise |
| **70-89%** | Clear structure, appropriate terminology |
| **50-69%** | Adequate but could be better organized |
| **30-49%** | Disorganized or uses incorrect terminology |
| **0-29%** | Poor structure, significant terminology errors |

## Task Subtypes

### Diagram Interpretation Tasks

These tasks present an architecture diagram and ask the model to analyze it.

#### Service Identification
**What it tests**: Ability to recognize AWS services from diagrams and explain their roles.

**Good response example**:
> "The architecture includes **Amazon EC2** instances for the web and application tiers, providing compute capacity for hosting the application logic. **Amazon RDS** serves as the managed database with Multi-AZ deployment for high availability. An **Elastic Load Balancer** distributes traffic across EC2 instances..."

**Poor response example**:
> "Uses EC2, RDS, ELB for the app."

#### Data Flow Analysis
**What it tests**: Tracing request/response paths through an architecture.

**Good response example**:
> "1. The user's request first reaches the Elastic Load Balancer via HTTPS. 2. The ELB routes the request to an available EC2 instance based on health checks. 3. The web tier processes the request and forwards it to the application tier..."

#### Security Assessment
**What it tests**: Identifying security controls and suggesting improvements.

#### Scalability Analysis
**What it tests**: Understanding scaling mechanisms and potential bottlenecks.

#### Cost Optimization
**What it tests**: Identifying cost drivers and optimization opportunities.

### Diagram Creation Tasks

These tasks give requirements and ask the model to design an architecture.

#### Requirements to Architecture
**What it tests**: Translating business requirements into AWS architecture.

#### Pattern Implementation
**What it tests**: Implementing specific architectural patterns (e.g., event-driven, microservices).

#### Problem Solving
**What it tests**: Designing solutions for migration or complex scenarios.

## How Scoring Works

### Blended Approach

Final scores combine:
- **70% LLM Judge**: Nuanced evaluation of reasoning and completeness
- **30% Deterministic Checks**: Keyword matching for expected elements

This blend prevents pure gaming of the judge while capturing nuanced quality.

### Anti-Gaming Measures

The scoring system includes mechanisms to prevent gaming:

1. **Hidden Criteria**: Additional evaluation criteria not detailed in public documentation
2. **Length Penalties**: Very short responses (< 50 words) receive reduced scores
3. **Repetition Detection**: Padding with repetitive content is penalized
4. **Deterministic Anchoring**: Keyword checks ensure expected content is present

These measures ensure that scores reflect genuine architectural understanding, not just gaming the evaluation.

## Overall Score Calculation

The overall score for an architecture response is:

```
overall = (accuracy + completeness + quality) / 3
```

## Expected Variance

Architecture scores may vary **±10%** between runs due to:
- LLM judge non-determinism
- Model API routing variations
- Temperature settings

This variance is expected and acceptable for benchmark comparisons.

## Calibration

The LLM judge has been calibrated against human-scored responses:
- **Target agreement rate**: ≥80% within tolerance
- **Tolerance**: ±0.15 per dimension
- **Calibration set**: 12 responses across quality tiers

See `scripts/measure_judge_agreement.py` for calibration methodology.

## Configuring the Judge Model

By default, the judge uses `openai/gpt-4o-mini`. Override with:

```bash
export ARCHITECTURE_JUDGE_MODEL="anthropic/claude-3-5-sonnet"
```

## Related Documentation

- [Main Scoring Documentation](SCORING.md)
- [Structured Output Formats](STRUCTURED_OUTPUTS.md) - Mermaid, PlantUML, JSON validation
- [CDK Failure Modes](CDK_FAILURE_MODES.md)
