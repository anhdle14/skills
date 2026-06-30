---
name: ship
disable-model-invocation: true
description: Orchestrate a feature from a plan doc to shipped, reviewed vertical slices through four human-invoked phases — grill, slice, build, review.
tags: [plan, engineering, productivity]
args: "<feature description or .ship/<feature-slug> path (optional)>"
---

# Ship

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Take a feature from a rough plan to shipped, reviewed vertical slices. The work splits into
four phases, each invoked explicitly by a human. This skill is the index and the handoff
contract between them. Shared contracts live in [REFERENCE.md](REFERENCE.md); the pattern
catalog the phases compose is in [PATTERNS.md](PATTERNS.md); a worked trace is in
[EXAMPLES.md](EXAMPLES.md).

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

- Confirm or create `.ship/<feature-slug>/PLAN.md`, then invoke the phases in order. Each
  phase reads the previous phase's artifacts from `.ship/` and writes its own there.
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
