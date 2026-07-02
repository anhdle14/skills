# Plan: make `/skill:ship` auto-resume or start from scratch

## Context

Today `/skill:ship` (`skills/ship/SKILL.md`) is a pure index + handoff contract. Its
"Running the pipeline" section tells the operator to *manually* invoke each phase in order
(`ship-grill` → `ship-slice` → `ship-review`). It does **not** inspect the durable
`.ship/<feature-slug>/` artifacts to figure out where a run left off. So re-running
`/skill:ship` after a break does nothing useful — the operator has to remember which phase
they were in and invoke it by hand.

The user wants: run `/skill:ship` and it **either auto-continues from the last run or walks
the operator from the start** — a single self-orienting entry point.

The reference fix (<https://github.com/open-gsd/gsd-core>, installed here under `.pi/gsd/`)
solves the same problem with a **detect-state-then-route** pattern:

- `next.md` — reads project state, applies routing rules (discuss→plan→execute→verify→
  complete), and immediately advances with zero friction.
- `resume-project.md` / `resume-work.md` — restore context, present a status card, detect
  incomplete work, and offer contextual next actions.

## Approach (recommended)

Port the gsd-core routing pattern into `skills/ship/SKILL.md` as a **state-detection +
routing preamble**, expressed in prose (NOT an executable — the pipeline deliberately ships
no script; REFERENCE.md).

`/skill:ship [arg]` becomes:

1. **Locate the feature.** Resolve the target `.ship/<feature-slug>/` from the arg, or
   discover existing slugs under `.ship/`.
2. **Detect the phase** from which artifacts exist (PLAN.md / SPEC.md / SLICES.md+STATE.md /
   REVIEW.md) and STATE.md contents (DONE, open blockers, incomplete slices).
3. **Route** to the correct next phase — resume mid-pipeline, or start from Phase 1 (create
   PLAN.md → grill) when nothing exists.

### Resolved design decisions

- **Friction: present, then confirm.** `/skill:ship` prints a status card + the recommended
  `▶ Next Up` command and **waits** for the operator (`y` / edit / different feature). It
  never auto-launches a phase. Preserves the current "between phases the human decides"
  principle.
- **Handoff: emit the exact command.** It does *not* execute the next phase inline. It prints
  the precise `/skill:ship-<phase> <slug>` command with a `/new first → fresh context window`
  hint, matching gsd-core's fresh-context guidance and keeping each phase isolated.
- **Multi-feature: only auto-resume when exactly one.** No arg + one in-flight `.ship/<slug>/`
  → resume it. No arg + several → list each with its detected phase and ask which. No arg +
  none → start Phase 1.

### Status card + handoff format (target)

```text
╔═ SHIP STATUS ═════════════════╗
 Feature: csv-export
 Phase 2 of 4 — SPEC.md written
 Blockers: none
╚═══════════════════════════════╝

▶ Next Up
/skill:ship-slice csv-export
(/new first → fresh context window)

Proceed?  y  ·  edit PLAN/SPEC  ·  different feature
```

### Resume-detection contract (deterministic markers)

Routing must not depend on prose parsing. Formalize in REFERENCE + emitted by ship-slice:

- `STATE.md` carries a `## Status` block; completion writes a final line `Overall: DONE`.
- `## Open blockers` listing anything other than `(none)` → still in Phase 3 (resume slice).
- Artifact presence is the primary signal; STATE markers disambiguate slice-in-progress vs.
  slice-done.

### Routing table (artifact presence → next action)

| Detected state | Next action |
|---|---|
| No `.ship/` or no `<slug>/PLAN.md` | Phase 1: confirm/create `PLAN.md`, then `ship-grill` |
| `PLAN.md`, no `SPEC.md` | Phase 2: `/skill:ship-grill` |
| `SPEC.md`, no `SLICES.md`/`STATE.md` | Phase 3: `/skill:ship-slice` (fresh) |
| `SLICES.md`+`STATE.md`, not DONE / open blockers | Phase 3: `/skill:ship-slice` (resume from STATE.md) |
| `STATE.md` overall DONE, no `REVIEW.md` | Phase 4: `/skill:ship-review` |
| `REVIEW.md` present | Report complete; offer re-review or new feature |

## Files to modify

- `skills/ship/SKILL.md` — replace the "Running the pipeline" section with the detect →
  status-card → route entry logic + routing table. Update the description/frontmatter to
  reflect the new single-entry-point behavior. Keep under ~100 lines (repo convention).
- `skills/ship/REFERENCE.md` — formalize the `STATE.md` `## Status` / `Overall: DONE` marker
  and the "resume-detection contract" so routing is deterministic.
- `skills/ship-slice/SKILL.md` — ensure the build always writes the deterministic
  `Overall: DONE` marker to `STATE.md` on completion (it already writes final progress; make
  the marker explicit).
- `AGENTS.md` — refresh the `ship` row/description to "single self-orienting entry point that
  resumes or starts" (and regenerate the skills index if metadata changed).

## Reuse

- gsd-core routing rules: `.pi/gsd/workflows/next.md` (Route 1–8), `.pi/gsd/workflows/
  resume-project.md` (status card, incomplete-work detection, quick-resume).
- Existing `.ship/` schema + STATE.md schema already defined in `skills/ship/REFERENCE.md`.
- STATE.md status conventions seen in real runs (e.g. `## Status`, `Overall: DONE`,
  `## Open blockers`).

## Steps

- [x] In `skills/ship-slice/SKILL.md`, make the completion step write a deterministic
      `## Status` block ending with `Overall: DONE` to `STATE.md`.
- [x] In `skills/ship/REFERENCE.md`, add the "Resume-detection contract": artifact→phase
      mapping and the `Overall: DONE` / `## Open blockers` markers.
- [x] In `skills/ship/SKILL.md`, replace "Running the pipeline" with:
  - [x] Step A — locate feature (arg, else scan `.ship/`; apply the one-vs-many rule).
  - [x] Step B — detect phase from artifacts + STATE.md markers (routing table).
  - [x] Step C — print the status card + `▶ Next Up` command, then wait for confirmation.
  - [x] Step D — Phase 1 fallback: when nothing exists, walk the operator from creating
        `PLAN.md` through to `/skill:ship-grill`.
- [x] Update `skills/ship/SKILL.md` frontmatter description to the single-entry-point wording.
- [x] Update `AGENTS.md` ship description; regenerate skills index if needed.
- [x] Run `deno task validate`.

## Verification

- [x] `deno task validate` passes (frontmatter/structure, <100-line SKILL).
- [x] Manual walk-through against the existing fixtures — each routes to the correct phase:
  - `.skill-eval/runs/ship/.ship/csv-export/` (PLAN only) → `/skill:ship-grill csv-export`.
  - `.skill-eval/runs/ship-grill/.ship/csv-export/` (has GLOSSARY/SPEC) → `/skill:ship-slice`.
  - `.skill-eval/runs/ship-slice/.ship/clearCompleted/` (STATE `Overall: DONE`) →
    `/skill:ship-review clearCompleted`.
  - `.skill-eval/runs/ship-review/.ship/csv-export/` (REVIEW.md present) → report complete.
- [x] No-arg with multiple slugs → lists them and asks; with exactly one → resumes it;
      with none → starts Phase 1.
- [x] Confirm no executable was added (pipeline ships no script — REFERENCE invariant).
