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

### Engineering Stack

Use this as the default product-engineering flow. The names are intentionally
plain so the next action is obvious.

| stage | skill | purpose |
|-------|-------|---------|
| research | `/research` | Answer what exists, why it matters, what to do, and how to challenge the recommendation |
| prototype | `/prototype` | Build a throwaway model, UI, or state machine to answer a design question |
| plan | `/plan` | Turn evidence into scope, sequence, risks, PRDs, issues, and verification |
| build | `/build` | Implement the planned change narrowly and in repo style |
| test | `/test` | Prove behavior through focused checks or the red-green-refactor loop |
| polish | `/polish` | Finish UX, code clarity, docs, edge cases, and handoff evidence |

### Supporting Engineering Skills

| skill | description |
|-------|-------------|
| `/code-structure` | Map modules, find structural friction, separate orchestration from services, and plan safe refactors |
| `/diagnose` | Disciplined bug diagnosis loop: reproduce → hypothesise → instrument → fix |
| `/review` | Two-axis code review: Standards + Spec, run in parallel |
| `/autoresearch` | Set up Karpathy-style autonomous research loops around the right metric and harness |
| `/triage` | Move issues through a triage state machine |
| `/qa` | Conversational QA session that files structured issues |
| `/grill-with-docs` | Grill a plan against the domain model, update CONTEXT.md + ADRs inline |

### Writing

| skill | description |
|-------|-------------|
| `/proofreading` | Proofread and improve an existing article draft section by section |
| `/writing` | Develop raw material into fragments, article drafts, or narrative beats |

### Productivity

| skill | description |
|-------|-------------|
| `/grill-me` | Relentless interview on any plan or design |
| `/handoff` | Compact the current session into a handoff document |
| `/write-a-skill` | Interactively build a new skill for this repo |

## Adding a skill

1. Create `skills/<name>/SKILL.md` with valid frontmatter.
2. Add supporting files beside it if needed.
3. Run `deno task validate`.
4. Update `CLAUDE.md`'s skills index if the skill list or metadata changed.

See `CLAUDE.md` for the full conventions.

## License

MIT
