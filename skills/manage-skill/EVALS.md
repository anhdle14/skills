# Skill Evaluation Guidance

How to build and grade the eval suite the Iron Law depends on. The runner is `scripts/eval_skill.py`.

## Case set

Start with at least three positive and three negative cases for a small atomic skill; 10 to 20 prompts when the behavior is broad. Use real prompts - the ones that produced the failure, and the near-misses that wrongly loaded the skill.

- **Positive cases** verify intended triggering *and* a usable outcome.
- **Negative cases** verify that nearby but irrelevant tasks leave the skill alone. A model-invocable skill without negative cases has an untested trigger contract, and `--static` rejects it.
- Every fixed failure becomes a permanent regression case. Cases are never deleted for passing.

Human-only skills cannot be trigger-tested (nothing selects on their description), so their suites carry positive behavior cases only. The runner injects their `SKILL.md` the way `/skill:name` does and skips the trigger assertion.

## Grade outcomes deterministically, in this order

1. Process exit status.
2. Expected or forbidden tool calls.
3. Expected files or file contents.
4. Response patterns that represent a concrete contract.
5. Structured LLM judgment (`--judge`), only for qualitative outcomes the four above cannot express.

Do not require one exact reasoning path when several paths produce the correct outcome. Assert on the artifact, not the narration.

## Isolation and trials

Each trial runs in a fresh temporary workspace with sessions, extensions, ambient skills, and context files disabled, so the only variable is the skill under test. Fixtures are copied in via `workspace`; setup runs as `startup` argument arrays, never shell strings.

Case prompts are executed verbatim by a real agent, so a suite is untrusted input: read any suite you did not author - including one arriving in a pull request - before running trials against it.

Run at least three trials for anything nondeterministic and report pass rates. Record the model with the result - a suite that passes on one model says nothing about another.

## Case schema

```json
{
  "skill": "tech-writing",
  "trials": 3,
  "cases": [
    {
      "name": "api-reference-from-spec",
      "prompt": "Write the API reference for our internal warmcache service from this spec.",
      "should_trigger": true,
      "tools": ["read", "write", "bash"],
      "workspace": "fixtures/warmcache",
      "startup": [["git", "init"]],
      "timeout_seconds": 300,
      "expect": {
        "response_regex": ["unverified", "scope"],
        "forbid_response_regex": ["I assumed the host"],
        "tool_names": ["write"],
        "read_path_regex": ["REFERENCE\\.md"],
        "file_exists": ["docs-notes.md"],
        "file_regex": { "warmcache.md": "This document does not cover" },
        "judge": "The doc marks every unverified claim instead of inventing a value."
      }
    }
  ]
}
```

Required per case: `name`, `prompt`, `should_trigger`. Everything else is optional.

## Regression gate

Run `--static` on every skill diff. Run model-backed cases before merging any change to a description, invocation mode, or behavior. A change is acceptable when it fixes or adds coverage **without** reducing established pass rates.

## Retirement ablation

`--compare-without-skill` runs identical cases with the skill loaded and with it absent. Baseline (skill-absent) failures never fail the run - they are the measurement. Equivalent pass rates across supported models mean a capability skill no longer earns its context; keep its cases as sentinels after deletion.

## Source

The lifecycle and eval design follow Philipp Schmid's [Don't Ship Skills Without Evals](https://www.youtube.com/watch?v=0vphxNt4wyk) and [Practical Guide to Evaluating and Testing Agent Skills](https://www.philschmid.de/testing-skills), adapted to Pi's Agent Skills and this repo's conventions.
