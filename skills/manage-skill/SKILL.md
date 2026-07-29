---
name: manage-skill
description: Create, update, evaluate, and retire skills in this repo as tested behavior - failing case first, eval suite, static checks, retirement ablation. Use whenever adding or changing a SKILL.md, its references, scripts, tags, description, invocation mode, or eval cases. Do not use for ordinary code, prose, or AGENTS.md edits that are not agent skills.
tags: [create, productivity, engineering]
args: "<skill name, idea, or path to an existing skill (optional)>"
---

# Manage a Skill

Persistence rule: context is volatile RAM; filesystem is durable disk. Write the failing-case transcript, eval suite, progress checkboxes, and trial results to files; re-read them before decisions and done checks.

A skill is **tested behavior, not reusable prompt prose**. It wrangles determinism out of a stochastic system, and **predictability** - the agent taking the same *process* every run, not producing the same output - is the root virtue. The Iron Law keeps you honest:

> **NO SKILL CHANGE WITHOUT A FAILING CASE FIRST.** Applies to new skills *and* edits. Wrote the skill before watching an agent fail? Delete it, start over.

Read [REFERENCE.md](REFERENCE.md) for vocabulary, description patterns, form matching, bulletproofing, and failure modes. Read [EVALS.md](EVALS.md) before writing or changing eval cases.

## Choose the branch

- **Create** - no skill exists yet. Run steps 1-7.
- **Update** - body, description, mode, or supporting files change. Run steps 3-7.
- **Evaluate** - measure an existing skill without changing it. Run step 5.
- **Retire** - decide whether a skill still earns its context. Run step 6.

## 1. Decide whether to create

Create when the technique is non-obvious, reused across projects, and applies broadly. Do **not** create for a one-off, a project-specific convention (that goes in `AGENTS.md`), or a mechanical constraint a linter or regex can enforce - automate those and save skills for judgment calls.

Classify it: a **capability** skill teaches behavior the current model cannot do consistently and becomes removable as models improve; a **preference** skill encodes conventions, safety boundaries, or workflow and lives as long as that contract holds. The classification decides how you read step 6.

## 2. Choose the invocation mode - explicitly

Every skill is one of two modes; the author must state which.

- **Human-only** (`disable-model-invocation: true`): zero context load, fires only when you type its name. Choose it for broad workflow routers and for anything the user should deliberately enter.
- **Model-invocable** (omit the flag): auto-fires and other skills can reach it, but its `description` sits in the context window every turn. Choose it when the agent must reach the skill on its own - especially when the failure happens precisely because nobody invoked it.

The description is the trigger contract: what it does, which intents fire it, and the near-miss tasks that must **not**. See REFERENCE.md "Writing the description".

## 3. RED: capture the failing case

Pick the task that tempts the failure. Run it on a fresh-context subagent **without** the skill and record, verbatim, what it does wrong and every rationalization it gives. **No observed failure means there is nothing to teach - stop.**

Turn that run into files before writing any skill text:

- The transcript, under `skills/<name>/validation-<date>.md` - gitignored, so it stays local evidence and never lands in the repo.
- The prompt, as a positive case in `skills/<name>/evals/<name>.json`, plus the near-miss prompts that must not trigger it as negative cases. EVALS.md has the schema and the grading order.

Complete when the eval suite contains the observed failure as a case and `--static` accepts the suite.

## 4. GREEN: write the minimal skill

Address the exact failures from RED - nothing speculative. Match the form to the failure (REFERENCE.md): a positive recipe or structural slot for wrong-shaped output, a prohibition plus rationalization table only for a discipline an agent skips under pressure. Structure the body as an **information hierarchy**: ordered **steps** each ending on a *checkable* completion criterion, and **reference** consulted on demand. Inline what every run needs; disclose to `REFERENCE.md` what only some runs reach; put deterministic mechanics in `scripts/` instead of prose an agent must re-derive. One excellent, runnable example beats five languages.

## 5. Verify: static checks, then trials

```bash
python3 skills/manage-skill/scripts/eval-skill.py --skill skills/<name> --static
python3 skills/manage-skill/scripts/eval-skill.py --skill skills/<name> --trials 3 --judge
python3 skills/manage-skill/scripts/eval-skill.py --all --static --require-cases   # whole repo
```

Static checks cover frontmatter, name/directory match, the persistence line, body size, local links, the `AGENTS.md` index row (link, install command, mode marker, and description verbatim), and suite shape. Trials measure triggering and behavior against the cases.

Report **pass rates**, not a lucky single pass. Then REFACTOR: every new rationalization gets an explicit counter and a permanent regression case; then prune - one **single source of truth** per meaning, delete **no-ops** (lines the agent already obeys), collapse restated ideas into a **leading word**. Re-run after cutting.

Complete when static checks pass and every enabled-mode case passes at the suite's trial count.

## 6. Retire

```bash
python3 skills/manage-skill/scripts/eval-skill.py --skill skills/<name> --compare-without-skill
```

Remove a **capability** skill only when baseline pass rates match the skill-enabled rates and negative-trigger behavior does not regress. Keep the eval suite after deleting the skill - it is the sentinel that justifies restoring it when a model regresses. Do not retire a **preference** skill because a base model passes generic examples; its job is the repo's contract, not raw ability.

## 7. Wire it into the repo

- Skill at `skills/<name>/SKILL.md` (name: lowercase, numbers, hyphens; matching the directory). `REFERENCE.md` / `EVALS.md` siblings for on-demand detail, `scripts/` for tools, `evals/<name>.json` for cases.
- Body starts with the persistence rule line and stays under ~100 lines.
- Add the `AGENTS.md` index row with `npx skills add anhdle14/skills@<name>`, repeating the frontmatter description verbatim, marked `*(human-only)*` iff the frontmatter disables model invocation, and mirror it in `README.md`.
- Changed the harness itself? Run `python3 skills/manage-skill/tests/test_eval_skill.py`.

## Checklist

- [ ] RED failing case observed and its transcript saved before any skill text existed
- [ ] Failure encoded as an eval case; near-misses encoded as negative cases
- [ ] Classification (capability or preference) and invocation mode chosen explicitly
- [ ] Frontmatter valid: `name`, `description`, `tags`; `disable-model-invocation` iff human-only; `args` if it takes input
- [ ] Description is a trigger contract with negative boundaries - never a workflow summary
- [ ] Guidance form matches the failure type; one excellent example, not multi-language
- [ ] Deterministic mechanics live in `scripts/`, on-demand detail in a sibling `.md`
- [ ] `--static` clean; trials reported as pass rates with model and trial count
- [ ] REFACTOR: loopholes countered, no-ops pruned, single source of truth
- [ ] `AGENTS.md` and `README.md` rows match the skill's real mode
