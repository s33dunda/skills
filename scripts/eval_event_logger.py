#!/usr/bin/env python3
"""Append real-time harness-efficiency study events to a JSONL log."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

CONDITIONS = {"control", "treatment"}
TIERS = {"light", "medium", "heavy"}
EVENT_TYPES = {
    "run_started",
    "parent_turn_observed",
    "subagent_spawned",
    "subagent_completed",
    "subagent_errored",
    "resumed_after_interrupt",
    "run_completed",
    "run_abandoned",
    "note",
}
DEFAULT_OUTPUT = "docs/exec-plans/active/harness-efficiency-study-events.jsonl"


def _nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be >= 0")
    return parsed


@dataclass
class RunEvent:
    schema_version: int
    logged_at: str
    repo: str
    condition: str
    task_id: str
    run_index: int
    tier: str
    event_type: str
    model_name: str | None = None
    actor: str | None = None
    observed_turn_index: int | None = None
    note: str | None = None


def build_event(args: argparse.Namespace) -> RunEvent:
    if args.event_type == "parent_turn_observed" and args.observed_turn_index is None:
        raise ValueError("observed_turn_index is required for parent_turn_observed events")
    return RunEvent(
        schema_version=1,
        logged_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        repo=args.repo,
        condition=args.condition,
        task_id=args.task_id,
        run_index=args.run_index,
        tier=args.tier,
        event_type=args.event_type,
        model_name=args.model_name,
        actor=args.actor,
        observed_turn_index=args.observed_turn_index,
        note=args.note,
    )


def append_event(path: Path, event: RunEvent) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(event), sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to the JSONL event log.")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--condition", required=True, choices=sorted(CONDITIONS))
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--run-index", required=True, type=_nonnegative_int)
    parser.add_argument("--tier", required=True, choices=sorted(TIERS))
    parser.add_argument("--event-type", required=True, choices=sorted(EVENT_TYPES))
    parser.add_argument("--model-name")
    parser.add_argument("--actor")
    parser.add_argument("--observed-turn-index", type=_nonnegative_int)
    parser.add_argument("--note")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    event = build_event(args)
    output = Path(args.output)
    append_event(output, event)
    print(f"appended 1 event to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
