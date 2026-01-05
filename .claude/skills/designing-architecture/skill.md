---
name: designing-architecture
description: Knowledge and patterns for designing software architectures and system design.
---

# Designing Architecture Skill

This skill provides patterns and techniques for designing robust software architectures.

## Architecture Patterns

### Layered Architecture
```
┌─────────────────────────────────┐
│       Presentation Layer        │
├─────────────────────────────────┤
│        Application Layer        │
├─────────────────────────────────┤
│         Domain Layer            │
├─────────────────────────────────┤
│       Infrastructure Layer      │
└─────────────────────────────────┘
```

### Hexagonal Architecture (Ports & Adapters)
```
              ┌─────────────────┐
              │   REST API      │
              └────────┬────────┘
                       │
┌──────────┐   ┌──────▼──────┐   ┌──────────┐
│ Database │◀──│   Domain    │──▶│ External │
│ Adapter  │   │   Core      │   │   API    │
└──────────┘   └─────────────┘   └──────────┘
```

### Microservices
```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Service │  │ Service │  │ Service │
│    A    │  │    B    │  │    C    │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┼────────────┘
                  │
           ┌──────▼──────┐
           │ Message Bus │
           └─────────────┘
```

### Event-Driven Architecture
```
┌─────────┐     ┌───────────┐     ┌─────────┐
│ Producer│────▶│Event Store│────▶│Consumer │
└─────────┘     └───────────┘     └─────────┘
```

## Design Principles

### SOLID
- **S**ingle Responsibility - One reason to change
- **O**pen/Closed - Open for extension, closed for modification
- **L**iskov Substitution - Subtypes must be substitutable
- **I**nterface Segregation - Many specific interfaces
- **D**ependency Inversion - Depend on abstractions

### Other Principles
- **DRY** - Don't Repeat Yourself
- **KISS** - Keep It Simple, Stupid
- **YAGNI** - You Aren't Gonna Need It
- **Separation of Concerns**
- **Fail Fast**

## Common Patterns

### Repository Pattern
```python
class UserRepository:
    def get_by_id(self, user_id: str) -> User: ...
    def save(self, user: User) -> None: ...
    def delete(self, user_id: str) -> None: ...
    def find_by_email(self, email: str) -> Optional[User]: ...
```

### Service Layer
```python
class OrderService:
    def __init__(self, order_repo, payment_service, notification_service):
        self.order_repo = order_repo
        self.payment = payment_service
        self.notifications = notification_service

    def place_order(self, order: Order) -> OrderResult:
        self.order_repo.save(order)
        self.payment.charge(order.total)
        self.notifications.send_confirmation(order)
```

### Factory Pattern
```python
class NotificationFactory:
    @staticmethod
    def create(type: str) -> Notification:
        if type == "email":
            return EmailNotification()
        elif type == "sms":
            return SMSNotification()
        elif type == "push":
            return PushNotification()
        raise ValueError(f"Unknown type: {type}")
```

### Strategy Pattern
```python
class PaymentStrategy(Protocol):
    def process(self, amount: Decimal) -> PaymentResult: ...

class StripePayment:
    def process(self, amount: Decimal) -> PaymentResult: ...

class PayPalPayment:
    def process(self, amount: Decimal) -> PaymentResult: ...

class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def pay(self, amount: Decimal) -> PaymentResult:
        return self.strategy.process(amount)
```

## Non-Functional Requirements

### Scalability
- Horizontal vs vertical scaling
- Stateless services
- Caching strategies
- Database sharding

### Reliability
- Circuit breakers
- Retry with backoff
- Graceful degradation
- Health checks

### Security
- Authentication/Authorization
- Data encryption
- Input validation
- Audit logging

### Performance
- Caching layers
- Async processing
- Connection pooling
- Query optimization

## Architecture Decision Records (ADR)

ADRs should be stored in `/strategy/adrs/` using the naming convention `###-kebab-case-title.md`.

**Before making architectural decisions**, check existing ADRs to avoid revisiting settled questions.

Template:
```markdown
# ADR-001: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD

## Context
[Why is this decision needed?]

## Decision
[What was decided?]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Trade-off 1]
- [Trade-off 2]

### Risks
- [Risk 1]
```

### Workflow Integration

ADRs are part of the broader strategy workflow:
- `/strategy/VISION.md` — Strategic context
- `/strategy/OKRs.md` — Current priorities
- `/strategy/epics/` — Feature initiatives
- `/strategy/tasks/` — Specific work items
- `/strategy/adrs/` — Architectural decisions (you are here)

## Diagramming

### Component Diagram
```
┌─────────────────────────────────────────┐
│              Application                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │   API   │  │ Service │  │   DB    │  │
│  │ Gateway │─▶│  Layer  │─▶│ Access  │  │
│  └─────────┘  └─────────┘  └────┬────┘  │
└──────────────────────────────────┼──────┘
                                   │
                            ┌──────▼──────┐
                            │  Database   │
                            └─────────────┘
```

### Sequence Diagram (ASCII)
```
Client          API           Service        Database
  │              │               │               │
  │──request────▶│               │               │
  │              │──validate────▶│               │
  │              │              ││──query───────▶│
  │              │              ││◀──result──────│
  │              │◀──response───│               │
  │◀──response───│               │               │
```
