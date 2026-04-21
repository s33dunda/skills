# skills

A skill suite that turns an idea into an agent-ready repository. Distributed as a monorepo of [SKILL.md](https://github.com/anthropics/skills) packages installable into Claude Code, Augment, Codex, and any other agent that speaks the skill format.

## The Workflow

```
plot  ->  seed.md  ->  cultivate  ->  farmers
```

- **`plot`** captures the minimum viable idea as a structured brief (`seed.md`).
- **`seed.md`** is the handoff artifact: project identity, scope, stack, success criteria, agent surface, open questions.
- **`cultivate`** reads `seed.md` (or audits an existing repo) and prepares the repository for agents -- `AGENTS.md`, knowledge map, architectural guardrails, execution-plan conventions, CI/lint/test feedback exposure. Cultivate is applied harness engineering.
- **Farmers** are the agents that then work the repo. In *this* repo, farmers use Anthropic's [`skill-creator`](https://github.com/anthropics/skills) to iterate on the skills themselves.

## Install

Install both skills into any supported agent via the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx -y skills@latest add s33dunda/skills
```

Or install a single skill by path:

```bash
npx -y skills@latest add s33dunda/skills/skills/plot
npx -y skills@latest add s33dunda/skills/skills/cultivate
```

## Skills

| Skill | Path | Purpose |
| --- | --- | --- |
| `plot` | `skills/plot` | Capture a minimum viable project idea and emit `seed.md`. |
| `cultivate` | `skills/cultivate` | Consume `seed.md` (or audit a live repo) and prepare it for AI agents. |

## Validation

Before publishing changes, validate the monorepo:

```bash
python3 scripts/validate_skills.py
```

This checks each installable skill for required frontmatter, eval metadata, and Python helper syntax. CI runs the skill eval suite on every PR and posts a sticky status comment.

## Repository Layout

```text
.
├── AGENTS.md              # agent working norms for this repo
├── README.md              # this file
├── seed.md                # the seed for this repo, produced by plot
├── scripts/               # monorepo-level tooling (validator, eval runner)
└── skills/
    ├── README.md          # skill index
    ├── plot/
    └── cultivate/
```

Each skill directory is self-contained: `SKILL.md` + `references/` + `scripts/` + `evals/`.
