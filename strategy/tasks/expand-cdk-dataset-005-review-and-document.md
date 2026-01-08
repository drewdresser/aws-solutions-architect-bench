# Task: Review Dataset and Document Prompt Contract

**Epic:** [expand-cdk-dataset.md](../epics/expand-cdk-dataset.md)
**Size:** `S`
**Status:** `Done`

## Context

After expanding the dataset, review all items for quality and consistency, then document the "prompt contract" that specifies expected input/output format. This ensures evaluation is fair and prompts are unambiguous.

## Acceptance Criteria

- [x] All 40+ items reviewed for quality and synthesizability
- [x] Prompt contract documented in `docs/CDK_PROMPT_CONTRACT.md`
- [x] Dataset statistics computed and documented
- [x] Any problematic items fixed or removed
- [x] EPICS.md updated to mark epic as Done

## Technical Notes

**Target Files:**
- `evals/cdk_synth/cdk_synth.jsonl` — Final review
- `docs/CDK_PROMPT_CONTRACT.md` — New documentation
- `strategy/epics/expand-cdk-dataset.md` — Status update
- `strategy/EPICS.md` — Summary update

**Prompt Contract Contents:**

```markdown
# CDK Synthesis Prompt Contract

## Overview

This document specifies the format and expectations for CDK synthesis evaluation items.

## Input Format

Each CDK prompt explicitly:
- Specifies Python as the implementation language
- Requests AWS CDK v2 (aws-cdk-lib)
- Asks for "a complete CDK app that can be synthesized"
- Describes the architecture requirements clearly

## Expected Output

Model responses should:
- Provide complete, runnable Python code
- Include all necessary imports
- Define a Stack class and App instantiation
- Call app.synth() at the end

## Evaluation Criteria

- **Pass**: `cdk synth` exits with code 0
- **Fail**: Any synthesis error (missing imports, syntax errors, invalid constructs)

## Metadata Schema

```json
{
  "id": "cdk_XXX",
  "input": "Write a Python AWS CDK v2 app...",
  "target": null,
  "metadata": {
    "difficulty": "beginner|intermediate|advanced",
    "domains": ["networking", "security", ...],
    "aws_services": ["VPC", "Lambda", ...],
    "skill": "legacy_domain_tag"
  }
}
```

## Difficulty Levels

- **Beginner**: Single service, basic configuration
- **Intermediate**: 2-4 services, common patterns
- **Advanced**: 5+ services, complex architectures

## Domain Categories

[List all domains with descriptions]
```

**Dataset Statistics to Compute:**

```bash
# Total items
wc -l evals/cdk_synth/cdk_synth.jsonl

# Difficulty distribution
cat evals/cdk_synth/cdk_synth.jsonl | jq -r '.metadata.difficulty' | sort | uniq -c

# Domain distribution
cat evals/cdk_synth/cdk_synth.jsonl | jq -r '.metadata.domains[]' | sort | uniq -c

# Unique AWS services
cat evals/cdk_synth/cdk_synth.jsonl | jq -r '.metadata.aws_services[]' | sort -u | wc -l
```

**Quality Review Checklist:**
- [ ] Each prompt specifies Python + CDK v2
- [ ] Each prompt has clear, unambiguous requirements
- [ ] No prompts require external resources
- [ ] Difficulty ratings are consistent
- [ ] Domain tags are accurate
- [ ] AWS services lists are complete

**Approach:**
1. Run synthesis test on sample of items (5-10)
2. Review prompts for clarity and consistency
3. Fix any issues found
4. Write prompt contract documentation
5. Compute and record statistics
6. Update epic status

**Gotchas:**
- Don't just count items — verify quality
- Document any patterns that frequently fail
- Include examples in prompt contract
- Update CDK_FAILURE_MODES.md if new patterns found

## Dependencies

- **Blocked by:** Tasks 002, 003, 004
- **Blocks:** None (epic completion)

## Verification

```bash
# Verify final count
wc -l evals/cdk_synth/cdk_synth.jsonl
# Should be 40+

# Verify prompt contract exists
cat docs/CDK_PROMPT_CONTRACT.md | head -20

# Verify epic status updated
grep "Status" strategy/epics/expand-cdk-dataset.md
# Should show "Done"

# Run full CDK eval to verify dataset works
make bench.cdk  # or equivalent
```
