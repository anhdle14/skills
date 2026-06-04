---
name: request-refactor-plan
description: Create a detailed refactor plan with tiny commits via user interview, then file it as an issue. Use when user wants to plan a refactor, create a refactoring RFC, or break a refactor into safe incremental steps.
tags: [plan, engineering, transform]
---

# Request Refactor Plan

Create a detailed refactor plan through structured interview, then file it as an issue on the project tracker.

## Process

1. **Understand the problem.** Ask for a detailed description of the problem and any potential solution ideas.

2. **Verify in the codebase.** Explore the repo to confirm assertions and understand the current state.

3. **Explore alternatives.** Ask whether other approaches have been considered. Present any alternatives you see.

4. **Interview about the implementation.** Be detailed and thorough:
   - What exactly changes?
   - What does NOT change (explicit scope boundary)?
   - What are the risks?
   - What's the rollback plan?

5. **Hammer out scope.** Work out exactly what will and won't be touched.

6. **Check test coverage.** Look for existing tests in the affected area. If insufficient, ask what the testing plan is.

7. **Break into tiny commits.** Follow Martin Fowler: "make each refactoring step as small as possible, so that you can always see the program working."

8. **File the issue** using this template:

```markdown
## Problem Statement
[the problem, from the developer's perspective]

## Solution
[the proposed solution]

## Alternatives Considered
[other approaches and why they were rejected]

## Scope
### In scope
- [...]

### Out of scope
- [...]

## Commit Plan
1. [first tiny commit — always passing tests]
2. [second tiny commit — always passing tests]
3. [...]

## Testing Plan
[how the refactor will be verified]

## Risks
[what could go wrong and how to mitigate]
```
