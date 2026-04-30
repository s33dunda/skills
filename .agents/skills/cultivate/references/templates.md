# Cultivate Repo Templates

Use these templates as starting points. Keep them small and adapt them to the repository after inspection.

## Harness Knowledge Store Layout

This layout comes from `references/harness-openai-blog.md`. Install it by default unless the repository already has an explicit, better-localized convention. Scale content down for small repos, but keep the map stable so future agents know where to put new knowledge.

```text
AGENTS.md
ARCHITECTURE.md
docs/
├── design-docs/
│   ├── README.md
│   ├── index.md
│   └── core-beliefs.md
├── exec-plans/
│   ├── active/
│   │   └── README.md
│   ├── completed/
│   │   └── README.md
│   └── tech-debt-tracker.md
├── generated/
│   └── README.md
├── product-specs/
│   ├── README.md
│   └── index.md
├── references/
│   └── README.md
├── PLANS.md
├── QUALITY.md
├── RELIABILITY.md
└── SECURITY.md
```

Optional, install when relevant:

- `docs/DESIGN.md` for visual/product design principles.
- `docs/FRONTEND.md` for UI implementation rules, routes, screenshots, accessibility, and browser-driven validation.
- `docs/PRODUCT_SENSE.md` for product taste, target users, and prioritization heuristics.

For directories with no real content yet, add a short `README.md` explaining when to create files there. Do not leave empty directories; git will drop them and agents will miss the intended home for future context.

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

- Architecture: `ARCHITECTURE.md`
- Plans convention: `docs/PLANS.md`
- Quality and verification: `docs/QUALITY.md`
- Reliability: `docs/RELIABILITY.md`
- Security boundaries: `docs/SECURITY.md`
- Product specs: `docs/product-specs/index.md`
- Design docs: `docs/design-docs/index.md`
- Active ExecPlans: `docs/exec-plans/active/`
- Tech debt: `docs/exec-plans/tech-debt-tracker.md`
- External references: `docs/references/`

## Execution Plans

- Use `docs/PLANS.md` for multi-file, cross-cutting, or multi-session work.
- Put active plans in `docs/exec-plans/active/` and move completed plans to `docs/exec-plans/completed/`.

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

The `Deeper Context` section is not optional once those docs exist. A thin AGENTS file that mentions only `README.md`, `ARCHITECTURE.md`, or `docs/PLANS.md` is a weak cultivate application when the richer knowledge-store docs are present.

### Nested `AGENTS.md` (monorepos)

In a monorepo, nest per service or package. In a large single-package repo, nest for the high-leverage local surfaces that have different norms: implementation package, tests, docs/examples, generated-code, apps, packages, or services. Tools concatenate from repo root to the current working directory, so deeper files extend (not replace) the root. In Codex specifically, `AGENTS.override.md` at any level replaces parent instructions -- reserve it for release freezes, incident mode, or paths with elevated security constraints.

```text
/repo/AGENTS.md                            -- project-wide rules
  /repo/src/AGENTS.md                      -- implementation-local rules
  /repo/tests/AGENTS.md                    -- regression and fixture rules
  /repo/docs_src/AGENTS.md                 -- runnable docs/examples rules
  /repo/services/AGENTS.md                 -- service defaults
    /repo/services/api/AGENTS.md           -- API-specific rules
    /repo/services/payments/AGENTS.override.md  -- Codex: replaces parent
```

Nested files should stay short and operational. Use this shape:

```md
# [Subtree] Guide

## Scope

This subtree owns [implementation/tests/docs/examples/etc.].

## Working Norms

- Keep changes close to the existing local flow that owns the behavior.
- Prefer nearby patterns before introducing new helpers, fixtures, or surfaces.
- [One or two repo-specific local rules.]

## Validation

- Pair changes here with [nearest test/docs/generated-artifact command or expectation].
- Run the smallest relevant check first, then the root Definition of Done when finishing.
```

For study treatments, a large repo with only a root `AGENTS.md` is a weak application unless the audit explains why local subtree guidance would not change behavior.

### Canonical -> tool-specific files

`AGENTS.md` is the open standard read natively by Codex, Copilot, Cursor, Windsurf, Amp, and Devin. If a team also uses `CLAUDE.md` (Claude Code) or `.cursor/rules`, treat `AGENTS.md` as canonical and mirror to the others -- do not maintain parallel instruction sets that drift.

## Root `ARCHITECTURE.md`

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

## `docs/design-docs/README.md`

```md
# Design Docs

Use this directory for durable design reasoning: core beliefs, accepted and rejected approaches, verification notes, and decision history that agents should preserve across PRs.

Create a new document here when a design choice affects more than one file, changes how future agents should think, or records a tradeoff that would otherwise live only in chat. Link each document from `index.md`.
```

## `docs/design-docs/index.md`

```md
# Design Docs Index

| Doc | Status | Last Verified | Why It Matters |
| --- | --- | --- | --- |
| `core-beliefs.md` | draft | YYYY-MM-DD | Agent-first principles and repository taste. |
```

## `docs/design-docs/core-beliefs.md`

```md
# Core Beliefs

- The repository is the system of record; facts that matter to future agents belong in versioned files.
- `AGENTS.md` is a map, not a manual.
- Repeated rules should become tests, linters, schemas, or scripts with remediation-aware messages.
- Small, reversible changes beat large undocumented rewrites.
```

## `docs/product-specs/README.md`

```md
# Product Specs

Use this directory for user-facing behavior, workflows, acceptance criteria, and product decisions. Product specs answer "what should happen for the user?" while `ARCHITECTURE.md` answers "where does it live in the system?"

Add or update a spec when behavior changes, a new user journey is introduced, or an old assumption becomes wrong. Link specs from `index.md`.
```

## `docs/product-specs/index.md`

```md
# Product Specs Index

| Spec | Status | Owner | Verification |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |
```

## `docs/generated/README.md`

```md
# Generated Docs

Use this directory for facts generated from code, schemas, APIs, command inventories, or external systems. Every generated file should say how to regenerate it and what command verifies freshness.

Do not hand-edit generated artifacts unless the file explicitly says it is safe.
```

## `docs/references/README.md`

```md
# References

Use this directory for external references that agents need locally: LLM-readable upstream docs, protocol notes, design-system references, deployment docs, or vendor constraints.

Prefer small, task-relevant excerpts or generated `*-llms.txt` snapshots over huge copied manuals. Record the source URL and retrieval date at the top of each reference when possible.
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

## `docs/RELIABILITY.md`

```md
# Reliability

## Critical Journeys

List the user or system journeys that must remain reliable.

## Failure Modes

Document known failure modes, retries, rate limits, backoff behavior, and recovery commands.

## Validation

Name exact commands, health checks, logs, metrics, or traces agents can use to prove reliability.
```

## `docs/SECURITY.md`

```md
# Security

## Secrets And Credentials

Document where secrets come from, which files must never contain them, and the command or check that helps catch leaks.

## Trust Boundaries

Name external systems, user-controlled inputs, auth scopes, and dangerous operations.

## Safe Change Rules

List actions that require explicit human approval, feature flags, or additional review.
```

## `docs/PLANS.md`

Use an ExecPlan for multi-hour, multi-milestone, or cross-cutting work. Small changes get an ephemeral plan or no plan. The skeleton below is the one-file-per-plan canonical shape from the OpenAI cookbook. Copy it into `docs/exec-plans/active/<slug>.md` for each new effort; move it to `docs/exec-plans/completed/<slug>.md` when complete. `docs/PLANS.md` itself is the index and convention doc.

`docs/PLANS.md` (convention doc):

```md
# Execution Plans

Complex work (multi-milestone, cross-cutting, or expected to span more than one agent session) runs against an ExecPlan checked into this repo under `docs/exec-plans/active/<slug>.md`.

## When to write one

- The change touches more than one subsystem.
- Acceptance requires more than one observable signal.
- The work will span multiple agent sessions.
- Risk of destructive or hard-to-reverse steps (migrations, schema changes, rollouts).

Small, single-file changes do not need an ExecPlan.

## How to write one

Copy the template below to `docs/exec-plans/active/<slug>.md`. Keep the plan current as work proceeds:

- Update `Progress` at every stopping point.
- Record decisions in the `Decision Log` as they are made, not after the fact.
- Record unexpected findings in `Surprises & Discoveries`.
- Close each major milestone with an `Outcomes & Retrospective` entry.

## Plan lifecycle

- New plans live in `docs/exec-plans/active/`.
- Completed plans move to `docs/exec-plans/completed/`.
- Long-lived cleanup and recurring drift are tracked in `docs/exec-plans/tech-debt-tracker.md`.

## Non-interactivity

Do not prompt the operator for "next steps" mid-plan. Resolve ambiguity autonomously, record the choice in the `Decision Log`, and continue to the next milestone.
```

Per-effort ExecPlan skeleton:

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
