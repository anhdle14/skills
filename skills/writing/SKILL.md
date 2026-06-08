---
name: writing
description: Develop raw writing material into fragments, article drafts, or narrative beats without proofreading an existing draft. Use when user wants to ideate, collect fragments, shape notes into an article, write beat-by-beat, or turn raw material into publishable prose.
tags: [writing, create, transform]
args: "<path to raw material or output file (optional)>"
---

# Writing

Use this for pre-draft and drafting work. For proofreading, restructuring, or improving an existing article draft, use `/proofreading`.

Read [REFERENCE.md](REFERENCE.md) for the selected mode before writing.

## Choose Mode

- **Fragments** — user wants to ideate, collect raw material, or avoid structure.
- **Shape** — user has notes/fragments/rough material and wants a publishable article.
- **Beats** — user wants a narrative journey, choose-your-own-adventure style.

If unclear, infer from the user's words. Ask only when choosing the wrong mode would destroy useful work.

## Common Rules

- Preserve the author's phrasing unless the user asks for polish.
- Re-read target files before every write; the user may edit between turns.
- Never overwrite raw material. Shape and beats produce a separate article file.
- Ask once for a save path if none was provided and a file artifact is needed.
- Write incrementally. Do not batch a whole article unless explicitly asked.

## Output

Each turn should either append useful material to the active file or present a small set of choices that moves the piece forward.

Final responses should state the mode used, files touched, what was added, and any remaining gaps.

## Anti-Patterns

- Proofreading an existing draft here instead of using `/proofreading`.
- Imposing an outline during fragment capture.
- Treating all raw material as mandatory.
- Writing ahead after the user chose only one direction.
