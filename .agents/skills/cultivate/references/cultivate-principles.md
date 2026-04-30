# Cultivate Engineering Principles

This reference distills harness engineering into repository practices an agent can apply. The full canon lives in `harness-engineering.md`; read this file when you need the operational shortlist.

## Core Idea

A coding agent is only as effective as the environment it can observe and act inside. Human time is scarce, so invest in repository structure, tools, checks, and feedback loops that let agents make progress without asking humans to copy context into prompts.

Humans steer. Agents execute. The repository is the system of record.

## Principles

### Give Agents A Map, Not A Manual

Keep the root `AGENTS.md` short. It should orient the agent and point to deeper sources of truth. A giant all-purpose instruction file competes with task context, hides priorities, and grows stale.

### Make The Repo The System Of Record

If future agents need to know a decision, constraint, workflow, or domain fact, put it in versioned repository files. External documents, chat threads, and tacit human knowledge are invisible during most agent runs.

### Use Progressive Disclosure

Start with a small entrypoint, then link to focused docs by topic. Agents should be able to load only the context needed for the task at hand.

### Enforce Architecture Mechanically

Documentation helps, but repeated rules should become tests, linters, schema checks, or CI jobs. Enforce boundaries and invariants centrally while leaving local implementation freedom. When you write a custom lint, put the remediation instructions in the error message -- the violation becomes useful context for the next agent run.

### Parse At The Boundary

Data entering the system should be parsed into typed shapes once, at the edge. Downstream code should never probe or guess at external shapes. This prevents agents from replicating uncertain assumptions across the codebase.

### Prefer Boring, Legible Dependencies

Favor technologies with stable APIs, composable semantics, and strong representation in training data. Sometimes it is cheaper to reimplement a small, tightly integrated helper with full test coverage than to wrap an opaque upstream library.

### Make Validation Agent-Legible

Agents need direct feedback. Prefer commands, logs, metrics, traces, screenshots, health checks, and reproducible workflows that an agent can run and interpret. The more of the running application an agent can inspect programmatically, the more autonomy the harness can safely grant.

### Treat Plans As First-Class Artifacts

For long or risky work, use checked-in execution plans with progress, decisions, acceptance criteria, and validation evidence. A plan should let a future agent resume without hidden context.

### Capture Taste Once, Apply Continuously

When review feedback repeats, encode it in docs or tooling. If the same issue keeps appearing in agent PRs, the cultivate is missing a rule, template, test, or feedback loop.

### Agent Struggle Is Environment Signal

When an agent repeatedly fails at a task, the reflex is not "try harder" or "have a human write it." It is: what capability, tool, guardrail, doc, or abstraction is missing, and how do we encode it so the agent can do it next time? Each fix becomes infrastructure for all future runs.

### Run Continuous Garbage Collection

Agent-generated code tends to replicate local patterns, including weak ones. Schedule or prompt periodic cleanup passes for stale docs, duplicated helpers, drift from architecture, flaky tests, and quality gaps. Technical debt behaves like a high-interest loan -- pay it down continuously rather than in painful bursts.

### Match Merge Philosophy To Throughput

When agent throughput outpaces human attention, corrections are cheap and waiting is expensive. Favor short-lived PRs, minimal blocking gates, and agent-to-agent review. This tradeoff only holds under strong architectural guardrails -- without them, cheap corrections compound into drift.

### Write Command-First, Not Prose-First

Every rule in `AGENTS.md` should map to an exact shell invocation whose exit code is the check. Replace "run the tests" with a named command. Replace "follow our style" with the linter invocation. Style guidance with no enforcement command is routinely ignored; style guidance with a one-line `ruff check` command is not.

### Make Closure Explicit

Include a `Definition of Done` in `AGENTS.md` and in every ExecPlan. Name the specific exit codes, HTTP responses, or observable behaviors that prove a task is complete. "I think I'm done" is the default failure mode for unsupervised agents; explicit closure criteria eliminate it.

### Organize Instructions By Task

Prefer `When Writing Code` / `When Reviewing` / `When Releasing` sections over flat style lists. Task-organized files let the agent pull only the rules relevant to the current turn. Flat lists force every rule to be parsed on every task, which is how instructions fall out of context on long runs.

### Name The Never List

Destructive recovery is the most expensive failure mode. When blocked, agents invent -- deleting lockfiles, force-pushing, bypassing tests, skipping validation. A short `Never` list in `AGENTS.md` (paired with concrete `When Blocked` escalation paths) prevents the class of failure the `Unresolved` report can't undo.

### Respect The Size Budget

Keep `AGENTS.md` under ~150 lines total and each section under ~50. Codex enforces a default 32 KiB limit (`project_doc_max_bytes`) and content beyond it is truncated. Front-load commands and closure; push style preferences and historical rationale to referenced docs.

### Use Nested AGENTS.md For Monorepos

Root `AGENTS.md` for project-wide rules; service or package `AGENTS.md` for local conventions. Tools concatenate from root to the working directory. In Codex, `AGENTS.override.md` replaces parent instructions -- reserve it for release freezes, incident mode, or paths with elevated security constraints.

### ExecPlans Are Living Documents

For multi-milestone or multi-hour work, use an ExecPlan with the mandatory sections (`Purpose`, `Progress`, `Surprises & Discoveries`, `Decision Log`, `Outcomes & Retrospective`, plus context/plan/steps/validation). Update the plan as work proceeds; resolve ambiguities inline and record them in the Decision Log rather than stopping.

### Cultivate Runs Non-Interactively

Once invoked, cultivate drives to a finished slice. Ambiguity gets resolved in favor of the smallest defensible interpretation; the operator sees the choice (and the alternatives) in the `Unresolved` output section, not as a mid-run question. Interactive ideation belongs to the `plot` skill, not cultivate.

## Cultivate Maturity Signals

Strong cultivatees usually have:

- A concise `AGENTS.md` with commands and links.
- A docs map for architecture, product behavior, quality, reliability, security, and plans.
- CI and local commands that agents can run without special human setup.
- Mechanical checks for important invariants.
- Clear PR/review expectations and validation evidence.
- Observability or debugging paths for runtime behavior.
- A process for retiring stale docs and bad patterns.

Weak cultivatees usually have:

- No agent entrypoint, or a huge unstructured one.
- Important knowledge trapped in tickets, chat, or people's heads.
- Rules expressed only as preferences in prose.
- Unclear test commands or checks that require manual interpretation.
- No pattern for complex plans or decision logs.
- Drift that is cleaned up only by occasional heroic human effort.
