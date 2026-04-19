# Agent Guide

## Orientation

This repository is a monorepo of Codex skills. Each installable skill lives under
`skills/<skill-name>/` and must contain a valid `SKILL.md`.

Use the root `README.md` for user-facing install instructions and this file for
agent workflow.

## Useful Commands

- Validate skill packaging: `python3 scripts/validate_skills.py`
- Install a skill from GitHub:
  `python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo s33dunda/skills --path skills/<skill-name>`

## Repository Map

- `skills/`: installable skill directories.
- `skills/README.md`: index of available skills.
- `scripts/validate_skills.py`: repo-level validation for skill structure and bundled Python scripts.

## Working Norms

Keep each skill self-contained. Put reusable guidance in `references/`, deterministic helpers in
`scripts/`, templates/assets in `assets/`, and test prompts in `evals/`.

The core guardrail is installability: every skill directory must have matching `name` frontmatter,
a non-empty `description`, valid eval metadata when present, and syntactically valid Python helpers.

Before committing, run `python3 scripts/validate_skills.py`. If a skill includes Python helpers,
the validator parses them with `ast` so syntax errors are caught before publishing.
