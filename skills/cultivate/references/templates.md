# Cultivate Repo Templates

Use these templates as starting points. Keep them small and adapt them to the repository after inspection.

## Root `AGENTS.md`

```md
# Agent Guide

## Orientation

This repository contains [brief purpose]. Start with `README.md` for human setup and this file for agent-specific workflow.

## Useful Commands

- Install dependencies: `[command]`
- Run tests: `[command]`
- Run lint/type checks: `[command]`
- Start locally: `[command]`
- Python environment: prefer `uv run ...` when this repo uses `uv.lock` or declares `uv` in its setup docs.

## Repository Map

- `src/`: [main application/library code]
- `tests/`: [test suite]
- `docs/`: [architecture, product, and operational notes]
- `.github/workflows/`: [CI definitions]

## Deeper Context

- Architecture: `docs/ARCHITECTURE.md`
- Quality and verification: `docs/QUALITY.md`
- Complex work plans: `docs/PLANS.md`

## Working Norms

Read the relevant docs before changing a subsystem. Prefer existing patterns and run the narrowest useful check before finishing. If a repeated rule matters, encode it in a test, lint, schema, or script rather than only adding prose.
```

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

```md
# Execution Plans

Use an execution plan for multi-step features, risky refactors, cross-cutting changes, or work expected to span more than one agent session.

An execution plan should include:

- Goal and user-visible outcome.
- Repository context and files likely to change.
- Milestones with progress checkboxes.
- Decisions and why they were made.
- Validation commands and expected results.
- Recovery notes for future agents.

Keep the plan current as work proceeds. A future agent should be able to resume from the plan plus the current working tree.
```

## Cultivate Audit Report

```md
# Cultivate Audit

## Current State

Summarize what exists today.

## Gaps By Category

- Orientation:
- Knowledge system:
- Enforceable rules:
- Validation feedback:
- Autonomy workflow:
- Entropy control:

## Recommended First Improvements

List the smallest changes that would most improve agent effectiveness.

## Verification

Describe checks run during the audit and any missing validation paths.
```
