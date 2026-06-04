---
name: grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates CONTEXT.md and ADRs inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
tags: [plan, engineering]
args: "<plan or topic to grill on>"
---

# Grill With Docs

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Domain awareness

During exploration, look for:

**Single-context layout** (most repos):
```
/
├── CONTEXT.md
└── docs/adr/
```

**Multi-context layout** (monorepos):
```
/
├── CONTEXT-MAP.md
├── docs/adr/          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

Create files lazily — only when you have something to write.

## During the session

**Challenge against the glossary.** When the user uses a term that conflicts with `CONTEXT.md`, call it out. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

**Sharpen fuzzy language.** When the user uses vague or overloaded terms, propose a precise canonical term.

**Stress-test with scenarios.** Invent edge cases that force the user to be precise about concept boundaries.

**Cross-reference with code.** If the user states how something works, check whether the code agrees. Surface contradictions.

**Update `CONTEXT.md` inline.** When a term is resolved, update `CONTEXT.md` immediately. It is a glossary only — no implementation details, no specs, no scratch-pad content.

**Offer ADRs sparingly.** Only when all three are true:
1. Hard to reverse — the cost of changing your mind later is meaningful
2. Surprising without context — a future reader will wonder "why did they do it this way?"
3. Result of a real trade-off — there were genuine alternatives

## ADR format

```markdown
# ADR-NNNN: [Title]

## Status
Accepted

## Context
[What situation led to this decision?]

## Decision
[What was decided?]

## Consequences
[What becomes easier or harder as a result?]
```

## CONTEXT.md format

```markdown
# [Project Name] Domain

## Language

**[Term]**: [Definition — precise, jargon-free, from the user's perspective]
_Avoid_: [alternative phrasings to reject]

## Relationships
- [Term A] holds many [Term B]s

## Flagged ambiguities
- "[old term]" — resolved: [how it was resolved]
```
