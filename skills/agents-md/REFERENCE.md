# AGENTS.md Reference

The section template, repo-scan checklist, and interview script. Source
discipline: target ≤80 lines, hard cap 120; every line must prevent a specific
mistake or it gets deleted. (Official docs say "under 200" — the 80-line target
is a deliberate forcing function, stricter on purpose for better adherence.)

---

## Section template

Not every section is required. Include a section only if it carries lines that
prevent mistakes. Order roughly:

```markdown
# <Project Name>

One or two lines: what this project IS and the single most important thing an
agent must understand about it.

## Commands

- build: `<cmd>`
- test: `<cmd>`         # how to run one test, not just the whole suite
- lint/format: `<cmd>`
- run/dev: `<cmd>`

## Architecture

3–6 bullets an agent can't quickly infer: the non-obvious module boundaries,
the data flow, where the entry points are, what talks to what.

## Conventions

Only the ones a linter does NOT enforce. Imperative + positive alternative.
- Never <X>; instead <Y>.

## Gotchas

Footguns, sharp edges, "this looks wrong but is intentional" notes. The things
that have burned someone before.

## Out of scope / do not touch

Generated files, vendored code, areas requiring human sign-off.

## Approval gates

Actions that require asking first: migrations, force-push, dependency changes,
anything touching prod or shared state.

## External docs

- <url> — purpose; read-only / update-here.
```

---

## Repo-scan checklist (Step 1, fan out)

Gather these so you never ask the user something the repo already answers:

- [ ] **Manifests / stack** — package.json, deno.json, pyproject.toml, go.mod,
      Cargo.toml, Gemfile, etc. Languages, runtimes, key deps.
- [ ] **Commands** — build, test (incl. single-test invocation), lint, format,
      run/dev. Check scripts, Makefile, justfile, Taskfile, CI workflows. If no
      single-test script exists, derive the form from the test runner's CLI
      (e.g. `vitest run <file> -t <name>`); if undecidable, mark `TODO(human):`
      rather than inventing one.
- [ ] **Structure** — top-level layout, entry points, where source vs. tests
      vs. generated code live.
- [ ] **Linter / formatter configs** — .eslintrc, .prettierrc, ruff.toml,
      rustfmt.toml, .editorconfig. These rules belong in the tool, not AGENTS.md.
- [ ] **Git patterns** — commit message style, branch naming, PR conventions
      (from `git log` and any CONTRIBUTING).
- [ ] **Existing docs** — README, CONTRIBUTING, docs/, ADRs.
- [ ] **MCPs / integrations** — configured MCP servers, .claude/ settings.

---

## Interview script (Step 2)

Ask only what the scan can't reveal. Batch these; don't drip one at a time.

1. **Purpose / WHY** — What is this project for, and what's the one thing an
   agent most needs to understand before changing code here?
2. **Gotchas** — What footguns or surprising behaviors have burned people?
   What looks wrong but is intentional?
3. **Out of scope** — What should an agent never touch or modify? What needs
   human sign-off?
4. **Approval gates** — Which actions require asking first (migrations,
   force-push, adding deps, prod/shared-state changes)?
5. **Testing philosophy** — What does "tested" mean here? Required before a
   change is considered done? Any tests that must not be mocked?
6. **External docs** — Any canonical docs/dashboards to reference by URL?
   For each: read-only, or is it updated from here?

---

## What to exclude (always)

- **Linter-enforceable rules** — indentation, quote style, import ordering,
  line length. Put them in the tool config; the agent runs the formatter.
- **Restated framework defaults** — things true of any project using the stack.
- **Speculative scaffolding** — "we might add X later," empty placeholder
  sections.
- **Cached external docs** — link by URL with a freshness/update note; never
  paste content that will go stale.
- **Narrative / history** — how the codebase evolved belongs in git, not here.

---

## Placement

- `./AGENTS.md` — project root, committed; the default target.
- Nested `path/to/pkg/AGENTS.md` — monorepo per-package; loads on demand and
  **inherits** ancestors, so state only what differs from the parent.
- `AGENTS.local.md` — personal, uncommitted overrides; add to `.gitignore`.
- Claude interop — `./CLAUDE.md` (or `./.claude/CLAUDE.md`, `~/.claude/CLAUDE.md`)
  whose body is `@AGENTS.md`; see the AGENTS.md note below.

## Overflow target

When the root file would exceed 80 lines, push instructions that only matter in
part of the tree into `.claude/rules/*.md` with `paths:` frontmatter (preferred
over a generic `docs/architecture.md`). Link to them; don't pre-create empty
files.

## Formatting rules

- Reference other files with plain `see path/to/doc.md`. **Avoid `@imports`** —
  they load in full at launch (up to 4 hops) and burn context whether or not
  they're relevant. Reserve `@` only for AGENTS.md interop.
- Durable, discovered mistakes can be appended later via the `#` / `/memory`
  shortcut; auto-memory (`MEMORY.md`) captures learnings, so AGENTS.md need not.

## AGENTS.md note

Claude reads `CLAUDE.md`, not `AGENTS.md`. If a repo standardizes on AGENTS.md,
create a `CLAUDE.md` whose body is `@AGENTS.md` (the one sanctioned use of `@`),
or symlink the two. Decide this in Step 0, not after drafting.
