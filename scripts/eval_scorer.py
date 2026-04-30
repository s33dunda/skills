#!/usr/bin/env python3
"""Summarize harness-efficiency study JSONL run logs."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

DEFAULT_INPUT = "docs/exec-plans/active/harness-efficiency-study-runs.jsonl"


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


def _count_true(records: list[dict[str, Any]], key: str) -> int:
    return sum(1 for record in records if record.get(key) is True)


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[(record["tier"], record["condition"])].append(record)

    def metrics_for(items: list[dict[str, Any]]) -> dict[str, Any]:
        count = len(items)
        completed_count = _count_true(items, "completed")
        all_turn_records = [record for record in items if record.get("turns") is not None]
        exact_turn_records = [
            record for record in items
            if record.get("turns") is not None and record.get("turn_source", "exact") == "exact"
        ]
        observed_turn_records = [
            record for record in items
            if record.get("turns") is not None and record.get("turn_source") == "observed"
        ]
        token_records = [
            record for record in items
            if record.get("tokens_input") is not None or record.get("tokens_output") is not None
        ]
        return {
            "runs": count,
            "completed_runs": completed_count,
            "completion_rate": completed_count / count if count else 0.0,
            "mean_turns": _mean(all_turn_records, "turns"),
            "turn_run_count": len(all_turn_records),
            "mean_turns_exact": _mean(exact_turn_records, "turns"),
            "exact_turn_run_count": len(exact_turn_records),
            "mean_turns_observed": _mean(observed_turn_records, "turns"),
            "observed_turn_run_count": len(observed_turn_records),
            "mean_regressions": _mean(items, "regression_count"),
            "mean_clarifications": _mean(items, "clarification_count"),
            "mean_files_touched": _mean(items, "files_touched"),
            "mean_lines_changed": _mean(items, "lines_changed"),
            "mean_tokens_input": _mean(items, "tokens_input"),
            "mean_tokens_output": _mean(items, "tokens_output"),
            "token_run_count": len(token_records),
        }

    per_tier: dict[str, dict[str, Any]] = {}
    for (tier, condition), items in sorted(grouped.items()):
        per_tier.setdefault(tier, {})[condition] = metrics_for(items)

    aggregate_grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        aggregate_grouped[record["condition"]].append(record)
    aggregate = {
        condition: metrics_for(items)
        for condition, items in sorted(aggregate_grouped.items())
    }
    return {"aggregate": aggregate, "per_tier": per_tier}


def render_markdown(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("## Aggregate")
    lines.append("")
    lines.extend(_render_table(summary["aggregate"]))
    for tier, tier_summary in summary["per_tier"].items():
        lines.append("")
        lines.append(f"## Tier: {tier}")
        lines.append("")
        lines.extend(_render_table(tier_summary))
    return "\n".join(lines)


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _render_table(summary: dict[str, Any]) -> list[str]:
    lines = [
        "| Condition | Runs | Completion % | Mean turns | Turn runs | Mean exact turns | Exact turn runs | Mean observed turns | Observed turn runs | Mean regressions | Mean clarifications | Mean files | Mean lines | Mean input tokens | Mean output tokens | Token runs |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for condition, metrics in summary.items():
        lines.append(
            "| {condition} | {runs} | {completion_rate} | {mean_turns} | {turn_run_count} | {mean_turns_exact} | {exact_turn_run_count} | {mean_turns_observed} | {observed_turn_run_count} | {mean_regressions} | {mean_clarifications} | {mean_files_touched} | {mean_lines_changed} | {mean_tokens_input} | {mean_tokens_output} | {token_run_count} |".format(
                condition=condition,
                runs=metrics["runs"],
                completion_rate=_fmt(metrics["completion_rate"] * 100),
                mean_turns=_fmt(metrics["mean_turns"]),
                turn_run_count=metrics["turn_run_count"],
                mean_turns_exact=_fmt(metrics["mean_turns_exact"]),
                exact_turn_run_count=metrics["exact_turn_run_count"],
                mean_turns_observed=_fmt(metrics["mean_turns_observed"]),
                observed_turn_run_count=metrics["observed_turn_run_count"],
                mean_regressions=_fmt(metrics["mean_regressions"]),
                mean_clarifications=_fmt(metrics["mean_clarifications"]),
                mean_files_touched=_fmt(metrics["mean_files_touched"]),
                mean_lines_changed=_fmt(metrics["mean_lines_changed"]),
                mean_tokens_input=_fmt(metrics["mean_tokens_input"]),
                mean_tokens_output=_fmt(metrics["mean_tokens_output"]),
                token_run_count=metrics["token_run_count"],
            )
        )
    return lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to the JSONL run log.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = load_records(Path(args.input))
    summary = summarize(records)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(render_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
