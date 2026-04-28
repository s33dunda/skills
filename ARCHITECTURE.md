# Architecture Map

## Purpose

This repository houses installable `SKILL.md` packages — `cultivate` and `plot` — distributed via the `vercel-labs/skills` CLI. The workflow it enables is: `plot` → `seed.md` → `cultivate` → farmer agents execute against the prepared repo.

## Main Flows

1. **Skill authoring**: edit `skills/<name>/SKILL.md`, `references/`, `scripts/`, `evals/`, and `CHANGELOG.md`.
2. **Validation**: `uv run python scripts/validate_skills.py` checks frontmatter, metadata, Python syntax, and eval structure for every skill in the repo.
3. **Skill installation**: `python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo s33dunda/skills --path skills/<skill-name>` installs a skill into Codex or another agent host.
4. **Harness audit**: `uv run python skills/cultivate/scripts/audit_cultivate.py .` reports cultivate gaps against the repo itself or any target path.

## Boundaries

- Each skill is self-contained: `SKILL.md`, `references/`, `scripts/`, `evals/evals.json`, `CHANGELOG.md`. No cross-skill imports.
- `scripts/` at repo root are repo-level utilities (validate, test). Not skill helpers.
- Skill scripts in `skills/*/scripts/` must be deterministic and offline — no network calls.
- `pyproject.toml` + `uv.lock` declare the repo runner; never use a global `python` or `pip`.

## Extension Points

- **New skill**: add a directory under `skills/` with the required structure. The validator enforces it.
- **New validator rule**: extend `scripts/validate_skills.py` and add a test in `scripts/test_validate_skills.py`.
- **New references or helpers**: add to `skills/<name>/references/` or `skills/<name>/scripts/` — not to repo root.

## Mechanical Enforcement

- `uv run python scripts/validate_skills.py` — packaging gate; run after any `SKILL.md` or helper change.
- `uv run python -m unittest scripts.test_validate_skills` — validator unit tests.
- `uv run python skills/cultivate/scripts/audit_cultivate.py .` — harness gap check for this repo.
