---
name: write-a-skill
description: Builds or improves agent skills with trigger metadata, progressive disclosure, supporting files, and validation gates. Use when user wants to create, write, build, audit, refactor, or improve a skill.
tags: [productivity, create]
---

# Write a Skill

Use this for new skills and for improving existing skills. For the fuller pattern library, read [REFERENCE.md](REFERENCE.md) when choosing structure, splitting files, or auditing a skill set.

## Process

1. **Classify the job** — workflow, domain reference, tool wrapper, writing style, planning session, verification loop, or installer/orchestration skill. Name the expected output before drafting.
2. **Gather requirements** — ask only for missing facts that change behavior: triggers, non-triggers, artifacts, tools/scripts, references, constraints, and validation commands.
3. **Draft progressive disclosure** — keep `SKILL.md` as the activation and workflow guide. Move long examples, framework details, schemas, or command catalogs into `REFERENCE.md`, `EXAMPLES.md`, or `scripts/`.
4. **Review the trigger surface** — front-load the capability and likely user phrases. Include synonyms and exclude adjacent skills through body guidance.
5. **Write and validate** — write to `skills/<name>/`, run `deno task validate`, then run `deno task install --update-index` if the skill list changed.

## SKILL.md Schema

```yaml
---
name: skill-name                        # kebab-case, matches folder name
description: >                          # ≤1024 chars — this is what agents read to decide whether to load the skill
  What it does. Use when [specific triggers].
tags: [tag1, tag2]                      # pick from: analyze, create, plan, transform, manage, productivity, engineering, writing
args: "<arg-name> <optional-arg>"       # optional — document accepted arguments
---
```

## Description Requirements

The description is **the only thing an agent sees** when deciding which skill to load. It must answer:

1. What capability does this skill provide?
2. When/why should it trigger? (specific keywords, contexts, file types)
3. Which adjacent requests should still match because users use different words?

**Good:** `Extract text and tables from PDF files. Use when working with PDFs or user mentions forms, extraction, or document parsing.`

**Bad:** `Helps with documents.`

## Skill Structure

```text
skills/
└── skill-name/
    ├── SKILL.md           # required — main instructions + frontmatter
    ├── REFERENCE.md       # optional — detailed docs and variant guidance
    ├── EXAMPLES.md        # optional — realistic prompts/outputs
    └── scripts/           # optional — utility scripts for deterministic operations
        └── helper.ts
```

## Common Sections

- **When To Use** — activation and non-activation boundaries
- **Workflow** — ordered actions, with branch points called out
- **Output** — artifact or final-answer shape
- **Verification** — commands, evidence, or completion criteria
- **Anti-Patterns** — common failure modes the agent should avoid
- **Related Skills** — handoffs to nearby workflows

## When to Add Scripts

Add a script (TypeScript + Deno) when:

- Operation is deterministic: validation, formatting, file manipulation
- Same code would be regenerated repeatedly
- Errors need explicit structured handling
- Workflow needs a fragile command sequence

Scripts save tokens and improve reliability vs re-generating equivalent code each time.

## When to Split Files

Split into separate reference files when:

- `SKILL.md` would exceed ~100 lines
- Content has distinct domains or variants
- Advanced features are rarely needed and would clutter the main file

## Review Checklist

- [ ] Description includes "Use when..." triggers
- [ ] Description names synonyms users will actually type
- [ ] `SKILL.md` under ~100 lines (split if longer)
- [ ] Workflow has explicit output and verification expectations
- [ ] No time-sensitive information baked in
- [ ] Consistent terminology throughout
- [ ] Anti-patterns or boundaries prevent adjacent-skill confusion
- [ ] `tags` accurately reflect the skill's category
- [ ] `args` documented if the skill accepts arguments
- [ ] `deno task validate` passes
