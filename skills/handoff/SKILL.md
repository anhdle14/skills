---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. Use when switching agents, ending a session, or when the user says "handoff".
tags: [productivity, plan]
args: "<what the next session will focus on (optional)>"
---

# Handoff

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

## Workflow

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS — not the current workspace.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Output

Use this shape:

- Current objective
- Current state
- Files and artifacts touched
- Commands run and results
- Open decisions or blockers
- Suggested next steps
- Suggested skills

## Verification

Before finishing, check the handoff has enough path, command, and status detail for a fresh agent to continue without the original transcript.
