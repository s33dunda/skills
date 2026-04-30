# Repo-Local Agent Skills

This directory mirrors the installable skills from `../skills/` so agent clients
that scan `.agents/` can use them directly from a fresh checkout.

- Canonical source: `../skills/<name>/`
- Repo-local mirror: `.agents/skills/<name>/`
- Mirror refresh command: `uv run python scripts/sync_agents_skills.py`
- Validation command: `uv run python scripts/validate_skills.py`

Validation only checks this committed mirror. It does not inspect `~/.codex`,
`.claude`, or any other local host install. For hosts that do not read
`.agents/`, use the normal `npx skills` install flow.

Do not edit mirrored skill files here by hand. Edit `skills/<name>/`, run the
sync command, then run validation.
