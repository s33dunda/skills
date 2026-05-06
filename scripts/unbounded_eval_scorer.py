#!/usr/bin/env python3
"""Summarize unbounded harness-efficiency study JSONL logs."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

DEFAULT_INPUT = "docs/exec-plans/active/unbounded-harness-study-runs.jsonl"
SCORE_KEYS = ("navigation_score", "scope_score", "validation_score", "handoff_score")


def load_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
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
            records.append(data)
    return records


def _mean(records: list[dict[str, Any]], key: str) -> float | None:
    values = [record[key] for record in records if record.get(key) is not None]
    if not values:
        return None
    return mean(values)


def _score_total(record: dict[str, Any]) -> int | None:
    values = [record.get(key) for key in SCORE_KEYS]
    if any(value is None for value in values):
        return None
    return sum(int(value) for value in values)


def _mean_score_total(records: list[dict[str, Any]]) -> float | None:
    totals = [_score_total(record) for record in records]
    scored = [total for total in totals if total is not None]
    if not scored:
        return None
    return mean(scored)


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    def metrics_for(items: list[dict[str, Any]]) -> dict[str, Any]:
        count = len(items)
        completed_count = sum(1 for item in items if item.get("completed") is True)
        scored_count = sum(1 for item in items if _score_total(item) is not None)
        return {
            "runs": count,
            "completed_runs": completed_count,
            "completion_rate": completed_count / count if count else 0.0,
            "scored_runs": scored_count,
            "mean_score_total": _mean_score_total(items),
            "mean_navigation_score": _mean(items, "navigation_score"),
            "mean_scope_score": _mean(items, "scope_score"),
            "mean_validation_score": _mean(items, "validation_score"),
            "mean_handoff_score": _mean(items, "handoff_score"),
            "mean_turns": _mean([item for item in items if item.get("turns") is not None], "turns"),
            "mean_files_touched": _mean(items, "files_touched"),
            "mean_lines_changed": _mean(items, "lines_changed"),
            "mean_regressions": _mean(items, "regression_count"),
            "mean_clarifications": _mean(items, "clarification_count"),
        }

    aggregate_grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    type_grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    tier_grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        aggregate_grouped[record["condition"]].append(record)
        type_grouped[(record["task_type"], record["condition"])].append(record)
        tier_grouped[(record["tier"], record["condition"])].append(record)

    by_type: dict[str, dict[str, Any]] = {}
    for (task_type, condition), items in sorted(type_grouped.items()):
        by_type.setdefault(task_type, {})[condition] = metrics_for(items)

    by_tier: dict[str, dict[str, Any]] = {}
    for (tier, condition), items in sorted(tier_grouped.items()):
        by_tier.setdefault(tier, {})[condition] = metrics_for(items)

    return {
        "aggregate": {condition: metrics_for(items) for condition, items in sorted(aggregate_grouped.items())},
        "by_task_type": by_type,
        "by_tier": by_tier,
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _render_table(summary: dict[str, Any]) -> list[str]:
    lines = [
        "| Condition | Runs | Completion % | Scored runs | Mean total score | Navigation | Scope | Validation | Handoff | Mean turns | Mean files | Mean lines | Mean regressions | Mean clarifications |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for condition, metrics in summary.items():
        lines.append(
            "| {condition} | {runs} | {completion_rate} | {scored_runs} | {mean_score_total} | {mean_navigation_score} | {mean_scope_score} | {mean_validation_score} | {mean_handoff_score} | {mean_turns} | {mean_files_touched} | {mean_lines_changed} | {mean_regressions} | {mean_clarifications} |".format(
                condition=condition,
                runs=metrics["runs"],
                completion_rate=_fmt(metrics["completion_rate"] * 100),
                scored_runs=metrics["scored_runs"],
                mean_score_total=_fmt(metrics["mean_score_total"]),
                mean_navigation_score=_fmt(metrics["mean_navigation_score"]),
                mean_scope_score=_fmt(metrics["mean_scope_score"]),
                mean_validation_score=_fmt(metrics["mean_validation_score"]),
                mean_handoff_score=_fmt(metrics["mean_handoff_score"]),
                mean_turns=_fmt(metrics["mean_turns"]),
                mean_files_touched=_fmt(metrics["mean_files_touched"]),
                mean_lines_changed=_fmt(metrics["mean_lines_changed"]),
                mean_regressions=_fmt(metrics["mean_regressions"]),
                mean_clarifications=_fmt(metrics["mean_clarifications"]),
            )
        )
    return lines


def render_markdown(summary: dict[str, Any]) -> str:
    lines = ["## Aggregate", ""]
    lines.extend(_render_table(summary["aggregate"]))
    for task_type, task_summary in summary["by_task_type"].items():
        lines.extend(["", f"## Task Type: {task_type}", ""])
        lines.extend(_render_table(task_summary))
    for tier, tier_summary in summary["by_tier"].items():
        lines.extend(["", f"## Tier: {tier}", ""])
        lines.extend(_render_table(tier_summary))
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to the JSONL run log.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = summarize(load_records(Path(args.input)))
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(render_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
