# Workflow Pattern Catalog

The composable agentic patterns the ship workflow draws on. Each has a hard boundary;
this catalog is the single source of truth so no phase re-derives them.

`ship-slice` composes **Fan Out and Synthesize** (independent slices in parallel) plus
**Loop Until Done** (drive each slice to green). `ship-review` composes **Adversarial
Verification** (attack the deliverable to break it).

## When a single pass is enough

Do NOT reach for a pattern if the work fits one context window with room to spare, needs no
side effects, can be quality-checked in the same pass that produces it, and is cheap to
retry by hand. Patterns add latency, token cost, and coordination overhead; use them only
when the single-pass ceiling is the real bottleneck.

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

```text
Single pass enough?                            -> YES -> use a single pass
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

**Hard boundary:** exactly one branch runs per input. If multiple branches could plausibly
apply, redesign the classifier to produce a single winner, or the task belongs in Fan Out.

**Failure mode:** classifier returns ambiguous or overlapping categories. Fix: add a
tie-breaker rule or merge the overlapping branches.

## Pattern 2 - Fan Out and Synthesize

Work splits into N independent parallel subtasks; all run; results merge into one output.
This is how `ship-slice` runs the independent slices in a phase.

**Hard boundary:** all branches run. If some branches are conditional, that is Classify and
Act with parallelism inside a branch, not Fan Out.

**Failure mode:** branches are not independent — they depend on each other's output. Fix:
sequence the dependent ones; only parallelize the independent ones.

## Pattern 3 - Adversarial Verification

A generator produces a claim; a separate adversary tries to invalidate it; only claims that
survive the attack are accepted. This is how `ship-review` interrogates deliverables.

**Hard boundary:** the adversary's goal is strictly to INVALIDATE — find flaws,
counterexamples, contradictions. It is an opponent trying to break the claim, not a
reviewer offering polish.

**Distinct from Loop Until Done:** Adversarial is a single challenge round (or a fixed
number); Loop Until Done iterates until a convergence condition is met.

**Failure mode:** adversary and generator share context and agree too easily. Fix: give the
adversary only the claim and the spec, not the generator's reasoning.

## Pattern 4 - Generate and Filter

Generate a large candidate set, then apply a pre-defined filter to retain only those meeting
absolute criteria.

**Hard boundary:** filter criteria must be defined BEFORE generation and are absolute
(pass/fail), not comparative.

**Failure mode:** filter criteria are vague or comparative ("pick the better ones"). Fix:
convert each criterion into a binary yes/no test, or route to Tournament.

## Pattern 5 - Tournament

Candidates compete in head-to-head comparisons; the winner of each bout advances until one
remains.

**Hard boundary:** judgment is RELATIVE ("A is better than B"), not absolute ("A meets the
threshold").

**Failure mode:** comparing candidates on different criteria in different bouts. Fix: define
a single judging rubric used in every comparison.

## Pattern 6 - Loop Until Done

An agent attempts a task; an evaluator checks against an exit condition; if unmet, the agent
refines and tries again. This is how `ship-slice` drives a slice to green.

**Hard boundary:** the exit condition must be stated BEFORE the loop starts. If you do not
know what "done" looks like, the loop will not terminate predictably.

**Failure mode:** exit condition is vague ("looks good"), causing infinite refinement. Fix:
make the exit condition measurable and add a max-iteration cap with a fallback.

---

## Chaining

Patterns compose. The rule: each pattern's exit condition must be explicit before handing
off to the next — never let a loop hand off mid-iteration.

| Chain | When to use |
|-------|-------------|
| Fan Out -> Loop Until Done | Parallelize slices; refine each until it converges |
| Adversarial -> Loop Until Done | Adversary surfaces a flaw; loop drives a fix |
| Generate and Filter -> Tournament | Filter removes invalid; tournament picks the best finalist |

### Chaining anti-patterns

| Chain | Why it fails |
|-------|--------------|
| Loop -> Loop (nested) | Inner loop's exit condition is usually the outer loop's criterion; flatten |
| Adversarial -> Adversarial (same adversary) | Redundant; use a stronger or different adversary |
| Tournament -> Tournament | Implies the first had unclear criteria; define one rubric |
