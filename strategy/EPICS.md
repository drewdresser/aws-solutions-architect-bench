# Epics Overview

*Last updated: 2026-01-07 (expand-architecture-dataset completed)*

## Epic Summary

| Epic | OKR Alignment | Priority | Dependencies | Status |
|------|---------------|----------|--------------|--------|
| [scoring-and-aggregation-hardening.md](epics/scoring-and-aggregation-hardening.md) | O1/KR4 | High | None (foundational) | Done |
| [reproducibility-and-ci.md](epics/reproducibility-and-ci.md) | O1/KR1, O1/KR3 | High | scoring-and-aggregation-hardening | Done |
| [cdk-eval-reliability.md](epics/cdk-eval-reliability.md) | O2/KR4 | High | None | Done |
| [public-leaderboard-and-release.md](epics/public-leaderboard-and-release.md) | O1/KR2 | High | scoring-and-aggregation-hardening, reproducibility-and-ci | Done |
| [llm-judge-architecture-scoring.md](epics/llm-judge-architecture-scoring.md) | O2/KR1, O2/KR2 | High | None | Done |
| [structured-diagram-formats-and-validation.md](epics/structured-diagram-formats-and-validation.md) | O2/KR3 | Medium | llm-judge-architecture-scoring | Done |
| [expand-mcq-dataset.md](epics/expand-mcq-dataset.md) | O3/KR1 | Medium | None | Not Started |
| [expand-architecture-dataset.md](epics/expand-architecture-dataset.md) | O3/KR2 | Medium | structured-diagram-formats-and-validation | Done |
| [expand-cdk-dataset.md](epics/expand-cdk-dataset.md) | O3/KR3 | Low | cdk-eval-reliability | Not Started |
| [category-score-reporting.md](epics/category-score-reporting.md) | O3/KR4 | Medium | expand-mcq, expand-architecture, expand-cdk | Not Started |
| [launch-post-and-positioning.md](epics/launch-post-and-positioning.md) | O4/KR1 | Medium | public-leaderboard-and-release | Not Started |
| [credibility-and-distribution.md](epics/credibility-and-distribution.md) | O4/KR2 | Low | launch-post-and-positioning | Not Started |
| [contribution-workflow.md](epics/contribution-workflow.md) | O4/KR3 | Low | public-leaderboard-and-release | Not Started |
| [log-transparency-and-drilldown.md](epics/log-transparency-and-drilldown.md) | O1/KR2, O4 | Medium | public-leaderboard-and-release | Not Started |

---

## Recommended Work Order

```
Phase 1 (Foundation) - DONE:
  ├── scoring-and-aggregation-hardening ────┐
  └── reproducibility-and-ci ◄──────────────┘
                                            │
Phase 2 (Core Release & Scoring) - DONE:    │
  ├── cdk-eval-reliability ◄────────────────┤ (DONE)
  ├── public-leaderboard-and-release ◄──────┤ (DONE)
  └── llm-judge-architecture-scoring ◄──────┘ (DONE)
                                            │
Phase 3 (Scoring Improvements) - DONE:      │
  └── structured-diagram-formats ◄──────────┤ (DONE)
                                            │
Phase 4 (Dataset Expansion):                │
  ├── expand-mcq-dataset ◄──────────────────┤ (no blockers)
  ├── expand-architecture-dataset ◄─────────┤ (DONE)
  └── expand-cdk-dataset ◄──────────────────┤ (needs cdk-eval-reliability)
                                            │
Phase 5 (Reporting):                        │
  └── category-score-reporting ◄────────────┤ (needs all expand-*)
                                            │
Phase 6 (Launch & Growth):                  │
  ├── launch-post-and-positioning ◄─────────┤ (needs public-leaderboard)
  ├── credibility-and-distribution ◄────────┤ (needs launch-post)
  ├── contribution-workflow ◄───────────────┤ (needs public-leaderboard)
  └── log-transparency-and-drilldown ◄──────┘ (needs public-leaderboard)
```

### Phase Details

**Phase 1 — Foundation (DONE)**
- **scoring-and-aggregation-hardening**: Fixed weight normalization, added pytest infrastructure, documented scoring formula. All 6 tasks complete.
- **reproducibility-and-ci**: Added tests to CI, fixed static site, deployed GitHub Pages, documented quickstart and reproducibility tolerance. All 5 tasks complete.

**Phase 2 — Core Release & Scoring (DONE)**
- **cdk-eval-reliability**: DONE. All 5 tasks complete. Added local execution fallback for CI, improved code extraction (multiple patterns), added diagnostic logging, documented failure modes.
- **public-leaderboard-and-release**: DONE. All 5 tasks complete. Added timestamp metadata, enhanced UI with category highlighting and mobile support, expanded methodology section, created v0.1.0 release.
- **llm-judge-architecture-scoring**: DONE. All 5 tasks complete. Implemented LLM-as-judge scorer with rubrics for all subtypes, anti-gaming mechanisms (hidden criteria, length checks, blended scoring), calibration dataset with 12 samples, published documentation.

**Phase 3 — Scoring Improvements (DONE)**
- **structured-diagram-formats-and-validation**: DONE. All 5 tasks complete. Implemented Mermaid/PlantUML/JSON validators, created JSON schema for architectures, integrated validation into scorer with score modifiers, updated dataset items with format requirements, created comprehensive documentation.

**Phase 4 — Dataset Expansion** (can parallelize some)
- **expand-mcq-dataset**: Grow practice exam from ~20 to 50+ questions with domain tagging. No blockers.
- **expand-architecture-dataset**: DONE. All 5 tasks complete. Grew from 9 to 28 items with new architecture_critique subtype, 59 unique AWS services covered, all items tagged with aws_services and domains.
- **expand-cdk-dataset**: Grow from ~20 to 40+ prompts. Must wait for cdk-eval-reliability.

**Phase 5 — Reporting**
- **category-score-reporting**: Display per-category scores with definitions and variance estimates. Needs enough items in each category first.

**Phase 6 — Launch & Growth**
- **launch-post-and-positioning**: Public write-up explaining SA Bench methodology and value.
- **credibility-and-distribution**: Outreach for mentions/citations from practitioners and researchers.
- **contribution-workflow**: CONTRIBUTING.md, issue templates, and documentation for external contributors.
- **log-transparency-and-drilldown**: Click-to-view detailed evaluation logs from leaderboard. Uses Inspect's `inspect view bundle` for static HTML log viewer.

---

## Progress Summary

| Status | Count | Epics |
|--------|-------|-------|
| Done | 7 | scoring-and-aggregation-hardening, reproducibility-and-ci, cdk-eval-reliability, public-leaderboard-and-release, llm-judge-architecture-scoring, structured-diagram-formats-and-validation, expand-architecture-dataset |
| In Progress | 0 | — |
| Not Started | 7 | (all others) |

**Tasks Created**: 7 epics have tasks defined — all complete (37 total tasks)

**v0.1.0 Released!** [View on GitHub](https://github.com/drewdresser/aws-solutions-architect-bench/releases/tag/v0.1.0)

---

## What to Work on Next

Based on dependencies and priorities:

### Recommended: `expand-mcq-dataset`

**Why this epic?**
- Medium priority for O3/KR1 (Grow dataset)
- No blockers
- Grow practice exam from ~20 to 50+ questions
- Will help unblock category-score-reporting

**What it involves:**
- Add more practice exam questions across SA domains
- Tag questions by topic and difficulty (Associate/Pro)
- Ensure balanced coverage across AWS certification domains

**Epic file:** [expand-mcq-dataset.md](epics/expand-mcq-dataset.md)

---

### Alternative Options (can parallelize)

| Option | Priority | Notes |
|--------|----------|-------|
| **expand-mcq-dataset** | Medium | No blockers; grow from 20→50+ questions. |
| **expand-cdk-dataset** | Low | Now unblocked; grow from 20→40 prompts. |
| **launch-post-and-positioning** | Medium | Now unblocked (v0.1 released); public write-up about SA Bench. |
| **log-transparency-and-drilldown** | Medium | Now unblocked; add clickable detailed log viewer to leaderboard. |

---

## Risk Areas

- **CDK pass rate at 0%** — Local execution fallback added; needs validation in CI
- **Dataset expansion volume** — Growing from 20 to 50+ items across remaining tracks (MCQ, CDK) is significant effort
- **External adoption** — Getting credible mentions requires the benchmark to be genuinely useful

---

## Not Planned

| Idea | Reason |
|------|--------|
| Real AWS certification questions | Copyright concerns; must create original content |
| Live AWS deployments in eval | Cost and complexity; `cdk synth` validation sufficient |
| Multi-cloud expansion | Focus on AWS SA certification scope first |
