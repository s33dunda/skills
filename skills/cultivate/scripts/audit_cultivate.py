#!/usr/bin/env python3
"""Read-only repository cultivate scanner.

Reports signals that make a repository easier for coding agents to navigate,
validate, and maintain. The scanner is intentionally heuristic: it should guide
human/agent judgment, not pretend to grade every repo perfectly.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Signal:
    name: str
    status: str
    evidence: list[str]
    recommendation: str


TEXT_EXTENSIONS = {
    ".md", ".mdx", ".txt", ".rst", ".toml", ".json", ".yaml", ".yml", ".ini", ".cfg",
}

SKIP_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "node_modules", "dist", "build", "target",
    ".next", ".cache", "__pycache__",
}

STALE_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bFIXME\b", re.IGNORECASE),
    re.compile(r"out of date", re.IGNORECASE),
    re.compile(r"deprecated", re.IGNORECASE),
    re.compile(r"coming soon", re.IGNORECASE),
]


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def exists_any(root: Path, candidates: Iterable[str]) -> list[str]:
    found: list[str] = []
    for candidate in candidates:
        if (root / candidate).exists():
            found.append(candidate)
    return found


def walk_files(root: Path, max_files: int = 4000) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            files.append(Path(dirpath) / filename)
            if len(files) >= max_files:
                return files
    return files


def read_small_text(path: Path, limit: int = 120_000) -> str:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return ""
    try:
        return path.read_bytes()[:limit].decode("utf-8", errors="ignore")
    except OSError:
        return ""


def is_repo_guidance_file(path: str) -> bool:
    """Return true for files likely to describe the repo cultivate itself."""
    lower = path.lower()
    name = Path(path).name.lower()
    return (
        name in {"agents.md", "agent.md", "readme.md", "readme.rst", "readme.txt"}
        or lower.startswith(("docs/", "doc/", ".github/"))
    )


def find_files_containing(root: Path, patterns: list[re.Pattern[str]], files: list[Path]) -> list[str]:
    matches: list[str] = []
    for path in files:
        text = read_small_text(path)
        if text and any(pattern.search(text) for pattern in patterns):
            matches.append(rel(path, root))
    return sorted(set(matches))


def signal(name: str, evidence: list[str], recommendation: str) -> Signal:
    return Signal(name=name, status="present" if evidence else "missing", evidence=evidence, recommendation=recommendation)


def environment_evidence(root: Path) -> list[str]:
    evidence: list[str] = []
    if (root / "uv.lock").exists():
        evidence.append("uv.lock present; prefer uv run for Python commands")
    if (root / "package-lock.json").exists() or (root / "pnpm-lock.yaml").exists() or (root / "yarn.lock").exists():
        evidence.append("JavaScript lockfile present; use the repo's package manager for commands")
    if (root / "Cargo.lock").exists():
        evidence.append("Cargo.lock present; use cargo for Rust commands")
    if (root / "go.mod").exists():
        evidence.append("go.mod present; use go commands from the module root")
    return evidence


def documentation_validation_commands(root: Path, files: list[Path]) -> list[str]:
    command_patterns = [
        re.compile(r"\b(?:uv run )?pytest\b"),
        re.compile(r"\buv run ruff check\b"),
        re.compile(r"\bruff check\b"),
        re.compile(r"\b(?:uv run )?mypy\b"),
        re.compile(r"\b(?:uv run )?pyright\b"),
        re.compile(r"\btox\b|\bnox\b"),
        re.compile(r"\bnpm run (?:test|lint|typecheck|check|build)\b"),
        re.compile(r"\bpnpm (?:test|lint|typecheck|check|build)\b"),
        re.compile(r"\byarn (?:test|lint|typecheck|check|build)\b"),
        re.compile(r"\bgo test\b"),
        re.compile(r"\bcargo test\b"),
        re.compile(r"\bmake (?:test|lint|typecheck|check|build)\b"),
        re.compile(r"\bcheck_connection\.py\b"),
        re.compile(r"\bvalidate_skills\.py\b"),
    ]
    evidence: list[str] = []
    for file in files:
        relative = rel(file, root)
        if not relative.lower().endswith((".md", ".rst", ".txt")):
            continue
        text = read_small_text(file)
        if any(pattern.search(text) for pattern in command_patterns):
            evidence.append(f"{relative} documents validation/check commands")
    return sorted(set(evidence))


def package_commands(root: Path) -> list[str]:
    evidence: list[str] = []
    package_json = root / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            for key in sorted(data.get("scripts", {})):
                if any(term in key.lower() for term in ["test", "lint", "type", "check", "build"]):
                    evidence.append(f"package.json script: {key}")
        except Exception:
            evidence.append("package.json exists but could not be parsed")

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        text = read_small_text(pyproject).lower()
        for term in ["pytest", "ruff", "mypy", "pyright", "tox", "nox"]:
            if term in text:
                evidence.append(f"pyproject.toml references {term}")

    makefile = root / "Makefile"
    if makefile.exists():
        text = read_small_text(makefile)
        for target in ["test", "lint", "typecheck", "check", "build"]:
            if re.search(rf"^{re.escape(target)}\s*:", text, re.MULTILINE):
                evidence.append(f"Makefile target: {target}")

    return sorted(set(evidence))


def analyze(root: Path) -> dict:
    root = root.resolve()
    files = walk_files(root)
    rel_files = [rel(path, root) for path in files]
    guidance_files = [path for path in files if is_repo_guidance_file(rel(path, root))]

    docs = [p for p in rel_files if p.lower().startswith(("docs/", "doc/"))]
    workflows = [p for p in rel_files if p.startswith(".github/workflows/")]
    scripts = [p for p in rel_files if p.startswith(("scripts/", "bin/", "tools/"))]
    tests = [p for p in rel_files if p.startswith(("tests/", "test/")) or Path(p).name.startswith("test_") or Path(p).name.endswith(".test.ts")]

    architecture_patterns = [re.compile(r"architecture|dependency|layer|boundary|module", re.IGNORECASE)]
    observability_patterns = [re.compile(r"log|metric|trace|span|observability|telemetry|health", re.IGNORECASE)]
    plan_patterns = [re.compile(r"exec\s*plan|execution plan|decision log|progress", re.IGNORECASE)]
    guardrail_patterns = [re.compile(r"guardrail|validator|frontmatter|installability|lint|typecheck|mypy|ruff|eslint|schema|dependency rule|import rule", re.IGNORECASE)]

    signals = [
        signal("agent entrypoint", exists_any(root, ["AGENTS.md", "AGENT.md", ".github/copilot-instructions.md"]), "Add a short root AGENTS.md that maps commands, docs, and repo norms for agents."),
        signal("human orientation", exists_any(root, ["README.md", "README.rst", "README.txt"]), "Add or update README with setup and project purpose; keep agent-only details in AGENTS.md."),
        signal("repository knowledge base", docs[:12], "Create a docs/ map for architecture, quality, plans, and operational truth."),
        signal("architecture guidance", find_files_containing(root, architecture_patterns, guidance_files)[:12], "Document architecture boundaries and promote repeated boundary rules into checks."),
        signal("execution-plan workflow", find_files_containing(root, plan_patterns, guidance_files)[:12], "Add a lightweight plan template for complex or multi-session work."),
        signal("mechanical validation commands", (package_commands(root) + documentation_validation_commands(root, guidance_files))[:12], "Expose exact test/lint/type/build/smoke-check commands in AGENTS.md and CI."),
        signal("environment isolation", environment_evidence(root), "Document the repo-specific command runner, such as uv, npm, cargo, or go, so agents do not depend on global tools."),
        signal("CI workflows", workflows[:12], "Add CI for tests and high-value guardrails so agents get reliable feedback."),
        signal("test suite", tests[:12], "Add focused tests or smoke checks for critical behavior."),
        signal("agent-usable scripts", scripts[:12], "Create scripts for repeated validation, generation, audits, or maintenance tasks."),
        signal("guardrail references", find_files_containing(root, guardrail_patterns, guidance_files)[:12], "Turn repeated quality expectations into local tooling with actionable errors."),
        signal("observability/debugging guidance", find_files_containing(root, observability_patterns, guidance_files)[:12], "Document logs, metrics, traces, health endpoints, and debugging workflows agents can inspect."),
        signal("PR/issue workflow", exists_any(root, [".github/pull_request_template.md", ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE"]), "Add PR/issue templates that ask for acceptance criteria and validation evidence."),
    ]

    stale_hits = find_files_containing(root, STALE_PATTERNS, files)[:20]
    present = {item.name for item in signals if item.status == "present"}
    categories = {
        "orientation": ["agent entrypoint", "human orientation", "environment isolation"],
        "knowledge_system": ["repository knowledge base", "architecture guidance", "execution-plan workflow"],
        "enforceable_rules": ["mechanical validation commands", "CI workflows", "guardrail references"],
        "validation_feedback": ["test suite", "observability/debugging guidance", "agent-usable scripts"],
        "autonomy_workflow": ["execution-plan workflow", "PR/issue workflow"],
        "entropy_control": ["guardrail references", "agent-usable scripts"],
    }

    return {
        "repo": str(root),
        "signals": [asdict(item) for item in signals],
        "categories": {
            category: {
                "present": [name for name in names if name in present],
                "missing": [name for name in names if name not in present],
            }
            for category, names in categories.items()
        },
        "stale_doc_risk_markers": stale_hits,
        "scanned_files": len(files),
    }


def markdown_report(result: dict) -> str:
    lines: list[str] = [f"# Cultivate Audit: `{result['repo']}`", "", f"Scanned files: {result['scanned_files']}", "", "## Signals", ""]
    for item in result["signals"]:
        lines.append(f"### {item['name']} - {item['status']}")
        if item["evidence"]:
            lines.extend(f"- {evidence}" for evidence in item["evidence"][:8])
        else:
            lines.append(f"- Recommendation: {item['recommendation']}")
        lines.append("")

    lines.extend(["## Gap Categories", ""])
    for category, status in result["categories"].items():
        title = category.replace("_", " ").title()
        missing = ", ".join(status["missing"]) or "none"
        present = ", ".join(status["present"]) or "none"
        lines.append(f"- {title}: present: {present}; missing: {missing}")
    lines.append("")

    if result["stale_doc_risk_markers"]:
        lines.extend(["## Stale Doc Risk Markers", ""])
        lines.extend(f"- {path}" for path in result["stale_doc_risk_markers"])
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit repository cultivate signals for coding agents.")
    parser.add_argument("repo", nargs="?", default=".", help="Repository path to scan. Defaults to current directory.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = parser.parse_args()

    root = Path(args.repo)
    if not root.exists() or not root.is_dir():
        parser.error(f"repo path does not exist or is not a directory: {root}")

    result = analyze(root)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else markdown_report(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
