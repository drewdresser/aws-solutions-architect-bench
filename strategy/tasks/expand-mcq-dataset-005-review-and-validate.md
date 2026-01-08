# Task: Review, Validate, and Finalize Dataset

**Epic:** [expand-mcq-dataset.md](../epics/expand-mcq-dataset.md)
**Size:** `S`
**Status:** `Done`

## Context

After generating new questions, we need to review them for quality, ensure schema compliance, verify technical accuracy, and confirm the dataset meets the epic's success criteria.

## Acceptance Criteria

- [ ] All items pass JSON schema validation
- [ ] Total item count is 50+ (target: 50-55)
- [ ] Each item has consistent metadata:
  - [ ] `difficulty` field present (sa_associate/sa_pro)
  - [ ] `domain` field present and standardized
  - [ ] `aws_services` array present
- [ ] Balance verification:
  - [ ] ~25 Associate / ~25 Professional questions
  - [ ] At least 15 unique domains covered
  - [ ] ~60% single-select / ~40% multi-select
- [ ] No duplicate or near-duplicate questions
- [ ] All answers are technically accurate per current AWS best practices
- [ ] Multi-select questions have clear "(Select TWO.)" or similar instructions
- [ ] Run eval to verify questions work with the scoring system

## Technical Notes

**Relevant Files:**
- `evals/practice_exam/aws_sa.jsonl` — Full dataset
- `evals/practice_exam/tasks.py` — Eval task definition

**Validation Script:**
```python
import json
from collections import Counter

dataset = "evals/practice_exam/aws_sa.jsonl"
items = [json.loads(line) for line in open(dataset).read().strip().split("\n")]

print(f"Total items: {len(items)}")

# Check required fields
required_meta = ["difficulty", "domain"]
for item in items:
    meta = item.get("metadata", {})
    missing = [f for f in required_meta if f not in meta]
    if missing:
        print(f"Missing metadata: {missing} in question starting with '{item['input'][:50]}...'")

# Distribution stats
difficulties = Counter(i["metadata"]["difficulty"] for i in items)
domains = Counter(i["metadata"]["domain"] for i in items)
multi_select = sum(1 for i in items if isinstance(i["target"], list))

print(f"\nDifficulty distribution: {dict(difficulties)}")
print(f"Multi-select questions: {multi_select}/{len(items)}")
print(f"\nDomain distribution:")
for domain, count in sorted(domains.items()):
    print(f"  {domain}: {count}")
```

**Quality Checks:**
1. Read through each generated question
2. Verify the correct answer is actually correct
3. Ensure wrong answers are plausible but clearly wrong
4. Check that question complexity matches difficulty level
5. Verify multi-select questions specify how many answers to select

**Approach:**
1. Run validation script on full dataset
2. Manual review of each new generated question
3. Fix any technical inaccuracies
4. Run the practice exam eval to verify scoring works
5. Generate final statistics

**Gotchas:**
- Don't modify existing questions unless fixing errors
- Ensure all domains use consistent naming (lowercase, snake_case)
- Watch for questions that test the same concept with different wording

## Dependencies

- **Blocked by:** Tasks 002, 003, 004 (all generation/tagging tasks)
- **Blocks:** None (final task)

## Verification

```bash
# Final item count
wc -l evals/practice_exam/aws_sa.jsonl
# Should be 50+

# Run full validation
uv run python -c "
import json
items = [json.loads(l) for l in open('evals/practice_exam/aws_sa.jsonl')]
print(f'Total items: {len(items)}')
print(f'All have difficulty: {all(\"difficulty\" in i.get(\"metadata\", {}) for i in items)}')
print(f'All have domain: {all(\"domain\" in i.get(\"metadata\", {}) for i in items)}')
print(f'All have aws_services: {all(\"aws_services\" in i.get(\"metadata\", {}) for i in items)}')

from collections import Counter
print(f'Difficulty: {dict(Counter(i[\"metadata\"][\"difficulty\"] for i in items))}')
print(f'Domains: {len(set(i[\"metadata\"][\"domain\"] for i in items))} unique')
"

# Run the practice exam eval to verify everything works
uv run inspect eval evals/practice_exam/tasks.py --limit 5 --model openai/gpt-4o-mini
```
