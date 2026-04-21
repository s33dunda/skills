# Agent Guide

## Orientation

This repository is a monorepo of Codex skills. Each installable skill lives under
`skills/<skill-name>/` and must contain a valid `SKILL.md`.

Use the root `README.md` for user-facing install instructions and this file for
agent workflow.

## Useful Commands

- Validate skill packaging: `uv run python scripts/validate_skills.py` (or `python3 scripts/validate_skills.py`)
- Run validator unit tests: `uv run python -m unittest scripts.test_validate_skills` (or `python3 -m unittest scripts.test_validate_skills`)
- Sync the locked environment: `uv sync`
- Install a skill from GitHub:
  `python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo s33dunda/skills --path skills/<skill-name>`

The repo is stdlib-only Python; `uv.lock` + `pyproject.toml` declare the runner so agents never fall back to a global interpreter. `python3` is still acceptable for one-off validator calls.

## Repository Map

- `skills/`: installable skill directories.
- `skills/README.md`: index of available skills.
- `scripts/validate_skills.py`: repo-level validation for skill structure and bundled Python scripts.
- `scripts/test_validate_skills.py`: stdlib unittest fixtures for the validator (frontmatter allowlist, semver, metadata).
- `pyproject.toml` / `uv.lock`: declared Python runner for isolated invocations.
- `.github/pull_request_template.md` + `.github/ISSUE_TEMPLATE/`: PRs and issues must supply acceptance criteria and validation evidence.

## Execution Plans

For multi-skill or cross-cutting work (e.g. `SKILL.md` + evals + references + `CHANGELOG.md` in a single effort), open an ExecPlan under `docs/plans/<slug>.md`. Convention: `docs/PLANS.md`. Template: `docs/plans/_template.md` (mirrors the canonical skeleton in `skills/cultivate/references/templates.md`). Resolve ambiguity autonomously; record decisions in the plan's `Decision Log` rather than pausing to ask.

Single-file changes do not need a plan.

## Working Norms

Keep each skill self-contained. Put reusable guidance in `references/`, deterministic helpers in
`scripts/`, templates/assets in `assets/`, and test prompts in `evals/`.

The core guardrail is installability: every skill directory must have matching `name` frontmatter,
a non-empty `description`, valid eval metadata when present, and syntactically valid Python helpers.

Before committing, run `python3 scripts/validate_skills.py`. If a skill includes Python helpers,
the validator parses them with `ast` so syntax errors are caught before publishing.
