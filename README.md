# Skills

Personal agent skills for engineering, writing, and productivity. Works with any agent that supports skill/slash-command loading (Claude Code, etc.).

Inspired by [mattpocock/skills](https://github.com/mattpocock/skills) — same philosophy, with Deno.

## Quickstart

```sh
curl -fsSL https://raw.githubusercontent.com/anhdle14/skills/main/bootstrap.sh | sh
```

This will:

1. Clone the repo to `~/Developer/github.com/anhdle14/skills`
2. Install Deno if not present
3. Symlink `skills/` to `~/.claude/skills` and `~/.agents/skills` for Codex

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

The symlinks point at the repo, so updates are live immediately.

For repo-scoped Codex skills, use `.agents/skills` under the repository. This
repo's default installer uses the user-scoped Codex location, `~/.agents/skills`.

## Skill Reference

### Engineering

| skill | description |
|-------|-------------|
| `/code-structure` | Map modules, find structural friction, separate orchestration from services, and plan safe refactors |
| `/diagnose` | Disciplined bug diagnosis loop: reproduce → hypothesise → instrument → fix |
| `/tdd` | Test-driven development with red-green-refactor vertical slices |
| `/review` | Two-axis code review: Standards + Spec, run in parallel |
| `/autoresearch` | Set up Karpathy-style autonomous research loops around the right metric and harness |
| `/prototype` | Throwaway prototype to answer a design question |
| `/to-issues` | Break a plan into vertical-slice issues |
| `/to-prd` | Synthesize current context into a PRD |
| `/triage` | Move issues through a triage state machine |
| `/qa` | Conversational QA session that files structured issues |
| `/grill-with-docs` | Grill a plan against the domain model, update CONTEXT.md + ADRs inline |

### Writing

| skill | description |
|-------|-------------|
| `/edit-article` | Edit and improve an article draft section by section |
| `/writing-fragments` | Mine ideas into raw writing fragments before imposing structure |
| `/writing-shape` | Shape a pile of fragments into a publishable article |
| `/writing-beats` | Build an article beat-by-beat, choose-your-own-adventure style |

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
