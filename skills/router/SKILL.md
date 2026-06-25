---
name: router
disable-model-invocation: true
description: Human-only index of the disable-model-invocation skills - names each and when to reach for it.
tags: [productivity]
---

# Router

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

These skills set `disable-model-invocation: true`, so the agent never sees them and they never
auto-trigger. They cost zero context load; the price is that *you* are the index. This skill is that
index: type the invocation by hand.

| Skill | Invoke | Reach for it when |
|-------|--------|-------------------|
| **autoresearch** | `/skill:autoresearch` | Optimizing an agreed metric under a fixed harness with an autonomous experiment loop (Karpathy autoresearch protocol). |
| **orchestrate** | `/skill:orchestrate` | A hard task splits into parts suited to different workers - decompose, route each subtask, recurse on the hard parts, synthesize (the Conductor loop). |
| **trinity** | `/skill:trinity` | One coherent task whose correctness must be *earned* before you trust it - a Thinker-Worker-Verifier accept-or-revise loop. |

## Choosing between them

- **Split vs. verify.** `/orchestrate` when the work fans out across many workers; `/trinity` when a
  single problem needs checking and refinement. Orchestrate hands verification-heavy subtasks to
  trinity; trinity steps up to orchestrate when one task turns out to be many.
- **Pattern catalog.** Both compose the abstract workflow patterns catalogued in
  `/orchestrate`'s `PATTERNS.md` - read it to pick a shape before running either loop.
