---
name: ship-review
disable-model-invocation: true
description: The review gate for shipped deliverables — verify goal-backward against the spec, attack the code adversarially, then classify every finding by severity and action, apply the safe fixes, and escalate the judgment calls.
tags: [analyze, engineering, productivity]
args: "<.ship/<feature-slug> path (optional)>"
---

# Ship · Review

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Phase 4 of the ship workflow, and the gate the work passes through before it is trusted.
The review is opinionated so that "passed the gate" means the same thing every time: the
spec's promised behavior exists and runs, tests and evidence back the intent, and no
correctness, reliability, or security defect survives. Nothing is done until the gate is
green. Read `.ship/<feature-slug>/SPEC.md`, `SLICES.md`, and `STATE.md` first. Shared
contracts are in [../ship/REFERENCE.md](../ship/REFERENCE.md); the Adversarial Verification
pattern is in [../ship/PATTERNS.md](../ship/PATTERNS.md).

## Two checks, run in order

Run both against the artifact and the spec — never against the build's own reasoning.

### Check 1 — goal-backward verification (intent-anchored)

Start from what the spec PROMISED and confirm it actually exists and works:

- **Do not trust the SUMMARYs.** They record what the build *said* it did; you verify what
  the code *actually* does. These often differ.
- For each deliverable, user story, and acceptance bar in the spec, find the code that
  delivers it and confirm the behavior — read the code, trace the path, run it where you can.
- **Gather reviewer-visible evidence** for the intended behavior: run the gates, exercise the
  path, capture output. Missing evidence for a promised behavior is itself an `ask-user`
  finding, not a silent pass.
- Run the repo's full gates (the spec's verify commands: typecheck, lint, tests, build). If a
  declared gate cannot execute (missing dep, no lockfile), do not treat it as a hard blocker —
  verify the behavior directly and record the unrunnable gate as its own finding.
- Check every assumption logged in `STATE.md` — a defaulted grey area may be wrong.

### Check 2 — adversarial quality attack

Now try to BREAK the deliverable, not polish it. Given only the code and the spec, hunt for:

- Edge cases and inputs the slices did not handle; race conditions; error paths.
- Security issues — injection, unvalidated input, leaked secrets, unsafe defaults.
- Dead code, missing tests, weak seams, and tests that assert implementation not behavior.
- Architecture smells — wrong boundaries, duplication, leaks across the spec's seams.
- Standards/ADR violations recorded in the spec or glossary.

## Classify every finding: severity × action

Each finding carries two axes. Severity says how bad; **action says how it resolves** — this
is what turns a report into a gate.

**Severity** — `error` (broken/unsafe, blocks the gate) · `warning` (real defect or risk, not
blocking) · `info` (note only).

**Action** — the resolution path:

- **`auto-fix`** — objective correctness, reliability, or security issues you can fix
  mechanically without a judgment call. Stays `auto-fix` even when the smallest correct fix
  re-adds a little previously deleted logic. Drive these to green in a bounded loop (ship's
  verify loop + retry cap in REFERENCE): smallest correct fix, re-run the affected gate,
  repeat until clean or the cap is hit. Commit outcomes, not process.
- **`ask-user`** — intent-sensitive or ambiguous. Reserve it for: challenging an intentional
  product or design choice, arguing an intentional addition/removal/guard should be undone,
  or reporting that evidence for a promised behavior is missing. Never fix these — stop and
  escalate with the finding, the intent it touches, and a fix direction (hard-blocker
  protocol); do not decide it for the user.
- **`no-op`** — informational; record and move on.

A finding that survives the retry cap is a hard blocker — escalate rather than loop.

## Report

Write `.ship/<feature-slug>/REVIEW.md` with findings ordered by severity, each tagged with
its action and enough detail to act on:

- 🔴 **error** — spec not met, broken behavior, or a security issue (blocks the gate).
- 🟡 **warning** — a real defect or risk that is not blocking.
- 🟢 **info** — an optional enhancement or simplification.

For each finding: where it is, why it matters, its action (`auto-fix` applied / `ask-user`
escalated / `no-op`), and the fix direction. Record which `auto-fix` findings you resolved
and how you verified them. End with the gate verdict — **green** only when no `error` remains
and every `ask-user` finding is resolved — and report back to the user. If the gate is not
green, recommend returning to `/skill:ship-slice` to close the blockers.

## Anti-patterns

- **Trusting SUMMARYs** — verify the code, not the claims about it.
- **Polishing instead of attacking** — Check 2's job is to invalidate, not to suggest style.
- **Reading the build's reasoning before judging** — judge the artifact against the spec.
- **Severity without action** — every finding must say how it resolves, not just how bad it is.
- **Auto-fixing a judgment call** — anything that touches author intent is `ask-user`; never
  silently undo an intentional choice.
- **Looping past the cap** — a fix that repeats the same failure is a hard blocker; escalate.
