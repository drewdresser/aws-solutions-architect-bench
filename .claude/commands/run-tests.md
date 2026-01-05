---
name: run-tests
description: Execute the project's test suite with detailed reporting.
allowed-tools:
  - Bash
  - Read
---

# Run Tests Command

Execute tests with comprehensive output and reporting.

## Process

### 1. Detect Test Framework
- Python: pytest
- JavaScript: jest/vitest
- Go: go test

### 2. Run Tests
```bash
# Python - full suite
uv run pytest -v

# Python - with coverage
uv run pytest --cov=src --cov-report=term-missing

# JavaScript
pnpm test

# JavaScript - with coverage
pnpm test -- --coverage
```

### 3. Report Results

## Output Format

```markdown
## Test Results

### Summary
| Metric | Value |
|--------|-------|
| Total | 142 |
| Passed | 140 |
| Failed | 2 |
| Skipped | 0 |
| Duration | 4.2s |

### Coverage
| Module | Coverage |
|--------|----------|
| src/auth | 94% |
| src/api | 87% |
| src/utils | 91% |
| **Total** | **90%** |

### Failures
[Details of any failures]

### Slow Tests
| Test | Duration |
|------|----------|
| test_integration_full | 2.1s |
| test_database_migration | 1.8s |
```

## Options

### Run Specific Tests
```bash
# By file
uv run pytest tests/test_auth.py -v

# By name pattern
uv run pytest -k "login" -v

# By marker
uv run pytest -m "slow" -v
```

### Quick Mode
```bash
# Stop on first failure
uv run pytest -x

# Last failed only
uv run pytest --lf
```

### Verbose Mode
```bash
# Show print statements
uv run pytest -s

# Show local variables on failure
uv run pytest -l
```

## Example

```
Running tests...

========================= test session starts =========================
collected 142 items

tests/test_auth.py::test_login_success PASSED
tests/test_auth.py::test_login_invalid_password PASSED
tests/test_auth.py::test_login_user_not_found PASSED
...

========================= 142 passed in 4.2s =========================

Coverage: 90%
```
