# Harness Efficiency Study Report

Completed: 2026-05-04

## Summary

The completed current-treatment pass compared raw pinned repositories against the current `cultivate` treatment, where the treatment repos use the layered harness protocol formerly called Treatment B.

The study covered all 45 issue slots from the manifest, with paired control and treatment rows for each slot. Both conditions completed the same number of runnable tasks: 34 completed and 11 non-repro or environment skips per condition. No new regressions were recorded in either condition.

The clearest measured difference was not completion rate. It was solution shape: treatment averaged slightly fewer changed lines in the current pass, and a few tasks showed materially narrower treatment patches. The effect was smaller than the earlier pilot suggested because many fast-pass runs converged to identical file and line counts.

## Current-Pass Metrics

Current-pass rows include task IDs ending in `-current` plus the earlier layered rows ending in `-layered`.

| Condition | Runs | Completed | Completion | Mean files | Mean lines | Mean lines, completed only | Regressions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Control | 45 | 34 | 75.56% | 1.87 | 35.98 | 47.62 | 0 |
| Treatment | 45 | 34 | 75.56% | 1.87 | 35.29 | 46.71 | 0 |

By tier:

| Tier | Condition | Runs | Completed | Mean lines | Mean lines, completed only |
| --- | --- | ---: | ---: | ---: | ---: |
| Light | Control | 15 | 12 | 32.40 | 40.50 |
| Light | Treatment | 15 | 12 | 30.60 | 38.25 |
| Medium | Control | 15 | 10 | 31.93 | 47.90 |
| Medium | Treatment | 15 | 10 | 31.93 | 47.90 |
| Heavy | Control | 15 | 12 | 43.60 | 54.50 |
| Heavy | Treatment | 15 | 12 | 43.33 | 54.17 |

Among the 34 task pairs where both conditions completed, treatment changed fewer lines in 3 pairs, the same number in 28 pairs, and more lines in 3 pairs. Mean line delta was `-0.91` lines for treatment minus control; median delta was `0`.

Largest treatment-smaller examples:

- `arrow-1269-layered`: control 102 lines, treatment 38 lines.
- `python-tabulate-357-layered`: control 173 lines, treatment 154 lines.
- `fastapi-11215-layered`: control 56 lines, treatment 52 lines.

Largest treatment-larger examples:

- `python-tabulate-354-layered`: control 48 lines, treatment 75 lines.
- `arrow-1237-layered`: control 16 lines, treatment 35 lines.
- `arrow-1210-layered`: control 12 lines, treatment 22 lines.

## Interpretation

The current `cultivate` harness did not improve task completion rate in this pass. Both conditions completed the same runnable tasks and skipped the same non-reproducing or environment-mismatched tasks.

The evidence for efficiency is modest but positive on churn: treatment averaged slightly fewer changed lines overall and produced several narrower patches on tasks where the harness pointed agents toward local ownership and validation. The median pairwise delta was zero, so the right claim is not "cultivate always makes patches smaller." The better claim is: when the task has meaningful navigation ambiguity, the harness can reduce solution breadth; when the task is already locally obvious, both conditions converge.

The study also validated an important negative result: issue metadata alone is not enough. Eleven issue slots per condition were non-reproducible or not represented in the pinned baseline/environment. Preflight repro checks are part of the study method, not administrative overhead.

## Method Notes

- Control repos were pinned raw upstream checkouts.
- Treatment repos were pinned at the same upstream SHAs with the current cultivate harness applied.
- The active treatment condition is the layered protocol formerly called Treatment B.
- Runs used fresh disposable sandboxes under `$STUDY_WORKSPACE/runs/`; baseline `workdirs/` were not mutated.
- Token usage was not measured because the execution path did not expose stable API-grade usage data.
- Turn counts for the fast-pass rows are parent-observed proxies, not exact subagent-internal telemetry.
- Validation emphasized direct repros and focused tests. Broader suites were run when practical for the repo and environment.

## Conclusion

The completed study supports a narrower claim than the original ambition: the current cultivate harness is reliable as a treatment and can reduce patch breadth on navigation-sensitive tasks, but this dataset does not show a completion-rate lift. The most defensible user-facing result is a mixed but useful efficiency signal: equal success, zero recorded regressions, and slightly lower mean changed lines for treatment, with strong task-level examples and several counterexamples.

## Artifacts

- Issue manifest: `docs/exec-plans/active/harness-efficiency-study-issues.md`
- Run log: `docs/exec-plans/active/harness-efficiency-study-runs.jsonl`
- Event log: `docs/exec-plans/active/harness-efficiency-study-events.jsonl`
- External workspace: `$STUDY_WORKSPACE`
- Current pass protocol: `$STUDY_WORKSPACE/logs/current-pass-protocol.md`
- Pending-run merge summary: `$STUDY_WORKSPACE/logs/current-pass-merge-summary.md`
