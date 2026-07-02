# Ship Reference

Shared contracts for every phase of the ship workflow: the `.ship/` layout and file
schemas, the subagent substrate, vertical-slice rules, the verify loop, gates, the
hard-blocker protocol, budgets, and the commit policy. Phase `SKILL.md` files cross-
reference this so none of them re-derive it. The pattern catalog is in [PATTERNS.md](PATTERNS.md).

---

## The `.ship/` directory (durable disk, gitignored)

Context is volatile RAM; `.ship/` is the durable disk and the only channel that carries
state between phases and between subagents. Everything the workflow produces lives here;
only the actual feature **code** is committed to the project. `.ship/` is gitignored.

```text
.ship/<feature-slug>/
├── PLAN.md          # phase 1 (ship-plan): the reviewed plan doc (any format)
├── SPEC.md          # phase 2: the handoff contract (schema below)
├── GLOSSARY.md      # phase 2: domain terms, created lazily
├── decisions/       # phase 2: ADRs (NNNN-title.md), created lazily
├── SLICES.md        # phase 3: slice breakdown + dependency graph + phase grouping
├── STATE.md         # phase 3: progress, decisions log, logged assumptions, open blockers
├── slices/<NN>-<slug>/
│   ├── PLAN.md      #   task list for the slice
│   ├── PROGRESS.md  #   checkboxes, updated as tasks complete
│   └── SUMMARY.md   #   what actually shipped (written by the implementing subagent)
└── REVIEW.md        # phase 4: prioritized issues + improvements
```

Re-read the relevant files before any decision and before any done check.

### Resume-detection contract (how `/skill:ship` orients)

`/skill:ship` is a single self-orienting entry point: it reads the durable artifacts under
`.ship/<feature-slug>/` to decide whether to resume a run or start one, then routes to the
correct phase. Routing must be deterministic — driven by artifact presence and explicit
markers, never by parsing prose. The contract:

- **Artifact presence maps to phase.** `PLAN.md` → Phase 1 (`ship-plan`) done; `SPEC.md` → grill done;
  `SLICES.md` + `STATE.md` → slice started; `REVIEW.md` → review done.
- **`STATE.md` carries a `## Status` block.** The autonomous build writes a final line
  exactly `Overall: DONE` when every slice is accepted. Its absence means the slice phase is
  still in progress (resume `ship-slice`).
- **`## Open blockers`** lists `(none)` when clear, or the blocker(s) otherwise. Anything
  other than `(none)` keeps the run in Phase 3.

| Detected state | Next phase |
|---|---|
| No `.ship/` or no `<slug>/PLAN.md` | Phase 1: `ship-plan` (author + review `PLAN.md`), then `ship-grill` |
| `PLAN.md`, no `SPEC.md` | Phase 2: `ship-grill` |
| `SPEC.md`, no `SLICES.md`/`STATE.md` | Phase 3: `ship-slice` (fresh) |
| `SLICES.md`+`STATE.md`, no `Overall: DONE` or open blockers | Phase 3: `ship-slice` (resume from `STATE.md`) |
| `STATE.md` `Overall: DONE`, no `REVIEW.md` | Phase 4: `ship-review` |
| `REVIEW.md` present | Complete; offer re-review or a new feature |

---

### SPEC.md schema (the handoff contract)

The spec must be complete enough that the autonomous phase needs nothing else:

- **Goal** — what shipping this delivers, from the user's perspective.
- **Scope & boundaries** — explicitly in and explicitly out.
- **Deliverables** — the concrete artifacts that must exist when done.
- **User stories / behaviors** — extensive; the externally observable behavior.
- **Seams** — where the feature is tested; prefer the fewest, highest seams.
- **Verify commands** — the exact typecheck / lint / test / build commands for this repo.
- **Standards** — conventions, ADRs, and quality bars the code must meet.
- **Grey-area defaults** — the decided answer for every choice the slicer might otherwise
  have to guess.

---

## Subagent substrate (tool-agnostic)

A "subagent" is any isolated unit of work. Use the **highest tier your agent actually
supports**; never assume one you cannot confirm.

- **Tier A — real subagents.** If your agent can spawn subagents or select a model per call,
  dispatch each slice (and each verify) to its own subagent. This gives true isolation and
  real parallel fan-out. A verifier subagent must be a *different* instance than the
  producer and must not see the producer's private reasoning — only the artifact and the
  spec.
- **Tier B — single-context role-play.** If only one context is available, play each role in
  sequence yourself. **Write every artifact to a file under `.ship/`** and have the next
  role read that file, not your working memory. The file boundary is what keeps a verifier
  from rubber-stamping its own work.

Dispatch is a reasoning judgment, not a script — this skill ships no executable.

---

## Vertical-slice rules

Slice the spec into **tracer bullets**, not horizontal layers:

- Each slice cuts a narrow but COMPLETE path through every layer (data, logic, interface,
  tests) end to end.
- A finished slice is demoable or verifiable on its own.
- Any prefactoring ("make the change easy, then make the easy change") is its own first slice.
- The dependency graph is explicit: disjoint slices fan out in parallel; a slice that reads
  another's output sequences after it. Group independent slices into phases that run
  without blocking each other.

---

## The verify loop (earned correctness per slice)

Each slice passes through three roles before it is trusted. Bind one subagent to one role:

- **Worker** — implements the slice; does TDD at the spec's seams where a test framework
  exists; produces the artifact and a SUMMARY. Does not judge its own output.
- **Verifier** — a *different* subagent. Sees the artifact + the spec, NOT the worker's
  reasoning. Returns exactly `ACCEPT` or `REVISE: <specific defect and fix direction>`.
  Verifies the slice's GOAL is met, not just that tasks ran.
- On `REVISE`, feed the diagnosis back and retry (prefer a different worker). On `ACCEPT`,
  the slice is done.

## Gates (definition of "green")

Auto-detect the repo's gates and run them for every slice; prefer the spec's explicit verify
commands when present. Typical detection:

- typecheck / compile (e.g. `tsc`, `cargo check`, `go build`)
- lint (e.g. eslint, ruff, golangci-lint) and formatting
- tests (run the slice's tests continuously; the full suite once at phase end)
- build, when the repo defines one

A slice is green only when every applicable gate passes.

---

## Hard-blocker protocol (when to pause)

The autonomous phase is hands-off. Pause and report ONLY on a hard blocker:

1. A slice cannot reach green after the retry cap.
2. A decision is required that the spec does not answer (and cannot be safely defaulted).
3. Two consecutive retries fail with the **same** diagnosis (no progress).

Otherwise keep going. For a defaultable grey area, choose the spec-consistent default, **log
the assumption to STATE.md**, and continue — `ship-review` will surface it. On any pause,
write the blocker to STATE.md with enough context to resume cold.

## Budgets

Keep a per-slice retry cap (default 3) and a small global turn budget. A retry that does not
change the diagnosis is not progress — stop and escalate rather than loop forever.

---

## Commit policy

**Commit outcomes, not process.** The git log reads like a changelog of what shipped, not a
diary of planning. Commit one logical change per completed slice (or per task within it).
Never commit `.ship/` — it is gitignored. Run the gates before committing.
