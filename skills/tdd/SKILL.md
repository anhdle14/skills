---
name: tdd
description: Test-driven development with red-green-refactor loop using vertical tracer-bullet slices. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development.
tags: [engineering, create]
---

# Test-Driven Development

## Philosophy

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** exercise real code paths through public APIs. They describe *what* the system does, not *how*. A good test survives refactors because it doesn't care about internal structure.

**Bad tests** are coupled to implementation — they mock internal collaborators, test private methods, or break when you rename an internal function without changing behavior.

## Anti-Pattern: Horizontal Slices

**Do not write all tests first, then all implementation.** This produces tests that verify the *shape* of things, not behavior. They pass when behavior breaks and fail when behavior is fine.

```text
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical tracer bullets):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

## Workflow

### 1. Plan

Before writing any code:

- [ ] Confirm what interface changes are needed
- [ ] Confirm which behaviors to test (prioritize — you can't test everything)
- [ ] List behaviors to test (not implementation steps)
- [ ] Get user approval on the plan

Use the project's domain glossary for test names and interface vocabulary.

### 2. Tracer Bullet

Write ONE test for ONE behavior:

```text
RED:   write test → fails
GREEN: write minimal code to pass → passes
```

This is your tracer bullet — proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```text
RED:   write next test → fails
GREEN: minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass the current test
- Don't anticipate future tests
- Focus on observable behavior at public interfaces

### 4. Refactor

After all tests pass:

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Per-Cycle Checklist

```text
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
