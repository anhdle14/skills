# Orchestration Reference

Contracts, the workflow-spec format, routing heuristics, recursion rules, and worker-pool tiers for the Conductor loop in [SKILL.md](SKILL.md).

---

## Source synthesis

This protocol adapts the **Conductor** paper ("Learning to Orchestrate Agents in Natural Language with the Conductor"). The Conductor is a model trained to solve hard tasks *indirectly*: instead of answering, it emits an agentic workflow that divides the task, delegates targeted subtasks to a pool of worker models, and designs how information flows between them. The transferable idea — not the training method — is what this skill encodes: **decompose, route, recurse, synthesize**, all expressed in natural language.

Two of the paper's findings shape the rules below:

- **Harder tasks deserve more steps.** The Conductor learns to allocate more compute (more steps, more workers, verification rounds) to hard problems and to keep easy ones to one or two steps. Match step count to difficulty; do not pad.
- **No single worker is best at everything.** Routing each subtask to the worker whose strengths fit it beats sending everything to the strongest single worker.

For the iterative verification of a single subtask, this skill defers to `/trinity` (the Thinker-Worker-Verifier loop). For the abstract pattern definitions it composes, see [PATTERNS.md](PATTERNS.md).

---

## The workflow-spec format

A workflow is N steps described by three index-aligned lists. Step `i` is the triple `(model_id[i], subtask[i], access_list[i])`.

- **`model_id[i]`** — the worker assigned to step `i`. May be a named worker, a role-played persona, or *yourself* (which triggers recursion — see below).
- **`subtask[i]`** — a self-contained, prompt-engineered instruction for that worker. Write it as if the worker sees nothing but this string plus the outputs named in its access list. Be explicit about the expected output shape.
- **`access_list[i]`** — the indices of earlier steps whose outputs step `i` may read. Empty `[]` means a cold start with no prior context; `[0, 2]` means it sees the outputs of steps 0 and 2 and nothing else.

The access list **is the dependency graph**:

- Steps with **disjoint** access lists (none depends on another's output) are independent and may **fan out in parallel**.
- A step whose access list names another step **must run after** it (sequence).
- A synthesis step typically has an access list naming every branch it merges.

Worked snippet — count complete subarrays, then implement:

```
model_id    = [ reasoning_worker,          coding_worker ]
subtask     = [ "Design an efficient algorithm to count
                 complete subarrays of an array; return
                 the approach and complexity",
                "Implement the algorithm from the prior
                 step in Python; return runnable code" ]
access_list = [ [],                        [0] ]
```

Step 1 sequences after step 0 because it reads step 0's design.

---

## Routing heuristics

Route by the *character* of the subtask, not by brand. Maintain a small registry of the workers actually available to you and match capability to task.

| Subtask character | Route to |
|---|---|
| Precise long-form code, refactor, debugging | strongest coding worker |
| Step-by-step math, proof, derivation | strongest reasoning worker |
| Broad recall, drafting, summarization | fast generalist worker |
| Scientific or domain knowledge | worker strongest in that domain |
| Checking another worker's output | a *different* worker than the one that produced it |

Rules:

- When the pool allows it, the checker is always a different worker than the producer — independence catches errors a self-check misses.
- If only one worker exists, role-play the distinct subtasks in sequence (Tier B below); the routing logic is unchanged, only the dispatch differs.
- Re-route adaptively: if a worker's output fails a check, try a different worker for the retry rather than the same one.

---

## Recursion and test-time scaling

You may name yourself as `model_id[i]` to re-enter the whole Conductor loop on a single hard subtask — a recursive topology that buys more test-time compute where it matters. Guardrails:

- **Must shrink.** The recursive subtask must be strictly smaller than the parent. If it is not smaller, do not recurse — solve it directly or route it.
- **Depth cap.** Default maximum recursion depth is two. Decrement the remaining depth on each descent.
- **Shared turn budget.** Recursion spends the same global turn budget as the top level; it does not get a fresh one. Decrement it.
- **Return contract.** A recursive call returns its synthesized result to the parent step exactly as any worker would.

---

## Worker-pool substrate tiers

The protocol is identical across tiers; only how you dispatch a `model_id` changes. Choose the **highest tier actually available** and never assume a tier you cannot confirm.

- **Tier A — real workers.** When sub-agents or per-call model selection are available, dispatch each `model_id` to a distinct sub-agent or model. You get true isolation and real parallelism for fan-out.
- **Tier B — single-context role-play.** When only one model and one context are available, play each `model_id` and role in sequence yourself. Keep role boundaries strict and **write each step's output to a file**, so a later checking step reads the artifact from disk rather than from your working memory.
- **Tier C — external workers via MCP.** Only when an MCP model bridge is genuinely connected. Never assume it; if it is absent, degrade to Tier B.

Dispatch is the runtime's job, not a bundled script — this skill ships no script because every decision (decompose, route, recurse) is a reasoning judgment, not a deterministic transform.

---

## Stopping conditions

Stop and return when any of these holds:

1. The final synthesis is produced and any required checks passed.
2. The global turn budget is hit.
3. The recursion-depth cap is hit.
4. Two consecutive retries of the same step fail with the same diagnosis (no progress) — stop and escalate rather than loop.

On any non-success stop, return the best-verified partial result plus the outstanding question. Re-read the progress file before declaring done.

---

## Cross-reference

- [PATTERNS.md](PATTERNS.md) — boundary definitions of Fan Out and Synthesize, Loop Until Done, and Adversarial Verification, which this protocol composes. Do not re-derive them here.
- `/trinity` — the Thinker-Worker-Verifier loop to hand a single subtask that needs iterative checking.
