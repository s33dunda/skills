# Skill Index

Install all skills in this monorepo via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx -y skills@latest add s33dunda/skills
```

Or install a single skill by path:

```bash
npx -y skills@latest add s33dunda/skills/skills/plot
npx -y skills@latest add s33dunda/skills/skills/cultivate
```

## Available Skills

| Skill | Purpose | Version |
| --- | --- | --- |
| `plot` | Capture a minimum viable project idea as `seed.md`. | see `plot/CHANGELOG.md` |
| `cultivate` | Consume `seed.md` (or audit an existing repo) and emit the harness bundle (`AGENTS.md` + `docs/{ARCHITECTURE,QUALITY,PLANS}.md`). | see `cultivate/CHANGELOG.md` |

Each skill carries a semver `version` field in its `SKILL.md` frontmatter. Breaking changes to a skill's interface bump the major; added capabilities bump the minor; prose or reference fixes bump the patch.

## Contributor Check

From the repo root, run:

```bash
python3 scripts/validate_skills.py
```

The validator checks frontmatter (`name`, `description`, `version`), eval metadata, and Python helper syntax. CI runs the skill eval suite on every PR.
