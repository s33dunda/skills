# Repo Signals

Before asking the user anything, scan the working directory for already-present signal. Every field extracted here is one less question to ask.

The scan is silent — no output to the user — and produces a draft seed.md in memory that the elicitation loop (see `SKILL.md` Step 2) then refines.

## What To Scan

Run the scan in order. First hit wins; don't overwrite richer signal with weaker signal.

### 1. Git Remote → `name`

```bash
git config --get remote.origin.url
```

Extract the repo slug (`.../owner/repo.git` → `repo`). Use it as the provisional `name`. Skip if not a git repo or no remote configured.

### 2. Manifests → `stack`

Read whichever exist, in order of specificity:

| File | Fields extracted |
|------|------------------|
| `pyproject.toml` | `[project].name`, `[project].description`, Python version, declared deps |
| `package.json` | `name`, `description`, Node engine, `dependencies` keys |
| `Cargo.toml` | `[package].name`, `[package].description`, edition, declared deps |
| `go.mod` | module path, Go version |
| `composer.json` | `name`, `description`, PHP version, `require` keys |
| `Gemfile` + `*.gemspec` | gem name, summary, Ruby version, runtime deps |
| `deno.json` / `bun.lockb` | runtime signal |
| `.tool-versions` / `.nvmrc` / `.python-version` | runtime signal |

For `stack`: take top-level language + 1–2 high-signal frameworks from the dependency list (e.g. "python, fastmcp, httpx"), not a full lockfile dump.

For `description`: if present, use it as a provisional `tagline` — but mark as `(from manifest)` in the status board so the user can overwrite.

### 3. `README.md` → `tagline`, `problem`

Read the top of `README.md`:
- **H1** → fallback provisional `tagline` (if manifest `description` is empty)
- **First paragraph after H1** → provisional `problem` statement
- **Badges / "Why?" section** → may contain `audience` or `problem` signal

Keep extractions short. Prefer user's original prose over paraphrase.

### 4. Existing Plot Artifacts → merge, don't overwrite

If any of these exist, treat them as prior state to merge into the draft:

| File | Action |
|------|--------|
| `seed.md` | Parse frontmatter + sections. Use as the baseline draft. Only elicit on fields marked `TBD` or missing. |
| `plot.md` | Legacy name for seed.md (pre-0.2). Same handling. |
| `AGENTS.md` | Read the `## Orientation` or equivalent section → populates `agents` field signal. |
| `.github/workflows/*` | Presence of CI → signal that cultivate has already run. Note it, don't re-plot. |

If `seed.md` already exists and is complete, **don't overwrite** — surface this to the user and ask whether they want to refine specific sections or start fresh.

### 5. Top-Level Tree → structural hints

```bash
ls -la
```

Quick checks (don't dump the whole tree in the status board, just note the hints):

- `src/` + `tests/` → standard app layout
- `packages/` or workspace root → monorepo; ask whether plot covers the whole repo or one package
- `.github/` + `CI` → existing harness (connects to cultivate)
- `docs/` → existing docs surface (cultivate may already have run)
- No files at all → pure pre-repo plotting; no signal expected

## Fallbacks

If the working directory contains none of the above (e.g. plot is being called in a fresh conversation with no filesystem context or from a note-only directory), skip this phase entirely and start the elicitation loop with an empty draft.

Do not speculate. An empty draft with explicit `?` markers is better than one invented from thin air.

## Merge Rules

When combining repo signal with conversation-history signal and user elicitation:

1. **User-stated wins.** If the user already described the project in the thread, that text overrides manifest `description`.
2. **Manifest wins over README.** Manifest `description` fields are curated; README paragraphs are often aspirational marketing.
3. **Existing `seed.md` wins over inferred signal.** If the user already produced a seed, that's the baseline.
4. **Anything ambiguous becomes a `?` on the status board.** Don't guess — elicit.

## Status Board Format

After scanning, present a compact status board before showing the elicitation menu. Example:

```
Here's what I've gathered:
  name:     ynab-mcp              (from git remote)
  stack:    python, fastmcp       (from pyproject.toml)
  tagline:  MCP server for YNAB   (from README.md, draft)
  problem:  ?
  audience: ?
  scope:    ?
  agents:   ?
  success:  ?
```

Use `(from <source>)` annotations so the user knows what's inferred vs. what's confirmed. They can correct anything at any point via direct feedback (see `SKILL.md` Step 4).
