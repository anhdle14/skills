---
name: edit-article
description: Edit and improve articles by restructuring sections, improving clarity, and tightening prose. Use when user wants to edit, revise, or improve an article draft.
tags: [writing, transform]
args: "<path to article file>"
---

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
