# Reliability

## Critical Journeys

- `uv run python scripts/validate_skills.py` exits 0 on a fresh clone.
- A skill installed from this repo loads cleanly in Codex or another agent host.
- Agent clients that scan `.agents/skills/` can use the same skills without a separate install step.
- `uv run python skills/cultivate/scripts/audit_cultivate.py .` runs read-only without modifying files.

## Failure Modes

- **Validator non-zero**: the error message names the file and expected format. Fix the reported frontmatter field or Python syntax.
- **`uv.lock` drift**: run `uv sync` to reconcile.
- **`evals.json` syntax error**: `validate_skills.py` reports the parsing failure; fix the JSON.
- **`.agents/skills/` drift**: run `uv run python scripts/sync_agents_skills.py`, then rerun validation.
- **Skill not found in a local host install**: check that `name` in `SKILL.md` frontmatter matches the directory name, that the validator passes, and that the host was installed through its own path such as `npx skills`. Repo validation does not inspect `~/.codex/skills` or `.claude`.

## Validation

- `uv run python scripts/validate_skills.py` exits 0 → all skills pass the packaging gate.
- `uv run python -m unittest scripts.test_validate_skills` → all tests OK.
- `uv run python scripts/sync_agents_skills.py` → `.agents/skills/` is regenerated from `skills/`.
