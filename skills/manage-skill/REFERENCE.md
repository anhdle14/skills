# Manage a Skill - Reference

Deeper material for `manage-skill`. Load on demand; `SKILL.md` is the workflow and [EVALS.md](EVALS.md) is the eval contract.

## Classification

Name the kind of skill before writing it - it decides how you read the retirement step.

- **Capability** - teaches behavior the current model cannot perform consistently. Expected to become removable as models improve; retire it when the ablation shows the base model matches it.
- **Preference** - encodes repo conventions, safety boundaries, operational knowledge, or workflow. It lives as long as that contract holds, and a capable base model is not an argument for deleting it.

## Vocabulary

Predictability is the root virtue - the agent running the same *process* every time. These terms name the levers that serve it.

- **Context load** - tokens a skill costs the window. A model-invocable `description` pays this on *every* turn; the body pays it only when read.
- **Cognitive load** - what *you* must remember. A human-only skill trades context load for cognitive load: no description in reach, so you are the index that recalls it exists. When human-only skills outgrow memory, an index/router doc cures it.
- **Information hierarchy** - the ladder ranking material by how immediately the agent needs it: (1) in-skill **step** - an ordered action in `SKILL.md`; (2) in-skill **reference** - a fact consulted on demand; (3) **external reference** - pushed to a sibling file behind a pointer, loaded only when the pointer fires.
- **Completion criterion** - the condition ending a step. Make it *checkable* (can the agent tell done from not-done?) and, where it matters, *exhaustive* ("every modified model accounted for", not "produce a list"). Vague criteria invite premature completion.
- **Progressive disclosure** - moving material down the ladder (out of `SKILL.md` into a linked file) so the top stays legible. A **branch** - a distinct way the skill is used - is the cleanest disclosure test: inline what every branch needs, push behind a pointer what only some reach.
- **Co-location** - keep a concept's definition, rules, and caveats under one heading so reading one part brings its neighbours.
- **Leading word** - a compact concept already in the model's pretraining (*tracer bullet*, *fog of war*, *red*) that anchors a whole region of behaviour in a few tokens. Repeated across the skill it accrues a distributed definition; shared with your prompts and docs it also sharpens invocation.
- **Single source of truth** - one authoritative place per meaning, so a behaviour change is a one-place edit.

## Writing the description

For a **model-invocable** skill the description does two jobs: state what the skill is, and list the triggers that fire it. Every word is permanent context load, so prune it harder than the body.

- Third person, injected into the system prompt. Front-load the leading word.
- **NEVER summarize the workflow.** Agents follow the summary *instead of* reading the skill. A description that said "code review between tasks" made an agent do one review when the skill required two; stripping it to a pure trigger fixed it.
- One trigger per **branch**. Synonyms renaming a single branch are duplication - collapse them.
- Use words an agent would search for: error strings, symptoms ("flaky", "hangs"), tool and file names.

```yaml
# BAD - first person, vague, no trigger
description: I help you write async tests

# BAD - summarizes the workflow; agent follows this and skips the skill
description: Use when executing plans - dispatch a subagent per task with review between tasks

# GOOD - triggering conditions only, no workflow
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently
```

For a **human-only** skill the description is a one-line human-facing summary; strip the trigger phrasing since nothing selects on it.

Name skills verb-first / gerund for what they do: `creating-skills` > `skill-creation`, `root-cause-tracing` > `debugging-techniques`.

## Match the form to the failure

Classify the baseline failure before writing - the form that fixes one type backfires on another.

| Baseline failure | Right form | Wrong form |
|---|---|---|
| Skips a rule under pressure (knows better, does it anyway) | Prohibition + rationalization table + red-flags list | Soft guidance ("prefer…", "consider…") |
| Output has the wrong shape (bloated, buried verdict, restated spec) | Positive recipe / contract: state what the output *is*, its parts in order | Prohibition list ("don't restate", "never narrate") |
| Omits a required element it already produces | Structural: a REQUIRED field/slot in the template it fills | Prose reminders near the template |
| Behavior should depend on a condition | Conditional keyed to an observable predicate | Unconditional rule + exemption clauses |

Prohibitions backfire on *shaping* problems: under a competing incentive the agent negotiates with "don't X" and often produces more of it than no guidance at all. A recipe leaves nothing to negotiate. No nuance clauses ("don't X unless…") - they reopen the negotiation; express a real exception as its own conditional on an observable predicate. Exemption clauses don't scope ("this limit doesn't apply to code blocks" still suppresses code blocks) - restructure so the rule can't reach the exempt part.

## Bulletproofing discipline skills

Only for the discipline case (agent knows the rule, skips it under pressure).

- **Close every loophole explicitly.** Not "Delete it" but "Delete it. Start over. Don't keep it as reference, don't adapt it, don't look at it. Delete means delete."
- **Spirit vs letter.** State early: "Violating the letter of the rules is violating the spirit of the rules." Cuts off a whole class of rationalization.
- **Rationalization table.** Every excuse from baseline testing, paired with its reality.
- **Red-flags list.** Phrases that signal the agent is about to violate, each ending "→ STOP and start over."

## Testing (RED - GREEN - REFACTOR)

- **Pressure types** - stack them for discipline skills: time ("just ship it"), sunk cost ("you already wrote it"), authority ("the senior dev said skip it"), exhaustion (late in a long task).
- **Always run a no-guidance control.** If the control doesn't exhibit the failure, there is nothing to fix - don't author the guidance.
- **Micro-test wording before full scenarios.** Full pressure runs are the final gate but slow. Verify wording first: fresh-context sample per call, system prompt = the realistic full context, user message = a tempting task; 5+ reps per variant; read every flagged match by hand (template echoes masquerade as hits); treat variance as a metric - five different interpretations means the wording isn't binding, tighten the form before adding words.
- Test by skill type: discipline → complies under stacked pressure; technique → applies correctly to a new scenario; pattern → recognizes when it applies (and when not); reference → retrieves and applies the right fact.

## No-op review

An instruction earns its context cost only when an eval can distinguish its presence from its absence. Delete lines that ask the agent to:

- write high-quality code, be careful, or make output readable;
- follow best practices without naming a specific practice;
- read files before changing them, or any other behavior the harness already requires.

## Failure modes

Diagnose a misbehaving skill by name.

- **Premature completion** - ending a step before it's genuinely done. Fix the completion criterion first (cheap); only if it's irreducibly fuzzy *and* you observe the rush, split the sequence to hide later steps.
- **Duplication** - the same meaning in more than one place. Costs maintenance and tokens and inflates the meaning's apparent rank. Collapse to a single source of truth or a leading word.
- **Sediment** - stale layers that accrete because adding feels safe and removing feels risky. The default fate without a pruning discipline.
- **Sprawl** - simply too long even when every line is live. Cure with the ladder: disclose reference behind pointers, split by branch or sequence.
- **No-op** - a line the model already obeys by default, so you pay load to say nothing. Test: does it change behaviour vs the default? A weak leading word ("be thorough" when the agent already is) is a no-op; fix with a stronger word ("relentless"), not more prose.
