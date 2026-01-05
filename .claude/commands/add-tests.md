---
name: add-tests
description: Add comprehensive tests for existing code.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Add Tests Command

Add comprehensive test coverage for specified code.

## Process

### 1. Analyze the Code
- Read the target file/function
- Identify public interfaces
- Map dependencies to mock
- List edge cases

### 2. Plan Tests
- Happy path cases
- Error cases
- Edge cases
- Boundary conditions

### 3. Write Tests
- Follow existing test patterns in the project
- Use appropriate fixtures
- Keep tests focused and isolated
- Use descriptive names

### 4. Verify
- Run new tests
- Check coverage increase

## Test Structure

```python
class TestFeatureName:
    """Tests for [feature description]."""

    def test_happy_path(self):
        """Should [expected behavior] when [condition]."""
        # Arrange
        # Act
        # Assert

    def test_error_case(self):
        """Should raise [error] when [condition]."""
        # Arrange
        # Act & Assert
        with pytest.raises(ExpectedError):
            function_under_test(invalid_input)

    def test_edge_case(self):
        """Should handle [edge case]."""
        # Arrange
        # Act
        # Assert
```

## Naming Convention

```python
# Pattern: test_[action]_[condition]_[expected_result]

def test_login_with_valid_credentials_returns_token():
def test_login_with_expired_password_prompts_reset():
def test_login_with_locked_account_returns_403():
```

## Coverage Checklist

- [ ] Normal inputs
- [ ] Empty inputs
- [ ] Null/None inputs
- [ ] Boundary values
- [ ] Error conditions
- [ ] Async behavior (if applicable)
- [ ] Concurrent access (if applicable)

## Output

```
Adding tests for: src/auth/login.py

Test file: tests/test_login.py

Tests added:
- test_login_success
- test_login_invalid_password
- test_login_user_not_found
- test_login_empty_email
- test_login_empty_password

Running tests...
✓ All 5 tests passed

Coverage: 85% → 94% (+9%)
```
