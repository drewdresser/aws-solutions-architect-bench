---
name: commit-push-pr
description: Commit staged changes, push to remote, and create a pull request.
allowed-tools:
  - Bash
  - Read
---

# Commit, Push, and PR Command

Complete the full git workflow: commit changes, push to remote, and create a pull request.

## Process

### 1. Pre-flight Checks
```bash
# Ensure we're not on main/master
git branch --show-current

# Check for staged changes
git diff --cached --stat

# Check remote status
git remote -v
```

### 2. Commit (if changes staged)
```bash
# Generate conventional commit message
git commit -m "type(scope): description"
```

### 3. Push
```bash
# Push with upstream tracking
git push -u origin $(git branch --show-current)
```

### 4. Create PR
```bash
# Create PR with title and body
gh pr create --title "type(scope): description" --body "## Summary
- Change 1
- Change 2

## Test Plan
- [ ] Test case 1
- [ ] Test case 2"
```

## PR Template

```markdown
## Summary
[Brief description of changes]

## Changes
- [Change 1]
- [Change 2]

## Test Plan
- [ ] [How to verify]

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No security issues
```

## Safeguards

- Never push directly to main/master
- Require at least one staged change
- Verify remote exists before push
- Check if PR already exists for branch

## Output

```
Committing...
✓ Committed: feat(auth): add password reset

Pushing...
✓ Pushed to origin/feature/password-reset

Creating PR...
✓ PR created: https://github.com/org/repo/pull/123

Summary:
- Commit: abc1234
- Branch: feature/password-reset
- PR: #123
```
