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
  version: "0.2.2"
---

# Cultivate Repo

Use this skill to help an agent improve a repository as a working environment for future agents. The goal is not more documentation for its own sake. The goal is a repo where agents can discover context, verify behavior, respect architecture, and improve the system without relying on hidden human memory.

## Operating Philosophy

Cultivate is an applied form of harness engineering: humans steer, agents execute, the repository is the system of record. From an agent's perspective, anything it cannot access in the repository effectively does not exist. Cultivate's job is to make the things that matter -- intent, architecture, conventions, verification -- first-class, versioned, and mechanically enforceable without drowning the agent in prose.

Read `references/harness-openai-blog.md` before changing the default documentation or directory structure. It is the concrete source for the harness layout this skill should install: short `AGENTS.md`, root `ARCHITECTURE.md`, and a structured `docs/` knowledge store with design docs, product specs, execution plans, generated docs, references, and focused system docs. Read `references/harness-engineering.md` for the full conceptual foundation when a decision needs that grounding. Read `references/cultivate-principles.md` for the operational shortlist when picking what to change.

## Non-Interactivity Contract

Cultivate runs to completion without menu-style prompts or confirmation gates. Ideation is `plot`'s job -- by the time cultivate is invoked, a `seed.md` or an existing repo is the input, and the skill is expected to execute against it.

- Resolve ambiguity autonomously. When the seed is sparse, contradicts the working tree, or the repo has gaps, pick the smallest defensible interpretation and proceed. Record the choice and the alternatives in the handoff output, not mid-run as a question.
- Do not ask "what do you want next?" between steps. Drive to a finished slice (audit, proposal, or applied change).
- Unresolved questions are an output artifact -- a dedicated section in the handoff -- not a blocker.

This mirrors the ExecPlans guidance from the OpenAI cookbook: "do not prompt the user for 'next steps'; simply proceed to the next milestone. Resolve ambiguities autonomously."

## Entry Modes

Cultivate is invoked in two shapes. Determine which one applies before doing anything else:

- **Post-plot handoff.** A `seed.md` exists (produced by the `plot` skill) and describes the intended project. The repository may be empty, freshly scaffolded, or partially built. Start from the seed.
- **Existing-repo audit.** No `seed.md`, but a real repository exists with code, conventions, and history. Start from the audit.

The two modes converge once the initial read is complete, but the first step differs.

### Default Output Shape

A bare invocation -- "run cultivate against this seed", "cultivate this repo" -- resolves to an **applied change**, not a proposal. Drive to a committed slice: write the files, run the checks, report what landed. Propose-mode is an explicit opt-in ("propose a cultivate slice", "what would cultivate do here", "audit-only"). Audit-mode is an explicit opt-in ("audit this repo"). If the operator did not name a mode, apply.

Applying means: pick the smallest high-leverage slice the audit and seed justify, write it, verify it, and return the implementation output pattern (what changed, why, checks, Unresolved). Do not ask whether to proceed.

## Start With The Seed (Post-Plot)

If a `seed.md` is present at the repo root or supplied by the user, read it before anything else. It is the intent document cultivate should optimize the harness around.

Extract and hold on to:

- `name`, `tagline`, `stack`, and `status` from the frontmatter.
- The **Agents** section -- what AI agents will actually do in this repo. This is the single most load-bearing field for cultivate, because it determines which harness investments pay off.
- **Scope (MVP)** and explicit **Out** items -- these bound what the initial `AGENTS.md` should cover.
- **Success** -- the observable shape of a working v1, which drives which validation commands belong in the harness now versus later.
- **Constraints** and **Open Questions** -- anything the cultivate should flag as TBD rather than over-specifying.

If the seed is sparse or inconsistent with what exists on disk, do not stop. The seed is intent, not a contract with the code; intent drifts. Pick the smallest defensible reconciliation, proceed with it, and record the mismatch and the alternative interpretations in the handoff output so the next agent (or the operator reading the report) can correct course.

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
- The harness knowledge-store skeleton from `references/harness-openai-blog.md`: root `ARCHITECTURE.md`, `docs/PLANS.md`, `docs/QUALITY.md`, `docs/RELIABILITY.md`, `docs/SECURITY.md`, plus `docs/design-docs/`, `docs/product-specs/`, `docs/exec-plans/`, `docs/generated/`, and `docs/references/`.
- README/index placeholders inside knowledge-store directories that do not yet have project-specific content. Empty directories disappear from git and teach agents nothing; a short README should say when to use the directory and what belongs there.
- A planning template for complex work, with decision and progress logs.
- A mechanical check for one recurring invariant rather than more prose about the invariant.
- A clear test/verification section that names exact commands and expected signals.
- For Python repositories, prefer isolated commands such as `uv run pytest`, `uv run ruff check`, or `uv run python scripts/tool.py` when `uv.lock`, `pyproject.toml`, or existing docs indicate `uv` is the project runner.

When the user asks to implement cultivate improvements, choose one focused slice unless they explicitly ask for a broad overhaul. Explain why that slice increases agent leverage.

If a `seed.md` exists, let its **Agents** and **Success** fields narrow the slice. A repo whose agents will "run evals and open cleanup PRs" needs different scaffolding than a repo whose agents will "review PRs and respond to bug reports" -- do not build generic prose when the seed tells you the specific one. The directory skeleton is still useful even for small repos because it gives future context a stable home; scale the content down, not the map away.

## What To Encode Where

Use this division of responsibility:

- `AGENTS.md`: short entrypoint. Include project map, high-value commands, important conventions, and links to deeper docs. Keep it scannable. (Detailed shape rules below.)
- `ARCHITECTURE.md`: root architecture map. Put top-level system purpose, layers, flows, boundaries, extension points, and mechanical architecture checks here so it is easy to discover from `AGENTS.md`.
- `docs/`: the repository knowledge store, not a catch-all dumping ground. Prefer this layout unless the repo already has a strong conflicting convention:
  - `docs/design-docs/` -- design history, core beliefs, accepted/rejected approaches, verification status.
  - `docs/product-specs/` -- user-facing behavior, workflows, acceptance criteria, product decisions.
  - `docs/exec-plans/active/` and `docs/exec-plans/completed/` -- living plans and completed execution records; include `docs/exec-plans/tech-debt-tracker.md`.
  - `docs/generated/` -- generated schemas, command inventories, API summaries, or other regenerated facts.
  - `docs/references/` -- external docs or LLM-readable reference snapshots such as `uv-llms.txt`.
  - `docs/PLANS.md`, `docs/QUALITY.md`, `docs/RELIABILITY.md`, `docs/SECURITY.md` -- cross-cutting operating docs.
  - Add `docs/DESIGN.md`, `docs/FRONTEND.md`, and `docs/PRODUCT_SENSE.md` when the repo has UI, design, or product-shaping work.
- Scripts, tests, linters, schemas, CI: rules that should be enforced repeatedly or are easy to forget. Custom lint messages should include remediation text so violations teach the next agent.
- Issue/PR templates: human-facing prompts that capture acceptance criteria, validation evidence, screenshots, logs, and rollout notes.
- Generated docs: only for facts that can be regenerated or validated, such as schema summaries or command inventories.

If a fact lives only in chat, a ticket, a meeting, or a person's head, treat it as invisible to future agents until it is encoded in the repo.

## AGENTS.md Shape

`AGENTS.md` is the open cross-tool standard read natively by Codex, Copilot, Cursor, Windsurf, Amp, and Devin (Claude Code uses `CLAUDE.md`; mirror, do not duplicate). The patterns that actually change agent behavior are operational, not literary.

- **Command-first.** Every instruction should map to an exact shell invocation an agent can run and check the exit code of. Replace "run the tests" with ``Test: `uv run pytest -v` ``. Replace "follow our style" with a linter command.
- **Definition of Done.** Include an explicit closure section: the specific exit codes and observable outputs that prove a task is complete. "I think I'm done" is the default failure mode; this eliminates it.
- **Task-organized sections.** Prefer `When Writing Code` / `When Reviewing` / `When Releasing` over flat style lists. Agents select by task; flat lists force them to parse every rule every turn.
- **Escalation rules.** Include `When Blocked` (what to do after N retries) and a `Never` list (destructive recovery patterns to refuse: deleting lockfiles, force-pushing, skipping tests).
- **Three-tier action boundaries.** Always / Ask / Never. Always-allowed actions keep agents moving; Ask-required actions gate risky work; Never actions are hard refusals.
- **Size discipline.** Keep sections under ~50 lines and the whole file under ~150. Codex enforces a default 32 KiB limit (`project_doc_max_bytes`) -- long files get truncated. Front-load commands and closure; defer style preferences.
- **Hierarchy for monorepos.** Nest `AGENTS.md` per service or package; tools walk from repo root to the current directory and concatenate. In Codex, `AGENTS.override.md` replaces parent instructions (use for release freezes or security-sensitive paths).
- **Mirror, don't duplicate.** `AGENTS.md` is canonical. If a team also uses `CLAUDE.md` or `.cursor/rules`, generate them from the same source rather than maintaining parallel instruction sets that will drift.

Anti-patterns to strip out: prose paragraphs without commands, ambiguous directives ("be careful", "where possible"), contradictory priorities without explicit ordering, and style guides with no enforcement command.

## ExecPlans (PLANS.md)

For multi-hour, multi-milestone, or high-unknown work, cultivate installs an ExecPlan workflow. The pattern comes from the OpenAI cookbook ("Using PLANS.md for multi-hour problem solving") and the harness blog's `docs/exec-plans/` layout.

- Place the convention/index at `docs/PLANS.md`, active plans under `docs/exec-plans/active/`, completed plans under `docs/exec-plans/completed/`, and long-lived debt in `docs/exec-plans/tech-debt-tracker.md`. Reference these from `AGENTS.md` so agents know when and how to use them.
- An ExecPlan is a _living document_. Mandatory sections: `Purpose / Big Picture`, `Progress`, `Surprises & Discoveries`, `Decision Log`, `Outcomes & Retrospective`, plus `Context and Orientation`, `Plan of Work`, `Concrete Steps`, `Validation and Acceptance`, `Idempotence and Recovery`, `Artifacts and Notes`, and `Interfaces and Dependencies`.
- Every ExecPlan must be self-contained: a novice agent with no prior context should be able to read the plan plus the working tree and produce a working, observable result.
- Acceptance is phrased as observable behavior ("after starting the server, `curl localhost:8080/health` returns `200 OK`"), not internal attributes.
- Living-document discipline: decisions land in the Decision Log as they are made; unexpected findings land in Surprises & Discoveries; Progress is updated at every stopping point; Outcomes & Retrospective closes each major milestone.
- **Agents do not prompt the user mid-plan.** They resolve ambiguity autonomously, record the decision, and continue. This matches cultivate's own non-interactivity contract.

Reach for an ExecPlan when the seed's scope, a request's acceptance criteria, or an audit's remediation list exceeds what fits comfortably in one agent turn. Small changes get an ephemeral plan or no plan; cross-cutting refactors and greenfield features get an ExecPlan checked into the repo.

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
- Read `references/harness-openai-blog.md` when choosing the default knowledge-store directory structure or explaining why `AGENTS.md` should point into `docs/` instead of holding everything itself.
- Read `references/cultivate-principles.md` when you need the operational checklist.
- Read `references/templates.md` when drafting `AGENTS.md`, cultivate docs, quality docs, execution-plan guidance, or audit reports.
- Run `scripts/audit_cultivate.py` when you need a quick read-only baseline.

## Output Patterns

Cultivate always returns a finished artifact. Concrete rules:

- **Never append a "which of these next?" menu.** No trailing lists of options for the operator to pick from. No "tell me which" closers. No "say the word and I'll ...". The last section of the output is always `Unresolved` followed by `Verification`, in that order.
- **Open items go into `Unresolved`.** Mismatches, assumptions, interpretations chosen and rejected, follow-up work worth doing -- all recorded as append-only content in `Unresolved`, not as mid-run questions.
- **Pick the shape from the invocation**, using the `Default Output Shape` rules above. A bare invocation is an applied change; propose-only and audit-only are explicit opt-ins.

For a seed handoff (propose-only opt-in), return:

1. What you extracted from `seed.md` (especially the Agents and Success fields).
2. The cultivate slice you recommend first, tied back to that intent.
3. `Unresolved`: mismatches between seed and on-disk state, the interpretation you proceeded with, and the alternatives you rejected.
4. Verification or rollout notes.

For an audit-only request, return:

1. Current cultivate summary.
2. Top gaps by leverage.
3. Recommended first improvements.
4. `Unresolved`: assumptions made during the audit and any repo questions the operator should confirm.
5. Verification or rollout notes.

For an implementation request, return:

1. What you changed.
2. Why it improves agent legibility or enforceability (cite the harness principle or AGENTS.md pattern invoked).
3. What checks you ran and their observed results.
4. `Unresolved`: follow-up cultivate work worth doing next, and any assumptions baked into the slice.

## Verification

After editing, run the most relevant existing checks. For Python projects, prefer `uv run ...` when available so validation uses the repository's isolated environment. If no reliable command exists, say that explicitly and identify the missing validation path as a cultivate gap.

For documentation-only edits, at minimum verify links/paths referenced by the new docs where practical. For scripts or mechanical checks, run the script on the current repository and include the observed result.
