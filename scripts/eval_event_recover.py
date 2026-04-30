#!/usr/bin/env python3
"""Summarize live harness-efficiency event logs for interrupted-run recovery."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

DEFAULT_INPUT = "docs/exec-plans/active/harness-efficiency-study-events.jsonl"


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for lineno, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(data, dict):
                raise ValueError(f"{path}:{lineno}: expected object")
            events.append(data)
    return events


def summarize_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, int], list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        key = (
            event["repo"],
            event["condition"],
            event["task_id"],
            event["run_index"],
        )
        grouped[key].append(event)

    rows: list[dict[str, Any]] = []
    for key, items in sorted(grouped.items()):
        observed_turns = [item["observed_turn_index"] for item in items if item.get("observed_turn_index") is not None]
        rows.append(
            {
                "repo": key[0],
                "condition": key[1],
                "task_id": key[2],
                "run_index": key[3],
                "events": len(items),
                "max_observed_turn_index": max(observed_turns) if observed_turns else None,
                "interruptions": sum(1 for item in items if item["event_type"] == "resumed_after_interrupt"),
                "latest_event_type": items[-1]["event_type"],
                "latest_logged_at": items[-1]["logged_at"],
            }
        )
    return rows


def render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Repo | Condition | Task | Run | Events | Max observed turn | Interruptions | Latest event | Latest timestamp |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {repo} | {condition} | {task_id} | {run_index} | {events} | {max_observed_turn_index} | {interruptions} | {latest_event_type} | {latest_logged_at} |".format(
                repo=row["repo"],
                condition=row["condition"],
                task_id=row["task_id"],
                run_index=row["run_index"],
                events=row["events"],
                max_observed_turn_index=row["max_observed_turn_index"] if row["max_observed_turn_index"] is not None else "n/a",
                interruptions=row["interruptions"],
                latest_event_type=row["latest_event_type"],
                latest_logged_at=row["latest_logged_at"],
            )
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to the JSONL event log.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = summarize_events(load_events(Path(args.input)))
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        print(render_markdown(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
