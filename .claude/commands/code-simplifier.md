---
name: code-simplifier
description: Simplify complex code while preserving behavior.
allowed-tools:
  - Read
  - Edit
  - Bash
  - Grep
---

# Code Simplifier Command

Identify and simplify overly complex code while preserving exact behavior.

## Complexity Indicators

- Deep nesting (> 3 levels)
- Long functions (> 50 lines)
- Many parameters (> 5)
- Complex conditionals
- Duplicate code blocks
- Unclear variable names

## Simplification Techniques

### 1. Early Returns
```python
# Before
def process(data):
    if data is not None:
        if data.is_valid:
            if data.has_items:
                return do_work(data)
    return None

# After
def process(data):
    if data is None:
        return None
    if not data.is_valid:
        return None
    if not data.has_items:
        return None
    return do_work(data)
```

### 2. Extract Functions
```python
# Before
def handle_order(order):
    # 50 lines of validation
    # 30 lines of processing
    # 20 lines of notification

# After
def handle_order(order):
    validate_order(order)
    process_order(order)
    notify_customer(order)
```

### 3. Use Built-ins
```python
# Before
result = []
for item in items:
    if item.is_active:
        result.append(item.name)

# After
result = [item.name for item in items if item.is_active]
```

### 4. Simplify Conditionals
```python
# Before
if x == True:
    return True
else:
    return False

# After
return x
```

## Process

1. **Identify** - Find complex code sections
2. **Understand** - Ensure you know what it does
3. **Simplify** - Apply appropriate technique
4. **Verify** - Run tests to confirm behavior unchanged

## Output Format

```markdown
## Simplification Report

### Files Analyzed
- `src/api/handler.py`
- `src/utils/processor.py`

### Changes Made

#### src/api/handler.py

**Before** (complexity: 8):
```python
[original code]
```

**After** (complexity: 3):
```python
[simplified code]
```

**Technique**: Early returns, extract function

### Metrics
| File | Before | After | Reduction |
|------|--------|-------|-----------|
| handler.py | 8 | 3 | 62% |

### Verification
✓ All tests pass
```

## Rules

- Never change behavior
- Run tests after each change
- Prefer readability over cleverness
- Document non-obvious simplifications
- Keep changes focused and reviewable
