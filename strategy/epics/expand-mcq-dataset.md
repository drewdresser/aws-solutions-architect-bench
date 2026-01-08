# Epic: Expand MCQ Dataset

## User Value

A larger, more comprehensive practice exam dataset provides statistically stable scores and covers the breadth of AWS SA domains, making the benchmark more representative of real certification prep.

## Success Criteria

- [ ] MCQ set grown from 20 to at least 50 questions
- [ ] Questions tagged by AWS domain (compute, storage, networking, security, etc.)
- [ ] Questions tagged by difficulty level (Associate vs Professional)
- [ ] Balanced coverage across core SA domains
- [ ] Questions sourced from diverse scenarios (not repetitive patterns)

## Technical Approach

Add new questions to `evals/practice_exam/aws_sa.jsonl`. Implement tagging schema in JSONL format. Consider automated generation of questions from AWS documentation with manual curation. Ensure questions cover Well-Architected pillars and common SA scenarios.

## OKR Alignment

- **Objective**: O3 — Expand task coverage and stabilize category scores
- **Key Result**: KR1 — Grow Practice Exam set from ~20 to at least [N] questions

## Dependencies

- **Depends on**: None (can start independently)
- **Blocks**: category-score-reporting (need enough data for stable category scores)
- **Priority**: `Medium`

## Tasks

- [ ] [001-create-generation-script](../tasks/expand-mcq-dataset-001-create-generation-script.md) — Create PEP723 script using OpenAI API to generate MCQ items
- [ ] [002-expand-associate-questions](../tasks/expand-mcq-dataset-002-expand-associate-questions.md) — Generate 15 new SA Associate-level questions
- [ ] [003-expand-pro-questions](../tasks/expand-mcq-dataset-003-expand-pro-questions.md) — Generate 15 new SA Professional-level questions
- [ ] [004-add-aws-services-tags](../tasks/expand-mcq-dataset-004-add-aws-services-tags.md) — Add aws_services metadata tags to all questions
- [ ] [005-review-and-validate](../tasks/expand-mcq-dataset-005-review-and-validate.md) — Review, validate, and finalize the dataset

## Status

`In Progress`
