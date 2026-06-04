---
name: write-a-skill
description: Interactively build a new agent skill — gather requirements, draft SKILL.md with proper frontmatter, bundle supporting files, and walk the user through it step by step. Use when user wants to create, write, or build a new skill.
tags: [productivity, create]
---

# Write a Skill

## Process

1. **Gather requirements** — ask the user:
   - What task or domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?

2. **Draft the skill** — create:
   - `SKILL.md` with the schema below
   - Additional reference files if content exceeds ~100 lines
   - Utility scripts under `scripts/` if deterministic operations are needed

3. **Review with user** — present the draft and ask:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?

4. **Write to `skills/<name>/`** in this repo after approval.

5. **Run `deno task install --update-index`** to regenerate the `CLAUDE.md` skills table.

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

**Good:** `Extract text and tables from PDF files. Use when working with PDFs or user mentions forms, extraction, or document parsing.`

**Bad:** `Helps with documents.`

## Skill Structure

```text
skills/
└── skill-name/
    ├── SKILL.md           # required — main instructions + frontmatter
    ├── REFERENCE.md       # optional — detailed docs if SKILL.md would exceed ~100 lines
    ├── EXAMPLES.md        # optional — usage examples
    └── scripts/           # optional — utility scripts for deterministic operations
        └── helper.ts
```

## When to Add Scripts

Add a script (TypeScript + Deno) when:

- The operation is deterministic (validation, formatting, file manipulation)
- The same code would be generated repeatedly across sessions
- Errors need explicit structured handling

Scripts save tokens and improve reliability vs re-generating equivalent code each time.

## When to Split Files

Split into separate reference files when:

- `SKILL.md` would exceed ~100 lines
- Content has distinct domains (e.g. separate format guides)
- Advanced features are rarely needed and would clutter the main file

## Review Checklist

- [ ] Description includes "Use when..." triggers
- [ ] `SKILL.md` under ~100 lines (split if longer)
- [ ] No time-sensitive information baked in
- [ ] Consistent terminology throughout
- [ ] `tags` accurately reflect the skill's category
- [ ] `args` documented if the skill accepts arguments
