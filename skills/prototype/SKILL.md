---
name: prototype
description: Build a throwaway prototype to answer a design question before committing. Routes to a terminal app for state/logic questions, or multiple UI variations for design questions. Use when user wants to prototype, sanity-check a data model or state machine, mock up a UI, or says "prototype this", "let me play with it", "try a few designs".
tags: [create, plan, engineering]
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered:

- **"Does this logic / state model feel right?"** → Build a tiny interactive terminal app that pushes the state machine through cases that are hard to reason about on paper.
- **"What should this look like?"** → Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

If the question is ambiguous and the user isn't reachable, default to whichever matches the surrounding code (backend module → logic; page/component → UI) and state the assumption at the top.

## Rules for both branches

1. **Throwaway from day one, clearly marked.** Locate it close to where it'll be used; name it so it's obviously not production.
2. **One command to run.** Whatever the project's task runner supports.
3. **No persistence by default.** State lives in memory unless the question explicitly involves a database.
4. **Skip the polish.** No tests, no error handling beyond runnable, no abstractions.
5. **Surface the state.** After every action (logic) or variant switch (UI), print/render the full relevant state.
6. **Delete or absorb when done.** Don't leave it rotting in the repo.

## When done

Capture the **answer** somewhere durable (commit message, ADR, issue, or `NOTES.md` next to the prototype). The prototype itself should be deleted once it's answered its question.
