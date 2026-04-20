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
