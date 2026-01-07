# CDK Synthesis Evaluation: Known Failure Modes

This document describes known limitations and failure modes in the CDK synthesis evaluation track. Understanding these helps interpret CDK scores correctly.

## Overview

The CDK track evaluates a model's ability to generate valid AWS CDK Python code that successfully synthesizes to CloudFormation. Scores reflect:
- Code extraction success (can we parse the model's output?)
- Synthesis success (does `cdk synth` pass?)
- Optional: CloudFormation linting (does cfn-lint find issues?)

A 0% score may indicate **evaluation infrastructure failure** rather than model capability. Always check logs for extraction or sandbox errors.

## Code Extraction Failures

### Missing Code Blocks

**Problem:** Models sometimes provide code inline without fencing.

**Example (fails extraction):**
```
The CDK code is:
from aws_cdk import App
app = App()
```

**Example (passes extraction):**
````
```python
from aws_cdk import App
app = App()
```
````

**Mitigation:** Prompts explicitly request `python` code blocks. If issues persist, the fallback extractor attempts to use the raw text.

### Multiple Code Blocks

**Problem:** Some models split code across multiple blocks (setup, then implementation).

**Example:**
````
First, import the libraries:
```python
from aws_cdk import App
```

Then create the stack:
```python
class MyStack(Stack):
    pass
```
````

**Behavior:** Extraction takes the **largest** code block, assuming it's the complete implementation.

**Mitigation:** Prompts request complete code in a single block.

### Unsupported Language Tags

**Problem:** Models may use non-standard language tags.

**Supported tags:**
- `python` (primary)
- `py` (alternative)
- `Python` (capitalized, case-insensitive)
- Untagged ` ``` ` blocks (fallback)

**Not supported:**
- `python3`
- `cdk`
- Other variants

## Synthesis Failures

### Missing Imports

**Problem:** Models often forget required imports.

**Common missing imports:**
```python
from aws_cdk import App, Stack  # Often missing
from constructs import Construct  # Required for CDK v2
```

**Example error:**
```
NameError: name 'Stack' is not defined
```

**Mitigation:** Prompts specify CDK v2 and list required imports.

### Invalid Construct Usage

**Problem:** Models may use deprecated, renamed, or non-existent constructs.

**Example issues:**
- Using `core.Construct` instead of `constructs.Construct` (CDK v1 vs v2)
- Missing required properties on constructs
- Using props that don't exist

**Example error:**
```
TypeError: __init__() got an unexpected keyword argument 'bucket_name'
```

### Missing App/Synth Call

**Problem:** Code that defines stacks but doesn't synthesize them.

**Incomplete (fails):**
```python
class MyStack(Stack):
    pass
```

**Complete (passes):**
```python
app = App()
MyStack(app, "MyStack")
app.synth()
```

### Python Syntax Errors

**Problem:** Generated code has syntax errors.

**Common issues:**
- Unclosed parentheses/brackets
- Invalid indentation
- Mixing Python 2/3 syntax

## Environment Failures

### Docker Sandbox Issues (Original Scorer)

**Problem:** In CI environments, Docker sandbox may fail to start.

**Symptoms:**
- 0% pass rate on all items
- Timeout errors
- "sandbox error" in explanations

**Cause:** Docker-in-Docker issues in GitHub Actions runners.

**Solution:** Use `aws_cdk_synth_local` task which uses subprocess instead of Docker.

### Local Execution Setup

**Problem:** Local scorer requires CDK CLI to be installed.

**Requirements:**
```bash
# Install Node.js 18+
npm install -g aws-cdk

# Verify installation
cdk --version
```

**Error if missing:**
```
cdk command not found - install with: npm install -g aws-cdk
```

### Timeout Issues

**Problem:** Complex CDK stacks may exceed 60-second timeout.

**Symptoms:**
- "cdk synth timed-out" in explanation
- Usually affects stacks with many resources

**Mitigation:** Prompts request simple, focused stacks.

## Prompt Ambiguity

### Underspecified Requirements

**Problem:** Vague prompts lead to valid but unverifiable code.

**Ambiguous (many valid approaches):**
> "Create an S3 bucket"

**Specific (verifiable):**
> "Create an S3 bucket with versioning enabled and a DESTROY removal policy"

### Missing Context

**Problem:** Prompts don't specify CDK version or construct library versions.

**Mitigation:** All prompts specify "AWS CDK v2" and "Python".

## How to Interpret CDK Scores

### Score Meaning

| Score | Interpretation |
|-------|----------------|
| 0% | Either all code failed OR evaluation infrastructure issue |
| 1-30% | Likely extraction or basic syntax issues |
| 30-70% | Mix of passing and failing; check specific failures |
| 70-100% | Strong CDK capability |

### Debugging Low Scores

1. **Check logs for patterns:**
   - "No code block found" → Extraction failure
   - "sandbox error" → Docker issue, use local mode
   - "cdk command not found" → Missing CDK CLI
   - Specific Python errors → Model code quality issue

2. **Run single items:**
   ```bash
   make eval.cdk LIMIT=1
   ```

3. **Inspect model output:**
   Check if the model's response contains valid, complete CDK code.

### Known Limitations

- **Binary scoring:** Pass/fail only; no partial credit for "almost correct" code
- **No runtime validation:** Code must synth, but we don't deploy it
- **Single-file only:** Multi-file CDK projects not supported
- **No external dependencies:** Can't test code requiring npm packages beyond aws-cdk-lib

## Changelog

- **2026-01-06:** Initial documentation of failure modes
- **2026-01-06:** Added local execution mode to address Docker sandbox issues
- **2026-01-06:** Improved code extraction to handle multiple patterns
