# BMAD Elicitation — Origins and Extension Guide

Plot's interactive loop (Step 3+ in `SKILL.md`) is a direct adoption of the [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) `bmad-advanced-elicitation` core skill. This file exists so future iterations of `plot` can evolve the elicitation loop without re-deriving the pattern from first principles.

## What BMAD is

BMAD (Breakthrough Method for Agile AI-Driven Development) is an open-source methodology that treats AI agents as first-class contributors in an agile workflow — analyst, PM, architect, dev, QA — each as a specialized persona with its own skills and outputs. The `core-skills` directory inside BMAD holds reusable techniques that any agent can invoke, and `bmad-advanced-elicitation` is the one that matters to plot.

Source:
- Repo: <https://github.com/bmad-code-org/BMAD-METHOD>
- Skill: `src/core-skills/bmad-advanced-elicitation/SKILL.md`
- Methods registry: `src/core-skills/bmad-advanced-elicitation/methods.csv` (50 methods across 11 categories)

License: MIT (same as ours). Attribution: this file.

## Why plot adopted it

The v0.1 plot flow asked every missing-field question in one pass. Two problems observed in practice:

1. **Cognitive overload.** A wall of 6–8 questions mid-conversation caused users to either answer the first two and ignore the rest, or give shallow "I dunno, figure it out" responses that degraded the artifact.
2. **No iteration surface.** Once questions were asked, there was no natural re-entry point for "wait, let me refine the agents section." The flow was linear: ask, answer, write.

BMAD's menu-driven loop fixes both. The user picks *one* area to zoom in on, gets 1–2 targeted questions, sees the draft update, and chooses whether to apply. Then the menu re-appears. The loop gives the user a steering wheel rather than a funnel.

## What we faithfully adopted

- CSV schema (`num, category, method_name, description, output_pattern`) — identical so methods can be portable.
- 5-item numbered menu with `[r]` reshuffle / `[a]` list all / `[x]` proceed.
- `HALT` discipline: after the menu, and after every "apply changes? (y/n/edit)" prompt.
- Smart Selection: pick methods by current context (gap state), balance categories, include 1–2 foundational + 3 specialized.
- Direct feedback re-enters the loop rather than breaking out.
- Multi-number input executes methods in sequence (`1,3,5`).

## What we deliberately diverged on

- **`[f]` free-form as a first-class menu item.** BMAD treats free-form input as implicit direct feedback. Plot surfaces it explicitly because pre-repo ideation often wants "just let me talk it out" as a discoverable option.
- **Batched apply-prompt on multi-number.** BMAD shows the apply prompt per-method. Plot batches it for multi-number input (`"1,3"` → run both → one apply prompt). Reduces ceremony when the user is rapid-firing.
- **Domain specialization.** BMAD methods are generic (analyst, writer, architect). Plot methods map to seed-schema fields (`agent` category → Agents section, `scope` category → Scope section). The `output_pattern` column encodes the mapping.

If BMAD upstream evolves its pattern, check these divergences before merging changes — they may or may not still make sense.

## Extending `methods.csv`

Add a method when either:

- A seed-schema field has no corresponding elicitation technique (check the `category → field` mapping in `SKILL.md`).
- A recurring user situation isn't served well by existing methods (e.g., "I know what I want to build but I'm stuck on the naming" → would justify a framing-category `Naming Workshop` method).

### Schema

| Column | Guidance |
|--------|----------|
| `num` | Monotonically increasing integer. Don't renumber — append. |
| `category` | One of: `framing`, `scope`, `agent`, `risk`, `context`. Add a new category only if 2+ new methods would fit it. |
| `method_name` | Title-Case, 2–4 words. Evocative; avoid generic (`Ask About X`). |
| `description` | One sentence. State what the method does AND why it's valuable. No periods at end (CSV convention). |
| `output_pattern` | Arrow-separated flow: `input → transformation → output`. Flexible; treated as a guide, not a template. |

### Quality bar

Before adding a method, verify:

1. It produces content for at least one seed-schema field (or improves one already present).
2. It's distinct enough from existing methods that the Smart Selection step would pick it in a situation the others wouldn't cover.
3. It survives the 5-method cap — if you can't imagine it making it into a realistic top-5 in any scenario, it's noise.

### Pruning

Methods that haven't been picked in real sessions for multiple iterations are candidates for removal. Track this in `CHANGELOG.md` when it happens.

## Upstream to watch

- **BMAD's party-mode** (multiple persona voices in one elicitation). Not adopted — plot is one user, one idea. Could be interesting for cultivate-style multi-agent context.
- **BMAD's CSV loader script** (`resolve_config.py` for layered config). Not adopted — plot's CSV is static. If plot ever gets team/personal customization, consider adopting.
- **BMAD's agent roster integration**. Out of scope for plot. In scope for a future `cultivate` elicitation pass (where different agent personas genuinely matter).

## Future iteration notes

Improvements that future `skill-creator`-driven iterations should consider:

- **Method chaining hints.** After certain methods complete, suggest the logical next method (`Agent Tasks Inventory` → `Cultivate Alignment`).
- **Persona seeding in framing methods.** `User Persona Zoom` currently asks the user to pick a persona. Could pre-suggest 2–3 based on extracted audience signal.
- **Eval coverage for the loop itself.** Current `evals/evals.json` tests the seed.md artifact. No eval tests the loop discipline (does the skill actually HALT? does it re-present the menu?). A scripted eval harness that simulates menu responses would close this gap.
- **Method decay weighting.** If a method fires repeatedly and produces the same "I don't know" response, the Smart Selection step should deprioritize it next reshuffle.
