#!/usr/bin/env python3
"""Validate the installable skill directories in this monorepo."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
AGENTS_SKILLS_DIR = ROOT / ".agents" / "skills"
SYNC_IGNORE_DIRS = {"__pycache__"}
SYNC_IGNORE_SUFFIXES = {".pyc", ".pyo"}


def error(message: str) -> str:
    return f"ERROR: {message}"


BLOCK_SCALAR_INDICATORS = {">", ">-", ">+", "|", "|-", "|+"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$")

# Mirrors anthropics/skills skill-creator quick_validate.py so skills published
# from this repo stay loadable by the upstream validator.
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}
ALLOWED_METADATA_KEYS = {"version"}


def parse_frontmatter(skill_md: Path) -> tuple[dict[str, Any], list[str]]:
    problems: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, [error(f"{skill_md.relative_to(ROOT)} must start with YAML frontmatter")]

    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, [error(f"{skill_md.relative_to(ROOT)} frontmatter is missing closing ---")]

    data: dict[str, Any] = {}
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            problems.append(error(f"{skill_md.relative_to(ROOT)} has orphaned continuation line: {line!r}"))
            i += 1
            continue
        if ":" not in line:
            problems.append(error(f"{skill_md.relative_to(ROOT)} has malformed frontmatter line: {line!r}"))
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in BLOCK_SCALAR_INDICATORS:
            continuation: list[str] = []
            i += 1
            while i < end and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
                continuation.append(lines[i].strip())
                i += 1
            data[key] = " ".join(part for part in continuation if part)
            continue
        if value == "" and i + 1 < end and lines[i + 1].startswith((" ", "\t")):
            nested: dict[str, str] = {}
            i += 1
            while i < end and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
                subline = lines[i]
                if not subline.strip() or subline.strip().startswith("#"):
                    i += 1
                    continue
                if ":" not in subline:
                    problems.append(error(f"{skill_md.relative_to(ROOT)} has malformed frontmatter line: {subline!r}"))
                    i += 1
                    continue
                subkey, subvalue = subline.split(":", 1)
                nested[subkey.strip()] = subvalue.strip().strip('"').strip("'")
                i += 1
            data[key] = nested
            continue
        data[key] = value.strip('"').strip("'")
        i += 1

    return data, problems


def _display(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def validate_skill(skill_dir: Path) -> list[str]:
    problems: list[str] = []
    rel_dir = _display(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    rel_md = _display(skill_md)

    if not skill_md.exists():
        return [error(f"{rel_dir} is missing SKILL.md")]

    frontmatter, fm_problems = parse_frontmatter(skill_md)
    problems.extend(fm_problems)

    unexpected = sorted(set(frontmatter) - ALLOWED_FRONTMATTER_KEYS)
    if unexpected:
        problems.append(error(
            f"{rel_md} frontmatter has unexpected key(s): "
            f"{', '.join(unexpected)}. Allowed: {', '.join(sorted(ALLOWED_FRONTMATTER_KEYS))}"
        ))

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not name:
        problems.append(error(f"{rel_md} frontmatter is missing name"))
    elif name != skill_dir.name:
        problems.append(error(
            f"{rel_md} name {name!r} does not match directory {skill_dir.name!r}"
        ))

    if not description:
        problems.append(error(f"{rel_md} frontmatter is missing description"))

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        problems.append(error(f"{rel_md} frontmatter is missing metadata mapping"))
    else:
        unexpected_meta = sorted(set(metadata) - ALLOWED_METADATA_KEYS)
        if unexpected_meta:
            problems.append(error(
                f"{rel_md} metadata has unexpected key(s): "
                f"{', '.join(unexpected_meta)}. Allowed: {', '.join(sorted(ALLOWED_METADATA_KEYS))}"
            ))
        version = metadata.get("version")
        if not version:
            problems.append(error(f"{rel_md} metadata is missing version"))
        elif not SEMVER.match(version):
            problems.append(error(
                f"{rel_md} metadata.version {version!r} must be semver (X.Y.Z)"
            ))

    evals_json = skill_dir / "evals" / "evals.json"
    if evals_json.exists():
        rel_evals = _display(evals_json)
        try:
            data = json.loads(evals_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(error(f"{rel_evals} is invalid JSON: {exc}"))
        else:
            if data.get("skill_name") != skill_dir.name:
                problems.append(error(f"{rel_evals} skill_name must be {skill_dir.name!r}"))
            if not isinstance(data.get("evals"), list):
                problems.append(error(f"{rel_evals} must contain an evals list"))

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.rglob("*.py"):
            try:
                ast.parse(script.read_text(encoding="utf-8"))
            except SyntaxError as exc:
                problems.append(error(f"{_display(script)} has Python syntax error: {exc}"))

    return problems


def skill_dirs_in(directory: Path) -> list[Path]:
    return sorted(path for path in directory.iterdir() if path.is_dir())


def relative_files(directory: Path) -> set[Path]:
    files: set[Path] = set()
    for path in directory.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SYNC_IGNORE_DIRS for part in path.relative_to(directory).parts):
            continue
        if path.suffix in SYNC_IGNORE_SUFFIXES:
            continue
        files.add(path.relative_to(directory))
    return files


def validate_agents_mirror(primary_skill_dirs: list[Path]) -> list[str]:
    problems: list[str] = []
    if not AGENTS_SKILLS_DIR.exists():
        return [error(".agents/skills/ directory is missing; run `uv run python scripts/sync_agents_skills.py`")]

    primary_names = [path.name for path in primary_skill_dirs]
    mirror_dirs = skill_dirs_in(AGENTS_SKILLS_DIR)
    mirror_names = [path.name for path in mirror_dirs]

    missing = sorted(set(primary_names) - set(mirror_names))
    extra = sorted(set(mirror_names) - set(primary_names))
    if missing:
        problems.append(error(f".agents/skills/ missing mirrored skill(s): {', '.join(missing)}"))
    if extra:
        problems.append(error(f".agents/skills/ has extra skill(s): {', '.join(extra)}"))

    for mirror_dir in mirror_dirs:
        problems.extend(validate_skill(mirror_dir))

    for primary_dir in primary_skill_dirs:
        mirror_dir = AGENTS_SKILLS_DIR / primary_dir.name
        if not mirror_dir.exists():
            continue

        primary_files = relative_files(primary_dir)
        mirror_files = relative_files(mirror_dir)
        missing_files = sorted(primary_files - mirror_files)
        extra_files = sorted(mirror_files - primary_files)
        for path in missing_files:
            problems.append(error(f".agents/skills/{primary_dir.name} missing mirrored file {path.as_posix()}"))
        for path in extra_files:
            problems.append(error(f".agents/skills/{primary_dir.name} has extra file {path.as_posix()}"))
        for path in sorted(primary_files & mirror_files):
            source = primary_dir / path
            mirror = mirror_dir / path
            if source.read_bytes() != mirror.read_bytes():
                problems.append(error(
                    f".agents/skills/{primary_dir.name}/{path.as_posix()} differs from "
                    f"skills/{primary_dir.name}/{path.as_posix()}; run `uv run python scripts/sync_agents_skills.py`"
                ))

    return problems


def main() -> int:
    if not SKILLS_DIR.exists():
        print(error("skills/ directory is missing"), file=sys.stderr)
        return 1

    skill_dirs = skill_dirs_in(SKILLS_DIR)
    if not skill_dirs:
        print(error("skills/ contains no skill directories"), file=sys.stderr)
        return 1

    problems: list[str] = []
    for skill_dir in skill_dirs:
        problems.extend(validate_skill(skill_dir))
    problems.extend(validate_agents_mirror(skill_dirs))

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    print(
        f"Validated {len(skill_dirs)} skill(s) and .agents mirror: "
        f"{', '.join(path.name for path in skill_dirs)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
