#!/usr/bin/env python3
"""Sync installable skills into .agents/skills for repo-local agent clients."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "skills"
TARGET_DIR = ROOT / ".agents" / "skills"

IGNORE_NAMES = {"__pycache__", ".DS_Store"}


def ignore_generated(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in IGNORE_NAMES or name.endswith((".pyc", ".pyo"))}


def sync() -> list[str]:
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"source skills directory missing: {SOURCE_DIR}")

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    source_skill_names = sorted(path.name for path in SOURCE_DIR.iterdir() if path.is_dir())
    for stale in sorted(path for path in TARGET_DIR.iterdir() if path.is_dir() and path.name not in source_skill_names):
        shutil.rmtree(stale)

    for name in source_skill_names:
        source = SOURCE_DIR / name
        target = TARGET_DIR / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target, ignore=ignore_generated)

    return source_skill_names


def main() -> int:
    names = sync()
    print(f"Synced {len(names)} skill(s) to .agents/skills: {', '.join(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
