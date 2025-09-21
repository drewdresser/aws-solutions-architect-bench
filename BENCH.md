# Benchmark Runs (Nightly)

This repo benchmarks multiple model families on two tracks:
- **Practice Exam (MCQ)** — fast, stable
- **CDK Synth** — codegen + `cdk synth` inside a network-isolated container
- **Architecture Diagram** - review architecture diagrams

Nightly CI runs `make bench.daily`:
- Uses the **robust** CDK task variant
- Sweeps the default `MODELS` set (see Makefile)
- Aggregates a **weighted leaderboard** (`results/leaderboard.csv/.json`)
- Uploads artifacts + prints a summary table to the workflow page

## Local quickstart

```bash
uv sync
OPENROUTER_API_KEY=... make bench.daily
make board.json
