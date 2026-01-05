---
name: lint-fix
description: Automatically fix linting issues in the codebase.
allowed-tools:
  - Bash
  - Read
  - Edit
---

# Lint Fix Command

Automatically fix linting and formatting issues.

## Process

### 1. Run Linter in Fix Mode
```bash
# Python (ruff)
uv run ruff check . --fix
uv run ruff format .

# JavaScript/TypeScript (eslint + prettier)
pnpm lint --fix
pnpm format
```

### 2. Report Changes
- List files modified
- Summarize fixes applied
- Note any issues requiring manual fix

### 3. Verify
```bash
# Re-run linter to confirm clean
uv run ruff check .
pnpm lint
```

## Auto-Fixable Issues

### Python (ruff)
- Import sorting
- Unused imports
- Trailing whitespace
- Missing newlines
- Quote style
- Line length (where possible)

### JavaScript/TypeScript
- Semicolons
- Quote style
- Trailing commas
- Import order
- Unused variables (removal)
- Spacing/indentation

## Manual Intervention

Some issues can't be auto-fixed:
- Complex logic restructuring
- Type errors
- Security issues
- Naming conventions

## Output

```
Running lint fix...

Python:
✓ Fixed 12 issues in 5 files
  - Sorted imports: 5 files
  - Removed unused imports: 3 files
  - Fixed line length: 4 issues

Remaining issues requiring manual fix:
⚠ src/api/handler.py:42 - Function too complex (C901)

Verification:
✓ No linting errors
```
