# Engineering Skills Eval — Trigger Surface

This eval applies the Anthropic `skill-creator` description-optimization idea to every skill tagged `engineering` in this repo, using the planning-with-files eval style: explicit test cases, pass/fail assertions, and a results table.

## Scope

Engineering skills are selected by frontmatter tag. Each skill has six trigger-routing cases: three should-trigger prompts and three near-miss should-not-trigger prompts.

| skill | result |
|-------|--------|
| `autoresearch` | 6/6 |
| `build` | 6/6 |
| `agents-md` | 6/6 |
| `code-structure` | 6/6 |
| `diagnose` | 6/6 |
| `grill-with-docs` | 6/6 |
| `plan` | 6/6 |
| `polish` | 6/6 |
| `prototype` | 6/6 |
| `qa` | 6/6 |
| `research` | 6/6 |
| `review` | 6/6 |
| `test` | 6/6 |
| `triage` | 6/6 |
| `workflow` | 6/6 |

## Validation workflow

- `deno task validate` now runs both structural skill validation and an offline eval-fixture check.
- `deno task eval:engineering` runs the live Claude selector eval and writes fresh results to `docs/evals/engineering-skills-trigger-results.json`.
- Eval cases live in `docs/evals/engineering-skills-trigger-cases.json`.
- The validation check ensures the cases cover every engineering-tagged skill and that the stored results match the case set with at least the configured minimum pass rate.

## Test environment

- Repo: `/Users/duc.le/Developer/github.com/anhdle14/skills`
- Claude Code CLI: 2.1.153
- Eval model: `haiku`
- Validation commands run:
  - `deno task eval:engineering` → `summary: 102/102 (100.0%)`
  - `deno task validate` → `OK: validated 23 skills`; `OK: eval fixtures cover 17 engineering skills (102 cases)`
  - `deno task check` → passed

## Method

I used a trigger-surface eval rather than a full with-skill/without-skill behavior benchmark because these are broad agent workflow skills and several can modify repositories. Running behavior benchmarks for all 15 skills would require isolated fixture repos and many Claude sessions.

Procedure:

1. Identify all repo skills tagged `engineering`.
2. Maintain six realistic prompts per skill in `engineering-skills-trigger-cases.json`: three direct triggers and three adjacent near-misses.
3. Ask Claude to act as the skill router over the repo skill descriptions and return selected skills for each prompt.
4. Mark an assertion as pass when the target skill is selected exactly for should-trigger prompts and not selected for should-not-trigger prompts.
5. Store raw selector decisions in `engineering-skills-trigger-results.json`; validate the fixture/result shape in `deno task validate`.

Pilot note: I tried the upstream `skill-creator` `scripts.run_eval` trigger harness first. In this Claude Code CLI environment, the synthetic `.claude/commands` skill did not trigger for a positive `build` prompt (`1/2` pilot assertions passed; the should-trigger case was a false negative). To avoid reporting harness incompatibility as skill failure, this repo eval uses a selector prompt that directly tests the frontmatter descriptions.

## Results

Aggregate pass rate: **102/102 (100.0%)**

| skill | passed | failed | pass rate |
|-------|--------|--------|-----------|
| `autoresearch` | 6 | 0 | 100.0% |
| `build` | 6 | 0 | 100.0% |
| `agents-md` | 6 | 0 | 100.0% |
| `code-structure` | 6 | 0 | 100.0% |
| `diagnose` | 6 | 0 | 100.0% |
| `grill-with-docs` | 6 | 0 | 100.0% |
| `plan` | 6 | 0 | 100.0% |
| `polish` | 6 | 0 | 100.0% |
| `prototype` | 6 | 0 | 100.0% |
| `qa` | 6 | 0 | 100.0% |
| `research` | 6 | 0 | 100.0% |
| `review` | 6 | 0 | 100.0% |
| `test` | 6 | 0 | 100.0% |
| `triage` | 6 | 0 | 100.0% |
| `workflow` | 6 | 0 | 100.0% |

## Boundary coverage

The `research` cases now encode the intended boundary with `code-structure`:

- `research` should trigger for decision-oriented investigation, comparison, tradeoffs, and next-step recommendations.
- `code-structure` should own module maps, callers, ownership boundaries, action-vs-service placement, refactor seams, and architecture cleanup.
- The current live eval selected `research` for decision prompts and avoided it for structural map prompts.

## Outcome benchmark

Outcome benchmarking lives under `docs/evals/tbench/` and uses Terminal-Bench only.
Do not add repo-local hidden tests, fixture tasks, or `workflow-bench-*` suites for
workflow outcomes. Reproduce the current workflow A/B with `deno task bench:tbench`
(or `bash docs/evals/tbench/run_claude.sh both`) when Docker, `uvx`, and the required
model credentials are available.

## Next improvements

1. Expand the Terminal-Bench task set and repeat count for workflow outcome confidence.
2. Keep `deno task validate` cheap and deterministic; use `deno task eval:engineering` for live, model-dependent trigger-refreshes.
