# ExecPlan: harness-efficiency-fastapi-ab

Status: complete
Owner: maintainer
Started: 2026-04-29

## Purpose / Big Picture

Run a focused FastAPI restart pilot after the `cultivate` hardening pass. The immediate goal is not to restart the whole study, but to answer one narrower question first: does the hardened root-only harness (`Treatment A`) produce a better agent outcome than raw control on a real FastAPI issue, and if not, does a layered local-guidance variant (`Treatment B`) help?

Success means we complete one concrete FastAPI issue under control and Treatment A, compare the outcomes honestly, and only then add layered local guidance and rerun the same issue as Treatment B. This keeps the treatment evolution interpretable instead of changing multiple variables at once.

## Context and Orientation

- Repository areas touched: `docs/exec-plans/active/`, `docs/exec-plans/active/harness-efficiency-*.jsonl`
- Prior art in this repo: aborted `docs/exec-plans/active/harness-efficiency-study.md`, active `docs/exec-plans/active/cultivate-hardening.md`
- External workspace: `$STUDY_WORKSPACE`
- Selected issue for this pilot: `fastapi/fastapi` issue `#11215`

## Interfaces and Dependencies

- Upstream: pinned FastAPI control checkout, hardened root-only FastAPI treatment copy, issue repro from GitHub issue `#11215`
- Downstream: decision on whether the main study should restart with root-only hardened cultivate or with a layered local-guidance variant
- Blockers: local FastAPI env provisioning and reproducible baseline issue confirmation

## Plan of Work

1. Milestone A -- prepare fresh control and Treatment A sandboxes for FastAPI issue `#11215`, confirm the baseline repro, and log the setup.
2. Milestone B -- run the control vs Treatment A pair, validate outcomes, and record the comparison.
3. Milestone C -- if warranted, add layered local guidance to create Treatment B, rerun against a fresh control sandbox, and compare again.

## Concrete Steps

### Milestone A

- [x] Pick the first FastAPI issue for the restart pilot.
- [x] Create fresh control and Treatment A sandboxes from the pinned workdirs.
- [x] Provision identical local environments and confirm the baseline issue repro in both.

### Milestone B

- [x] Log pilot events for the control and Treatment A runs.
- [x] Run the control issue-fix attempt on a fresh FastAPI sandbox.
- [x] Run the Treatment A issue-fix attempt on a fresh FastAPI sandbox.
- [x] Validate both outcomes with direct repro plus the narrowest relevant pytest slice.
- [x] Append run records to `harness-efficiency-study-runs.jsonl` with distinct task IDs for the root-only variant.

### Milestone C

- [x] Decide whether Treatment A was strong enough or whether layered local guidance is still needed.
- [x] If needed, add nested local guidance to create Treatment B on a fresh FastAPI treatment copy.
- [x] Run a fresh control vs Treatment B comparison on the same issue.
- [x] Append run records for the layered variant and summarize the comparison.

## Validation and Acceptance

- [x] Baseline repro for `#11215` is confirmed in both control and Treatment A before any code edits.
- [x] Control and Treatment A runs are both logged with clear notes and validation summaries.
- [x] If Treatment B is introduced, it is compared on the same issue with a fresh control sandbox.
- [x] `python3 scripts/eval_scorer.py --input docs/exec-plans/active/harness-efficiency-study-runs.jsonl` still exits 0 after logging the new runs.

## Idempotence and Recovery

- Pilot sandboxes live under `$STUDY_WORKSPACE/ab-pilot/` and can be deleted/recreated freely.
- The run/event logs are append-only; distinct task IDs keep this A/B pilot separate from the earlier aborted study rows.
- If one run is interrupted, record it explicitly rather than overwriting or silently retrying.

## Progress

- 2026-04-29: Plan created. Selected `fastapi/fastapi` issue `#11215` for the restart pilot because it has a concrete, self-contained repro and is plausibly sensitive to harness quality in both framework and docs navigation.
- 2026-04-29: Created fresh sandboxes at `$STUDY_WORKSPACE/ab-pilot/fastapi-11215-root-control-r0` and `$STUDY_WORKSPACE/ab-pilot/fastapi-11215-root-treatment-r0`.
- 2026-04-29: Provisioned identical `uv` environments inside both sandboxes and confirmed the baseline issue repro: the endpoint returns `200`, but only `['response']` is observed, which means the injected `BackgroundTasks` work is swallowed by the custom response background task.
- 2026-04-29: Completed the root-only comparison. Control and Treatment A both fixed the issue with the same two-file strategy (`fastapi/routing.py` plus `tests/test_dependency_contextmanager.py`). Treatment A was only slightly narrower at `56` changed lines versus `58` for control, so it was encouraging but not enough signal on its own.
- 2026-04-29: Created fresh layered B sandboxes at `$STUDY_WORKSPACE/ab-pilot/fastapi-11215-layered-control-r0` and `$STUDY_WORKSPACE/ab-pilot/fastapi-11215-layered-treatment-r0`, added nested local `AGENTS.md` files in `fastapi/`, `tests/`, and `docs_src/` to the treatment copy, reprovisioned both environments, and reran the same issue.
- 2026-04-29: Completed the layered comparison. Fresh control again took the broader `56`-line regression path, while Treatment B landed the same two-file fix in `52` changed lines by reusing the existing lifecycle test state instead of introducing new state keys.

## Surprises & Discoveries

- 2026-04-29: The issue is present in both control and the hardened root-only Treatment A sandbox, which is exactly what we want for a fair comparison and also a useful sanity check that the treatment did not accidentally pre-fix the bug.
- 2026-04-29: Fresh FastAPI test environments pulled `python-multipart==0.0.27`, whose `PendingDeprecationWarning` trips this repo's warnings-as-errors pytest configuration during collection. Pinning `python-multipart==0.0.12` restored a symmetric baseline in all four sandboxes; this is a study-environment normalization step, not a treatment difference.
- 2026-04-29: The first layered-treatment regression draft polluted `sync_bg` for a later test because this file intentionally shares mutable module-level state across lifecycle tests. Restoring the shared state at the end of the new regression kept the patch smaller than control while respecting the existing test structure.

## Decision Log

- 2026-04-29: Start with FastAPI issue `#11215` instead of a deeper routing bug. Reason: the issue page contains a concrete minimal repro and a bounded expected behavior, making it a better first restart slice than a broader OpenAPI or router-propagation bug.
- 2026-04-29: Represent root-only and layered variants as distinct task IDs rather than changing the logger schema mid-pilot. Reason: the current study tooling only understands `control` vs `treatment`, so task-level separation is the least disruptive way to compare Treatment A and Treatment B.

## Outcomes & Retrospective

- Root-only hardened `Treatment A` did better than control, but only weakly: same files, same strategy, same observed turns, and only a `2`-line reduction in the regression patch (`56` vs `58`).
- Layered local guidance produced the first clearly stronger FastAPI result in this restarted pilot: same observed turns and same successful fix, but a smaller overall patch (`52` vs `56`) and a more local regression strategy.
- This does not prove the layered variant is universally better, but it is the strongest evidence so far that heavy repos may benefit from nested local guidance beyond the hardened root `AGENTS.md`.

## Artifacts and Notes

- FastAPI issue source: `https://github.com/fastapi/fastapi/issues/11215`
- Control sandbox: `$STUDY_WORKSPACE/ab-pilot/fastapi-11215-root-control-r0`
- Treatment A sandbox: `$STUDY_WORKSPACE/ab-pilot/fastapi-11215-root-treatment-r0`
- Layered control sandbox: `$STUDY_WORKSPACE/ab-pilot/fastapi-11215-layered-control-r0`
- Layered treatment sandbox: `$STUDY_WORKSPACE/ab-pilot/fastapi-11215-layered-treatment-r0`
