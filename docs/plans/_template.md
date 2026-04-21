# ExecPlan: <short descriptive title>

## Purpose / Big Picture

One or two paragraphs. Why this work exists, what the user-visible outcome is, and what success looks like in plain language.

## Context and Orientation

- Repository areas touched: `skills/...`, `scripts/...`, `docs/...`
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

- [ ] `python3 scripts/validate_skills.py` exits 0.
- [ ] `python3 -m unittest scripts.test_validate_skills` exits 0.
- [ ] [other observable, e.g. "audit_cultivate.py flips `execution-plan workflow` from missing to present"].

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
