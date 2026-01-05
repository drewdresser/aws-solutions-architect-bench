---
name: verify-changes
description: Verify that recent changes meet quality standards before commit/push.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Verify Changes Command

Run comprehensive verification on staged or recent changes.

## Verification Checklist

### 1. Code Quality
```bash
# Linting
uv run ruff check .
pnpm lint

# Type checking
uv run ty
pnpm typecheck
```

### 2. Tests
```bash
# Run relevant tests
uv run pytest
pnpm test
```

### 3. Build
```bash
# Verify build succeeds
pnpm build
```

### 4. Security
```bash
# Check for secrets
git diff --cached | grep -E "(password|secret|api_key|token)" || echo "No secrets found"
```

### 5. Documentation
- Check if new public APIs have docstrings
- Verify README is current

## Output Format

```markdown
## Verification Report

### Summary
[Pass/Fail overall status]

### Checks

| Check | Status | Details |
|-------|--------|---------|
| Lint | ✓ Pass | No issues |
| Types | ✓ Pass | No errors |
| Tests | ✓ Pass | 42 passed |
| Build | ✓ Pass | Build successful |
| Security | ✓ Pass | No secrets detected |

### Issues Found
[List any issues if present]

### Recommendation
[Ready to commit / Needs attention]
```

## Quick Mode

For fast verification:
```bash
# Just run essential checks
uv run ruff check . && uv run pytest tests/ -x -q
```

## Example Output

```
Running verification...

✓ Lint: No issues
✓ Types: No errors
✓ Tests: 42 passed, 0 failed
✓ Build: Success
✓ Security: No secrets detected

Verification Result: PASS

Ready to commit!
```
