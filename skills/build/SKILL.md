---
name: build
description: Implements planned software changes with narrow edits, repo conventions, and continuous verification. Use when user asks to build, implement, code, make the change, ship a feature, or continue from an approved plan.
tags: [create, engineering]
args: "<feature, fix, plan, or issue reference (optional)>"
---

# Build

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Build is the fourth stage of the engineering stack:

```text
research -> prototype -> plan -> build -> test -> polish
```

The job is to make the intended change real while keeping the repo coherent.

## When To Use

Use this when the target behavior is clear enough to edit code. If the user
explicitly asks for TDD, use `/test` for the red-green-refactor loop. If the
task is a hard bug with unclear cause, use `/diagnose` first.

## Workflow

### 1. Reconfirm The Target

State the behavior being changed and the smallest acceptable result. Check the
current worktree before editing and preserve unrelated user changes.

### 2. Read The Local Shape

Inspect existing patterns, helpers, tests, naming, and ownership boundaries in
the touched area. Prefer local conventions over new abstractions.

### 3. Edit Narrowly

Make the smallest cohesive change that implements the behavior. Keep commits or
logical chunks small enough that each could be explained and verified.

### 4. Verify As You Go

Run focused checks after meaningful chunks. If verification is too slow or
blocked, record what would prove the change and why it was not run.

### 5. Prepare For Test

Leave notes for the `/test` stage: expected behavior, touched seams, new or
changed commands, and any residual risk.

## Output

When done, report:

- What changed
- Where it changed
- What verification ran
- What remains for `/test` or `/polish`

## Anti-Patterns

- Broad rewrites to make a small change feel cleaner.
- Inventing a framework where the repo has a working pattern.
- Claiming implementation is complete without naming verification.
