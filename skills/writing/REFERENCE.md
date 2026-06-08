# Writing Reference

## Fragments Mode

Run a grilling session that produces fragments. Interview the user about whatever they want to write about. Do not impose phases, outlines, or structure.

As fragments emerge, append them to a single markdown file. Capture fragments from the first thing the user says, including the initial prompt.

On first write: one H1 with a working title, nothing else.

A fragment is any piece of text that might survive into the final article. It must be readable by the author, but need not be comprehensible to a cold reader. The bar is "is this a piece of good writing?" not "is this a self-contained argument?"

Examples:

- A sharp sentence the author might deploy later
- A claim with a one-line justification
- A vignette, scenario, analogy, or code snippet
- A half-thought to work out later
- A quote, dialogue, or overheard line
- A cluster of observations that hang together by feel

File format:

```markdown
# Working title

First fragment lives here.

---

Second fragment.
```

Fragments are separated by `\n---\n`. No headings inside the body. No tags. No imposed order.

Append silently. Mention what you added in passing, but do not interrupt the conversation. Never overwrite; only append or edit a specific fragment if the user asks.

## Shape Mode

Treat the input file as a raw pile. Read it end-to-end before doing anything else.

Run a shaping session that produces a separate article document. Do not edit the raw material file.

Workflow:

1. Read the pile and form a sense of what is in it.
2. Draft 2-3 candidate openings. Each implies a different thesis or angle. The chosen opening defines what the rest of the article must do.
3. Grow paragraph by paragraph. After the opening lands, ask what the reader needs next. Pull material from the pile.
4. Argue format choices out loud: paragraph, list, table, callout, quote, or code block.
5. Append each agreed paragraph immediately. Loop until the user says the article is done.

Useful questions:

- What does this paragraph do for the reader that the previous one did not?
- If I cut this, what breaks?
- Is this prose, or should it be a list?
- The opening promised X; have we drifted to Y?

Format guidance:

- Prose carries argument; lists carry parallel items.
- Use callouts only when inline treatment would derail the main argument.
- Use tables when the same fields repeat 3+ times.
- Quote when the original wording is the point; paraphrase when only the idea matters.

Out of scope:

- Mining for new fragments not in the pile
- Editing the raw material file
- Publishing or platform-specific formatting

## Beats Mode

Use when the article should feel like a journey rather than an argument.

Workflow:

1. Write 2-3 candidate starting beats from the raw material. Each is a different entry point. Preview where each might lead.
2. The user picks one. Write only that beat to the article file.
3. Re-read the article file. Offer 2-3 candidate next beats: different directions the journey could pivot from the current state.
4. Loop one beat at a time until the article reaches a natural end.

A beat is one move in the journey: it sets a scene, lands a point, asks a question, drops an aside, or twists the angle. It may be one sentence or several paragraphs. If it needs five paragraphs and three subheadings, split it.

Rules:

- Append one beat at a time.
- Never write ahead.
- Preserve user edits absolutely.
- If the user asks to rewrite or replace a prior beat, edit that beat in place and leave the rest alone.
- End when the journey is complete, not when the pile is empty.
