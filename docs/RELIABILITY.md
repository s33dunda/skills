# Reliability

## Critical Journeys

- `uv run python scripts/validate_skills.py` exits 0 on a fresh clone.
- A skill installed from this repo loads cleanly in Codex or another agent host.
- `uv run python skills/cultivate/scripts/audit_cultivate.py .` runs read-only without modifying files.

## Failure Modes

- **Validator non-zero**: the error message names the file and expected format. Fix the reported frontmatter field or Python syntax.
- **`uv.lock` drift**: run `uv sync` to reconcile.
- **`evals.json` syntax error**: `validate_skills.py` reports the parsing failure; fix the JSON.
- **Skill not found after install**: check that `name` in `SKILL.md` frontmatter matches the directory name and that the validator passes.

## Validation

- `uv run python scripts/validate_skills.py` exits 0 → all skills pass the packaging gate.
- `uv run python -m unittest scripts.test_validate_skills` → all tests OK.
