# Orchestration Examples

One end-to-end trace of the Conductor loop in [SKILL.md](SKILL.md), showing decomposition, parallel fan-out over disjoint access lists, a recursion on a hard sub-part with budget decrement, and synthesis.

---

## Example — "Build a CLI that summarizes a CSV and flags anomalies"

A multi-part task: parse the CSV, compute summary statistics, detect anomalous rows, and wire it into a CLI. Independent parts can fan out; one part is hard enough to recurse on.

### Step 0 — Decompose (Thinker)

Write the plan to `progress.md` before running anything:

```
budgets: turns=5, recursion_depth=2
steps:
  1 parse + schema infer        (independent)
  2 summary statistics          (independent)
  3 anomaly detection           (hard — likely recurse)
  4 CLI wiring + synthesis      (depends on 1,2,3)
```

### Steps 1-3 — Spec and fan out

The three computation steps have disjoint access lists, so they run in parallel (Tier A: three sub-agents; Tier B: role-played in sequence, each output written to a file).

```
model_id    = [ coding_worker,        reasoning_worker,     SELF,                coding_worker ]
subtask     = [ "Parse the CSV and
                 infer column types;
                 return a typed schema
                 and row iterator",
                "Given a typed schema,
                 list the summary stats
                 to compute per column
                 type; return the list",
                "Detect anomalous rows
                 robustly across mixed
                 column types",
                "Wire steps into a CLI
                 with one summarize
                 command; return runnable
                 code" ]
access_list = [ [],                   [0],                  [0],                 [0, 1, 2] ]
```

Step 1 reads nothing; steps 2 and 3 both read step 1's schema (so they sequence after 1 but are independent of each other and fan out together); step 4 reads all three.

### Step 3 — Recurse on the hard part

Anomaly detection across mixed column types is too broad for one pass, so `model_id[3] = SELF`. Recurse with a **smaller** subtask and decremented budgets (`recursion_depth: 2 -> 1`):

```
sub-steps:
  3a numeric outliers   (z-score / IQR)     access []
  3b categorical rares  (frequency floor)   access []
  3c merge 3a, 3b into a per-row flag        access [3a, 3b]
```

3a and 3b have disjoint access lists → fan out. 3c synthesizes. The recursion returns a single per-row anomaly flag to its parent step, exactly as any worker would. It shrank (mixed-type detection → two typed detectors + a merge), so the recursion was allowed.

### Step 4 — Synthesize (Worker) + check

`coding_worker` assembles the CLI from steps 1, 2, and 3. Because correctness matters, hand the assembled result to `/trinity` rather than eyeballing it; record its verdict in `progress.md`.

### Stop

Synthesis produced, check passed, two of five turns spent (the recursion counted against the shared budget). Return the CLI, the step trace, the verifier verdict, and `turns=2/5`. Re-read `progress.md` before declaring done.

---

## What this trace demonstrates

- **Difficulty-matched steps** — four top-level steps for a genuinely multi-part task, not for padding.
- **Access list as dependency graph** — disjoint lists fan out, overlapping lists sequence.
- **Recursion that shrinks** — `SELF` only on the hard part, with a smaller subtask and a decremented budget.
- **Deferred verification** — the check is handed to `/trinity`, not re-implemented here.
- **Persistence** — plan and every output live in `progress.md`, re-read before the done check.
