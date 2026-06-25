---
name: trinity
disable-model-invocation: true
description: Thinker-Worker-Verifier role loop that iterates accept-or-revise across turns until a result is verified or a turn budget is hit.
tags: [engineering, analyze, productivity]
args: "<task to solve via the role loop (optional)>"
---

# Trinity

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Solve one task by cycling a chosen worker through three roles across turns — a Thinker that strategizes, a Worker that executes, and a Verifier that judges. Each turn appends to a shared transcript; the loop halts when the Verifier accepts or a turn budget is hit. Role contracts, routing, and worker tiers live in [REFERENCE.md](REFERENCE.md); a worked trace is in [EXAMPLES.md](EXAMPLES.md).

## When to use

Use the tri-role loop when correctness must be earned, not assumed:

- The result must be checked and refined before you can trust it.
- A single attempt keeps failing review and you need a structured revise cycle.
- The task is one coherent problem, not a multi-part one.

Do NOT use it when a single pass is obviously correct and cheap to confirm. For a task that splits into independent parts routed across workers, step up to `/orchestrate`. To pick an abstract pattern in the first place, see the catalog in `/orchestrate` (PATTERNS.md) — this loop is its Loop Until Done plus Adversarial Verification, made concrete; cross-reference, do not re-explain.

## The roles

- **Thinker** — analyzes the state and returns strategy, decomposition, or critique. Never emits the final answer.
- **Worker** — executes one concrete step (code, math, derivation) and returns the artifact.
- **Verifier** — judges the latest artifact against the acceptance criteria and returns exactly `ACCEPT` or `REVISE: <diagnosis>`.

## The loop

1. **Think.** A Thinker turn decomposes the task and states the acceptance criteria. Write them to a transcript file.
2. **Route.** Pick the best available worker for the next turn's role and task character (REFERENCE). Choose the highest worker tier actually available (REFERENCE).
3. **Work.** A Worker turn produces the artifact. Append it to the transcript.
4. **Verify.** A *different* worker, acting as Verifier, sees the artifact and the criteria but NOT the Worker's private reasoning, and returns `ACCEPT` or `REVISE: <specific defect and fix direction>`.
5. **Iterate.** On `REVISE`, feed the diagnosis back to a Thinker or Worker turn and repeat. On `ACCEPT`, stop.
6. **Stop** on accept or when the turn budget is hit; re-read the transcript before the done check.

## Budgets and stopping

Default turn budget is five. Stop on Verifier `ACCEPT`, on budget exhaustion, or when two consecutive `REVISE` turns carry the same diagnosis (no progress) — then escalate rather than loop. On any non-accept stop, return the best-verified partial plus the outstanding diagnosis.

## Output

Return the final solution, the turn-by-turn role trace (which worker held which role, each verdict), the final verdict, and turns consumed. Persist the transcript to a file so it survives context loss.

## Anti-patterns

- **Rubber-stamp Verifier** — an `ACCEPT` with no scrutiny; require a specific diagnosis on every `REVISE`.
- **Leaky Verifier** — letting the Verifier see the Worker's reasoning, so it agrees too easily; give it only the artifact and criteria.
- **Thinker leakage** — a Thinker that emits the final answer instead of strategy.
- **Budget-free looping** — iterating with no turn cap and no no-progress check.
- **Self-verification** — the producer checking its own work when a different worker is available.
