---
name: lint-check
description: Check code for linting issues without making changes.
allowed-tools:
  - Bash
  - Read
---

# Lint Check Command

Check code for linting and style issues without modifying files.

## Process

### 1. Run Linters
```bash
# Python
uv run ruff check .

# JavaScript/TypeScript
pnpm lint

# Format check (no changes)
uv run ruff format --check .
pnpm format --check
```

### 2. Report Issues

## Output Format

```markdown
## Lint Report

### Summary
| Category | Issues |
|----------|--------|
| Errors | 2 |
| Warnings | 5 |
| Style | 12 |

### Errors (must fix)
| File | Line | Code | Message |
|------|------|------|---------|
| src/api.py | 42 | E501 | Line too long |
| src/auth.py | 18 | F401 | Unused import |

### Warnings
[List of warnings]

### Style Issues
[List of style issues]

### Quick Fix
Run `lint-fix` to auto-fix [X] issues.
```

## Issue Categories

### Python (ruff)
- **E**: Errors (pycodestyle)
- **W**: Warnings (pycodestyle)
- **F**: Fatal (pyflakes)
- **I**: Import sorting
- **N**: Naming conventions
- **UP**: Upgrade suggestions

### JavaScript (eslint)
- **error**: Must fix
- **warn**: Should fix
- **off**: Disabled rules

## Example

```
Checking lint...

Python (ruff):
src/api/handler.py:42:80 E501 Line too long (92 > 88 characters)
src/api/handler.py:15:1 F401 'os' imported but unused
src/utils/helpers.py:8:1 I001 Import block is un-sorted

Found 3 issues

JavaScript (eslint):
src/components/Button.tsx:12:5 warning Unexpected console.log
src/utils/format.ts:8:10 error 'unused' is defined but never used

Found 2 issues (1 error, 1 warning)

Total: 5 issues
Auto-fixable: 4
Manual fix needed: 1
```
