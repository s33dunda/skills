# Harness Engineering

Cultivate is an applied form of harness engineering. This reference distills the source canon so an agent can cite it, reason from it, and apply it consistently without rediscovering the ideas each run.

## Source

- Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world," OpenAI, February 11, 2026. <https://openai.com/index/harness-engineering/>
- Related: "Using PLANS.md for multi-hour problem solving" (OpenAI cookbook, ExecPlans).
- Related: matklad, "ARCHITECTURE.md" (2021-02-06) -- the provenance of the short map-style architecture doc.
- Related: Alexis King, "Parse, don't validate" -- the boundary-parsing pattern.

## Core Thesis

> Humans steer. Agents execute. The repository is the system of record.

When a team's primary job is no longer to write code but to design the environment agents work inside, the engineering effort moves from code to scaffolding, tooling, abstractions, and feedback loops. The scarce resource becomes human time and attention, so the harness must keep agents productive without copy-pasting human context into prompts.

## Key Principles

### Give agents a map, not a manual

A short `AGENTS.md` (~100 lines) is a table of contents, not an encyclopedia. A monolithic guide crowds out task context, causes agents to pattern-match locally instead of navigate intentionally, rots instantly as rules go stale, and resists mechanical verification. Deeper knowledge lives in a structured `docs/` tree that agents load progressively.

### The repository is the system of record

From an agent's point of view, anything it cannot access in-context effectively does not exist. Knowledge in Slack, Google Docs, tickets, meeting notes, or people's heads is invisible during a run. If a fact should influence future work, encode it in versioned repo artifacts (markdown, schemas, code, executable plans).

### Progressive disclosure

Start agents with a small, stable entrypoint and teach them where to look next. Domain-specific references (architecture, product specs, quality grades, execution plans, external library `llms.txt` bundles) load on demand rather than being front-loaded.

### Enforce invariants, not implementations

Documentation alone cannot keep a high-throughput agent-generated codebase coherent. Encode repeated rules as linters, structural tests, schema checks, or CI jobs. Be strict about boundaries (dependency direction, data parsing, naming, observability hooks) and loose about local implementation choices. Custom lint messages should include remediation instructions so a violation becomes useful context the next time the agent runs.

### Parse, don't validate, at the boundary

Data that crosses the system edge gets parsed into typed shapes once. Agents should not probe or guess at external shapes downstream -- that leads to replication of uncertain assumptions. The exact library is unimportant; the discipline is.

### Layered domain architecture

Each business domain is divided into a fixed set of layers with forward-only dependencies (for example: Types -> Config -> Repo -> Service -> Runtime -> UI). Cross-cutting concerns enter through a single explicit interface (Providers). Constraints like these are normally postponed until a team has hundreds of engineers; with agents they are an early prerequisite because they convert speed into compounding leverage instead of drift.

### Prefer boring, legible dependencies

Technologies with stable APIs, composable semantics, and strong representation in training data are easier for agents to model. It is sometimes cheaper to reimplement a small, tightly integrated helper (with full test coverage and telemetry) than to wrap an opaque upstream library.

### Treat plans as first-class artifacts

Lightweight changes get ephemeral plans; complex work gets checked-in ExecPlans with progress logs, decisions, acceptance criteria, and validation evidence. A future agent should be able to resume from the plan plus the working tree with no hidden context.

### Make validation agent-legible

Expose the application itself to the agent: bootable per worktree, queryable logs (LogQL) and metrics (PromQL) and traces, DOM snapshots and screenshots via Chrome DevTools Protocol. Prompts like "no span in these four critical user journeys exceeds two seconds" only work when the feedback loop is mechanical.

### Throughput changes the merge philosophy

When agent throughput vastly exceeds human attention, corrections are cheap and waiting is expensive. Favor short-lived PRs, minimal blocking gates, agent-to-agent review, and follow-up runs over retries-with-human-review. This is a tradeoff that is only safe under strong architectural guardrails.

### Treat agent struggle as environment signal

When an agent repeatedly fails at a task, the reflex is not "try harder" or "write it by hand." It is: what capability, tool, guardrail, doc, or abstraction is missing, and how do we encode it so the agent can do it next time? The missing piece then becomes infrastructure for all future runs.

### Continuous garbage collection

Agent-generated code replicates local patterns, including the weak ones. Encode "golden principles" and schedule recurring cleanup passes (stale docs, duplicated helpers, drift from architecture, flaky tests, quality regressions). Technical debt behaves like a high-interest loan; pay it down in small continuous increments rather than manual Friday sweeps.

### Capture taste once, enforce continuously

When review feedback repeats, that is a signal the harness is missing a rule, template, test, or feedback loop. Promote the taste into code or lint; let it apply everywhere at once forever.

## What To Optimize For

- **Agent legibility of the product itself** -- UI state, logs, metrics, and traces should be programmatically inspectable.
- **Mechanical verifiability of knowledge** -- cross-links, freshness, coverage checked by CI.
- **Compounding investment in capability** -- every fix for an agent struggle becomes reusable infrastructure.
- **Human attention on intent and outcomes** -- not on reviewing every line.

## Failure Modes To Avoid

- One giant `AGENTS.md` that tries to be the manual.
- Rules expressed only as prose when they should be mechanical.
- Unversioned knowledge trapped in chat or heads.
- Human-rewrite reflex when agents struggle instead of building the missing capability.
- Blocking gates and exhaustive human code review in a high-throughput environment.
- Expecting early velocity without upfront investment in environment specification.

## How Cultivate Applies This

The `cultivate` skill is a concrete, repo-scoped application of harness engineering. It does not try to build the full OpenAI-internal harness (observability stacks, DevTools wiring, doc-gardening agents). It aims for the smallest change that raises agent leverage given the repository's current state and its declared agent responsibilities. The principles above are the decision-making frame when choosing what to encode, what to enforce, and what to defer.
