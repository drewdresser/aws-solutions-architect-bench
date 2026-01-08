# Task: Create MCQ Generation Script

**Epic:** [expand-mcq-dataset.md](../epics/expand-mcq-dataset.md)
**Size:** `M`
**Status:** `Todo`

## Context

Similar to the architecture dataset expansion, we need a PEP723 script to efficiently generate new MCQ items using OpenAI (via OpenRouter). This script will ensure schema consistency and enable rapid, high-quality question generation across different AWS domains and difficulty levels.

## Acceptance Criteria

- [ ] Script uses PEP723 inline metadata for dependencies (openai, pydantic, python-dotenv)
- [ ] Script can be run with `uv run scripts/generate_mcq_items.py`
- [ ] Generates items matching the exact JSONL schema of existing items
- [ ] Accepts CLI arguments for: domain, difficulty (sa_associate/sa_pro), count, output file
- [ ] Uses structured outputs (JSON mode) to ensure valid schema
- [ ] Includes validation that generated items match expected schema
- [ ] Supports both single-select and multi-select question generation
- [ ] Generates realistic AWS certification-style questions

## Technical Notes

**Relevant Files:**
- `evals/practice_exam/aws_sa.jsonl` — Target schema to match
- `scripts/generate_arch_items.py` — Reference implementation pattern
- `evals/practice_exam/tasks.py` — MCQ task definition

**Schema Reference:**
```json
{
  "input": "Question text with instructions like (Select TWO.)",
  "choices": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
  "target": "A" | ["A", "B"],
  "metadata": {
    "difficulty": "sa_associate" | "sa_pro",
    "domain": "networking|compute|storage|security|..."
  }
}
```

**Supported Domains:**
- compute, storage, networking, security, database
- serverless, messaging, high_availability, scaling
- cost, cost_management, iam, operations
- big_data, architecture, global_architecture, modernization
- NEW: compliance, data_analytics, disaster_recovery, integration, migration, ml_ai, monitoring, management

**Approach:**
1. Mirror the PEP723 pattern from generate_arch_items.py
2. Create Pydantic models for MCQ schema validation
3. Build prompts that generate AWS certification-style questions
4. Support --multi-select flag for generating multi-answer questions
5. Use OpenRouter with same pattern as architecture script

**Gotchas:**
- Choice format should use letter prefixes (A., B., C., etc.) in the choices array for clarity
- Target field is string for single-select, array for multi-select
- Multi-select questions should include "(Select TWO.)" or similar in the input
- Questions must be technically accurate per AWS best practices

## Dependencies

- **Blocked by:** None
- **Blocks:** Tasks 002-004 (generation tasks use this script)

## Verification

```bash
# Script runs without errors
uv run scripts/generate_mcq_items.py --help

# Generates valid single-select item
uv run scripts/generate_mcq_items.py --domain networking --difficulty sa_associate --count 1 --dry-run

# Generates valid multi-select item
uv run scripts/generate_mcq_items.py --domain security --difficulty sa_pro --multi-select --count 1 --dry-run

# Validate output schema
python -c "import json; [json.loads(l) for l in open('test_output.jsonl')]"
```
