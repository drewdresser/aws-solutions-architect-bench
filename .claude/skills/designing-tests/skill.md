---
name: designing-tests
description: Knowledge and patterns for designing comprehensive test strategies and writing effective tests.
---

# Designing Tests Skill

This skill provides patterns and techniques for creating effective test suites.

## Testing Pyramid

```
           /\
          /  \      E2E (10%)
         /----\
        /      \    Integration (20%)
       /--------\
      /          \  Unit (70%)
     /------------\
```

## Test Design Patterns

### 1. Arrange-Act-Assert (AAA)
```python
def test_user_registration():
    # Arrange - Set up test data and dependencies
    user_data = {"email": "test@example.com", "password": "secure123"}

    # Act - Execute the code under test
    result = register_user(user_data)

    # Assert - Verify the outcome
    assert result.success is True
    assert result.user.email == "test@example.com"
```

### 2. Given-When-Then (BDD)
```python
def test_discount_for_premium_users():
    # Given a premium user with items in cart
    user = create_premium_user()
    cart = create_cart(user, items=[item(price=100)])

    # When calculating the total
    total = cart.calculate_total()

    # Then a 20% discount is applied
    assert total == 80
```

### 3. Test Fixtures
```python
@pytest.fixture
def db_session():
    """Provide a clean database session for each test."""
    session = create_session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def authenticated_user(db_session):
    """Provide an authenticated user."""
    user = User.create(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user
```

### 4. Parameterized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123abc", "123ABC"),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```

## Edge Cases Checklist

### Input Validation
- [ ] Empty/null inputs
- [ ] Boundary values (0, -1, MAX_INT)
- [ ] Invalid types
- [ ] Special characters
- [ ] Unicode strings
- [ ] Very long inputs
- [ ] Whitespace handling

### State Management
- [ ] Initial state
- [ ] After successful operation
- [ ] After failed operation
- [ ] Concurrent modifications
- [ ] Recovery from errors

### External Dependencies
- [ ] Network timeout
- [ ] Service unavailable
- [ ] Invalid response format
- [ ] Rate limiting
- [ ] Partial failures

### Time-Based
- [ ] Timezone handling
- [ ] Daylight saving transitions
- [ ] Leap years
- [ ] Date boundaries

## Mocking Strategies

### When to Mock
- External APIs
- Database calls (for unit tests)
- Time-dependent operations
- Random number generation
- File system operations

### When NOT to Mock
- The code under test
- Simple value objects
- Pure functions
- Internal implementation details

### Mock Examples
```python
# Mock external API
@patch('services.payment.stripe_client')
def test_payment_processing(mock_stripe):
    mock_stripe.charge.return_value = {"id": "ch_123", "status": "succeeded"}
    result = process_payment(amount=100)
    assert result.success is True

# Mock time
@freeze_time("2024-01-15")
def test_subscription_expiry():
    sub = Subscription(expires_at=datetime(2024, 1, 14))
    assert sub.is_expired() is True
```

## Test Organization

### File Structure
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
├── e2e/
│   └── test_user_flows.py
├── fixtures/
│   └── conftest.py
└── factories/
    └── user_factory.py
```

### Naming Conventions
```python
# Pattern: test_[action]_[condition]_[expected_result]
def test_login_with_valid_credentials_returns_token():
def test_login_with_invalid_password_returns_401():
def test_login_with_locked_account_raises_AccountLockedException():
```

## Coverage Guidelines

| Component | Target |
|-----------|--------|
| Business logic | 90%+ |
| Utilities | 85%+ |
| API endpoints | 80%+ |
| Configuration | 60%+ |

## Anti-Patterns to Avoid

- **Flaky tests** - Tests that sometimes pass, sometimes fail
- **Slow tests** - Unit tests should be < 100ms
- **Test interdependence** - Tests that rely on other tests
- **Over-mocking** - Mocking everything including the thing you're testing
- **Assert-less tests** - Tests without meaningful assertions
- **Duplicate tests** - Testing the same thing multiple ways
