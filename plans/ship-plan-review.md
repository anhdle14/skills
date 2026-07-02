# Review: `ship-plan` skill (Phase 1 of the ship pipeline)

Reviewed against `plans/ship-plan.md` (the spec) — deliverables `skills/ship-plan/{SKILL.md,REFERENCE.md,plannotator.json}` and the wiring edits to `skills/ship/`, `AGENTS.md`, `README.md`, `skills/router/SKILL.md`, `.gitignore`.

## Gate verdict: 🟢 GREEN

No `error` remains; the one real defect was `auto-fix`-class and has been fixed and re-verified. No `ask-user` findings.

## Check 1 — goal-backward verification

Every plan promise traced to code and confirmed:

- **plannotator.json** — planning phase writes `.ship/<slug>/PLAN.md` and ends by handing to `/skill:ship-grill`; executing phase hands off without implementing (uses valid `${planFilePath}`/`${todoList}` template vars per `config.ts`). ✓
- **SKILL.md** — 89 lines (≤100), persistence rule present, no `20xx`, three-tier gate ordered Tier 1 `plannotator_submit_plan` → Tier 2 `command -v plannotator` → Tier 3 in-chat, degrade notices only below Tier 1, grill handoff, anti-patterns. ✓
- **REFERENCE.md** — full tier contract, config-template rationale, activation steps, `.pi/` gitignore note. ✓
- **Wiring** — `ship/SKILL.md` Phase 1 = `ship-plan`; `ship/REFERENCE.md` routing row `no PLAN.md → ship-plan`; index/router/README rows added; `.gitignore` `!.pi/plannotator.json`. ✓
- **Gates** — `deno task validate` (13 skills), `make lint`, `rg "no skill" skills/ship/` → none. ✓
- **Tier 2 command** — `plannotator annotate <path> --gate --json` verified against `apps/hook/server/cli.ts` usage. ✓

## Check 2 — adversarial attack

### 🟡 warning · `auto-fix` (APPLIED) — fabricated `--render-html` flag

`SKILL.md`, `REFERENCE.md`, and `plans/ship-plan.md` documented a `--render-html` flag for the planning-time annotation aid and claimed it was "verified in cli.ts". The real plannotator CLI has **no such flag**: `plannotator annotate` supports `--markdown`, and HTML is rendered **raw by default** — the delivered docs both invented the flag name and inverted the semantics. An agent following this at Tier 1/2 would run an unknown flag.

- **Fix applied:** replaced with `[--markdown]` and corrected the description ("HTML renders raw by default; `--markdown` converts it") in all three files.
- **Verified:** `rg render-html` → none; validate + lint re-run green.

### 🟢 info · `no-op` — `activeTools` whitelist omits `read`/`write`/`edit`/`bash`

The planning phase `activeTools` is `["grep","find","ls","plannotator_submit_plan"]`, yet the systemPrompt tells the agent it has `read/write/edit/bash`. `config.ts` `resolveTools` treats `activeTools` as a replacing whitelist, so this looked like it could block writing `PLAN.md`. **Not a defect:** the list is byte-identical to plannotator's own built-in planning config, which functions (its built-in prompt also describes writing markdown) — the extension supplies core tools as always-on and `activeTools` gates only the additional restricted set. The deliverable is correct-by-construction (mirrors proven upstream). No action.

### No other findings

Config merge-layer description, `null`/`""`/`[]` clearing semantics, `⏸ ship-plan` status label, and the `{"decision":...,"feedback":...}` contract all match `config.ts`. No security surface (ships prose + data, no executable). Scope matches the plan (annotation aid in; code review / annotate-last / sharing / setup-goal out).

## Recommendation

Ship it. The auto-fix is committed alongside the review; no return to `ship-slice` needed.
