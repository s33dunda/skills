# ExecPlan: cultivate-hardening

Status: active
Owner: maintainer
Started: 2026-04-29

## Purpose / Big Picture

Harden the `cultivate` skill so its treatment output is applied more consistently, especially in `AGENTS.md`. The immediate goal is to eliminate the weakly applied harness pattern surfaced by the aborted harness-efficiency pilot: repos that technically get a cultivate bundle but still end up with a thin `AGENTS.md` that fails to expose the deeper knowledge-store docs agents actually need.

Success means the skill, its templates, and its audit all agree on a stronger default shape, and a fresh dogfood pass on light/medium/heavy control-repo copies produces harnesses that include the richer `Deeper Context` guidance instead of the weak variant.

## Context and Orientation

- Repository areas touched: `skills/cultivate/SKILL.md`, `skills/cultivate/references/templates.md`, `skills/cultivate/scripts/audit_cultivate.py`, `skills/cultivate/evals/evals.json`, `skills/cultivate/CHANGELOG.md`, `docs/exec-plans/active/`
- Prior art in this repo: root `AGENTS.md`, aborted `docs/exec-plans/active/harness-efficiency-study.md`
- External references: `skills/cultivate/references/harness-openai-blog.md`, `skills/cultivate/references/harness-engineering.md`
- Starting state assumptions: `main` branch in `$SKILLS_REPO`; study workspace lives under `$STUDY_WORKSPACE`

## Interfaces and Dependencies

- Upstream: current `cultivate` skill behavior, the study workspace control repos, existing repo harness patterns in this monorepo
- Downstream: future cultivate invocations, the restarted harness-efficiency study, and any users evaluating `cultivate` as a reusable skill
- Blockers and required coordination: none; this is repo-local and uses local workspace copies only

## Plan of Work

1. Milestone A -- tighten the skill contract and templates around required AGENTS deep-context structure.
2. Milestone B -- strengthen the cultivate audit and evals so the weakly applied treatment pattern is detectable.
3. Milestone C -- dogfood the hardened skill on light/medium/heavy control-repo copies and record the result.

## Concrete Steps

### Milestone A

- [x] Update `skills/cultivate/SKILL.md` to make the stronger AGENTS shape explicit and harder to under-apply.
- [x] Update `skills/cultivate/references/templates.md` so the canonical AGENTS template includes the required deep-context links and execution-plan guidance.
- [x] Bump `skills/cultivate` version and add a changelog entry.

### Milestone B

- [x] Extend `skills/cultivate/scripts/audit_cultivate.py` so it detects weak AGENTS shapes, especially missing deep-context links when the linked docs exist.
- [x] Update `skills/cultivate/evals/evals.json` so the eval set covers the treatment-misapplication failure mode.
- [x] Run repo validation in `skills`.

### Milestone C

- [x] Create light/medium/heavy test copies from the control repos in `$STUDY_WORKSPACE/workdirs/`.
- [x] Apply the hardened cultivate skill to each copy.
- [x] Run the cultivate audit against each copy and confirm the richer AGENTS shape is present.
- [x] Record findings back into this plan and checkpoint in git.

## Validation and Acceptance

- [ ] `uv run python scripts/validate_skills.py` exits 0.
- [ ] `uv run python -m unittest scripts.test_validate_skills` exits 0.
- [ ] The updated audit flags the old weak `fastapi-treatment` style AGENTS shape as missing at least one relevant signal.
- [ ] Light/medium/heavy dogfood copies each end with an `AGENTS.md` that includes a `Deeper Context` section linking into the cultivated knowledge store.

## Idempotence and Recovery

- Skill and template edits are idempotent via git.
- Audit runs are read-only and can be repeated freely.
- Dogfood copies live outside the repo and can be deleted/recreated without affecting the pinned study baselines.

## Progress

- 2026-04-29: Plan created after aborting the first study round. Current diagnosis: the treatment condition was too weakly applied in some repos because cultivate described, but did not strongly enforce, the richer AGENTS shape.
- 2026-04-29: Hardened `skills/cultivate/SKILL.md`, `references/templates.md`, `scripts/audit_cultivate.py`, `evals/evals.json`, and `CHANGELOG.md` around the AGENTS weak-application failure mode.
- 2026-04-29: Validated the `skills` repo after the hardening patch: `uv run python scripts/validate_skills.py` and `uv run python -m unittest scripts.test_validate_skills` both passed.
- 2026-04-29: Re-ran the stronger audit against the old treatment outputs. `fastapi-treatment` now fails `AGENTS structural sections` and `AGENTS deep-context links`; `structlog-treatment` still fails `AGENTS deep-context links`. This confirms the old audit was too forgiving.
- 2026-04-29: Created retest copies at `$STUDY_WORKSPACE/retests/python-tabulate-hardened`, `$STUDY_WORKSPACE/retests/structlog-hardened`, and `$STUDY_WORKSPACE/retests/fastapi-hardened`, then applied the hardened AGENTS shape to each.
- 2026-04-29: The retest copies all pass the new AGENTS structure and deep-context checks. Light (`python-tabulate-hardened`), medium (`structlog-hardened`), and heavy (`fastapi-hardened`) all show `AGENTS structural sections: present` and `AGENTS deep-context links: present`.

## Surprises & Discoveries

- 2026-04-29: The current cultivate audit does not meaningfully distinguish between a rich AGENTS entrypoint and the thin `fastapi-treatment` variant, even though the difference is study-significant.
- 2026-04-29: The stronger audit revealed that the problem was broader than the obvious FastAPI failure. `python-tabulate-treatment` also lacked the canonical section structure, and `structlog-treatment` still orphaned part of the knowledge store despite looking strong on casual inspection.
- 2026-04-29: Using real control-repo copies was worth it. The light repo (`python-tabulate`) lacked a `docs/` tree entirely, which forced the harness application to prove it could create and then properly index the knowledge store rather than only polishing an already-populated tree.

## Decision Log

- 2026-04-29: Use real control-repo copies from the study workspace for the hardening pass instead of tiny fixtures. Reason: the failure mode appeared on real repos with real doc sprawl, so the fix should prove itself there too.
- 2026-04-29: Seed the retest copies with the corresponding treatment harness files, then repair the AGENTS entrypoints to the hardened contract. Reason: this keeps the dogfood pass focused on the failure mode that mattered most to the study -- weak root navigation -- without retyping every harness document from scratch.

## Outcomes & Retrospective

- Milestone A closed 2026-04-29: the skill contract and canonical AGENTS template now treat deep-context linkage as required once cultivated docs exist.
- Milestone B closed 2026-04-29: the audit and eval set now detect the weak-treatment pattern instead of letting it pass.
- Milestone C substantially complete 2026-04-29: light/medium/heavy retest copies all passed the new AGENTS structure and deep-context checks, which is enough evidence to trust the hardening direction before restarting the larger study.

## Artifacts and Notes

- Aborted pilot plan: `docs/exec-plans/active/harness-efficiency-study.md`
- Study workspace: `$STUDY_WORKSPACE`
- Retest copies:
  - `$STUDY_WORKSPACE/retests/python-tabulate-hardened`
  - `$STUDY_WORKSPACE/retests/structlog-hardened`
  - `$STUDY_WORKSPACE/retests/fastapi-hardened`
