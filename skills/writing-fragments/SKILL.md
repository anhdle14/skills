---
name: writing-fragments
description: Mine the user for writing fragments — claims, vignettes, sharp sentences, half-thoughts — and append them to a single document as raw material for a future article. Use when user wants to develop ideas before imposing structure, mentions "fragments", "ideate", or "raw material" for writing.
tags: [writing, create]
args: "<path to save fragments (optional)>"
---

# Writing Fragments

Run a grilling session that produces fragments. Interview the user relentlessly about whatever they want to write about. Do not impose phases, outlines, or structure — that is explicitly out of scope.

As fragments emerge, append them to a single markdown file. Re-read the file before every write — the user may have edited it between turns.

If the user did not pass a path, ask once where to save the document, then remember it for the rest of the session.

Capture fragments from the very first thing the user says, including the initial prompt.

On first write: one H1 with a working title, nothing else.

## What is a fragment

A fragment is any piece of text that might survive into the final article. It must be readable by the author, but need not be comprehensible to a cold reader. The bar is "is this a piece of good writing?" not "is this a self-contained argument?"

Examples:
- A sharp sentence you'd want to deploy somewhere but don't yet know where
- A claim with a one-line justification
- A vignette: a thing that happened, a code snippet, a scenario, an analogy
- A half-thought: "something about how X feels like Y, work this out later"
- A quote, a piece of dialogue, an overheard line
- A cluster of related observations that hang together by feel

## File format

```markdown
# Working title

First fragment lives here.

---

Second fragment.

---

> A quoted line.

A reaction to it.
```

Fragments are separated by `\n---\n`. No headings inside the body. No tags. No order beyond the order they were added.

## Writing rhythm

Append silently. Mention what you added in passing ("adding that"), but don't interrupt the conversation. Before every write: re-read the file from disk. Never overwrite — only append (or edit a specific fragment if the user asks).
