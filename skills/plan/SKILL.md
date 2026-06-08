---
name: plan
description: Turns evidence into engineering plans, PRDs, or vertical-slice issue breakdowns with scope, sequence, risks, and verification. Use when user asks for a plan, PRD, implementation plan, roadmap, tickets, issues, or breakdown before coding.
tags: [plan, engineering, create, manage]
args: "<goal, artifact, or repo area (optional)>"
---

# Plan

Plan is the third stage of the engineering stack:

```text
research -> prototype -> plan -> build -> test -> polish
```

The job is to decide what will be built, how it is sliced, and how done will be
proved. PRDs and implementation issues are plan outputs, not separate skills.

## When To Use

Use this after enough research or prototyping exists to sequence work. Also use
it for PRDs, tickets, implementation issues, or roadmaps. If the unknown is
still conceptual or experiential, go back to `/research` or `/prototype`.

## Workflow

### 1. Ground The Plan

Summarize the evidence: repo state, user goal, prototype result, constraints,
and non-goals. If evidence is missing, name the missing fact instead of filling
it with speculation.

### 2. Define Scope

Separate in scope, out of scope, open questions, and assumptions.

### 3. Choose Artifact

- **Plan**: scope, ordered steps, risks, verification, next stage.
- **PRD**: problem, solution, stories, decisions, criteria, rollback, out of
  scope.
- **Issues**: independently grabbable vertical slices with dependencies,
  acceptance criteria, verification, and out-of-scope notes.

Only publish to an issue tracker when the user asks.

### 4. Sequence The Work

Prefer vertical slices that leave the repo working after each step. Each step
should name likely files/areas, visible behavior, verification, and dependency.

For issues, prefer many thin slices over few thick ones. Label slices `AFK` when
an agent can implement them alone, and `HITL` when a decision is required.

### 5. Name Risks

Call out migration risk, compatibility risk, test gaps, performance risk,
security risk, and places where user input is required.

### 6. Hand Off

End with the next stack stage:

- `/build` when the plan is actionable
- `/prototype` when the plan still rests on a design guess
- `/test` when implementation exists and needs behavior proof

## Output

Use the requested shape:

- **Plan**: Scope, Sequence, Risks, Next.
- **PRD**: Problem Statement, Solution, User Stories, Implementation Decisions,
  Testing Decisions, Acceptance Criteria, Rollback / Failure Handling, Out of
  Scope.
- **Issue**: What to build, Acceptance criteria, Blocked by, Verification, Out
  of scope.

## Anti-Patterns

- Layer-by-layer plans that cannot be verified until the end.
- Plans that omit verification.
- Treating unresolved product decisions as engineering tasks.
- Publishing issues before checking granularity and dependencies with the user.
