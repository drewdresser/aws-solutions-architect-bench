# Task: Document Known CDK Eval Failure Modes

**Epic:** [cdk-eval-reliability.md](../epics/cdk-eval-reliability.md)
**Size:** `S`
**Status:** `Done`

## Context

The OKR requires publishing a "known failure modes" document. This helps users understand why CDK scores may be lower than expected and what limitations exist.

## Acceptance Criteria

- [ ] `docs/CDK_FAILURE_MODES.md` created
- [ ] Documents extraction failures with examples
- [ ] Documents sandbox/execution failures
- [ ] Documents prompt ambiguity issues
- [ ] Linked from main README and SCORING.md

## Technical Notes

**Relevant Files:**
- `docs/CDK_FAILURE_MODES.md` — New file to create
- `docs/SCORING.md` — Add link to failure modes
- `README.md` — Add link in CDK section

**Content outline:**
```markdown
# CDK Synthesis Evaluation: Known Failure Modes

## Overview
This document describes known limitations and failure modes...

## Code Extraction Failures

### Missing Code Blocks
Models sometimes provide code inline without fencing...
**Example:** [show model output that fails extraction]
**Mitigation:** Use explicit prompt instruction to use ```python blocks

### Multiple Code Blocks
Some models split code across multiple blocks...
**Example:** [show multi-block output]
**Mitigation:** Extraction takes first block; ensure complete code in one block

## Synthesis Failures

### Missing Imports
Models often forget required imports...
**Example:** `from aws_cdk import App, Stack` missing
**Mitigation:** Prompt explicitly lists required imports

### Invalid Construct Usage
Models may use deprecated or non-existent constructs...
**Example:** Using `lambda_.Function` with wrong props
**Mitigation:** Dataset prompts specify CDK v2 requirements

## Environment Failures

### Docker Sandbox Issues
In CI environments, Docker sandbox may fail to start...
**Symptoms:** 0% pass rate, timeout errors
**Mitigation:** Use local execution mode (tasks_local.py)

### Timeout Issues
Complex CDK stacks may exceed 60-second timeout...
**Mitigation:** Increase VERIFY_TIMEOUT or simplify prompts

## Prompt Ambiguity

### Underspecified Requirements
Vague prompts lead to valid but unverifiable code...
**Example:** "Create an S3 bucket" (many valid approaches)
**Mitigation:** Prompts specify exact requirements

## How to Interpret CDK Scores

- 0% may indicate evaluation infrastructure failure, not model capability
- Pass/fail is binary; partial credit not given
- Scores vary based on extraction success, not just code quality
```

**Gotchas:**
- Collect real failure examples from logs
- Keep document concise and actionable
- Update as new failure modes are discovered

## Dependencies

- **Blocked by:** 002, 003 (need to diagnose issues first to document them)
- **Blocks:** None

## Verification

```bash
# Check document exists and is linked
test -f docs/CDK_FAILURE_MODES.md
grep -q "CDK_FAILURE_MODES" docs/SCORING.md
grep -q "CDK_FAILURE_MODES" README.md
```
