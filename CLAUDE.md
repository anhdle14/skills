# Skills

Agent skills organized as a flat directory under `skills/`. Each skill is a folder containing `SKILL.md` and optional supporting files.

## Skills Index

<!-- skills-index-start -->
| skill | tags | description |
|-------|------|-------------|
| [autoresearch](skills/autoresearch/SKILL.md) | engineering, plan, analyze | Sets up and runs Karpathy-style autoresearch with metric-first clarification and the upstream experiment protocol. Use when user wants to set up autoresearch, run autonomous research experiments, optimize a training metric, or mentions karpathy/autoresearch. Args: `"<run tag, metric, or repo path (optional)>"` |
| [caveman](skills/caveman/SKILL.md) | productivity | Provides ultra-compressed communication while preserving full technical accuracy. Use when user says "caveman mode", "talk like caveman", "less tokens", "be brief", or invokes /caveman. |
| [code-structure](skills/code-structure/SKILL.md) | analyze, engineering, transform, plan | Analyze and improve code structure by mapping modules, finding deepening opportunities, separating orchestration from service mechanics, and planning safe refactors. Use when unfamiliar with a code area, deciding what belongs in actions versus services, extracting repeated operational blocks, improving architecture, or planning a refactor. |
| [diagnose](skills/diagnose/SKILL.md) | analyze, engineering | Runs a disciplined reproduce, minimise, hypothesise, instrument, fix, and regression-test loop for hard bugs and performance regressions. Use when user says "diagnose this" / "debug this", reports a bug, says something is broken/throwing/failing, or describes a performance regression. |
| [edit-article](skills/edit-article/SKILL.md) | writing, transform | Edit and improve articles by restructuring sections, improving clarity, and tightening prose. Use when user wants to edit, revise, or improve an article draft. Args: `"<path to article file>"` |
| [grill-me](skills/grill-me/SKILL.md) | plan, productivity | Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me". Args: `"<plan or topic to grill on>"` |
| [grill-with-docs](skills/grill-with-docs/SKILL.md) | plan, engineering | Challenges a plan against the existing domain model, sharpens terminology, and updates project context docs and ADRs as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions. Args: `"<plan or topic to grill on>"` |
| [handoff](skills/handoff/SKILL.md) | productivity, plan | Compact the current conversation into a handoff document for another agent to pick up. Use when switching agents, ending a session, or when the user says "handoff". Args: `"<what the next session will focus on (optional)>"` |
| [prototype](skills/prototype/SKILL.md) | create, plan, engineering | Builds a throwaway prototype to answer a design question before committing. Use when user wants to prototype, sanity-check a data model or state machine, mock up a UI, or says "prototype this", "let me play with it", "try a few designs". |
| [qa](skills/qa/SKILL.md) | analyze, manage, engineering | Interactive QA session where user reports bugs or issues conversationally, and the agent files structured issues on the issue tracker. Use when user wants to report bugs, do QA, file issues conversationally, or mentions "QA session". |
| [review](skills/review/SKILL.md) | analyze, engineering | Reviews code changes along standards and spec axes with parallel sub-agents. Use when user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X". Args: `"<commit, branch, tag, or merge-base to diff against>"` |
| [tdd](skills/tdd/SKILL.md) | engineering, create | Test-driven development with red-green-refactor loop using vertical tracer-bullet slices. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development. |
| [to-issues](skills/to-issues/SKILL.md) | plan, engineering, manage | Break a plan, spec, or PRD into independently-grabbable issues using tracer-bullet vertical slices. Use when user wants to convert a plan into issues, create implementation tickets, or break down work into issues. Args: `"<issue reference, URL, or path (optional)>"` |
| [to-prd](skills/to-prd/SKILL.md) | plan, engineering, create | Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context, formalize a feature, or document what's being built. |
| [triage](skills/triage/SKILL.md) | manage, engineering | Triage issues through a state machine of five canonical roles. Use when user wants to create an issue, triage issues, review incoming bugs or feature requests, prepare issues for an AFK agent, or manage issue workflow. |
| [write-a-skill](skills/write-a-skill/SKILL.md) | productivity, create | Builds a new agent skill with frontmatter, supporting files, and review steps. Use when user wants to create, write, or build a new skill. |
| [writing-beats](skills/writing-beats/SKILL.md) | writing, create | Shape an article as a journey of beats, choose-your-own-adventure style — pick a starting beat, write only that beat, then offer options for the next beat until the article reaches a natural end. Use when user has raw material and wants to assemble it as a narrative rather than an argument. Args: `"<path to raw material file>"` |
| [writing-fragments](skills/writing-fragments/SKILL.md) | writing, create | Mine the user for writing fragments — claims, vignettes, sharp sentences, half-thoughts — and append them to a single document as raw material for a future article. Use when user wants to develop ideas before imposing structure, mentions "fragments", "ideate", or "raw material" for writing. Args: `"<path to save fragments (optional)>"` |
| [writing-shape](skills/writing-shape/SKILL.md) | writing, transform | Shape a pile of raw material into an article — draft candidate openings, grow the piece paragraph by paragraph, argue about format at each step. Use when user has notes, fragments, or a rough draft and wants help turning it into something publishable. Args: `"<path to raw material file>"` |
<!-- skills-index-end -->

## Conventions

### Adding a skill

1. Create `skills/<name>/SKILL.md` with the required frontmatter.
2. Add supporting files in the same folder if needed.
3. Run `deno task install --update-index` to regenerate this table.

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

### Scripts

Scripts live under `scripts/` inside the skill folder or at `scripts/` in the repo root for shared utilities. Use TypeScript + Deno with `@std/cli` for argument parsing.
