---
name: writing-shape
description: Shape a pile of raw material into an article — draft candidate openings, grow the piece paragraph by paragraph, argue about format at each step. Use when user has notes, fragments, or a rough draft and wants help turning it into something publishable.
tags: [writing, transform]
args: "<path to raw material file>"
---

# Writing Shape

The user has passed (or will pass) a markdown file of raw material. Treat it as the input pile — anything from a tidy list of fragments to a wall of unstructured prose. Read it end-to-end before doing anything else.

Run a shaping session that produces a separate article document. Do NOT edit the raw material file — it is read-only.

If the user did not say where to save the article, ask once and remember the path. Re-read the article file from disk before every write.

## The loop

1. **Read the pile.** Form a sense of what's in it.

2. **Draft 2–3 candidate openings.** Each implies a different thesis or angle. Show all of them. Force the user to pick or compose a hybrid. The chosen opening defines what the rest of the article must do.

3. **Grow paragraph by paragraph.** After the opening lands, ask "given this opening, what does the reader need to hear next?" Pull material from the pile. Argue about whether the next beat is a paragraph, a list, a table, a callout, a quote, a code block. Each format choice should be deliberate and defensible.

4. **Append to the article file as you go.** Don't batch. Write each agreed paragraph immediately.

5. **Loop step 3 until the article is done.** The user decides when it's done.

## Conversational moves to keep using

- "What does this paragraph do for the reader that the previous one didn't?"
- "If I cut this, what breaks?"
- "Is this prose, or should it be a list? Why prose?"
- "This sentence is doing two jobs — split it or pick one."
- "The opening promised X. We've drifted to Y. Either re-thread it or change the opening."

## Format arguments to have out loud

- **Prose vs. list.** Prose carries argument; lists carry parallel items. If items aren't truly parallel, prose is better.
- **Inline vs. callout.** Tips/warnings go in callouts only if they'd genuinely derail the main argument inline.
- **Table vs. repeated structure.** If the same shape repeats 3+ times with the same fields: table. Otherwise prose.
- **Quote vs. paraphrase.** Quote when the original wording is the point. Paraphrase when only the idea matters.

## Out of scope

- Mining for new fragments not in the pile — name the gap and either get the user to fill it or cut the section
- Editing the raw material file
- Publishing or platform-specific formatting
