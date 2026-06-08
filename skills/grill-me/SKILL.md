---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
tags: [plan, productivity]
args: "<plan or topic to grill on>"
---

# Grill Me

## Workflow

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Question Rules

- Ask the highest-leverage unresolved question first.
- Include your recommended answer and why.
- Do not ask for facts already discoverable from the repo or existing docs.
- Track decisions already made so you do not re-open them accidentally.

## Done

Stop when the plan has explicit decisions, unresolved risks, and next actions. Summarize those three lists.
