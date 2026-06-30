---
name: ship-review
disable-model-invocation: true
description: Deeply review shipped deliverables — verify goal-backward against the spec, attack the code adversarially for issues, and report prioritized findings and improvements.
tags: [analyze, engineering, productivity]
args: "<.ship/<feature-slug> path (optional)>"
---

# Ship · Review

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Phase 4 of the ship workflow. Scan the deliverables for issues and improvements, then report
back. Two complementary passes: goal-backward verification against the spec, and an
adversarial quality attack. Read `.ship/<feature-slug>/SPEC.md`, `SLICES.md`, and `STATE.md`
first. Shared contracts are in [../ship/REFERENCE.md](../ship/REFERENCE.md); the Adversarial
Verification pattern is in [../ship/PATTERNS.md](../ship/PATTERNS.md).

## Pass 1 — goal-backward verification

Start from what the spec PROMISED and confirm it actually exists and works:

- **Do not trust the SUMMARYs.** They record what the build *said* it did; you verify what
  the code *actually* does. These often differ.
- For each deliverable, user story, and acceptance bar in the spec, find the code that
  delivers it and confirm the behavior — read the code, trace the path, run it where you can.
- Run the repo's full gates (the spec's verify commands: typecheck, lint, tests, build). If a
  declared gate cannot execute (missing dep, no lockfile), do not treat it as a hard blocker —
  verify the behavior directly (run the function under the runtime) and record the unrunnable
  gate as its own finding.
- Check every assumption logged in `STATE.md` — a defaulted grey area may be wrong.
- Note any promised deliverable that is missing, partial, or diverges from the spec.

## Pass 2 — adversarial quality attack

Now try to BREAK the deliverable, not polish it. Given only the code and the spec (not the
build's reasoning), hunt for:

- Edge cases and inputs the slices did not handle; race conditions; error paths.
- Security issues — injection, unvalidated input, leaked secrets, unsafe defaults.
- Dead code, missing tests, weak seams, and tests that assert implementation not behavior.
- Architecture smells — wrong boundaries, duplication, leaks across the spec's seams.
- Standards/ADR violations recorded in the spec or glossary.

## Report

Write `.ship/<feature-slug>/REVIEW.md` with findings ordered by severity, each with enough
detail to act on:

- 🔴 **Blocker** — spec not met, broken behavior, or a security issue.
- 🟡 **Should fix** — a real defect or risk that is not a blocker.
- 🟢 **Improvement** — an optional enhancement or simplification.

For each finding: where it is, why it matters, and the fix direction. End with a one-line
verdict — does the feature meet the spec, yes or no — and report back to the user. If
blockers remain, recommend returning to `/skill:ship-slice` to close them.

## Anti-patterns

- **Trusting SUMMARYs** — verify the code, not the claims about it.
- **Polishing instead of attacking** — Pass 2's job is to invalidate, not to suggest style.
- **Reading the build's reasoning before judging** — judge the artifact against the spec.
- **Unprioritized findings** — every item carries a severity and a fix direction.
