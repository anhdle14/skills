# Skills

Agent skills organized as a flat directory under `skills/`. Each skill is a folder containing `SKILL.md` and optional supporting files.

## Skills Index

Install everything with `npx skills add anhdle14/skills --all`, or grab a single skill with the command in its row.

| skill | install | description |
|-------|---------|-------------|
| [agents-md](skills/agents-md/SKILL.md) | `npx skills add anhdle14/skills@agents-md` | Create or rewrite the per-folder agent context file that an agent reads on every turn. Use when the user wants to create, bootstrap, or rewrite an AGENTS.md / CLAUDE.md / agent context file, or onboard an agent to a repo. Args: `"<target folder (defaults to cwd)>"` |
| [autoresearch](skills/autoresearch/SKILL.md) *(human-only)* | `npx skills add anhdle14/skills@autoresearch` | Sets up and runs the Karpathy-style autoresearch protocol - metric-first clarification, then an autonomous experiment loop under a fixed harness. Args: `"<run tag, metric, or repo path (optional)>"` |
| [code-structure](skills/code-structure/SKILL.md) | `npx skills add anhdle14/skills@code-structure` | Analyze and improve code structure by mapping modules, finding deepening opportunities, separating orchestration from service mechanics, and planning safe refactors. Use when unfamiliar with a code area, deciding what belongs in actions versus services, extracting repeated operational blocks, improving architecture, or planning a refactor. |
| [manage-skill](skills/manage-skill/SKILL.md) | `npx skills add anhdle14/skills@manage-skill` | Create, update, evaluate, and retire skills in this repo as tested behavior - failing case first, eval suite, static checks, retirement ablation. Use whenever adding or changing a SKILL.md, its references, scripts, tags, description, invocation mode, or eval cases. Do not use for ordinary code, prose, or AGENTS.md edits that are not agent skills. Args: `"<skill name, idea, or path to an existing skill (optional)>"` |
| [proofreading](skills/proofreading/SKILL.md) | `npx skills add anhdle14/skills@proofreading` | Proofread and improve existing article drafts by restructuring sections, improving clarity, and tightening prose. Use when the user wants to proofread, revise, or improve an existing prose draft. Args: `"<path to article file>"` |
| [prose-writing](skills/prose-writing/SKILL.md) | `npx skills add anhdle14/skills@prose-writing` | Develop raw material into non-technical prose - essays, articles, reports, newsletters, narrative and creative pieces - as fragments, drafts, or beats. Use when the user wants to ideate, collect fragments, shape notes into an article or report, write beat-by-beat, or turn raw material into publishable prose. Args: `"<path to raw material or output file (optional)>"` |
| [research](skills/research/SKILL.md) | `npx skills add anhdle14/skills@research` | Explores user intent, requirements, and design before implementation. Use when the user asks to research, brainstorm, design, or modify behavior before implementation. Args: `"<idea, feature, or behavior change (optional)>"` |
| [tech-writing](skills/tech-writing/SKILL.md) | `npx skills add anhdle14/skills@tech-writing` | Write or review technical documentation for software and engineering audiences - READMEs, API references, how-to guides for using a system or API, design docs, runbooks, release notes, error messages, PR descriptions - grounded in verified facts and Google's technical writing standards. Use when the user wants to write, draft, edit, review, or improve a developer-facing or engineering document about code, systems, APIs, or infrastructure. Not for personal, ceremonial, or life-event writing (speeches, toasts, invitations, packing or planning guides) even when it uses words like "guide" or "step by step" - use /prose-writing instead. Args: `"<doc path, topic, or draft to review (optional)>"` |
| [webgpu-threejs-tsl](skills/webgpu-threejs-tsl/SKILL.md) | `npx skills add anhdle14/skills@webgpu-threejs-tsl` | TSL and WebGPU node-shader toolkit covering node materials, GPU compute, post-processing, and WGSL integration. Use when building Three.js WebGPU apps, writing TSL shaders or node materials, porting GLSL to TSL, authoring GPU compute shaders, or assembling post-processing effects. |
Skills marked *(human-only)* carry `disable-model-invocation: true` - they never auto-trigger and are invoked explicitly (e.g. `/skill:autoresearch`).

## Conventions

### Adding a skill

1. Create `skills/<name>/SKILL.md` with the required frontmatter.
2. Add supporting files in the same folder if needed: `REFERENCE.md` / `EVALS.md` for on-demand detail, `scripts/` for tools, `evals/<name>.json` for eval cases.
3. Validate the skill with `manage-skill` (see below), then update the skills index above if the skill list or metadata changed.

```yaml
---
name: skill-name
description: What it does. Use when [specific triggers].
tags: [tag1, tag2]
args: "<arg-name>"   # optional
---
```

### Tags

Tags are freeform labels for browsing - use whatever fits the skill. Common ones already in use: `engineering`, `writing`, `analyze`, `create`, `transform`, `plan`, `productivity`, `design`. Add new ones when they help.

### Skill validation rules

Keep `SKILL.md` lightweight - the ordered workflow plus only the material every run needs. Everything else moves out of the file and is reached by a pointer:

- **Reference / detail** (glossaries, pattern tables, deep methodology, long examples) lives in a sibling `REFERENCE.md` or `EXAMPLES.md`, loaded on demand - not inlined.
- **Executable tools** live in `scripts/` and are invoked by the skill, never transcribed into it.
- `SKILL.md` stays under ~100 lines. A section that is pure lookup rather than an ordered action is a candidate to disclose; any meaning duplicated across files collapses to a single source of truth.
- Every `SKILL.md` carries the persistence rule: context is volatile RAM; filesystem is durable disk. Important plans, progress checkboxes, failures, and verification evidence go to files.
- A pure-lookup skill is tagged `reference` and **omits** the persistence rule: it runs no multi-turn workflow, so the line would be an instruction unrelated to its purpose - which a reader has no use for and a security scanner reads as prompt injection.
- **Eval cases** live in `evals/<name>.json`: the observed failure as a positive case, and the near-miss prompts that must not trigger the skill as negative cases. A model-invocable skill without negative cases has an untested trigger contract.

**Always validate with `manage-skill`.** Before adding or editing any skill, run the [`manage-skill`](skills/manage-skill/SKILL.md) workflow and checklist against it - a failing case first, then the minimal skill, then the checks:

```sh
python3 skills/manage-skill/scripts/eval_skill.py --all --static --require-cases   # every skill
python3 skills/manage-skill/scripts/eval_skill.py --skill skills/<name>            # trials
```
