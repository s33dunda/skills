#!/usr/bin/env python3
"""Format eval results as markdown for GitHub Actions step summary."""
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_file")
    parser.add_argument("--skill", default="")
    args = parser.parse_args()

    with open(args.results_file) as f:
        data = json.load(f)

    skill = data.get("skill_name", args.skill)
    passed = data.get("passed", 0)
    total = data.get("total", 0)
    rate = data.get("pass_rate", 0)
    icon = "✅" if rate >= 0.6 else "❌"

    print(f"## {icon} Skill Evals: `{skill}`")
    print(f"\n**{passed}/{total} assertions passed ({rate:.0%})**\n")

    for ev in data.get("evals", []):
        ev_rate = ev.get("pass_rate", 0)
        ev_icon = "✅" if ev_rate >= 0.6 else "❌"
        print(f"### {ev_icon} Eval {ev['id']}")
        print(f"\n> {ev['prompt'][:120]}...\n")
        for g in ev.get("graded", []):
            check = "✓" if g["passed"] else "✗"
            print(f"- {check} {g['text']}")
        print()

if __name__ == "__main__":
    main()
