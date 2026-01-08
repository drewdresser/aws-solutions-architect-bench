# SA Bench: Measuring AI on Solutions Architect Work

*Can AI pass the AWS Solutions Architect exam? More importantly, can it actually do the job?*

## The Problem

Large language models are increasingly being used for cloud architecture work. Engineers ask Claude to design VPC topologies. Teams use ChatGPT to draft CDK infrastructure. Architects consult AI for cost optimization strategies.

But how good are these models, really?

Until now, we've relied on anecdotes: "It hallucinated a non-existent service," or "It nailed the DR strategy." These stories are interesting, but they don't help us make informed decisions about which models to use for which tasks—or whether to use them at all.

**SA Bench changes that.** It's an open-source benchmark that evaluates LLMs on real AWS Solutions Architect tasks across three dimensions: certification knowledge, architectural reasoning, and infrastructure code generation.

## What SA Bench Measures

### Practice Exam (34% of overall score)

AWS certification-style multiple choice questions testing service selection, best practices, and architectural decision-making.

**Example Task:**
> A company runs a public-facing three-tier web application in a VPC across multiple Availability Zones. Amazon EC2 instances for the application tier running in private subnets need to download software patches from the internet. However, the EC2 instances cannot be directly accessible from the internet. Which actions should be taken to allow the EC2 instances to download the needed patches? (Select TWO.)

The dataset includes 50 questions spanning 25 AWS domains—from networking and security to disaster recovery and ML/AI—balanced across Associate and Professional difficulty levels.

**Why it matters:** Certification knowledge is foundational. If a model can't answer these questions correctly, it probably shouldn't be architecting production systems.

### Architecture Design (33% of overall score)

Tasks that require analyzing or designing AWS architectures. This category tests reasoning, not just recall.

**Interpretation tasks** present the model with an architecture diagram and ask it to:
- Identify services and explain their roles
- Trace data flows through the system
- Assess security posture and suggest improvements
- Analyze scalability characteristics
- Identify cost optimization opportunities

**Creation tasks** give requirements and ask the model to design a solution:
- Translate business requirements into architecture
- Implement specific patterns (CQRS, Saga, event-driven)
- Design migration strategies

**Example Task:**
> Analyze the given architecture diagram which includes Amazon EKS with Karpenter for auto-scaling, AWS App Mesh for service mesh, Amazon RDS, and Amazon CloudFront. Identify the scaling mechanisms present, potential bottlenecks, and the benefits of the scalability features implemented.

The dataset contains 28 items across 9 subtypes, covering beginner through advanced scenarios with 59 unique AWS services.

**Why it matters:** Real SA work isn't multiple choice. It requires understanding complex systems, identifying issues that aren't obvious, and reasoning about tradeoffs.

We score these tasks using an LLM-as-judge approach. A judge model evaluates responses across accuracy (did they get it right?), completeness (did they cover everything?), and quality (is the reasoning sound?). See the methodology section below for details.

### CDK Synthesis (33% of overall score)

Generate AWS CDK Python code that actually works—that is, code that `cdk synth` successfully compiles into CloudFormation.

**Example Task:**
> Write an AWS CDK Python app that creates a private VPC with two isolated subnets and an S3 Gateway Endpoint. Use AWS CDK v2 (aws-cdk-lib). Emit a complete CDK app that can be synthesized.

**Why it matters:** Infrastructure-as-code is how modern teams deploy to AWS. A model that can reason about architecture but can't write valid CDK has limited practical value.

The evaluation is strict: we run `cdk synth` on the generated code. If it produces valid CloudFormation, the model passes. If it throws any error—import failure, syntax error, invalid construct—the model fails. No partial credit.

This binary scoring is intentional. In the real world, CDK code either works or it doesn't. A "90% correct" CDK stack still won't deploy.

## Methodology

### Scoring

Each category produces a score from 0.0 to 1.0:
- **Practice Exam**: Binary (correct/incorrect)
- **Architecture Design**: LLM-as-judge scoring across accuracy, completeness, and quality
- **CDK Synthesis**: Binary (`cdk synth` succeeds or fails)

The overall score is a weighted average: `(practice_exam × 0.34) + (architecture_design × 0.33) + (cdk_synth × 0.33)`.

### LLM-as-Judge for Architecture

Multiple choice questions are easy to score—the answer is right or wrong. Architecture tasks are harder. "Good" architecture involves tradeoffs, and reasonable people disagree on specifics.

We use an LLM judge with detailed rubrics for each task subtype. The judge evaluates responses across three dimensions (accuracy, completeness, quality), guided by explicit scoring criteria and expected elements from the dataset.

To prevent gaming, we combine the judge's assessment (70%) with deterministic keyword checks (30%), and apply penalties for suspiciously short or repetitive responses.

### Structured Output Validation

For architecture creation tasks, we validate that models produce properly structured diagrams. We support Mermaid flowcharts, PlantUML component diagrams, and JSON architecture specifications—checking syntax, required elements, and structural validity.

## Current Results

| Model | Practice Exam | Architecture | CDK | Overall |
|-------|---------------|--------------|-----|---------|
| Claude Sonnet 4 | 95% | — | 5% | 41% |
| Claude Opus 4 | 85% | — | 0% | 34% |
| OpenAI o3 | 80% | — | 0% | 32% |
| GPT-4.1 | 60% | — | 7.5% | 29% |
| Grok 3 Mini | 65% | — | 0% | 26% |

*Note: Architecture scores are still being calibrated and are not yet included in overall scoring.*

### What the Data Shows

**1. Certification knowledge doesn't predict coding ability.**

Claude Sonnet 4 scores 95% on practice exams but only 5% on CDK synthesis. The gap between "knowing the answer" and "writing working code" is enormous.

**2. CDK is hard for everyone.**

No model exceeds 10% on CDK synthesis. The challenge isn't just knowing what to build—it's producing syntactically correct, importable, synthesizable Python code with the right CDK constructs.

**3. Exam performance varies widely.**

The top model (Sonnet 4 at 95%) outperforms the bottom (GPT-4.1 at 60%) by 35 percentage points on the same questions. Model choice matters for knowledge tasks.

## What Models Get Wrong

### Practice Exam Failures

Models typically fail MCQs through plausible-but-incorrect reasoning:

> **Question:** Which service provides managed DDoS protection?
>
> **Wrong answer (common):** "AWS WAF provides DDoS protection by filtering malicious traffic at the application layer."
>
> **Why it's wrong:** WAF handles application-layer attacks (SQL injection, XSS). AWS Shield is the dedicated DDoS protection service.

The issue isn't random guessing—it's confident reasoning that leads to the wrong conclusion.

### Architecture Failures

Common failure modes in architecture tasks:

- **Missing security considerations**: Designs without encryption, IAM, or network isolation
- **Ignoring the question**: Providing a generic architecture instead of addressing specific requirements
- **Incomplete tradeoff analysis**: Stating a recommendation without explaining why or what's sacrificed

### CDK Failures

CDK tasks fail for several reasons:

1. **Import errors**: Wrong module paths, missing imports, nonexistent constructs
2. **Syntax errors**: Invalid Python that won't parse
3. **CDK errors**: Valid Python that CDK can't synthesize (wrong props, missing required fields)
4. **Extraction failures**: Code buried in explanation that we can't reliably extract

**Example of a common failure:**

```python
# Model generates this:
from aws_cdk import aws_s3 as s3
bucket = s3.Bucket(self, "MyBucket", versioned=True)

# But forgets the App and Stack boilerplate:
# app = App()
# stack = Stack(app, "MyStack")
# app.synth()
```

The model understands S3 buckets. It even uses correct CDK construct properties. But without the App/Stack scaffolding, `cdk synth` fails. This pattern—correct fragments in an incomplete structure—is the most common failure mode.

## Limitations

**Dataset size**: 50 MCQs, 28 architecture items, and ~20 CDK prompts. We're expanding, but scores have higher variance than a 1000-item benchmark would.

**CDK reliability**: The CDK evaluation pipeline is sensitive to extraction issues and environment configuration. A 0% score sometimes reflects evaluation bugs, not model capability.

**Architecture calibration**: LLM judges are imperfect. We've calibrated against human scores, but there's inherent variance in evaluating open-ended responses.

**Model access**: We evaluate through OpenRouter, which means we're testing whatever model versions are deployed there—not necessarily the latest.

## Running SA Bench Yourself

```bash
git clone https://github.com/drewdresser/aws-solutions-architect-bench
cd aws-solutions-architect-bench
uv sync
cp .env.example .env  # Add your OPENROUTER_API_KEY
make bench && make board.json
```

Requirements: Python 3.12+, Docker (for CDK), [uv](https://docs.astral.sh/uv/), OpenRouter API key.

Full documentation: [GitHub Repository](https://github.com/drewdresser/aws-solutions-architect-bench)

## The Bigger Picture

AI is changing how Solutions Architect work gets done. That's not speculation—it's happening now, in companies of all sizes.

SA Bench doesn't answer whether AI *should* do this work. It answers *how well* different models perform on specific tasks, with reproducible measurements.

Some findings are encouraging (95% on certification questions). Others are sobering (5% on CDK). Both are useful to know.

If you're evaluating AI tools for your architecture team, these benchmarks give you a starting point. If you're building AI-assisted architecture tools, they give you targets to beat.

And if you're an AI model, well—you've got some CDK homework to do.

---

**Live Leaderboard**: [drewdresser.github.io/aws-solutions-architect-bench](https://drewdresser.github.io/aws-solutions-architect-bench/)

**GitHub**: [github.com/drewdresser/aws-solutions-architect-bench](https://github.com/drewdresser/aws-solutions-architect-bench)

**Methodology Details**: [Scoring Documentation](https://github.com/drewdresser/aws-solutions-architect-bench/blob/main/docs/SCORING.md)

---

*SA Bench is an open-source project. Contributions welcome—especially new evaluation tasks, dataset expansions, and scoring improvements.*
