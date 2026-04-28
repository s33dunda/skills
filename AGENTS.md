# Agent Guide

## Orientation

This repository is a monorepo of installable `SKILL.md` packages. The workflow is `plot -> seed.md -> cultivate -> farmers`; this repo houses the `plot` and `cultivate` skills themselves. Distribution is via the [`vercel-labs/skills`](https://github.com/vercel-labs/skills) CLI.

Start with `README.md` for human setup and install paths, `seed.md` for project identity and scope, and this file for agent workflow.

## Useful Commands

- Validate skill packaging: `uv run python scripts/validate_skills.py`
- Run validator unit tests: `uv run python -m unittest scripts.test_validate_skills`
- Audit harness gaps: `uv run python skills/cultivate/scripts/audit_cultivate.py .`
- Sync the locked environment: `uv sync`
- Full verify: `uv run python scripts/validate_skills.py && uv run python -m unittest scripts.test_validate_skills`
- Install a skill into Codex: `python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo s33dunda/skills --path skills/<skill-name>`

The repo is stdlib-only Python; `uv.lock` + `pyproject.toml` declare the runner so agents never fall back to a global interpreter. Bare `python3` is acceptable only when `uv` is unavailable.

## Repository Map

- `skills/`: installable skill directories (`plot`, `cultivate`). Each carries `SKILL.md`, `references/`, `scripts/`, `evals/`, `CHANGELOG.md`.
- `skills/README.md`: human-facing skill index.
- `scripts/validate_skills.py`: frontmatter / metadata / Python-syntax gate for every skill.
- `scripts/test_validate_skills.py`: stdlib unittest fixtures for the validator.
- `docs/PLANS.md` + `docs/plans/_template.md`: ExecPlan convention and skeleton.
- `docs/exec-plans/active/`: active ExecPlans. `docs/exec-plans/completed/`: closed plans.
- `docs/exec-plans/tech-debt-tracker.md`: long-lived cleanup items.
- `ARCHITECTURE.md`: system purpose, flows, boundaries, enforcement.
- `.github/pull_request_template.md` + `.github/ISSUE_TEMPLATE/`: PRs and issues must supply acceptance criteria and validation evidence.
- `seed.md`: project identity, scope, success criteria, deferrals.

## Deeper Context

- Harness engineering canon: `skills/cultivate/references/harness-engineering.md`, `skills/cultivate/references/cultivate-principles.md`.
- Canonical templates (AGENTS.md / PLANS.md / audit report): `skills/cultivate/references/templates.md`.
- BMAD elicitation (source of `plot`'s method CSV): `skills/plot/references/bmad-elicitation.md`.
- Seed schema: `skills/plot/references/seed-schema.md`.

## Execution Plans

Open an ExecPlan at `docs/exec-plans/active/<slug>.md` when work (a) touches more than one skill, (b) changes `SKILL.md` plus its references plus its evals in the same effort, or (c) will span multiple agent sessions. Convention: `docs/PLANS.md`. Template: `docs/plans/_template.md`. Move to `docs/exec-plans/completed/` when done. Resolve ambiguity autonomously; record decisions in the plan's `Decision Log`. Single-file changes do not need a plan.

## When Writing or Editing a Skill

- Run `uv run python scripts/validate_skills.py` after every change to `SKILL.md` frontmatter, every new/edited Python helper, and every `evals/evals.json` edit.
- Bump the `version` field in `SKILL.md` frontmatter and add a matching `CHANGELOG.md` entry. Patch for prose/reference fixes; minor for added capabilities; major for breaking `SKILL.md` interface changes.
- Keep `SKILL.md` lean. Long-form guidance belongs in `references/`; deterministic logic belongs in `scripts/`.
- When adding or reshaping elicitation methods in `plot`, update `skills/plot/references/bmad-elicitation.md` in the same commit. The CSV and its theory-of-use travel together.
- Prefer existing patterns in peer skills over introducing new layouts.

## When Reviewing a PR

- Run the `Full verify` command above.
- Confirm the PR template's `Acceptance criteria` section has observable, mechanical items (a `[command] exits 0` or `audit flips X -> present`, not "feels cleaner").
- Confirm `Validation evidence` shows actual command output, not claims of output.
- Confirm the `ExecPlan reference` field is either linked or explicitly marked `n/a`.
- Check the diff against the `Definition of Done` below.

## Definition of Done

A task is complete when ALL of the following hold:

1. `uv run python scripts/validate_skills.py` exits 0.
2. `uv run python -m unittest scripts.test_validate_skills` reports all tests OK.
3. If a skill's behavior changed: its `version` is bumped and `CHANGELOG.md` has a matching entry.
4. If the cultivate audit was red for a gap this task intended to close: `uv run python skills/cultivate/scripts/audit_cultivate.py .` shows that gap as `present` (or, for `CI workflows`, still `missing` by design per `seed.md` `## Deferred`).
5. No new files outside the documented layout (`skills/*`, `scripts/`, `docs/`, `.github/`, root `AGENTS.md` / `README.md` / `seed.md` / `pyproject.toml` / `uv.lock`).

## When Blocked

- If the validator fails after 3 attempts at a targeted fix: stop, paste the full `validate_skills.py` output into the PR or handoff, and mark the gap in `Unresolved`.
- If the audit regresses (a previously-present gap flips to `missing`): treat it as a blocker; do not commit until understood or intentionally recorded in `seed.md` `## Deferred`.
- If a required file or helper does not exist: record it under `Unresolved` and proceed with the smallest reversible alternative. Do not silently invent a new layout.
- If an elicitation method appears to be missing for `plot`'s Smart Selection: log the gap in `skills/plot/references/bmad-elicitation.md` rather than adding a method mid-run.

## Never

- Delete `evals/evals.json` to make the validator pass. Fix the eval or fix the prompt.
- Commit a `SKILL.md` change without a `version` bump and matching `CHANGELOG.md` entry.
- Force-push to `main`.
- Edit `skills/plot/methods.csv` without also updating `skills/plot/references/bmad-elicitation.md`.
- Add a new top-level directory or skill without a `SKILL.md` that the validator accepts.
- Commit credentials, tokens, or `.env` contents. `.env` and variants are gitignored; keep them that way.
- Introduce a network call into a skill's bundled Python helpers. Helpers are deterministic and offline.

## Working Norms

Keep each skill self-contained. Put reusable guidance in `references/`, deterministic helpers in `scripts/`, templates/assets in `assets/`, and test prompts in `evals/`. The core guardrail is installability: every skill directory must have matching `name` frontmatter, a non-empty `description`, valid eval metadata when present, and syntactically valid Python helpers. If a rule starts repeating across PRs, encode it as a test, validator check, or audit signal rather than restating it here.
