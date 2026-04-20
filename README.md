# skills

A monorepo of Codex skills maintained by s33dunda.

## Install

Install a skill from this repo with the bundled `skill-installer` helper:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo s33dunda/skills \
  --path skills/cultivate
```

After installing, restart Codex to pick up new skills.

You can also install from a GitHub URL:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/s33dunda/skills/tree/main/skills/cultivate
```

## Skills

| Skill | Path | Purpose |
| --- | --- | --- |
| `cultivate` | `skills/cultivate` | Turn repositories into agent-legible, enforceable Codex cultivatees. |

## Validation

Before publishing changes, validate the monorepo:

```bash
python3 scripts/validate_skills.py
```

This checks each installable skill for required frontmatter, eval metadata, and Python helper syntax.

## Repository Layout

```text
.
+-- AGENTS.md
+-- README.md
+-- scripts/
|   +-- validate_skills.py
+-- skills/
    +-- cultivate/
        +-- SKILL.md
        +-- evals/
        +-- references/
        +-- scripts/
```

Each skill directory is installable by passing its path to `install-skill-from-github.py`.
