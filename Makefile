# === aws-solutions-architect-bench :: Makefile ===
# Quick evals + leaderboards. Override vars at call time, e.g.:
#   make eval.practice MODELS=openrouter/openai/gpt-4o
#   make eval.cdk CDK_TASK=evals/cdk_synth/tasks_robust.py LIMIT=5
#   make bench.daily
#
# .env support (OPENROUTER_API_KEY, etc.)
ifneq (,$(wildcard .env))
include .env
export
endif

# ---- Tunables (override via CLI) ----
INSPECT ?= uv run inspect
PY      ?= uv run python

# Comma-separated model list for eval-set/evals
MODELS  ?= openrouter/anthropic/claude-sonnet-4,openrouter/openai/gpt-4.1,openrouter/openai/gpt-5

# Practice (MCQ) task
PRACTICE_TASK ?= evals/practice_exam/tasks.py

# CDK task variant (use tasks.py - the only variant that exists)
CDK_TASK ?= evals/cdk_synth/tasks.py

# Architecture task
ARCH_TASK ?= evals/architecture_design/tasks.py

# Limit items per task (0 = no limit)
LIMIT   ?= 0

# Logs / results
DATE    := $(shell date +%Y%m%d-%H%M%S)
LOGROOT ?= logs
LOGDIR  ?= $(LOGROOT)/run-$(DATE)
RESULTS ?= results
LATEST_LOGS := $(shell ls -dt $(LOGROOT)/* 2>/dev/null | head -1)

# ---- Meta ----
.PHONY: help env deps clean test eval.practice eval.cdk bench bench.daily board.csv board.json board.simple

help:
	@echo "Targets:"
	@echo "  deps           - install Python deps via uv"
	@echo "  test           - run test suite"
	@echo "  env            - bootstrap .env from example if missing"
	@echo "  eval.practice  - run MCQ eval (PRACTICE_TASK)"
	@echo "  eval.cdk       - run CDK eval (CDK_TASK)"
	@echo "  bench          - run both tracks into a single logs dir"
	@echo "  bench.daily    - robust overnight run (uses tasks_robust + full MODELS)"
	@echo "  board.csv      - weighted leaderboard -> results/leaderboard.csv (LATEST_LOGS)"
	@echo "  board.json     - same as above + JSON"
	@echo "  board.simple   - single-run aggregate via scripts/aggregate_inspect.py"
	@echo "Vars: MODELS, LIMIT, LOGDIR, PRACTICE_TASK, CDK_TASK, LOGROOT, RESULTS"

# ---- Setup ----
deps:
	uv sync

test:
	uv run pytest tests/ -v

env:
	@test -f .env || (cp .env.example .env && echo "✓ Created .env from .env.example")

# ---- Evals ----
eval.practice: | $(LOGDIR)
	@echo "▶ Running PRACTICE: $(PRACTICE_TASK)"
	$(INSPECT) eval $(PRACTICE_TASK) \
		$(if $(filter-out 0,$(LIMIT)),--limit $(LIMIT),) \
		--model $(firstword $(subst ,, ,$(MODELS))) \
		--logs-dir $(LOGDIR)

eval.cdk: | $(LOGDIR)
	@echo "▶ Running CDK: $(CDK_TASK)"
	$(INSPECT) eval $(CDK_TASK) \
		$(if $(filter-out 0,$(LIMIT)),--limit $(LIMIT),) \
		--model $(firstword $(subst ,, ,$(MODELS))) \
		--logs-dir $(LOGDIR)

eval.arch: | $(LOGDIR)
	@echo "▶ Running ARCH: evals/architecture_design/tasks.py"
	$(INSPECT) eval evals/architecture_design/tasks.py:architecture_design \
		$(if $(filter-out 0,$(LIMIT)),--limit $(LIMIT),) \
		--model $(firstword $(subst ,, ,$(MODELS))) \
		--log-dir $(LOGDIR)

bench: | $(LOGDIR)
	@echo "▶ Running eval-set across: $(PRACTICE_TASK) + $(CDK_TASK) + $(ARCH_TASK)"
	$(INSPECT) eval-set $(PRACTICE_TASK) $(CDK_TASK) $(ARCH_TASK) \
		$(if $(filter-out 0,$(LIMIT)),--limit $(LIMIT),) \
		--model $(MODELS) \
		--log-dir $(LOGDIR)

bench.daily:
	@$(MAKE) bench CDK_TASK=evals/cdk_synth/tasks.py LIMIT=0 LOGDIR=$(LOGROOT)/nightly-$(DATE)

# ---- Leaderboards ----
$(RESULTS):
	@mkdir -p $(RESULTS)

board.csv: | $(RESULTS)
	@test -n "$(LATEST_LOGS)" || (echo "No logs found under $(LOGROOT)"; exit 1)
	@echo "▶ Aggregating weighted leaderboard from: $(LATEST_LOGS)"
	$(PY) scripts/aggregate_multi.py \
		--log-dir $(LATEST_LOGS) \
		--outfile $(RESULTS)/leaderboard.csv \
		--json-out /dev/null
	@echo "✓ Wrote $(RESULTS)/leaderboard.csv"

board.json: | $(RESULTS)
	@test -n "$(LATEST_LOGS)" || (echo "No logs found under $(LOGROOT)"; exit 1)
	@echo "▶ Aggregating weighted leaderboard (CSV + JSON) from: $(LATEST_LOGS)"
	$(PY) scripts/aggregate_multi.py \
		--log-dir $(LATEST_LOGS) \
		--outfile $(RESULTS)/leaderboard.csv \
		--json-out $(RESULTS)/leaderboard.json
	@echo "✓ Wrote $(RESULTS)/leaderboard.csv and $(RESULTS)/leaderboard.json"

board.simple: | $(RESULTS)
	@test -n "$(LATEST_LOGS)" || (echo "No logs found under $(LOGROOT)"; exit 1)
	@echo "▶ Simple aggregate (single Inspect run) from: $(LATEST_LOGS)"
	$(PY) scripts/aggregate_inspect.py \
		--log-dir $(LATEST_LOGS) > $(RESULTS)/aggregate.txt
	@echo "✓ Wrote $(RESULTS)/aggregate.txt"

# ---- Misc ----
$(LOGDIR):
	@mkdir -p $(LOGDIR)

clean:
	@echo "Cleaning results/*"
	@rm -rf $(RESULTS)/*
