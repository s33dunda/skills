#!/usr/bin/env python3
"""Append unbounded harness-efficiency study records to a JSONL log."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

CONDITIONS = {"control", "treatment"}
TASK_TYPES = {"navigation", "implementation", "maintenance"}
TIERS = {"medium", "heavy"}
TURN_SOURCES = {"exact", "observed", "missing"}
USAGE_SOURCES = {"none", "subagent_notification", "api"}
DEFAULT_OUTPUT = "docs/exec-plans/active/unbounded-harness-study-runs.jsonl"


def _nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be >= 0")
    return parsed


def _score(value: str) -> int:
    parsed = int(value)
    if parsed < 0 or parsed > 3:
        raise argparse.ArgumentTypeError("must be between 0 and 3")
    return parsed


def _nonnegative_float(value: str) -> float:
    parsed = float(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be >= 0")
    return parsed


@dataclass
class UnboundedRunRecord:
    schema_version: int
    logged_at: str
    repo: str
    condition: str
    task_id: str
    task_type: str
    run_index: int
    tier: str
    completed: bool
    navigation_score: int | None
    scope_score: int | None
    validation_score: int | None
    handoff_score: int | None
    turns: int | None
    turn_source: str
    clarification_count: int
    files_touched: int
    lines_changed: int
    regression_count: int
    model_name: str | None = None
    duration_seconds: float | None = None
    usage_source: str = "none"
    tokens_input: int | None = None
    tokens_output: int | None = None
    tests_before_green: bool | None = None
    tests_after_green: bool | None = None
    tests_before_summary: str | None = None
    tests_after_summary: str | None = None
    needs_human_scoring: bool = False
    scoring_notes: str | None = None
    notes: str | None = None


def _resolve_turn_source(turns: int | None, turn_source: str | None) -> str:
    if turn_source is None:
        return "exact" if turns is not None else "missing"
    if turns is None and turn_source != "missing":
        raise ValueError("turn_source must be 'missing' when turns is omitted")
    if turns is not None and turn_source == "missing":
        raise ValueError("turn_source cannot be 'missing' when turns is provided")
    return turn_source


def build_record(args: argparse.Namespace) -> UnboundedRunRecord:
    tokens_present = args.tokens_input is not None or args.tokens_output is not None
    if tokens_present and args.usage_source == "none":
        raise ValueError("usage_source cannot be 'none' when token fields are provided")
    if args.tests_before_summary and args.tests_before_green is None:
        raise ValueError("tests_before_green is required when tests_before_summary is provided")
    if args.tests_after_summary and args.tests_after_green is None:
        raise ValueError("tests_after_green is required when tests_after_summary is provided")

    return UnboundedRunRecord(
        schema_version=1,
        logged_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        repo=args.repo,
        condition=args.condition,
        task_id=args.task_id,
        task_type=args.task_type,
        run_index=args.run_index,
        tier=args.tier,
        completed=args.completed,
        navigation_score=args.navigation_score,
        scope_score=args.scope_score,
        validation_score=args.validation_score,
        handoff_score=args.handoff_score,
        turns=args.turns,
        turn_source=_resolve_turn_source(args.turns, args.turn_source),
        clarification_count=args.clarification_count,
        files_touched=args.files_touched,
        lines_changed=args.lines_changed,
        regression_count=args.regression_count,
        model_name=args.model_name,
        duration_seconds=args.duration_seconds,
        usage_source=args.usage_source,
        tokens_input=args.tokens_input,
        tokens_output=args.tokens_output,
        tests_before_green=args.tests_before_green,
        tests_after_green=args.tests_after_green,
        tests_before_summary=args.tests_before_summary,
        tests_after_summary=args.tests_after_summary,
        needs_human_scoring=args.needs_human_scoring,
        scoring_notes=args.scoring_notes,
        notes=args.notes,
    )


def append_record(path: Path, record: UnboundedRunRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(record), sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to the JSONL run log.")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--condition", required=True, choices=sorted(CONDITIONS))
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--task-type", required=True, choices=sorted(TASK_TYPES))
    parser.add_argument("--run-index", required=True, type=_nonnegative_int)
    parser.add_argument("--tier", required=True, choices=sorted(TIERS))
    parser.add_argument("--completed", dest="completed", action="store_true")
    parser.add_argument("--not-completed", dest="completed", action="store_false")
    parser.add_argument("--navigation-score", type=_score)
    parser.add_argument("--scope-score", type=_score)
    parser.add_argument("--validation-score", type=_score)
    parser.add_argument("--handoff-score", type=_score)
    parser.add_argument("--turns", type=_nonnegative_int)
    parser.add_argument("--turn-source", choices=sorted(TURN_SOURCES))
    parser.add_argument("--clarification-count", required=True, type=_nonnegative_int)
    parser.add_argument("--files-touched", required=True, type=_nonnegative_int)
    parser.add_argument("--lines-changed", required=True, type=_nonnegative_int)
    parser.add_argument("--regression-count", required=True, type=_nonnegative_int)
    parser.add_argument("--model-name")
    parser.add_argument("--duration-seconds", type=_nonnegative_float)
    parser.add_argument("--usage-source", default="none", choices=sorted(USAGE_SOURCES))
    parser.add_argument("--tokens-input", type=_nonnegative_int)
    parser.add_argument("--tokens-output", type=_nonnegative_int)
    parser.add_argument("--tests-before-green", dest="tests_before_green", action="store_true")
    parser.add_argument("--tests-before-red", dest="tests_before_green", action="store_false")
    parser.add_argument("--tests-after-green", dest="tests_after_green", action="store_true")
    parser.add_argument("--tests-after-red", dest="tests_after_green", action="store_false")
    parser.add_argument("--tests-before-summary")
    parser.add_argument("--tests-after-summary")
    parser.add_argument("--needs-human-scoring", action="store_true")
    parser.add_argument("--scoring-notes")
    parser.add_argument("--notes")
    parser.set_defaults(completed=None, tests_before_green=None, tests_after_green=None)
    args = parser.parse_args()
    if args.completed is None:
        parser.error("one of --completed / --not-completed is required")
    return args


def main() -> int:
    args = parse_args()
    record = build_record(args)
    output = Path(args.output)
    append_record(output, record)
    print(f"appended 1 record to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
