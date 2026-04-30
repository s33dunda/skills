# skills

A skill suite that turns an idea into an agent-ready repository. Distributed as a monorepo of [SKILL.md](https://github.com/anthropics/skills) packages installable into Claude Code, Augment, Codex, and any other agent that speaks the skill format.

## The Workflow

```
plot  ->  seed.md  ->  cultivate  ->  {AGENTS, ARCHITECTURE, QUALITY, PLANS}.md  ->  farmers
```

- **`plot`** captures the minimum viable idea as a structured brief (`seed.md`).
- **`seed.md`** is the handoff artifact: project identity, scope, stack, success criteria, agent surface, open questions.
- **`cultivate`** reads `seed.md` (or audits an existing repo) and emits the harness bundle: `AGENTS.md` at the root plus `docs/ARCHITECTURE.md`, `docs/QUALITY.md`, `docs/PLANS.md`, together with mechanical checks and execution-plan conventions. Cultivate is applied harness engineering.
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

Fresh checkouts also include a repo-local `.agents/skills/` mirror. Agent
clients that know how to scan `.agents/` can load `plot` and `cultivate`
without a separate install step. This repo does not validate or manage local
user-state installs such as `~/.codex/skills` or `.claude`; use the `npx
skills` commands above for those hosts when needed.

When a canonical skill changes, refresh the committed `.agents/skills/` mirror
from `skills/` with:

```bash
uv run python scripts/sync_agents_skills.py
```

## Skills

| Skill | Path | Purpose |
| --- | --- | --- |
| `plot` | `skills/plot` | Capture a minimum viable project idea and emit `seed.md`. |
| `cultivate` | `skills/cultivate` | Consume `seed.md` (or audit a live repo) and prepare it for AI agents. |

## Validation

Before publishing changes, validate the monorepo:

```bash
uv run python scripts/validate_skills.py
```

This checks each installable skill for required frontmatter, eval metadata,
Python helper syntax, and committed `.agents/skills/` mirror drift. It does not
inspect `~/.codex/skills`, `.claude`, or other local agent install locations.

## Repository Layout

```text
.
├── AGENTS.md              # agent working norms for this repo
├── README.md              # this file
├── .agents/               # repo-local agent-client mirror of the skills
├── seed.md                # the seed for this repo, produced by plot
├── scripts/               # monorepo-level tooling (validator)
└── skills/
    ├── README.md          # skill index
    ├── plot/
    └── cultivate/
```

Each skill directory is self-contained: `SKILL.md` + `references/` + `scripts/` + `evals/`.
