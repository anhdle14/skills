---
name: research
description: Researches engineering decisions by gathering evidence about current behavior, constraints, options, tradeoffs, and next steps. Use when user asks to research, investigate, compare approaches, answer what exists/why/what to do, or start the engineering stack. For module maps, architecture, service boundaries, or refactor shape, use code-structure.
tags: [analyze, engineering, plan]
args: "<question, feature, bug, or repo area (optional)>"
---

# Research

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Research is the first stage of the engineering stack:

```text
research -> prototype -> plan -> build -> test -> polish
```

The shape is always: **what, why, do, challenge**.

## When To Use

Use this when the work is unclear and a decision needs evidence before
prototyping, planning, or implementation. Research may inspect code, docs,
tests, issues, and external references, but its job is to answer a decision:
**what exists, why it matters, what should happen next, and what assumptions
could be wrong**.

Use `/code-structure` instead when the request centers on module maps, callers,
ownership boundaries, action-vs-service placement, repeated operational blocks,
architecture cleanup, or refactor shape. If the user says "understand this code
area" and the expected output is a structural map, use `/code-structure`; if the
expected output is evidence for a product or technical decision, use research.

Do not use this for metric-driven autonomous ML experiments; use
`/autoresearch`. For a live bug with symptoms, use `/diagnose`.

## Workflow

### 1. What

Name the concrete question. Inspect the repo, docs, tests, runtime behavior, and
existing decisions that bear on it. Prefer local evidence over memory.

Capture:

- Current behavior or architecture
- Relevant files, commands, data paths, constraints, and prior decisions
- Known constraints and unknowns

### 2. Why

State why the question matters:

- User or maintainer outcome
- Failure mode or opportunity
- Cost of doing nothing
- Success criteria

### 3. Do

Recommend the smallest next action that can move the work forward. Route to the
next stack stage when appropriate:

- `/prototype` when the answer needs a throwaway model or UI
- `/plan` when enough is known to sequence implementation
- `/build` when the change is obvious and low-risk
- `/test` when the main gap is proof through behavior tests
- `/polish` when the implementation exists but quality is unfinished

### 4. Challenge

Attack the recommendation before presenting it:

- What assumption would break it?
- What cheaper path might work?
- What risk or migration cost is being hidden?
- What evidence is missing?

## Output

Use this shape: `What` evidence-backed current state; `Why` reason and
success criteria; `Do` recommended next action; `Challenge` risks,
counterarguments, and missing evidence; `Next` stack stage and first step.

## Related Skills

- `/code-structure` for structural maps, architecture/refactor questions, and
  deciding where logic belongs across modules or layers.
- `/diagnose` for live bugs, failures, regressions, and root-cause loops.
- `/plan` when the decision is already made and the user needs sequencing.

## Anti-Patterns

- Research that never names a decision.
- Producing a module/caller map when the user asked for a recommendation.
- Collecting links or files without explaining why they matter.
- Skipping the challenge section because the answer feels obvious.
