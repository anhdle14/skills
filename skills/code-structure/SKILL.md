---
name: code-structure
description: Analyze and improve code structure by mapping modules, finding deepening opportunities, separating orchestration from service mechanics, and planning safe refactors. Use when unfamiliar with a code area, deciding what belongs in actions versus services, extracting repeated operational blocks, improving architecture, or planning a refactor.
tags: [analyze, engineering, transform, plan]
---

# Code Structure

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
6. Run the repo's normal verification commands.

If the user asks for a refactor plan or issue, include: problem statement, solution, alternatives considered, scope boundaries, tiny commit plan where tests pass after each step, testing plan, risks, and rollback path.

## Watch For

- **God service**: one huge method hides the whole flow and removes caller control.
- **Leaky service**: service reaches into database tables or domain state directly.
- **Inconsistent service API**: every helper has different parameter and error conventions.
- **Premature abstraction**: logic used once is extracted because it "might" be reused.
- **Policy drift**: service starts deciding business rules that callers should own.
- **Map without decision**: orientation that never names the structural change it enables.

## Review Questions

- What module owns the domain concept?
- Does the proposed interface hide meaningful complexity, or just rename it?
- If this service disappeared, would the operation be duplicated across callers?
- Can each caller still express domain rules clearly?
- Are all inputs visible, and are success/failure states explicit?
- Would a bug fix in this operation now apply everywhere it should?
