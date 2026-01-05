# Vision

## North Star

Make Solutions Architect capability measurable, reproducible, and comparable across LLMs.

## Vision (12-24 months)

In 12–24 months, **SA Bench** is the widely-cited, AWS-focused benchmark for evaluating LLMs on Solutions Architect tasks, with:

* A **public, reproducible evaluation harness** that runs against multiple models and produces stable scores
* A **visible leaderboard** that credible people reference when discussing “which model is best at SA work”
* A curated suite of **AWS-only SA tasks** spanning multiple output types, including:
  * AWS service selection and “when to use X vs Y” decisions
  * Well-Architected-style reviews and tradeoff analysis
  * Architecture diagram understanding and generation (using structured, scorable formats where possible)
  * (Optional track) infrastructure-as-code tasks like **CDK**, if it stays meaningfully differentiating
* **Task-appropriate grading**:
  * Some tasks scored **automatically** (structure checks, exact matches, rubric parsing, constraint validation)
  * Some tasks scored via **LLM-as-judge** with transparent rubrics and anti-gaming measures
  * **No human judging** as a dependency for core scoring
* Clear documentation and examples so the benchmark is easy to **run, reproduce, and talk about publicly**—supporting your core narrative: how AI is reshaping the Solutions Architect role.

## Mission
- Build an AWS-focused benchmark suite that measures LLM performance on real Solutions Architect work across models, agents, and tools/workflows.
- Provide a reproducible evaluation harness and a public, credible leaderboard with category-level scores that make strengths and gaps legible.
- Support public understanding of how AI is changing the Solutions Architect role by making SA capability measurable, comparable, and discussable.

## Strategic Bets

1. **AWS-only focus beats breadth.** Keeping SA Bench AWS-specific reduces ambiguity, enables tighter rubrics, and accelerates credibility and adoption.
2. **Structured outputs make architecture scorable.** Diagram-heavy and architectural tasks can be evaluated reliably by using constrained representations (e.g., Mermaid/PlantUML/JSON schemas) plus deterministic checks where possible.
3. **LLM-as-judge can be dependable with the right constraints.** With fixed rubrics, consistency checks, and anti-gaming design, model-based grading can cover subjective SA reasoning without requiring human judges for core scoring.
4. **Category scores are more useful than a single number.** Breaking results into capability slices (diagram understanding/generation, CDK, exam Q&A, etc.) better reflects real SA work and makes the leaderboard more actionable and talkable.
5. **A strong public narrative creates pull.** A clear leaderboard plus the story of “SA work is changing” will attract citations, discussion, and eventual adoption by credible voices and potentially labs.

## Non-Goals

* **Not an arena or head-to-head chat competition** (no subjective battles, no live preference voting).
* **Not a roleplay / simulation benchmark** (no “act as an SA in a meeting” evaluations).
* **Not multi-cloud (v1)** — SA Bench is **AWS-only** for now.
* **Not dependent on human graders** for core scoring and leaderboard updates.
* **Not measuring writing style** (verbosity, tone, persuasion) except where it directly affects correctness/completeness.
* **Not limited to purely applied architecture scenarios** — SA Bench may include **general cloud knowledge testing** through AWS certification-style questions and answers.

## Success Metrics

- Leaderboard adoption/credibility: achieve at least [N] publicly visible citations/mentions of the SA Bench leaderboard by credible practitioners/researchers within [time window] of launch.
- Reproducibility: a fresh user can run the harness and reproduce leaderboard scores within a defined tolerance (e.g., ±[X]%) using documented settings.
- Coverage: v1 ships with 4 category tracks (diagram understanding, diagram generation, CDK, exam Q&A) and each category has enough tasks to be stable (not overly sensitive to a single item).
- Usage: reach [N] eval runs and/or [N] forks and/or [N] contributors indicating the benchmark is being used, not just read.
