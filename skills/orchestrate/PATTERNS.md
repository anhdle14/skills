# Workflow Pattern Catalog

The six composable agentic workflow patterns the Conductor loop in [SKILL.md](SKILL.md) draws on.
Each has a hard boundary; this catalog is the single source of truth for their definitions,
so neither this skill nor `/trinity` re-derives them.

## When a single prompt is enough

Do NOT reach for a pattern if the task fits one context window with room to spare, needs no
external tools or side effects, can be quality-checked in the same pass that produces it, and is
cheap to retry by hand. Patterns add latency, token cost, and coordination complexity; use them
only when the single-prompt ceiling is the actual bottleneck.

## Quick reference

| Pattern | Shape | Hard constraint |
|---------|-------|-----------------|
| **Classify and Act** | input -> ONE branch executes | Only one branch runs |
| **Fan Out and Synthesize** | input -> N parallel agents -> merged output | ALL branches run; results combined |
| **Adversarial Verification** | claim -> adversary attacks -> surviving claim | Adversary goal is to INVALIDATE |
| **Generate and Filter** | input -> many candidates -> filtered set | Criteria are absolute, pre-defined |
| **Tournament** | candidates -> head-to-head -> winner | Comparison is RELATIVE, not absolute |
| **Loop Until Done** | attempt -> eval exit condition -> refine | Iterative; exit condition explicit upfront |

## Choosing a pattern

```
Single prompt enough?                          -> YES -> use a single prompt
Input types radically different?               -> YES -> Classify and Act
All dimensions needed, independent?            -> YES -> Fan Out and Synthesize
Must survive active attack?                    -> YES -> Adversarial Verification
Absolute pass/fail criteria, breadth first?    -> YES -> Generate and Filter
Relative quality judgment, need one winner?    -> YES -> Tournament
Quality threshold known, iteration count not?  -> YES -> Loop Until Done
```

---

## Pattern 1 - Classify and Act

A classifier decides which branch handles the input; only that branch executes.

**Hard boundary:** exactly one branch runs per input. If multiple branches could plausibly apply,
redesign the classifier to produce a single winner, or the task belongs in Fan Out.

**Use when:** inputs are categorically different and need genuinely different handling, and sending
all inputs through all branches would be wasteful or wrong.

**Distinct from Fan Out and Synthesize:** Fan Out runs ALL branches intentionally; Classify and Act
runs EXACTLY ONE.

**Failure mode:** classifier returns ambiguous or overlapping categories. Fix: add a tie-breaker
rule or merge the overlapping branches.

## Pattern 2 - Fan Out and Synthesize

Work splits into N independent parallel subtasks; all run; results merge into one output.

**Hard boundary:** all branches run. If some branches are conditional, that is Classify and Act
with parallelism inside a branch, not Fan Out.

**Use when:** the task has genuinely independent dimensions (e.g. review for bugs + style +
security) and parallelism reduces latency while all results are needed.

**Distinct from Tournament:** Fan Out combines all results; Tournament eliminates candidates down
to one.

**Failure mode:** branches are not independent - they depend on each other's output. Fix: sequence
the dependent ones; only parallelize the independent ones.

## Pattern 3 - Adversarial Verification

A generator produces a claim; a separate adversary tries to invalidate it; only claims that survive
the attack are accepted.

**Hard boundary:** the adversary's goal is strictly to INVALIDATE - find flaws, counterexamples,
contradictions. It is an opponent trying to break the claim, not a reviewer offering improvements.

**Use when:** correctness is critical and hard to verify by inspection, false positives are costly
(security, legal, factual claims), or you need independent confirmation a solution holds under attack.

**Distinct from Generate and Filter:** Generate and Filter applies pre-defined criteria mechanically;
Adversarial Verification uses active reasoning to discover unanticipated flaws.

**Distinct from Loop Until Done:** Adversarial is a single challenge round (or a fixed number);
Loop Until Done iterates until a convergence condition is met, not until an adversary is satisfied.

**Failure mode:** adversary and generator share context and agree too easily. Fix: give the
adversary only the claim, not the generator's reasoning.

## Pattern 4 - Generate and Filter

Generate a large candidate set, then apply a pre-defined filter to retain only those meeting
absolute criteria.

**Hard boundary:** filter criteria must be defined BEFORE generation and are absolute (pass/fail),
not comparative. If you find yourself picking the "best" of the passing candidates, you have moved
into Tournament territory.

**Use when:** the solution space is large and diverse (breadth is valuable first), acceptance
criteria can be stated as hard rules, and multiple passing candidates are an acceptable outcome.

**Distinct from Tournament:** Generate and Filter keeps everything above the bar; Tournament picks
the single best from among peers.

**Failure mode:** filter criteria are vague or comparative ("pick the better ones"). Fix: convert
each criterion into a binary yes/no test, or route to Tournament.

## Pattern 5 - Tournament

Candidates compete in head-to-head comparisons; the winner of each bout advances until one remains
(bracket elimination, round-robin - the mechanism varies, but relative comparison drives elimination).

**Hard boundary:** judgment is RELATIVE ("A is better than B for this task"), not absolute
("A meets the threshold"). With an absolute threshold, use Generate and Filter first, then
Tournament on the finalists if needed.

**Use when:** quality is easier to judge comparatively than against an absolute bar, you need
exactly one winner, and the candidate count is small enough for pairwise comparison.

**Distinct from Fan Out and Synthesize:** Fan Out combines all outputs; Tournament eliminates all
but one.

**Failure mode:** comparing candidates on different criteria in different bouts, producing
inconsistent rankings. Fix: define a single judging rubric used in every comparison.

## Pattern 6 - Loop Until Done

An agent attempts a task; an evaluator checks against an exit condition; if unmet, the agent refines
and tries again.

**Hard boundary:** the exit condition must be stated BEFORE the loop starts. If you do not know
what "done" looks like, the loop will not terminate predictably.

**Use when:** the quality threshold is known but the iteration count is not, and refinement from
feedback (not adversarial attack) is the right mechanism - code that must pass tests, prose that
must meet a rubric.

**Distinct from Adversarial Verification:** Loop Until Done refines toward a goal; Adversarial
Verification challenges a claim to break it and does not help the generator improve.

**Failure mode:** exit condition is vague ("looks good"), causing infinite refinement. Fix: make
the exit condition measurable or add a max-iteration cap with a fallback.

---

## Chaining

Patterns compose. The rule: each pattern's exit condition must be explicit before handing off to
the next - never let a loop hand off to a tournament mid-iteration.

| Chain | When to use |
|-------|-------------|
| Classify -> Fan Out | Route to a parallel handler per category |
| Generate and Filter -> Tournament | Filter removes invalid; tournament picks best from finalists |
| Adversarial -> Loop Until Done | Adversary surfaces flaw; loop drives generator to fix it |
| Fan Out -> Loop Until Done | Parallelize subtasks; refine each until it converges |
| Classify -> Loop Until Done | Route to the right retry strategy per input type |

### Chaining anti-patterns

| Chain | Why it fails |
|-------|--------------|
| Tournament -> Tournament | Second tournament implies the first had unclear criteria; define one rubric |
| Loop -> Loop (nested) | Inner loop's exit condition is usually the outer loop's criterion; flatten into one |
| Generate and Filter -> Generate and Filter | Second filter means criteria were incomplete; combine into one pass |
| Adversarial -> Adversarial (same adversary) | Redundant; use a stronger or different adversary in one pass |
| Classify -> Classify (same input) | Overlapping classifiers; redesign into one classifier with more branches |
