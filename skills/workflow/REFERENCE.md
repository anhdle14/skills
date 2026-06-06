# Workflow Pattern Reference

Full boundary definitions, anti-confusion notes, and failure modes for the
six workflow patterns.

---

## Pattern 1 — Classify and Act

**What it does:** A classifier decides which branch handles the input. Only
that branch executes.

**Structure:**
```
input → [Classifier] → branch A
                     → branch B
                     → branch C   (only one fires)
```

**Hard boundary:** Exactly one branch runs per input. If multiple branches
could plausibly apply, the classifier must be redesigned to produce a single
winner, or the task belongs in Fan Out.

**Use when:**
- Inputs are categorically different and require genuinely different handling
- Sending all inputs through all branches would be wasteful or wrong

**Distinct from Fan Out and Synthesize:** Fan Out runs ALL branches
intentionally. Classify and Act runs EXACTLY ONE.

**Failure mode:** Classifier returns ambiguous or overlapping categories.
Fix: add a tie-breaker rule or merge the overlapping branches.

---

## Pattern 2 — Fan Out and Synthesize

**What it does:** Work splits into N independent parallel subtasks. All run.
Results merge into a single output.

**Structure:**
```
input → [Agent A] ──┐
input → [Agent B] ──┤ → [Synthesizer] → output
input → [Agent C] ──┘
```

**Hard boundary:** All branches run. If some branches are conditional,
that's Classify and Act with parallelism inside a branch, not Fan Out.

**Use when:**
- Task has genuinely independent dimensions (e.g. review for bugs + style + security)
- Parallelism reduces latency and all results are needed

**Distinct from Tournament:** Fan Out combines all results. Tournament
eliminates candidates down to one.

**Failure mode:** Branches are not independent — they depend on each other's
output. Fix: sequence the dependent ones; only parallelize the independent ones.

---

## Pattern 3 — Adversarial Verification

**What it does:** A generator produces a claim. A separate adversary agent
tries to invalidate it. Only claims that survive the attack are accepted.

**Structure:**
```
input → [Generator] → claim → [Adversary] → passes? → output
                                           → fails?  → rejection / refinement
```

**Hard boundary:** The adversary's goal is strictly to INVALIDATE — find
flaws, counterexamples, contradictions. It is not a reviewer offering
improvements; it is an opponent trying to break the claim.

**Use when:**
- Output correctness is critical and hard to verify by inspection
- False positives are costly (security, legal, factual claims)
- You need independent confirmation that a solution holds under attack

**Distinct from Generate and Filter:** Generate and Filter applies pre-defined
criteria mechanically. Adversarial Verification uses active reasoning to
discover unanticipated flaws.

**Distinct from Loop Until Done:** Adversarial is a single challenge round
(or a fixed number of rounds). Loop Until Done iterates until a convergence
condition is met, not until an adversary is satisfied.

**Failure mode:** Adversary and generator share context and "agree" too
easily. Fix: give the adversary only the claim, not the generator's reasoning.

---

## Pattern 4 — Generate and Filter

**What it does:** Generate a large candidate set, then apply a pre-defined
filter to retain only those meeting absolute criteria.

**Structure:**
```
input → [Generator] → [candidate 1, candidate 2, ..., candidate N]
                   → [Filter: criterion A AND B AND C]
                   → [passing candidates]
```

**Hard boundary:** Filter criteria must be defined BEFORE generation. They
are absolute (pass/fail), not comparative. If you find yourself picking the
"best" of the passing candidates, you have moved into Tournament territory.

**Use when:**
- Solution space is large and diverse; breadth is valuable first
- Acceptance criteria can be stated as hard rules
- Multiple passing candidates are an acceptable (or desired) outcome

**Distinct from Tournament:** Generate and Filter keeps everything above the
bar. Tournament picks the single best from among peers.

**Distinct from Adversarial Verification:** Filter is mechanical rule
application. Adversary uses reasoning to surface flaws not covered by the rules.

**Failure mode:** Filter criteria are vague or comparative ("pick the better
ones"). Fix: convert each criterion into a binary yes/no test, or route to
Tournament.

---

## Pattern 5 — Tournament

**What it does:** Candidates compete in head-to-head comparisons. The winner
of each bout advances. The process continues until one candidate remains.

**Structure:**
```
[A vs B] → winner
[C vs D] → winner
     ↓        ↓
   [winner vs winner] → champion
```

Or: round-robin rankings, bracket elimination — the mechanism varies, but
relative comparison drives elimination.

**Hard boundary:** Judgment is RELATIVE ("A is better than B for this task"),
not absolute ("A meets the threshold"). If you have an absolute threshold,
use Generate and Filter first, then Tournament on the finalists if needed.

**Use when:**
- Quality is easier to judge comparatively than against an absolute bar
- You need exactly one winner, not a passing set
- The number of valid candidates is small enough for pairwise comparison

**Distinct from Fan Out and Synthesize:** Fan Out combines all outputs.
Tournament eliminates all but one.

**Distinct from Generate and Filter:** Filter applies absolute rules.
Tournament applies relative judgment.

**Failure mode:** Comparing candidates on different criteria in different
bouts, producing inconsistent rankings. Fix: define a single judging rubric
used in every comparison.

---

## Pattern 6 — Loop Until Done

**What it does:** An agent attempts a task. An evaluator checks against an
exit condition. If not met, the agent refines and tries again.

**Structure:**
```
input → [Agent] → output → [Evaluator] → exit condition met? → done
                                       → not met?           → feedback → [Agent] (loop)
```

**Hard boundary:** The exit condition must be stated BEFORE the loop starts.
If you don't know what "done" looks like, the loop will not terminate
predictably.

**Use when:**
- Quality threshold is known but the number of iterations is not
- Refinement from feedback is the right mechanism (not adversarial attack)
- Tasks like: code that must pass tests, prose that must meet a rubric

**Distinct from Adversarial Verification:** Loop Until Done refines toward a
goal. Adversarial Verification challenges a claim to break it — it does not
help the generator improve.

**Failure mode:** Exit condition is vague ("looks good"), causing infinite
refinement. Fix: make the exit condition measurable or add a max-iteration
cap with a fallback.

---

## Chaining Anti-Patterns

| Chain | Why it fails |
|-------|--------------|
| Tournament → Tournament | Second tournament implies first had unclear criteria; define one rubric instead |
| Loop → Loop (nested) | Inner loop's exit condition is usually the outer loop's criterion; flatten into one loop |
| Generate and Filter → Generate and Filter | Second filter means criteria were incomplete; combine into one filter pass |
| Adversarial → Adversarial (same adversary) | Redundant; use a stronger or different adversary in one pass |
| Classify → Classify (same input) | Overlapping classifiers; redesign into one classifier with more branches |

---

## Decision Tree

```
Single prompt enough? → YES → stop, use a single prompt
         ↓ NO
Input types radically different? → YES → Classify and Act
         ↓ NO
All dimensions needed, independent? → YES → Fan Out and Synthesize
         ↓ NO
Must survive active attack? → YES → Adversarial Verification
         ↓ NO
Absolute pass/fail criteria, breadth first? → YES → Generate and Filter
         ↓ NO
Relative quality judgment, need one winner? → YES → Tournament
         ↓ NO
→ Loop Until Done
```
