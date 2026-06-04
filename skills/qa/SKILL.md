---
name: qa
description: Interactive QA session where user reports bugs or issues conversationally, and the agent files structured issues on the issue tracker. Use when user wants to report bugs, do QA, file issues conversationally, or mentions "QA session".
tags: [analyze, manage, engineering]
---

# QA Session

Run an interactive QA session. The user describes problems. You clarify, explore the codebase for context, and file issues that are durable, user-focused, and use the project's domain language.

## For each issue the user raises

### 1. Listen and lightly clarify

Let the user describe the problem in their own words. Ask **at most 2–3 short clarifying questions** focused on:

- What they expected vs what actually happened
- Steps to reproduce (if not obvious)
- Whether it's consistent or intermittent

Do NOT over-interview. If the description is clear enough to file, move on.

### 2. Explore the codebase (in background)

While the user continues describing issues, explore the relevant area of the codebase to understand:

- Which module owns this behavior
- Whether there's existing test coverage
- What the domain glossary calls this concept

### 3. Draft the issue

Use the project's domain language. Include:

- Clear title (user-facing, not implementation-facing)
- What the user expected
- What actually happened
- Steps to reproduce
- Which module is likely responsible (from your codebase exploration)

### 4. Confirm before filing

Show the draft to the user: "Does this capture the issue?" File only after confirmation.

## Ending the session

When the user says they're done, summarize:

- How many issues were filed
- Any patterns you noticed (same module? same area?)
- Suggested next skill to invoke (e.g. `/triage` to prioritize, `/diagnose` for a specific bug)
