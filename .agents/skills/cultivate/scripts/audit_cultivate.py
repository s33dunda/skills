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


def exists_all(root: Path, candidates: Iterable[str]) -> list[str]:
    """Return candidates that exist, preserving order.

    The caller can compare length with the input list when it needs to know
    whether a whole harness bundle is present.
    """
    return [candidate for candidate in candidates if (root / candidate).exists()]


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


def root_agents_text(root: Path) -> tuple[str, str | None]:
    for candidate in ("AGENTS.md", "AGENT.md"):
        path = root / candidate
        if path.exists():
            return read_small_text(path), candidate
    return "", None


def structured_signal(name: str, found: list[str], missing: list[str], recommendation: str) -> Signal:
    evidence = [f"{item} present" for item in found]
    status = "present" if not missing else "missing"
    if missing:
        evidence.append("Missing: " + ", ".join(missing))
    return Signal(name=name, status=status, evidence=evidence, recommendation=recommendation)


def agents_section_signal(root: Path) -> Signal:
    text, agents_name = root_agents_text(root)
    if not text or not agents_name:
        return Signal(
            name="AGENTS structural sections",
            status="missing",
            evidence=[],
            recommendation="Add a root AGENTS.md with Orientation, Useful Commands/Commands, Repository Map, Deeper Context, Definition of Done, When Blocked, and Never sections.",
        )

    checks = [
        ("Orientation", re.compile(r"^##\s+Orientation\b", re.MULTILINE)),
        ("Useful Commands/Commands", re.compile(r"^##\s+(?:Useful Commands|Commands)\b", re.MULTILINE)),
        ("Repository Map", re.compile(r"^##\s+Repository Map\b", re.MULTILINE)),
        ("Deeper Context", re.compile(r"^##\s+Deeper Context\b", re.MULTILINE)),
        ("Definition of Done", re.compile(r"^##\s+Definition of Done\b", re.MULTILINE)),
        ("When Blocked", re.compile(r"^##\s+When Blocked\b", re.MULTILINE)),
        ("Never", re.compile(r"^##\s+Never\b", re.MULTILINE)),
        ("Task-scoped work section", re.compile(r"^##\s+When (?:Writing|Reviewing|Planning|Releasing|Working)\b", re.MULTILINE)),
    ]
    found = [label for label, pattern in checks if pattern.search(text)]
    missing = [label for label, pattern in checks if not pattern.search(text)]
    return structured_signal(
        name="AGENTS structural sections",
        found=found,
        missing=missing,
        recommendation="Add the canonical AGENTS section shape so agents see commands, map, deeper docs, closure, escalation, and hard refusals in one place.",
    )


def agents_deeper_context_signal(root: Path) -> Signal:
    text, agents_name = root_agents_text(root)
    if not text or not agents_name:
        return Signal(
            name="AGENTS deep-context links",
            status="missing",
            evidence=[],
            recommendation="Add a Deeper Context section that links the root architecture and docs knowledge store from AGENTS.md.",
        )

    lower_text = text.lower()
    link_checks: list[tuple[str, list[str], list[str]]] = [
        ("ARCHITECTURE.md", ["ARCHITECTURE.md"], ["architecture.md"]),
        ("docs/PLANS.md", ["docs/PLANS.md"], ["docs/plans.md"]),
        ("docs/QUALITY.md", ["docs/QUALITY.md"], ["docs/quality.md"]),
        ("docs/RELIABILITY.md", ["docs/RELIABILITY.md"], ["docs/reliability.md"]),
        ("docs/SECURITY.md", ["docs/SECURITY.md"], ["docs/security.md"]),
        ("docs/design-docs/index.md", ["docs/design-docs/index.md", "docs/design-docs/README.md"], ["docs/design-docs/index.md", "docs/design-docs/readme.md"]),
        ("docs/product-specs/index.md", ["docs/product-specs/index.md", "docs/product-specs/README.md"], ["docs/product-specs/index.md", "docs/product-specs/readme.md"]),
        ("docs/exec-plans/active/", ["docs/exec-plans/active"], ["docs/exec-plans/active"]),
        ("docs/exec-plans/tech-debt-tracker.md", ["docs/exec-plans/tech-debt-tracker.md"], ["docs/exec-plans/tech-debt-tracker.md"]),
        ("docs/references/", ["docs/references"], ["docs/references"]),
    ]

    found: list[str] = []
    missing: list[str] = []
    for label, existing_candidates, needles in link_checks:
        if not any((root / candidate).exists() for candidate in existing_candidates):
            continue
        if any(needle in lower_text for needle in needles):
            found.append(label)
        else:
            missing.append(label)

    return structured_signal(
        name="AGENTS deep-context links",
        found=found,
        missing=missing,
        recommendation="When cultivated docs exist, AGENTS.md should point at them from a dedicated Deeper Context section instead of leaving the knowledge store orphaned.",
    )


def pyproject_project_dirs(root: Path) -> list[str]:
    """Infer top-level Python package directories from pyproject metadata."""
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return []

    text = read_small_text(pyproject)
    names = re.findall(r"(?m)^\s*name\s*=\s*[\"']([^\"']+)[\"']", text)
    dirs: list[str] = []
    for name in names:
        normalized = re.sub(r"[-.]+", "_", name).lower()
        for candidate in {normalized, name.lower()}:
            if candidate and (root / candidate).is_dir():
                dirs.append(candidate)
    return sorted(set(dirs))


def layerable_subtrees(root: Path) -> list[str]:
    """Return top-level subtrees where local AGENTS guidance may matter."""
    conventional = [
        "src",
        "lib",
        "tests",
        "test",
        "docs_src",
        "examples",
        "apps",
        "packages",
        "services",
        "cmd",
        "internal",
        "pkg",
    ]
    candidates = [item for item in conventional if (root / item).is_dir()]
    candidates.extend(pyproject_project_dirs(root))
    return sorted(set(candidates))


def nested_agents_files(root: Path) -> list[str]:
    matches: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        path = Path(dirpath)
        if path == root:
            continue
        if "AGENTS.md" in filenames:
            matches.append(rel(path / "AGENTS.md", root))
    return sorted(set(matches))


def nested_agents_signal(root: Path) -> Signal:
    subtrees = layerable_subtrees(root)
    if len(subtrees) < 2:
        return Signal(
            name="layered AGENTS coverage",
            status="present",
            evidence=["No obvious multi-surface repo shape detected; root AGENTS.md is likely enough."],
            recommendation="Add nested AGENTS.md only when distinct implementation, test, docs/example, app, package, or service subtrees need local guidance.",
        )

    covered = [subtree for subtree in subtrees if (root / subtree / "AGENTS.md").exists()]
    all_nested = nested_agents_files(root)
    target_count = min(2, len(subtrees))
    evidence: list[str] = [f"Layerable subtrees detected: {', '.join(subtrees)}"]
    if covered:
        evidence.append("Covered layerable subtrees: " + ", ".join(covered))
    if all_nested:
        evidence.append("Nested AGENTS.md files: " + ", ".join(sorted(all_nested)[:8]))

    status = "present" if len(covered) >= target_count else "missing"
    if status == "missing":
        missing = [subtree for subtree in subtrees if subtree not in covered]
        evidence.append("Missing nested guidance candidates: " + ", ".join(missing[:8]))

    return Signal(
        name="layered AGENTS coverage",
        status=status,
        evidence=evidence,
        recommendation="For large multi-surface repos, add short nested AGENTS.md files to the highest-leverage implementation, tests, docs/example, app, package, or service subtrees.",
    )


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


def bundle_signal(name: str, root: Path, required: list[str], recommendation: str) -> Signal:
    present = exists_all(root, required)
    missing = [item for item in required if item not in present]
    evidence = [f"{item} present" for item in present]
    status = "present" if not missing else "missing"
    if missing:
        evidence.append("Missing: " + ", ".join(missing))
    return Signal(name=name, status=status, evidence=evidence, recommendation=recommendation)


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

    harness_dirs = [
        "docs/design-docs",
        "docs/product-specs",
        "docs/exec-plans",
        "docs/exec-plans/active",
        "docs/exec-plans/completed",
        "docs/generated",
        "docs/references",
    ]
    harness_docs = [
        "ARCHITECTURE.md",
        "docs/PLANS.md",
        "docs/QUALITY.md",
        "docs/RELIABILITY.md",
        "docs/SECURITY.md",
    ]
    placeholder_docs = [
        "docs/design-docs/README.md",
        "docs/product-specs/README.md",
        "docs/exec-plans/active/README.md",
        "docs/exec-plans/completed/README.md",
        "docs/generated/README.md",
        "docs/references/README.md",
        "docs/design-docs/index.md",
        "docs/product-specs/index.md",
        "docs/exec-plans/tech-debt-tracker.md",
    ]

    signals = [
        signal("agent entrypoint", exists_any(root, ["AGENTS.md", "AGENT.md", ".github/copilot-instructions.md"]), "Add a short root AGENTS.md that maps commands, docs, and repo norms for agents."),
        agents_section_signal(root),
        agents_deeper_context_signal(root),
        nested_agents_signal(root),
        signal("human orientation", exists_any(root, ["README.md", "README.rst", "README.txt"]), "Add or update README with setup and project purpose; keep agent-only details in AGENTS.md."),
        signal("repository knowledge base", docs[:12], "Create a docs/ map for architecture, quality, plans, and operational truth."),
        signal("root architecture map", exists_any(root, ["ARCHITECTURE.md"]), "Add root ARCHITECTURE.md as the high-discoverability architecture map referenced from AGENTS.md."),
        bundle_signal("harness knowledge-store directories", root, harness_dirs, "Create docs/design-docs, docs/product-specs, docs/exec-plans/{active,completed}, docs/generated, and docs/references with README/index placeholders."),
        bundle_signal("harness operating docs", root, harness_docs, "Add root ARCHITECTURE.md plus docs/PLANS.md, docs/QUALITY.md, docs/RELIABILITY.md, and docs/SECURITY.md."),
        bundle_signal("knowledge-store placeholders", root, placeholder_docs, "Add README.md/index placeholders so empty harness directories survive git and explain when agents should use them."),
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
        "orientation": ["agent entrypoint", "AGENTS structural sections", "layered AGENTS coverage", "human orientation", "environment isolation"],
        "knowledge_system": [
            "AGENTS deep-context links",
            "repository knowledge base",
            "root architecture map",
            "harness knowledge-store directories",
            "harness operating docs",
            "knowledge-store placeholders",
            "architecture guidance",
            "execution-plan workflow",
        ],
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
