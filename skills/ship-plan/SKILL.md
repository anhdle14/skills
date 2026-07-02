---
name: ship-plan
disable-model-invocation: true
description: Phase 1 of the ship pipeline — pair with the user to author a reviewed PLAN.md, using plannotator's visual review gate when available and degrading gracefully when it is not, then hand off to ship-grill.
tags: [plan, engineering, productivity]
args: "<feature description or .ship/<feature-slug> path (optional)>"
---

# Ship · Plan

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Phase 1 of the ship workflow. Pair with the user to turn a rough idea into a reviewed
`.ship/<feature-slug>/PLAN.md` — the artifact `/skill:ship-grill` interrogates into `SPEC.md`.
This phase authors and reviews the *plan*; it does not write code and does not write the spec.
Shared contracts (the `.ship/` layout, resume-detection, Tier A/B substrate) live in
[../ship/REFERENCE.md](../ship/REFERENCE.md); the review-gate tier contract and how to activate
the plannotator config are in [REFERENCE.md](REFERENCE.md).

This skill *forks plannotator by forcing it via prompts*: when plannotator is present it drives
plannotator's browser review UI; when it is not, it falls back to a plain in-chat review. It
ships no executable — only the prose loop below and a config template
(`plannotator.json`) you activate once (see REFERENCE).

## The plan loop

Save the plan to `.ship/<feature-slug>/PLAN.md` (`<feature-slug>` is short kebab-case, e.g.
`csv-export`). `.ship/` is gitignored. Reuse the same path across revisions so plan-diff can
track changes. Then repeat until the plan is complete:

1. **Explore.** Read, grep, find, ls to build context. Actively hunt for existing functions and
   patterns to reuse — never propose new code where a suitable implementation already exists.
2. **Update `PLAN.md`.** Capture each discovery immediately; do not wait until the end.
3. **Ask the user.** Only about what the code cannot answer — requirements, preferences,
   tradeoffs, edge-case priority. Batch related questions. Then return to step 1.

Start by scanning key files to size the task, write a skeleton `PLAN.md`, and ask your first
questions — do not explore exhaustively before engaging the user.

### PLAN.md structure

- **Context** — the problem, what prompted it, the intended outcome.
- **Approach** — your recommended approach only.
- **Files to modify** — the critical paths that will change.
- **Reuse** — existing functions/utilities you found, with file paths.
- **Steps** — an implementation checklist of `- [ ]` items.
- **Verification** — how to test the change end to end.

Keep it scannable but detailed enough for `ship-grill` to interrogate.

## The review gate (auto-detect, prefer the highest tier)

Never ask the user which tier to use — probe, then use the best available. Announce with a
one-line notice ONLY when you drop below Tier 1. Full contract in REFERENCE.

1. **Tier 1 — native.** If the `plannotator_submit_plan` tool is available, call it with the
   `PLAN.md` path. The browser review opens; approve proceeds, deny returns annotations, and
   resubmission shows a plan diff. Revise with targeted edits (never a full rewrite) and
   resubmit the same path.
2. **Tier 2 — CLI.** Else if `plannotator` is on `PATH`, run
   `plannotator annotate .ship/<feature-slug>/PLAN.md --gate --json` and read the structured
   decision from stdout. Print: `plannotator extension not active — using the annotate CLI gate`.
3. **Tier 3 — in-chat.** Else write `PLAN.md`, ask the user to review it in chat, and iterate to
   an explicit approval. Print: `plannotator not detected — using in-chat review gate`.

At Tier 1/2 you may pull a reference doc, URL, or HTML artifact into the annotate UI while
planning (`plannotator annotate <path|url> [--markdown]`; HTML renders raw by default, `--markdown`
converts it). Not available at Tier 3.

## Hand off to grill

Once the plan is approved, do **not** implement it and do **not** write `SPEC.md`. Print the
reviewed `PLAN.md` path and recommend the next command:

```text
▶ Next Up
/skill:ship-grill <feature-slug>
(/new first → fresh context window)
```

`ship-grill` interrogates the plan into the complete `SPEC.md` handoff contract.

## Anti-patterns

- **Writing code or the spec here** — Phase 1 produces only a reviewed `PLAN.md`.
- **Asking what the code answers** — explore first; save questions for user-only decisions.
- **Rewriting the whole plan on feedback** — make targeted edits so plan-diff stays meaningful.
- **Forcing a tier** — auto-detect; degrade gracefully instead of failing when plannotator is absent.
- **Committing `.ship/`** — it is gitignored; only feature code is ever committed.
