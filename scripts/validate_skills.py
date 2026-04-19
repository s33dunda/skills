#!/usr/bin/env python3
"""Validate the installable skill directories in this monorepo."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def error(message: str) -> str:
    return f"ERROR: {message}"


def parse_frontmatter(skill_md: Path) -> tuple[dict[str, str], list[str]]:
    problems: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, [error(f"{skill_md.relative_to(ROOT)} must start with YAML frontmatter")]

    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, [error(f"{skill_md.relative_to(ROOT)} frontmatter is missing closing ---")]

    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            problems.append(error(f"{skill_md.relative_to(ROOT)} has malformed frontmatter line: {line!r}"))
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")

    return data, problems


def validate_skill(skill_dir: Path) -> list[str]:
    problems: list[str] = []
    rel_dir = skill_dir.relative_to(ROOT)
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return [error(f"{rel_dir} is missing SKILL.md")]

    frontmatter, fm_problems = parse_frontmatter(skill_md)
    problems.extend(fm_problems)

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not name:
        problems.append(error(f"{skill_md.relative_to(ROOT)} frontmatter is missing name"))
    elif name != skill_dir.name:
        problems.append(error(f"{skill_md.relative_to(ROOT)} name {name!r} does not match directory {skill_dir.name!r}"))

    if not description:
        problems.append(error(f"{skill_md.relative_to(ROOT)} frontmatter is missing description"))

    evals_json = skill_dir / "evals" / "evals.json"
    if evals_json.exists():
        try:
            data = json.loads(evals_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(error(f"{evals_json.relative_to(ROOT)} is invalid JSON: {exc}"))
        else:
            if data.get("skill_name") != skill_dir.name:
                problems.append(error(f"{evals_json.relative_to(ROOT)} skill_name must be {skill_dir.name!r}"))
            if not isinstance(data.get("evals"), list):
                problems.append(error(f"{evals_json.relative_to(ROOT)} must contain an evals list"))

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.rglob("*.py"):
            try:
                ast.parse(script.read_text(encoding="utf-8"))
            except SyntaxError as exc:
                problems.append(error(f"{script.relative_to(ROOT)} has Python syntax error: {exc}"))

    return problems


def main() -> int:
    if not SKILLS_DIR.exists():
        print(error("skills/ directory is missing"), file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        print(error("skills/ contains no skill directories"), file=sys.stderr)
        return 1

    problems: list[str] = []
    for skill_dir in skill_dirs:
        problems.extend(validate_skill(skill_dir))

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skill(s): {', '.join(path.name for path in skill_dirs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
