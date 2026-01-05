---
name: analyzing-projects
description: Knowledge and patterns for understanding project structures, architectures, and codebases.
---

# Analyzing Projects Skill

This skill provides patterns and techniques for understanding unfamiliar codebases and project structures.

## Quick Reconnaissance

### 1. Project Type Detection

Check for key files to identify the project type:

| File | Indicates |
|------|-----------|
| `package.json` | Node.js project |
| `pyproject.toml` | Modern Python project |
| `requirements.txt` | Python project |
| `go.mod` | Go project |
| `Cargo.toml` | Rust project |
| `pom.xml` | Java Maven project |
| `build.gradle` | Java Gradle project |
| `Gemfile` | Ruby project |

### 2. Framework Detection

| File/Pattern | Framework |
|--------------|-----------|
| `next.config.js` | Next.js |
| `vite.config.ts` | Vite |
| `angular.json` | Angular |
| `src/App.vue` | Vue.js |
| `manage.py` | Django |
| `app.py` / Flask imports | Flask |
| `main.go` | Go |
| `src/main.rs` | Rust |

### 3. Architecture Patterns

Look for these directory structures:

```
# Monolith
src/
  models/
  views/
  controllers/

# Microservices
services/
  user-service/
  order-service/
  payment-service/

# Domain-Driven Design
src/
  domain/
  application/
  infrastructure/

# Feature-based
src/
  features/
    auth/
    dashboard/
    settings/
```

## Key Files to Read First

1. **`/strategy/VISION.md`** - Strategic context (if exists)
2. **`/strategy/OKRs.md`** - Current priorities (if exists)
3. **`/strategy/adrs/`** - Architecture decisions (if exists)
4. **README.md** - Project overview and setup
5. **package.json / pyproject.toml** - Dependencies and scripts
6. **docker-compose.yml** - Services and infrastructure
7. **.env.example** - Required configuration
8. **Makefile / justfile** - Available commands

### Strategy Folder (if present)

If a `/strategy/` folder exists, prioritize reading:

| File | Purpose |
|------|---------|
| `VISION.md` | North star, strategic bets, non-goals |
| `OKRs.md` | Current quarter objectives |
| `epics/*.md` | Active feature initiatives |
| `tasks/*.md` | Specific work items |
| `adrs/*.md` | Settled architectural decisions |

## Mapping Dependencies

### External Dependencies
```bash
# Python
cat pyproject.toml | grep -A 100 "\[dependencies\]"

# Node
cat package.json | jq '.dependencies, .devDependencies'
```

### Internal Dependencies
```bash
# Find imports
grep -rh "^import\|^from" src/ | sort | uniq -c | sort -rn

# Find module usage
grep -rn "from src\." . --include="*.py"
```

## Understanding Data Flow

1. **Entry points** - Where requests come in
2. **Routes/Controllers** - Request handling
3. **Services** - Business logic
4. **Models** - Data structures
5. **Repositories** - Data access
6. **External APIs** - Outbound calls

## Common Patterns to Identify

### Authentication
- JWT tokens
- Session-based
- OAuth providers

### Database
- ORM (SQLAlchemy, Prisma, TypeORM)
- Raw SQL
- NoSQL (MongoDB, Redis)

### API Style
- REST
- GraphQL
- gRPC
- WebSocket

### Testing Strategy
- Unit tests
- Integration tests
- E2E tests

## Analysis Checklist

- [ ] Does a `/strategy/` folder exist? If so, read VISION.md and OKRs.md first.
- [ ] Are there ADRs in `/strategy/adrs/`? These contain settled decisions.
- [ ] What type of project is this?
- [ ] What framework(s) are used?
- [ ] What is the directory structure pattern?
- [ ] What are the main entry points?
- [ ] What are the key dependencies?
- [ ] How is configuration managed?
- [ ] What testing approach is used?
- [ ] How is the project built and deployed?
