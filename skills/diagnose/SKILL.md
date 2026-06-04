---
name: diagnose
description: Runs a disciplined reproduce, minimise, hypothesise, instrument, fix, and regression-test loop for hard bugs and performance regressions. Use when user says "diagnose this" / "debug this", reports a bug, says something is broken/throwing/failing, or describes a performance regression.
tags: [analyze, engineering]
---

# Diagnose

A discipline for hard bugs. Skip phases only when explicitly justified.

When exploring the codebase, use the project's domain glossary to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a fast, deterministic, agent-runnable pass/fail signal for the bug, you will find the cause. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. Be aggressive. Be creative. Refuse to give up.

### Ways to construct one — try in order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer).
5. **Replay a captured trace** — save a real network request / payload / event log to disk; replay it in isolation.
6. **Throwaway harness** — minimal subset of the system with a single function call.
7. **Property / fuzz loop** — run 1000 random inputs and look for the failure mode.
8. **Bisection harness** — `git bisect run` across commits.
9. **Differential loop** — run same input through old vs new version and diff outputs.
10. **HITL bash script** — last resort; use `scripts/hitl-loop.template.sh` so the loop is still structured.

### Iterate on the loop itself

- Can I make it faster? (Cache setup, skip unrelated init, narrow scope.)
- Can I make the signal sharper? (Assert on the specific symptom.)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem.)

### Non-deterministic bugs

Goal is a **higher reproduction rate**, not a clean repro. Loop 100×, parallelise, add stress. A 50%-flake is debuggable; 1% is not.

### When you genuinely cannot build a loop

Stop and say so. List what you tried. Ask for: (a) access to the reproducing environment, (b) a captured artifact, or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

## Phase 2 — Reproduce

Run the loop. Confirm:

- [ ] The loop produces the failure the **user** described — not a different failure nearby.
- [ ] The failure is reproducible (or at a high enough rate).
- [ ] You have captured the exact symptom.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any. Each must be falsifiable:

> "If X is the cause, then changing Y will make the bug disappear / changing Z will make it worse."

Show the ranked list to the user before testing. They often have domain knowledge that re-ranks instantly.

## Phase 4 — Instrument

Each probe maps to a specific prediction from Phase 3. Change one variable at a time.

Tool preference:

1. Debugger / REPL inspection.
2. Targeted logs at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup = single grep.

**Perf bugs:** establish a baseline measurement first (timing harness, profiler, query plan), then bisect.

## Phase 5 — Fix + regression test

Write the regression test **before the fix** — but only at a **correct seam** (one that exercises the real bug pattern as it occurs at the call site).

If no correct seam exists, note it — the architecture is preventing the bug from being locked down.

If a correct seam exists:

1. Turn the minimised repro into a failing test.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 loop.

## Phase 6 — Cleanup + post-mortem

- [ ] Original repro no longer reproduces
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed
- [ ] Throwaway prototypes deleted
- [ ] Correct hypothesis stated in the commit message

Ask: what would have prevented this bug? If architectural change is needed, hand off to `/code-structure`.
