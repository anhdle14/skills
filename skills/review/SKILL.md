---
name: review
description: Two-axis code review — Standards (does the code follow this repo's conventions?) and Spec (does it match what the issue/PRD asked for?). Runs both in parallel sub-agents and reports side by side. Use when user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
tags: [analyze, engineering]
args: "<commit, branch, tag, or merge-base to diff against>"
---

# Review

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

## Process

### 1. Pin the fixed point

The user must supply a reference: commit SHA, branch name, tag, or `main`/`master`. If not supplied, ask.

```bash
git diff <ref>...HEAD
```

### 2. Gather context (in parallel)

**Standards sub-agent:**
- Read `CLAUDE.md`, `AGENTS.md`, any `docs/standards/` or `docs/style/` files
- Read `docs/adr/` for architectural decisions in the changed area
- Evaluate the diff against documented conventions

**Spec sub-agent:**
- Read the originating issue / PRD (ask the user for the reference if not in context)
- Read the diff
- Evaluate whether acceptance criteria are met

### 3. Report

Present findings side by side:

```
## Standards
[findings]

## Spec
[findings]

## Summary
[overall verdict — ship / needs work / discuss]
```

Flag blockers (must fix) separately from suggestions (nice to have).
