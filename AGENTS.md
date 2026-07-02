# Skills

Agent skills organized as a flat directory under `skills/`. Each skill is a folder containing `SKILL.md` and optional supporting files.

## Skills Index

<!-- skills-index-start -->
| skill | tags | description |
|-------|------|-------------|
| [agents-md](skills/agents-md/SKILL.md) | create, engineering, productivity | Create or rewrite the per-folder agent context file that an agent reads on every turn. Use when the user wants to create, bootstrap, or rewrite an AGENTS.md / CLAUDE.md / agent context file, or onboard an agent to a repo. Args: `"<target folder (defaults to cwd)>"` |
| [autoresearch *(human-only)*](skills/autoresearch/SKILL.md) | engineering, plan, analyze | Sets up and runs the Karpathy-style autoresearch protocol - metric-first clarification, then an autonomous experiment loop under a fixed harness. Args: `"<run tag, metric, or repo path (optional)>"` |
| [code-structure](skills/code-structure/SKILL.md) | analyze, engineering, transform, plan | Analyze and improve code structure by mapping modules, finding deepening opportunities, separating orchestration from service mechanics, and planning safe refactors. Use when unfamiliar with a code area, deciding what belongs in actions versus services, extracting repeated operational blocks, improving architecture, or planning a refactor. |
| [proofreading](skills/proofreading/SKILL.md) | writing, transform | Proofread and improve existing article drafts by restructuring sections, improving clarity, and tightening prose. Use when the user wants to proofread, revise, or improve an existing prose draft. Args: `"<path to article file>"` |
| [research](skills/research/SKILL.md) | analyze, engineering, plan | Explores user intent, requirements, and design before implementation. Use when the user asks to research, brainstorm, design, or modify behavior before implementation. Args: `"<idea, feature, or behavior change (optional)>"` |
| [router *(human-only)*](skills/router/SKILL.md) | productivity | Human-only index of the disable-model-invocation skills - names each and when to reach for it. |
| [ship *(human-only)*](skills/ship/SKILL.md) | plan, engineering, productivity | Single self-orienting entry point for the four-phase ship pipeline - detects where a feature left off from its .ship/ artifacts and resumes it, or walks you from the start through grill, slice, build, review. Args: `"<feature description or .ship/<feature-slug> path (optional)>"` |
| [ship-grill *(human-only)*](skills/ship-grill/SKILL.md) | plan, engineering, productivity | Relentlessly interview a plan doc into a complete spec - resolve every grey area, build the glossary and ADRs, and write the handoff contract the autonomous build runs on. Args: `"<.ship/<feature-slug> path or feature description (optional)>"` |
| [ship-review *(human-only)*](skills/ship-review/SKILL.md) | analyze, engineering, productivity | The review gate for shipped deliverables - verify goal-backward against the spec, attack the code adversarially, then classify every finding by severity and action, apply the safe fixes, and escalate the judgment calls. Args: `"<.ship/<feature-slug> path (optional)>"` |
| [ship-slice *(human-only)*](skills/ship-slice/SKILL.md) | plan, engineering, productivity | Autonomously turn a spec into shipped vertical slices - decompose into tracer bullets, run them in non-blocking phases, fan out subagents, drive each to green, and commit outcomes. Args: `"<.ship/<feature-slug> path (optional)>"` |
| [webgpu-threejs-tsl](skills/webgpu-threejs-tsl/SKILL.md) | create, design, engineering, transform | TSL and WebGPU node-shader toolkit covering node materials, GPU compute, post-processing, and WGSL integration. Use when building Three.js WebGPU apps, writing TSL shaders or node materials, porting GLSL to TSL, authoring GPU compute shaders, or assembling post-processing effects. |
| [writing](skills/writing/SKILL.md) | writing, create, transform | Develop raw writing material into fragments, article drafts, or narrative beats without proofreading an existing draft. Use when user wants to ideate, collect fragments, shape notes into an article, write beat-by-beat, or turn raw material into publishable prose. Args: `"<path to raw material or output file (optional)>"` |
<!-- skills-index-end -->

## Engineering Stack

The broad engineering entry points are `/research` for evidence-gathering and
design, `/code-structure` for module maps and refactor shape, and `/agents-md`
for onboarding an agent to a repo.

Some skills are human-only (`disable-model-invocation: true`) and never
auto-trigger; invoke them explicitly: `/skill:autoresearch` and the ship
pipeline (`/skill:ship`, `/skill:ship-grill`, `/skill:ship-slice`,
`/skill:ship-review`). `/skill:router` is the human-only index that names them
and when to reach for each.

## Conventions

### Adding a skill

1. Create `skills/<name>/SKILL.md` with the required frontmatter.
2. Add supporting files in the same folder if needed.
3. If the skill is tagged `engineering`, add at least 3 trigger and 3 near-miss cases to `docs/evals/engineering-skills-trigger-cases.json`, then regenerate results with `deno task eval:engineering` (requires the `claude` CLI).
4. Run `deno task validate` to check frontmatter and structure.
5. Update the skills index above if the skill list or metadata changed.

```yaml
---
name: skill-name
description: What it does. Use when [specific triggers].
tags: [tag1, tag2]
args: "<arg-name>"   # optional
---
```

### Valid tags

| tag | use for |
|-----|---------|
| `analyze` | investigation, debugging, review, summarization |
| `create` | generating new artifacts — code, docs, issues, skills |
| `plan` | design sessions, grilling, prototyping, PRDs |
| `transform` | editing, refactoring, translating existing content |
| `manage` | issue tracking, triage, workflow |
| `engineering` | software development work |
| `writing` | prose, articles, documentation |
| `productivity` | workflow tools, meta-skills |
| `design` | visual, UX, and interface work meant for human consumption — web, graphics, shaders, layout |

### Skill file size

Keep `SKILL.md` under ~100 lines. Split into `REFERENCE.md`, `EXAMPLES.md`, or `scripts/` when it grows larger.

### Two kinds of eval (do not conflate)

- **Trigger eval** (`engineering-skills-trigger-*`, `deno task eval:engineering`) — does a
  skill's description get *selected* for a query? Required for every model-invocable
  engineering skill (human-only skills are hidden from selection and exempt).
- **Outcome benchmark** (`docs/evals/tbench/*`, `deno task bench:tbench`) — does a workflow
  scaffold (e.g. the ship pipeline) improve a real agentic loop on Terminal-Bench?
  A/B the stock `terminus` agent against `workflow-terminus` on the same model and task
  set. Outcome benchmarking must use Terminal-Bench only; do not add repo-local hidden
  tests, fixture tasks, or workflow-bench suites. Results and reproduction notes live in
  `docs/evals/tbench/RESULTS.md`.

Every `SKILL.md` must carry the persistence rule: context is volatile RAM; filesystem is durable disk. Important plans, progress checkboxes, failures, and verification evidence go to files.

### Scripts

Scripts live under `scripts/` inside the skill folder or at `scripts/` in the repo root for shared utilities. Use TypeScript + Deno with `@std/cli` for argument parsing.
