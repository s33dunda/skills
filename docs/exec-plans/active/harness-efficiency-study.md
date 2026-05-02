# ExecPlan: harness-efficiency-study

Status: paused for treatment hardening (pilot data retained; resume with layered treatment)
Owner: maintainer
Started: 2026-04-28

## Pause Status

This study round is intentionally paused as a mainline evaluation pass.

Reason: the original treatment condition was too weakly applied in a non-trivial subset of the cultivated repos, so continued control-vs-treatment runs would spend additional cycles on a condition we no longer trust as a clean representation of the intended cultivate treatment.

What remains valid:

- the issue manifest and repo pinning work from Milestone A
- the control/treatment workspace setup from Milestone B
- the eval logger, scorer, event logger, and turn-backfill tooling from Milestone C
- the completed run logs as pilot data and process evidence

What is not valid enough to treat as final study evidence:

- any strong user-facing claim that the current treatment condition represents a consistently and correctly applied cultivate harness across all study repos

Reuse path after the skill fix:

- keep this plan as the pilot record
- copy or supersede it with a fresh active ExecPlan after cultivate is strengthened and the treatment application protocol is re-run
- only resume Milestone D mainline evals once treatment validity has been re-audited across all study repos
- compare the hardened root treatment against the layered treatment before deciding whether layered local `AGENTS.md` files become the default study condition

## Purpose / Big Picture

Produce empirical data showing that applying a cultivate harness to an open-source repository measurably improves AI agent efficiency on real engineering tasks. The study compares harnessed repos (treatment) against matched raw repos (control) using real open GitHub issues as the task battery.

Success means a reproducible dataset with task completion rates, turns-to-completion, and regression rates for both conditions across three complexity tiers — or a documented null result with enough data to draw a conclusion either way.

## Context and Orientation

- Study design: between-subjects, two conditions per repo. Control = raw repo at a fixed commit. Treatment = same commit + cultivate harness applied via this skill.
- Complexity tiers: light, medium, heavy (three repos per tier, nine total).
- Task source: real open GitHub issues from each repo — problem definition, repro steps, and expected behavior are already validated by the project community.
- Prior art in this repo: `skills/cultivate/SKILL.md`, `skills/cultivate/references/harness-engineering.md`.
- External prior art: `docs/references/harness-efficiency-prior-art.md` — OpenAI blog case study, SWE-bench repo variance data, Crosley AGENTS.md patterns, Friel ExecPlans, code agent failure trajectories.
- Tracking: per-run structured log (JSON) capturing turn count, token usage, test pass rate, regression count, clarification requests, files touched, lines changed. Logging infrastructure is Milestone C.

## Prior Art Summary

Three published findings directly shape this study's design. Full citations and notes in `docs/references/harness-efficiency-prior-art.md`.

**1. SWE-bench: ~5x repo-level variance in agent success rates** (Jimenez et al., ICLR 2024; Yang et al., NeurIPS 2024). Some repos see <10% resolution, others >50% — purely from repo characteristics, not model choice. Task success also degrades with files modified and lines changed. *Design implication:* run both conditions on the same repos and tasks (our between-subjects design already handles this). Log `files_touched` and `lines_changed` as covariates — if treatment agents navigate faster they should touch fewer files.

**2. Prose-only AGENTS.md → zero behavioral change** (Crosley, Feb 2026). The patterns that measurably change agent behavior are command-first instructions with verifiable exit codes, explicit Definition of Done, and a Never list. *Design implication:* treatment AGENTS.md must include Useful Commands and Definition of Done, not just structured prose. Milestone B validation must verify this.

**3. OpenAI harness case study: 3.5 PRs/engineer/day at ~1M LoC** (Lopopolo, Feb 2026). Observational, no control group — that's the gap this study closes. Also: encoding "golden principles" as mechanical checks eliminated 20% weekly cleanup time (every Friday). *Design implication:* sets a plausible upper bound on effect size; helps interpret results (if our effect is large, it's consistent with published evidence; if small, it's a genuine finding about the marginal value of harness in isolation from team culture).

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
| Token usage | Input + output tokens when a stable source is available (`API` preferred; subagent notifications are opportunistic only) |
| Clarification requests | Count of turns where the agent asks the user a question rather than proceeding |
| Files touched | Count of distinct files the agent modified (covariate — SWE-bench shows success degrades with this) |
| Lines changed | Net lines added + deleted (covariate — same degradation signal as files touched) |

**Tracking note**: token usage is optional in the first pass. When runs happen through the monthly ChatGPT/Codex account or subagents, the logger records `usage_source` and may leave token fields empty. If we later want authoritative token-efficiency metrics, the evals need to run through the OpenAI API (or another provider that exposes equivalent usage metadata), which in practice means provisioning an API key and accepting separate API billing. The same logger schema can then store authoritative `tokens_input` / `tokens_output` values from API responses. Turns, completion, regressions, files touched, and lines changed remain the primary cross-condition metrics in the monthly-account path.

## Plan of Work

1. **Milestone A** — Repo selection and issue curation: pin each repo at a commit SHA, select 5 open issues per repo, record selection in a structured manifest.
2. **Milestone B** — Treatment repo setup: apply cultivate harness to treatment forks of all nine repos.
3. **Milestone C** — Eval logging infrastructure: build a lightweight script that records per-run metrics to a structured JSON log.
4. **Milestone D** — Eval runs: run each task N=5 times per condition (control and treatment) using the logging harness.
5. **Milestone E** — Scoring and analysis: score results, produce per-tier and aggregate comparison report.

## Concrete Steps

### Milestone A

- [x] For each repo in the selection table, identify the most recent commit SHA before the earliest selected issue was filed or its fix was merged.
- [x] Select 5 open issues per repo meeting the criteria above. Record in `docs/exec-plans/active/harness-efficiency-study-issues.md` (issue number, URL, label, difficulty estimate, pinned SHA).
- [x] Confirm issues are still open and unresolved at the pinned SHA for each repo.

### Milestone B

- [x] Fork or clone each repo at its pinned SHA into a paired `<repo>-control/` and `<repo>-treatment/` working directory.
- [x] Run `/cultivate` on each treatment directory; commit the resulting harness files.
- [x] Confirm control directories have no harness files beyond what the upstream repo already ships.
- [x] Verify that each treatment AGENTS.md contains at least one executable command block and an explicit Definition of Done (prose-only AGENTS.md produces zero behavioral change per Crosley 2026).

### Milestone C

- [x] Write `scripts/eval_logger.py`: accepts a run result (repo, condition, task id, turns, completion outcome, clarification_count, files_touched, lines_changed, regressions, optional token usage, and optional test-status fields) and appends to `docs/exec-plans/active/harness-efficiency-study-runs.jsonl`.
- [x] Write `scripts/eval_scorer.py`: reads the JSONL log and produces per-tier and aggregate summary tables (completion rate, mean turns, mean regressions, and optional token summaries when usage data is present).
- [x] Add a test for both scripts in `scripts/test_eval_tools.py`.

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
- 2026-04-28: Milestone A manifest created at `docs/exec-plans/active/harness-efficiency-study-issues.md` with 45 curated issue tasks and pinned SHAs for all nine study slots.
- 2026-04-28: Re-verified the issue manifest against GitHub. All 45 selected issues remain open, and all nine pinned SHAs predate the earliest selected issue for their repo.
- 2026-04-28: Milestone B setup started. External study workspace chosen at `$STUDY_WORKSPACE` so paired control/treatment repos do not pollute this monorepo's working tree.
- 2026-04-28: Created all nine cached upstream clones plus paired control/treatment worktrees at the pinned SHAs under `$STUDY_WORKSPACE/workdirs`.
- 2026-04-28: Verified the nine control repos are pristine and contain zero upstream `AGENTS.md`, `AGENTS.override.md`, or `CLAUDE.md` files.
- 2026-04-28: Applied the cultivate harness to all nine treatment repos and committed each treatment harness on a local `study-cultivate` branch.
- 2026-04-28: Ran a Milestone B acceptance sweep: all nine treatment repos are clean, all nine `AGENTS.md` files contain command-first validation guidance plus explicit completion criteria, and the cultivate audit now shows only non-blocking repo-specific gaps such as missing environment-isolation conventions or agent-usable scripts.
- 2026-04-28: Implemented `scripts/eval_logger.py`, `scripts/eval_scorer.py`, and `scripts/test_eval_tools.py` for the opportunistic-token Milestone C path.
- 2026-04-28: Smoke-tested the logger/scorer on a temporary JSONL file and ran `python3 scripts/test_eval_tools.py`, `uv run python scripts/validate_skills.py`, and `uv run python -m unittest scripts.test_validate_skills`.
- 2026-04-28: Ran the first Milestone D pilot pair against `un33k/python-slugify` issue `#167` using disposable `runs/` sandboxes and lightweight subagents for the control and treatment conditions.
- 2026-04-28: Logged the first two real run records to `docs/exec-plans/active/harness-efficiency-study-runs.jsonl` and confirmed that `scripts/eval_scorer.py` can summarize a mixed-condition pilot log end to end.
- 2026-04-28: Ran the first code-path Milestone D pair against `un33k/python-slugify` issue `#175` after pre-provisioning matching Python 3.11 virtualenvs in both run sandboxes. Both control and treatment fixed the CLI bug, added a targeted regression test, and passed the direct CLI repro plus focused `unittest` checks.
- 2026-04-28: Ran the next bounded Milestone D pair against `un33k/python-slugify` issue `#169`. Both control and treatment correctly recognized that the runtime behavior was already correct at the pinned SHA and limited their changes to focused regression tests.
- 2026-04-28: Ran the first higher-signal non-slugify pair against `astanin/python-tabulate` issue `#427`. Both conditions fixed the HTML alignment bug, but the control run also edited `README.md` while the treatment run stayed within implementation and tests.
- 2026-04-28: Ran a second `astanin/python-tabulate` pair against issue `#354`. Both conditions fixed the width overflow bug and restored the repro to a 105-character line cap, but they took different implementation and regression-test paths.
- 2026-04-28: Ran the first `arrow-py/arrow` pair against issue `#1259`. Both conditions fixed the `tzinfo=None` factory crash and added a focused regression test, while taking slightly different implementation hooks inside `ArrowFactory.get`.
- 2026-04-28: Started accumulating repeat runs on proven tasks. The second `astanin/python-tabulate` issue `#427` pair (`run_index=1`) again succeeded in both conditions, but this time control took a much broader internal-plumbing path than treatment while still landing the same user-visible behavior.
- 2026-04-28: Repeated `arrow-py/arrow` issue `#1259` (`run_index=1`). Both conditions again solved the crash with the same two-file scope, but converged even more tightly than the first pair: both fixes stayed within `ArrowFactory.get` and a focused `tests/test_factory.py` regression.
- 2026-04-28: Repeated `astanin/python-tabulate` issue `#354` (`run_index=1`). Both conditions again fixed the width bug and passed the full `pytest` suite, but treatment found a much smaller implementation while preserving the same 105-character output cap.
- 2026-04-29: Ran the first `arrow-py/arrow` pair against issue `#1269`. Both conditions taught `dehumanize()` to accept shortened English units (`mins`, `secs`) and passed the focused `dehumanize` pytest slice plus the direct repro, but treatment kept the fix narrower by staying out of locale parsing.
- 2026-04-29: Added real-time event logging helpers for interrupted or resumed eval runs. `scripts/eval_event_logger.py` appends parent-observed run-state events, and `scripts/eval_event_recover.py` summarizes the latest per-run event trail plus the highest observed turn index without claiming hidden subagent-internal turns.
- 2026-04-30: Added model tracking to the event log and compact readout table. Reason: the original pilot mostly used `gpt-5.4-mini`, the FastAPI A/B pilot used `gpt-5.4`, and the Arrow Treatment B restart used `gpt-5`; model must therefore be treated as a run parameter, not background trivia.
- 2026-04-29: Ran the first `arrow-py/arrow` pair against issue `#1237` with the new live event log enabled. Both conditions fixed the mixed-decimal `dehumanize()` bug, passed the exact direct repro, and passed both the focused `dehumanize` slice and the full `tests/test_arrow.py` file; treatment again landed the narrower patch.
- 2026-04-29: Ran the first `astanin/python-tabulate` pair against issue `#357` with the live event log enabled. Both conditions implemented grouped column separators for `fancy_outline`, passed the exact grouped-header repro, and passed both the focused `fancy_outline` slice and the full `test/test_output.py` file; treatment again achieved the same user-visible output with a smaller patch.
- 2026-04-29: Repeated `astanin/python-tabulate` issue `#357` (`run_index=1`). Both conditions again implemented the grouped separator boundary and passed the same focused `fancy_outline` slice, but control widened further on the repeat while treatment stayed almost exactly on its original narrow path.
- 2026-04-29: Ran the first `astanin/python-tabulate` pair against issue `#358`. Both conditions added bounded `typst` formatter support, passed the direct `tablefmt='typst'` repro, and passed the focused `typst` slice plus the full `test/test_output.py` file. This time treatment was slightly broader in file scope because it also updated README/help discoverability.
- 2026-04-29: Added explicit turn provenance to the run log (`exact`, `observed`, `missing`) plus a backfill utility that derives parent-observed turns from the event log. The current study log was backfilled for 8 recent event-logged runs so users can see recorded turn data in the JSONL instead of only in scorer output.
- 2026-04-29: Ran the first medium-tier pair against `psf/requests` issue `#6890`. Both conditions fixed the escaped-quote cookie corruption bug, passed the direct repro, and passed a focused cookie regression slice. The broader `tests/test_requests.py` file still has a preexisting unrelated mTLS/TLS certificate failure in the baseline checkout, so the pair is logged as a successful fix with `regression_count = 0` rather than as a green-full-suite run.
- 2026-04-29: Started `psf/requests` issue `#6917` and hit a subagent usage-limit interruption before any tracked code edits landed. Instead of dropping the attempt on the floor, the study now records it as an explicit non-completed `run_index=0` pair with preflight repro/test telemetry, parent-observed turns, and `run_abandoned` event-log termini so a later retry can use `run_index=1` without overwriting the interruption evidence.
- 2026-04-29: Retried `psf/requests` issue `#6917` as `run_index=1` after the quota window reset. Both conditions fixed the UTF-8 `StringIO` `Content-Length` bug and passed the direct repro, but they diverged in scope: control stayed in `src/requests/utils.py` plus `tests/test_utils.py`, while treatment also added a focused `PreparedRequest` regression in `tests/test_requests.py`.
- 2026-04-29: Ran the first medium-tier pair against `psf/requests` issue `#6990`. Both conditions fixed the digest-auth semicolon-path bug and passed the direct local repro, but treatment stayed narrower: control changed `auth.py`, `tests/test_lowlevel.py`, and `HISTORY.md`, while treatment stayed in `auth.py` plus `tests/test_requests.py`.
- 2026-04-29: Ran the first non-requests medium-tier pair against `hynek/structlog` issue `#710`. Both conditions fixed the async `thread_name` attribution bug and passed the direct repro plus the focused `CallsiteParameterAdder` async test slice, but control achieved the same behavior with a much smaller patch (`45` changed lines vs. `87`).
- 2026-04-29: Ran the first `fastapi/typer` medium-tier pair against issue `#493`. Both conditions fixed the missing `BOOL` type in `--help` for explicit bool options and passed the direct help-output repro plus focused tests, with near-total convergence: both landed a three-file `TyperOption` help-formatting fix, and treatment was only slightly smaller (`77` changed lines vs. `81`).
- 2026-04-29: Ran the second `fastapi/typer` medium-tier pair against issue `#445`. Both conditions fixed the single-command `result_callback` bug and passed the direct callback-fire repro plus `tests/test_others.py`, but they differed a bit in finish style: control stayed code-and-test only, while treatment also touched one tutorial page while still landing a slightly smaller patch (`27` changed lines vs. `33`).
- 2026-04-30: Restarted light-tier issue resolution against the new Treatment B baselines with `arrow-py/arrow` issue `#1210`. Both control and Treatment B fixed the `Arrow.interval` type hints, added focused `get_type_hints` regression coverage, passed the focused `TestArrowInterval` slice, passed the direct type-hint check, and passed the full suite (`1854 passed, 1 xfailed, 1 xpassed`). Control was smaller (`12` changed lines), while Treatment B made an additional `span_range` typing/normalization consistency change (`22` changed lines).
- 2026-04-30: Continued the Treatment B restart on `arrow-py/arrow` issue `#1237`. Both control and Treatment B fixed decimal-fraction `dehumanize()` parsing, passed the direct repro (`2 days 3.5 hours ago` -> `2025-12-08T05:30:00+00:00`), passed the focused `TestArrowDehumanize` slice, and passed the full suite (`1854 passed, 1 xfailed, 1 xpassed`). Control was smaller (`16` changed lines); Treatment B added more typing structure around the numeric accumulator (`35` changed lines).
- 2026-04-30: Re-preflighted `arrow-py/arrow` issue `#1240` for the Treatment B restart and skipped it again as non-runnable: from a January 9 reference point, both January 24 and January 25 already humanize as `in 2 weeks` in both control and Treatment B baselines. Prepared `arrow-py/arrow` issue `#1259` next; both baselines reproduce the crash when `arrow.get('2025-01-01', 'YYYY-MM-DD', tzinfo=None)` is called.
- 2026-04-30: Ran `arrow-py/arrow` issue `#1259` under the Treatment B restart. Both control and Treatment B fixed explicit `tzinfo=None` handling in `ArrowFactory.get`, passed the direct repro, passed the focused `TestGet` slice, and passed the full suite (`1854 passed, 1 xfailed, 1 xpassed`). This pair converged exactly on logged churn: both touched 2 files and changed 9 lines.
- 2026-04-30: Ran `arrow-py/arrow` issue `#1269` under the Treatment B restart. Both control and Treatment B fixed shortened English `dehumanize()` units (`min`, `mins`, `sec`, `secs`), passed the direct repro, passed the focused `TestArrowDehumanize` slice, and passed the full suite. This time Treatment B was much smaller (`38` changed lines) than control (`102` changed lines), while both touched 3 files.
- 2026-04-30: Started the Treatment B restart for `astanin/python-tabulate`. Issue `#315` was skipped after preflight because both baselines already rendered `tabulate({'x': []}, headers='keys', maxcolwidths=100)` the same as the no-`maxcolwidths` empty table. Issue `#354` reproduced and both control and Treatment B fixed the `fancy_grid` max-width overflow, dropping max line length from `107` to `105` and passing the full suite (`255 passed, 38 skipped`). Control was smaller (`48` changed lines) than Treatment B (`75` changed lines).
- 2026-05-01: Continued the `astanin/python-tabulate` Treatment B restart with issue `#357`. Both control and Treatment B implemented grouped-column separators for `fancy_outline`, replacing literal Python-list headers with flattened headers and the requested double separator glyphs. Both passed the direct repro, focused `fancy_outline` output slice, full suite (`255 passed, 38 skipped`), and `git diff --check`; Treatment B was slightly smaller (`154` changed lines) than control (`173` changed lines).

## Surprises & Discoveries

- 2026-04-28: Two originally selected repos could not support an issue-based task battery as written. `jmoiron/humanize` had zero open issues; `encode/httpx` has issues disabled.
- 2026-04-28: The manifest's `Opened` column needed a clarified convention. It intentionally stores date-only values for readability, while the full `createdAt` timestamps were verified separately.
- 2026-04-28: None of the nine upstream control repos already ships an agent harness entrypoint file. The treatment condition will therefore measure harness introduction from a clean zero-baseline across the whole battery.
- 2026-04-28: Generated local build artifacts can distort the cultivate audit. `structlog-treatment` had a local `.tox` tree that pushed the scanner to its 4000-file cap and created false negatives for repository knowledge-base and execution-plan signals; removing the generated directory restored the expected audit output.
- 2026-04-28: The monthly ChatGPT/subagent path can surface usage snippets, but not as a stable machine-readable accounting source. The run logger therefore treats token fields as optional and records provenance instead of forcing fake precision.
- 2026-04-28: More authoritative token-efficiency measurement requires API-backed runs, not just the monthly ChatGPT/Codex account. The study docs now say this explicitly so the tradeoff between zero-marginal-cost runs and API-grade token accounting is visible in the plan itself.
- 2026-04-28: The first low-complexity pilot task (`python-slugify` issue `#167`) was so bounded that both control and treatment converged on the same one-line README change. That is useful as a logger/scorer smoke test, but it is unlikely to reveal harness effects by itself.
- 2026-04-28: `python-slugify` issue `#172` did not reproduce at the pinned SHA once a valid Python 3.11 environment was provisioned; the baseline already transliterates `º` -> `o` and `ª` -> `a`. The issue manifest therefore needs a lightweight repro check before each task is queued for actual eval runs.
- 2026-04-28: Older pinned repos can silently fail under the machine's default interpreter. `python-slugify` requires Python `>=3.10`, but the default `python3` on this machine is `3.9.6`, so Milestone D needs explicit interpreter selection during sandbox setup.
- 2026-04-28: The `python-slugify` battery is weaker than the original manifest suggested. One task is maintainer-policy text (`#166`), one task does not reproduce at the pinned SHA (`#172`), and two tasks are intentionally tiny (`#167`, `#169`). The repo still works as a light-tier pilot target, but it is not a strong candidate for high-signal harness separation by itself.
- 2026-04-28: The first `python-tabulate` run pair produced a more useful shape than the slugify pilots. Both conditions solved the bug, but treatment was narrower in file scope while still preserving the same targeted test and repro outcomes.
- 2026-04-28: `python-tabulate` continues to produce richer divergence than `python-slugify`, but not always in the same direction. On issue `#354`, treatment matched control on files touched and turns while taking a slightly larger patch; the more informative difference was *where* each run chose to encode the regression (`test_regression.py` vs. `test_output.py`).
- 2026-04-28: `arrow-py/arrow` issue `#1259` gave a clean same-scope comparison: both runs touched the same two files and added the same kind of regression coverage, but one removed a special-case branch while the other normalized `tzinfo=None` earlier in the kwargs flow. This is a good example of harness effects not necessarily changing scope, but potentially still changing path selection.
- 2026-04-28: Repeating a previously proven task (`python-tabulate` issue `#427`) did not simply replay the first pair. On `run_index=1`, both conditions still solved the bug, but control widened into an internal partial-based refactor while treatment stayed on the direct mapping path. Repeat runs therefore appear necessary even for low-tier tasks; one pass per issue is not enough to characterize agent behavior.
- 2026-04-28: Repeating `arrow-py/arrow` issue `#1259` produced less variance than repeating `python-tabulate` issue `#427`. That suggests some tasks are inherently more path-stable than others, which is exactly why the study needs repeated runs across multiple repos instead of relying on a single anecdotal pair.
- 2026-04-28: Repeating `python-tabulate` issue `#354` again favored treatment on patch size without changing outcome quality. Both runs passed the full suite and hit the same 105-character cap, but treatment used a much smaller code change. This is the clearest repeated-run evidence so far that harness guidance can reduce solution breadth on the same task.
- 2026-04-29: `arrow-py/arrow` issue `#1269` produced another clear narrow-vs-broad split. Control updated both the main parser path and English locale aliases, while treatment solved the same user-visible problem with a smaller parser-only normalization plus the same focused regression coverage.
- 2026-04-29: Existing in-session agents can complete useful study runs even when fresh worker spawning is quota-limited, but they do not expose the same stable turn-count metadata. The logger/scorer therefore now treats `turns` like token usage: optional when instrumentation is unavailable, with summary tables reporting how many runs contributed to turn averages.
- 2026-04-29: Interrupted-run recovery benefits more from an event trail than from forcing a final scalar turn count. Parent-observed events such as `run_started`, `parent_turn_observed`, and `resumed_after_interrupt` preserve state cleanly even when the underlying agent path does not expose authoritative internal-turn telemetry.
- 2026-04-29: `arrow-py/arrow` issue `#1240` did not reproduce at the pinned SHA during preflight even though it remains open on GitHub. The January 24/25 threshold examples now both render as `in 2 weeks`, which is another reminder that open issue state alone is not enough to justify spending a control/treatment pair.
- 2026-04-29: The new event log already paid for itself on the `arrow #1237` pair. We now have durable parent-side milestones for `run_started`, `subagent_spawned`, `subagent_completed`, and `run_completed`, plus observed-turn checkpoints, without needing to overclaim hidden subagent-internal step counts.
- 2026-04-29: `python-tabulate` issue `#357` produced one of the clearest scope differences yet on a feature task. Both conditions landed the same grouped-separator output, but treatment kept the implementation more tightly scoped to `fancy_outline` while control threaded the concept more broadly through normalization and rendering.
- 2026-04-29: The collab thread cap does not block the study as long as we can reuse standing agents and keep the event trail explicit. Reusing `Newton` and `Laplace` preserved the control/treatment structure with no loss of reproducibility because the run-state was logged parent-side.
- 2026-04-29: Repeating `python-tabulate` issue `#357` increased, rather than reduced, the control-treatment contrast. Treatment reproduced nearly the same narrow patch shape on the second pass, while control became even broader and also changed column padding more aggressively. This is unusually strong repeat-run evidence that the harness can stabilize solution scope on a feature task, not just on bug fixes.
- 2026-04-29: `python-tabulate` issue `#358` is a useful counterexample to a too-simple “treatment always narrows scope” story. Both conditions landed working Typst support, but treatment also updated discoverability surfaces (`README.md` and help text), making it slightly broader in file scope while still smaller in total line count. That suggests the harness can sometimes encourage a more user-facing completion instinct rather than pure implementation minimization.
- 2026-04-29: Turn data needs explicit provenance, not just presence or absence. After the event-log rollout, we can now distinguish exact turn counts from parent-observed turn proxies and from genuinely missing turn data. That is a much more credible presentation for users evaluating whether the harness affects interaction cost.
- 2026-04-30: The first Treatment B restart pair is a counterexample to "layered always means less churn." On `arrow #1210`, Treatment B matched control on success, files touched, and validation, but broadened the implementation to keep `span_range` typing/runtime normalization consistent with `interval`. That may be a defensible completeness instinct, but it should be scored as more churn for this task.
- 2026-04-30: The `arrow #1237` Treatment B restart repeated the same pattern: equal success and validation, but broader typing-oriented patch shape in Treatment B. That suggests the layered Arrow guidance may be steering agents toward local consistency/completeness rather than raw minimization on typing/parser-adjacent tasks.
- 2026-04-30: `arrow #1259` is the first Arrow Treatment B restart pair where Treatment B and control converged almost exactly: same files, same changed-line count, same implementation hook, same validation. This is useful evidence against overfitting the "Treatment B is broader on Arrow" story from `#1210` and `#1237`, but it is still not positive less-churn evidence by itself.
- 2026-04-30: `arrow #1269` restored the earlier positive less-churn signal for layered guidance on a parser/locale task. Control generalized locale timeframe strings and dehumanize iteration, while Treatment B introduced a narrower dehumanize-only alias surface with stronger parametrized coverage. That is a better user-facing example than `#1259` because outcome quality stayed equal while changed lines dropped by more than half.
- 2026-04-30: `python-tabulate #354` is a fresh counterexample against treating Treatment B as automatically lower churn. Both runs solved the same width overflow with identical validation, but Treatment B spent more lines on exact-output regression coverage while control kept the patch smaller. This strengthens the current interpretation: layered guidance changes solution shape, but "less churn" still needs per-task evidence rather than assumption.
- 2026-05-01: `python-tabulate #357` again shows task-level variance rather than a one-way effect. On this feature task, both conditions chose the same two-file ownership boundary and the same narrow `fancy_outline` scope, while Treatment B ended modestly smaller. This is positive for Treatment B on changed lines, but the absolute patch is still broad because the feature itself touches separator rendering internals.
- 2026-04-29: Medium-tier repos introduce a different evaluation wrinkle than the lightweight formatter/parser tasks: the relevant test file can already be red on the pinned baseline for unrelated environmental or fixture reasons. `psf/requests` issue `#6890` is the first concrete example, and it reinforces why the study log needs both before/after test-state fields and explicit regression counts instead of a single undifferentiated green/red bit.
- 2026-04-29: Eval telemetry needs to survive quota and session interruptions just as much as code regressions. The aborted `httpx-6917` pair demonstrated that an explicit non-completed run row plus `run_abandoned` event-log closure is much better than silently omitting the attempt, because it preserves completion-rate impact and leaves a clean audit trail for a later retry.
- 2026-04-29: Repeated medium-tier validation can interact through shared temp extraction paths even when the source repos are isolated. The first treatment-side `tests/test_utils.py` rerun for `httpx-6917` compared against a stale extracted `$TMPDIR/.../test_utils.py` left by an earlier run; clearing that temp file restored a clean pass. This is a study-environment artifact, not a code regression, and it should be called out explicitly whenever it appears.
- 2026-04-29: Pinned-repo `uv` environments can quietly point at the editable install from a baseline workdir instead of the disposable run sandbox. The control `httpx-6990` worker verified against `workdirs/httpx-control`; parent-side validation had to force `PYTHONPATH=src` against the run sandbox to confirm the actual run artifact. This needs to be the default validation posture for future requests-based runs.
- 2026-04-29: `structlog` issue `#710` is a strong example of how an existing test seam can encode the current bug workaround instead of the desired behavior. The pinned baseline already had a focused async `CallsiteParameterAdder` test, but it explicitly dropped `thread` and `thread_name` from the async assertion. That made the pair especially useful: both conditions had to change not only implementation but also what the test considered worth asserting.
- 2026-04-29: Older pre-PEP 621 repos can require a different study setup path. The pinned `fastapi/typer` checkout uses an older `flit` backend that cannot do editable installs through modern `build_editable`, so the clean study path was: create a local `uv` venv, install only the runtime/test dependencies, and validate the repo source tree with `PYTHONPATH=.`, not a package install.
- 2026-04-29: The second `typer` pair reinforced that the harness does not always force a narrower implementation. On issue `#445`, both runs converged on the same narrow behavioral fix, but treatment still chose to add a small doc touch while ending slightly smaller overall. That is a good reminder that “treatment” can sometimes manifest as a more complete user-facing finish, not just fewer edited files.
- 2026-04-29: Study execution is now paused and this plan is reclassified as a pilot record. Investigation of `fastapi-treatment`, `celery-treatment`, and `rich-treatment` showed the cultivate treatment was too weakly applied in at least part of the battery, especially around `AGENTS.md` exposing the deeper knowledge-store links. Further Milestone D runs are intentionally halted until cultivate and the treatment protocol are tightened.
- 2026-04-30: Packaged the Treatment B layered-harness protocol into `skills/cultivate` as version `0.2.5`, including explicit instructions for short nested `AGENTS.md` files in large multi-surface repos, template guidance, eval coverage, and an audit signal for `layered AGENTS coverage`. The local installed skill copy was refreshed to `0.2.5` so subsequent `/cultivate` runs use the layered protocol.
- 2026-04-30: Created fresh Treatment B baseline copies for all nine study repos at `$STUDY_WORKSPACE/workdirs/*-treatment-b`. Each copy starts from the pinned control SHA, applies the hardened root cultivate harness, adds nested local `AGENTS.md` files to high-leverage subtrees where applicable, and has a local `study-treatment-b` commit. A cultivate audit confirms canonical root `AGENTS.md` structure, deep-context links, and layered coverage for every multi-surface Treatment B copy.

## Decision Log

- 2026-04-28: Use real open GitHub issues as the task battery instead of synthetic tasks. Reason: the community has already done the work to identify and validate real problems, providing ground truth without additional curation effort.
- 2026-04-28: Keep navigation/architecture tasks synthetic (2 of 5 per repo). Reason: open issues rarely ask "explain how X works" — those questions have no clear issue analog but are high-signal for harness value.
- 2026-04-28: N=5 runs per condition per task. Reason: enough variance for Mann-Whitney U and Fisher's exact test without requiring a large compute budget.
- 2026-04-28: Continuous execution model — no fixed end date. Reason: user preference; milestone gates drive progress rather than calendar dates.
- 2026-04-28: Added `files_touched` and `lines_changed` as logged covariates. Reason: SWE-bench data (Jimenez et al. 2024, Yang et al. 2024) shows agent success degrades with both; if treatment reduces these for equivalent tasks, it is itself evidence of faster navigation.
- 2026-04-28: Added AGENTS.md command-first quality check to Milestone B. Reason: Crosley (2026) documents that prose-only AGENTS.md produces zero observable behavioral change; treatment quality must be verified mechanically, not assumed.
- 2026-04-28: Anchored expected effect size to Lopopolo (2026) observational data (3.5 PRs/engineer/day, 20% cleanup elimination). Our study provides the causal comparison that case study cannot — same repos, same tasks, harness as the only variable.
- 2026-04-28: Substituted `arrow-py/arrow` for the `jmoiron/humanize` slot. Reason: `jmoiron/humanize` had zero open GitHub issues, so it could not support a five-issue task battery.
- 2026-04-28: Substituted `psf/requests` for the `encode/httpx` slot. Reason: `encode/httpx` has GitHub issues disabled, so it could not support issue-based task curation.
- 2026-04-28: Interpreted "open and unresolved at the pinned SHA" as "the described gap should still exist in the pinned codebase." Reason: the plan also requires pinning at or before the earliest selected issue timestamp, which can predate issue filing.
- 2026-04-28: Split Milestone A verification into two layers. Reason: GitHub can confirm issue state and pin chronology immediately, but actual repro-on-pinned-checkout confirmation requires cloned repos and belongs with Milestone B setup.
- 2026-04-28: Commit plan progress incrementally as milestones advance. Reason: the study spans multiple sessions and needs durable checkpoints rather than long-lived uncommitted state.
- 2026-04-28: Use an external workspace with cached source clones plus paired worktrees for control and treatment. Reason: it keeps the `skills` repo clean, reduces redundant network transfer, and makes Milestone B idempotent.
- 2026-04-28: Treat the cultivate audit's remaining `environment isolation` and `agent-usable scripts` findings as non-blocking for Milestone B. Reason: the study's treatment condition only needs a committed harness with command-first guidance and no critical navigation gaps; some upstream repos do not declare a single canonical runner or do not yet ship reusable local scripts.
- 2026-04-28: Make token usage optional in Milestone C and record a `usage_source` for each run. Reason: the near-term plan is to use the monthly ChatGPT/Codex account plus subagents, which does not provide stable API-grade token accounting; the schema should still be ready for future API-based runs.
- 2026-04-28: Use disposable per-run sandboxes under `$STUDY_WORKSPACE/runs/` instead of mutating the baseline control/treatment workdirs directly. Reason: preserves the pinned study baselines, makes reruns cheap, and keeps file-diff measurement local to each attempt.
- 2026-04-28: For delegated subagent runs, count `turns` as the number of reported shell/tool actions plus the final completion response. Reason: this is the most stable turn-like proxy available from subagent notifications without API telemetry or a richer transcript export.
- 2026-04-28: Add a preflight repro check before launching a control/treatment pair. Reason: issue metadata alone is not enough; `python-slugify` issue `#172` stayed open on GitHub but no longer reproduced at the pinned SHA in a correctly provisioned environment.
- 2026-04-28: Pre-provision run sandboxes with a repo-compatible interpreter and editable install before delegated runs begin. Reason: it keeps environment drift from dominating agent effort and makes cross-condition comparisons about the harness rather than local machine setup.
- 2026-04-28: After establishing the logger/scorer loop on `python-slugify`, shift subsequent Milestone D pilots toward other repos with richer issue quality. Reason: continuing to spend runs on shallow, low-variance tasks is unlikely to teach us much about harness effects.
- 2026-04-29: Make `turns` optional in the run log and add `turn_run_count` to scorer output. Reason: some agent-execution paths provide trustworthy completion and diff data but not comparable turn counts; the study should record those runs without inventing precision or distorting the turn averages.
- 2026-04-30: Treat layered local `AGENTS.md` files as the Treatment B candidate, not just a one-off FastAPI patch. Reason: the FastAPI issue `#11215` pilot showed the same production fix and validation with slightly less regression-fixture churn, and the next question is whether that layered guidance beats the hardened root-only Treatment A across more repos and issues.
- 2026-04-30: Keep the original `*-treatment` workdirs as pilot/root-treatment history and create separate `*-treatment-b` workdirs for the restarted treatment condition. Reason: this preserves provenance for the paused study while giving future Milestone D runs a clean, auditable layered baseline.
- 2026-04-29: Add a separate append-only event log for live run-state capture. Reason: interruptions and resumptions are easier to reconstruct from a timestamped event trail than from a single final run record, and this keeps recovery support separate from the main scored metrics.
- 2026-04-29: Abort this study round as a mainline evaluation and preserve it as a pilot. Reason: the current treatment condition is no longer trusted as a uniformly well-applied cultivate harness, so more runs would add cost without adding trustworthy evidence. A later study should reuse the Milestone A-C artifacts but restart Milestone D after the skill and treatment application protocol are repaired.

## Outcomes & Retrospective

This pilot was still valuable. It validated the logging/scoring workflow, exposed turn-telemetry gaps that are now repaired, and surfaced a much more important methodological issue than any single run outcome: treatment validity is itself a first-class dependency. The current cultivate treatment can produce strong harnesses, but this round showed it can also be applied too weakly to support a trustworthy user-facing comparative study. The right next step is skill hardening and treatment re-audit, not additional eval volume.

## Artifacts and Notes

- Issue manifest: `docs/exec-plans/active/harness-efficiency-study-issues.md`
- Run log: `docs/exec-plans/active/harness-efficiency-study-runs.jsonl`
- Final report (to be created): `docs/exec-plans/completed/harness-efficiency-study-report.md`
- External repo workspace: `$STUDY_WORKSPACE`
- Treatment B restart readout:

| Task | Condition | Model | Outcome | Files | Lines | Validation | Notes |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `fastapi-11215-layered` | control | `gpt-5.4` | pass | 2 | 56 | Direct repro plus focused `test_dependency_contextmanager` slice passed. | Fresh control repeated the two-file routing/test strategy. |
| `fastapi-11215-layered` | Treatment B | `gpt-5.4` | pass | 2 | 52 | Direct repro plus focused `test_dependency_contextmanager` slice passed. | Reused existing lifecycle test state instead of adding new state keys. |
| `arrow-1210-layered` | control | `gpt-5` | pass | 2 | 12 | Direct type-hint check, focused `TestArrowInterval` slice, and full suite passed. | Smallest direct `Arrow.interval` annotation/test fix. |
| `arrow-1210-layered` | Treatment B | `gpt-5` | pass | 2 | 22 | Direct type-hint check, focused `TestArrowInterval` slice, and full suite passed. | Broader consistency change also updated `span_range` typing/runtime normalization. |
| `arrow-1237-layered` | control | `gpt-5` | pass | 2 | 16 | Direct repro, focused `TestArrowDehumanize` slice, and full suite passed. | Decimal-aware regex plus int/float parsing and focused regression test. |
| `arrow-1237-layered` | Treatment B | `gpt-5` | pass | 2 | 35 | Direct repro, focused `TestArrowDehumanize` slice, and full suite passed. | Same fix shape plus broader typing annotations for numeric accumulator state. |
| `arrow-1240-layered` | both | `gpt-5` | skipped | n/a | n/a | Preflight only. | Did not reproduce: January 24 and January 25 from January 9 both humanize as `in 2 weeks` in both baselines. |
| `arrow-1259-layered` | control | `gpt-5` | pass | 2 | 9 | Direct repro, focused `TestGet` slice, and full suite passed. | Explicit `tzinfo=None` treated like omitted `tzinfo` with focused factory regression. |
| `arrow-1259-layered` | Treatment B | `gpt-5` | pass | 2 | 9 | Direct repro, focused `TestGet` slice, and full suite passed. | Nearly identical two-file patch shape and exact same logged churn as control. |
| `arrow-1269-layered` | control | `gpt-5` | pass | 3 | 102 | Direct repro, focused `TestArrowDehumanize` slice, and full suite passed. | Generalized locale timeframe aliases and parser iteration for shortened English units. |
| `arrow-1269-layered` | Treatment B | `gpt-5` | pass | 3 | 38 | Direct repro, focused `TestArrowDehumanize` slice, and full suite passed. | Smaller dehumanize-only alias surface with parametrized past/future regression coverage. |
| `python-tabulate-315-layered` | both | `gpt-5` | skipped | n/a | n/a | Preflight only. | Did not reproduce: empty dict-of-lists table with `maxcolwidths=100` already matches no-`maxcolwidths` output in both baselines. |
| `python-tabulate-354-layered` | control | `gpt-5` | pass | 2 | 48 | Direct repro, focused output/regression/textwrapper slice, full suite, and `git diff --check` passed. | Narrower padding guard; max line length dropped from `107` to `105`. |
| `python-tabulate-354-layered` | Treatment B | `gpt-5` | pass | 2 | 75 | Direct repro, focused output/regression/textwrapper slice, full suite, and `git diff --check` passed. | Same behavior with broader exact `fancy_grid` regression coverage; max line length dropped from `107` to `105`. |
| `python-tabulate-357-layered` | control | `gpt-5` | pass | 2 | 173 | Direct repro, focused `fancy_outline` output slice, full suite, and `git diff --check` passed. | Flattened grouped headers and rendered double separator glyphs for `fancy_outline`. |
| `python-tabulate-357-layered` | Treatment B | `gpt-5` | pass | 2 | 154 | Direct repro, focused `fancy_outline` output slice, full suite, and `git diff --check` passed. | Same feature with smaller grouped-boundary tracking patch and exact regression coverage. |

- Eval tooling:
  - `scripts/eval_logger.py`
  - `scripts/eval_scorer.py`
  - `scripts/eval_event_logger.py`
  - `scripts/eval_event_recover.py`
  - `scripts/eval_turn_backfill.py`
  - `scripts/test_eval_tools.py`
- Treatment harness commits:
  - `jmoiron-humanize-treatment` -> `7f0e35958fc8f301f550657ed07d44dbab8d78d7`
  - `python-tabulate-treatment` -> `69bb274426296c746d87de8be44f3fa0e311ff1e`
  - `python-slugify-treatment` -> `27d28191d94effa57e675ae8e3db8b5a164516a6`
  - `httpx-treatment` -> `2c50ac8ed98815e0ffe129a074ac69d0ea342699`
  - `typer-treatment` -> `3120c5c9ce0cd54debc52370623bfc2a71b816fa`
  - `structlog-treatment` -> `e148e573f67d6c5ab48820e093d67235b7525be1`
  - `fastapi-treatment` -> `f71beec1292e59023e864f07f408fbda3c022bff`
  - `celery-treatment` -> `9a5e0999e1ada311795d27893d701fdc03296cff`
  - `rich-treatment` -> `25b211fb6c6de8846e779e23c921e95b896d3449`
- Treatment B harness commits:
  - `jmoiron-humanize-treatment-b` -> `c3cb0640ddcb47d8974fb844f0fbeb4a180f46ef`
  - `python-tabulate-treatment-b` -> `e137ef2ec0751a425b7acf839838c3cd5355425a`
  - `python-slugify-treatment-b` -> `b725e4c62b134081135d581464e969d64578189d`
  - `httpx-treatment-b` -> `bdeb93e4ebb62f523bb93fcb96e79739d096cdae`
  - `typer-treatment-b` -> `02f099cf9cd3e67db87ff76ba5eae028a267669c`
  - `structlog-treatment-b` -> `cff3bb6339d1c4d33d99a4c12e37f7a0f8b37305`
  - `fastapi-treatment-b` -> `30655eee73c46e9e5152cc30ba04a95b5f7b6dfc`
  - `celery-treatment-b` -> `4b794230e31a2ae8a4508392e87eb910de88d931`
  - `rich-treatment-b` -> `08ab3f42c5f82e39f68133e8c9e02c0a4d0f81ba`
