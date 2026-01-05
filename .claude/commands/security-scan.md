---
name: security-scan
description: Scan the codebase for security vulnerabilities and issues.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Security Scan Command

Scan the codebase for potential security vulnerabilities.

## Scan Areas

### 1. Dependency Vulnerabilities
```bash
# Python
uv pip audit

# Node
pnpm audit
```

### 2. Secret Detection
```bash
# Check for hardcoded secrets
grep -rn "password\s*=" --include="*.py" --include="*.ts" .
grep -rn "api_key\s*=" --include="*.py" --include="*.ts" .
grep -rn "secret\s*=" --include="*.py" --include="*.ts" .
```

### 3. Code Patterns
- SQL injection risks
- Command injection risks
- XSS vulnerabilities
- Insecure deserialization
- Path traversal

### 4. Configuration
- Debug mode enabled
- Insecure defaults
- Missing security headers

## Output Format

```markdown
## Security Scan Report

### Summary
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 3 |
| Low | 5 |

### Critical Issues
[None found - or list issues]

### High Severity
#### [Issue Title]
- **File**: `src/api/auth.py:42`
- **Type**: Hardcoded secret
- **Description**: API key found in source code
- **Remediation**: Move to environment variable

### Medium Severity
[List medium issues]

### Low Severity
[List low issues]

### Dependency Vulnerabilities
| Package | Version | Vulnerability | Fix Version |
|---------|---------|---------------|-------------|
| requests | 2.25.0 | CVE-2023-xxx | 2.28.0 |

### Recommendations
1. [Prioritized action items]
2. [...]
```

## Common Patterns to Check

### SQL Injection
```python
# Dangerous
query = f"SELECT * FROM users WHERE id = {user_id}"

# Safe
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Command Injection
```python
# Dangerous
os.system(f"echo {user_input}")

# Safe
subprocess.run(["echo", user_input], shell=False)
```

### XSS
```javascript
// Dangerous
element.innerHTML = userInput;

// Safe
element.textContent = userInput;
```

## Example

```
Running security scan...

Dependency Audit:
✓ Python: No known vulnerabilities
⚠ Node: 2 moderate vulnerabilities

Secret Detection:
⚠ Found 1 potential hardcoded secret
  src/config.py:15 - API_KEY = "sk-..."

Code Analysis:
⚠ src/api/search.py:42 - Potential SQL injection
✓ No XSS vulnerabilities detected
✓ No command injection detected

Summary: 3 issues found (0 critical, 1 high, 2 medium)
```
