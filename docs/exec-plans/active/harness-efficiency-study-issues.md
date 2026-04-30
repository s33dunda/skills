# Harness Efficiency Study Issue Manifest

Milestone A issue curation for `docs/exec-plans/active/harness-efficiency-study.md`.

Generated: 2026-04-28

## Selection Notes

- All selected tasks were open on 2026-04-28.
- `Pinned SHA` is the latest upstream commit at or before the earliest selected issue's `createdAt` timestamp for that repo.
- For historical consistency, "open and unresolved at the pinned SHA" is interpreted as "the described gap should still exist in the pinned codebase"; issue objects themselves may have been filed after the pinned commit.
- `Label(s)` reflects GitHub labels exactly when present. Unlabeled issues were kept only when the issue body included a clear repro, expected-vs-actual description, or an explicit bounded request.
- The `Opened` column stores the issue date (`YYYY-MM-DD`) for scanability; full GitHub `createdAt` timestamps were verified during Milestone A confirmation.

## Verification Summary

- `45/45` selected issues were still `OPEN` when re-checked against GitHub on 2026-04-28.
- `9/9` pinned SHAs are at or before the earliest selected issue timestamp for their repo, so the study can reproduce checkout state deterministically.
- This file now captures **issue-state and chronology verification**. Full **repro-on-pinned-checkout verification** remains a Milestone B setup task when the study clones each repo at its pinned SHA.

| Repo | Pinned SHA | Pin commit date (UTC) | Earliest selected issue (UTC) | Chronology check |
| --- | --- | --- | --- | --- |
| `Textualize/rich` | `1d402e0c59f8765e420a5a4440eb2fca7465d1ae` | `2026-01-24T21:42:08Z` | `2026-01-27T19:07:34Z` | `OK` |
| `arrow-py/arrow` | `1d70d0091980ea489a64fa95a48e99b45f29f0e7` | `2024-11-20T05:41:58Z` | `2025-04-03T10:56:50Z` | `OK` |
| `astanin/python-tabulate` | `3b2b69505b3962ace99ac69ee96da1224b477f1a` | `2024-02-27T11:42:58Z` | `2024-03-04T09:59:44Z` | `OK` |
| `celery/celery` | `87db973f08dba416a0a605ed7fd72e47f5dbd5bd` | `2026-02-04T14:08:05Z` | `2026-02-09T09:13:31Z` | `OK` |
| `fastapi/fastapi` | `eef1b7d51530be64ddd48e02b5ca46f28a0ebfc1` | `2024-02-28T14:04:27Z` | `2024-02-28T14:57:07Z` | `OK` |
| `fastapi/typer` | `c3a4c72a4f1a18b7f16addb508862ec63411fa63` | `2020-08-16T14:52:47Z` | `2021-03-31T20:03:15Z` | `OK` |
| `hynek/structlog` | `3a7006d616bd828ed4eb5c66756f8bdc13fc5fea` | `2025-03-07T07:32:24Z` | `2025-03-08T15:25:28Z` | `OK` |
| `psf/requests` | `a2fd25ff34b66ef71b54dfc90e09a4e4152357f6` | `2025-02-11T15:58:59Z` | `2025-02-11T17:30:11Z` | `OK` |
| `un33k/python-slugify` | `7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4` | `2026-01-07T16:28:09Z` | `2026-01-08T22:03:37Z` | `OK` |

## Repo Slots

| Tier | Study slot | Selected repo | Status | Pinned SHA | Note |
| --- | --- | --- | --- | --- | --- |
| Light | `jmoiron/humanize` | `arrow-py/arrow` | substituted | `1d70d0091980ea489a64fa95a48e99b45f29f0e7` | `jmoiron/humanize` had zero open issues; `arrow` is a close Python date/humanization substitute with an active open issue pool. |
| Light | `astanin/python-tabulate` | `astanin/python-tabulate` | unchanged | `3b2b69505b3962ace99ac69ee96da1224b477f1a` | Original study repo retained. |
| Light | `un33k/python-slugify` | `un33k/python-slugify` | unchanged | `7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4` | Original study repo retained; issue pool is shallow, so bounded docs/test/maintenance tasks are included. |
| Medium | `encode/httpx` | `psf/requests` | substituted | `a2fd25ff34b66ef71b54dfc90e09a4e4152357f6` | `encode/httpx` has GitHub issues disabled; `requests` is a close Python HTTP client substitute with a strong open bug pool. |
| Medium | `tiangolo/typer` | `fastapi/typer` | unchanged | `c3a4c72a4f1a18b7f16addb508862ec63411fa63` | Repo moved under the `fastapi` org; issue source is the current upstream. |
| Medium | `hynek/structlog` | `hynek/structlog` | unchanged | `3a7006d616bd828ed4eb5c66756f8bdc13fc5fea` | Original study repo retained. |
| Heavy | `tiangolo/fastapi` | `fastapi/fastapi` | unchanged | `eef1b7d51530be64ddd48e02b5ca46f28a0ebfc1` | Repo moved under the `fastapi` org; issue source is the current upstream. |
| Heavy | `celery/celery` | `celery/celery` | unchanged | `87db973f08dba416a0a605ed7fd72e47f5dbd5bd` | Original study repo retained. |
| Heavy | `Textualize/rich` | `Textualize/rich` | unchanged | `1d402e0c59f8765e420a5a4440eb2fca7465d1ae` | Original study repo retained. |

## Issue Manifest

| Tier | Study slot | Repo | Issue | Label(s) | Difficulty | Opened | Pinned SHA | Selection note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Light | `jmoiron/humanize` | `arrow-py/arrow` | [#1210](https://github.com/arrow-py/arrow/issues/1210) Type hints for `Arrow.interval` should show `Arrow` as possible type for `start` and `end` arguments | `bug` | low | 2025-04-03 | `1d70d0091980ea489a64fa95a48e99b45f29f0e7` | Clear typing mismatch with a concrete requested signature change. |
| Light | `jmoiron/humanize` | `arrow-py/arrow` | [#1237](https://github.com/arrow-py/arrow/issues/1237) Make `dehumanize()` handle values with decimal fractions correctly | `enhancement` | medium | 2025-12-10 | `1d70d0091980ea489a64fa95a48e99b45f29f0e7` | Bounded parser enhancement with an explicit expected output. |
| Light | `jmoiron/humanize` | `arrow-py/arrow` | [#1240](https://github.com/arrow-py/arrow/issues/1240) Strange `humanize` intervals | `bug` | medium | 2026-01-09 | `1d70d0091980ea489a64fa95a48e99b45f29f0e7` | Repro describes a wrong threshold boundary in `humanize()`. |
| Light | `jmoiron/humanize` | `arrow-py/arrow` | [#1259](https://github.com/arrow-py/arrow/issues/1259) `arrow.get()` behaviour for `tzinfo=None` | `bug` | low | 2026-03-05 | `1d70d0091980ea489a64fa95a48e99b45f29f0e7` | Small constructor-path bug with an explicit stack trace. |
| Light | `jmoiron/humanize` | `arrow-py/arrow` | [#1269](https://github.com/arrow-py/arrow/issues/1269) Shortened time units | `enhancement` | low | 2026-04-12 | `1d70d0091980ea489a64fa95a48e99b45f29f0e7` | Narrow feature request with failing examples for `mins` and `secs`. |
| Light | `astanin/python-tabulate` | `astanin/python-tabulate` | [#315](https://github.com/astanin/python-tabulate/issues/315) `[bug]` Error if trying to render a table with no rows using `maxcolwidths` | `none` | low | 2024-03-04 | `3b2b69505b3962ace99ac69ee96da1224b477f1a` | Direct crash repro with expected behavior. |
| Light | `astanin/python-tabulate` | `astanin/python-tabulate` | [#354](https://github.com/astanin/python-tabulate/issues/354) `maxcolwidths` isn't properly respected: extra whitespace is added | `bug, enhancement, breaking changes` | medium | 2024-11-14 | `3b2b69505b3962ace99ac69ee96da1224b477f1a` | Has a concrete testcase and a visible formatting defect. |
| Light | `astanin/python-tabulate` | `astanin/python-tabulate` | [#357](https://github.com/astanin/python-tabulate/issues/357) Feature request: column separators | `enhancement` | medium | 2025-01-14 | `3b2b69505b3962ace99ac69ee96da1224b477f1a` | Feature request is scoped to a specific formatting capability and syntax proposal. |
| Light | `astanin/python-tabulate` | `astanin/python-tabulate` | [#358](https://github.com/astanin/python-tabulate/issues/358) Feature request: add typst table format support | `enhancement` | medium | 2025-02-03 | `3b2b69505b3962ace99ac69ee96da1224b477f1a` | Bounded new formatter target with a clear user-facing deliverable. |
| Light | `astanin/python-tabulate` | `astanin/python-tabulate` | [#427](https://github.com/astanin/python-tabulate/issues/427) HTML table does not apply left column alignment | `none` | low | 2026-04-07 | `3b2b69505b3962ace99ac69ee96da1224b477f1a` | HTML output bug with an exact repro and expected attribute behavior. |
| Light | `un33k/python-slugify` | `un33k/python-slugify` | [#166](https://github.com/un33k/python-slugify/issues/166) Slugify licensing update and PRs | `none` | low | 2026-01-08 | `7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4` | Included because the repo's open issue pool is shallow; bounded project-maintenance text change. |
| Light | `un33k/python-slugify` | `un33k/python-slugify` | [#167](https://github.com/un33k/python-slugify/issues/167) Inconsistent workflow badge reference in README | `none` | low | 2026-02-13 | `7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4` | Tiny docs fix with an explicit mismatch and desired alignment. |
| Light | `un33k/python-slugify` | `un33k/python-slugify` | [#169](https://github.com/un33k/python-slugify/issues/169) Add edge case test for whitespace-only input | `none` | low | 2026-02-13 | `7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4` | Bounded test-only task with clear expected behavior. |
| Light | `un33k/python-slugify` | `un33k/python-slugify` | [#172](https://github.com/un33k/python-slugify/issues/172) Ordinal indicators are not slugified | `none` | low | 2026-02-21 | `7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4` | Small transliteration bug with a concrete mapping request. |
| Light | `un33k/python-slugify` | `un33k/python-slugify` | [#175](https://github.com/un33k/python-slugify/issues/175) `--regex-pattern` option ignored by CLI | `none` | low | 2026-04-27 | `7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4` | Command-line bug with exact repro and expected output. |
| Medium | `encode/httpx` | `psf/requests` | [#6890](https://github.com/psf/requests/issues/6890) Incorrect Handling of Escaped Quotes in Cookie Values | `none` | medium | 2025-02-11 | `a2fd25ff34b66ef71b54dfc90e09a4e4152357f6` | Strong repro and code pointer for cookie sanitization behavior. |
| Medium | `encode/httpx` | `psf/requests` | [#6917](https://github.com/psf/requests/issues/6917) Incorrect Content-Length header with `StringIO` body | `none` | medium | 2025-03-21 | `a2fd25ff34b66ef71b54dfc90e09a4e4152357f6` | Byte-vs-character length bug with a detailed script and expected header value. |
| Medium | `encode/httpx` | `psf/requests` | [#6990](https://github.com/psf/requests/issues/6990) `uri` field of digest authentication incorrectly filled when the URL contains semicolons in path | `none` | medium | 2025-07-12 | `a2fd25ff34b66ef71b54dfc90e09a4e4152357f6` | Repro script plus standards reference makes this a strong bounded bug task. |
| Medium | `encode/httpx` | `psf/requests` | [#7040](https://github.com/psf/requests/issues/7040) `2.32.5` breaks passing custom SSL context | `none` | medium | 2025-10-06 | `a2fd25ff34b66ef71b54dfc90e09a4e4152357f6` | Regression with a narrow adapter repro and suggested remediation shape. |
| Medium | `encode/httpx` | `psf/requests` | [#7223](https://github.com/psf/requests/issues/7223) Chardet is used, when it is available, not when `[use-chardet-on-py3]`-extra is installed | `none` | medium | 2026-02-24 | `a2fd25ff34b66ef71b54dfc90e09a4e4152357f6` | Optional-dependency behavior bug with a deterministic `uv` repro. |
| Medium | `tiangolo/typer` | `fastapi/typer` | [#259](https://github.com/fastapi/typer/issues/259) `[BUG]` `ctx.obj` not passed to autocompletion function | `bug` | medium | 2021-03-31 | `c3a4c72a4f1a18b7f16addb508862ec63411fa63` | Clear bug statement around context propagation in autocompletion. |
| Medium | `tiangolo/typer` | `fastapi/typer` | [#266](https://github.com/fastapi/typer/issues/266) `[BUG]` Auto-completion not work in pwsh | `bug` | medium | 2021-04-14 | `c3a4c72a4f1a18b7f16addb508862ec63411fa63` | Platform-specific completion bug with a direct install/repro path. |
| Medium | `tiangolo/typer` | `fastapi/typer` | [#445](https://github.com/fastapi/typer/issues/445) `result_callback` is ignored when only one subcommand exists | `question` | medium | 2022-08-18 | `c3a4c72a4f1a18b7f16addb508862ec63411fa63` | Labeled as a question, but describes a concrete behavioral inconsistency with repro steps. |
| Medium | `tiangolo/typer` | `fastapi/typer` | [#493](https://github.com/fastapi/typer/issues/493) Boolean `typer.Option` missing type and default value in `--help` | `question, investigate` | medium | 2022-11-09 | `c3a4c72a4f1a18b7f16addb508862ec63411fa63` | Bounded help-output bug with a specific expected rendering. |
| Medium | `tiangolo/typer` | `fastapi/typer` | [#1537](https://github.com/fastapi/typer/issues/1537) `ModuleNotFoundError: No module named 'typer'` after upgrading dependencies | `none` | low | 2026-02-11 | `c3a4c72a4f1a18b7f16addb508862ec63411fa63` | Startup/import regression candidate with a short, explicit failure symptom. |
| Medium | `hynek/structlog` | `hynek/structlog` | [#710](https://github.com/hynek/structlog/issues/710) Thread name `CallsiteParameterAdder` parameter doesn't work in async methods | `bug` | medium | 2025-03-08 | `3a7006d616bd828ed4eb5c66756f8bdc13fc5fea` | Async callsite bug with a precise parameter-level failure. |
| Medium | `hynek/structlog` | `hynek/structlog` | [#779](https://github.com/hynek/structlog/issues/779) Make consistent attribute access for `is_enabled_for` / `isEnabledFor` | `none` | low | 2025-12-23 | `3a7006d616bd828ed4eb5c66756f8bdc13fc5fea` | Narrow API-consistency fix with concrete method names. |
| Medium | `hynek/structlog` | `hynek/structlog` | [#789](https://github.com/hynek/structlog/issues/789) Allow deeper customization of locals hiding behavior in `ExceptionDictTransformer` | `none` | medium | 2026-02-20 | `3a7006d616bd828ed4eb5c66756f8bdc13fc5fea` | Scoped enhancement to one transformer hook with a concrete extension point. |
| Medium | `hynek/structlog` | `hynek/structlog` | [#799](https://github.com/hynek/structlog/issues/799) Per-field truncation / summarization for large nested log fields | `none` | medium | 2026-03-29 | `3a7006d616bd828ed4eb5c66756f8bdc13fc5fea` | Enhancement request is bounded to a processor-level capability. |
| Medium | `hynek/structlog` | `hynek/structlog` | [#804](https://github.com/hynek/structlog/issues/804) traceback does not show if log exception with `.aexception` | `none` | low | 2026-04-09 | `3a7006d616bd828ed4eb5c66756f8bdc13fc5fea` | Small async exception-formatting bug with obvious expected output. |
| Heavy | `tiangolo/fastapi` | `fastapi/fastapi` | [#11215](https://github.com/fastapi/fastapi/issues/11215) Custom `Response(background=...)` overwrites injected `BackgroundTasks` | `question` | medium | 2024-02-28 | `eef1b7d51530be64ddd48e02b5ca46f28a0ebfc1` | Behavior is described as a footgun, but the issue gives a concrete conflict and expected preservation semantics. |
| Heavy | `tiangolo/fastapi` | `fastapi/fastapi` | [#13056](https://github.com/fastapi/fastapi/issues/13056) Can't use `Annotated` with `ForwardRef` | `bug` | medium | 2024-12-10 | `eef1b7d51530be64ddd48e02b5ca46f28a0ebfc1` | OpenAPI generation bug with minimal repro code. |
| Heavy | `tiangolo/fastapi` | `fastapi/fastapi` | [#13175](https://github.com/fastapi/fastapi/issues/13175) Duplicated `OperationID` when adding route with multiple methods | `question, question-migrate` | low | 2025-01-08 | `eef1b7d51530be64ddd48e02b5ca46f28a0ebfc1` | Labeled as a question, but the duplicate-ID behavior is concrete and bounded. |
| Heavy | `tiangolo/fastapi` | `fastapi/fastapi` | [#13399](https://github.com/fastapi/fastapi/issues/13399) Dependency models created from `Form` input lose field-set metadata and validate default values | `question` | medium | 2025-02-20 | `eef1b7d51530be64ddd48e02b5ca46f28a0ebfc1` | Issue describes a specific model-construction bug with concrete expected semantics. |
| Heavy | `tiangolo/fastapi` | `fastapi/fastapi` | [#15401](https://github.com/fastapi/fastapi/issues/15401) SSE `stream_item_type` not propagated through `APIRouter` + `include_router` | `none` | medium | 2026-04-21 | `eef1b7d51530be64ddd48e02b5ca46f28a0ebfc1` | Fresh router-propagation bug with a focused surface area. |
| Heavy | `celery/celery` | `celery/celery` | [#10102](https://github.com/celery/celery/issues/10102) Connection retry do not work with purge option at startup | `Issue Type: Bug Report` | medium | 2026-02-09 | `87db973f08dba416a0a605ed7fd72e47f5dbd5bd` | Startup-path bug with a single option interaction. |
| Heavy | `celery/celery` | `celery/celery` | [#10172](https://github.com/celery/celery/issues/10172) Celery worker warm shutdown with SQS backend leaves in-flight message until visibility timeout | `Issue Type: Bug Report` | high | 2026-03-04 | `87db973f08dba416a0a605ed7fd72e47f5dbd5bd` | Infra-specific but still bounded to warm-shutdown behavior for one backend. |
| Heavy | `celery/celery` | `celery/celery` | [#10195](https://github.com/celery/celery/issues/10195) New-style errbacks in `_call_task_errbacks` silently halt the rest when one fails | `none` | medium | 2026-03-13 | `87db973f08dba416a0a605ed7fd72e47f5dbd5bd` | Code pointer plus explicit control-flow failure makes this a strong bug task. |
| Heavy | `celery/celery` | `celery/celery` | [#10269](https://github.com/celery/celery/issues/10269) Add ability to rename `celery_delayed_N` queues or at least add a namespacing prefix | `Issue Type: Feature Request` | medium | 2026-04-15 | `87db973f08dba416a0a605ed7fd72e47f5dbd5bd` | Feature request is narrow and operationally motivated. |
| Heavy | `celery/celery` | `celery/celery` | [#10284](https://github.com/celery/celery/issues/10284) `TimeoutError` and reconnect regression in `5.6.3` | `Issue Type: Bug Report, Issue Type: Regression` | high | 2026-04-25 | `87db973f08dba416a0a605ed7fd72e47f5dbd5bd` | Explicit regression report appropriate for the heavy tier. |
| Heavy | `Textualize/rich` | `Textualize/rich` | [#3948](https://github.com/Textualize/rich/issues/3948) Table title always displays on the left when `soft_wrap` is `True` | `Needs triage` | low | 2026-01-27 | `1d402e0c59f8765e420a5a4440eb2fca7465d1ae` | Small rendering bug with a narrow trigger condition. |
| Heavy | `Textualize/rich` | `Textualize/rich` | [#3960](https://github.com/Textualize/rich/issues/3960) Traceback `__notes__` from outermost exception shown on all exceptions in chain | `none` | medium | 2026-02-08 | `1d402e0c59f8765e420a5a4440eb2fca7465d1ae` | Detailed exception-display bug with expected note placement. |
| Heavy | `Textualize/rich` | `Textualize/rich` | [#4028](https://github.com/Textualize/rich/issues/4028) Failure to propagate formatting overrides via `ConsoleOptions` | `Needs triage` | medium | 2026-03-02 | `1d402e0c59f8765e420a5a4440eb2fca7465d1ae` | Scoped rendering-options bug in a well-defined code path. |
| Heavy | `Textualize/rich` | `Textualize/rich` | [#4090](https://github.com/Textualize/rich/issues/4090) `Text.from_ansi` leaves empty lines when input string has CRLF line endings | `Needs triage` | low | 2026-04-22 | `1d402e0c59f8765e420a5a4440eb2fca7465d1ae` | Clear parser bug with a simple line-ending repro. |
| Heavy | `Textualize/rich` | `Textualize/rich` | [#4093](https://github.com/Textualize/rich/issues/4093) `RichHandler` file links on Windows use incorrect VS Code path format | `Needs triage` | medium | 2026-04-23 | `1d402e0c59f8765e420a5a4440eb2fca7465d1ae` | Platform-specific output bug with explicit expected URI format. |
