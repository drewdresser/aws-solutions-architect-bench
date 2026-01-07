# Task: Add pytest and Test Infrastructure

**Epic:** [scoring-and-aggregation-hardening.md](../epics/scoring-and-aggregation-hardening.md)
**Size:** `S`
**Status:** `Done`

## Context

No test infrastructure exists. Before adding aggregation tests, we need pytest configured and a basic test structure in place.

## Acceptance Criteria

- [ ] `pytest` added to pyproject.toml dependencies
- [ ] `tests/` directory created with `__init__.py`
- [ ] `tests/conftest.py` with basic fixtures (if needed)
- [ ] `uv run pytest` runs successfully (even with no tests)
- [ ] Makefile target `test` added for convenience

## Technical Notes

**Relevant Files:**
- `pyproject.toml` — Add pytest dependency
- `tests/` — New directory to create
- `Makefile` — Add test target

**Approach:**
1. Add `pytest>=8.0` to pyproject.toml dependencies
2. Create `tests/` directory with `__init__.py`
3. Create minimal `tests/conftest.py`
4. Add Makefile target: `test: uv run pytest`
5. Run `uv sync` to install

**Gotchas:**
- Ensure tests can import from `scripts/` (may need path configuration)
- Consider adding `pytest-cov` for coverage reporting later

## Dependencies

- **Blocked by:** None
- **Blocks:** 003, 004 (tests need infrastructure)

## Verification

```bash
uv sync
uv run pytest --collect-only  # Should show 0 tests collected, no errors
make test  # Should run without errors
```
