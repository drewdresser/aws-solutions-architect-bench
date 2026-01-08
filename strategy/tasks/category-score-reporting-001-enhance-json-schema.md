# Task: Enhance Leaderboard JSON with Category Metadata

**Epic:** [category-score-reporting.md](../epics/category-score-reporting.md)
**Size:** `S`
**Status:** `Done`

## Context

The current leaderboard JSON includes per-category scores but lacks metadata about each category (description, sample size, weight). Adding this metadata enables the UI to display richer category information and helps users understand what each score represents.

## Acceptance Criteria

- [x] `_metadata.categories` expanded to include per-category details
- [x] Each category includes: name, description, weight, sample_count
- [x] JSON schema updated to reflect new structure
- [x] Backwards compatible (existing fields preserved)
- [x] Tests pass with new schema

## Technical Notes

**Target Files:**
- `scripts/aggregate_multi.py` — Update metadata generation
- `schemas/leaderboard.schema.json` — Update schema definition

**Current Schema:**
```json
{
  "_metadata": {
    "categories": ["practice_exam", "architecture_design", "cdk_synth"]
  }
}
```

**Enhanced Schema:**
```json
{
  "_metadata": {
    "categories": {
      "practice_exam": {
        "name": "Practice Exam",
        "description": "AWS certification-style MCQ questions",
        "weight": 0.34,
        "sample_count": 50,
        "scoring": "binary"
      },
      "architecture_design": {
        "name": "Architecture Design",
        "description": "Diagram interpretation and architectural reasoning",
        "weight": 0.33,
        "sample_count": 28,
        "scoring": "rubric"
      },
      "cdk_synth": {
        "name": "CDK Synthesis",
        "description": "Infrastructure-as-code generation with AWS CDK",
        "weight": 0.33,
        "sample_count": 40,
        "scoring": "binary"
      }
    }
  }
}
```

**Approach:**
1. Update `aggregate_multi.py` to build category metadata dict
2. Pull sample counts from actual dataset files
3. Pull weights from `task_registry.py`
4. Update JSON schema to validate new structure
5. Ensure backwards compatibility with existing consumers

**Gotchas:**
- Don't break existing UI that reads `_metadata.categories` as array
- Consider providing both formats during transition
- Sample counts should be computed dynamically, not hardcoded

## Dependencies

- **Blocked by:** None
- **Blocks:** Task 002 (UI needs this metadata)

## Verification

```bash
# Generate leaderboard and check metadata
make board.json
cat results/leaderboard.json | jq '._metadata.categories'

# Validate against schema
uv run python -c "import jsonschema; ..."

# Run tests
make test
```
