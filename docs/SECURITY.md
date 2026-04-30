# Security

## Secrets And Credentials

- No live credentials or tokens belong in this repository.
- `.env` and variants are gitignored. Do not add exceptions.
- Skill helper scripts in `skills/*/scripts/` are deterministic and offline. Do not introduce network calls or token reads into them.

## Trust Boundaries

- `SKILL.md` files are read by agent hosts (Codex, Cursor, etc.) at invocation time. Keep them free of executable content beyond the prose instructions they carry.
- `scripts/validate_skills.py` uses Python `ast`/`compile` for syntax checks, not `exec`. Do not change this to dynamic evaluation.

## Safe Change Rules

- Every `SKILL.md` behavioral change requires a version bump and matching `CHANGELOG.md` entry before merge.
- Do not add dependencies to `pyproject.toml` without reviewing their transitive graph. The repo is intentionally stdlib-only.
- Do not add a new top-level directory or skill without a `SKILL.md` that the validator accepts.
