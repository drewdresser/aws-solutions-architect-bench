# Epic: Expand MCQ Dataset

## User Value

A larger, more comprehensive practice exam dataset provides statistically stable scores and covers the breadth of AWS SA domains, making the benchmark more representative of real certification prep.

## Success Criteria

- [x] MCQ set grown from 20 to at least 50 questions (achieved: 50 questions)
- [x] Questions tagged by AWS domain (compute, storage, networking, security, etc.) - 25 unique domains
- [x] Questions tagged by difficulty level (Associate vs Professional) - 25 each
- [x] Balanced coverage across core SA domains
- [x] Questions sourced from diverse scenarios (not repetitive patterns) - 76 unique AWS services

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

- [x] [001-create-generation-script](../tasks/expand-mcq-dataset-001-create-generation-script.md) — Create PEP723 script using OpenAI API to generate MCQ items
- [x] [002-expand-associate-questions](../tasks/expand-mcq-dataset-002-expand-associate-questions.md) — Generate 15 new SA Associate-level questions
- [x] [003-expand-pro-questions](../tasks/expand-mcq-dataset-003-expand-pro-questions.md) — Generate 15 new SA Professional-level questions
- [x] [004-add-aws-services-tags](../tasks/expand-mcq-dataset-004-add-aws-services-tags.md) — Add aws_services metadata tags to all questions
- [x] [005-review-and-validate](../tasks/expand-mcq-dataset-005-review-and-validate.md) — Review, validate, and finalize the dataset

## Status

`Done`
