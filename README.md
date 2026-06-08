# Skills

Personal agent skills for engineering, writing, and productivity. Works with any agent that supports skill/slash-command loading (Claude Code, etc.).

## Quickstart

```sh
curl -fsSL https://raw.githubusercontent.com/anhdle14/skills/main/bootstrap.sh | sh
```

This will:

1. Clone the repo to `~/Developer/github.com/anhdle14/skills`
2. Install Deno if not present
3. Symlink `skills/` to `~/.claude/skills` and `~/.agents/skills`
4. Link each personal skill under `~/.codex/skills` while preserving `.system`

## Manual install

```sh
git clone https://github.com/anhdle14/skills ~/Developer/github.com/anhdle14/skills
cd ~/Developer/github.com/anhdle14/skills
deno task install
```

## Copy skills to a specific project

```sh
# Copy all skills
deno task install --copy-to /path/to/project/.claude/skills

# Copy specific skills only
deno task install --copy-to /path/to/project/.claude/skills --skill diagnose --skill grill-me
```

## Update

```sh
git -C ~/Developer/github.com/anhdle14/skills pull
```

The symlinks point at the repo, so updates are live immediately. Re-run
`deno task install` after adding, removing, or renaming skills so
`~/.codex/skills` gets refreshed.

For repo-scoped Codex skills, use `.agents/skills` under the repository. This
repo's default installer uses the user-scoped Codex locations,
`~/.agents/skills` and `~/.codex/skills`.

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
| `/caveman` | Ultra-compressed communication mode (~75% fewer tokens) |
| `/write-a-skill` | Interactively build a new skill for this repo |

## Adding a skill

```sh
deno run --allow-read --allow-write install.ts  # or: deno task install
```

See `CLAUDE.md` for the full conventions.

## License

MIT
