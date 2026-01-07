# Task: Improve Code Extraction Robustness

**Epic:** [cdk-eval-reliability.md](../epics/cdk-eval-reliability.md)
**Size:** `M`
**Status:** `Done`

## Context

The `_extract_code()` function uses a simple regex to extract Python code from model output. Different models format code blocks differently, leading to extraction failures that cause false negatives.

## Acceptance Criteria

- [ ] Code extraction handles multiple code block formats (```python, ```py, ```, no fence)
- [ ] Extraction logs what it found/attempted for debugging
- [ ] Unit tests cover common model output patterns
- [ ] False negative rate documented with examples

## Technical Notes

**Relevant Files:**
- `evals/cdk_synth/tasks.py` — `_extract_code()` function at line 18-24

**Current implementation:**
```python
CODE_RE = re.compile(r"```python\n(.*?)```", re.DOTALL | re.IGNORECASE)

def _extract_code(raw: str) -> str:
    if m := CODE_RE.search(raw):
        return textwrap.dedent(m.group(1))
    # fallback: remove ANSWER: lines
    cleaned = re.sub(r"^ANSWER:.*$", "", raw, flags=re.IGNORECASE | re.MULTILINE)
    return textwrap.dedent(cleaned).strip()
```

**Issues:**
1. Only matches `python` language tag, not `py` or untagged blocks
2. Doesn't handle multiple code blocks (should it take first? last? largest?)
3. Fallback is too aggressive (returns entire response minus ANSWER lines)
4. No logging to diagnose extraction failures

**Patterns to handle:**
- ` ```python\n...\n``` ` (current)
- ` ```py\n...\n``` ` (common alternative)
- ` ```\n...\n``` ` (untagged)
- ` ```Python\n...\n``` ` (capitalized - IGNORECASE handles this)
- Multiple blocks (model explains then provides code)
- No code blocks at all (model inline code)

**Improved implementation sketch:**
```python
def _extract_code(raw: str) -> str:
    # Try multiple patterns in order of specificity
    patterns = [
        r"```python\n(.*?)```",
        r"```py\n(.*?)```",
        r"```\n(.*?)```",
    ]
    for pattern in patterns:
        if m := re.search(pattern, raw, re.DOTALL | re.IGNORECASE):
            code = textwrap.dedent(m.group(1))
            logger.debug(f"Extracted code via pattern: {pattern[:20]}...")
            return code

    # Fallback with warning
    logger.warning("No code block found, using fallback extraction")
    # ... existing fallback
```

**Gotchas:**
- Some models put explanation in the code block
- Some models use markdown inside code blocks
- Need to handle imports that span the preamble

## Dependencies

- **Blocked by:** None (can develop independently)
- **Blocks:** None

## Verification

```bash
# Run tests for code extraction
uv run pytest tests/test_code_extraction.py -v

# Test with real model outputs (save samples)
uv run python -c "
from evals.cdk_synth.tasks import _extract_code
samples = [...] # paste real model outputs
for s in samples:
    print(_extract_code(s)[:100])
"
```
