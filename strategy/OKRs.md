# OKRs — Q1 2026 (Jan–Mar 2026)

## Objective 1 — Ship SA Bench v0.1 as a credible, reproducible public benchmark
**Intent:** Make it easy for others to run, trust, and cite SA Bench.

### Key Results
- KR1: Publish a public benchmark release (v0.1) with a “one-command run” path (e.g., Makefile + documented env setup) that produces the same leaderboard outputs on a fresh machine within a defined tolerance (e.g., ±X%).
- KR2: Host the leaderboard publicly (e.g., GitHub Pages) with a stable URL and clear “how scores are computed” documentation.
- KR3: Add CI automation for repeatable runs (nightly or scheduled) that generates `leaderboard.json` and updates the hosted leaderboard artifact.
- KR4: Fix benchmark aggregation correctness (weights sum to 1.0; per-category scores consistent; overall score definition documented and enforced by tests).

**Epics (planned):**
- public-leaderboard-and-release
- reproducibility-and-ci
- scoring-and-aggregation-hardening


## Objective 2 — Make scoring robust and aligned with SA Bench’s long-term vision
**Intent:** Move architecture evaluation beyond keyword heuristics and reduce opportunities for gaming.

### Key Results
- KR1: Implement an LLM-as-judge scoring path for architecture tasks with a published rubric and judge prompt(s), including at least one anti-gaming mechanism (e.g., hidden test points, schema validation, multi-judge self-consistency, or adversarial formatting checks).
- KR2: Establish scorer quality checks for the architecture track (e.g., judge agreement rate >= [target]% on a small sanity set, or correlation with deterministic checks where applicable).
- KR3: Standardize output formats where possible (Mermaid/PlantUML/JSON) for diagram generation and add automatic structural validation (parseable + required nodes/edges present).
- KR4: For CDK synth, diagnose low pass rates and improve reliability of the evaluation (e.g., reduce false negatives, improve extraction/parsing, add clearer constraints); publish a short “known failure modes” doc.

**Epics (planned):**
- llm-judge-architecture-scoring
- structured-diagram-formats-and-validation
- cdk-eval-reliability


## Objective 3 — Expand task coverage and stabilize category scores
**Intent:** Reduce variance and make category scores meaningful and comparable over time.

### Key Results
- KR1: Grow the Practice Exam (MCQ) set from ~20 to at least [N] questions spanning core SA domains; tag items by topic + difficulty (Associate/Pro).
- KR2: Grow Architecture track from ~8 to at least [N] items, balanced across:
  - diagram understanding
  - diagram generation
  - (optional) architecture critique / tradeoff analysis (if it fits the same scoring approach)
- KR3: Grow CDK track from ~20 to at least [N] prompts, with tagging by domain (networking/serverless/security/data/etc.) and a documented “prompt contract” to reduce ambiguity.
- KR4: Publish category-level score reporting as first-class output (per-category score, confidence notes/variance estimates if feasible, and a clear definition of what each category measures).

**Epics (planned):**
- expand-mcq-dataset
- expand-architecture-dataset
- expand-cdk-dataset
- category-score-reporting


## Objective 4 — Earn credible public attention for the leaderboard
**Intent:** Make SA Bench cite-worthy among high-credibility audiences.

### Key Results
- KR1: Launch a public write-up explaining what SA Bench measures, why it exists, and how to interpret scores; include examples of tasks and failure cases.
- KR2: Achieve at least [N] credible mentions/citations of the leaderboard (e.g., respected practitioners/researchers, major community accounts, or labs referencing results).
- KR3: Get at least [N] external contributors or PRs (new tasks, scorer improvements, documentation fixes), showing the project is usable and not just a personal repo.

**Epics (planned):**
- launch-post-and-positioning
- credibility-and-distribution
- contribution-workflow
