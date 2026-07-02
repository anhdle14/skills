# Plan: fork plannotator into a new `ship-plan` (Phase 1 of the ship pipeline)

> STATUS: READY FOR REVIEW — all decisions resolved. Option 1 (config override + thin
> skill), strictly Phase 1 → hand to `ship-grill`, three-tier auto-detecting review gate,
> minimal scope + doc/URL/HTML annotation, one-line notice only when degrading below Tier 1.

## Context

The `ship` pipeline (`skills/ship/`) is a four-phase feature workflow:

1. **Plan** — "bring any doc, save as `.ship/<slug>/PLAN.md`". **No skill exists for this phase.**
2. `ship-grill` — interview the plan into a complete `SPEC.md`.
3. `ship-slice` — autonomously build vertical slices.
4. `ship-review` — adversarial review gate.

Phase 1 is the only phase without a skill; the design doc (`plans/vertical-slice-workflow.md`)
explicitly names *"Plannotator (planning mode, no skill)"* as its intended tool. This change
promotes Phase 1 to a first-class `ship-plan` skill that **forks plannotator by forcing it via
prompts** — reusing plannotator's browser review UI when present, and degrading gracefully when
it is not — to produce the reviewed `.ship/<slug>/PLAN.md` that `ship-grill` consumes.

This repo's agents run on **Pi**, and plannotator ships a **Pi extension** whose
`plannotator.json` defines the two-phase model (`planning` → `executing`) this very session is
running under. That config is the fork target — not the whole Bun app.

## What plannotator is (research findings)

Repo: `github.com/backnotprop/plannotator` (cloned at `/tmp/pi-github-repos/backnotprop/plannotator`).
Local, browser-based review surface that plugs into agents via hooks/commands. Runtime: **Bun**.

### Feature catalog

| Feature | What it does | CLI / trigger |
|---|---|---|
| **Plan review** | Agent proposes plan → browser UI → approve / deny-with-annotations / approve-with-notes; blocks until decision. | harness hooks (Claude `ExitPlanMode`, Codex `Stop`, Pi `plannotator_submit_plan`). |
| **Plan versioning / diff** | On resubmission, "Plan Diff" highlights what changed. | automatic |
| **Code review** | Uncommitted changes or remote PRs; line comments; git/jj/p4/GitHub/GitLab. | `plannotator review [--git] [PR_URL]` |
| **Annotate** | Any markdown/text/HTML file, URL, or folder. `--gate` = Approve button; `--json`/`--hook` = structured decision; `--markdown` converts HTML (raw by default). | `plannotator annotate <path\|url\|folder> [--markdown]` |
| **Annotate-last** | Annotate the agent's last message. | `plannotator annotate-last` |
| **AI-in-the-loop** | Ask AI about what you're reviewing; AI reviews post diff comments. | in-UI |
| **Sharing / multiplayer** | Share plan+annotations via URL (hash or encrypted short-link); import teammate feedback. Disable via `PLANNOTATOR_SHARE=disabled`. | `room.plannotator.ai` |
| **Archive / sessions** | Read-only browser of saved decisions; list/reopen sessions. | `plannotator archive` / `sessions` |
| **improve-context / setup-goal** | Inject planning context; goal interview / facts UI. | hooks / `setup-goal` |

### Decision contract & Pi extension

- Plan review stdin: hook event JSON (`tool_input.plan`); stdout: `{"decision":"approved|dismissed|annotated","feedback":"..."}`.
- Pi config merge (project wins): built-in `plannotator.json` → `~/.pi/agent/plannotator.json` → `<cwd>/.pi/plannotator.json`.
  A project override can fully replace `phases.planning.{systemPrompt, activeTools, statusLabel, model, thinking}`.
- Planning phase default `activeTools`: `grep, find, ls, plannotator_submit_plan`; markdown-only writes.
- Prompt template vars: `${planFilePath}`, `${todoList}`, `${completedCount}`, `${totalCount}`, `${remainingCount}`, `${phase}`.
- Shared event API: `plannotator:request` action `plan-review` / `annotate` for programmatic use.

## Approach (DECIDED — Option 1: config override + thin skill, no code fork)

"Fork" = force plannotator into the ship workflow via **prompts/config**, plus a portable
prose skill. Two artifacts, shipped in the skill folder for portability:

1. **`skills/ship-plan/plannotator.json`** (a *template*, not live config — data, not code, so
   the "ships no executable" invariant holds). Overrides `phases.planning.systemPrompt` (and
   `statusLabel`) to be ship-aware: write `.ship/<slug>/PLAN.md`, follow the ship layout, end by
   handing off to `/skill:ship-grill` instead of jumping to an `executing` phase.
   - **Why a template, not a live `.pi/plannotator.json`:** `.pi/` is gitignored here, and this
     is a *portable* skills collection — when installed into another project the config must
     live in *that* project's `.pi/`. Activation is a documented one-time copy step
     (`<project>/.pi/plannotator.json` for project scope, or `~/.pi/agent/plannotator.json`
     for global). For dogfooding in THIS repo, optionally add `!.pi/plannotator.json` to
     `.gitignore` so the activated config can be committed.
2. **`skills/ship-plan/SKILL.md`** (human-only, ≤100 lines, portable prose) — the pipeline-facing
   Phase-1 entry point. Drives the plan-authoring loop and selects the review gate by
   auto-detection, so it works with OR without plannotator.

### Three-tier review gate (auto-detect, prefer highest)

Mirrors the pipeline's Tier A/B substrate ("use the highest tier your agent actually supports",
`ship/REFERENCE.md`). Probe in order; use the best available; print a one-line notice ONLY when
below Tier 1:

| Tier | Precondition | Review gate | Driven by |
|---|---|---|---|
| **1 native** | `plannotator_submit_plan` tool available (Pi extension active) | browser annotate + approve/deny + plan-diff on resubmit | activated `.pi/plannotator.json` + `plannotator_submit_plan` |
| **2 CLI** | `plannotator` binary on PATH | `plannotator annotate .ship/<slug>/PLAN.md --gate --json` → browser gate + structured feedback | skill shells out |
| **3 in-chat** | nothing installed | write `PLAN.md`, ask user to review in chat, iterate to approval | pure prose, any agent |

Probe: `plannotator_submit_plan` present → Tier 1; else `command -v plannotator` → Tier 2; else
Tier 3. Never ask the user which tier. Notice example when degrading: *"plannotator not detected
— using in-chat review gate"*.

### Scope (minimal + planning-time annotation)

- **In:** the core plan-authoring loop; the three-tier review gate; plan-diff on resubmit (free at
  Tier 1); **pulling arbitrary docs / URLs / HTML into the annotate UI during planning** as a
  reference aid (`plannotator annotate <path|url> [--markdown]`, Tier 1/2 only — noted as
  unavailable at Tier 3).
- **Out:** code review of diffs/PRs, annotate-last, sharing/multiplayer, setup-goal — separate
  concerns, not part of Phase-1 planning.

### Placement — strictly Phase 1

`ship-plan` produces a reviewed `PLAN.md`, then hands off to `/skill:ship-grill` (which still does
the deep interview → `SPEC.md`). No overlap with grill; the pipeline stays four phases.

## Files to create / modify

**Create**

- `skills/ship-plan/SKILL.md` — human-only Phase-1 skill (frontmatter, persistence rule, the plan
  loop, the three-tier gate + detection, doc/URL/HTML annotation aid, handoff to grill,
  anti-patterns). ≤100 lines; no `20xx` strings.
- `skills/ship-plan/plannotator.json` — the ship-aware planning-phase config template.
- `skills/ship-plan/REFERENCE.md` (only if SKILL.md would exceed 100 lines) — the full tier
  detection contract, the config template rationale, and activation instructions.

**Modify**

- `skills/ship/SKILL.md` — "The four phases" §: Phase 1 becomes `/skill:ship-plan` (not "no
  skill"); update the Phase-1 fallback and the routing narrative. Keep ≤100 lines.
- `skills/ship/REFERENCE.md` — resume-detection contract: `no PLAN.md` → route to `ship-plan`
  (currently "confirm/create PLAN.md, then ship-grill"). Update the routing table row.
- `AGENTS.md` — add the `ship-plan` row to the skills index; update the ship-family paragraph;
  regenerate the index block between `<!-- skills-index-start -->` / `-end -->`.
- `README.md` — add `ship-plan` to the human-only skills listing.
- `.gitignore` — (optional, dogfooding only) `!.pi/plannotator.json` to allow committing the
  activated config in this repo.

**Not touched**

- No trigger-eval cases needed (human-only skills are exempt, per validator + AGENTS conventions).
- No `docs/evals` changes required.

## Reuse

- Ship contracts: `skills/ship/REFERENCE.md` (`.ship/` layout, resume-detection, Tier A/B framing).
- plannotator Pi config schema: `apps/pi-extension/plannotator.json` + `config.ts` (merge layers,
  overridable fields, template vars) — basis for the config template.
- plannotator CLI: `annotate --gate --json`, `--markdown` (verified in `apps/hook/server/cli.ts`; HTML renders raw by default).
- Existing ship skill prose conventions (persistence rule line, anti-patterns, human-only frontmatter).

## Steps

- [x] Write `skills/ship-plan/plannotator.json` — ship-aware `phases.planning.systemPrompt`
      (writes `.ship/<slug>/PLAN.md`, hands to `ship-grill`) + `statusLabel`.
- [x] Write `skills/ship-plan/SKILL.md` — plan loop + three-tier gate + detection + annotation
      aid + grill handoff + anti-patterns (≤100 lines, persistence rule, no `20xx`).
- [x] Split overflow into `skills/ship-plan/REFERENCE.md` if needed (tier contract, activation).
- [x] Update `skills/ship/SKILL.md` (Phase 1 = ship-plan) and `skills/ship/REFERENCE.md`
      (routing table: no PLAN.md → ship-plan).
- [x] Update `AGENTS.md` (index row + ship paragraph), `README.md`, and `skills/router/SKILL.md`.
- [x] Add `!.pi/plannotator.json` to `.gitignore` for dogfooding.
- [x] `deno task validate` and `make lint`.

## Verification

- [x] `deno task validate` passes (13 skills; frontmatter, ≤100 lines, persistence rule, kebab
      name, no `20xx`, valid tags, quoted args).
- [x] `make lint` (markdownlint) passes on SKILL.md / AGENTS.md / README.md.
- [x] Router walk-through wired: empty `.ship/` → routing table + Phase-1 fallback → `ship-plan`
      → reviewed `PLAN.md` → `/skill:ship-grill`.
- [x] Tier detection prose ordered correctly (Tier 1 `plannotator_submit_plan` → Tier 2
      `command -v plannotator` → Tier 3 in-chat) with degrade notices only below Tier 1.
- [x] Config template planning phase writes `.ship/<slug>/PLAN.md` and hands to grill; executing
      phase hands off without implementing (verified by inspection).
- [x] `grep -rn "no skill" skills/ship/` → none; Phase 1 no longer described as skill-less.
