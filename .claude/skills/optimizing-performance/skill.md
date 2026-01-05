---
name: optimizing-performance
description: Knowledge and patterns for identifying and resolving performance issues.
---

# Optimizing Performance Skill

This skill provides patterns and techniques for performance optimization.

## Performance Analysis Process

### 1. Measure First
```bash
# Python profiling
python -m cProfile -s cumtime script.py

# Memory profiling
python -m memory_profiler script.py

# Node.js profiling
node --prof app.js
node --prof-process isolate-*.log > processed.txt
```

### 2. Identify Bottlenecks
- CPU-bound: Computation heavy
- I/O-bound: Waiting for disk/network
- Memory-bound: High memory usage
- Concurrency: Lock contention

### 3. Optimize Systematically
- Focus on hotspots (80/20 rule)
- One change at a time
- Measure after each change
- Document trade-offs

## Common Optimizations

### Database

#### N+1 Query Problem
```python
# Bad: N+1 queries
users = User.query.all()
for user in users:
    print(user.orders)  # Query per user!

# Good: Eager loading
users = User.query.options(joinedload(User.orders)).all()
for user in users:
    print(user.orders)  # Already loaded
```

#### Indexing
```sql
-- Identify slow queries
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Add index
CREATE INDEX idx_users_email ON users(email);

-- Composite index for common queries
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

#### Query Optimization
```sql
-- Bad: SELECT *
SELECT * FROM users WHERE status = 'active';

-- Good: Select needed columns
SELECT id, name, email FROM users WHERE status = 'active';

-- Bad: LIKE with leading wildcard
SELECT * FROM users WHERE name LIKE '%john%';

-- Better: Full-text search or specific patterns
SELECT * FROM users WHERE name LIKE 'john%';
```

### Caching

#### Application-Level Cache
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(x, y):
    return complex_calculation(x, y)
```

#### Distributed Cache (Redis)
```python
import redis

cache = redis.Redis()

def get_user(user_id):
    # Try cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # Fetch from DB
    user = db.query(User).get(user_id)

    # Store in cache
    cache.setex(f"user:{user_id}", 3600, json.dumps(user.to_dict()))
    return user.to_dict()
```

#### HTTP Caching
```python
from flask import make_response

@app.route('/static-data')
def static_data():
    response = make_response(get_static_data())
    response.headers['Cache-Control'] = 'public, max-age=3600'
    response.headers['ETag'] = compute_etag(data)
    return response
```

### Async Processing

#### Background Jobs
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def send_email(to, subject, body):
    # Heavy operation in background
    email_service.send(to, subject, body)

# Usage
send_email.delay("user@example.com", "Welcome", "...")
```

#### Async I/O
```python
import asyncio
import aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
```

### Memory Optimization

#### Generators Instead of Lists
```python
# Bad: Loads all into memory
def get_all_users():
    return [User.from_row(row) for row in db.fetchall()]

# Good: Process one at a time
def get_all_users():
    for row in db.fetchall():
        yield User.from_row(row)
```

#### Slots for Classes
```python
class Point:
    __slots__ = ['x', 'y']  # 40% less memory than dict

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

#### Weak References
```python
import weakref

class Cache:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
```

### Algorithm Optimization

#### Time Complexity
| Operation | List | Dict/Set |
|-----------|------|----------|
| Lookup | O(n) | O(1) |
| Insert | O(n) | O(1) |
| Delete | O(n) | O(1) |

```python
# Bad: O(n) lookup
if item in my_list:  # Scans entire list
    ...

# Good: O(1) lookup
if item in my_set:  # Hash lookup
    ...
```

#### Space-Time Trade-offs
```python
# Compute once, store result (memoization)
@lru_cache(maxsize=1000)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Performance Checklist

### Database
- [ ] Queries are using indexes
- [ ] No N+1 query problems
- [ ] Pagination for large result sets
- [ ] Connection pooling enabled
- [ ] Queries select only needed columns

### Application
- [ ] Expensive operations are cached
- [ ] Heavy work is done asynchronously
- [ ] Resources are properly cleaned up
- [ ] Memory usage is bounded
- [ ] No memory leaks

### Network
- [ ] API responses are compressed
- [ ] Static assets are cached
- [ ] Minimal round trips
- [ ] Connection pooling/keep-alive

### Frontend
- [ ] Assets are minified
- [ ] Images are optimized
- [ ] Lazy loading for large lists
- [ ] Bundle size is reasonable

## Monitoring

### Key Metrics
- Response time (p50, p95, p99)
- Throughput (requests/second)
- Error rate
- CPU/Memory usage
- Database query time

### Tools
- APM: New Relic, Datadog, Sentry
- Profiling: py-spy, cProfile, Chrome DevTools
- Database: EXPLAIN, pg_stat_statements
- Load testing: k6, locust, wrk
