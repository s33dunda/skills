---
name: skills
tagline: "A skill suite that turns an idea into an agent-ready repo via a repeatable plot -> cultivate workflow."
stack: [Markdown, YAML, Python]
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
  architectural guardrails, lint/test feedback exposure.
- Installable for any supported agent via `npx skills add s33dunda/skills`.
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
- **Python 3** powers repo-level tooling: `validate_skills.py` and its unit
  tests. `uv` is the declared runner for isolated invocations (`uv.lock` +
  `pyproject.toml`); stdlib `python3` remains supported for validator calls.
- **Distribution**: `vercel-labs/skills` CLI (`npx skills add s33dunda/skills`).

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
- The workflow has been exercised end-to-end at least once on a real project:
  `plot` -> `seed.md` -> `cultivate` -> agent-driven PRs merged.
- README clearly communicates the agricultural flow and both skills are listed.

## Constraints

- Solo maintainer (s33dunda).
- Upstream dependency on the `vercel-labs/skills` CLI: frontmatter format,
  discovery rules, and search paths follow its conventions. Breaking changes
  upstream can break install.
- No paid CI budget. Validator and validator-unit-tests run locally only;
  model-backed skill evals are deferred (see `Deferred` below).

## Open Questions

- **Eventual additional skills.** Is there a third skill (e.g. `harvest` to
  convert a proven agent-ready repo into a template)? Out of scope for v1 but
  worth noting so naming stays in the agricultural metaphor.

## Deferred

- **Skill eval CI.** Originally in scope; removed because model-backed evals
  require an `ANTHROPIC_API_KEY` budget the solo maintainer cannot currently
  justify. Prompts remain in each skill's `evals/evals.json` for local /
  manual runs; the runner and Actions workflow have been removed from the
  repo. Reinstate when there is a CI budget or a free equivalent path.

## Resolved Since Plot

- Plot output filename drift -- plot now produces `seed.md` (commit 6d42dcd).
- Cultivate entry point from `seed.md` -- documented and anchored in harness
  engineering (commit 339f411).
- README drift -- root README rewritten to list both skills and use the
  `skills` CLI; `skills/README.md` follows in the same pass.
- Release / versioning -- `version` frontmatter (semver) is now required by
  the validator; each skill has a `CHANGELOG.md` seeded at 0.1.0.
- ExecPlan workflow installed -- `docs/PLANS.md` convention + 12-section
  `docs/plans/_template.md` mirror cultivate's canonical template.
- Environment isolation -- `pyproject.toml` + `uv.lock` declare the repo's
  runner; agents no longer depend on a global `python3`.
- PR/issue templates -- `.github/pull_request_template.md` and
  `.github/ISSUE_TEMPLATE/` ask contributors for acceptance criteria and
  validation evidence.
