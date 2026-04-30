# Changelog

All notable changes to the `plot` skill are documented in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this skill
uses [Semantic Versioning](https://semver.org/).

## [0.2.1] - 2026-04-21

### Added

- **No-gaps case in Smart Selection (`SKILL.md` Step 3).** When `seed.md`
  already exists and every required + recommended field is populated, Smart
  Selection now has an explicit rule: skew toward `risk` + `context` methods
  (Pre-mortem, Constraints Audit, Prior Art Survey, Competitive Complaint
  Scan), revisit `scope` if the seed is aging, include Cultivate Alignment
  when plans may have evolved, and de-prioritize `framing` unless the core
  pitch has drifted. Discovered during the 0.2.0 self-test against this repo
  (seed was already complete) and logged as debt; closing it in 0.2.1.

## [0.2.0] - 2026-04-21

### Added

- **Ambient context gathering (Step 1).** Plot now scans the working directory
  before asking the user anything — git remote → name, manifests
  (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, etc.) → stack,
  `README.md` → tagline/problem, existing `seed.md`/`AGENTS.md` → prior state
  to merge. Documented in `references/repo-signals.md`.
- **BMAD-style elicitation loop.** Replaces the "ask all questions at once"
  step. Plot presents a status board of gathered/missing fields, then offers
  5 numbered elicitation methods + `[r]` reshuffle / `[a]` list all /
  `[f]` free-form / `[x]` proceed. HALTs after each menu and after each
  "apply these changes?" prompt. Method registry lives in `methods.csv`
  (BMAD `num, category, method_name, description, output_pattern` format).
- `methods.csv` — 15 methods across `framing`, `scope`, `agent`, `risk`,
  `context` categories, including `Agent Tasks Inventory` and `Cultivate
  Alignment` that target the plot→cultivate handoff.
- `references/bmad-elicitation.md` — origins, attribution, and extension
  guide for the elicitation loop; documents divergences from upstream
  BMAD and the quality bar for adding/pruning methods. Required reading
  before future iterations touch `methods.csv` or the Step 3-4 flow.

### Changed

- `SKILL.md` restructured into `CRITICAL LLM INSTRUCTIONS` + `FLOW` sections
  mirroring the BMAD advanced-elicitation skill. The final artifact
  (`seed.md`) and the seed schema are unchanged.

## [0.1.0] - 2026-04-21

### Added

- Initial release. `plot` captures the minimum viable project idea -- identity,
  scope, stack, agents, success criteria, constraints, open questions -- and
  writes it to `seed.md` as a structured handoff to `cultivate`.
- `references/seed-schema.md` documents the artifact the skill emits.
- `evals/evals.json` covers brief capture, explicit out-of-scope handling, and
  plot-to-cultivate handoff fidelity.
