# CDK Synth Evaluation - OpenRouter Error Handling Solutions

This directory contains solutions for handling intermittent OpenRouter API errors during CDK evaluation runs.

## Problem

The original evaluation sometimes fails with `OpenRouterError` (500 Internal Server Error) during the `self_critique()` step. This is a transient API issue with OpenRouter, not a problem with the CDK code being evaluated.

## Solutions

### 1. Enhanced Original (tasks.py)
- **File**: `tasks.py`
- **Description**: The original task with improved retry configuration
- **Changes**:
  - Increased `max_retries` from 3 to 5
  - Increased `timeout` from 60s to 180s
  - Added retry configuration to the `generate()` step

**Usage**:
```bash
inspect eval evals/cdk_synth/tasks.py --model openrouter/anthropic/claude-opus-4
```

### 2. No Self-Critique (tasks_no_critique.py)
- **File**: `tasks_no_critique.py`
- **Description**: Removes the `self_critique()` step entirely to avoid API errors
- **Changes**:
  - Removed `self_critique()` from the solver pipeline
  - Faster execution (fewer API calls)
  - No risk of self-critique API failures

**Usage**:
```bash
inspect eval evals/cdk_synth/tasks_no_critique.py --model openrouter/anthropic/claude-opus-4
```

### 3. Robust Self-Critique (tasks_robust.py)
- **File**: `tasks_robust.py`
- **Description**: Custom self-critique solver with comprehensive error handling
- **Features**:
  - Exponential backoff retry logic
  - Fallback to original answer on persistent errors
  - Detailed logging of retry attempts
  - Configurable retry count and error handling behavior

**Usage**:
```bash
inspect eval evals/cdk_synth/tasks_robust.py --model openrouter/anthropic/claude-opus-4
```

## Recommended Approach

For production use, I recommend:

1. **Quick Fix**: Use `tasks_no_critique.py` to eliminate the error source entirely
2. **Full Solution**: Use `tasks_robust.py` for the most comprehensive error handling
3. **Minimal Changes**: Use `tasks.py` if you want to keep the original structure with just better retries

## Testing

To test the solutions:

```bash
# Test with a small sample size first
inspect eval evals/cdk_synth/tasks_robust.py --model openrouter/anthropic/claude-opus-4 --limit 3

# Run full evaluation
inspect eval evals/cdk_synth/tasks_robust.py --model openrouter/anthropic/claude-opus-4 --log-dir results/
```

## Configuration Options

### GenerateConfig Parameters
- `max_retries`: Number of retry attempts for API calls (default: 5)
- `timeout`: Timeout in seconds for each API call (default: 180)

### Robust Self-Critique Parameters
- `max_retries`: Retry attempts for self-critique (default: 3)
- `fallback_on_error`: Continue with original answer on persistent errors (default: True)

## Monitoring

The robust solution includes logging to help monitor retry attempts:
- `Self-critique completed on attempt X`
- `Self-critique attempt X failed: [error]`
- `Self-critique failed after all retries, continuing with original answer`

## Performance Impact

- **No Self-Critique**: Fastest, ~33% fewer API calls
- **Enhanced Original**: Moderate, same API calls but with retries
- **Robust Self-Critique**: Slowest initially, but more reliable completion rate 