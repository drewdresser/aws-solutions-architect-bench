# Repository Guidelines

## Project Structure & Module Organization
Keep Python evaluation logic inside `evals/`. `evals/practice_exam/` holds multiple-choice tasks and the `aws_sa.jsonl` dataset; `evals/cdk_synth/` pairs task definitions with Docker assets for CDK validation. Shared helpers live in `scripts/`, while generated outputs belong in `results/` and published artifacts in `docs/`. Use `demo/` for lightweight examples or spikes so the main modules stay production-focused.

## Build, Test, and Development Commands
Install or refresh dependencies with `uv sync`. Run a targeted evaluation locally via `uv run inspect eval evals/practice_exam/tasks.py --model <model-id>`. Execute the full benchmark with `uv run inspect eval-set evals/practice_exam/tasks.py evals/cdk_synth/tasks.py --model <model-list> --logs-dir logs/<tag>`. When working on CDK flows, pre-build the container once using `docker compose -f evals/cdk_synth/compose.yaml build` to mirror CI validation.

## Coding Style & Naming Conventions
Write Python for 3.12+ using 4-space indentation and PEP 8 conventions. Prefer descriptive task names (`aws_solutions_architect`) and snake_case module files. Decorate new evaluations with `@task` and keep docstrings concise but actionable. Datasets stay in JSONL with kebab-case filenames; append entries rather than reordering to keep diffs reviewable.

## Testing Guidelines
Treat every new dataset or solver change as a runnable test: execute the relevant `inspect eval` and store logs under `logs/`. For CDK changes, ensure the synthesized stacks pass both `cdk synth` and `cfn-lint` inside the provided Docker workflow. Add regression prompts to `demo/` when debugging so others can reproduce failures quickly.

## Commit & Pull Request Guidelines
Match the existing conventional-emoji style, e.g., `✨ feat: add VPC peering scenarios`. Keep the subject line under ~70 characters and use imperative voice. Pull requests should outline the evaluation scope, list impacted datasets, and attach key log snippets or `results/` artifacts. Link related issues, note required credentials, and include screenshots only when UI assets change.

## Security & Configuration Tips
Copy `.env.example` to `.env`, inject OpenRouter keys locally, and never commit secrets or customer data. Scrub generated logs before sharing, and prefer redacting account IDs over deleting evidence needed for reproducibility.
