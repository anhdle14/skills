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
| **ship** | `/skill:ship` | **Whole pipeline, incl. review.** Driving a feature from a plan doc to shipped, reviewed vertical slices - the index and handoff contract for the four-phase pipeline below. |
| **ship-grill** | `/skill:ship-grill` | Interrogating a plan doc into a complete spec - resolve every grey area, build the glossary and ADRs, write the handoff contract. |
| **ship-slice** | `/skill:ship-slice` | **Build-only; spec already final.** Autonomously building a spec as vertical tracer-bullet slices across non-blocking phases, fanning out subagents, pausing only on a hard blocker. |
| **ship-review** | `/skill:ship-review` | Deeply reviewing finished deliverables - goal-backward against the spec plus an adversarial quality attack, reported as prioritized findings. |

## Choosing between them

- **One pipeline, four phases.** `/skill:ship` is the index; run its phases in order -
  grill the plan into a spec, slice and build it autonomously, then review. Each phase is
  also usable on its own.
- **Pattern catalog.** The ship phases compose the abstract workflow patterns catalogued in
  `skills/ship/PATTERNS.md` - read it to pick a shape before running a phase.
