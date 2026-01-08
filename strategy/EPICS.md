# Epics Overview

*Last updated: 2026-01-07 (category-score-reporting completed)*

## Epic Summary

| Epic | OKR Alignment | Priority | Dependencies | Status |
|------|---------------|----------|--------------|--------|
| [scoring-and-aggregation-hardening.md](epics/scoring-and-aggregation-hardening.md) | O1/KR4 | High | None (foundational) | Done |
| [reproducibility-and-ci.md](epics/reproducibility-and-ci.md) | O1/KR1, O1/KR3 | High | scoring-and-aggregation-hardening | Done |
| [cdk-eval-reliability.md](epics/cdk-eval-reliability.md) | O2/KR4 | High | None | Done |
| [public-leaderboard-and-release.md](epics/public-leaderboard-and-release.md) | O1/KR2 | High | scoring-and-aggregation-hardening, reproducibility-and-ci | Done |
| [llm-judge-architecture-scoring.md](epics/llm-judge-architecture-scoring.md) | O2/KR1, O2/KR2 | High | None | Done |
| [structured-diagram-formats-and-validation.md](epics/structured-diagram-formats-and-validation.md) | O2/KR3 | Medium | llm-judge-architecture-scoring | Done |
| [expand-mcq-dataset.md](epics/expand-mcq-dataset.md) | O3/KR1 | Medium | None | Done |
| [expand-architecture-dataset.md](epics/expand-architecture-dataset.md) | O3/KR2 | Medium | structured-diagram-formats-and-validation | Done |
| [expand-cdk-dataset.md](epics/expand-cdk-dataset.md) | O3/KR3 | Low | cdk-eval-reliability | Done |
| [category-score-reporting.md](epics/category-score-reporting.md) | O3/KR4 | Medium | expand-mcq, expand-architecture, expand-cdk | Done |
| [launch-post-and-positioning.md](epics/launch-post-and-positioning.md) | O4/KR1 | Medium | public-leaderboard-and-release | Done |
| [credibility-and-distribution.md](epics/credibility-and-distribution.md) | O4/KR2 | Low | launch-post-and-positioning | Not Started |
| [contribution-workflow.md](epics/contribution-workflow.md) | O4/KR3 | Low | public-leaderboard-and-release | Not Started |
| [log-transparency-and-drilldown.md](epics/log-transparency-and-drilldown.md) | O1/KR2, O4 | Medium | public-leaderboard-and-release | Done |

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
Phase 4 (Dataset Expansion) - DONE:         │
  ├── expand-mcq-dataset ◄──────────────────┤ (DONE)
  ├── expand-architecture-dataset ◄─────────┤ (DONE)
  └── expand-cdk-dataset ◄──────────────────┤ (DONE)
                                            │
Phase 5 (Reporting) - DONE:                 │
  └── category-score-reporting ◄────────────┤ (DONE)
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

**Phase 4 — Dataset Expansion (DONE)**
- **expand-mcq-dataset**: DONE. All 5 tasks complete. Grew from 20 to 50 questions, 25 unique domains, 76 unique AWS services, balanced 25/25 Associate/Pro split, 30 single-select/20 multi-select.
- **expand-architecture-dataset**: DONE. All 5 tasks complete. Grew from 9 to 28 items with new architecture_critique subtype, 59 unique AWS services covered, all items tagged with aws_services and domains.
- **expand-cdk-dataset**: DONE. All 5 tasks complete. Grew from 20 to 40 prompts with 10 beginner, 17 intermediate, 13 advanced. 53 unique AWS services, 19 domain categories. Created prompt contract documentation.

**Phase 5 — Reporting (DONE)**
- **category-score-reporting**: DONE. All 4 tasks complete. Enhanced JSON schema with category metadata (name, description, weight, sample_count, confidence, margin). Added UI tooltips and weight badges on category headers. Updated SCORING.md with confidence methodology and JSON schema documentation.

**Phase 6 — Launch & Growth**
- **launch-post-and-positioning**: DONE. All 4 tasks complete. Created launch blog post (docs/LAUNCH_POST.md), added Open Graph/Twitter Card meta tags, polished README with badges and "What is SA Bench?" section, created social media posts for Twitter/X and LinkedIn.
- **credibility-and-distribution**: Outreach for mentions/citations from practitioners and researchers.
- **contribution-workflow**: CONTRIBUTING.md, issue templates, and documentation for external contributors.
- **log-transparency-and-drilldown**: DONE. All 4 tasks complete. Created log bundling script (scripts/bundle_logs.sh), added clickable model links to leaderboard, integrated log bundling into CI workflow, logs deployed to GitHub Pages at /logs/.

---

## Progress Summary

| Status | Count | Epics |
|--------|-------|-------|
| Done | 12 | scoring-and-aggregation-hardening, reproducibility-and-ci, cdk-eval-reliability, public-leaderboard-and-release, llm-judge-architecture-scoring, structured-diagram-formats-and-validation, expand-architecture-dataset, expand-mcq-dataset, launch-post-and-positioning, expand-cdk-dataset, log-transparency-and-drilldown, category-score-reporting |
| In Progress | 0 | — |
| Not Started | 2 | credibility-and-distribution, contribution-workflow |

**Tasks Created**: 12 epics have tasks defined (68 total tasks)

**v0.1.0 Released!** [View on GitHub](https://github.com/drewdresser/aws-solutions-architect-bench/releases/tag/v0.1.0)

---

## What to Work on Next

Based on dependencies and priorities:

### Up Next: `credibility-and-distribution`

**Status:** Not Started

**Description:** Outreach for mentions/citations from practitioners and researchers.

**Epic file:** [credibility-and-distribution.md](epics/credibility-and-distribution.md)

### Up Next: `contribution-workflow`

**Status:** Not Started

**Description:** CONTRIBUTING.md, issue templates, and documentation for external contributors.

**Epic file:** [contribution-workflow.md](epics/contribution-workflow.md)

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
