---
name: review
description: Reviews code changes for correctness, standards, spec fit, security, performance, and missing verification. Use when user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
tags: [analyze, engineering]
args: "<commit, branch, tag, or merge-base to diff against>"
---

# Review

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Review the diff between `HEAD` and a fixed point the user supplies.

Primary axes:

- **Correctness** — bugs, edge cases, data loss, broken behavior
- **Standards** — repo conventions, domain language, architectural decisions
- **Spec** — acceptance criteria and intended behavior
- **Security** — auth, input handling, secrets, unsafe side effects
- **Performance** — avoidable slow paths, N+1s, excessive work
- **Verification** — missing or weak tests, unproven claims

Use parallel sub-agents for independent axes when available, then aggregate findings.

## Process

### 1. Pin the fixed point

The user must supply a reference: commit SHA, branch name, tag, or `main`/`master`. If not supplied, ask. Never review against a moving or guessed base without saying so.

```bash
git diff <ref>...HEAD
```

### 2. Gather context

- Read the diff and changed tests first.
- Read `CLAUDE.md`, `AGENTS.md`, standards, style docs, and ADRs in changed areas.
- Read the originating issue, PRD, or spec. Ask for it if not in context.
- Run or inspect verification only when it materially changes confidence.

### 3. Review independently

When sub-agents are available, split at least:

- **Standards/spec reviewer** — conventions, architecture, acceptance criteria.
- **Bug/security reviewer** — correctness, edge cases, trust boundaries.

When sub-agents are unavailable, keep the axes separate in your own notes.

### 4. Verify the verification

Do not accept "tests pass" as enough. Check whether tests cover the changed behavior, fail for the right reason, and exercise public seams.

### 5. Report

```markdown
## Findings
- [severity] file:line — issue, impact, evidence, suggested fix

## Open Questions
[only questions that block confidence]

## Verification
[commands inspected/run and what they prove]
```

Findings lead. Summaries are secondary. If there are no findings, say so and name residual test risk.

## Anti-Patterns

- Rubber-stamping because the diff is small.
- Reporting style preferences as bugs.
- Reviewing implementation before understanding tests and spec.
- Treating generated or AI-written code as lower risk.
