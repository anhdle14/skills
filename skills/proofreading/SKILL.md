---
name: proofreading
description: Proofread and improve existing article drafts by restructuring sections, improving clarity, and tightening prose. Use when user wants to proofread, edit, revise, clean up, or improve an existing draft.
tags: [writing, transform]
args: "<path to article file>"
---

# Proofreading

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

## When To Use

Use for an existing prose draft. If the user has only fragments, notes, raw material, or wants to draft from scratch, hand off to `/writing`.

## Workflow

1. Divide the article into sections based on its headings. Think about the main points in each section.

   Information is a directed acyclic graph — pieces of information depend on other pieces. Make sure the order of sections respects these dependencies.

   Confirm the sections with the user.

2. For each section:

   a. Rewrite the section to improve clarity, coherence, and flow. Use maximum 240 characters per paragraph.

   b. Present the rewrite to the user before applying it.

   c. Apply approved changes to the file immediately.

3. After all sections are done, do a final pass for:
   - Consistent terminology throughout
   - Transitions between sections
   - Opening and closing paragraphs

## Output

Apply approved edits to the source file. In the final response, summarize changed sections and any unresolved structural concerns.

## Anti-Patterns

- Rewriting the whole article before the user accepts the direction.
- Optimizing sentences while the section order is still incoherent.
