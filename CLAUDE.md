# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an AI model evaluation repository using the Inspect AI framework. It contains evaluations for testing AI model performance on AWS-related tasks, including AWS Solutions Architect practice exams and AWS CDK code generation.

## Development Commands

### Dependencies
```bash
uv sync  # Install all dependencies
```

### Running Evaluations
```bash
# Run a single evaluation
inspect eval <path_to_eval>.py --model <model_name>

# Example: Run CDK synth evaluation
inspect eval evals/cdk_synth/tasks.py --model openai/gpt-4.1 --log-dir results/

# Run multiple models against an evaluation set
inspect eval-set <path_to_eval>.py --model openai/gpt-4.1,anthropic/claude-sonnet-4 --logs-dir logs/<unique_folder_name>
```

## Architecture

### Core Framework
- Built on **Inspect AI** framework for model evaluation
- Uses **uv** for Python dependency management
- Requires Python 3.12+

### Evaluation Structure
- `evals/` - Main evaluation modules, each containing:
  - `tasks.py` - Task definition using Inspect AI decorators
  - `*.jsonl` - Dataset files with evaluation samples
  - Supporting files (Dockerfile, compose.yaml for containerized evaluations)

- `demo/` - Simple example evaluations for learning the framework
- `scripts/` - Utility scripts for aggregation and task management
- `results/` and `logs/` - Evaluation outputs and logs

### Task Types

**AWS CDK Synth (`evals/cdk_synth/`)**
- Tests model ability to generate valid AWS CDK Python code
- Uses Docker sandbox with CDK CLI for verification
- Scorer runs `cdk synth` and optional `cfn-lint` validation
- Custom regex extraction for Python code blocks
- Timeout: 60 seconds for synthesis

**AWS Practice Exam (`evals/practice_exam/`)**
- Multiple choice questions for AWS Solutions Architect certification
- Supports both single and multi-answer questions
- Uses choice scorer with shuffle for answer order randomization

### Key Components

**Solvers**: Chain of thought, generate, self-critique, multiple_choice
**Scorers**: Custom `cdk_verify()`, `choice()`, `exact()`
**Datasets**: JSONL format with FieldSpec for input/target/choices mapping
**Sandbox**: Docker-based execution environment for CDK evaluations

### Task Registry
`scripts/task_registry.py` defines evaluation metadata:
- Task aliases and patterns for identification
- Scoring metrics and pass criteria
- Task weighting for composite scoring

## Model Configuration
The repository supports various AI models through OpenRouter and direct APIs. Check README.md for current model list including OpenAI, Anthropic, Google, Mistral, and others.

## Container Setup
CDK evaluations use containerized environments defined in `compose.yaml` files with pre-installed AWS CDK tools.