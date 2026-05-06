#!/usr/bin/env python3
"""Stdlib tests for eval_logger.py and eval_scorer.py."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_event_logger import append_event, build_event  # noqa: E402
from eval_event_recover import load_events, summarize_events  # noqa: E402
from eval_turn_backfill import backfill_records  # noqa: E402
from eval_logger import RunRecord, append_record, build_record  # noqa: E402
from eval_scorer import load_records, summarize  # noqa: E402
from unbounded_eval_logger import build_record as build_unbounded_record  # noqa: E402
from unbounded_eval_scorer import summarize as summarize_unbounded  # noqa: E402


class EvalEventLoggerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _args(self, **overrides: object) -> Namespace:
        data = {
            "repo": "fastapi",
            "condition": "control",
            "task_id": "fastapi-15401",
            "run_index": 0,
            "tier": "heavy",
            "event_type": "parent_turn_observed",
            "model_name": "gpt-5",
            "actor": "parent",
            "observed_turn_index": 3,
            "note": "third visible turn",
        }
        data.update(overrides)
        return Namespace(**data)

    def test_appends_valid_event(self) -> None:
        output = self.root / "events.jsonl"
        event = build_event(self._args())
        append_event(output, event)
        lines = output.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        data = json.loads(lines[0])
        self.assertEqual(data["event_type"], "parent_turn_observed")
        self.assertEqual(data["model_name"], "gpt-5")
        self.assertEqual(data["observed_turn_index"], 3)

    def test_requires_observed_turn_for_parent_turn_events(self) -> None:
        with self.assertRaisesRegex(ValueError, "observed_turn_index"):
            build_event(self._args(observed_turn_index=None))


class EvalLoggerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _args(self, **overrides: object) -> Namespace:
        data = {
            "repo": "fastapi",
            "condition": "treatment",
            "task_id": "fastapi-15401",
            "run_index": 0,
            "tier": "heavy",
            "completed": True,
            "turns": 12,
            "turn_source": None,
            "clarification_count": 1,
            "files_touched": 4,
            "lines_changed": 87,
            "regression_count": 0,
            "issue_number": 15401,
            "model_name": None,
            "duration_seconds": None,
            "usage_source": "none",
            "tokens_input": None,
            "tokens_output": None,
            "tests_before_green": True,
            "tests_after_green": True,
            "tests_before_summary": "baseline green",
            "tests_after_summary": "post-change green",
            "needs_human_scoring": False,
            "notes": "pilot",
        }
        data.update(overrides)
        return Namespace(**data)

    def test_appends_valid_record(self) -> None:
        output = self.root / "runs.jsonl"
        record = build_record(self._args(usage_source="subagent_notification"))
        append_record(output, record)

        lines = output.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        data = json.loads(lines[0])
        self.assertEqual(data["repo"], "fastapi")
        self.assertEqual(data["condition"], "treatment")
        self.assertEqual(data["turns"], 12)
        self.assertEqual(data["turn_source"], "exact")
        self.assertEqual(data["usage_source"], "subagent_notification")
        self.assertEqual(data["schema_version"], 1)
        self.assertIn("logged_at", data)

    def test_rejects_tokens_without_usage_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "usage_source"):
            build_record(self._args(tokens_input=10))

    def test_rejects_summary_without_boolean_status(self) -> None:
        with self.assertRaisesRegex(ValueError, "tests_before_green"):
            build_record(self._args(tests_before_green=None))

    def test_allows_missing_turns_for_uninstrumented_runs(self) -> None:
        record = build_record(self._args(turns=None, usage_source="none"))
        self.assertIsNone(record.turns)
        self.assertEqual(record.turn_source, "missing")

    def test_allows_observed_turns(self) -> None:
        record = build_record(self._args(turns=2, turn_source="observed"))
        self.assertEqual(record.turn_source, "observed")

    def test_rejects_missing_turns_with_non_missing_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "turn_source"):
            build_record(self._args(turns=None, turn_source="observed"))


class EvalScorerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _record(self, **overrides: object) -> dict[str, object]:
        base: dict[str, object] = {
            "schema_version": 1,
            "logged_at": "2026-04-28T18:20:40Z",
            "repo": "fastapi",
            "condition": "treatment",
            "task_id": "fastapi-15401",
            "run_index": 0,
            "tier": "heavy",
            "completed": True,
            "turns": 10,
            "turn_source": "exact",
            "clarification_count": 1,
            "files_touched": 4,
            "lines_changed": 100,
            "regression_count": 0,
            "usage_source": "none",
            "tokens_input": None,
            "tokens_output": None,
            "needs_human_scoring": False,
        }
        base.update(overrides)
        return base

    def test_load_and_summarize_records(self) -> None:
        output = self.root / "runs.jsonl"
        records = [
            self._record(condition="control", tier="light", turns=8, completed=True, files_touched=2),
            self._record(condition="control", tier="light", turns=12, completed=False, files_touched=6, regression_count=1),
            self._record(condition="treatment", tier="light", turns=6, completed=True, files_touched=3),
            self._record(condition="treatment", tier="heavy", turns=14, completed=True, files_touched=5, tokens_input=120, tokens_output=30, usage_source="api"),
        ]
        with output.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record) + "\n")

        loaded = load_records(output)
        summary = summarize(loaded)

        self.assertEqual(summary["aggregate"]["control"]["runs"], 2)
        self.assertEqual(summary["aggregate"]["control"]["completed_runs"], 1)
        self.assertEqual(summary["aggregate"]["control"]["turn_run_count"], 2)
        self.assertEqual(summary["aggregate"]["control"]["exact_turn_run_count"], 2)
        self.assertEqual(summary["aggregate"]["treatment"]["runs"], 2)
        self.assertAlmostEqual(summary["aggregate"]["treatment"]["completion_rate"], 1.0)
        self.assertAlmostEqual(summary["per_tier"]["light"]["control"]["mean_turns"], 10.0)
        self.assertAlmostEqual(summary["per_tier"]["light"]["control"]["mean_turns_exact"], 10.0)
        self.assertAlmostEqual(summary["per_tier"]["light"]["control"]["mean_regressions"], 0.5)

    def test_summarize_tolerates_missing_token_fields(self) -> None:
        summary = summarize(
            [
                self._record(condition="control", tier="medium", turns=9),
                self._record(condition="treatment", tier="medium", turns=7, tokens_input=80, tokens_output=20, usage_source="api"),
            ]
        )
        self.assertIsNone(summary["aggregate"]["control"]["mean_tokens_input"])
        self.assertEqual(summary["aggregate"]["control"]["token_run_count"], 0)
        self.assertEqual(summary["aggregate"]["treatment"]["token_run_count"], 1)
        self.assertEqual(summary["aggregate"]["treatment"]["mean_tokens_output"], 20)

    def test_summarize_tolerates_missing_turns(self) -> None:
        summary = summarize(
            [
                self._record(condition="control", tier="medium", turns=None),
                self._record(condition="treatment", tier="medium", turns=7),
            ]
        )
        self.assertEqual(summary["aggregate"]["control"]["exact_turn_run_count"], 0)
        self.assertIsNone(summary["aggregate"]["control"]["mean_turns_exact"])
        self.assertEqual(summary["aggregate"]["treatment"]["exact_turn_run_count"], 1)

    def test_summarize_tracks_observed_turns_separately(self) -> None:
        summary = summarize(
            [
                self._record(condition="control", tier="medium", turns=2, turn_source="observed"),
                self._record(condition="treatment", tier="medium", turns=7, turn_source="exact"),
            ]
        )
        self.assertEqual(summary["aggregate"]["control"]["turn_run_count"], 1)
        self.assertEqual(summary["aggregate"]["control"]["mean_turns"], 2)
        self.assertEqual(summary["aggregate"]["control"]["observed_turn_run_count"], 1)
        self.assertEqual(summary["aggregate"]["control"]["exact_turn_run_count"], 0)
        self.assertEqual(summary["aggregate"]["control"]["mean_turns_observed"], 2)


class UnboundedEvalTests(unittest.TestCase):
    def _args(self, **overrides: object) -> Namespace:
        data = {
            "repo": "fastapi/fastapi",
            "condition": "treatment",
            "task_id": "fastapi-navigation-routing",
            "task_type": "navigation",
            "run_index": 0,
            "tier": "heavy",
            "completed": True,
            "navigation_score": 3,
            "scope_score": 2,
            "validation_score": 3,
            "handoff_score": 2,
            "turns": 2,
            "turn_source": "observed",
            "clarification_count": 0,
            "files_touched": 0,
            "lines_changed": 0,
            "regression_count": 0,
            "model_name": "gpt-5",
            "duration_seconds": None,
            "usage_source": "none",
            "tokens_input": None,
            "tokens_output": None,
            "tests_before_green": None,
            "tests_after_green": None,
            "tests_before_summary": None,
            "tests_after_summary": None,
            "needs_human_scoring": False,
            "scoring_notes": "good map",
            "notes": "pilot",
        }
        data.update(overrides)
        return Namespace(**data)

    def test_unbounded_logger_builds_scored_record(self) -> None:
        record = build_unbounded_record(self._args())
        self.assertEqual(record.task_type, "navigation")
        self.assertEqual(record.turn_source, "observed")
        self.assertEqual(record.navigation_score, 3)
        self.assertEqual(record.scope_score, 2)

    def test_unbounded_logger_rejects_inconsistent_turn_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "turn_source"):
            build_unbounded_record(self._args(turns=None, turn_source="observed"))

    def test_unbounded_scorer_summarizes_rubric(self) -> None:
        records = [
            {
                "condition": "control",
                "tier": "medium",
                "task_type": "navigation",
                "completed": True,
                "navigation_score": 2,
                "scope_score": 1,
                "validation_score": 2,
                "handoff_score": 1,
                "turns": 2,
                "files_touched": 0,
                "lines_changed": 0,
                "regression_count": 0,
                "clarification_count": 0,
            },
            {
                "condition": "treatment",
                "tier": "medium",
                "task_type": "navigation",
                "completed": True,
                "navigation_score": 3,
                "scope_score": 3,
                "validation_score": 2,
                "handoff_score": 2,
                "turns": 2,
                "files_touched": 0,
                "lines_changed": 0,
                "regression_count": 0,
                "clarification_count": 0,
            },
        ]
        summary = summarize_unbounded(records)
        self.assertEqual(summary["aggregate"]["control"]["runs"], 1)
        self.assertEqual(summary["aggregate"]["treatment"]["mean_score_total"], 10)
        self.assertEqual(summary["by_task_type"]["navigation"]["control"]["mean_score_total"], 6)


class EvalEventRecoverTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_load_and_summarize_events(self) -> None:
        output = self.root / "events.jsonl"
        events = [
            {
                "schema_version": 1,
                "logged_at": "2026-04-29T12:00:00Z",
                "repo": "arrow-py/arrow",
                "condition": "control",
                "task_id": "arrow-1269",
                "run_index": 0,
                "tier": "light",
                "event_type": "run_started",
                "actor": "parent",
                "observed_turn_index": None,
                "note": None,
            },
            {
                "schema_version": 1,
                "logged_at": "2026-04-29T12:01:00Z",
                "repo": "arrow-py/arrow",
                "condition": "control",
                "task_id": "arrow-1269",
                "run_index": 0,
                "tier": "light",
                "event_type": "parent_turn_observed",
                "actor": "parent",
                "observed_turn_index": 4,
                "note": None,
            },
            {
                "schema_version": 1,
                "logged_at": "2026-04-29T12:02:00Z",
                "repo": "arrow-py/arrow",
                "condition": "control",
                "task_id": "arrow-1269",
                "run_index": 0,
                "tier": "light",
                "event_type": "resumed_after_interrupt",
                "actor": "parent",
                "observed_turn_index": None,
                "note": "picked back up",
            },
        ]
        with output.open("w", encoding="utf-8") as handle:
            for event in events:
                handle.write(json.dumps(event) + "\n")
        rows = summarize_events(load_events(output))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["max_observed_turn_index"], 4)
        self.assertEqual(rows[0]["interruptions"], 1)
        self.assertEqual(rows[0]["latest_event_type"], "resumed_after_interrupt")


class EvalTurnBackfillTests(unittest.TestCase):
    def test_backfills_missing_turns_from_event_rows(self) -> None:
        records = [
            {
                "repo": "astanin/python-tabulate",
                "condition": "control",
                "task_id": "python-tabulate-357",
                "run_index": 0,
                "turns": None,
            },
            {
                "repo": "astanin/python-tabulate",
                "condition": "treatment",
                "task_id": "python-tabulate-357",
                "run_index": 0,
                "turns": 5,
                "turn_source": "exact",
            },
        ]
        event_rows = [
            {
                "repo": "astanin/python-tabulate",
                "condition": "control",
                "task_id": "python-tabulate-357",
                "run_index": 0,
                "max_observed_turn_index": 2,
            }
        ]
        updated, changed = backfill_records(records, event_rows)
        self.assertEqual(changed, 1)
        self.assertEqual(updated[0]["turns"], 2)
        self.assertEqual(updated[0]["turn_source"], "observed")
        self.assertEqual(updated[1]["turn_source"], "exact")


if __name__ == "__main__":
    unittest.main()
