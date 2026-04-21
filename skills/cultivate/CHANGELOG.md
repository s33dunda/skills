# Changelog

All notable changes to the `cultivate` skill are documented in this file. The
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
skill uses [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-04-21

### Added

- **Non-Interactivity Contract** in `SKILL.md`: cultivate drives to a finished
  slice once invoked. Ambiguities are resolved autonomously and surfaced in an
  `Unresolved` section of the handoff, never as mid-run questions. Interactive
  ideation stays with the `plot` skill.
- 2026 harness engineering signal in `references/harness-engineering.md`:
  Lopopolo (OpenAI, Feb 2026), Friel (ExecPlans, Oct 2025), Choi (Codex
  modernization, Nov 2025), Crosley (AGENTS.md Patterns, Feb 2026), OpenAI
  AGENTS.md and best-practices docs. New principles: command-first
  instructions, explicit closure (`Definition of Done`), three-tier action
  boundaries (Always / Ask / Never), semantic linting (errors that teach),
  escalation rules, and hierarchy/override for multi-scope repos.
- Operational counterparts in `references/cultivate-principles.md`:
  command-first, explicit closure, task-organized sections, the `Never` list,
  size budget (~150 lines total, Codex `project_doc_max_bytes` default of
  32 KiB), nested `AGENTS.md` for monorepos, ExecPlans as living documents,
  and the non-interactivity principle.
- Canonical ExecPlan skeleton in `references/templates.md` with the mandatory
  sections: `Purpose / Big Picture`, `Context and Orientation`, `Interfaces
  and Dependencies`, `Plan of Work`, `Concrete Steps`, `Validation and
  Acceptance`, `Idempotence and Recovery`, `Progress`, `Surprises &
  Discoveries`, `Decision Log`, `Outcomes & Retrospective`, `Artifacts and
  Notes`.
- Nested `AGENTS.md` / `AGENTS.override.md` template and canonical ->
  tool-specific mirroring guidance (Codex / Copilot / Cursor / Windsurf /
  Amp / Devin read `AGENTS.md`; Claude Code reads `CLAUDE.md` -- mirror, do
  not duplicate).

### Changed

- Upgraded the root `AGENTS.md` template to the command-first shape:
  named commands for install/test/lint/format/start/verify, explicit
  `Definition of Done`, `When Writing Code` / `When Reviewing Code`,
  `When Blocked` escalation paths, and a `Never` list.
- Rewrote the `docs/PLANS.md` convention doc plus a per-effort ExecPlan
  template at `docs/plans/_template.md`, replacing the earlier prose-only
  guidance.
- Upgraded the Cultivate Audit Report template with category prompts that
  name the specific 2026 patterns (Definition of Done, When Blocked, Never
  list, size budget, nested AGENTS.md, ExecPlan discipline) and an
  `Unresolved` section for assumptions, interpretations, and follow-ups.
- Replaced "surface mismatch to the user" language in `SKILL.md` with the
  autonomous-reconciliation-plus-`Unresolved`-report pattern.

### Notes

- Version bump from 0.1.0 to 0.2.0 reflects the non-interactivity contract
  (behavioral change in how cultivate handles ambiguity) and the upgraded
  AGENTS.md / ExecPlan templates (output-shape change).

## [0.1.0] - 2026-04-21

### Added

- Initial versioned release. `cultivate` prepares a repository for AI agents by
  emitting the canonical harness bundle: `AGENTS.md` at the root plus
  `docs/ARCHITECTURE.md`, `docs/QUALITY.md`, and `docs/PLANS.md`.
- Anchored the skill in harness engineering via
  `references/harness-engineering.md` (conceptual foundation) and
  `references/cultivate-principles.md` (operational checklist).
- Added a post-plot entry mode that ingests `seed.md` (especially the **Agents**
  and **Success** sections) and narrows the cultivate slice to the specific
  agent surface instead of a generic scaffold.
- Added an existing-repo audit mode backed by `scripts/audit_cultivate.py`.

### Changed

- Flattened `docs/agents/` to `docs/` as the default harness target; kept
  `docs/agents/` documented as an escape hatch for repos whose `docs/` is
  already owned by a published site.
