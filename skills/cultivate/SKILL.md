---
name: cultivate
description: Cultivate a repository -- prepare it so farmers (AI agents) can work it. Use this skill to make a repo agent-legible and enforceable: create or improve AGENTS.md, build a knowledge map, add execution-plan workflows, encode architecture guardrails, expose CI/lint/test feedback to agents, and reduce drift from agent-generated PRs. The cultivate skill is the bridge between a s33ded idea and a repo ready for farmers to execute on. Replaces cultivate.
---

# Cultivate Repo

Use this skill to help an agent improve a repository as a working environment for future agents. The goal is not more documentation for its own sake. The goal is a repo where agents can discover context, verify behavior, respect architecture, and improve the system without relying on hidden human memory.

The operating philosophy is: humans steer; agents execute; the repository is the system of record.

## Start With An Audit

Before proposing or editing anything, inspect the target repository.

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

Do not begin by writing a large manual. Large instruction blobs crowd out task context, rot quickly, and become hard for agents to prioritize.

## Implementation Strategy

Prefer the smallest change that makes the next agent more capable.

Good first improvements are usually:

- A short root `AGENTS.md` that acts as a map, not an encyclopedia.
- A repo-local docs index under `docs/` or `docs/agents/` that points to deeper sources of truth.
- A planning template for complex work, with decision and progress logs.
- A mechanical check for one recurring invariant rather than more prose about the invariant.
- A clear test/verification section that names exact commands and expected signals.
- For Python repositories, prefer isolated commands such as `uv run pytest`, `uv run ruff check`, or `uv run python scripts/tool.py` when `uv.lock`, `pyproject.toml`, or existing docs indicate `uv` is the project runner.

When the user asks to implement cultivate improvements, choose one focused slice unless they explicitly ask for a broad overhaul. Explain why that slice increases agent leverage.

## What To Encode Where

Use this division of responsibility:

- `AGENTS.md`: short entrypoint. Include project map, high-value commands, important conventions, and links to deeper docs. Keep it scannable.
- `docs/` or `docs/agents/`: durable repository knowledge such as architecture, product constraints, quality standards, troubleshooting, and execution-plan conventions.
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

- Read `references/cultivate-principles.md` when you need the conceptual checklist behind the skill.
- Read `references/templates.md` when drafting `AGENTS.md`, cultivate docs, quality docs, execution-plan guidance, or audit reports.
- Run `scripts/audit_cultivate.py` when you need a quick read-only baseline.

## Output Patterns

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
