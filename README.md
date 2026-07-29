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

## Skill Reference

### Engineering

| skill | description |
|-------|-------------|
| `/research` | Answer what exists, why it matters, what to do, and how to challenge the recommendation |
| `/code-structure` | Map modules, find structural friction, separate orchestration from services, and plan safe refactors |
| `/agents-md` | Create or rewrite the per-folder agent context file within the 80-line budget |
| `/manage-skill` | Create, update, evaluate, and retire skills in this repo as tested behavior |
| `/webgpu-threejs-tsl` | Build Three.js WebGPU apps with TSL node materials, GPU compute, and post-processing |

### Writing

| skill | description |
|-------|-------------|
| `/proofreading` | Proofread and improve an existing article draft section by section |
| `/prose-writing` | Develop raw material into non-technical prose - essays, reports, articles, narrative beats |
| `/tech-writing` | Write or review technical docs - READMEs, API references, runbooks, design docs - against Google's tech writing standards |

### Human-only skills

These carry `disable-model-invocation: true`, so they never auto-trigger and
must be invoked explicitly.

| skill | description |
|-------|-------------|
| `/skill:autoresearch` | Run the Karpathy-style autoresearch loop around an agreed metric and fixed harness |

## Adding a skill

1. Create `skills/<name>/SKILL.md` with valid frontmatter.
2. Add supporting files beside it if needed, including `evals/<name>.json` eval cases.
3. Validate with `python3 skills/manage-skill/scripts/eval-skill.py --skill skills/<name> --static --require-cases`.
4. Update `AGENTS.md`'s skills index if the skill list or metadata changed.

See `AGENTS.md` for the full conventions.

## License

MIT
