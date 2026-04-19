# skills

A monorepo of Codex skills maintained by s33dunda.

## Install

Install a skill from this repo with the bundled `skill-installer` helper:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo s33dunda/skills \
  --path skills/harness-repo
```

After installing, restart Codex to pick up new skills.

You can also install from a GitHub URL:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/s33dunda/skills/tree/main/skills/harness-repo
```

## Skills

| Skill | Path | Purpose |
| --- | --- | --- |
| `harness-repo` | `skills/harness-repo` | Turn repositories into agent-legible, enforceable Codex harnesses. |

## Repository Layout

```text
.
├── README.md
└── skills/
    └── harness-repo/
        ├── SKILL.md
        ├── evals/
        ├── references/
        └── scripts/
```

Each skill directory is installable by passing its path to `install-skill-from-github.py`.
