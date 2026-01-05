---
name: sync-branch
description: Synchronize current branch with the latest changes from main/master.
allowed-tools:
  - Bash
---

# Sync Branch Command

Update the current branch with the latest changes from the main branch.

## Process

### 1. Pre-flight Checks
```bash
# Check for uncommitted changes
git status

# Identify main branch
git remote show origin | grep "HEAD branch"
```

### 2. Fetch Latest
```bash
git fetch origin
```

### 3. Rebase or Merge
```bash
# Preferred: Rebase for clean history
git rebase origin/main

# Alternative: Merge if rebase is problematic
git merge origin/main
```

### 4. Handle Conflicts (if any)
- List conflicting files
- Provide guidance on resolution
- Continue rebase/merge after resolution

### 5. Verify
```bash
# Check status
git status

# Show branch relation to origin
git log --oneline origin/main..HEAD
```

## Conflict Resolution

If conflicts occur:

```
Conflicts detected in:
- src/api/handler.py
- src/utils/helpers.py

To resolve:
1. Edit conflicting files
2. Remove conflict markers (<<<<, ====, >>>>)
3. Stage resolved files: git add <file>
4. Continue: git rebase --continue
```

## Output

```
Syncing branch: feature/auth-update

Fetching origin...
✓ Fetched latest changes

Rebasing onto origin/main...
✓ Rebased 3 commits

Branch is now 3 commits ahead of origin/main

Commits on this branch:
- abc1234 feat(auth): add password validation
- def5678 test(auth): add validation tests
- ghi9012 docs(auth): update API docs
```

## Safeguards

- Warn if uncommitted changes exist
- Never force push to shared branches
- Preserve commit history
- Abort on complex conflicts (let user decide)
