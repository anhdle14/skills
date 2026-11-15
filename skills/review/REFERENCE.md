# Review Reference

Use the artifact's acceptance criteria and source of truth. Report only findings that could change a decision or outcome.

## Findings

For every finding, include:

- **Severity:** blocker, high, medium, low, or note. Explain priority through impact, not labels alone.
- **Location:** `path:line`, section, step, or a short identifying quote.
- **Evidence:** the observed behavior or exact conflicting statements.
- **Impact:** who or what is affected and under which conditions.
- **Suggested change:** a concrete correction or the missing evidence needed to decide.

Do not pad a review with stylistic preferences. Put questions, assumptions, and optional improvements in separate sections. A clean review still states its scope and limitations.

## Code and diffs

- Trace changed behavior through callers, state transitions, error paths, and relevant tests.
- Look for regressions, data loss, security boundaries, race conditions, compatibility changes, and missing failure handling.
- Check that tests exercise the reported behavior and do not weaken prior guarantees.
- Run focused checks only when safe and useful. Report exact commands and results; do not imply tests ran when they did not.

## Architecture, designs, and plans

- Compare proposal to stated goals, constraints, and non-goals.
- Check dependencies and ordering, ownership, migration and rollback, failure modes, operational burden, and alternatives where consequential.
- For plans, check each phase has concrete validation and exit criteria. Flag missing decisions and open questions that prevent execution.
- Distinguish a defect in the proposal from a question that needs owner input.

## Documents and research

- Verify factual claims against implementation, supplied source material, or primary sources as appropriate.
- Check whether citations support the attached claims. For research, identify publication status and conflicting evidence where relevant.
- Do not rewrite for style unless requested. Route proofreading and prose edits to the `writing` skill.

## Multiple reviewers

Select reviewers from distinct model developers when the host exposes reliable model identities. A shared gateway does not by itself make models the same developer, but report the gateway and model identity so the user can judge independence. Do not infer vendor identity from a model nickname alone. If three independent reviewers are unavailable, report exactly who was available and continue only if useful; label the result as partial, not a completed council. Keep prompts scoped and read-only. Independently verify findings before reporting them.
