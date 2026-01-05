---
name: create-epics
description: Analyze strategy docs and codebase to generate epics that advance OKRs.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Task
---

# Create Epics Command

Generate strategic epics by analyzing the project's vision, OKRs, codebase state, and existing work.

## When to Use

- Vision and OKRs are defined but no epics exist yet
- All existing epics are marked as `Done`
- Starting a new quarter and need fresh epics aligned to updated OKRs
- Want to identify the next logical body of work

## Prerequisites

The project must have:
- `/strategy/VISION.md` — Strategic foundation
- `/strategy/OKRs.md` — Current quarter objectives

## Process

### 1. Read Strategic Context

```bash
# Required files
/strategy/VISION.md
/strategy/OKRs.md
```

Extract and understand:
- North Star and Vision
- Current OKRs and Key Results
- Strategic Bets (what approaches are we betting on)
- Non-Goals (what we're explicitly NOT doing)
- Success Metrics

### 2. Analyze Existing State

Check for existing epics and their status:

```bash
# List existing epics
ls /strategy/epics/

# For each epic, check status
grep -l "Status.*Done" /strategy/epics/*.md
grep -l "Status.*In Progress" /strategy/epics/*.md
```

**If in-progress epics exist**: Ask user if they want to continue those or create new ones.

### 3. Review ADRs

Check `/strategy/adrs/` for architectural decisions that constrain or guide epic creation:
- Technology choices already made
- Patterns to follow
- Approaches explicitly rejected

### 4. Explore Codebase

Understand the current state of the project:

- **Project structure**: What exists? What's missing?
- **Technical debt**: Are there obvious gaps or issues?
- **Dependencies**: What's already integrated?
- **Test coverage**: What areas lack testing?

Use the Task tool with `subagent_type=Explore` for codebase analysis:
- "What is the current project structure and architecture?"
- "What features are implemented vs. stubbed out?"
- "What are the main entry points and how do they connect?"

### 5. Generate Epics

Create epics that:

1. **Advance OKRs** - Each epic should contribute to at least one Key Result
2. **Are technically grounded** - Based on actual codebase state, not assumptions
3. **Have clear user value** - Deliver meaningful outcomes
4. **Are appropriately scoped** - Achievable within a reasonable timeframe
5. **Respect non-goals** - Don't create epics for things explicitly out of scope

### 6. Analyze Dependencies & Priority

For each epic, determine:

**Dependencies:**
- What must exist before this epic can start?
- What other epics rely on this one completing?
- Are there shared technical foundations?

**Priority:**
- **High**: Foundational work, blocks other epics, critical to OKRs
- **Medium**: Important but can wait for high-priority work
- **Low**: Nice-to-have, can be deferred if needed

Document these in each epic's Dependencies section to make work order explicit and discoverable.

### 7. Write Epic Files

For each epic, create a file in `/strategy/epics/<epic-name>.md`:

```markdown
# Epic: [User-Facing Outcome]

## User Value

[1-2 sentences: Why does this matter to users?]

## Success Criteria

- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

## Technical Approach

[2-4 sentences: How will we implement this? What patterns/technologies?]

## OKR Alignment

- **Objective**: [Which OKR objective this advances]
- **Key Result**: [Which specific KR this contributes to]

## Dependencies

- **Depends on**: [List epics that must complete first, or "None"]
- **Blocks**: [List epics that depend on this one, or "None"]
- **Priority**: `High` | `Medium` | `Low`

## Tasks

<!-- Tasks will be created just-in-time when work begins -->
- [ ] _Tasks to be defined when epic starts_

## Status

`Not Started`
```

### 8. Update OKRs

Add links to the newly created epics in `/strategy/OKRs.md`:

```markdown
**Related Epics:** [epic-name.md](epics/epic-name.md), [another-epic.md](epics/another-epic.md)
```

## Output Summary

After creating epics, provide:

```
## Epics Created

| Epic | OKR Alignment | Priority | Dependencies |
|------|---------------|----------|--------------|
| [epic-name.md](epics/epic-name.md) | O1/KR2 | High | None |
| [another-epic.md](epics/another-epic.md) | O2/KR1 | Medium | Depends on epic-name |

## Recommended Work Order

1. **[epic-name]** - No dependencies, high priority, foundational work
2. **[another-epic]** - Depends on epic-name completing
3. **[third-epic]** - Can work in parallel with another-epic

## Risk Areas

- [Any concerns or uncertainties]

## Not Created (and why)

- [Idea that was considered but rejected]: [Reason - e.g., violates non-goals]
```

**Note**: All dependencies are persisted in each epic's Dependencies section, making work order clear for future reference.

## Guidelines

### Good Epic Characteristics

- **Outcome-focused**: Describes what users can do, not implementation details
- **Measurable**: Success criteria are specific and testable
- **Clearly sequenced**: Dependencies are explicitly documented for work order clarity
- **Valuable**: Delivers meaningful user or business value
- **Estimable**: Scope is clear enough to roughly estimate effort

### Avoid

- Epics that are just "refactoring" with no user-facing value
- Epics that violate stated non-goals
- Epics with vague success criteria ("improve performance")
- Epics that duplicate existing in-progress work
- Epics not connected to any OKR

### Naming Convention

Use kebab-case with user-facing outcome:
- `user-authentication.md`
- `export-to-pdf.md`
- `real-time-collaboration.md`
- `mobile-responsive-dashboard.md`

## Example Interaction

**User**: `/create-epics`

**Agent**:
1. Reads VISION.md and OKRs.md
2. Checks existing epics - finds 2 marked Done, 0 in progress
3. Reviews 3 ADRs for constraints
4. Explores codebase structure
5. Proposes 3 new epics aligned to Q1 OKRs
6. Analyzes dependencies and assigns priorities
7. Writes epic files with Dependencies section populated
8. Updates OKRs.md with epic links
9. Outputs summary with recommended work order

## Error Handling

| Situation | Response |
|-----------|----------|
| No `/strategy/VISION.md` | Ask user to create strategy docs first |
| No `/strategy/OKRs.md` | Ask user to define OKRs first |
| OKRs are stale/completed | Suggest updating OKRs before creating epics |
| In-progress epics exist | Ask if user wants to continue those or generate new |
| Codebase is empty | Generate bootstrap epics (setup, initial features) |
