# Cultivate Engineering Principles

This reference distills the cultivate-engineering approach into repository practices an agent can apply.

## Core Idea

A coding agent is only as effective as the environment it can observe and act inside. Human time is scarce, so invest in repository structure, tools, checks, and feedback loops that let agents make progress without asking humans to copy context into prompts.

## Principles

### Give Agents A Map, Not A Manual

Keep the root `AGENTS.md` short. It should orient the agent and point to deeper sources of truth. A giant all-purpose instruction file competes with task context, hides priorities, and grows stale.

### Make The Repo The System Of Record

If future agents need to know a decision, constraint, workflow, or domain fact, put it in versioned repository files. External documents, chat threads, and tacit human knowledge are invisible during most agent runs.

### Use Progressive Disclosure

Start with a small entrypoint, then link to focused docs by topic. Agents should be able to load only the context needed for the task at hand.

### Enforce Architecture Mechanically

Documentation helps, but repeated rules should become tests, linters, schema checks, or CI jobs. Enforce boundaries and invariants centrally while leaving local implementation freedom.

### Make Validation Agent-Legible

Agents need direct feedback. Prefer commands, logs, metrics, traces, screenshots, health checks, and reproducible workflows that an agent can run and interpret.

### Treat Plans As First-Class Artifacts

For long or risky work, use checked-in execution plans with progress, decisions, acceptance criteria, and validation evidence. A plan should let a future agent resume without hidden context.

### Capture Taste Once, Apply Continuously

When review feedback repeats, encode it in docs or tooling. If the same issue keeps appearing in agent PRs, the cultivate is missing a rule, template, test, or feedback loop.

### Run Continuous Garbage Collection

Agent-generated code tends to replicate local patterns, including weak ones. Schedule or prompt periodic cleanup passes for stale docs, duplicated helpers, drift from architecture, flaky tests, and quality gaps.

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
