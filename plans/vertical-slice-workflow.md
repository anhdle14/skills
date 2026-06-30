# Plan: `ship` — GitHub-local vertical-slice feature workflow

## Context

Add an agentic workflow to this skills repo that drives a new feature from idea to
shipped, locally-committed vertical slices with minimal human babysitting. Four
human-invocable phases, wrapped by one orchestrator skill. The old `orchestrate` and
`trinity` skills are deleted; their pattern catalog and verify-loop are folded into the
new `ship` family.

The pipeline:

1. **Plannotator** (planning mode, no skill) — create the first plan doc.
2. **`/skill:ship-grill`** — relentless interview that makes the doc match the user's real
   answers, builds glossary/ADRs, and emits the spec(s) the autonomous phase needs.
3. **`/skill:ship-slice`** — autonomously slice the spec into vertical tracer bullets, run
   them in phases without blocking, fan out as many subagents as needed. Hands-off; pause
   only on hard blockers.
4. **`/skill:ship-review`** — deep review of the deliverables (goal-backward + quality),
   report back.

All four are human-only; the agent never auto-triggers them. `/skill:ship` is the
orchestrator/index that explains the pipeline and hands off between phases.

## Decisions (resolved with user)

- **Packaging:** `ship` orchestrator + `ship-grill` / `ship-slice` / `ship-review`, all
  `disable-model-invocation: true`. **Delete `orchestrate` + `trinity`**, fold their
  patterns into `ship`.
- **"GitHub" = fully local:** no `gh`/issues/PRs. A **gitignored `.ship/` folder** is the
  context-passing channel between phases and subagents. Only feature **code** is committed.
- **Artifacts:** everything (plan, spec, slice plans, progress, review) lives under
  `.ship/`; nothing workflow-related is committed.
- **Autonomy:** fully hands-off; **pause only on hard blockers**.
- **Done bar:** `ship-slice` runs each slice to green via **auto-detected gates**
  (typecheck/lint/test/build) + **TDD at seams**; `ship-review` does **goal-backward
  verification against the spec + a quality/standards pass**.

## Constraints (from this repo)

- Portable skills collection: `skills/<name>/SKILL.md`, consumed by any agent. Validator
  (`scripts/validate-skills.ts`) enforces, per **SKILL.md only**:
  - ≤ 100 lines; must contain the exact persistence rule string; `name` kebab-case and ==
    folder name; valid `tags`; `args` quoted; no `20xx` years.
  - Human-only skills are **exempt** from the "Use when …" two-sentence description rule
    and need **no trigger eval cases** (confirmed: today's `orchestrate`/`trinity` have none).
- `REFERENCE.md` / `PATTERNS.md` / `EXAMPLES.md` are **not** validated → free of the
  line/persistence limits; fold long content there.
- `.pi/gsd/` is gitignored (external reference framework), not a dependency.

## Reuse (existing assets, folded into `ship`)

- `skills/orchestrate/PATTERNS.md` — the 6-pattern catalog → moves to `skills/ship/PATTERNS.md`.
  `ship-slice` composes **Fan Out and Synthesize** + **Loop Until Done**; `ship-review`
  composes **Adversarial Verification**.
- `skills/orchestrate/REFERENCE.md` — worker-pool **Tier A/B** (real subagents vs
  single-context role-play), routing, recursion/budget rules → fold into `skills/ship/REFERENCE.md`.
- `skills/trinity/` — **Thinker-Worker-Verifier** verify-before-trust loop → becomes
  `ship-slice`'s per-slice verify gate and `ship-review`'s adversarial pass.
- `skills/research/` — grill→design→spec→self-review discipline → basis for `ship-grill`
  (one question at a time, recommend an answer, explore code instead of asking; placeholder/
  consistency/scope/ambiguity self-review of the spec).
- Builtin subagents: `worker` (context: fork), `reviewer`, `scout`, `planner`.
- GSD reference ideas (`.pi/gsd/`): autonomous phase loop, **goal-backward verification**,
  "commit outcomes not process", non-blocking parallel phases.

## Approach

A tightly-coupled skill family under `skills/`. Shared operational contracts live once in
`skills/ship/REFERENCE.md` + `skills/ship/PATTERNS.md`; each phase `SKILL.md` is
self-contained for its phase and cross-references those (same pattern as router→orchestrate
today). All phase skills are human-only.

### `.ship/` layout (gitignored, context-passing channel)

```
.ship/<feature-slug>/
├── PLAN.md          # phase 1 (Plannotator) output
├── SPEC.md          # phase 2: scope, boundaries, deliverables, user stories,
│                    #          verify commands/standards, seams
├── GLOSSARY.md      # phase 2: domain terms (created lazily)
├── decisions/       # phase 2: ADRs (created lazily)
├── SLICES.md        # phase 3: vertical-slice breakdown + dependency graph + phase grouping
├── STATE.md         # phase 3: progress, decisions log, logged assumptions, blockers
├── slices/<NN>-<slug>/{PLAN,PROGRESS,SUMMARY}.md   # phase 3: per-slice
└── REVIEW.md        # phase 4: prioritized issues + improvements report
```

### Phase behaviour

- **`ship` (orchestrator, human-only):** explains the 4-phase pipeline, the `.ship/` layout,
  the subagent tiers, budgets, and hard-blocker protocol; tells the human which phase to
  invoke next. The router/index for the family.
- **`ship-grill`:** load PLAN.md; interview relentlessly (one question at a time, lead with
  a recommended answer, explore the codebase instead of asking when answerable); actively
  build GLOSSARY/ADRs; capture the project's exact verify commands + standards; resolve every
  grey area so the spec is a complete handoff contract; write SPEC.md and self-review it
  (placeholder/consistency/scope/ambiguity scan). Stop when the spec needs nothing more.
- **`ship-slice` (autonomous):** read SPEC; decompose into tracer-bullet vertical slices
  (each cuts through all layers, demoable); build the dependency graph; group independent
  slices into non-blocking phases. Per phase, fan out subagents (Tier A `worker`; Tier B
  role-play fallback) — disjoint slices in parallel, one slice per subagent — each implements,
  does TDD at seams, runs auto-detected gates to green, commits outcomes (not process), writes
  SUMMARY. A *different* agent verifies each slice goal-backward. Re-read SLICES/STATE after
  each phase. **Pause only on a hard blocker** (can't reach green after the retry cap; a
  decision missing from the spec; two identical consecutive failures). Otherwise keep going,
  logging any grey-area assumption to STATE.
- **`ship-review` (deep review):** scan all deliverables; goal-backward verify the code
  delivers what SPEC promised (don't trust SUMMARYs); run full gates; adversarial quality pass
  (security, edge cases, dead code, missing tests, architecture smells). Write a prioritized
  REVIEW.md and report back.

## Files to create / modify / delete

**Create**

- `skills/ship/SKILL.md` — orchestrator/index (human-only).
- `skills/ship/PATTERNS.md` — pattern catalog (moved from orchestrate, reframed for ship).
- `skills/ship/REFERENCE.md` — `.ship/` schemas, subagent Tier A/B, verify-gate auto-detect,
  TDD-at-seams, hard-blocker protocol + stop conditions, budgets, git "commit outcomes" policy.
- `skills/ship/EXAMPLES.md` — one worked end-to-end trace.
- `skills/ship-grill/SKILL.md`
- `skills/ship-slice/SKILL.md`
- `skills/ship-review/SKILL.md`

**Modify**

- `.gitignore` — add `.ship/`.
- `skills/router/SKILL.md` — drop orchestrate/trinity rows; add the ship family; repoint the
  PATTERNS.md reference to `skills/ship/PATTERNS.md`.
- `AGENTS.md` — skills index table, "Engineering Stack" + human-only paragraph, and the
  tbench note (mark the orchestrate+trinity benchmark as historical).
- `README.md` — human-only skills table.
- `docs/evals.md` — drop orchestrate/trinity rows (regenerate or hand-edit).

**Delete**

- `skills/orchestrate/` and `skills/trinity/` (entire folders).

**Untouched / historical**

- `docs/evals/tbench/RESULTS.md` — keep as historical record; add a one-line note that the
  workflow was superseded by `ship`. No trigger eval cases needed (all ship skills human-only).

## Frontmatter shape (each ship skill)

```yaml
---
name: ship            # matches folder; ship-grill / ship-slice / ship-review
disable-model-invocation: true
description: <one sentence; no "Use when" needed for human-only>
tags: [plan, engineering, productivity]
args: "<feature description or .ship/<feature> path (optional)>"
---
```

Each `SKILL.md` opens with the exact persistence-rule line and stays ≤ 100 lines.

## Steps

- [ ] Add `.ship/` to `.gitignore`.
- [ ] Create `skills/ship/` (SKILL.md + PATTERNS.md + REFERENCE.md + EXAMPLES.md), folding in
      orchestrate's PATTERNS + worker-tier/budget reference and trinity's verify-loop.
- [ ] Create `skills/ship-grill/SKILL.md` (grill + spec + glossary/ADRs + self-review).
- [ ] Create `skills/ship-slice/SKILL.md` (slice → phases → fan-out subagents → verify → blockers).
- [ ] Create `skills/ship-review/SKILL.md` (goal-backward + adversarial quality → REVIEW.md).
- [ ] Delete `skills/orchestrate/` and `skills/trinity/`.
- [ ] Update `skills/router/SKILL.md`, `AGENTS.md`, `README.md`, `docs/evals.md`; note tbench
      RESULTS.md as historical.
- [ ] Verify (below).

## Verification

- [ ] `deno task validate` passes (frontmatter, ≤100 lines, persistence rule, no orphan refs).
- [ ] `make lint` (markdownlint) passes on README/AGENTS/all SKILL.md.
- [ ] `grep -rn "orchestrate\|trinity" skills/ AGENTS.md README.md docs/evals.md` returns only
      intentional/historical mentions (no dangling index rows or broken links).
- [ ] Dry-run the pipeline on a tiny sample feature: Plannotator → `/skill:ship-grill` writes
      `.ship/<f>/SPEC.md` → `/skill:ship-slice` produces slices + a committed code change with
      green gates → `/skill:ship-review` writes `.ship/<f>/REVIEW.md`. Confirm `.ship/` is
      gitignored and only code was committed.
