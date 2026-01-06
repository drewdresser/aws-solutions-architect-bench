# Task: Document One-Command Quickstart

**Epic:** [reproducibility-and-ci.md](../epics/reproducibility-and-ci.md)
**Size:** `S`
**Status:** `Done`

## Context

README has a quick start section but doesn't highlight the "one-command run" path clearly. Users should be able to reproduce leaderboard results with minimal friction.

## Acceptance Criteria

- [ ] README prominently shows one-command path: `make bench && make board.json`
- [ ] Prerequisites clearly listed (Python 3.12+, uv, Docker, API key)
- [ ] Environment setup documented (`.env` configuration)
- [ ] Expected output described (what files are created, where)
- [ ] Troubleshooting section for common issues

## Technical Notes

**Relevant Files:**
- `README.md` — Enhance Quick Start section
- `.env.example` — May need additional comments

**Approach:**
Restructure Quick Start to emphasize the simple path:
1. Clone
2. `uv sync`
3. Set up `.env`
4. `make bench && make board.json`
5. View `results/leaderboard.json`

Add a "Reproduce Leaderboard" section that's even more explicit.

**Content to add:**
```markdown
## Reproduce the Leaderboard

```bash
git clone https://github.com/drewdresser/aws-sa-bench
cd aws-sa-bench
uv sync
cp .env.example .env  # Add your OPENROUTER_API_KEY
make bench && make board.json
cat results/leaderboard.json
```
```

**Gotchas:**
- Docker must be running for CDK eval
- API costs may be a concern for users

## Dependencies

- **Blocked by:** None
- **Blocks:** None

## Verification

```bash
# Follow the documented steps on a fresh clone
# Verify leaderboard.json is produced
```
