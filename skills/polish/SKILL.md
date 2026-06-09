---
name: polish
description: Finishes engineering work with a quality pass over UX, code clarity, docs, edge cases, and handoff evidence. Use when user asks to polish, refine, clean up, harden, finish, improve the UX, or prepare work for review.
tags: [transform, engineering]
args: "<feature, diff, file, or repo area (optional)>"
---

# Polish

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Polish is the final stage of the engineering stack:

```text
research -> prototype -> plan -> build -> test -> polish
```

The job is to remove avoidable friction without changing the intended behavior.

## When To Use

Use this after the build and test stages, or when the user asks for a final
quality pass. For adversarial code review, use `/review`.

## Workflow

### 1. Scan The Surface

Look at the actual changed surface: UI, API, CLI output, docs, errors, tests,
types, and diff. Identify friction a user or maintainer would feel.

### 2. Tighten Behavior

Improve edge states, validation, empty states, loading states, error messages,
accessibility, naming, or docs when they are part of the changed behavior.

### 3. Tighten Code

Remove dead code, throwaway prototypes, duplicate branches, confusing names, and
unnecessary abstractions. Keep the cleanup scoped to the work.

### 4. Re-Verify

Run the focused checks that prove the polish did not change intended behavior.
If visual or interactive behavior changed, inspect it at the relevant surface.

### 5. Prepare Handoff

Summarize what is finished, what was verified, and any residual risk. If a fresh
agent needs to continue, use `/handoff`.

## Output

Report:

- Quality changes made
- Verification rerun
- Remaining risk or follow-up

## Anti-Patterns

- Cosmetic churn across unrelated files.
- Refactoring during polish without a concrete maintainer benefit.
- Changing scope after tests already proved the original behavior.
