#!/usr/bin/env python3
"""Run skill evals using the Claude CLI and grade results."""
import argparse
import json
import os
import subprocess
import sys
import tempfile

def run_eval(skill_path, prompt, skill_name):
    """Run a single eval with the skill loaded."""
    full_prompt = f"""You have access to the following skill. Follow its instructions to complete the task.

SKILL ({skill_name}):
---
{open(f'{skill_path}/SKILL.md').read()}
---

TASK: {prompt}

Complete this task following the skill instructions. If the skill produces a file output, write it to the current directory."""

    result = subprocess.run(
        ["claude", "-p", full_prompt, "--output-format", "text"],
        capture_output=True, text=True, timeout=120
    )
    return result.stdout if result.returncode == 0 else f"ERROR: {result.stderr}"

def grade(output, assertions):
    """Simple keyword-based grading."""
    results = []
    for a in assertions:
        text = a.get("text", "")
        # Basic heuristics based on assertion text
        passed = False
        evidence = "auto-graded"
        lo = output.lower()
        if "yaml frontmatter" in text.lower() or "frontmatter" in text.lower():
            passed = output.strip().startswith("---") and "name:" in output and "tagline:" in output
        elif "agents section" in text.lower():
            passed = "## agents" in lo or "## agent" in lo
        elif "kebab-case" in text.lower():
            import re
            m = re.search(r'^name:\s*(\S+)', output, re.MULTILINE)
            passed = bool(m and re.match(r'^[a-z][a-z0-9-]+$', m.group(1)))
        elif "explicit out" in text.lower() or "scope out" in text.lower():
            passed = "**out" in lo or "out (explicitly" in lo
        elif "success section" in text.lower():
            passed = "## success" in lo
        elif "agents reflects" in text.lower() or "write features" in text.lower():
            passed = "write features" in lo and "pr" in lo
        elif "crud" in text.lower():
            passed = "crud" in lo or ("create" in lo and "read" in lo and "update" in lo)
        elif "typescript" in text.lower():
            passed = "typescript" in lo
        elif "clarifying questions" in text.lower() or "asks questions" in text.lower():
            passed = "?" in output and ("question" in lo or "clarif" in lo)
        elif "trigger" in text.lower():
            passed = "trigger" in lo
        elif "stack" in text.lower() and "question" in text.lower():
            passed = any(x in lo for x in ["stack", "language", "swift", "python", "script type"])
        elif "open questions" in text.lower():
            passed = "open questions" in lo or "tbd" in lo
        else:
            passed = len(output) > 100  # fallback: non-empty output
        results.append({"text": text, "passed": passed, "evidence": evidence})
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--evals", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--pass-threshold", type=float, default=0.6)
    args = parser.parse_args()

    with open(args.evals) as f:
        evals_data = json.load(f)

    skill_name = evals_data.get("skill_name", os.path.basename(args.skill))
    evals = evals_data.get("evals", [])

    all_results = []
    total_assertions = 0
    total_passed = 0
    details_lines = []

    for ev in evals:
        prompt = ev["prompt"]
        assertions = ev.get("assertions", [])
        print(f"Running eval {ev['id']}: {prompt[:60]}...", file=sys.stderr)

        output = run_eval(args.skill, prompt, skill_name)
        graded = grade(output, assertions)

        passed = sum(1 for g in graded if g["passed"])
        total = len(graded)
        total_passed += passed
        total_assertions += total

        details_lines.append(f"**Eval {ev['id']}** — {passed}/{total} passed")
        for g in graded:
            icon = "✓" if g["passed"] else "✗"
            details_lines.append(f"  {icon} {g['text']}")

        all_results.append({"eval_id": ev["id"], "prompt": prompt, "output": output, "graded": graded, "pass_rate": passed/total if total else 0})

    overall_rate = total_passed / total_assertions if total_assertions else 0
    summary = {
        "skill_name": skill_name,
        "passed": total_passed,
        "total": total_assertions,
        "pass_rate": overall_rate,
        "evals": all_results,
        "details": "\n".join(details_lines)
    }

    with open(args.output, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"{skill_name}: {total_passed}/{total_assertions} ({overall_rate:.0%})", file=sys.stderr)
    sys.exit(0 if overall_rate >= args.pass_threshold else 1)

if __name__ == "__main__":
    main()
