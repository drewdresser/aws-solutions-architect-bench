# SA Bench Social Media Launch Posts

Ready-to-post content for launching SA Bench on social media.

---

## Twitter/X Posts

### Launch Announcement

```
Introducing SA Bench: measuring AI on AWS Solutions Architect work

We evaluated LLMs across:
- Certification-style practice exams
- Architecture diagram analysis
- CDK infrastructure code generation

Surprising finding: 95% on exams, 5% on CDK. Knowledge != implementation.

Live leaderboard: https://drewdresser.github.io/aws-solutions-architect-bench/
```

### Interesting Finding

```
Can AI pass the AWS Solutions Architect exam?

Claude Sonnet 4: 95%
GPT-4.1: 60%
Grok 3 Mini: 65%

But ask them to write CDK code that actually compiles? Everyone scores under 10%.

The gap between "knowing the answer" and "doing the work" is huge.

https://drewdresser.github.io/aws-solutions-architect-bench/
```

### Question Hook

```
If you're using AI for AWS architecture work, do you know how it actually performs?

SA Bench measures LLMs on real SA tasks:
- Multiple choice certification questions
- Architecture design & analysis
- Infrastructure-as-code generation

Results might surprise you.

https://drewdresser.github.io/aws-solutions-architect-bench/
```

### Methodology Highlight

```
How do you score an architecture design? It's not multiple choice.

SA Bench uses LLM-as-judge with transparent rubrics:
- Accuracy: Did they get it right?
- Completeness: Did they cover everything?
- Quality: Is the reasoning sound?

Plus anti-gaming measures to prevent shortcuts.

Details: https://github.com/drewdresser/aws-solutions-architect-bench/blob/main/docs/ARCHITECTURE_SCORING.md
```

### Call to Action

```
Run SA Bench on your favorite AI model:

git clone github.com/drewdresser/aws-solutions-architect-bench
uv sync
make bench

Compare against the leaderboard. Contribute new tasks. See how your model stacks up.

All open source: https://github.com/drewdresser/aws-solutions-architect-bench
```

---

## LinkedIn Posts

### Main Launch Post

```
I've been curious about how well AI models actually perform at Solutions Architect work - not just chat, but real technical tasks.

So I built SA Bench, an open-source benchmark that evaluates LLMs on:

- AWS certification-style practice exams (50 questions across 25 domains)
- Architecture diagram analysis and design (28 tasks testing reasoning, not recall)
- CDK infrastructure-as-code generation (code that must actually compile)

Early results show interesting patterns:

Claude Sonnet 4 leads overall at 41%, scoring 95% on practice exams but only 5% on CDK synthesis. The gap between "knowing the answer" and "writing working code" is enormous.

No model exceeds 10% on CDK. Generating syntactically correct, synthesizable CDK code is genuinely hard for current LLMs.

The methodology uses LLM-as-judge for architecture tasks with transparent rubrics and anti-gaming measures. Full scoring documentation is public.

Live leaderboard and methodology: https://drewdresser.github.io/aws-solutions-architect-bench/

GitHub (run it yourself, contribute tasks): https://github.com/drewdresser/aws-solutions-architect-bench

Would love feedback from the SA community. What tasks should we add? What are you seeing in practice?

#AWS #AI #SolutionsArchitect #CloudArchitecture #LLM
```

### Technical Deep Dive Post

```
How do you measure AI performance on open-ended architecture work?

Multiple choice is easy - the answer is right or wrong. But architecture tasks involve tradeoffs, and reasonable people disagree on specifics.

For SA Bench, we built an LLM-as-judge scoring system:

1. Detailed rubrics for each task type (service identification, data flow analysis, security assessment, etc.)

2. Three evaluation dimensions:
   - Accuracy: Does it match expected answers?
   - Completeness: Are all elements covered?
   - Quality: Is reasoning sound and professional?

3. Anti-gaming measures:
   - Blended scoring (70% judge + 30% deterministic checks)
   - Penalties for suspiciously short or repetitive responses
   - Hidden criteria not in public documentation

4. Calibration against human-scored responses (80%+ agreement target)

The result: nuanced evaluation that captures quality differences without being gameable.

Full methodology: https://github.com/drewdresser/aws-solutions-architect-bench/blob/main/docs/ARCHITECTURE_SCORING.md

The broader question: as AI becomes more capable, how do we measure what matters for professional work?

#AIEvaluation #MachineLearning #SoftwareEngineering
```

---

## Notes

- Twitter posts are within 280 character limit (including link expansion)
- LinkedIn posts designed to avoid truncation on first 3 lines
- All posts link to leaderboard as primary CTA
- Avoid overly promotional language - focus on findings and methodology
- Consider timing: post during business hours for cloud practitioner audience
