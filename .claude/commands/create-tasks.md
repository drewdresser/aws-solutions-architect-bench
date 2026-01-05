---
name: create-tasks
description: Break down an epic into actionable, developer-ready tasks with technical grounding.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Task
---

# Create Tasks Command

Act as an **expert product manager** to break down an epic into well-scoped, actionable tasks that developers (or AI agents) can execute independently.

## When to Use

- An epic exists and is ready to start (`Not Started` → `In Progress`)
- An epic is `In Progress` but has no tasks or incomplete task breakdown
- Scope has changed and tasks need re-planning
- Starting a new phase of work on an existing epic

## Prerequisites

The project must have:
- `/strategy/VISION.md` — Strategic foundation
- `/strategy/OKRs.md` — Current quarter objectives
- `/strategy/epics/<epic-name>.md` — The epic to break down

## Process

### 1. Identify Target Epic

If not specified, list available epics and ask which to break down:

```bash
ls /strategy/epics/
```

Confirm with the user which epic to create tasks for.

### 2. Read Strategic Context

Load the full context hierarchy:

```bash
# Strategic foundation
/strategy/VISION.md

# Current priorities
/strategy/OKRs.md

# Target epic
/strategy/epics/<epic-name>.md
```

Extract and internalize:
- **Vision & Non-Goals**: What we're building toward, and what's out of scope
- **OKR Alignment**: Which Key Results this epic contributes to
- **Epic Success Criteria**: The measurable outcomes we must achieve
- **Technical Approach**: Stated implementation direction
- **Dependencies**: What must exist before tasks can execute

### 3. Review ADRs

Check `/strategy/adrs/` for architectural decisions that constrain task design:

```bash
ls /strategy/adrs/
```

Pay attention to:
- Technology choices that affect implementation
- Patterns to follow or avoid
- Integration approaches already decided
- Performance or security constraints

### 4. Deep Codebase Analysis

**This is critical.** Tasks must be grounded in reality, not assumptions.

Use the Task tool with `subagent_type=Explore` for thorough analysis:

**Structural Analysis:**
- "What is the current project structure and file organization?"
- "What modules/packages exist and how are they connected?"
- "What's the entry point and request/data flow?"

**Relevant Implementation:**
- "What code already exists related to [epic topic]?"
- "What interfaces, types, or contracts are defined that we'll integrate with?"
- "What utilities, helpers, or patterns are already established?"

**Gap Analysis:**
- "What's missing to implement [epic success criteria]?"
- "What needs to be created vs. modified vs. extended?"
- "Are there stubs or TODOs related to this epic?"

**Technical Debt:**
- "What existing issues in this area should be addressed?"
- "Are there blocking refactors needed first?"

### 5. Apply Product Manager Thinking

Before writing tasks, think like a PM:

**User Journey Mapping:**
- What's the user's path through this feature?
- What are the critical moments that must work?
- Where could users get confused or blocked?

**Risk Assessment:**
- Which parts have technical uncertainty?
- What could go wrong and how do we mitigate?
- Where should we prototype first?

**Sequencing Strategy:**
- What's the minimum viable slice?
- What can be parallelized?
- What depends on what?

**Scope Management:**
- What's essential vs. nice-to-have?
- What could be deferred to a follow-up epic?
- Are we respecting non-goals?

### 6. Design Task Breakdown

Create tasks that are:

| Quality | Description |
|---------|-------------|
| **Atomic** | Can be completed in a single focused session (S/M preferred) |
| **Independent** | Minimal dependencies on other in-progress work |
| **Testable** | Clear acceptance criteria that can be verified |
| **Valuable** | Delivers incremental progress toward epic success |
| **Technically Grounded** | Based on actual codebase state, not assumptions |

**Task Categories to Consider:**

1. **Foundation Tasks** — Setup, scaffolding, interfaces
2. **Core Implementation** — Main feature logic
3. **Integration Tasks** — Connecting to existing systems
4. **Edge Case Handling** — Error states, validation, edge cases
5. **Testing Tasks** — Unit tests, integration tests (only if substantial)
6. **Polish Tasks** — UX refinement, performance optimization

### 7. Determine Task Order

Analyze dependencies to create a logical work order:

**Dependency Types:**
- **Hard Dependencies**: Task B literally cannot start until Task A completes
- **Soft Dependencies**: Task B is easier after Task A, but could technically start
- **Parallel Tracks**: Independent work streams that can proceed simultaneously

**Prioritization Factors:**
- Risk reduction (tackle uncertainty early)
- Unblocking other tasks
- Quick wins for momentum
- Critical path items

### 8. Write Task Files

For each task, create `/strategy/tasks/<epic-name>-###-<description>.md`:

```markdown
# Task: [Clear, Action-Oriented Title]

**Epic:** [epic-name.md](../epics/epic-name.md)  
**Size:** `S` | `M` | `L` | `XL`  
**Status:** `Todo`

## Context

[1-2 sentences: Why this task exists and how it fits into the epic]

## Acceptance Criteria

- [ ] [Specific, testable requirement 1]
- [ ] [Specific, testable requirement 2]
- [ ] [Specific, testable requirement 3]

## Technical Notes

**Relevant Files:**
- `path/to/file.ts` — [What needs to change]
- `path/to/another.ts` — [What to integrate with]

**Approach:**
[2-4 sentences on suggested implementation approach]

**Gotchas:**
- [Potential pitfall to avoid]
- [Edge case to handle]

## Dependencies

- **Blocked by:** [Task ###, or "None"]
- **Blocks:** [Task ###, or "None"]

## Verification

```bash
# How to verify this task is complete
[command to run tests or check functionality]
```
```

### 9. Update Epic File

Add task links to the parent epic's Tasks section:

```markdown
## Tasks

- [ ] [epic-name-001-description.md](../tasks/epic-name-001-description.md)
- [ ] [epic-name-002-description.md](../tasks/epic-name-002-description.md)
- [ ] [epic-name-003-description.md](../tasks/epic-name-003-description.md)
```

Update epic status to `In Progress` if it was `Not Started`.

### 10. Generate Summary

Output a clear summary:

```markdown
## Tasks Created for [Epic Name]

| # | Task | Size | Dependencies | Risk |
|---|------|------|--------------|------|
| 001 | [description](../tasks/epic-name-001-desc.md) | S | None | Low |
| 002 | [description](../tasks/epic-name-002-desc.md) | M | 001 | Medium |
| 003 | [description](../tasks/epic-name-003-desc.md) | S | None | Low |

**Total Size:** [X S, Y M, Z L]

## Recommended Work Order

### Phase 1: Foundation (can parallelize)
- 001 — [Brief description]
- 003 — [Brief description]

### Phase 2: Core Implementation
- 002 — [Brief description] (after 001)

### Phase 3: Polish
- 004 — [Brief description]

## Risk Areas

- **[Task ###]**: [Why it's risky and mitigation strategy]

## Deferred / Out of Scope

- [Feature idea]: Deferred to follow-up epic because [reason]
- [Nice-to-have]: Out of scope per non-goals

## Open Questions

- [ ] [Any decision that needs user input before proceeding]
```

## Guidelines

### Good Task Characteristics

- **Action-oriented title**: Starts with a verb ("Implement", "Add", "Create", "Integrate")
- **Right-sized**: S or M preferred; L/XL should be rare and may need splitting
- **Self-contained context**: Agent can understand it without reading other tasks
- **Concrete acceptance criteria**: Not "works correctly" but "returns 200 OK with user object"
- **Includes verification**: How to prove it's done

### Task Title Patterns

| Pattern | Example |
|---------|---------|
| **Create [thing]** | Create user authentication middleware |
| **Implement [feature]** | Implement password reset flow |
| **Add [capability]** | Add email validation to signup form |
| **Integrate [system]** | Integrate Stripe payment webhook |
| **Update [thing] to [do something]** | Update user model to include preferences |
| **Fix [issue]** | Fix race condition in session refresh |

### Naming Convention

`<epic-name>-###-<brief-description>.md`

- Epic name matches the epic file (kebab-case)
- Three-digit zero-padded number (001, 002, 003)
- Brief description in kebab-case (3-5 words max)

Examples:
- `user-authentication-001-setup-auth-middleware.md`
- `user-authentication-002-implement-login-endpoint.md`
- `user-authentication-003-add-session-management.md`

### Avoid

- Tasks that are too vague ("Make the UI better")
- Tasks that are too large (multi-day efforts)
- Tasks with unclear completion criteria
- Tasks that duplicate work in another task
- Tasks that violate stated non-goals
- Tasks without technical grounding in the actual codebase

## Example Interaction

**User**: `/create-tasks user-authentication`

**Agent**:
1. Reads VISION.md, OKRs.md, and user-authentication.md epic
2. Reviews relevant ADRs (finds ADR-003 on session management approach)
3. Explores codebase:
   - Finds existing User model in `src/models/user.ts`
   - Finds API routes in `src/routes/`
   - Notes existing middleware pattern in `src/middleware/`
   - Identifies missing: auth endpoints, session handling, password hashing
4. Applies PM thinking:
   - Maps login → session → protected route flow
   - Identifies password hashing as low-risk, session management as higher
5. Designs 6 tasks with logical sequencing
6. Writes task files with relevant file paths and technical notes
7. Updates epic with task links and sets status to `In Progress`
8. Outputs summary with work order and risk assessment

## Error Handling

| Situation | Response |
|-----------|----------|
| Epic not found | List available epics and ask user to specify |
| Epic already has tasks | Ask if user wants to add more or regenerate |
| No `/strategy/` folder | Direct user to set up strategy docs first |
| Epic status is `Done` | Confirm user wants to reopen and add tasks |
| Missing VISION.md or OKRs.md | Warn about limited context, proceed with epic only |
| Codebase is empty | Generate bootstrap/scaffolding tasks |

## Integration with Other Commands

- After `/create-tasks`, developers or agents can pick up individual tasks
- Use `/architect` if tasks reveal need for design decisions → create ADR
- Update task status as work progresses
- When all tasks complete, update epic status to `Done`

