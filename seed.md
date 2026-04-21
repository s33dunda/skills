---
name: skills
tagline: "A skill suite that turns an idea into an agent-ready repo via a repeatable plot -> cultivate workflow."
stack: [Markdown, YAML, Python, GitHub Actions]
status: draft
---

## Problem

Preparing a repository so that AI agents can reliably work in it is ad-hoc and
inconsistent. Every team reinvents `AGENTS.md`, knowledge maps, execution-plan
conventions, CI feedback loops, and architectural guardrails. The result is
drift, hidden human context, and agents that fail in ways that could have been
caught by structure.

`skills` provides a repeatable, opinionated workflow for this: capture the idea
(`plot`), hand off a structured brief (`seed.md`), and prepare the target repo
for agents (`cultivate`). Farmers (the agents themselves) then work the repo.

## Audience

Platform engineers and engineers building or maintaining agentic systems who
need a consistent, repo-level preflight before letting agents run. Not targeted
at end-users of agents; targeted at the people wiring agents into codebases.

## Scope (MVP)

**In:**

- `plot` skill -- captures the minimum viable idea and writes `seed.md`.

- `cultivate` skill -- consumes `seed.md` (or an existing repo) and prepares it
  for agents: AGENTS.md, knowledge map, execution-plan conventions,
  architectural guardrails, CI/lint/test feedback exposure.
- Installable for any supported agent via `npx skills add s33dunda/skills`.
- Skill eval CI that runs on PRs and posts a sticky status comment.
- Validator (`scripts/validate_skills.py`) enforces SKILL.md structure.

**Out (explicitly):**

- A standalone `seed` skill. `seed.md` is the artifact produced by `plot`,

  consumed by `cultivate`; there is no middle skill.
- A bespoke CLI. Distribution stays on the `vercel-labs/skills` CLI.
- Alternate skill formats (Anthropic Skills, Cursor rules, etc.). SKILL.md is
  the unit.
- Multi-language/i18n support.
- Hosted registry / discovery beyond GitHub + `npx skills add`.

## Stack

- **SKILL.md + YAML frontmatter** is the unit of distribution. Frontmatter uses
  folded block scalars so descriptions with colons parse cleanly.
- **Python 3** powers repo-level tooling: `validate_skills.py`,
  `run_skill_evals.py`, `format_eval_summary.py`.
- **GitHub Actions** runs evals per PR and posts a sticky comment with results.
- **Distribution**: `vercel-labs/skills` CLI (`npx skills add s33dunda/skills`).
- **Eval runner**: invokes the `claude` CLI in CI; gracefully degrades when the
  binary is unavailable so the runner does not crash on misconfiguration.

## Agents

Agents working *in* this repo are expected to use Anthropic's `skill-creator`
skill to continuously iterate on the skills housed here. Concrete surfaces:

- Author new skills from a brief (respecting SKILL.md frontmatter rules and the
  folded-scalar convention for descriptions).
- Refine existing skill prose and reference material.
- Keep evals current; write new eval prompts as skills evolve.
- Maintain cross-skill consistency: naming, frontmatter shape, `references/`
  vs `scripts/` vs `assets/` layout.
- Review and reconcile drift between SKILL.md instructions and actual tool
  behavior (e.g. artifact filename conventions).

Agents consuming skills downstream (farmers) are out of scope for *this* repo's
agent surface; that's whatever codebase `cultivate` was pointed at.

## Success

v1 is shipped when all of the following are observably true:

- `npx -y skills@latest add s33dunda/skills` installs both skills into Augment
  and Claude Code without errors.
- Skill eval CI runs on every PR, posts a sticky comment with per-eval
  pass/fail, and stays green on `main`.
- The workflow has been exercised end-to-end at least once on a real project:
  `plot` -> `seed.md` -> `cultivate` -> agent-driven PRs merged.
- README clearly communicates the agricultural flow and both skills are listed
  (currently only `cultivate` is listed -- drift to fix).

## Constraints

- Solo maintainer (s33dunda).
- Upstream dependency on the `vercel-labs/skills` CLI: frontmatter format,
  discovery rules, and search paths follow its conventions. Breaking changes
  upstream can break install.
- Eval CI depends on the `claude` CLI binary being available in the GitHub
  Actions runner; must degrade gracefully when it isn't.

## Open Questions

- **Plot output filename drift.** `skills/plot/SKILL.md` instructs agents to
  write `plot.md`, but the intended artifact is `seed.md`. The plot skill's
  own SKILL.md and references need updating to match.
- **Release / versioning.** No story yet for how consumers learn that a skill
  changed (no `version` frontmatter, no changelog convention). Decide before
  cultivate consumers start pinning.
- **`cultivate` entry point from `seed.md`.** The cultivate skill currently
  audits a live repo but doesn't explicitly document consuming a `seed.md`.
  The handoff needs to be specified.
- **README drift.** Root README lists only `cultivate` and references an old
  Codex-specific installer; needs rewriting for the `skills` CLI path and to
  list `plot`.
- **Eventual additional skills.** Is there a third skill (e.g. `harvest` to
  convert a proven agent-ready repo into a template)? Out of scope for v1 but
  worth noting so naming stays in the agricultural metaphor.
