# Review and writing skill migration

## Goal and decisions

Replace the three writing skills with one model-invocable `writing` skill, and adapt t3dotgg/tstack's `council` skill into a model-invocable `review` skill.
The worktree was clean at the initial inspection.
No skill files have changed.

- A normal review uses one reviewer.
- A deep, thorough, comprehensive, council, or equivalent review uses three reviewers from different providers.
- Model selection uses available harness capabilities, not hard-coded claims about the latest models.
- Missing providers or failed reviewers are reported; they are not silently substituted.
- Writing always consults ASD-STE100 guidance, adapted to the genre rather than claiming strict STE compliance.
- Research-paper writing uses arXiv and field-relevant primary sources, with verified citations and cross-references.
- Plans and substantive user replies are first-class writing tasks.
- No commits, pushes, machine-global skill changes, dependency additions, or harness changes are included.

## Design

### Review

Create `skills/review/SKILL.md` with a concise workflow and on-demand supporting references.
Preserve useful upstream council behavior, source attribution, and applicable license notices.
Cover code and local diffs, architecture, implementation plans, technical and non-technical documents, and research arguments.
Distinguish substantive review from proofreading, which belongs to `writing`.

A normal review uses one reviewer; deep-review wording selects three independent, cross-provider reviewers.
Use the current agent for the single-reviewer path unless the user explicitly requests delegation.
The deep-review request authorizes the council workflow, subject to host policies.
Keep reviews read-only unless the user also asks for fixes.
Do not edit a checkout while delegates review it.
Verify findings against the artifact and report concrete evidence, severity, impact, and suggested changes.
Separate verified defects from questions and preferences.
Report coverage, unresolved disagreements, and limitations even when no defects are found.
Do not require numeric scores or a PR.
Do not edit PR descriptions, post comments, or iterate indefinitely without authorization.

### Writing

Create `skills/writing/SKILL.md`, with focused references for prose, technical documents, research papers, plans, and replies.
Keep the entry point under approximately 100 lines.
Use an explicit trigger contract covering drafting, rewriting, proofreading, summaries, explanations, plans, and substantive replies.
Exclude code-only changes, exact-output requests, and mechanical data transfers that must not be rewritten.
A skill description improves discoverability but cannot guarantee that every host loads it on every turn.

Use a shared workflow: establish audience and purpose, collect evidence, choose structure, draft or edit, then check correctness and clarity.
For brief replies, perform this in a lightweight pass without creating notes files, announcing a mode, or asking for an outline.
For substantial artifacts, persist decisions, evidence, unresolved questions, and progress.
Lead with the answer, use concrete language, preserve meaning and authorial voice, and remove unnecessary text without removing needed qualifications.
Preserve explicit user constraints and exact quotations.
Remove the old arbitrary paragraph-character limit and unnecessary per-section approval requirements.

Always consult a compact local STE application reference.
Bundle the requested original PDF only after checking its actual copyright statement and redistribution conditions.
Record its source, issue, checksum, and applicable notices; keep any adaptation clearly separate from the original standard.
If redistribution is not permitted, stop that part and offer a local, untracked reference with acquisition instructions instead of silently omitting the requested reference.
Do not claim full STE compliance based on an advisory prose checker.

For research papers, search the actual field rather than maintaining a generic list of papers.
Verify title, authors, identifier, version, and the claim supported by each citation.
Follow relevant references and citing work where available, distinguish preprints from peer-reviewed publications, and record conflicting findings and limitations.
Never fabricate citations, results, novelty claims, or cross-references.

Provide a plan template grounded in the actual upstream Plannotator templates after locating them in its source.
Include goal, evidence, scope and exclusions, decisions, phases, exact validation commands, exit criteria, risks, and open questions.
Integrate through a skill-local template and instructions for the host's existing review flow, not edits to Plannotator or its global configuration.

### Migration

Preserve useful material and the advisory checker from the existing skills rather than concatenating their entry points.
Move useful regression cases into the new suite and retain historical coverage.
Former routing negatives between the three writing skills become positive unified-writing cases where appropriate.
Retire `prose-writing`, `tech-writing`, and `proofreading` only after replacement coverage passes.
Update `AGENTS.md`, `README.md`, and active cross-references; do not rewrite historical reports merely to remove old names.
Keep `review` and `writing` distinct: review assesses substance; writing produces and improves communication.

## Execution phases

Each phase runs in a fresh session that reads this plan and the durable evidence files.
Applicable `manage-skill` instructions authorize fresh-context evaluation trials; unrelated delegation is outside scope.

### Phase 1: Verify sources and record baseline failures

- Clone or fetch t3dotgg/tstack under `~/Developer/github.com/t3dotgg/tstack` and Plannotator under `~/Developer/github.com/backnotprop/plannotator`.
- Inspect their applicable instructions and licenses before reusing content.
- Locate the actual council source and Plannotator templates and pin the reviewed commits.
- Download and extract the supplied PDF with an available tool; inspect its copyright statement before deciding whether to track it.
- Read the existing writing references, checker, and evaluation suites in full.
- Create evaluation cases before skill text, including observed baseline failures and near-miss prompts.
- Save fresh-context baseline transcripts to gitignored validation files.

Validation commands:

```sh
git status --short
python3 skills/manage-skill/scripts/eval_skill.py --help
python3 skills/manage-skill/scripts/eval_skill.py --skill skills/review --compare-without-skill
python3 skills/manage-skill/scripts/eval_skill.py --skill skills/writing --compare-without-skill
```

Inspect the runner before invocation and use its supported baseline-only path if comparison requires an existing skill.
Record the exact supported command in the evidence file before execution; do not create skill text merely to satisfy the runner.
Exit when source provenance and redistribution terms are resolved and real baseline failures are recorded for the behavior being taught.
Stop and report if the required baseline cannot run or no failure is observed.

### Phase 2: Implement and test the two skills

- Write minimal entry points, supporting references, source notices, and the plan template.
- Add the permitted STE reference artifacts.
- Add broad positive and negative coverage, with at least three trials per nondeterministic case.
- Test ordinary versus deep review, unavailable providers, non-PR artifacts, conflicting findings, and no unauthorized edits.
- Test prose creation, proofreading, technical accuracy, scientific citations, plan quality, brief replies, exact-output preservation, and no unnecessary workflow overhead.
- Preserve prior regressions and verify that the replacement fixes the observed failures.

Validation commands:

```sh
python3 skills/manage-skill/scripts/eval_skill.py --skill skills/review --static
python3 skills/manage-skill/scripts/eval_skill.py --skill skills/writing --static
python3 skills/manage-skill/scripts/eval_skill.py --skill skills/review --trials 3 --judge
python3 skills/manage-skill/scripts/eval_skill.py --skill skills/writing --trials 3 --judge
```

Exit when all enabled-mode cases pass and failed or unavailable trials are accounted for.
Record models, trial counts, and pass rates, not merely example outputs.

### Phase 3: Retire old entry points and verify the repository

- Run replacement-versus-baseline comparisons and preserve the old regression cases as migration sentinels.
- Remove the three superseded skill directories after migrating useful references, scripts, and cases.
- Update index rows and active links to the new names.
- Review the full diff for lost behavior, weakened assertions, unintended files, and missing notices.

Validation commands:

```sh
python3 skills/manage-skill/scripts/eval_skill.py --skill skills/writing --compare-without-skill
python3 skills/manage-skill/scripts/eval_skill.py --all --static --require-cases
python3 skills/manage-skill/tests/test_eval_skill.py
rg -n 'prose-writing|tech-writing|proofreading' AGENTS.md README.md skills
git diff --check
git diff --stat
git status --short
```

Classify remaining old-name matches as historical records, intentional migration evidence, or defects.
Exit when repository checks pass, active links resolve, and replacement coverage has not regressed.
Report changed paths, exact commands, trial pass rates, reference provenance, and any unresolved limitations.

## Evidence and open items

- Upstream skill: https://github.com/t3dotgg/tstack/blob/main/skills/council/SKILL.md
- Requested standard: https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf
- Usage-rights notice: https://www.asd-ste100.org/STE_downloads.html
- Plannotator source: https://github.com/backnotprop/plannotator
- arXiv version guidance: https://info.arxiv.org/help/versions.html
- The PDF URL responds, but web indexing treated it as binary; the standard's text and copyright statement have not yet been verified.
- The official STE site reserves rights and says the current edition's copyright statement controls usage.
- The exact Plannotator plan-template source is not yet located.
- Available evaluation models and three-provider capacity must be checked before running trials.
