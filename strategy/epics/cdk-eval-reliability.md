# Epic: CDK Eval Reliability

## User Value

CDK synthesis evaluation produces accurate pass/fail results, reducing false negatives so that working CDK code is properly credited—making the CDK track useful and trustworthy.

## Success Criteria

- [ ] CDK pass rate improved from 0% to realistic baseline (investigate root cause)
- [ ] False negative rate documented and reduced
- [ ] Code extraction/parsing improved to handle common model output formats
- [ ] "Known failure modes" document published
- [ ] Clearer prompt constraints to reduce ambiguity in expected outputs

## Technical Approach

Diagnose why current CDK pass rate is 0% in leaderboard. Review `evals/cdk_synth/tasks.py` code extraction logic. Test against known-good CDK outputs to identify parsing issues. Add more robust code block extraction. Document edge cases and limitations.

## OKR Alignment

- **Objective**: O2 — Make scoring robust and aligned with SA Bench's long-term vision
- **Key Result**: KR4 — Diagnose low CDK pass rates and improve reliability

## Dependencies

- **Depends on**: None (can start independently)
- **Blocks**: expand-cdk-dataset (fix reliability before expanding)
- **Priority**: `High`

## Tasks

- [ ] [001-fix-missing-task-files](../tasks/cdk-eval-reliability-001-fix-missing-task-files.md)
- [ ] [002-diagnose-sandbox-in-ci](../tasks/cdk-eval-reliability-002-diagnose-sandbox-in-ci.md)
- [ ] [003-improve-code-extraction](../tasks/cdk-eval-reliability-003-improve-code-extraction.md)
- [ ] [004-add-local-execution-fallback](../tasks/cdk-eval-reliability-004-add-local-execution-fallback.md)
- [ ] [005-document-failure-modes](../tasks/cdk-eval-reliability-005-document-failure-modes.md)

## Status

`In Progress`
