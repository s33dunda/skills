# Plot Schema

The `plot.md` output format. The file opens with YAML frontmatter for machine-readable fields, followed by prose sections for richer context.

## Template

```markdown
---
name: <kebab-case-project-name>
tagline: "<one sentence: what it does and for whom>"
stack: [<primary language>, <framework if any>, <runtime>]
status: draft
---

## Problem

<What friction or gap does this project address? Who feels it? Why does it matter now?>

## Audience

<Who uses this? Be specific -- "developers building MCP servers" is better than "developers".>

## Scope (MVP)

**In:**
- <core capability 1>
- <core capability 2>

**Out (explicitly):**
- <thing that's tempting but deferred>

## Stack

<Explain the choices. If undecided, say so and explain the tradeoffs being weighed.>

## Agents

<What will AI agents do in this repo? What tasks will they own or assist with? This drives what cultivate will encode.>

## Success

<What does a working v1 look like? What can you run, observe, or ship?>

## Constraints

<Timeline, team size, hard dependencies, things that cannot change. Omit section if none.>

## Open Questions

<Unresolved decisions that should be answered before or during s33d. Use TBD if genuinely unknown.>

## Prospect (optional)

<Market or competitive context, if researched.>

## Survey (optional)

<Technical prior art or existing code references, if researched.>
```

## Field Definitions

| Field | Required | Notes |
|-------|----------|-------|
| name | yes | kebab-case, becomes the repo name |
| tagline | yes | one sentence, present tense, specific |
| stack | yes | list, even rough preferences count |
| status | yes | always "draft" for a new plot |
| Problem | yes | why this exists |
| Audience | recommended | who benefits |
| Scope | recommended | MVP boundary, explicit outs matter |
| Stack (prose) | recommended | rationale, not just names |
| Agents | recommended | drives cultivate decisions |
| Success | recommended | observable v1 definition |
| Constraints | optional | only if real constraints exist |
| Open Questions | optional | unresolved decisions |
| Prospect | optional | only if researched |
| Survey | optional | only if researched |
