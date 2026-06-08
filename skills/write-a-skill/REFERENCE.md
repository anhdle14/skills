# Skill Pattern Reference

Observed patterns:

- Focused skills are often long and explicit, with `When to Use`, workflow phases, anti-patterns, red flags, and verification gates.
- Compact personal skills work best when they stay under the local line budget, use strong workflow shape, and avoid explanatory padding.
- Operational skills tend to need routing, artifact sync, completion statuses, safety boundaries, and tool-backed workflows.
- Large skill libraries commonly separate canonical skills, agent-specific copies, docs, and translations; repeated sections include `When to Activate`, `How It Works`, examples, best practices, related skills, and verification loops.

## Common Structure

A strong personal skill usually has this shape:

1. Frontmatter with a clear capability sentence and a trigger sentence starting with `Use when`.
2. A short activation or boundary section when adjacent skills could conflict.
3. Ordered workflow steps.
4. Explicit output shape or artifact path.
5. Verification or completion criteria.
6. Anti-patterns, red flags, or "do not" rules where agents often drift.
7. Related skill handoffs only when they change behavior.

Do not force every section into every skill. A mode skill like `caveman` can stay tiny. A workflow skill like `diagnose`, `review`, or `to-issues` needs stronger output and verification gates.

## Common Skill Families

Repeated useful families:

- Debugging and diagnosis: reproduce, localize, instrument, fix, regression-test, report evidence.
- Test-driven development: red/green/refactor, smallest honest test, public seams, coverage only where meaningful.
- Review and quality: correctness, standards, spec fit, security, performance, and verification strength.
- Planning and specification: current-state evidence, scope boundaries, acceptance criteria, rollback, issue slicing.
- QA and verification: conversational issue capture, browser/e2e checks, build/type/lint/test gates, proof of completion.
- Context and handoff: compact state, save artifacts, restore work, route to the next skill.
- Skill authoring and skill-set audit: trigger metadata, progressive disclosure, validation scripts, overlap reduction.
- Writing workflows: fragments, shaping, beat-by-beat construction, editing, and voice/style preservation.
- Safety and operations: destructive-action boundaries, deployment checks, canaries, and completion statuses.

## Description Pattern

Use two sentences:

```text
Does X for Y. Use when user says A, asks for B, is doing C, or mentions D.
```

Rules:

- Put the key noun and verb in the first 10 words.
- Include user phrases, not only formal terminology.
- Prefer concrete triggers over broad categories.
- Avoid "helps with", "assists", and generic adjectives.
- If the skill must not trigger implicitly, say that in the body and make the description narrow.

## Section Pattern

Use these section names when they fit:

- `When To Use`: trigger and non-trigger boundaries.
- `Workflow`: the ordered path.
- `Output`: final artifact shape, issue body, report shape, or next-action format.
- `Verification`: commands, checks, or evidence required before claiming done.
- `Anti-Patterns`: common errors that would make the skill worse than a normal prompt.
- `Related Skills`: explicit handoff conditions.

## Progressive Disclosure

Keep `SKILL.md` under the repo validator limit and move detail out:

- `REFERENCE.md`: long concepts, framework variants, detailed checklists.
- `EXAMPLES.md`: realistic prompts and outputs.
- `scripts/`: deterministic commands, formatters, validators, fetchers, or scaffolds.
- `assets/`: templates or files used in generated output.

Every referenced file must be named from `SKILL.md` with when to read it. Avoid deep reference chains.

## Patterns Worth Keeping

- Anti-patterns, red flags, "verify the verification", and source-driven decisions.
- Terse bodies, strong workflows, and small personal scope.
- Completion statuses, safety gates, context recovery, and artifact handoffs.
- Activation sections, related-skill routing, validation loops, and skill-set audits.

## Audit Heuristics

For a skill-set audit, inspect:

- Skills with missing or vague descriptions.
- Skills whose descriptions overlap without a routing rule.
- Skills over the line budget that should split references.
- Skills that produce artifacts without an output template.
- Skills that can claim completion without evidence.
- Skills that repeat deterministic command logic instead of using scripts.
