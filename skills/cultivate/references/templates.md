# Cultivate Repo Templates

Use these templates as starting points. Keep them small and adapt them to the repository after inspection.

## Root `AGENTS.md`

Keep each section under ~50 lines and the total file under ~150. Codex enforces a default 32 KiB limit (`project_doc_max_bytes`); long files get truncated. Front-load commands and closure; push style preferences to referenced docs.

```md
# Agent Guide

## Orientation

This repository contains [brief purpose]. Start with `README.md` for human setup and this file for agent workflow.

## Useful Commands

- Install: `[command]`
- Test: `[command]` (Python example: `uv run pytest -v`)
- Lint: `[command]` (Python examples: `uv run ruff check`, `uv run mypy`)
- Format: `[command]` (Python example: `uv run ruff format`)
- Start locally: `[command]`
- Full verify: `[command chain, e.g. uv run ruff check && uv run pytest]`

## Repository Map

- `src/`: [main application/library code]
- `tests/`: [test suite]
- `docs/`: [architecture, product, and operational notes]
- `.github/workflows/`: [CI definitions]

## Deeper Context

- Architecture: `docs/ARCHITECTURE.md`
- Quality and verification: `docs/QUALITY.md`
- Complex work plans: `docs/PLANS.md`

## When Writing Code

- Run the relevant check after every file change (e.g. `uv run ruff check`).
- Add tests for new behavior; the test command is named above.
- Prefer existing patterns in `src/` over introducing new ones.

## When Reviewing Code

- Run the full verify command above.
- Confirm new behavior is covered by a test.
- Check the diff against the `Definition of Done` below.

## Definition of Done

A task is complete when ALL of the following hold:

1. `[test command]` exits 0.
2. `[lint command]` exits 0.
3. Changed files match the architecture boundaries in `docs/ARCHITECTURE.md`.
4. [any project-specific observable behavior, e.g. `curl localhost:8080/health` returns 200].

## When Blocked

- If tests fail after 3 attempts: stop, report the failing test with full output, and flag it in the handoff.
- If a dependency is missing: check the package manifest first, then name the gap rather than installing silently.
- If a required file or command is absent: record the gap as `Unresolved` and proceed with the smallest reversible alternative.

## Never

- Delete files to resolve errors.
- Force-push to shared branches.
- Skip or disable failing tests to get to green.
- Commit credentials, tokens, or secrets.

## Working Norms

Read the relevant docs before changing a subsystem. Prefer existing patterns and run the narrowest useful check before finishing. If a repeated rule matters, encode it in a test, lint, schema, or script rather than only adding prose.
```

### Nested `AGENTS.md` (monorepos)

In a monorepo, nest per service or package. Tools concatenate from repo root to the current working directory, so deeper files extend (not replace) the root. In Codex specifically, `AGENTS.override.md` at any level replaces parent instructions -- reserve it for release freezes, incident mode, or paths with elevated security constraints.

```text
/repo/AGENTS.md                            -- project-wide rules
  /repo/services/AGENTS.md                 -- service defaults
    /repo/services/api/AGENTS.md           -- API-specific rules
    /repo/services/payments/AGENTS.override.md  -- Codex: replaces parent
```

### Canonical -> tool-specific files

`AGENTS.md` is the open standard read natively by Codex, Copilot, Cursor, Windsurf, Amp, and Devin. If a team also uses `CLAUDE.md` (Claude Code) or `.cursor/rules`, treat `AGENTS.md` as canonical and mirror to the others -- do not maintain parallel instruction sets that drift.

## `docs/ARCHITECTURE.md`

```md
# Architecture Map

## Purpose

Explain the system in terms a new agent can use to navigate the codebase safely.

## Main Flows

Describe the most important request, job, UI, or data flows. Name the files or modules where each flow begins and ends.

## Boundaries

List the architectural boundaries that matter. Include dependency direction, allowed imports, data ownership, or integration boundaries.

## Extension Points

Describe where new behavior should be added and which existing helpers or patterns to reuse.

## Mechanical Enforcement

List checks that enforce this architecture. If none exist, say which rule should be promoted into tooling first.
```

## `docs/QUALITY.md`

```md
# Quality And Verification

## Standard Checks

- Tests: `[command]` (Python example: `uv run pytest`)
- Lint/type checks: `[command]` (Python examples: `uv run ruff check`, `uv run mypy`)
- Build: `[command]`

## Critical User Journeys Or Behaviors

List the behaviors that must keep working and how an agent can verify them.

## Observability And Debugging

Document useful logs, metrics, traces, health endpoints, or debugging scripts.

## Known Gaps

Track missing checks, flaky tests, stale generated files, and areas where agents need human judgment.
```

## `docs/PLANS.md`

Use an ExecPlan for multi-hour, multi-milestone, or cross-cutting work. Small changes get an ephemeral plan or no plan. The skeleton below is the one-file-per-plan canonical shape from the OpenAI cookbook. Copy it into `docs/plans/<slug>.md` (or `.agent/plans/<slug>.md`) for each new effort; `docs/PLANS.md` itself is the index and convention doc.

`docs/PLANS.md` (convention doc):

```md
# Execution Plans

Complex work (multi-milestone, cross-cutting, or expected to span more than one agent session) runs against an ExecPlan checked into this repo under `docs/plans/<slug>.md`.

## When to write one

- The change touches more than one subsystem.
- Acceptance requires more than one observable signal.
- The work will span multiple agent sessions.
- Risk of destructive or hard-to-reverse steps (migrations, schema changes, rollouts).

Small, single-file changes do not need an ExecPlan.

## How to write one

Copy `docs/plans/_template.md` to `docs/plans/<slug>.md`. Keep the plan current as work proceeds:

- Update `Progress` at every stopping point.
- Record decisions in the `Decision Log` as they are made, not after the fact.
- Record unexpected findings in `Surprises & Discoveries`.
- Close each major milestone with an `Outcomes & Retrospective` entry.

## Non-interactivity

Do not prompt the operator for "next steps" mid-plan. Resolve ambiguity autonomously, record the choice in the `Decision Log`, and continue to the next milestone.
```

`docs/plans/_template.md` (per-effort ExecPlan skeleton):

```md
# ExecPlan: <short descriptive title>

## Purpose / Big Picture

One or two paragraphs. Why this work exists, what the user-visible outcome is, and what success looks like in plain language.

## Context and Orientation

- Repository areas touched: `src/...`, `tests/...`, `docs/...`
- Prior art in this repo: [links or file paths]
- External references: [RFCs, tickets, upstream docs]
- Starting state assumptions: [branch, env, data]

## Interfaces and Dependencies

- Upstream (inputs): services, APIs, data sources this plan relies on.
- Downstream (outputs): consumers that will see behavior changes.
- Blockers and required coordination: [teams, credentials, feature flags].

## Plan of Work

Milestones, in order. Each milestone is a slice that lands a shippable behavior or an observable checkpoint.

1. Milestone A -- [one-line description]
2. Milestone B -- [one-line description]
3. Milestone C -- [one-line description]

## Concrete Steps

For each milestone, the specific file-level or command-level actions. Keep steps small enough that a fresh agent can pick one up and run it.

### Milestone A

- [ ] Step A.1 -- [exact change or command]
- [ ] Step A.2 -- [exact change or command]

### Milestone B

- [ ] Step B.1 -- [exact change or command]

## Validation and Acceptance

Phrase acceptance as observable behavior, not internal attributes.

- [ ] `[test command]` exits 0.
- [ ] `[lint command]` exits 0.
- [ ] After starting the service, `curl localhost:8080/health` returns `200 OK` with body `{"status":"ok"}`.
- [ ] [other observable, e.g. "new row appears in `audit_log` within 1s of request"].

## Idempotence and Recovery

- How to re-run any step safely (which steps are idempotent, which are not).
- How to roll back each milestone if it goes wrong.
- Known side effects (writes to external systems, caches, queues).

## Progress

Append-only log of stopping points. A future agent should be able to resume from the latest entry.

- YYYY-MM-DD: [what was completed, current branch, next step].

## Surprises & Discoveries

Append-only. Findings that were not predicted by the plan and that change how the work should proceed.

- YYYY-MM-DD: [finding, why it matters, what changed in the plan].

## Decision Log

Append-only. Decisions made during execution, including ambiguities resolved without operator input.

- YYYY-MM-DD: Decided [X] over [Y] because [reason]. Alternatives considered: [Z].

## Outcomes & Retrospective

Filled in as each milestone closes.

- Milestone A closed YYYY-MM-DD: outcome [observed result], deviations from plan [list], follow-ups [links].

## Artifacts and Notes

Links to PRs, screenshots, traces, log excerpts, or scratch notes produced during the work.
```

## Cultivate Audit Report

Cultivate runs non-interactively. Audit reports always finish the run and expose open items as `Unresolved`, never as mid-run questions back to the operator.

```md
# Cultivate Audit

## Current State

Summarize what exists today: orientation files, docs layout, CI signals, existing `AGENTS.md` / `CLAUDE.md` / `PLANS.md`, and what agent responsibilities the repo declares (from `seed.md` if present, or inferred from the working tree).

## Gaps By Category

- Orientation (AGENTS.md command-first, Definition of Done, When Blocked, Never list, size budget):
- Knowledge system (ARCHITECTURE.md, QUALITY.md, discoverability, cross-links):
- Enforceable rules (lint, tests, schemas, scripts with remediation messages):
- Validation feedback (named commands, exit-code based closure, CI wiring):
- Autonomy workflow (ExecPlan template, living-document discipline, nested AGENTS.md for monorepos):
- Entropy control (stale docs, duplicated helpers, drift from stated architecture).

## Top Gaps By Leverage

Rank the gaps above by expected impact on agent effectiveness. Cite the harness principle each gap maps to.

## Recommended First Improvements

The smallest changes that would most raise agent leverage, in priority order. For each: the change, the principle it invokes, and the check that will confirm it landed.

## Unresolved

- Assumptions the audit made (especially where `seed.md` and the working tree disagree, or where the repo's declared agent responsibilities were inferred rather than stated).
- Interpretations chosen and the alternatives rejected.
- Repo questions worth confirming on the next pass (but not blocking this report).

## Verification

Checks run during the audit, with observed results. Missing validation paths are called out explicitly as cultivate gaps.
```
