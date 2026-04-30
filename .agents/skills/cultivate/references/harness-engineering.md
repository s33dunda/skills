# Harness Engineering

Cultivate is an applied form of harness engineering. This reference distills the source canon so an agent can cite it, reason from it, and apply it consistently without rediscovering the ideas each run.

## Sources

Primary:

- Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world," OpenAI, February 11, 2026. <https://openai.com/index/harness-engineering/>. Full-text mirror checked into this skill: `references/harness-openai-blog.md` -- read it directly when grounding an AGENTS.md / docs-tree decision rather than fetching the live page.
- Aaron Friel, "Using PLANS.md for multi-hour problem solving," OpenAI Cookbook, October 7, 2025. <https://cookbook.openai.com/articles/codex_exec_plans>
- Derrick Choi, "Modernizing your Codebase with Codex," OpenAI Cookbook, November 19, 2025. <https://cookbook.openai.com/examples/codex/code_modernization>
- "Best practices -- Codex," OpenAI Developers (current). <https://developers.openai.com/codex/learn/best-practices>
- "Custom instructions with AGENTS.md," OpenAI Developers (current). <https://developers.openai.com/codex/guides/agents-md/>

Field research and synthesis:

- Blake Crosley, "AGENTS.md Patterns: What Actually Changes Agent Behavior," February 28, 2026. <https://blakecrosley.com/blog/agents-md-patterns>
- "AGENTS.md Guide (2026): Copilot, Cursor & More," Vibecoding. <https://vibecoding.app/blog/agents-md-guide>
- "The Complete Guide to Agent Harness," harness-engineering.ai.
- Tian Pan, "Harness Engineering: The Discipline That Determines Whether Your AI Agents Actually Work," February 17, 2026.

Prior art:

- matklad, "ARCHITECTURE.md," February 6, 2021 -- short map-style architecture doc.
- Alexis King, "Parse, don't validate" -- boundary-parsing pattern.

## Core Thesis

> Humans steer. Agents execute. The repository is the system of record.

When a team's primary job is no longer to write code but to design the environment agents work inside, the engineering effort moves from code to scaffolding, tooling, abstractions, and feedback loops. The scarce resource becomes human time and attention, so the harness must keep agents productive without copy-pasting human context into prompts.

## Key Principles (Primary Source: Lopopolo)

Every principle in this subsection maps directly to Ryan Lopopolo's OpenAI blog post (Feb 2026). Read `references/harness-openai-blog.md` for the verbatim text. These are the load-bearing doctrine; when a decision needs grounding, start here.

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

### Semantic linting -- errors that teach

Mechanical checks should not only fire; they should include the remediation inline. A custom lint message like "imports from `src/web/` into `src/core/` are forbidden (layering violation); move shared helpers to `src/core/shared/` or invert the dependency" turns every violation into context for the next agent run. Unhelpful errors waste turns; teaching errors compound into agent capability.

## Key Principles (AGENTS.md Ecosystem)

These operational patterns are absent from the Lopopolo primary source but widely adopted in the broader AGENTS.md ecosystem (Codex best-practices, the `agents.md` open standard, field analysis by Crosley, 2026). They are compatible with Lopopolo's doctrine -- they operationalize "enforce invariants mechanically" and "progressive disclosure" in specific ways -- but they are not prescribed by it. Use them as defaults, not as primary canon.

### Instructions are command-first, not prose-first

The most reliable instruction-file patterns (Crosley, 2026; GitHub analysis of 2,500+ AGENTS.md repos) are operational rather than literary. Every rule the harness wants an agent to follow should map to an exact shell invocation whose exit code is the check. "Run the tests" is a suggestion; `` `uv run pytest -v` exits 0 `` is a rule. Style guides without an enforcement command reliably get ignored.

### Closure is explicit, not felt

"I think I'm done" is the most common failure mode for unsupervised agents. Encode `Definition of Done` as specific observable signals (exit codes, HTTP responses, log lines, file contents). An agent that cannot verify done-ness against a concrete check should not claim completion.

### Three-tier action boundaries

Productive harnesses partition actions into `Always` (safe, auto-run), `Ask` (requires human approval or narrow scoping), and `Never` (refused outright). Missing tiers produce either paralysis (nothing can run without asking) or drift (agents improvise destructive recoveries when blocked -- deleting lockfiles, bypassing checks, silently skipping tests). The `Never` list is as load-bearing as the `Always` list.

### Escalation rules prevent improvisation

When an agent is blocked, the default behavior is to invent a workaround. Explicit escalation paths (`If tests fail after 3 attempts: stop and report the failing test with full output`) and explicit prohibitions (`Never: delete files to resolve errors, force push, skip tests`) redirect the energy. Research on ambiguous bug reports (ICLR 2026 AMBIG-SWE) shows LLMs default to non-interactive behavior without explicit encouragement -- they proceed silently rather than ask, and resolve rates drop accordingly. The harness must name the moments where asking is required.

### Hierarchy and override for multi-scope repos

In a monorepo, a single root `AGENTS.md` is insufficient. Nested `AGENTS.md` files per service or package concatenate from root to the working directory; Codex additionally supports `AGENTS.override.md` to replace parent instructions. Use nesting for local conventions; use override for temporary states (release freezes, incident mode) or security-scoped paths.

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
