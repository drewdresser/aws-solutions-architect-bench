# Epics Overview

*Last updated: 2026-01-06 (cdk-eval-reliability completed)*

## Epic Summary

| Epic | OKR Alignment | Priority | Dependencies | Status |
|------|---------------|----------|--------------|--------|
| [scoring-and-aggregation-hardening.md](epics/scoring-and-aggregation-hardening.md) | O1/KR4 | High | None (foundational) | Done |
| [reproducibility-and-ci.md](epics/reproducibility-and-ci.md) | O1/KR1, O1/KR3 | High | scoring-and-aggregation-hardening | Done |
| [cdk-eval-reliability.md](epics/cdk-eval-reliability.md) | O2/KR4 | High | None | Done |
| [public-leaderboard-and-release.md](epics/public-leaderboard-and-release.md) | O1/KR2 | High | scoring-and-aggregation-hardening, reproducibility-and-ci | Done |
| [llm-judge-architecture-scoring.md](epics/llm-judge-architecture-scoring.md) | O2/KR1, O2/KR2 | High | None | Not Started |
| [structured-diagram-formats-and-validation.md](epics/structured-diagram-formats-and-validation.md) | O2/KR3 | Medium | llm-judge-architecture-scoring | Not Started |
| [expand-mcq-dataset.md](epics/expand-mcq-dataset.md) | O3/KR1 | Medium | None | Not Started |
| [expand-architecture-dataset.md](epics/expand-architecture-dataset.md) | O3/KR2 | Medium | structured-diagram-formats-and-validation | Not Started |
| [expand-cdk-dataset.md](epics/expand-cdk-dataset.md) | O3/KR3 | Low | cdk-eval-reliability | Not Started |
| [category-score-reporting.md](epics/category-score-reporting.md) | O3/KR4 | Medium | expand-mcq, expand-architecture, expand-cdk | Not Started |
| [launch-post-and-positioning.md](epics/launch-post-and-positioning.md) | O4/KR1 | Medium | public-leaderboard-and-release | Not Started |
| [credibility-and-distribution.md](epics/credibility-and-distribution.md) | O4/KR2 | Low | launch-post-and-positioning | Not Started |
| [contribution-workflow.md](epics/contribution-workflow.md) | O4/KR3 | Low | public-leaderboard-and-release | Not Started |

---

## Recommended Work Order

```
Phase 1 (Foundation) - DONE:
  ├── scoring-and-aggregation-hardening ────┐
  └── reproducibility-and-ci ◄──────────────┘
                                            │
Phase 2 (Core Release & Scoring) - ACTIVE:  │
  ├── cdk-eval-reliability ◄────────────────┤ (DONE)
  ├── public-leaderboard-and-release ◄──────┤ (ready to start)
  └── llm-judge-architecture-scoring ◄──────┘ (can parallelize)
                                            │
Phase 3 (Scoring Improvements):             │
  └── structured-diagram-formats ◄──────────┤ (needs llm-judge)
                                            │
Phase 4 (Dataset Expansion):                │
  ├── expand-mcq-dataset ◄──────────────────┤ (no blockers)
  ├── expand-architecture-dataset ◄─────────┤ (needs structured-diagram)
  └── expand-cdk-dataset ◄──────────────────┤ (needs cdk-eval-reliability)
                                            │
Phase 5 (Reporting):                        │
  └── category-score-reporting ◄────────────┤ (needs all expand-*)
                                            │
Phase 6 (Launch & Growth):                  │
  ├── launch-post-and-positioning ◄─────────┤ (needs public-leaderboard)
  ├── credibility-and-distribution ◄────────┤ (needs launch-post)
  └── contribution-workflow ◄───────────────┘ (needs public-leaderboard)
```

### Phase Details

**Phase 1 — Foundation (DONE)**
- **scoring-and-aggregation-hardening**: Fixed weight normalization, added pytest infrastructure, documented scoring formula. All 6 tasks complete.
- **reproducibility-and-ci**: Added tests to CI, fixed static site, deployed GitHub Pages, documented quickstart and reproducibility tolerance. All 5 tasks complete.

**Phase 2 — Core Release & Scoring (ACTIVE)**
- **cdk-eval-reliability**: DONE. All 5 tasks complete. Added local execution fallback for CI, improved code extraction (multiple patterns), added diagnostic logging, documented failure modes.
- **public-leaderboard-and-release**: Ready to start. Host leaderboard publicly with stable URL and methodology docs. Tasks not yet created.
- **llm-judge-architecture-scoring**: Can start independently. Implement LLM-as-judge for architecture track with rubrics and anti-gaming. Tasks not yet created.

**Phase 3 — Scoring Improvements**
- **structured-diagram-formats-and-validation**: Standardize output formats (Mermaid/PlantUML/JSON) and add structural validation. Depends on llm-judge epic being underway.

**Phase 4 — Dataset Expansion** (can parallelize some)
- **expand-mcq-dataset**: Grow practice exam from ~20 to 50+ questions with domain tagging. No blockers.
- **expand-architecture-dataset**: Grow from ~8 to 20+ items. Should wait for structured-diagram-formats.
- **expand-cdk-dataset**: Grow from ~20 to 40+ prompts. Must wait for cdk-eval-reliability.

**Phase 5 — Reporting**
- **category-score-reporting**: Display per-category scores with definitions and variance estimates. Needs enough items in each category first.

**Phase 6 — Launch & Growth**
- **launch-post-and-positioning**: Public write-up explaining SA Bench methodology and value.
- **credibility-and-distribution**: Outreach for mentions/citations from practitioners and researchers.
- **contribution-workflow**: CONTRIBUTING.md, issue templates, and documentation for external contributors.

---

## Progress Summary

| Status | Count | Epics |
|--------|-------|-------|
| Done | 4 | scoring-and-aggregation-hardening, reproducibility-and-ci, cdk-eval-reliability, public-leaderboard-and-release |
| In Progress | 0 | — |
| Not Started | 9 | (all others) |

**Tasks Created**: 4 epics have tasks defined — all complete (22 total tasks)

**v0.1.0 Released!** [View on GitHub](https://github.com/drewdresser/aws-solutions-architect-bench/releases/tag/v0.1.0)

---

## What to Work on Next

Based on dependencies and priorities:

### Recommended: `llm-judge-architecture-scoring`

**Why this epic?**
- High priority for O2 (Make scoring robust)
- No dependencies — can start immediately
- Improves architecture scoring beyond keyword heuristics
- Enables anti-gaming mechanisms for more credible evaluation

**What it involves:**
- Implement LLM-as-judge scoring for architecture tasks
- Create published rubrics and judge prompts
- Add anti-gaming mechanisms (hidden test points, multi-judge consistency)
- Establish scorer quality checks

**Epic file:** [llm-judge-architecture-scoring.md](epics/llm-judge-architecture-scoring.md)

---

### Alternative Options (can parallelize)

| Option | Priority | Notes |
|--------|----------|-------|
| **expand-cdk-dataset** | Low | Now unblocked; grow from 20→40 prompts. |
| **expand-mcq-dataset** | Medium | No blockers; grow from 20→50+ questions. |
| **launch-post-and-positioning** | Medium | Now unblocked (v0.1 released); public write-up about SA Bench. |

---

## Risk Areas

- **CDK pass rate at 0%** — Root cause not yet diagnosed; may require significant rework
- **LLM-as-judge reliability** — Judge agreement and anti-gaming mechanisms need careful design
- **Dataset expansion volume** — Growing from 20 to 50+ items across tracks is significant effort
- **External adoption** — Getting credible mentions requires the benchmark to be genuinely useful

---

## Not Planned

| Idea | Reason |
|------|--------|
| Real AWS certification questions | Copyright concerns; must create original content |
| Live AWS deployments in eval | Cost and complexity; `cdk synth` validation sufficient |
| Multi-cloud expansion | Focus on AWS SA certification scope first |
