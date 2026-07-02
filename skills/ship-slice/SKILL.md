---
name: ship-slice
disable-model-invocation: true
description: Autonomously turn a spec into shipped vertical slices — decompose into tracer bullets, run them in non-blocking phases, fan out subagents, drive each to green, and commit outcomes.
tags: [plan, engineering, productivity]
args: "<.ship/<feature-slug> path (optional)>"
---

# Ship · Slice

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Phase 3 of the ship workflow, and the autonomous one. Read `.ship/<feature-slug>/SPEC.md` and
build the feature as vertical slices, hands-off, pausing only on a hard blocker. The `.ship/`
layout, subagent tiers, vertical-slice rules, the verify loop, gates, the hard-blocker
protocol, and the commit policy all live in [../ship/REFERENCE.md](../ship/REFERENCE.md); the
patterns this phase composes (Fan Out and Synthesize + Loop Until Done) are in
[../ship/PATTERNS.md](../ship/PATTERNS.md).

## The loop

1. **Decompose.** Read the spec. Break it into vertical tracer-bullet slices (each cuts end
   to end and is demoable on its own; prefactoring is its own first slice). Build the
   dependency graph and group independent slices into non-blocking phases. Write all of this
   to `.ship/<feature-slug>/SLICES.md` and seed `STATE.md` before running anything. First apply
   PATTERNS' "when a single pass is enough" test: a one-operation spec is a single slice — do
   not manufacture phases or fan-out it does not need (a single slice still runs the verify loop).
2. **Fan out the phase.** For each phase, dispatch the independent slices in parallel — one
   subagent per slice (Tier A), or role-played in sequence writing each output to disk
   (Tier B). As many subagents as the phase has independent slices.
3. **Build each slice (Worker).** Implement the slice; do TDD at the spec's seams where a
   test framework exists; run the auto-detected gates to green; write `slices/<NN>-<slug>/
   SUMMARY.md`; commit the code (outcomes, not process).
4. **Verify each slice (Verifier).** A *different* subagent checks the artifact against the
   spec — goal achieved, not just tasks done — seeing the artifact and spec but not the
   worker's reasoning. Returns `ACCEPT` or `REVISE: <defect + fix>`. On `REVISE`, feed the
   diagnosis back and retry (prefer a different worker), up to the retry cap.
5. **Advance.** When a phase's slices all `ACCEPT`, re-read `SLICES.md` and `STATE.md` (to
   catch slices inserted mid-run) and start the next phase. Run the full test suite once at
   phase end.
6. **Finish.** When every slice is accepted, write final progress to `STATE.md` — including
   a `## Status` block whose last line is exactly `Overall: DONE` and an `## Open blockers`
   section reading `(none)` — then report. That `Overall: DONE` marker is the deterministic
   signal `/skill:ship` reads to route the run on to `ship-review` (see the resume-detection
   contract in [../ship/REFERENCE.md](../ship/REFERENCE.md)).

## Staying hands-off

This phase does not check in between slices. Keep going; for a defaultable grey area, choose
the spec-consistent default, log the assumption to `STATE.md`, and continue — `ship-review`
will surface it.

Pause and report ONLY on a hard blocker — a slice stuck after the retry cap (default 3), a
decision the spec does not answer, or no progress (a retry repeating its diagnosis). The full
protocol and budgets are in [../ship/REFERENCE.md](../ship/REFERENCE.md). On a pause, write the
blocker to `STATE.md` with enough context to resume cold, then stop.

## Anti-patterns

- **Horizontal slices** — a slice must cut every layer, not deliver one layer at a time.
- **Parallelizing dependent slices** — only disjoint slices fan out; sequence the rest.
- **Self-verification** — the verifier must be independent of the worker (Tier A) or read
  only the on-disk artifact (Tier B).
- **Pausing on defaultable grey areas** — default, log to `STATE.md`, keep going.
- **Committing `.ship/`** — gitignored; commit only the feature code, after gates pass.
