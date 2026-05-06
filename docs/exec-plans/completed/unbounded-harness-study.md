# ExecPlan: unbounded-harness-study

Status: completed
Owner: maintainer
Started: 2026-05-05
Completed: 2026-05-05

## Purpose / Big Picture

Run a second cultivate evaluation on medium/heavy repositories using tasks that are deliberately less bounded than issue fixes. The first completed study showed equal completion and only modest churn reduction; this study tests the hypothesis that cultivate helps more when agents must navigate, scope, validate, and explain work without file pointers.

Success means a reproducible mixed-task dataset with paired control/treatment rows for navigation, broad implementation, and autonomous maintenance prompts across six medium/heavy repos.

## Context and Orientation

- Repository areas touched: `docs/exec-plans/active/`, `docs/exec-plans/completed/`, `scripts/`
- Prior art in this repo: `docs/exec-plans/completed/harness-efficiency-study-report.md`, `docs/exec-plans/active/harness-efficiency-study.md`
- External workspace: `$STUDY_WORKSPACE` (`/Users/cdunda/Code/harness-efficiency-study` on the current host)
- Starting state: active treatment workdirs use current cultivate layered protocol at `$STUDY_WORKSPACE/workdirs/*-treatment`; root-only historical treatment dirs are deprecated.

## Interfaces and Dependencies

- Upstream: pinned medium/heavy control and treatment workdirs from the completed harness-efficiency study.
- Downstream: `docs/exec-plans/completed/unbounded-harness-study-report.md`.
- Blockers: none expected; runs can be skipped or scored low when a prompt cannot be validated in the pinned checkout.

## Plan of Work

1. Milestone A -- Create the unbounded ExecPlan, manifest, logger, and scorer.
2. Milestone B -- Run paired control/treatment agents for the mixed task battery.
3. Milestone C -- Human-score records, summarize results, and write the report.

## Concrete Steps

### Milestone A

- [x] Add `scripts/unbounded_eval_logger.py`.
- [x] Add `scripts/unbounded_eval_scorer.py`.
- [x] Extend `scripts/test_eval_tools.py` with unbounded logger/scorer coverage.
- [x] Create `docs/exec-plans/active/unbounded-harness-study-tasks.md` with 18 prompts and answer-key anchors.

### Milestone B

- [x] Verify six selected control/treatment workdirs are clean.
- [x] Create fresh run sandboxes under `$STUDY_WORKSPACE/runs/`.
- [x] Dispatch paired control/treatment runs for each task.
- [x] Collect pending JSONL records under `$STUDY_WORKSPACE/logs/unbounded-pending-runs/`.

### Milestone C

- [x] Merge validated pending records into `docs/exec-plans/active/unbounded-harness-study-runs.jsonl`.
- [x] Run `uv run python scripts/unbounded_eval_scorer.py --input docs/exec-plans/active/unbounded-harness-study-runs.jsonl`.
- [x] Human-score rubric fields where the worker left `needs_human_scoring=true`.
- [x] Write `docs/exec-plans/completed/unbounded-harness-study-report.md`.
- [x] Record final validation evidence in this plan.

## Validation and Acceptance

- [x] `docs/exec-plans/active/unbounded-harness-study-tasks.md` exists with 18 task rows.
- [x] `docs/exec-plans/active/unbounded-harness-study-runs.jsonl` has 36 paired rows.
- [x] `uv run python scripts/unbounded_eval_scorer.py --input docs/exec-plans/active/unbounded-harness-study-runs.jsonl` exits 0.
- [x] `uv run python scripts/validate_skills.py` exits 0.
- [x] `uv run python -m unittest scripts.test_validate_skills` exits 0.
- [x] `uv run python -m unittest scripts.test_eval_tools` exits 0.

## Idempotence and Recovery

- Run sandboxes are disposable. Delete and recreate `$STUDY_WORKSPACE/runs/<task_id>-<condition>-r0` from the matching baseline when retrying.
- Pending records are staged outside the repo first so the parent can validate and de-duplicate before appending to the central JSONL.
- The completed issue-fix log remains separate and should not be modified by this study.

## Progress

- 2026-05-05: Plan created. Dedicated unbounded logger/scorer scripts added; task manifest is next.
- 2026-05-05: Task manifest created with 18 medium/heavy mixed prompts. Logger/scorer unit tests passed, all six selected control/treatment workdirs were clean, and treatment audits passed key cultivate signals before dispatch.
- 2026-05-05: Twelve condition-isolated workers completed 36 runs and wrote pending records/artifacts. Parent-side scoring merged all rows into `docs/exec-plans/active/unbounded-harness-study-runs.jsonl` and generated `docs/exec-plans/completed/unbounded-harness-study-report.md`.
- 2026-05-05: Final validation passed: `uv run python scripts/validate_skills.py`, `uv run python -m unittest scripts.test_validate_skills`, and `uv run python -m unittest scripts.test_eval_tools`.

## Surprises & Discoveries

- 2026-05-05: The previous issue-fix dataset mainly measured bounded local fixes, so the new task battery intentionally omits file pointers and includes no-code navigation prompts.
- 2026-05-05: To reduce cross-condition leakage on navigation tasks, each repo/condition pair is run by a separate worker rather than one worker handling both control and treatment.

## Decision Log

- 2026-05-05: Limited the study to medium/heavy repos. Reason: the previous light-tier data showed the least room for harness advantage, while the cultivate hypothesis is strongest for multi-surface repositories.
- 2026-05-05: Kept the unbounded run log separate from `harness-efficiency-study-runs.jsonl`. Reason: the rubric fields and task semantics differ enough that mixing logs would make scorer output ambiguous.

## Outcomes & Retrospective

- Milestone A closed 2026-05-05: unbounded manifest, logger, scorer, and unit coverage were added.
- Milestone B closed 2026-05-05: all 36 paired runs completed with no missing records.
- Milestone C closed 2026-05-05: treatment scored `11.78 / 12` mean total versus control `11.50 / 12`; report written at `docs/exec-plans/completed/unbounded-harness-study-report.md`.

## Artifacts and Notes

- Task manifest: `docs/exec-plans/active/unbounded-harness-study-tasks.md`
- Run log: `docs/exec-plans/active/unbounded-harness-study-runs.jsonl`
- Pending records: `$STUDY_WORKSPACE/logs/unbounded-pending-runs/`
- Final report: `docs/exec-plans/completed/unbounded-harness-study-report.md`
