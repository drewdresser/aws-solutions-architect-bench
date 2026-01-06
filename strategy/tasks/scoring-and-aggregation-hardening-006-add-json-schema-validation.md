# Task: Add JSON Schema Validation for Leaderboard

**Epic:** [scoring-and-aggregation-hardening.md](../epics/scoring-and-aggregation-hardening.md)
**Size:** `M`
**Status:** `Todo`

## Context

The leaderboard.json output has no schema validation. Adding a JSON schema ensures the output format is consistent and documented, making it easier for consumers to integrate with the data.

## Acceptance Criteria

- [ ] `schemas/leaderboard.schema.json` created with JSON Schema definition
- [ ] Schema documents all required fields and types
- [ ] `aggregate_multi.py` validates output against schema before writing
- [ ] Test verifies schema validation catches malformed output
- [ ] Schema is documented in docs/SCORING.md or separate doc

## Technical Notes

**Relevant Files:**
- `schemas/leaderboard.schema.json` — New file
- `scripts/aggregate_multi.py` — Add validation step
- `tests/test_aggregate_multi.py` — Add schema validation test

**Schema definition:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["model", "overall"],
    "properties": {
      "model": {"type": "string"},
      "practice_exam": {"type": "number", "minimum": 0, "maximum": 1},
      "architecture_design": {"type": "number", "minimum": 0, "maximum": 1},
      "cdk_synth": {"type": "number", "minimum": 0, "maximum": 1},
      "overall": {"type": "number", "minimum": 0, "maximum": 1}
    }
  }
}
```

**Approach:**
1. Create schema file
2. Add `jsonschema` to dependencies (or use built-in validation)
3. In `main()`, validate DataFrame-to-JSON output before writing
4. Add test that attempts to write invalid data and expects failure

**Gotchas:**
- Consider whether to fail hard or warn on validation errors
- Schema needs to allow for future category additions

## Dependencies

- **Blocked by:** 002 (need test infra for validation tests)
- **Blocks:** None

## Verification

```bash
# Validate existing leaderboard against schema
uv run python -c "
import json
from jsonschema import validate
with open('schemas/leaderboard.schema.json') as s:
    schema = json.load(s)
with open('results/leaderboard.json') as f:
    data = json.load(f)
validate(data, schema)
print('Valid!')
"
```
