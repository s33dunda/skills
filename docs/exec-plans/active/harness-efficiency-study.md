# ExecPlan: harness-efficiency-study

Status: active
Owner: s33dunda
Started: 2026-04-28

## Purpose / Big Picture

Produce empirical data showing that applying a cultivate harness to an open-source repository measurably improves AI agent efficiency on real engineering tasks. The study compares harnessed repos (treatment) against matched raw repos (control) using real open GitHub issues as the task battery.

Success means a reproducible dataset with task completion rates, turns-to-completion, and regression rates for both conditions across three complexity tiers — or a documented null result with enough data to draw a conclusion either way.

## Context and Orientation

- Study design: between-subjects, two conditions per repo. Control = raw repo at a fixed commit. Treatment = same commit + cultivate harness applied via this skill.
- Complexity tiers: light, medium, heavy (three repos per tier, nine total).
- Task source: real open GitHub issues from each repo — problem definition, repro steps, and expected behavior are already validated by the project community.
- Prior art in this repo: `skills/cultivate/SKILL.md`, `skills/cultivate/references/harness-engineering.md`.
- Tracking: per-run structured log (JSON) capturing turn count, token usage, test pass rate, regression count, clarification requests. Logging infrastructure is Milestone C.

## Interfaces and Dependencies

- Upstream: GitHub issues for each target repo, pinned at a specific commit SHA.
- Downstream: comparative analysis report — treatment vs. control per tier and in aggregate.
- Blockers: eval logging infrastructure (Milestone C) must land before Milestone D runs begin.

## Repo Selection

| Tier | Repo | Rationale |
| --- | --- | --- |
| Light | `jmoiron/humanize` | Tiny domain (~1.5K LoC), clear API surface, active issue tracker |
| Light | `astanin/python-tabulate` | Single-module, well-tested, real bug reports |
| Light | `un33k/python-slugify` | Minimal (~300 LoC), deterministic, good floor data point |
| Medium | `encode/httpx` | Layered architecture, real-world HTTP semantics, large issue backlog |
| Medium | `tiangolo/typer` | CLI framework, clear boundaries, community-filed bugs |
| Medium | `hynek/structlog` | Structured logging, good test coverage, maintained |
| Heavy | `tiangolo/fastapi` | Complex web framework, massive issue tracker, real-world scope |
| Heavy | `celery/celery` | Distributed task queue, deep architecture, long-lived bugs |
| Heavy | `Textualize/rich` | Large but readable, excellent test suite, active issues |

## Task Battery

**Five tasks per repo, sourced from open GitHub issues.** For each repo, select issues that meet all of the following:

- Open at the time of repo pinning (not yet resolved).
- Has a clear problem statement and reproduction steps (or expected vs. actual behavior).
- Is bounded: a senior developer could attempt a fix in under two hours.
- Spans a mix of `bug` and `enhancement`/`feature` labels where the repo's labeling allows.

**Selection process per repo:**
1. Search open issues with labels `bug`, `enhancement`, or `good first issue`.
2. Pick 5 issues at varying difficulty. Record issue number, title, and URL.
3. Pin the repo at the commit SHA immediately before any fix for each selected issue (so the bug is present at the pinned state).

**Navigation / architecture tasks** are not sourced from issues — they are synthetic prompts ("explain how X is implemented", "where would you add Y?"). These are scored against ground truth from the codebase, not by test suite.

If a repo has insufficient labelled issues, substitute with issues that have clear discussion and attempted PRs (the community already validated the problem).

## Metrics

| Metric | How measured |
| --- | --- |
| Task completion | Pass/fail: does the change make the described issue's repro case pass, and does the existing test suite stay green? |
| Turns to completion | Count of agent conversation turns (tool calls + responses) until task is marked done or abandoned |
| Test pass rate | `pytest` (or repo-equivalent) green % after the agent's changes |
| Regression count | Tests that were green before the task, red after |
| Token usage | Input + output tokens from API call logs (requires running via API, not interactive UI) |
| Clarification requests | Count of turns where the agent asks the user a question rather than proceeding |

**Tracking note**: token usage and turn count require either API-mediated runs (where call logs are available) or a wrapping eval harness (Milestone C). For the first pass, turns and completion can be logged manually from agent session transcripts. Regressions are always mechanical (`pytest` diff).

## Plan of Work

1. **Milestone A** — Repo selection and issue curation: pin each repo at a commit SHA, select 5 open issues per repo, record selection in a structured manifest.
2. **Milestone B** — Treatment repo setup: apply cultivate harness to treatment forks of all nine repos.
3. **Milestone C** — Eval logging infrastructure: build a lightweight script that records per-run metrics to a structured JSON log.
4. **Milestone D** — Eval runs: run each task N=5 times per condition (control and treatment) using the logging harness.
5. **Milestone E** — Scoring and analysis: score results, produce per-tier and aggregate comparison report.

## Concrete Steps

### Milestone A

- [ ] For each repo in the selection table, identify the most recent commit SHA before the earliest selected issue was filed or its fix was merged.
- [ ] Select 5 open issues per repo meeting the criteria above. Record in `docs/exec-plans/active/harness-efficiency-study-issues.md` (issue number, URL, label, difficulty estimate, pinned SHA).
- [ ] Confirm issues are still open and unresolved at the pinned SHA for each repo.

### Milestone B

- [ ] Fork or clone each repo at its pinned SHA into a paired `<repo>-control/` and `<repo>-treatment/` working directory.
- [ ] Run `/cultivate` on each treatment directory; commit the resulting harness files.
- [ ] Confirm control directories have no harness files beyond what the upstream repo already ships.

### Milestone C

- [ ] Write `scripts/eval_logger.py`: accepts a run result (repo, condition, task id, turns, tokens, tests_before, tests_after, clarification_count) and appends to `docs/exec-plans/active/harness-efficiency-study-runs.jsonl`.
- [ ] Write `scripts/eval_scorer.py`: reads the JSONL log and produces per-tier and aggregate summary tables (completion rate, mean turns, mean regressions).
- [ ] Add a test for both scripts in `scripts/test_eval_tools.py`.

### Milestone D

- [ ] For each of the 45 tasks (9 repos × 5 tasks), run the task against both control and treatment, N=5 times each.
- [ ] Log each run via `eval_logger.py` immediately after completion.
- [ ] Flag any task where the correct answer is ambiguous for human scoring in Milestone E.

### Milestone E

- [ ] Run `eval_scorer.py` to generate the draft summary tables.
- [ ] Human-score any flagged ambiguous completions against the rubric: did the change address the issue's stated problem without regressing the test suite?
- [ ] Write `docs/exec-plans/completed/harness-efficiency-study-report.md` with findings.
- [ ] Move this plan to `docs/exec-plans/completed/`.

## Validation and Acceptance

- [ ] `docs/exec-plans/active/harness-efficiency-study-issues.md` exists with 45 rows (9 repos × 5 issues).
- [ ] Each treatment repo has a committed cultivate harness and `uv run python skills/cultivate/scripts/audit_cultivate.py <path>` shows no critical gaps.
- [ ] `docs/exec-plans/active/harness-efficiency-study-runs.jsonl` contains at least 450 entries (45 tasks × 2 conditions × 5 runs).
- [ ] `eval_scorer.py` exits 0 and produces a summary table.
- [ ] Report is written and this plan is moved to `completed/`.

## Idempotence and Recovery

- Issue selection (Milestone A) is idempotent: re-running the selection process on the same repos and SHAs must produce the same manifest.
- Eval runs (Milestone D) append to the JSONL log. Partial runs can be resumed by checking which (repo, condition, task, run_index) tuples are already in the log.
- Treatment harness application (Milestone B) is idempotent via git: re-running cultivate on an already-cultivated fork produces no new changes.

## Progress

- 2026-04-28: ExecPlan created. Repo selection and metric design finalized. Milestone A is next.

## Surprises & Discoveries

_(none yet)_

## Decision Log

- 2026-04-28: Use real open GitHub issues as the task battery instead of synthetic tasks. Reason: the community has already done the work to identify and validate real problems, providing ground truth without additional curation effort.
- 2026-04-28: Keep navigation/architecture tasks synthetic (2 of 5 per repo). Reason: open issues rarely ask "explain how X works" — those questions have no clear issue analog but are high-signal for harness value.
- 2026-04-28: N=5 runs per condition per task. Reason: enough variance for Mann-Whitney U and Fisher's exact test without requiring a large compute budget.
- 2026-04-28: Continuous execution model — no fixed end date. Reason: user preference; milestone gates drive progress rather than calendar dates.

## Outcomes & Retrospective

_(filled in as milestones close)_

## Artifacts and Notes

- Issue manifest (to be created): `docs/exec-plans/active/harness-efficiency-study-issues.md`
- Run log (to be created): `docs/exec-plans/active/harness-efficiency-study-runs.jsonl`
- Final report (to be created): `docs/exec-plans/completed/harness-efficiency-study-report.md`
