# Execution Plans

Complex work on this repo (multi-milestone, cross-cutting, or expected to span more than one agent session) runs against an ExecPlan checked in under `docs/exec-plans/active/<slug>.md`.

## When to write one

- The change touches more than one skill or more than one concern (e.g. `SKILL.md` + evals + references + `CHANGELOG.md` in a single effort).
- Acceptance requires more than one observable signal.
- The work will span multiple agent sessions and a fresh agent will need to resume from the plan plus the working tree.
- There is risk of destructive or hard-to-reverse steps (breaking changes to a skill's public shape, eval contract changes, CI reshuffles).

Small, single-file changes do not need an ExecPlan.

## How to write one

Copy `docs/plans/_template.md` to `docs/exec-plans/active/<slug>.md`. Keep the plan current as work proceeds:

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
