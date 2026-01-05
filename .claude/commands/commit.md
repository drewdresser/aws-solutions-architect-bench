---
name: commit
description: Create a conventional commit with auto-generated message based on staged changes.
allowed-tools:
  - Bash
  - Read
---

# Commit Command

Generate and execute a conventional commit based on staged changes.

## Allowed Operations

- `git status` - Check repository state
- `git diff --cached` - View staged changes
- `git diff --cached --stat` - View change statistics
- `git log --oneline -10` - View recent commits for style reference
- `git commit -m "..."` - Execute the commit

## Process

1. **Check staged changes**
   ```bash
   git diff --cached --stat
   ```

2. **If nothing staged**: Prompt user to stage files first

3. **Analyze changes** to determine:
   - What was modified
   - Type of change (feat, fix, refactor, etc.)
   - Scope of change

4. **Generate commit message** following conventional commits:
   ```
   type(scope): description

   [optional body]

   [optional footer]
   ```

5. **Execute commit**

## Commit Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Maintenance, deps, config |

## Examples

```bash
# Feature
git commit -m "feat(auth): add password reset flow"

# Bug fix
git commit -m "fix(api): handle null response from external service"

# Refactor
git commit -m "refactor(utils): extract date formatting to shared module"
```

## User Arguments

If the user provides hints, incorporate them:
- `commit auth` → scope is "auth"
- `commit "add login"` → use as description hint
- `commit fix` → type is "fix"

## Output

```
Staged changes:
 M src/auth/login.py
 A src/auth/reset.py

Commit message:
feat(auth): add password reset functionality

Committed: abc1234
```
