<!--
Keep each section short. If a section does not apply, write "n/a" rather
than deleting the heading — the headings are the template's enforcement.
-->

## What changed

<!-- One or two sentences. Name the skills / files touched. -->

## Why

<!-- Link the seed.md item, Open Question, audit gap, or issue that motivated
this. If this is a spec fix, name the principle it encodes. -->

## Acceptance criteria

<!-- Observable, mechanical. Not "feels cleaner". Examples:
     - `python3 scripts/validate_skills.py` exits 0.
     - `python3 skills/cultivate/scripts/audit_cultivate.py .` shows
       `Autonomy Workflow: missing: none`.
     - New eval prompt passes locally. -->

- [ ]
- [ ]

## Validation evidence

<!-- Paste the commands you ran and the relevant output (trimmed). -->

```
$ python3 scripts/validate_skills.py
...

$ python3 -m unittest scripts.test_validate_skills
...
```

## ExecPlan reference

<!-- If this PR implements part of a plan under `docs/plans/`, link it and
name the step. Otherwise write "n/a — single-file change" or equivalent. -->

## Breaking changes / migration

<!-- SKILL.md frontmatter shape? validator contract? CHANGELOG bump? If none,
write "none". If a skill version changes, confirm `CHANGELOG.md` is
updated and the frontmatter `version` is bumped. -->
