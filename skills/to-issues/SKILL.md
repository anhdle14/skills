---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable issues using tracer-bullet vertical slices. Use when user wants to convert a plan into issues, create implementation tickets, or break down work into issues.
tags: [plan, engineering, manage]
args: "<issue reference, URL, or path (optional)>"
---

# To Issues

Break a plan into independently-grabbable issues using vertical slices (tracer bullets).

## Process

### 1. Gather context

Work from whatever is in the conversation. If the user passes an issue reference, fetch it from the issue tracker and read its full body and comments.

### 2. Explore the codebase (if needed)

Understand the current state of the code. Issue titles and descriptions should use the project's domain glossary.

### 3. Draft vertical slices

Each issue is a thin vertical slice cutting through ALL integration layers end-to-end, NOT a horizontal layer slice.

**Vertical slice rules:**

- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones

**Slice types:**

- **HITL** — requires human interaction (architectural decision, design review)
- **AFK** — can be implemented and merged without human interaction

Prefer AFK over HITL where possible.

### 4. Quiz the user

Present as a numbered list. For each slice show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which slices must complete first (if any)
- **User stories covered**: from the source material (if any)

Ask:

- Does the granularity feel right?
- Are dependency relationships correct?
- Should any slices be merged or split?
- Are HITL/AFK assignments correct?

Iterate until the user approves.

### 5. Publish

Publish in dependency order (blockers first) so you can reference real IDs in "Blocked by".

Use this issue body template:

```markdown
## Parent
[reference to parent issue, if applicable]

## What to build
[concise description of this vertical slice — end-to-end behavior, not layer-by-layer]

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by
[reference to blocking issue, or "None — can start immediately"]
```

Do NOT close or modify any parent issue.
