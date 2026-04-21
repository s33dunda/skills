# Changelog

All notable changes to the `cultivate` skill are documented in this file. The
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
skill uses [Semantic Versioning](https://semver.org/).

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
