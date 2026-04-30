# Quality And Verification

## Standard Checks

- Validate skill packaging: `uv run python scripts/validate_skills.py`
- Validator unit tests: `uv run python -m unittest scripts.test_validate_skills`
- Harness audit: `uv run python skills/cultivate/scripts/audit_cultivate.py .`
- Refresh committed `.agents/skills/` mirror: `uv run python scripts/sync_agents_skills.py`
- Full verify: `uv run python scripts/validate_skills.py && uv run python -m unittest scripts.test_validate_skills`

## Critical Invariants

1. Every skill directory has matching `name` frontmatter, a non-empty `description`, valid eval metadata when present, and syntactically valid Python helpers.
2. `.agents/skills/` is a byte-for-byte mirror of `skills/` for every committed skill file, excluding generated Python cache artifacts.
3. `version` is bumped and `CHANGELOG.md` has a matching entry on every behavioral `SKILL.md` change.
4. Skill helper scripts in `skills/*/scripts/` make no network calls — they are deterministic and run offline.
5. `docs/exec-plans/` holds active and completed ExecPlans; `docs/exec-plans/tech-debt-tracker.md` tracks long-lived cleanup items.

The quality gate intentionally does not inspect user-local host installs such
as `~/.codex/skills` or `.claude`. Those are installed or refreshed outside the
repo, usually through the `npx skills` flow.

## Known Gaps

- No CI workflow. The validator and tests run locally only. Adding a GitHub Actions workflow is tracked in `docs/exec-plans/tech-debt-tracker.md`.
- Model-backed eval runs (against `evals/evals.json`) require an `ANTHROPIC_API_KEY` budget and are deferred per `seed.md`.
