# Ship · Plan — Reference

The detail behind `SKILL.md`: the review-gate tier contract, the plannotator config template,
and how to activate it. Shared ship contracts (`.ship/` layout, resume-detection, the Tier A/B
subagent substrate) live in [../ship/REFERENCE.md](../ship/REFERENCE.md) and are not repeated
here.

---

## Why "fork plannotator" is a config + prompt, not a code fork

[Plannotator](https://github.com/backnotprop/plannotator) is a local, browser-based review
surface for AI coding agents (Claude Code, Codex, Copilot, Gemini, OpenCode, Kiro, Droid, Amp,
Pi). Its Pi extension already implements the exact phase machine this phase needs — a restricted
`planning` phase that opens a browser review when the agent calls `plannotator_submit_plan`, and
an `executing` phase after approval.

Rather than fork the app (a Bun/TS project with a browser UI, hook servers, and multi-harness
integrations), `ship-plan` **reuses** it and specializes only the planning-phase *prompt* via a
config override. That keeps the ship pipeline's invariant intact: every ship phase ships prose
and data, never an executable.

---

## The review-gate tiers (full contract)

`ship-plan` selects a gate by capability detection — the same "use the highest tier your agent
actually supports" principle as the Tier A/B subagent substrate. Detect once at the start of the
review step; re-detect if the environment changes mid-session.

| Tier | Detection probe | Gate mechanism | Feedback channel |
|---|---|---|---|
| **1 native** | the `plannotator_submit_plan` tool is available in the session | call `plannotator_submit_plan` with the `PLAN.md` path; browser review opens | approve → proceed; deny → annotations returned to the agent; resubmit → plan diff |
| **2 CLI** | `command -v plannotator` succeeds | `plannotator annotate .ship/<slug>/PLAN.md --gate --json` | structured decision JSON on stdout (`{"decision":"approved\|dismissed\|annotated","feedback":"..."}`) |
| **3 in-chat** | neither of the above | write `PLAN.md`, ask the user to read and respond in chat | free-form chat approval / change requests |

Rules:

- **Prefer the highest available tier. Never ask the user which tier to use.**
- **Announce only on degrade.** Stay silent at Tier 1. When falling back, print exactly one line:
  - Tier 2: `plannotator extension not active — using the annotate CLI gate`
  - Tier 3: `plannotator not detected — using in-chat review gate`
- **Revise with targeted edits.** On denial, read `PLAN.md`, edit only what the feedback touches,
  and resubmit the same path. A full rewrite destroys the plan-diff signal at Tier 1.
- **Approval is explicit.** Do not proceed to the grill handoff on ambiguous feedback; iterate
  until the user clearly approves.

### Planning-time annotation aid (Tier 1/2 only)

While planning you may pull a reference document, URL, or rendered HTML artifact into the
annotate UI to discuss it with the user:

```bash
plannotator annotate <file.md | https://... | report.html> [--render-html]
```

`--render-html` renders HTML as-is instead of converting to markdown. This is a reference aid,
not the plan review gate — the gate is always the `PLAN.md` itself. Unavailable at Tier 3.

---

## The config template (`plannotator.json`)

`skills/ship-plan/plannotator.json` is a **template**, not live config. It overrides
plannotator's Pi-extension planning phase so the agent writes `.ship/<slug>/PLAN.md`, follows the
ship layout, and — on approval — hands off to `/skill:ship-grill` instead of implementing.

The Pi extension merges config in three layers, later layers winning:

1. built-in `plannotator.json` shipped with the extension
2. global user config: `~/.pi/agent/plannotator.json`
3. project-local config: `<project>/.pi/plannotator.json`

A field set in a higher layer replaces the lower one; a field set to `null`, `""`, or `[]` clears
the inherited value. Prompt template variables available inside `systemPrompt`: `${planFilePath}`,
`${todoList}`, `${completedCount}`, `${totalCount}`, `${remainingCount}`, `${phase}`.

### Activation

Copy the template into whichever scope you want, then restart / re-enter plan mode:

```bash
# project scope (this feature's repo)
mkdir -p .pi && cp skills/ship-plan/plannotator.json .pi/plannotator.json

# or global scope (all your projects)
mkdir -p ~/.pi/agent && cp skills/ship-plan/plannotator.json ~/.pi/agent/plannotator.json
```

Enter plan mode with `pi --plan`, `/plannotator`, or `Ctrl+Alt+P`. The status line shows
`⏸ ship-plan` when the override is active.

**Note on `.pi/` being gitignored.** In most repos `.pi/` is gitignored, so an activated
`.pi/plannotator.json` is a local, uncommitted setting — which is usually what you want. To commit
the activated config (e.g. to dogfood `ship-plan` in this skills repo), add a negation after the
`.pi/` rule in `.gitignore`:

```gitignore
.pi/
!.pi/plannotator.json
```

### Without the config

`ship-plan` still works with no config activated: the skill's own prose drives the plan loop, and
the review gate falls to Tier 2 (if the `plannotator` binary is installed) or Tier 3 (in-chat).
The config template only upgrades the experience to the native Tier 1 phase machine.
