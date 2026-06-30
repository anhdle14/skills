---
name: agents-md
description: Create or rewrite the per-folder agent context file that an agent reads on every turn. Use when the user wants to create, bootstrap, or rewrite an AGENTS.md / CLAUDE.md / agent context file, or onboard an agent to a repo.
tags: [create, engineering, productivity]
args: "<target folder (defaults to cwd)>"
---

# Create or Replace AGENTS.md

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

An AGENTS.md is read on **every** turn. Bloat down-weights every instruction in
the file, not just the tail. The job is a short, high-signal file where every
line prevents a specific mistake — not a project wiki.

**vs `/init`:** Use `/init` for a quick autonomous first draft. Use this skill
when you want the strict 80-line discipline, embedded behavioral principles, and
a deliberate rewrite of an unsalvageable file.

See [REFERENCE.md](REFERENCE.md) for the template, scan checklist, interview
script, and placement rules. See [PRINCIPLES.md](PRINCIPLES.md) for the four
behavioral principles to embed.

## Step 0 — Resolve target & classify

Resolve the target folder (default cwd) and find the git root. Decide the
filename: default to `AGENTS.md` (the cross-agent standard); for Claude `CLAUDE.md`
interop see [REFERENCE.md](REFERENCE.md). Check for
monorepo workspaces (package.json `workspaces`, `deno.json`/`go.work`/Cargo
workspaces, nx/turbo); if found, decide root-only vs. root + per-package, and
remember nested files **inherit** the parent — they state only deltas.

Then classify the existing file:

- **None** → create fresh.
- **Partially good** (>~50% of lines still prevent real mistakes) → harvest the
  good lines, then trim/rewrite around them.
- **Unsalvageable** (bloated, stale, contradictory) → read it, harvest still-true
  gotchas/gates, then replace.

## Step 1 — Fan out the repo scan

Gather facts an agent can derive, so you never ask the user for them — run the
[REFERENCE.md scan checklist](REFERENCE.md) in parallel and merge. On large
repos, bound scope to top-level + manifests + CI; skip vendored/generated trees.
Linter/formatter rules belong in the tool config, **never** in AGENTS.md.

## Step 2 — Interview for what only the user knows

Pre-fill answers from the scan (README → purpose, CI → testing), then ask the
user only to confirm or correct, plus the gaps the scan can't reveal. See the
[REFERENCE.md interview script](REFERENCE.md). Batch the questions.

**No user available (AFK/headless):** derive what you can from scan + existing
docs, mark genuine unknowns as `TODO(human): …` lines instead of inventing, and
skip the Step 5 confirm gate.

## Step 3 — Draft against the template

Write using the REFERENCE.md template and embed PRINCIPLES.md behaviors where
they fit. Rules are **imperative + positive alternative**: "Never force-push
shared branches; rebase locally then push normally." Reference other docs with
plain `see path/to/doc.md` — never `@imports`, which load eagerly and burn
context (reserve `@` only for AGENTS.md/CLAUDE.md interop).

## Step 4 — Loop until under budget

Exit condition, set before you start: **≤80 lines (hard cap 120), every line
prevents a specific mistake.** Run `deno run --allow-read scripts/budget-check.ts
<file>` for an objective count. If over, cut in this order: linter-enforceable
rules, restated framework defaults, speculative scaffolding, cached external
docs (link instead). If still over budget after those cuts, move the overflow to
a linked `.claude/rules/*.md` or aux doc — 120 is the hard stop.

## Step 5 — Confirm and write

Show the draft and line count. Write to the resolved path only after the user
confirms. If replacing, note what you dropped from the old file.
