# Technical Writing Reference

Distilled from [Google's Technical Writing courses](https://developers.google.com/tech-writing) (Tech Writing One and Two, Writing Helpful Error Messages, Tech Writing for Accessibility) and the house-style rules in the `google-gemini/gemini-cli` `docs-writer` skill.

## Words

- **Use terms consistently.** Pick one name per concept and never vary it for style. If you rename a thing mid-document, the reader assumes you mean two things.
- **Define new terms** on first use, or link to an existing definition. Never both invent a term and leave it undefined.
- **Acronyms:** spell the full term first, with the acronym in parentheses, then use the acronym only. Define an acronym only if it is significantly shorter *and* appears many times - otherwise repeat the full term.
- **Ambiguous pronouns:** replace `it`, `they`, `this`, `that` with the noun, or place the noun immediately after (`this user ID`). Use a pronoun only when its antecedent is in the same or the previous sentence and unmistakable.
- **Precise verbs:** prefer the specific verb (`generates`, `returns`, `retries`) over `is`/`does`/`happens`. Prefer `lets you` over `allows you to`.
- **Requirement words:** `must` for requirements, `we recommend` for recommendations, `must not` for prohibitions. Avoid `should` - the reader cannot tell whether it is optional.
- **Avoid** Latin abbreviations (`for example` not `e.g.`, `that is` not `i.e.`), `please`, marketing language, idioms, and anthropomorphism (`the server thinks`).

## Sentences

- **Active voice**, present tense, actor first: "The API returns a job ID", not "A job ID is returned". Passive is acceptable only when the actor is genuinely unknown or irrelevant.
- Sentences starting with an imperative verb (`Open the file.`) are active - the implied actor is the reader.
- **One idea per sentence.** A sentence carrying two ideas becomes two sentences, or a sentence plus a list.
- **Convert long sentences into lists.** A sentence enumerating three or more things wants to be a bulleted list; a sentence describing a sequence wants to be a numbered list.
- **Cut filler:** `in spite of the fact that` → `although`; `is able to` → `can`; `determine the location of` → `find`; `at this point in time` → `now`. Delete `there is`/`there are` openings by promoting the real subject.
- Address the reader as **you**. Contractions (`don't`, `it's`) are fine and keep the tone direct.
- Write standard US English for a global audience; avoid cultural references and humor that does not translate.

## Paragraphs

- Open with a **topic sentence** that states the paragraph's point. A reader who reads only topic sentences should still get the argument.
- One topic per paragraph. Move or delete any sentence that belongs to a different topic.
- Answer **what** you are telling the reader, **why** it matters, and **how** they use it (or how they know it is true).
- Keep paragraphs to 3-5 sentences. A one-sentence paragraph is fine; a ten-sentence paragraph is a wall.

## Lists and tables

- **Numbered lists** for sequences, **bulleted lists** for unordered sets. Numbering an unordered set implies a sequence that does not exist.
- **Keep items parallel:** same grammatical form, same capitalization, same punctuation, same voice across every item in one list.
- Start every item of a numbered step list with an **imperative verb**.
- **Introduce every list and table** with a sentence ending in a colon, ideally containing the word *following*: "Take the following steps to install the package:".
- Put **conditions before instructions**: "On the Settings page, click Save", not "Click Save on the Settings page".
- Mark optional steps as `Optional:`.
- Tables earn their place when the same 2+ fields repeat for 3+ items. Give every column a header; keep cells to a few words.

## Documents

- **State scope** ("This document describes...") and **non-scope** ("This document does not cover...") at the top. Restrict non-scope to topics the audience would reasonably expect. If the draft drifts outside the scope statement, either refocus the draft or change the statement.
- **Know your audience:** their role, the knowledge they arrive with, and the single gap the doc closes. Then write to that level. The *curse of knowledge* is the default failure - you forget which of your assumptions is not shared.
- **Key point first (BLUF).** Put the conclusion, the summary, or the answer before the derivation.
- **Task-based headings** name what the reader is doing (`Warm the cache before a deploy`), not the artifact or internal tool (`The carambola CLI`).
- Every heading is followed by an **overview paragraph** before any list, table, or subheading.
- Sentence case for headings and titles. Hierarchical headings that mirror the reader's journey. No hand-maintained table of contents.
- **Navigation** for anything long: an introduction, a summary, logical development, links to related material, and a `Next steps` section.
- Prefer **one source of truth**: link to the canonical explanation rather than restating it, so the two copies cannot diverge.

## Sample code

Good samples are **correct, runnable, concise, and commented**.

- Correct: it compiles or runs as written, and it does what the surrounding prose claims.
- Runnable: state prerequisites (installs, environment variables, auth) before the sample.
- Meaningful names. Never `foo`, `bar`, `baz`, `thing`.
- Comment the **non-obvious** part - the magic constant, the mode flag, the ordering constraint - never what the next line plainly does.
- Show the **expected output**, especially when the sample is hard for the reader to run.
- Keep the sample minimal: nothing in it that the point does not need.

## Illustrations

- **Write the caption first**, then build the illustration to match it. Captions are brief, state the takeaway, and focus attention. By convention the caption follows the figure.
- Use callouts, arrows, or a highlight to direct the eye instead of a paragraph describing which region you mean.
- Provide descriptive `alt` text for every image. Lowercase, hyphenated media filenames.

## Error messages

A good error message tells the reader **what happened, why, and what to do next**.

- Be specific and actionable: name the failing input, the constraint, and the fix.
- No blame, no jargon leakage, no bare error codes as the whole message.
- Identify the object precisely (which file, which field, which limit) so the reader can act without a debugger.
- Match severity to reality: do not warn about the routine or whisper about data loss.

## Formatting and links

- `code font` for filenames, commands, flags, API elements, and literal values. **Bold** for UI elements.
- Descriptive anchor text that makes sense out of context - never `click here` or a bare URL.
- Relative links within a repo's docs so they survive moves. When you rename a heading, grep for deep links to it and update them.
- Unambiguous dates (`January 22, 2026`), serial comma, periods inside quotation marks.
- Callouts (`> [!NOTE]`, `> [!WARNING]`) only for information that would derail the main flow inline.
- Use a collapsible `<details>` block for supplementary or data-heavy material.

## Document-type skeletons

Start from the shape, then delete what the reader does not need.

- **README:** what it is and who it is for → status/stability → install → smallest working example → common tasks → configuration → troubleshooting → contributing/links.
- **How-to guide:** the goal stated as an outcome → prerequisites → numbered steps, each with a verifiable result → verification step → troubleshooting → next steps.
- **Tutorial:** what you will build (with the finished artifact shown first) → setup → staged sections that each run successfully → recap → next steps.
- **API reference:** purpose → auth → endpoint or function signature → parameter table → response schema → status or error table → runnable example with output → limits and quotas.
- **Design doc:** scope and non-scope → context and problem → goals and non-goals → proposal → alternatives considered with the reason each lost → risks → rollout and migration → open questions.
- **Runbook:** the symptom or alert as the title → severity and impact → diagnosis commands with expected output → mitigation steps → verification → escalation path → follow-up.
- **Release notes:** version and date → breaking changes first with migration instructions → new features → fixes → known issues. Written for the upgrader, not the committer.
- **PR description:** what changed and why → the user-visible effect → how it was verified → risk and rollback → linked issue.
- **Docstring or code comment:** what the function does, its contract (parameters, return, errors raised), and the non-obvious *why*. Never restate the signature in prose.

## Review rubric

Review in this order; do not descend a level while the level above is broken.

1. **Correctness** - every claim traceable to code, config, or observed output. Flag unverifiable claims rather than smoothing them.
2. **Completeness** - prerequisites, auth, limits, error paths, and the unhappy path all present.
3. **Scope** - a scope statement exists and the content matches it; nothing off-topic survives.
4. **Structure** - heading order matches the reader's journey; headings are task-based; dependencies precede their dependents; no duplicate or orphan sections.
5. **Paragraphs** - topic sentences carry the argument; one topic each.
6. **Sentences and words** - active voice, one idea per sentence, consistent terms, no ambiguous pronouns, filler cut.
7. **Elements** - lists and tables introduced and parallel; samples runnable with expected output; alt text and link text descriptive.
8. **Mechanics** - `scripts/prose-check.sh` clean or every hit justified.

## Using an LLM on your own draft

Google's guidance, which applies to you as the writer: an LLM is good at first drafts, alternative phrasings, summaries, and format conversion - and it is confidently wrong about facts. Generated text is a starting point that a human with access to the source of truth must verify. Prompts for summaries should state style, audience, purpose, and tone.
