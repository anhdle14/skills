---
name: tech-writing
description: Write or review technical documentation for software and engineering audiences - READMEs, API references, how-to guides for using a system or API, design docs, runbooks, release notes, error messages, PR descriptions - grounded in verified facts and Google's technical writing standards. Use when the user wants to write, draft, edit, review, or improve a developer-facing or engineering document about code, systems, APIs, or infrastructure. Not for personal, ceremonial, or life-event writing (speeches, toasts, invitations, packing or planning guides) even when it uses words like "guide" or "step by step" - use /prose-writing instead.
tags: [writing, engineering, create, transform]
args: "<doc path, topic, or draft to review (optional)>"
---

# Technical Writing

Persistence rule: context is volatile RAM; filesystem is durable disk. Write the outline, open questions, and review findings to files; re-read them before drafting and before claiming done.

Non-technical prose - essays, reports, narrative, creative work - goes to `/prose-writing`. Existing non-technical drafts go to `/proofreading`.

> **Never document behavior you have not verified.** A gap in your knowledge becomes an open question in a file, never a confident sentence in the doc. An invented default, hostname, error string, limit, or field semantic is the one failure a reader cannot detect.

Rules and per-document-type skeletons live in [REFERENCE.md](REFERENCE.md). Read it before drafting or reviewing.

## Choose mode

- **Draft** - new document, or a new section of one.
- **Review** - an existing doc, docstring, or PR description needs editing.

Both modes run steps 1-3; drafting runs 4-5, review runs 6.

## 1. Ground every claim

Name the source of truth before writing a sentence: the code, config, schema, test, or CLI output that proves the behavior. Read it. For repo work, grep the implementation - not just the existing docs, which may already be stale.

Write `docs-notes.md` (beside the target doc, or in `/tmp`) with two lists:

- **Verified** - claim plus the `file_path:line` or command output that proves it.
- **Open questions** - anything the source does not settle.

Do not resolve an open question by guessing. Ask the user, or ship the doc with an explicit `TODO(unverified): <question>` inline. Nothing plausible-but-unchecked enters prose.

Complete when every factual claim you intend to write appears under **Verified**, or is tagged `TODO(unverified)`.

## 2. Fix the audience and the knowledge gap

Write down who reads this, what they already know, and the specific gap the doc closes. Serve that gap by choosing vocabulary and depth for it - do not add an `## Audience` section to the document itself.

Beware the curse of knowledge: list the terms you are about to use that this audience has not met, then define, link, or remove each one.

## 3. State scope, then outline

Draft the scope statement ("This document describes...") and the non-scope ("This document does not cover...", limited to topics the reader would reasonably expect). Then outline task-based headings - name what the reader is trying to accomplish, not the artifact or the tool.

Confirm the outline with the user before drafting anything long. Save it to `docs-notes.md`.

## 4. Draft

Lead with the point (BLUF): the doc, and each section, states its conclusion before its supporting detail. Every heading gets an overview paragraph before any list, table, or subheading.

Apply the sentence and word rules in REFERENCE.md. The four that break most drafts:

- Active voice, present tense, reader as "you", imperative verbs for steps.
- One idea per sentence; split any sentence carrying two.
- Introduce every list and table with a sentence ending in a colon; keep items parallel.
- Replace ambiguous `this`/`that`/`it` with the noun.

Sample code must be correct and runnable, use meaningful names (never `foo`), comment only the non-obvious part, and show the expected output.

Write incrementally, section by section, appending to the file. Do not batch a whole document unless the user asked for it.

## 5. Self-edit

Run `bash scripts/prose-check.sh <file>` for the mechanical rules, then fix what it flags or justify each keep in your report. The script is advisory, not the standard: never contort a sentence just to silence a hit - a justified keep beats a worse sentence.

Then do the judgment pass REFERENCE.md describes: cut every sentence the scope statement does not need, verify the opening's promises are delivered, check terminology is consistent, and re-read as the audience from step 2.

Complete when the check script is clean or every remaining hit is justified.

## 6. Review mode

Read the whole document before commenting. Then, in order: correctness against the source of truth, structure and heading order, then sentence-level polish - never polish sentences while the structure is wrong.

Report findings as a list with `file_path:line`, each carrying the concrete rewrite. Apply edits after the user accepts the direction; for a long doc, confirm the structural findings first.

## Report

State the mode, files touched, what you verified and against which source, what remains `TODO(unverified)`, and the check script result.

## Anti-patterns

| Rationalization | Reality |
|---|---|
| "A plausible default makes the doc more complete." | It makes the doc wrong in a way the reader will trust. Tag it `TODO(unverified)`. |
| "The existing docs say so." | Docs drift from code. The implementation is the source of truth. |
| "I'll note the assumptions in my final response." | The reader never sees your final response. Assumptions belong in the file. |
| "It's obvious what `this` refers to." | It was obvious to the writer. Name the noun. |
| "An `## Audience` section covers the audience." | Serving the audience is a vocabulary and depth choice, not a section. |
| "Rewording it made the checker pass." | The checker serves the reader, not the reverse. If the flagged sentence was clearer, keep it and say why. |
