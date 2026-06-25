---
name: orchestrate
disable-model-invocation: true
description: Conductor loop that decomposes a hard task, routes each subtask to the best worker, recurses on the hard parts, and synthesizes the results.
tags: [plan, engineering, productivity]
args: "<hard or multi-part task (optional)>"
---

# Orchestrate

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

You are the Conductor. For a hard, multi-part task you do not solve it directly — you decompose it, write a natural-language workflow spec, route each subtask to the best available worker, and synthesize their outputs. Recurse on the parts that are still too hard. Contracts, the spec format, routing heuristics, and worker tiers live in [REFERENCE.md](REFERENCE.md); the abstract pattern catalog this loop composes is in [PATTERNS.md](PATTERNS.md); a worked trace is in [EXAMPLES.md](EXAMPLES.md).

## When to orchestrate

Orchestrate only when the single-prompt ceiling is the real bottleneck:

- The task splits into parts that suit different skills or different workers.
- Parts are independent and can run in parallel, or a hard part needs its own decomposition.
- A single pass keeps producing work that fails review.

Do NOT orchestrate when one prompt fits with room to spare, no parts are genuinely independent, and quality is checkable in the same pass. Easy tasks are 1-2 steps; reserve more steps for genuinely hard ones.

## vs the pattern catalog and /trinity

[PATTERNS.md](PATTERNS.md) is the catalog of abstract patterns; this skill is one applied composition of them — Fan Out and Synthesize for independent steps plus recursion for hard ones. Read PATTERNS.md to pick a shape; use this skill to run the Conductor loop. When a single subtask must be checked and refined before you trust it, hand that subtask to `/trinity` rather than verifying it inline. Cross-reference both; do not re-explain them.

## The loop

1. **Decompose.** Break the task into ordered steps. Write the step list to a progress file before running anything.
2. **Spec each step** as three index-aligned lists — `model_id` (which worker), `subtask` (a prompt-engineered instruction for that worker), `access_list` (which prior step outputs it may read). Format details in REFERENCE.
3. **Route.** Pick the best available worker per step from its task character (routing table in REFERENCE). Choose the highest worker tier actually available (REFERENCE).
4. **Run** each step. Steps with disjoint access lists may fan out in parallel; dependent steps sequence. Capture every output to the progress file.
5. **Check** steps whose correctness matters. For verification-heavy steps, dispatch `/trinity`; for cheap checks, inspect inline.
6. **Recurse** only on a subtask still too hard, naming yourself as its `model_id`. The subtask must shrink, and you must decrement the recursion and turn budgets (rule in REFERENCE).
7. **Synthesize** the step outputs into the final answer.
8. **Stop** on success or when a budget is hit; re-read the progress file before the done check.

## Budgets

Keep a small global turn budget (default five turns) and a small recursion-depth cap (default two). A recursion that does not shrink the subtask is not allowed. On budget exhaustion, return the best-verified partial result plus the open question — never loop forever.

## Output

Return the final answer, the step trace (which worker ran which subtask with which access list), any verifier verdicts, and the budgets consumed. Persist the trace to a file so it survives context loss.

## Anti-patterns

- **Over-orchestrating** a task a single prompt would solve — run the ceiling test first.
- **Unbounded recursion** — every recursion must shrink the subtask and spend budget.
- **Mono-routing** every step to one worker — route by task character.
- **Assuming external workers exist** — degrade to the highest tier actually available.
- **Routing on hidden context** — a step sees only the outputs named in its access list.
