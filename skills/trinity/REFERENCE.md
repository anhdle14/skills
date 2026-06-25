# Trinity Reference

Role contracts, routing, worker-pool tiers, and stopping conditions for the tri-role loop in [SKILL.md](SKILL.md).

---

## Source synthesis

This protocol adapts the **TRINITY** paper ("TRINITY: An Evolved LLM Coordinator"). TRINITY pairs a tiny coordinator with a pool of capable LLMs and, over multiple turns, assigns one of three roles to a chosen worker each turn — Thinker, Worker, or Verifier — concatenating the full transcript so each turn sees what came before. The loop halts when the Verifier accepts the current response or a fixed turn budget is exhausted. The transferable idea — not the evolutionary training of the coordinator — is the **tri-role turn loop with an accept-or-revise gate**.

Two findings shape the rules below:

- **Verification earns the gains.** Removing the verifier role degrades hard reasoning; the accept-or-revise gate, not raw generation, is what lifts quality. Keep the Verifier honest.
- **More turns help, up to a budget.** Quality rises as the turn cap grows, then flattens — so cap the turns and stop on accept.

For the abstract patterns this loop composes, see the catalog in `/orchestrate` (PATTERNS.md). For a task that must be split across many workers rather than checked in one loop, defer to `/orchestrate`.

---

## Role contracts

Each turn binds one worker to one role with an explicit input and output contract.

### Thinker — strategizes

- **Input:** the task and the transcript so far.
- **Output:** a plan, decomposition, or critique of the partial solution — and, on the first turn, the explicit **acceptance criteria** the Verifier will use.
- **Hard rule:** never emits the final answer. If it starts solving, it has become a Worker.

### Worker — executes

- **Input:** the task, the transcript, and (if revising) the Verifier's last diagnosis.
- **Output:** one concrete artifact — code, a derivation, a numeric result.
- **Hard rule:** produces the artifact only; it does not judge its own output.

### Verifier — judges

- **Input:** the latest artifact and the acceptance criteria. **Not** the Worker's private chain of thought.
- **Output:** exactly one of:
  - `ACCEPT` — the artifact is correct, complete, and responsive to the task.
  - `REVISE: <diagnosis>` — names the **specific defect and the fix direction**, not a vibe.
- **Hard rule:** a `REVISE` with no actionable diagnosis is invalid; an `ACCEPT` without scrutiny is a rubber stamp.

---

## Routing

Pick the worker whose strengths fit the turn's role and task character.

| Turn character | Route to |
|---|---|
| Decomposition, strategy, critique | strongest reasoning worker as Thinker |
| Code, math, derivation | strongest worker for that task type as Worker |
| Judging an artifact | a *different* worker than the one that produced it, as Verifier |

Rules:

- **Rotate the Verifier away from the producer** whenever the pool allows it — independence is what catches errors a self-check misses.
- On `REVISE`, prefer a different Worker for the retry rather than the one that just failed.
- If only one worker exists, role-play each role in sequence (Tier B below); the contracts are unchanged, only dispatch differs.

---

## Worker-pool substrate tiers

The loop is identical across tiers; only how you dispatch a turn changes. Choose the **highest tier actually available** and never assume a tier you cannot confirm.

- **Tier A — real workers.** When sub-agents or per-call model selection are available, run each role as a distinct sub-agent or model. The Verifier is genuinely isolated from the Worker's reasoning.
- **Tier B — single-context role-play.** When only one model and one context are available, play each role in sequence. **Write each turn's artifact to a file** and have the Verifier read only that file plus the criteria — never the Worker's in-context reasoning. This file boundary is what prevents the Verifier from "agreeing with itself."
- **Tier C — external workers via MCP.** Only when an MCP model bridge is genuinely connected. If absent, degrade to Tier B.

Dispatch is the runtime's job, not a bundled script — this skill ships no script because every decision (which role, which worker, accept or revise) is a reasoning judgment.

---

## Stopping conditions

Stop and return when any of these holds:

1. The Verifier returns `ACCEPT`.
2. The turn budget is hit (default five).
3. Two consecutive `REVISE` turns carry the same diagnosis (no progress) — stop and escalate rather than loop.

On any non-accept stop, return the best-verified partial result plus the outstanding diagnosis. Re-read the transcript before declaring done.

---

## Cross-reference

- `/orchestrate` (PATTERNS.md) — boundary definitions of Loop Until Done and Adversarial Verification, which this loop composes.
- `/orchestrate` — the Conductor loop for splitting a multi-part task across workers; it can hand a single subtask to this skill for checking.
