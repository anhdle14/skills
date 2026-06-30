# Ship Examples

One end-to-end trace of the four-phase ship workflow, showing the artifacts each phase
writes to `.ship/`, parallel slice fan-out, the verify gate, a logged assumption, and the
review report. Contracts are in [REFERENCE.md](REFERENCE.md); patterns in [PATTERNS.md](PATTERNS.md).

---

## Example — "Add CSV export to the reports page"

### Phase 1 — Plan

A short design doc already exists. Save it as `.ship/csv-export/PLAN.md`. It says: users on
the reports page can download the current report as CSV, respecting active filters.

### Phase 2 — `/skill:ship-grill`

Interview, one question at a time, leading with a recommended answer; explore the codebase
instead of asking whatever the code can answer:

- "Stream the export or build it in memory?" → recommend stream (existing reports can be
  large). Logged as a decision.
- "Which delimiter and encoding?" → recommend `,` + UTF-8 with BOM (Excel-friendly).
- "Does export respect the active filter set?" → yes (from PLAN).
- New term surfaced: "report row" vs "display row" differ when grouping is on → write both
  to `GLOSSARY.md`; record the streaming choice as `decisions/0001-stream-csv-export.md`.

Capture the repo's verify commands (`pnpm typecheck`, `pnpm lint`, `pnpm test`,
`pnpm build`) and write `SPEC.md`: goal, scope (in: filtered export; out: XLSX, scheduled
exports), deliverables, user stories, the single seam (the export service), verify commands,
standards, and a default for every grey area. Self-review the spec for placeholders,
contradictions, scope creep, and ambiguity. Hand the spec to the user to confirm.

### Phase 3 — `/skill:ship-slice`

Read `SPEC.md`. Decompose into vertical tracer bullets and write `SLICES.md` with the graph:

```text
1 export service: filtered rows -> CSV string      (independent)
2 API route: GET /reports/:id/export.csv           (depends on 1)
3 UI: "Export CSV" button wired to the route        (depends on 2)
```

Slice 1 is independent; 2 and 3 sequence after it. There is no second independent slice
here, so the phase is mostly sequential — when a spec yields independent slices, they fan out
in parallel, one subagent each.

For each slice a Worker subagent implements with TDD at the export-service seam, runs the
gates to green, writes `slices/01-export-service/SUMMARY.md`, and commits the code. A
different Verifier subagent checks the artifact against the spec and returns `ACCEPT`.

Grey area hit mid-build: a report with zero rows. The spec did not say, but "empty export =
header row only" is consistent with the streaming decision, so the slicer takes that default,
logs it to `STATE.md` as an assumption, and continues — no pause. No hard blocker arises, so
the phase runs to completion hands-off.

### Phase 4 — `/skill:ship-review`

Goal-backward from the spec: does filtered CSV export actually exist and work? The reviewer
runs the full gates, reads the code (not just the SUMMARYs), and attacks it adversarially. It
writes `REVIEW.md`:

- 🔴 Filter state read from the URL, not the in-memory store — stale on rapid filter change.
- 🟡 No test covers the empty-report assumption logged in STATE.md.
- 🟢 Suggestion: cap export size or paginate for very large reports.

Report back to the user with the prioritized findings.

---

## What this trace demonstrates

- **`.ship/` as the spine** — every phase reads and writes the same on-disk folder.
- **Spec as a complete contract** — grilling resolved grey areas so the build ran hands-off.
- **Vertical slices** — each cuts end to end; independent ones would fan out in parallel.
- **Independent verification** — a different subagent than the producer judged each slice.
- **Logged assumption, not a pause** — a defaultable grey area kept the build moving and
  surfaced in review.
- **Goal-backward review** — the final pass verified delivered behavior, not task counts.
