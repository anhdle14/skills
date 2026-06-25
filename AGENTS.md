# Skills

Agent skills organized as a flat directory under `skills/`. Each skill is a folder containing `SKILL.md` and optional supporting files.

## Skills Index

<!-- skills-index-start -->
| skill | tags | description |
|-------|------|-------------|
| [agents-md](skills/agents-md/SKILL.md) | create, engineering, productivity | Create or replace the per-folder agent context file that gets read on every turn, holding it to the 80-line budget where every line prevents a mistake. Use when user wants to create, write, generate, bootstrap, or rewrite an AGENTS.md / CLAUDE.md / agent context file, or onboard an agent to a repo. Args: `"<target folder (defaults to cwd)>"` |
| [autoresearch *(human-only)*](skills/autoresearch/SKILL.md) | engineering, plan, analyze | Sets up and runs the Karpathy-style autoresearch protocol - metric-first clarification, then an autonomous experiment loop under a fixed harness. Args: `"<run tag, metric, or repo path (optional)>"` |
| [code-structure](skills/code-structure/SKILL.md) | analyze, engineering, transform, plan | Analyze and improve code structure by mapping modules, finding deepening opportunities, separating orchestration from service mechanics, and planning safe refactors. Use when unfamiliar with a code area, deciding what belongs in actions versus services, extracting repeated operational blocks, improving architecture, or planning a refactor. |
| [orchestrate *(human-only)*](skills/orchestrate/SKILL.md) | plan, engineering, productivity | Conductor loop that decomposes a hard task, routes each subtask to the best worker, recurses on the hard parts, and synthesizes the results. Args: `"<hard or multi-part task (optional)>"` |
| [proofreading](skills/proofreading/SKILL.md) | writing, transform | Proofread and improve existing article drafts by restructuring sections, improving clarity, and tightening prose. Use when user wants to proofread, edit, revise, clean up, or improve an existing draft. Args: `"<path to article file>"` |
| [research](skills/research/SKILL.md) | analyze, engineering, plan | Explores user intent, requirements, and design before implementation. Use when user asks to research, brainstorm, design, create features, build components, add functionality, or modify behavior before implementation. Args: `"<idea, feature, or behavior change (optional)>"` |
| [router *(human-only)*](skills/router/SKILL.md) | productivity | Human-only index of the disable-model-invocation skills - names each and when to reach for it. |
| [trinity *(human-only)*](skills/trinity/SKILL.md) | engineering, analyze, productivity | Thinker-Worker-Verifier role loop that iterates accept-or-revise across turns until a result is verified or a turn budget is hit. Args: `"<task to solve via the role loop (optional)>"` |
| [writing](skills/writing/SKILL.md) | writing, create, transform | Develop raw writing material into fragments, article drafts, or narrative beats without proofreading an existing draft. Use when user wants to ideate, collect fragments, shape notes into an article, write beat-by-beat, or turn raw material into publishable prose. Args: `"<path to raw material or output file (optional)>"` |
<!-- skills-index-end -->

## Engineering Stack

The broad engineering entry points are `/research` for evidence-gathering and
design, `/code-structure` for module maps and refactor shape, and `/agents-md`
for onboarding an agent to a repo.

Some skills are human-only (`disable-model-invocation: true`) and never
auto-trigger; invoke them explicitly: `/skill:autoresearch`,
`/skill:orchestrate`, and `/skill:trinity`. `/skill:router` is the human-only
index that names them and when to reach for each.

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

### Skill file size

Keep `SKILL.md` under ~100 lines. Split into `REFERENCE.md`, `EXAMPLES.md`, or `scripts/` when it grows larger.

### Two kinds of eval (do not conflate)

- **Trigger eval** (`engineering-skills-trigger-*`, `deno task eval:engineering`) — does a
  skill's description get *selected* for a query? Required for every engineering skill.
- **Outcome benchmark** (`docs/evals/tbench/*`, `deno task bench:tbench`) — does the
  orchestrate+trinity workflow scaffold improve a real agentic loop on Terminal-Bench?
  A/B the stock `terminus` agent against `workflow-terminus` on the same model and task
  set. Outcome benchmarking must use Terminal-Bench only; do not add repo-local hidden
  tests, fixture tasks, or workflow-bench suites. Results and reproduction notes live in
  `docs/evals/tbench/RESULTS.md`.

Every `SKILL.md` must carry the persistence rule: context is volatile RAM; filesystem is durable disk. Important plans, progress checkboxes, failures, and verification evidence go to files.

### Scripts

Scripts live under `scripts/` inside the skill folder or at `scripts/` in the repo root for shared utilities. Use TypeScript + Deno with `@std/cli` for argument parsing.
