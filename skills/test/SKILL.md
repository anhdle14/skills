---
name: test
description: Tests engineering changes through behavior proof, coverage, and red-green-refactor loops. Use when user asks to test, verify behavior, add coverage, prove a build works, use TDD, or mentions red-green-refactor.
tags: [engineering, create, analyze]
---

# Test

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Test is the fifth stage of the engineering stack:

```text
research -> prototype -> plan -> build -> test -> polish
```

The job is to prove behavior through public seams. When new behavior is being
built, prefer red-green-refactor.

## Philosophy

Tests verify behavior through public interfaces, not implementation details.
Code can change entirely; tests should not.

Good tests exercise real code paths through public APIs. Bad tests mock internal
collaborators, test private methods, or break when behavior is unchanged.

## Workflow

### 1. Name The Claims

List the behavior, integration, migration, or regression claims that need proof.
Prefer user-visible claims over implementation details.

### 2. Pick The Smallest Honest Test

- Pure logic or transformation -> unit test through public function/module API.
- Cross-module behavior -> integration test with real collaborators where cheap.
- User-visible flow -> browser, API, CLI, or smoke test at the boundary.
- Bug fix -> first write the test that would have caught the bug.

Do not mock the thing whose behavior you are trying to prove.

### 3. Use Red-Green-Refactor For New Behavior

Write one test for one behavior:

```text
RED:   write test -> fails
GREEN: write minimal code to pass -> passes
```

Then repeat for each remaining behavior. Never refactor while RED.

### 4. Verify Existing Builds

When implementation already exists, run focused checks first. Add regression
coverage only where a stable public seam exists and the risk justifies it.

### 5. Interpret Failures

Separate product failures, test harness failures, environment failures, and
unrelated pre-existing failures. Fix in-scope failures; report the rest clearly.

### 6. Refactor Only When Green

After tests pass, remove duplication, deepen modules, and rerun checks after
each meaningful cleanup.

## Output

Use this shape:

```markdown
## Claims
[what was tested]

## Evidence
[commands/checks and result]

## Gaps
[what remains unproven and why]

## Next
[/polish or the next failing behavior]
```

## Anti-Patterns

- Horizontal testing: write every test first, then every implementation.
- Running the biggest suite without knowing what it proves.
- Treating passing tests as proof when they do not cover the changed behavior.
- Brittle tests coupled to private implementation.
