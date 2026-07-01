# Skills

Personal agent skills for engineering, writing, and productivity. Works with any agent that supports skill/slash-command loading.

## Quickstart

Use the standard skills CLI instead of this repo carrying a custom installer:

```sh
npx skills add anhdle14/skills -g --all
```

This installs all skills globally for supported agents. To install into a project instead, omit `-g`:

```sh
npx skills add anhdle14/skills --all
```

For more options, run:

```sh
npx skills --help
```

## Update

```sh
npx skills update -g
```

If you cloned this repository for development, update the clone with:

```sh
git -C ~/Developer/github.com/anhdle14/skills pull
```

## Local development

```sh
git clone https://github.com/anhdle14/skills ~/Developer/github.com/anhdle14/skills
cd ~/Developer/github.com/anhdle14/skills
deno task validate
```

## Skill Reference

### Engineering

| skill | description |
|-------|-------------|
| `/research` | Answer what exists, why it matters, what to do, and how to challenge the recommendation |
| `/code-structure` | Map modules, find structural friction, separate orchestration from services, and plan safe refactors |
| `/agents-md` | Create or rewrite the per-folder agent context file within the 80-line budget |
| `/webgpu-threejs-tsl` | Build Three.js WebGPU apps with TSL node materials, GPU compute, and post-processing |

### Writing

| skill | description |
|-------|-------------|
| `/proofreading` | Proofread and improve an existing article draft section by section |
| `/writing` | Develop raw material into fragments, article drafts, or narrative beats |

### Human-only skills

These carry `disable-model-invocation: true`, so they never auto-trigger and
must be invoked explicitly. `/skill:router` is the index that names them.

| skill | description |
|-------|-------------|
| `/skill:router` | Human-only index: names the skills below and when to reach for each |
| `/skill:autoresearch` | Run the Karpathy-style autoresearch loop around an agreed metric and fixed harness |
| `/skill:ship` | Index + handoff contract for the four-phase feature pipeline (grill, slice, build, review) |
| `/skill:ship-grill` | Interrogate a plan doc into a complete spec — resolve grey areas, build glossary/ADRs |
| `/skill:ship-slice` | Autonomously build a spec as vertical slices across non-blocking phases, fanning out subagents |
| `/skill:ship-review` | The review gate for deliverables — goal-backward against the spec, adversarial attack, then classify findings by severity and action, auto-fix the safe ones, escalate the judgment calls |

## Adding a skill

1. Create `skills/<name>/SKILL.md` with valid frontmatter.
2. Add supporting files beside it if needed.
3. Run `deno task validate`.
4. Update `AGENTS.md`'s skills index if the skill list or metadata changed.

See `AGENTS.md` for the full conventions.

## License

MIT
