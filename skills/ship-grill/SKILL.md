---
name: ship-grill
disable-model-invocation: true
description: Relentlessly interview a plan doc into a complete spec — resolve every grey area, build the glossary and ADRs, and write the handoff contract the autonomous build runs on.
tags: [plan, engineering, productivity]
args: "<.ship/<feature-slug> path or feature description (optional)>"
---

# Ship · Grill

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Phase 2 of the ship workflow. Take the plan at `.ship/<feature-slug>/PLAN.md` and interrogate
it until it is a complete handoff contract: a `SPEC.md` the autonomous build phase can run on
without coming back to ask you anything. Shared contracts and the SPEC schema are in
[../ship/REFERENCE.md](../ship/REFERENCE.md). This phase precedes slicing — do not write code.

## The interview

Interview relentlessly about every aspect of the plan until you reach a shared understanding.
Walk each branch of the design tree, resolving dependencies between decisions one by one.

- **One question at a time.** Asking several at once is bewildering. Wait for the answer
  before the next question.
- **Lead with a recommended answer** for each question, with brief reasoning, plus an
  alternative or two.
- **Explore the codebase instead of asking** whenever the code can answer the question.
- **Drive toward zero grey areas.** Every choice the build might otherwise guess must have a
  decided answer captured in the spec. This is what lets the next phase run hands-off. When a
  grey area is second-order and the user has not weighed in, pick the spec-consistent default,
  record it in the grey-area-defaults table flagged for `ship-review`, and continue — do not block.

## Build the domain model as you go

Sharpen the language while you interview, writing it down the moment it crystallises:

- **Challenge fuzzy or overloaded terms** — propose one precise canonical name. Write
  resolved terms to `.ship/<feature-slug>/GLOSSARY.md` (create it lazily).
- **Record decisions as ADRs** under `.ship/<feature-slug>/decisions/NNNN-title.md` when a
  choice has lasting consequences (create the folder lazily).
- **Stress-test with concrete scenarios** — invent edge cases that force precise boundaries.
- **Cross-check against code** — if the user's claim contradicts the code, surface it.

## Capture what the build needs

Beyond decisions, the spec must carry the operational facts the autonomous phase depends on:

- The repo's exact **verify commands** (typecheck, lint, test, build).
- The **standards** and ADRs the code must respect.
- The **seams** where the feature is tested — prefer the fewest, highest seams.

## Write and self-review the spec

Write `.ship/<feature-slug>/SPEC.md` using the SPEC schema in REFERENCE (goal, scope &
boundaries, deliverables, user stories, seams, verify commands, standards, grey-area
defaults). Then self-review it before handing back:

- **Placeholder scan** — remove TODO, TBD, and vague requirements.
- **Consistency** — goal, scope, deliverables, and stories must agree.
- **Scope** — small enough to slice and ship as one feature; cut anything that does not serve
  the goal.
- **Ambiguity** — where a requirement could split two ways, pick one explicitly.

Then ask the user to review `SPEC.md`. If they request changes, update and repeat the
self-review. Proceed to `/skill:ship-slice` only once the spec answers everything the build
will need.

## Anti-patterns

- **Stacking questions** — one at a time, always with a recommendation.
- **Asking what the code already answers** — explore first.
- **Leaving grey areas** — an unanswered choice becomes a blocked or wrong build.
- **A spec full of placeholders** — self-review until none remain.
