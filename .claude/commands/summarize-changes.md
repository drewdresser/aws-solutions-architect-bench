---
name: summarize-changes
description: Generate a summary of recent changes in the repository.
allowed-tools:
  - Bash
  - Read
---

# Summarize Changes Command

Generate a human-readable summary of recent changes.

## Process

### 1. Gather Information
```bash
# Recent commits
git log --oneline -20

# Changed files
git diff --name-only HEAD~10

# Diff stats
git diff --stat HEAD~10
```

### 2. Analyze Changes
- Group by type (feature, fix, refactor)
- Identify major components affected
- Note breaking changes

### 3. Generate Summary

## Output Format

```markdown
## Change Summary

**Period**: [Date range or commit range]
**Commits**: [Count]
**Files Changed**: [Count]

### New Features
- [Feature 1] - [Brief description]
- [Feature 2] - [Brief description]

### Bug Fixes
- [Fix 1] - [What was fixed]
- [Fix 2] - [What was fixed]

### Improvements
- [Improvement 1]
- [Improvement 2]

### Breaking Changes
- [Breaking change if any]

### Files Most Changed
| File | Changes |
|------|---------|
| src/api/handler.py | +150, -42 |
| src/models/user.py | +80, -20 |

### Contributors
- [Author 1]: [X commits]
- [Author 2]: [X commits]
```

## Customization

Accept arguments for:
- Time range: `summarize-changes --since="1 week ago"`
- Commit range: `summarize-changes HEAD~10..HEAD`
- Branch comparison: `summarize-changes main..feature-branch`

## Example

```
Summarizing changes from last 10 commits...

## Change Summary

**Period**: Dec 28 - Jan 3
**Commits**: 10
**Files Changed**: 23

### New Features
- Password reset flow (auth module)
- Export to CSV functionality (reports)

### Bug Fixes
- Fixed null pointer in user lookup
- Corrected timezone handling in scheduler

### Improvements
- Optimized database queries in user service
- Added input validation to API endpoints

### Files Most Changed
| File | Changes |
|------|---------|
| src/auth/reset.py | +180, -0 |
| src/reports/export.py | +120, -15 |
```
