---
name: code-structure
description: Analyze and improve code structure by mapping modules, finding deepening opportunities, separating orchestration from service mechanics, and planning safe refactors. Use when unfamiliar with a code area, deciding what belongs in actions versus services, extracting repeated operational blocks, improving architecture, or planning a refactor.
tags: [analyze, engineering, transform, plan]
---

# Code Structure

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Single home for structure-level code work: map unfamiliar areas, find structural friction, separate orchestration from services, and plan safe refactors.

Core rule: preserve product meaning in orchestration, move reusable mechanics behind deep, explicit interfaces.

## When To Use

Use this when:

- You do not know an area and need a map of modules and callers.
- A module feels shallow, leaky, or hard to test.
- Multiple workflows repeat the same operation with small variations.
- A bug fix in one path should clearly apply to another path too.
- You are unsure whether logic belongs in an action/controller/job or a shared service.
- The user wants to improve architecture, consolidate coupled modules, or plan a refactor.

Do not extract when the logic is used once, is genuinely domain-specific, or the extraction would make the caller harder to understand.

## Concepts

- **Module**: anything with an interface and implementation: function, class, package, feature slice.
- **Interface**: everything a caller must know: types, invariants, ordering, config, errors.
- **Depth**: useful behavior behind a small interface.
- **Locality**: related change, bugs, and knowledge kept in one place.
- **Deletion test**: if deleting a module makes complexity vanish, it was a pass-through; if complexity reappears across callers, it was earning its keep.
- **Seam**: where behavior can change without editing every caller. One adapter is hypothetical; two adapters are real.

## Process

### 1. Map

Read the domain glossary and ADRs first. Map modules, callers, owned domain concepts, data/control flow, tests, and existing seams.

### 2. Find Friction

Look for:

- One concept scattered across many small modules.
- Shallow modules where the interface is almost as complex as the implementation.
- Helpers extracted only for testability while real bugs live in call orchestration.
- Repeated operational blocks across two or more callers.
- Tight coupling, leaked provider details, or inconsistent error semantics.

For each candidate, state files, problem, proposed change, test impact, and recommendation strength: `Strong`, `Worth exploring`, or `Speculative`.

### 3. Split Layers

Orchestration code owns auth, ownership, policy, state transitions, persistence decisions, user-facing error classification, and call order.

Services own provider/SDK/CLI details, reusable mechanics, health/readiness checks, retries, timeouts, command execution, and structured results.

```text
"What does this product flow mean?" -> orchestration
"How do we perform this operation?" -> service
```

### 4. Design Interfaces

Prefer small capability blocks over a single "do everything" service: `createRuntime`, `prepareRepository`, `detectPackageManager`, `installDependencies`, `runBuild`, `startPreview`.

Each service function should accept explicit parameters, return structured data or documented errors consistently, avoid direct domain-state mutation, and avoid product-policy decisions. Good services let callers choose strict, relaxed, partial, or retry-heavy behavior without duplicating mechanics.

### 5. Refactor Safely

1. Write or read the concrete workflow in orchestration code first.
2. Mark operational chunks repeated across two or more callers.
3. Extract only repeated, non-domain mechanics.
4. Replace one caller, verify, then migrate the rest.
5. Keep auth, state transitions, and user-facing error policy in orchestration.
6. Run the repo's normal verification commands. If the area has no test/build harness (common for the legacy code this skill targets), define verification as a type-check plus a before/after behavior snapshot of the affected paths, and treat matching it as the gate.

If the user asks for a refactor plan or issue, include: problem statement, solution, alternatives considered, scope boundaries, tiny commit plan where tests pass after each step, testing plan, risks, and rollback path.

## When evaluating or reviewing a change

Consult [REFERENCE.md](REFERENCE.md) for the service anti-patterns to watch for and the review questions to run against a proposed extraction or structure plan.
