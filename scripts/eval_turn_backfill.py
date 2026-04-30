#!/usr/bin/env python3
"""Backfill missing run-log turn counts from parent-observed event logs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from eval_event_recover import load_events, summarize_events
from eval_scorer import load_records

DEFAULT_RUNS = "docs/exec-plans/active/harness-efficiency-study-runs.jsonl"
DEFAULT_EVENTS = "docs/exec-plans/active/harness-efficiency-study-events.jsonl"


def backfill_records(
    records: list[dict[str, Any]],
    event_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    event_index = {
        (row["repo"], row["condition"], row["task_id"], row["run_index"]): row
        for row in event_rows
    }
    updated: list[dict[str, Any]] = []
    changed = 0
    for record in records:
        row = dict(record)
        row.setdefault("turn_source", "exact" if row.get("turns") is not None else "missing")
        key = (row["repo"], row["condition"], row["task_id"], row["run_index"])
        event_row = event_index.get(key)
        if (
            row.get("turns") is None
            and event_row is not None
            and event_row.get("max_observed_turn_index") is not None
        ):
            row["turns"] = event_row["max_observed_turn_index"]
            row["turn_source"] = "observed"
            changed += 1
        updated.append(row)
    return updated, changed


def write_records(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-input", default=DEFAULT_RUNS)
    parser.add_argument("--events-input", default=DEFAULT_EVENTS)
    parser.add_argument("--output", help="Output JSONL path. Defaults to --runs-input.")
    parser.add_argument("--check", action="store_true", help="Report pending backfills without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    runs_path = Path(args.runs_input)
    output_path = Path(args.output) if args.output else runs_path
    records = load_records(runs_path)
    event_rows = summarize_events(load_events(Path(args.events_input)))
    updated, changed = backfill_records(records, event_rows)
    if args.check:
        print(f"{changed} record(s) can be backfilled from observed event turns")
        return 0
    write_records(output_path, updated)
    print(f"wrote {len(updated)} record(s) to {output_path}; backfilled {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
