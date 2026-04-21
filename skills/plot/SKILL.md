---
name: plot
description: >-
  Plot a project -- capture the minimum viable idea so it can be grown into a real repo. Use
  this skill whenever the user wants to kick off a new project, describe an idea, flesh out
  a concept, or produce a structured brief that the cultivate skill can act on. Trigger on
  phrases like "I want to build", "new project idea", "let's start a project", "make a plan
  for", "I have an idea", or any time the user is at the ideation stage before a repo
  exists. Plot reads whatever context already exists in the conversation -- don't re-ask
  things already established -- then asks targeted questions to fill the gaps. Output is a
  seed.md file: a structured, agent-legible brief.
metadata:
  version: "0.2.1"
---

# Plot

Plot is the first step in the agricultural workflow:

**plot → seed.md → cultivate → farmers**

Its job is to capture the minimum viable idea -- enough signal that a repo can be created, seeded, and cultivated for AI agent execution. Think of it as turning a raw idea into a brief that removes ambiguity for every downstream step.

---

## CRITICAL LLM INSTRUCTIONS

- **MANDATORY:** Execute the steps in FLOW in exact order.
- Do NOT skip Step 1. Gather before you ask.
- Do NOT dump a wall of questions on the user. Use the menu-driven elicitation loop.
- **HALT** after presenting the menu and after every "apply these changes?" prompt. Wait for user input.
- Write `seed.md` only when the user picks `x`.

---

## FLOW

### Step 1 -- Gather Ambient Context

Before asking anything, collect signal from three sources in parallel:

1. **Conversation history.** Scan the current thread for already-stated project fields. The user may have explained the project at length already; don't waste their time repeating questions.
2. **Working directory.** Scan the filesystem per `references/repo-signals.md` (git remote → name, manifests → stack, README → tagline/problem, existing `seed.md` → baseline).
3. **Existing artifacts.** If `seed.md`, `plot.md`, or `AGENTS.md` exist, treat them as prior state to merge, not overwrite.

Build a draft seed.md in memory. Fields without signal are `?`. Do not invent content.

### Step 2 -- Present the Status Board

Show the user exactly what was gathered and what's still missing, in the format documented in `references/repo-signals.md`. Keep it compact — no more than 10 lines.

### Step 3 -- Offer Elicitation Methods

Load `./methods.csv`. The CSV columns are: `num, category, method_name, description, output_pattern`.

**Smart Selection.** Pick 5 methods that best fit the current gaps:

- Methods 1-2 should target the most urgent gaps (required fields still `?`: name, tagline, stack, problem).
- Methods 3-5 may explore recommended fields (audience, scope, agents, success) or apply critical techniques (risk, context).
- Always include at least one `agent`-category method if `agents` is `?` — that field drives cultivate.
- Balance categories. Don't pick 5 from the same category unless all gaps cluster there.

**No-gaps case (refinement mode).** When `seed.md` already exists and every
required + recommended field is populated, Smart Selection shifts from
gap-filling to pressure-testing. The user is refining a mature artifact, not
plotting from scratch:

- Skew toward `risk` and `context` categories (Pre-mortem, Constraints Audit,
  Prior Art Survey, Competitive Complaint Scan). These stress-test claims and
  surface positioning.
- Revisit `scope` if the seed is more than a few weeks old — Explicit Outs and
  Success Definition often need sharpening once the project has bumped into
  reality.
- Include one `agent`-category method (Cultivate Alignment) whenever the
  user's plans for the repo might have evolved since the last cultivate run.
- De-prioritize `framing`-category methods unless the user explicitly signals
  the core pitch has drifted. First Principles on a solved problem wastes
  the top-5 slots.

**Display Format:**

```
**Plot Elicitation Options**
Choose a number (1-5), [r] to Reshuffle, [a] List All, [f] Free-form, or [x] to Write seed.md:

1. [Method Name] — [one-line from description]
2. [Method Name] — [one-line from description]
3. [Method Name] — [one-line from description]
4. [Method Name] — [one-line from description]
5. [Method Name] — [one-line from description]
r. Reshuffle the list with 5 new options
a. List all methods with descriptions
f. Free-form — you describe, I extract
x. Write seed.md now (unknowns marked TBD)
```

**HALT and await response.**

### Step 4 -- Handle the Response

**Case 1-5 (numbered method):**

1. Execute the selected method using its `description` and `output_pattern` from the CSV.
2. Apply it to the current draft — ask the 1-2 targeted questions the method calls for, using whatever persona / framing the method prescribes.
3. **HALT** for the user's answer.
4. Update the draft with what you heard. Show only the fields that changed.
5. Ask: **"Apply these changes to the draft? (y/n/edit)"** and **HALT**.
6. If `y`: persist. If `n`: discard. If `edit` or any other reply: apply the user's revision.
7. Re-present the Step 2 status board + the Step 3 menu.

**Case r (Reshuffle):** Pick 5 different methods from the CSV using Smart Selection, re-present the menu.

**Case a (List All):** Compact table of every method (`num`, `method_name`, `description`). Let the user pick by number; then execute as Case 1-5.

**Case f (Free-form):** Invite the user to describe the project however they want. Extract fields from their prose, update the draft, then re-present the status board + menu.

**Case x (Proceed):** Go to Step 5.

**Case: Direct Feedback** (user responds with substantive content instead of a menu letter): Apply it to the draft as Case f. Re-present the menu.

**Case: Multiple Numbers** (e.g. "1,3"): Execute each method in sequence, with a single "apply these changes?" prompt at the end. Re-present the menu.

**Loop invariants:**

- Always re-present the menu after each method.
- The loop terminates only on `x` or explicit user override ("just write it", "good enough", etc.).
- Never write `seed.md` mid-loop.

### Step 5 -- Write seed.md and Hand Off

When the user picks `x`:

1. Write `seed.md` to the working directory using `references/seed-schema.md`. Mark any still-unknown fields as `TBD` rather than guessing.
2. Summarize briefly: what was captured, what's `TBD`, any fields the user might want to resolve before cultivate runs.
3. Suggest next step: running `cultivate` against the working directory (new repo) or the current repo (existing codebase).

---

## Cultivate Alignment

The `agents` field is the most important one for cultivate downstream. Cultivate's job is to make the repo legible and enforceable for AI agents — but what that means depends entirely on what those agents will do.

Examples:

- "agents will write features and open PRs" → cultivate needs AGENTS.md, PR templates, and CI feedback loops
- "agents will run evals and publish results" → cultivate needs execution-plan conventions and structured output paths
- "agents will manage releases" → cultivate needs version conventions, changelog format, and release scripts

If the user hasn't surfaced this by the end of the elicitation loop, the `Agent Tasks Inventory` and `Cultivate Alignment` methods in `methods.csv` exist precisely to close that gap.

## References

- `references/seed-schema.md` — the output artifact format; consult when writing `seed.md` in Step 5.
- `references/repo-signals.md` — what to scan in Step 1 and how to build the status board.
- `references/bmad-elicitation.md` — origins of the elicitation loop, divergences from upstream BMAD, and extension guide for `methods.csv`. Read before adding / removing / reshaping methods.
- `methods.csv` — the elicitation method registry (BMAD-format: `num, category, method_name, description, output_pattern`).
