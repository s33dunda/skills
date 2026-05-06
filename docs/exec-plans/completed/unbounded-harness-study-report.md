# Unbounded Harness Study Report

Completed: 2026-05-05

## Summary

The unbounded study ran a mixed N=1 fast pass across the six medium/heavy study slots: `requests`, `typer`, `structlog`, `fastapi`, `celery`, and `rich`. Each repo had one navigation prompt, one broad implementation prompt, and one autonomous maintenance prompt. Each task ran once in control and once in the current cultivate treatment for 36 total runs.

Both conditions completed every run with no recorded regressions and no clarification requests. Unlike the first issue-fix study, this pass did show a modest rubric lift for treatment: mean total score was `11.78 / 12` for treatment versus `11.50 / 12` for control.

The lift was not a completion-rate effect. It came from handoff quality and slightly better medium-tier scoping/navigation. Treatment handoff score averaged `3.00` versus `2.78` for control, and medium-tier total score averaged `11.78` versus `11.00`.

## Metrics

| Condition | Runs | Completed | Completion | Mean total score | Navigation | Scope | Validation | Handoff | Mean files | Mean lines | Regressions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Control | 18 | 18 | 100.00% | 11.50 | 2.89 | 2.89 | 2.94 | 2.78 | 1.33 | 19.89 | 0 |
| Treatment | 18 | 18 | 100.00% | 11.78 | 2.94 | 2.83 | 3.00 | 3.00 | 1.33 | 21.67 | 0 |

By task type:

| Task Type | Condition | Runs | Mean total score | Mean files | Mean lines |
| --- | --- | ---: | ---: | ---: | ---: |
| Navigation | Control | 6 | 11.83 | 0.00 | 0.00 |
| Navigation | Treatment | 6 | 12.00 | 0.00 | 0.00 |
| Implementation | Control | 6 | 11.50 | 3.00 | 41.00 |
| Implementation | Treatment | 6 | 11.50 | 2.83 | 36.00 |
| Maintenance | Control | 6 | 11.17 | 1.00 | 18.67 |
| Maintenance | Treatment | 6 | 11.83 | 1.17 | 29.00 |

By tier:

| Tier | Condition | Runs | Mean total score | Mean files | Mean lines |
| --- | --- | ---: | ---: | ---: | ---: |
| Medium | Control | 9 | 11.00 | 1.67 | 27.44 |
| Medium | Treatment | 9 | 11.78 | 1.56 | 29.11 |
| Heavy | Control | 9 | 12.00 | 1.00 | 12.33 |
| Heavy | Treatment | 9 | 11.78 | 1.11 | 14.22 |

## Interpretation

The unbounded pass supports a slightly stronger cultivate claim than the issue-fix pass: when prompts require architecture navigation, judgment about where to land changes, and a concise handoff, treatment outputs were more consistently complete and easier to evaluate.

The strongest treatment signal was in the medium tier. Treatment produced clearer before/after repros and risk handoffs for `typer`, `structlog`, and `requests`, while control sometimes landed valid changes with less explanation or broader diffs. On heavy repos, control was already near-ceiling in this N=1 pass, so there was little room for the harness to improve the rubric score.

Churn did not improve overall. Treatment changed fewer lines on implementation tasks (`36.00` vs `41.00`) but more lines on maintenance tasks (`29.00` vs `18.67`). The fair conclusion is that treatment improved answer quality and handoff more than patch size.

## Notable Examples

- `typer-implementation-current`: treatment included a direct failing repro for result-callback context propagation, a narrower two-file patch, focused tests, and a clear handoff; control also completed, but with a broader four-file patch and weaker handoff.
- `structlog-maintenance-current`: treatment added a more directly relevant callsite/process guardrail, while control added useful but less central processor coverage.
- `httpx-implementation-current`: both conditions solved the same body-length issue; treatment produced a smaller patch while preserving direct repro and focused test evidence.
- `fastapi-implementation-current` and `rich-implementation-current`: control scored as well or better on scope, showing that the harness does not dominate when the raw repo is already easy to navigate or the chosen treatment change is broader.

## Method Notes

- Control and treatment workers were condition-isolated: each worker saw only one repo/condition baseline and wrote pending records outside the central log.
- Navigation tasks were no-code and scored primarily on answer accuracy, ownership mapping, test targets, and clean-sandbox evidence.
- Implementation and maintenance diffs were left uncommitted in disposable sandboxes under `$STUDY_WORKSPACE/runs/`.
- Scores were assigned parent-side against the manifest answer-key anchors after reading pending records and artifacts.
- Turn counts are parent-observed proxies set to `2` for all runs; stable API-grade token telemetry was not available.

## Conclusion

This unbounded study gives cultivate a more favorable but still modest result: equal completion, zero regressions, and a small rubric lift concentrated in handoff and medium-tier task quality. It does not show a broad churn reduction. The best current claim is that cultivate helps agents produce more legible and reviewable work on ambiguous tasks, especially when repository structure is non-trivial but not so mature that raw navigation is already obvious.

## Artifacts

- Task manifest: `docs/exec-plans/active/unbounded-harness-study-tasks.md`
- Run log: `docs/exec-plans/active/unbounded-harness-study-runs.jsonl`
- Scorer: `scripts/unbounded_eval_scorer.py`
- Pending records: `$STUDY_WORKSPACE/logs/unbounded-pending-runs/`
- Run artifacts: `$STUDY_WORKSPACE/logs/unbounded-artifacts/`
- JSON summary: `$STUDY_WORKSPACE/logs/unbounded-summary.json`
