---
name: cultivate
description: >-
  Cultivate a repository -- prepare it so farmers (AI agents) can work it. Use this skill
  whenever the user wants to make a repo agent-legible and enforceable, hand off a `seed.md`
  from plot to an actual repository, add or improve `AGENTS.md`, build a knowledge map,
  introduce execution-plan workflows, encode architecture guardrails, expose CI/lint/test
  feedback to agents, or reduce drift from agent-generated PRs. Cultivate is applied
  harness engineering -- it is the bridge between a seeded idea (or an existing repo) and
  an environment where AI agents can execute reliably.
metadata:
  version: "0.1.0"
---

# Cultivate Repo

Use this skill to help an agent improve a repository as a working environment for future agents. The goal is not more documentation for its own sake. The goal is a repo where agents can discover context, verify behavior, respect architecture, and improve the system without relying on hidden human memory.

## Operating Philosophy

Cultivate is an applied form of harness engineering: humans steer, agents execute, the repository is the system of record. From an agent's perspective, anything it cannot access in the repository effectively does not exist. Cultivate's job is to make the things that matter -- intent, architecture, conventions, verification -- first-class, versioned, and mechanically enforceable without drowning the agent in prose.

Read `references/harness-engineering.md` for the full conceptual foundation when a decision needs that grounding. Read `references/cultivate-principles.md` for the operational shortlist when picking what to change.

## Entry Modes

Cultivate is invoked in two shapes. Determine which one applies before doing anything else:

- **Post-plot handoff.** A `seed.md` exists (produced by the `plot` skill) and describes the intended project. The repository may be empty, freshly scaffolded, or partially built. Start from the seed.
- **Existing-repo audit.** No `seed.md`, but a real repository exists with code, conventions, and history. Start from the audit.

The two modes converge once the initial read is complete, but the first step differs.

## Start With The Seed (Post-Plot)

If a `seed.md` is present at the repo root or supplied by the user, read it before anything else. It is the intent document cultivate should optimize the harness around.

Extract and hold on to:

- `name`, `tagline`, `stack`, and `status` from the frontmatter.
- The **Agents** section -- what AI agents will actually do in this repo. This is the single most load-bearing field for cultivate, because it determines which harness investments pay off.
- **Scope (MVP)** and explicit **Out** items -- these bound what the initial `AGENTS.md` should cover.
- **Success** -- the observable shape of a working v1, which drives which validation commands belong in the harness now versus later.
- **Constraints** and **Open Questions** -- anything the cultivate should flag as TBD rather than over-specifying.

If the seed is sparse or inconsistent with what exists on disk, surface the mismatch to the user before extrapolating. The seed is not a contract with the code; it is intent, and intent drifts.

## Start With An Audit

Whether or not a seed was present, inspect the target repository before proposing changes.

1. Find the repo root and read the nearest `AGENTS.md`, README, package manifests, CI workflows, and obvious docs indexes.
2. If filesystem access is available, run the bundled scanner:

   ```bash
   python3 /path/to/cultivate/scripts/audit_cultivate.py /path/to/repo
   ```

   Use `--json` when another tool or script will consume the output.

3. Summarize the current cultivate in six categories:
   - Orientation: how an agent learns what this repo is and how to work in it.
   - Knowledge system: where product, architecture, plans, and operational truth live.
   - Enforceable rules: which important norms are checked by tests, linters, CI, schemas, or scripts.
   - Validation feedback: how an agent can prove a change works.
   - Autonomy workflow: how agents handle plans, reviews, PRs, fixes, and follow-up.
   - Entropy control: how drift, stale docs, flaky tests, and bad copied patterns are found and cleaned up.

Do not begin by writing a large manual. Large instruction blobs crowd out task context, rot quickly, and become hard for agents to prioritize -- treat `AGENTS.md` as a table of contents, not an encyclopedia.

## Implementation Strategy

Prefer the smallest change that makes the next agent more capable.

Good first improvements are usually:

- A short root `AGENTS.md` that acts as a map, not an encyclopedia.
- A repo-local docs index under `docs/` that points to deeper sources of truth (use a nested namespace like `docs/agents/` only when `docs/` is already owned by a published site).
- A planning template for complex work, with decision and progress logs.
- A mechanical check for one recurring invariant rather than more prose about the invariant.
- A clear test/verification section that names exact commands and expected signals.
- For Python repositories, prefer isolated commands such as `uv run pytest`, `uv run ruff check`, or `uv run python scripts/tool.py` when `uv.lock`, `pyproject.toml`, or existing docs indicate `uv` is the project runner.

When the user asks to implement cultivate improvements, choose one focused slice unless they explicitly ask for a broad overhaul. Explain why that slice increases agent leverage.

If a `seed.md` exists, let its **Agents** and **Success** fields narrow the slice. A repo whose agents will "run evals and open cleanup PRs" needs different scaffolding than a repo whose agents will "review PRs and respond to bug reports" -- do not build the generic harness when the seed tells you the specific one.

## What To Encode Where

Use this division of responsibility:

- `AGENTS.md`: short entrypoint. Include project map, high-value commands, important conventions, and links to deeper docs. Keep it scannable.
- `docs/`: durable repository knowledge such as architecture, product constraints, quality standards, troubleshooting, and execution-plan conventions. Humans and agents read the same files -- do not split into a separate `docs/agents/` unless `docs/` is already owned by a published site.
- Scripts, tests, linters, schemas, CI: rules that should be enforced repeatedly or are easy to forget.
- Issue/PR templates: human-facing prompts that capture acceptance criteria, validation evidence, screenshots, logs, and rollout notes.
- Generated docs: only for facts that can be regenerated or validated, such as schema summaries or command inventories.

If a fact lives only in chat, a ticket, a meeting, or a person's head, treat it as invisible to future agents until it is encoded in the repo.

## Enforce Invariants, Not Taste Micromanagement

For recurring problems, ask: what capability or feedback loop is missing?

Prefer enforceable boundaries over long lists of preferences. Examples:

- Architecture boundaries: dependency rules, package layering checks, import restrictions.
- Data boundaries: parse or validate external shapes at the edge of the system.
- Observability: structured logging, trace/span naming, startup timing, critical journey metrics.
- Reliability: deterministic test commands, service health checks, retry/failure behavior.
- Maintainability: file-size limits, stale docs checks, duplicated helper detection, generated artifact freshness checks.

Use prose to teach intent. Use tooling to apply repeated rules.

## Templates And References

Load only what is needed:

- Read `references/harness-engineering.md` when you need the full conceptual foundation (the source canon cultivate applies).
- Read `references/cultivate-principles.md` when you need the operational checklist.
- Read `references/templates.md` when drafting `AGENTS.md`, cultivate docs, quality docs, execution-plan guidance, or audit reports.
- Run `scripts/audit_cultivate.py` when you need a quick read-only baseline.

## Output Patterns

For a seed handoff, return:

1. What you extracted from `seed.md` (especially the Agents and Success fields).
2. The cultivate slice you recommend first, tied back to that intent.
3. Any mismatches between seed and on-disk state that the user should resolve.
4. Verification or rollout notes.

For an audit-only request, return:

1. Current cultivate summary.
2. Top gaps by leverage.
3. Recommended first improvements.
4. Verification or rollout notes.

For an implementation request, return:

1. What you changed.
2. Why it improves agent legibility or enforceability.
3. What checks you ran.
4. Any follow-up cultivate work worth doing next.

## Verification

After editing, run the most relevant existing checks. For Python projects, prefer `uv run ...` when available so validation uses the repository's isolated environment. If no reliable command exists, say that explicitly and identify the missing validation path as a cultivate gap.

For documentation-only edits, at minimum verify links/paths referenced by the new docs where practical. For scripts or mechanical checks, run the script on the current repository and include the observed result.
