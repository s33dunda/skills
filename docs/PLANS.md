# Execution Plans

Complex work on this repo (multi-milestone, cross-cutting, or expected to span more than one agent session) runs against an ExecPlan checked in under `docs/plans/<slug>.md`.

## When to write one

- The change touches more than one skill or more than one concern (e.g. `SKILL.md` + evals + references + `CHANGELOG.md` in a single effort).
- Acceptance requires more than one observable signal.
- The work will span multiple agent sessions and a fresh agent will need to resume from the plan plus the working tree.
- There is risk of destructive or hard-to-reverse steps (breaking changes to a skill's public shape, eval contract changes, CI reshuffles).

Small, single-file changes do not need an ExecPlan.

## How to write one

Copy `docs/plans/_template.md` to `docs/plans/<slug>.md`. Keep the plan current as work proceeds:

- Update `Progress` at every stopping point.
- Record decisions in the `Decision L# Execution Plans

Complex work on this repo (multi-milestone, cross-cutting, or expected to er
Complex work onch 
## When to write one

- The change touches more than one skill or more than one concern (e.g. `SKILL.md` + evals + references + `CHANGELOG.md` in a single effort).
- Accepd t
- The change toucheci- Acceptance requires more than one observable signal.
- The work will span multiple agent sessions and a fresh agent will need to resume fron- The work will span multiple agent sessions and a fr i- There is risk of destructive or hard-to-reverse steps (breaking changes to a skill's public shape, eval contract chaal
Small, single-file changes do not need an ExecPlan.

## How to write one

Copy `docs/plans/_template.md` to `docs/plans/<slu
cd /Users/charlesdunda/Code/skills && ls -la docs/ docs/plans/ && echo "---VALIDATOR---" && python3 scripts/validate_skills.py && echo "---TESTS---" && python3 -m unittest scripts.test_validate_skills 2>&1 | tail -5 && echo "---AUDIT (autonomy_workflow section)---" && python3 skills/cultivate/scripts/audit_cultivate.py . 2>&1 | grep -A 1 -E "execution-plan workflow|repository knowledge base|Knowledge System|Autonomy Workflow" | head -20

ls -la /Users/charlesdunda/Code/skills/docs/ && ls -la /Users/charlesdunda/Code/skills/docs/plans/ && echo "---VALIDATOR---" && python3 /Users/charlesdunda/Code/skills/scripts/validate_skills.py && echo "---TESTS---" && (cd /Users/charlesdunda/Code/skills && python3 -m unittest scripts.test_validate_skills 2>&1 | tail -5) && echo "---AUDIT---" && python3 /Users/charlesdunda/Code/skills/skills/cultivate/scripts/audit_cultivate.py /Users/charlesdunda/Code/skills 2>&1 | tail -40

bash -c 'ls -la /Users/charlesdunda/Code/skills/docs/ && echo --- && ls -la /Users/charlesdunda/Code/skills/docs/plans/ && echo ---VALIDATOR--- && python3 /Users/charlesdunda/Code/skills/scripts/validate_skills.py && echo ---TESTS--- && cd /Users/charlesdunda/Code/skills && python3 -m unittest scripts.test_validate_skills 2>&1 | tail -5 && echo ---AUDIT--- && python3 /Users/charlesdunda/Code/skills/skills/cultivate/scripts/audit_cultivate.py /Users/charlesdunda/Code/skills 2>&1 | tail -40'

echo READY && python3 -c "import os; print('docs exists:', os.path.isdir('/Users/charlesdunda/Code/skills/docs'), 'plans exists:', os.path.isdir('/Users/charlesdunda/Code/skills/docs/plans'))"
