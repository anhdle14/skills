---
name: research
description: Researches engineering work by answering what exists, why it matters, what to do, and how to challenge assumptions. Use when user asks to research, investigate, understand a codebase, compare approaches, or start the engineering stack.
tags: [analyze, engineering, plan]
args: "<question, feature, bug, or repo area (optional)>"
---

# Research

Research is the first stage of the engineering stack:

```text
research -> prototype -> plan -> build -> test -> polish
```

The shape is always: **what, why, do, challenge**.

## When To Use

Use this when the work is unclear, the repo area is unfamiliar, or a decision
needs evidence before prototyping or planning.

Do not use this for metric-driven autonomous ML experiments; use
`/autoresearch`. For a live bug with symptoms, use `/diagnose`.

## Workflow

### 1. What

Name the concrete question. Inspect the repo, docs, tests, runtime behavior, and
existing decisions that bear on it. Prefer local evidence over memory.

Capture:

- Current behavior or architecture
- Relevant files, commands, data paths, and ownership boundaries
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

Use this shape:

```markdown
## What
[evidence-backed current state]

## Why
[reason this matters and success criteria]

## Do
[recommended next action]

## Challenge
[risks, counterarguments, missing evidence]

## Next
[stack stage and concrete first step]
```

## Anti-Patterns

- Research that never names a decision.
- Collecting links or files without explaining why they matter.
- Skipping the challenge section because the answer feels obvious.
