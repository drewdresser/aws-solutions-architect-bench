---
name: quick-fix
description: Rapidly fix a specific issue with minimal changes.
allowed-tools:
  - Read
  - Edit
  - Bash
  - Grep
  - Glob
---

# Quick Fix Mode

Apply a targeted fix with minimal changes. No refactoring, no improvements beyond the scope of the fix.

## Approach

1. **Understand the issue** - What exactly is broken?
2. **Locate the problem** - Find the specific code causing it
3. **Apply minimal fix** - Change only what's necessary
4. **Verify** - Confirm the fix works

## Rules

- **One fix at a time** - Don't bundle changes
- **Minimal diff** - Smallest possible change
- **No drive-by fixes** - Don't fix unrelated issues
- **No refactoring** - Even if the code is ugly
- **Test the fix** - Run relevant tests

## Process

```
Issue: [Description of the problem]

Location: [file:line]

Root cause: [Why it's happening]

Fix:
[Minimal code change]

Verification:
[Command to verify fix]
```

## Example

```
Issue: Login fails when email has uppercase letters

Location: src/auth/login.py:42

Root cause: Email comparison is case-sensitive

Fix:
- email == stored_email
+ email.lower() == stored_email.lower()

Verification:
uv run pytest tests/test_auth.py::test_login_case_insensitive -v
```

## Don'ts

- Don't reformat surrounding code
- Don't add comments explaining the fix
- Don't update unrelated tests
- Don't add error handling for other cases
- Don't suggest "while we're here" improvements
