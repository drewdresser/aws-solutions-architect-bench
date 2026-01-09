# SA Bench

[![Leaderboard](https://img.shields.io/badge/Leaderboard-Live-brightgreen)](https://drewdresser.github.io/aws-solutions-architect-bench/)
[![Nightly Benchmark](https://github.com/drewdresser/aws-solutions-architect-bench/actions/workflows/bench.yaml/badge.svg)](https://github.com/drewdresser/aws-solutions-architect-bench/actions/workflows/bench.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> Measuring LLM performance on AWS Solutions Architect tasks

**[Live Leaderboard](https://drewdresser.github.io/aws-solutions-architect-bench/)** | **[Launch Post](docs/LAUNCH_POST.md)** | [Scoring Methodology](docs/SCORING.md) | [Reproduce Results](#-reproduce-the-leaderboard)

## What is SA Bench?

SA Bench is an open-source benchmark that evaluates AI models on real AWS Solutions Architect work—not just certification questions, but practical tasks like architecture design and infrastructure-as-code generation.

**Current findings:**
- Top models score 95% on certification-style questions but under 10% on CDK code generation
- The gap between "knowing the answer" and "writing working code" is enormous
- Model choice matters significantly (35 percentage point spread on practice exams)

Read the [full launch post](docs/LAUNCH_POST.md) for methodology details and analysis.

## 🎯 Vision

The AWS Solutions Architect Bench aims to become the definitive benchmark for measuring AI model capabilities on authentic AWS Solutions Architect responsibilities:

- **Real-world scenarios**: Evaluations mirror actual day-to-day SA tasks
- **Practical skills**: Beyond certification knowledge to hands-on implementation
- **Comprehensive coverage**: From architecture design to CDK code generation
- **Industry relevance**: Tasks based on common customer requirements and patterns

## 📊 Current Evaluations

### 1. AWS Practice Exam (`evals/practice_exam/`)
Multiple-choice questions covering AWS Solutions Architect certification topics.
- **Format**: Single and multi-answer questions
- **Topics**: Core AWS services, architecture patterns, best practices
- **Scoring**: Choice-based with answer shuffling
- **Dataset**: `aws_sa.jsonl`

### 2. AWS CDK Synthesis (`evals/cdk_synth/`)
Tests ability to generate valid AWS CDK Python code that compiles and passes validation.
- **Format**: Code generation from natural language requirements
- **Validation**: `cdk synth` and optional `cfn-lint` (Docker or local execution)
- **Real-world focus**: Common infrastructure patterns and use cases
- **Known issues**: See [docs/CDK_FAILURE_MODES.md](docs/CDK_FAILURE_MODES.md) for troubleshooting

### 3. AWS Architecture Design (`evals/architecture_design/`)
Evaluates architectural reasoning across diagram interpretation and solution design.
- **Interpretation prompts**: Ask the model to analyze an AWS diagram, identify services, trace flows, or assess risks—with the PNG diagram embedded inline for vision-capable models
- **Creation prompts**: Require the model to draft new architectures from textual requirements or migration scenarios
- **Artifacts**: JSONL samples reference PNG diagrams stored in `diagrams/`; the solver embeds them as base64 images (and also preserves the file path for text-only fallbacks)
- **Scoring**: Custom heuristic scorer averaging accuracy, completeness, and quality based on rubric metadata

## 📏 Scoring Methodology

See **[docs/SCORING.md](docs/SCORING.md)** for detailed documentation of how scores are computed, including:
- Per-category scoring methods
- Overall score formula (weighted average)
- Weight rationale and normalization

## 🔄 Reproduce the Leaderboard

Reproduce published leaderboard results with a single command:

```bash
git clone https://github.com/drewdresser/aws-sa-bench
cd aws-sa-bench
uv sync
cp .env.example .env  # Add your OPENROUTER_API_KEY
make bench && make board.json
cat results/leaderboard.json
```

**Requirements:** Python 3.12+, Docker (running), [uv](https://docs.astral.sh/uv/), OpenRouter API key

**Expected output:** `results/leaderboard.json` and `results/leaderboard.csv` containing model scores across all evaluation categories.

See [Reproducibility](#reproducibility) below for expected variance between runs.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker (for CDK evaluations)
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone and install dependencies:**
   ```bash
   git clone https://github.com/drewdresser/aws-sa-bench
   cd aws-sa-bench
   uv sync
   ```

2. **Set up API credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your OPENROUTER_API_KEY
   ```

3. **Run a single evaluation:**
   ```bash
   inspect eval evals/practice_exam/tasks.py --model openrouter/anthropic/claude-sonnet-4
   ```

4. **Run comprehensive benchmark:**
   ```bash
   inspect eval-set evals/practice_exam/tasks.py evals/cdk_synth/tasks.py \
     --model openrouter/anthropic/claude-sonnet-4,openrouter/openai/gpt-4.1 \
     --logs-dir logs/benchmark-$(date +%Y%m%d)
   ```

5. **Run architecture design evaluation (vision-capable model recommended):**
   ```bash
   inspect eval evals/architecture_design/tasks.py:architecture_design \
     --model openrouter/anthropic/claude-sonnet-4 --max-samples 5
   ```
   Models without vision support still receive the textual question and the original diagram path, but results will be stronger with multimodal models.

### Troubleshooting

- **Docker not running:** CDK evaluations require Docker. Start Docker Desktop or `docker daemon`.
- **API key errors:** Ensure `OPENROUTER_API_KEY` is set in `.env` (not just exported in shell).
- **uv not found:** Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## 🏗️ Architecture

Part of the fun of starting this repo was to explore the [Inspect AI](https://inspect.ai-safety-institute.org.uk/) framework for robust, reproducible evaluations.

### Key Components

- **Tasks**: Evaluation definitions using Inspect AI decorators
- **Solvers**: Chain-of-thought, generate, self-critique, multiple-choice
- **Scorers**: Custom verification (CDK synthesis) and choice-based scoring
- **Sandbox**: Docker environments for safe code execution
- **Datasets**: JSONL format with structured field specifications

### Directory Structure

```
├── evals/                    # Main evaluation modules
│   ├── practice_exam/        # Certification-style questions
│   │   ├── tasks.py          # Task definition
│   │   └── aws_sa.jsonl      # Question dataset
│   └── cdk_synth/           # Infrastructure as Code
│       ├── tasks.py          # CDK generation task
│       ├── cdk_synth.jsonl   # Requirements dataset
│       ├── Dockerfile        # CDK environment
│       └── compose.yaml      # Container configuration
├── scripts/                  # Utilities and aggregation
├── demo/                     # Example evaluations
└── results/                  # Evaluation outputs
```

## 🎮 Supported Models

The benchmark supports various AI models through OpenRouter.

### OpenAI Models
- `openrouter/openai/o3`
- `openrouter/openai/gpt-4.1`
- `openrouter/openai/gpt-4.1-mini`

### Anthropic Models
- `openrouter/anthropic/claude-sonnet-4`
- `openrouter/anthropic/claude-opus-4`

### Google Models
- `openrouter/google/gemini-2.5-flash`
- `openrouter/google/gemini-pro`

### Others
- `openrouter/x-ai/grok-3-mini`
- `openrouter/amazon/nova-pro-v1`
- And many more through OpenRouter

## 📈 Roadmap

### Near Term
- [ ] Architecture design evaluations (diagram interpretation and creation)
- [ ] Cost optimization scenarios
- [ ] Security assessment tasks
- [ ] CloudTrail log dump needle in a haystack

### Medium Term
- [ ] Terraform generation alongside CDK
- [ ] Multi-account strategy evaluations
- [ ] Performance optimization scenarios
- [ ] Customer interaction simulations

### Long Term
- [ ] Full SA workflow evaluations
- [ ] Live AWS environment testing (with proper safeguards)
- [ ] Collaborative solution design tasks

## 🤝 Contributing

We welcome contributions that advance the benchmark's goal of measuring real-world AWS SA capabilities:

1. **New evaluation types**: Focus on authentic SA responsibilities
2. **Dataset expansion**: Add more diverse, realistic scenarios
3. **Improved scoring**: Better metrics for practical skill assessment
4. **Documentation**: Help others understand and use the benchmark


## 🔗 Related Projects

- [Inspect AI Framework](https://inspect.ai-safety-institute.org.uk/)
- [AWS CDK](https://aws.amazon.com/cdk/)
- [AWS Solutions Architect Certification](https://aws.amazon.com/certification/certified-solutions-architect-associate/)

---

**Note**: This benchmark is designed for evaluating AI model capabilities and is not affiliated with or endorsed by Amazon Web Services, Inc.
