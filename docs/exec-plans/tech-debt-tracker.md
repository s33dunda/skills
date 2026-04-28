# Tech Debt Tracker

Long-lived cleanup items and known gaps that don't warrant a full ExecPlan.

| Item | Added | Priority | Notes |
| --- | --- | --- | --- |
| Add CI workflow (GitHub Actions) for `uv run python scripts/validate_skills.py && uv run python -m unittest scripts.test_validate_skills` | 2026-04-28 | medium | Deferred in `seed.md` — no CI budget. Unblocks automated feedback on skill PRs. |
| Model-backed eval runner wired to `evals/evals.json` | 2026-04-28 | low | Requires `ANTHROPIC_API_KEY` budget. Deferred per `seed.md`. Prompts already in each skill's `evals/`. |
