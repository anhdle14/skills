---
name: ship
disable-model-invocation: true
description: Single self-orienting entry point for the four-phase ship pipeline — detects where a feature left off from its .ship/ artifacts and resumes it, or walks you from the start through grill, slice, build, review.
tags: [plan, engineering, productivity]
args: "<feature description or .ship/<feature-slug> path (optional)>"
---

# Ship

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Take a feature from a rough plan to shipped, reviewed vertical slices. The work splits into
four phases. Run `/skill:ship` and it orients itself: it reads the durable `.ship/` artifacts,
resumes an in-flight feature from wherever it stopped, or walks you from the start. This skill
is the index, the router, and the handoff contract between phases. Shared contracts live in
[REFERENCE.md](REFERENCE.md); the pattern catalog the phases compose is in
[PATTERNS.md](PATTERNS.md); a worked trace is in [EXAMPLES.md](EXAMPLES.md).

Everything the workflow produces lives under a gitignored `.ship/<feature-slug>/` folder —
the durable channel that carries state between phases and subagents. Only the feature code
is committed. The `.ship/` layout and all file schemas are in REFERENCE.

## The four phases

1. **Plan (any doc).** Start from any plan, spec, design, or manifest doc. Save it as
   `.ship/<feature-slug>/PLAN.md`. No skill required — bring whatever you already have.
2. **`/skill:ship-grill`.** A relentless interview that makes the plan match your real
   intent and resolves every grey area, then writes `SPEC.md` — the complete handoff
   contract the rest of the workflow runs on.
3. **`/skill:ship-slice`.** Autonomous. Slices the spec into vertical tracer bullets, runs
   them in non-blocking phases, fans out subagents, drives each slice to green, and commits
   outcomes. Hands-off — pauses only on a hard blocker.
4. **`/skill:ship-review`.** A deep review of the deliverables — goal-backward verification
   against the spec plus an adversarial quality pass — written to `REVIEW.md`.

## When to use ship

Use the full pipeline when a feature is large enough to need a written contract and to fan
out across parallel slices, and you want to hand the build off and walk away. For a one- or
two-step change that one pass handles with room to spare, skip it and just make the change.

Each phase is also usable on its own: grill to harden any plan, slice to execute any
existing spec, review to audit any finished work.

## Running the pipeline

`/skill:ship [feature-slug | description]` orients itself, then routes. It never launches a
phase itself — it detects state, prints a status card, and hands you the exact next command.

1. **Locate the feature.** If an arg names a slug or description, use it. Otherwise scan
   `.ship/`: exactly one in-flight `<slug>/` → resume it; several → list each with its
   detected phase and ask which; none → start Phase 1.
2. **Detect the phase** from artifact presence and `STATE.md` markers, per the
   resume-detection contract and routing table in [REFERENCE.md](REFERENCE.md) (`PLAN.md` →
   `SPEC.md` → `SLICES.md`+`STATE.md`/`Overall: DONE` → `REVIEW.md`).
3. **Present, then route.** Print a status card and the recommended `▶ Next Up` command, then
   wait — never auto-launch:

   ```text
   ╔═ SHIP STATUS ═════════════════╗
    Feature: csv-export
    Phase 2 of 4 — SPEC.md written
    Blockers: none
   ╚═══════════════════════════════╝

   ▶ Next Up
   /skill:ship-slice csv-export
   (/new first → fresh context window)

   Proceed?  y  ·  edit PLAN/SPEC  ·  different feature
   ```

4. **Phase 1 fallback (nothing exists).** Confirm or create `.ship/<feature-slug>/PLAN.md`
   from whatever plan/spec/design doc you have, then hand off to `/skill:ship-grill`.

- As the index, create only `PLAN.md` and a short handoff note; never pre-create `SPEC.md`,
  `SLICES.md`, `STATE.md`, or `REVIEW.md` — each downstream phase writes its own.
- Do not skip grilling before slicing: the autonomous phase only runs hands-off because the
  spec already answers its questions. A thin spec means a blocked or wrong build.
- Between phases, the human decides whether to proceed. Within `ship-slice`, the agent runs
  autonomously and stops only on a hard blocker (see REFERENCE).

## Anti-patterns

- **Slicing a thin spec** — if `ship-grill` left grey areas, the build guesses or stalls.
- **Horizontal slices** — slices must cut end to end, not deliver one layer at a time.
- **Self-verification** — the slice verifier and the review adversary must be independent of
  the producer (Tier A) or read only the on-disk artifact (Tier B).
- **Committing `.ship/`** — it is gitignored; commit only the feature code.
- **Looping a stuck slice** — a retry that repeats the same diagnosis is a hard blocker, not
  progress; escalate.
