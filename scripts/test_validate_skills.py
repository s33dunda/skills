#!/usr/bin/env python3
"""Fixture-based tests for scripts/validate_skills.py (stdlib only)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from textwrap import dedent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skills import validate_skill  # noqa: E402


def _write_skill(root: Path, name: str, frontmatter: str, body: str = "") -> Path:
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(f"---\n{frontmatter}---\n\n{body}", encoding="utf-8")
    return skill_dir


class ValidateSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_accepts_valid_skill(self) -> None:
        skill = _write_skill(
            self.root,
            "good",
            dedent(
                """\
                name: good
                description: A valid test skill.
                metadata:
                  version: "1.2.3"
                """
            ),
        )
        self.assertEqual(validate_skill(skill), [])

    def test_rejects_missing_metadata(self) -> None:
        skill = _write_skill(
            self.root,
            "no_meta",
            dedent(
                """\
                name: no_meta
                description: Missing metadata.
                """
            ),
        )
        problems = validate_skill(skill)
        self.assertTrue(
            any("missing metadata mapping" in p for p in problems),
            problems,
        )

    def test_rejects_missing_version(self) -> None:
        skill = _write_skill(
            self.root,
            "no_version",
            dedent(
                """\
                name: no_version
                description: Missing version.
                metadata:
                  version: ""
                """
            ),
        )
        problems = validate_skill(skill)
        self.assertTrue(
            any("metadata is missing version" in p for p in problems),
            problems,
        )

    def test_rejects_non_semver(self) -> None:
        skill = _write_skill(
            self.root,
            "bad_ver",
            dedent(
                """\
                name: bad_ver
                description: Non-semver version.
                metadata:
                  version: "v1"
                """
            ),
        )
        problems = validate_skill(skill)
        self.assertTrue(
            any("must be semver" in p for p in problems),
            problems,
        )

    def test_rejects_unexpected_top_level_key(self) -> None:
        skill = _write_skill(
            self.root,
            "extra",
            dedent(
                """\
                name: extra
                description: Has unexpected key.
                version: "1.0.0"
                metadata:
                  version: "1.0.0"
                """
            ),
        )
        problems = validate_skill(skill)
        self.assertTrue(
            any("unexpected key" in p for p in problems),
            problems,
        )

    def test_rejects_unexpected_metadata_key(self) -> None:
        skill = _write_skill(
            self.root,
            "meta_extra",
            dedent(
                """\
                name: meta_extra
                description: Unexpected metadata key.
                metadata:
                  version: "1.0.0"
                  author: "nobody"
                """
            ),
        )
        problems = validate_skill(skill)
        self.assertTrue(
            any("metadata has unexpected key" in p for p in problems),
            problems,
        )


if __name__ == "__main__":
    unittest.main()
