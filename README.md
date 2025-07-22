# AWS Solutions Architect Bench

A comprehensive evaluation framework for testing AI model performance on real-world AWS Solutions Architect tasks. This benchmark goes beyond simple multiple-choice questions to evaluate practical skills that AWS Solutions Architects use daily.

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
- **Validation**: Docker-based environment with `cdk synth` and `cfn-lint`
- **Real-world focus**: Common infrastructure patterns and use cases

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker (for CDK evaluations)
- uv package manager

### Installation

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd aws-solutions-architect-bench
   uv sync
   ```

2. **Set up API credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenRouter API key
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