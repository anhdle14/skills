---
name: to-prd
description: Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context, formalize a feature, or document what's being built.
tags: [plan, engineering, create]
---

# To PRD

Synthesize the current conversation and codebase understanding into a PRD. Do NOT interview the user — just synthesize what you already know.

## Process

1. Explore the repo to understand the current codebase state (if you haven't already). Use the project's domain glossary throughout.

2. Sketch the seams at which you'll test the feature. Prefer existing seams. Propose new ones at the highest point possible.

   Check with the user that these seams match their expectations.

3. Draft scope boundaries before solution details: what changes, what stays, and what is explicitly out of scope.

4. Write the PRD using the template below, then publish it to the project issue tracker.

## PRD Template

```markdown
## Problem Statement
[the problem the user is facing, from the user's perspective]

## Solution
[the solution, from the user's perspective]

## User Stories
[numbered list — as exhaustive as possible]
1. As a <actor>, I want <feature>, so that <benefit>

## Implementation Decisions
[modules to build/modify, interface changes, schema changes, API contracts, architectural decisions]
[no specific file paths or code snippets unless from a prototype that encodes a decision precisely]

## Testing Decisions
[what makes a good test for this feature, which modules to test, prior art in the codebase]

## Acceptance Criteria
[testable user-visible outcomes]

## Rollback / Failure Handling
[what happens if the implementation ships wrong, or why rollback is not applicable]

## Out of Scope
[explicit list of what this PRD does NOT cover]

## Further Notes
[anything else]
```

## Quality Gate

Before publishing, check that the PRD names current state evidence, user-visible outcomes, acceptance criteria, testing seams, out-of-scope items, and rollback/failure handling.
