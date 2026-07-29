---
name: prose-writing
description: Develop raw material into non-technical prose - essays, articles, reports, newsletters, narrative and creative pieces - as fragments, drafts, or beats. Use when the user wants to ideate, collect fragments, shape notes into an article or report, write beat-by-beat, or turn raw material into publishable prose.
tags: [writing, create, transform]
args: "<path to raw material or output file (optional)>"
---

# Prose Writing

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Use this for pre-draft and drafting work on non-technical prose: essays, articles, reports, newsletters, narrative and creative pieces.

- Proofreading, restructuring, or tightening an existing prose draft: `/proofreading`.
- Anything developer-facing - README, API reference, how-to, design doc, runbook, release notes, PR description: `/tech-writing`. Technical prose is judged on verified accuracy before voice, and that skill grounds every claim in a source of truth.

Read [REFERENCE.md](REFERENCE.md) for the selected mode before writing.

## Choose Mode

- **Fragments** — user wants to ideate, collect raw material, or avoid structure.
- **Shape** — user has notes/fragments/rough material and wants a publishable article.
- **Beats** — user wants a narrative journey, choose-your-own-adventure style.

Essays, reports, and analysis pieces use Shape mode; see "Reports and essays" in REFERENCE.md for what changes.

If unclear, infer from the user's words. Ask only when choosing the wrong mode would destroy useful work.

## Common Rules

- Preserve the author's phrasing unless the user asks for polish.
- Never invent a fact, figure, quote, or source to make a passage land. Mark the gap `TODO(unverified)` and keep writing.
- Re-read target files before every write; the user may edit between turns.
- Never overwrite raw material. Shape and beats produce a separate article file.
- Ask once for a save path if none was provided and a file artifact is needed.
- Write incrementally. Do not batch a whole article unless explicitly asked.
- Running non-interactively (batch/AFK): collapse the live offer-pick-grow-react loop into one pass — record the candidate choices and the direction you assume, write on that assumption, and state it in the final response instead of waiting for a turn.

## Output

Each turn should either append useful material to the active file or present a small set of choices that moves the piece forward.

Final responses should state the mode used, files touched, what was added, and any remaining gaps.

## Anti-Patterns

- Proofreading an existing draft here instead of using `/proofreading`.
- Imposing an outline during fragment capture.
- Treating all raw material as mandatory.
- Writing ahead after the user chose only one direction.
