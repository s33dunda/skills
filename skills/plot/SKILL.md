---
name: plot
description: Plot a project -- capture the minimum viable idea so it can be grown into a real repo. Use this skill whenever the user wants to kick off a new project, describe an idea, flesh out a concept, or produce a structured brief that downstream skills (seed, cultivate) can act on. Trigger on phrases like "I want to build", "new project idea", "let's start a project", "make a plan for", "I have an idea", or any time the user is at the ideation stage before a repo exists. Plot reads whatever context already exists in the conversation -- don't re-ask things already established -- then asks targeted questions to fill the gaps. Output is a plot.md file: a structured, agent-legible brief.
---

# Plot

Plot is the first step in the agricultural workflow:

**plot → seed → cultivate → farmers**

Its job is to capture the minimum viable idea -- enough signal that a repo can be created, seeded, and cultivated for AI agent execution. Think of it as turning a raw idea into a brief that removes ambiguity for every downstream step.

## How To Run A Plot

### Step 1 -- Read The Thread First

Before asking anything, scan the current conversation for already-established context. Extract anything that answers the fields in the plot schema (see `references/plot-schema.md`). The user may have already explained the project at length. Don't waste their time repeating questions.

Build a mental draft of the plot.md from what's already known.

### Step 2 -- Identify The Gaps

Compare what you extracted against the required fields. Only ask about what's genuinely missing or ambiguous. A good plot session should feel like a focused conversation, not a form.

Required fields (must be present in final output):
- `name` -- kebab-case project identifier
- `tagline` -- one sentence: what it does and for whom
- `problem` -- the core problem or friction being removed
- `stack` -- primary language(s), frameworks, runtime -- even rough preferences count

Strongly recommended (ask if not obvious from context):
- `audience` -- who uses this? (can be "just me"  that's fine)
- `agents` -- what will AI agents actually *do* in this repo? (write code? run evals? manage releases?) This shapes what cultivate will encode.
- `scope` -- MVP boundary: what's in, what's explicitly out
- `success` -- how does a working v1 look? what can you run or observe?

Optional enrichment (include if the user volunteers it, don't fish for it):
- `constraints` -- timeline, team size, hard dependencies, existing systems
- `prospect` -- Market or competitive context
- `survey` -- Prior technical research or existing code references

### Step 3 -- Ask Questions In One Pass

Ask all your gap-filling questions at once rather than one at a time. Group related questions naturally. Keep it conversational -- this is a planning chat, not an intake form.

If the idea is very rough, lead with open questions. If the idea is well-formed but missing a few specifics, go narrow and targeted.

### Step 4 -- Produce plot.md

Once you have enough to fill the required fields, write `plot.md` to the working directory. Follow the schema in `references/plot-schema.md`. The file should be readable by both humans and agents.

A good plot.md is:
- Specific enough that a developer (human or agent) can start making real decisions
- Honest about what's unknown or TBD
- Free of marketing fluff -- just clear signal
- Written in a way that cultivate can use directly to draft AGENTS.md

### Step 5 -- Summarize And Hand Off

After producing the file, give the user a brief summary of what was captured and call out any fields marked TBD that might need resolution before the seed step. Suggest next steps (run seed to create the repo, or run cultivate if a repo already exists).

## Optional Enrichment Phases

If the user explicitly asks for research before plotting, or if the idea clearly needs it, two enrichment phases can precede the final plot:

**prospect** -- Market and competitive landscape. Who else is doing this? What do users of similar tools complain about? What would make this 10x better?

**survey** -- Technical landscape. What libraries, frameworks, or existing repos are relevant? What prior art exists in the user's own codebase?

Both are optional. Plot is valid without them. If the user mentions either, do that research before writing plot.md and fold the findings into the relevant sections.

## Cultivate Alignment

The `agents` field is the most important one for cultivate downstream. Cultivate's job is to make the repo legible and enforceable for AI agents -- but what that means depends entirely on what those agents will do.

Examples:
- "agents will write features and open PRs" → cultivate needs AGENTS.md, PR templates, and CI feedback loops
- "agents will run evals and publish results" → cultivate needs execution-plan conventions and structured output paths
- "agents will manage releases" → cultivate needs version conventions, changelog format, and release scripts

If the user hasn't thought about this, prompt them: "*What do you imagine AI agents doing in this project once the repo exists?"*

## References

Read `references/plot-schema.md` when writing plot.md -- it has the exact field definitions and a template.
