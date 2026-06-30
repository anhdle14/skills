# Terminal-Bench A/B — orchestrate+trinity workflow vs plain prompting

> **Historical.** This A/B benchmarked an earlier `orchestrate`+`trinity` workflow
> scaffold (since superseded by the `ship` pipeline). The runs and findings are kept as a
> record of the verify-before-complete mechanism; the skills they reference no longer exist
> in `skills/`.

**Question:** does running the orchestrate+trinity workflow protocol beat a plain
agentic loop on the *same model*, scored on real Terminal-Bench tasks?

This doc has two runs of the same A/B, on two different shared substrates:

- **Run 2 — Claude Opus 4.8** (2026-06-23, below) — re-run on Claude instead of the
  OpenAI model, via a Bedrock-compatible proxy.
- **Run 1 — gpt-5.5** (original, further down) — the first run, on the OpenAI model.

---

## Run 2 — Claude Opus 4.8 (2026-06-23)

Re-ran the identical A/B with the shared model swapped from `gpt-5.5` to **Claude
Opus 4.8**, reached through a Bedrock-compatible proxy (`bedrock/global.anthropic.
claude-opus-4-8`, `temperature=1`, 1 attempt, 600s/task). Same 10 tasks, same two
arms (`terminus` vs `workflow-terminus`), same harness.

### Result (Opus 4.8)

| task                    | A (plain)      | B (workflow)   |                   |
| ----------------------- | -------------- | -------------- | ----------------- |
| chess-best-move         | **PASS**       | fail           | **A wins** (nondeterministic task) |
| configure-git-webserver | fail           | fail           | same              |
| csv-to-parquet          | PASS           | PASS           | same              |
| fibonacci-server        | fail           | fail           | same              |
| fix-git                 | PASS           | PASS           | same              |
| fix-permissions         | PASS           | PASS           | same              |
| grid-pattern-transform  | PASS           | PASS           | same              |
| heterogeneous-dates     | PASS           | PASS           | same              |
| nginx-request-logging   | fail           | fail           | same              |
| openssl-selfsigned-cert | PASS           | PASS           | same              |
| **accuracy**            | **7/10 (70%)** | **6/10 (60%)** | **−10pp**         |

On Opus the two arms tied on 9 of 10 tasks. The only difference is
`chess-best-move` — and it's **not** the workflow gate firing: B wrote `c3h3 g2g4`
(one of the two moves wrong; test wants `{e2e4, g2g4}`) while A wrote the correct
set. That's a *quality* miss on a hard puzzle, on the very task flagged as
nondeterministic in Run 1 (it flipped pass/fail there too, and is the 600s-timeout
task). Both arms genuinely failed the same other 3 (`configure-git-webserver`,
`fibonacci-server`, `nginx-request-logging`).

So on this substrate the workflow protocol added **no correctness** and lost a
coin-flip task. This is the opposite sign from Run 1's +20pp — but it lands exactly
on the same mechanism reading: the workflow's verify-before-complete gate only helps
when naive execution *declares premature success*. Opus's plain loop already
verifies its own work and doesn't stop short on these tasks (it solved `fix-git` and
`csv-to-parquet` unaided — the two tasks where gpt-5.5's plain loop needed the gate),
so there was nothing for the gate to catch, and the extra role-play scaffolding only
added variance. The mechanism reading remains: scaffolding helps on the margin
where a model stops short, not on tasks a capable model already nails.

### Cost (Opus 4.8)

Summed across all 10 tasks (terminus reports per-trial token totals):

| arm          | input tokens | output tokens | total     |
| ------------ | ------------ | ------------- | --------- |
| A (plain)    | 640,092      | 23,249        | 663,341   |
| B (workflow) | 556,357      | 22,194        | 578,551   |

B was not more expensive here in aggregate (A's totals were inflated by its longer,
ultimately-successful chess run). Per-task episode overhead for B was small (+0–1
episode on most tasks). On this run, the workflow arm cost about the same and scored
one task lower — no quality-per-token case for it on these checkable tasks.

### Validity checks (Opus 4.8)

- **All verdicts genuine.** Every task in both arms has `failure_mode=unset` (a real
  task pass/fail), except B's `configure-git-webserver` which was `test_timeout` —
  still a genuine both-fail, not a harness error. No `unknown_agent_error`.
- **Zero auth casualties.** Auth-expiry count over the whole ~18-min two-arm run:
  0. The token keep-alive (see Substrate compat) refreshed the bearer token across
  both arms; the Run-1 tail-task expiry failure mode did not recur.
- **Substrate parity.** Both arms loaded the identical `sitecustomize.py` compat
  layer; it touches only auth + response-shape plumbing, never either arm's prompt,
  model, or execution path.

### Substrate compat (how Claude was reached, and why it can't bias the A/B)

`terminus` is a LiteLLM agent; pointing it at Claude needed `bedrock/...` +
`api_base` + `AWS_BEARER_TOKEN_BEDROCK` (plus `uvx --with boto3`). Three
proxy/model quirks forced compatibility shims, all in `sitecustomize.py`
(auto-loaded via `PYTHONPATH`), all applied **identically to both arms** so they
cannot move the A/B:

1. **Token keep-alive.** The JWT lives ~60 min; a two-arm run outlives it. Wrapped
   `litellm.completion` to re-fetch the token every ~20 min and on any auth error.
2. **Forced schema-in-prompt.** LiteLLM advertises `response_format` as supported for
   Bedrock Claude, but the provider proxy rejects it. Dropped it from the model's
   supported-params so terminus falls back to injecting the JSON schema into the
   prompt — its own built-in path for non-structured-output models.
3. **Response normalization.** In that fallback Claude wraps JSON in ```json fences /
   prose and occasionally omits a required field. Strip to the `{…}` slice and fill
   missing required fields with **safe** defaults (`is_task_complete=False` = "keep
   working", so a missing field can never fabricate a pass) before terminus parses.

Reproduce Run 2: set `TB_BEDROCK_API_BASE` and `TB_BEDROCK_TOKEN_SCOPE`, then run
`bash docs/evals/tbench/run_claude.sh both` (needs Docker and `az`).

---

## Run 1 — gpt-5.5 (original)

### Setup

- Harness: Terminal-Bench `terminal-bench-core==0.1.1`, Docker-per-task.
- Both arms: `gpt-5.5` via an OpenAI-compatible proxy, `temperature=1`, 1 attempt, 600s/task.
- **A (baseline):** stock `terminus` agent — a plain single-model agentic loop ("normal prompt").
- **B (treatment):** `workflow-terminus` (`workflow_agent.py`) — identical loop, schema,
  model, temperature, and execution path; the ONLY change is a workflow protocol injected
  into the prompt (per-task routing: trinity's verify-before-complete gate for single
  tasks, orchestrate's decompose→synthesize for multi-part tasks).

Isolating the variable to "workflow scaffolding vs plain prompt" is the whole point — same
substrate, one knob.

### Result (gpt-5.5)

| task                    | A (plain)      | B (workflow)   |                  |
| ----------------------- | -------------- | -------------- | ---------------- |
| chess-best-move         | fail           | fail           | (both timed out) |
| configure-git-webserver | fail           | fail           | same             |
| csv-to-parquet          | fail           | **PASS**       | **B wins**       |
| fibonacci-server        | PASS           | PASS           | same             |
| fix-git                 | fail           | **PASS**       | **B wins**       |
| fix-permissions         | PASS           | PASS           | same             |
| grid-pattern-transform  | PASS           | PASS           | same             |
| heterogeneous-dates     | PASS           | PASS           | same             |
| nginx-request-logging   | fail           | fail           | same             |
| openssl-selfsigned-cert | PASS           | PASS           | same             |
| **accuracy**            | **5/10 (50%)** | **7/10 (70%)** | **+20pp**        |

The workflow arm won 2 tasks the baseline failed (`csv-to-parquet`, `fix-git`) and lost
none. Both arms failed the same 3 tasks. The gains are on tasks where naive execution
declares premature success — the trinity verify-before-complete gate ("check real output
before is_task_complete") is the plausible mechanism.

### Rerun of the 3 shared failures (2026-06-23)

Re-ran ONLY the tasks both arms failed above, same configs, to see if any were flippable.

| task                    | A (plain)             | B (workflow)        |                    |
| ----------------------- | --------------------- | ------------------- | ------------------ |
| chess-best-move         | fail (`agent_timeout`) | **PASS**            | **B flips to win** |
| configure-git-webserver | fail (`unset`)        | fail (`unset`)      | still both fail    |
| nginx-request-logging   | fail (7/8 subtests)   | fail (5/8 subtests) | still both fail    |

On rerun the workflow arm flipped `chess-best-move` fail→PASS; the baseline flipped
nothing. `configure-git-webserver` and `nginx-request-logging` stayed genuine both-fails
(`failure_mode=unset`; nginx's closest miss was `test_nginx_config_settings`, the rate-limit
directive). Consistent with the original finding: workflow gains show up where naive
execution stops short, not on tasks that are simply hard.

Caveat: `chess-best-move` is the 600s-timeout task and was nondeterministic here — A timed
out, B finished and passed. A single flip on one model / one attempt is directional, not
conclusive (see Limits).

Process notes from the rerun (both are gotchas for anyone reproducing):

- **zsh word-splitting.** The `$TASKS` variable in the Reproduce block assumes bash; zsh
  does not split unquoted variables, so the run errors instantly with `No such option`.
  Fixed below by using a shell array expanded as `"${TASKS[@]}"` (works in bash and zsh).
- **docker-build race.** Launching both arms concurrently raced them on building the same
  task image, and B's first `nginx-request-logging` attempt came back
  `unknown_agent_error` (not a real attempt). The build succeeds in isolation; re-running
  B's nginx alone (`--n-concurrent 1`) gave the clean 5/8-subtest genuine fail above. Run
  the arms sequentially, as the Reproduce block does.

### Validity checks (done before trusting the number)

- **Auth-expiry contamination ruled out.** The proxy bearer token expired late in the
  workflow run, but only touched `chess-best-move` (already failing with
  `agent_timeout` at episode 37, and failed in BOTH arms). The baseline run completed
  clean before any expiry. The two B-wins are genuine task passes, not auth casualties.
- **Protocol actually reached the model.** Verified the injected workflow preamble appears
  in every episode-0 prompt of the workflow run (4 keyword hits each).
- **Same failure set** on the 3 shared failures (`failure_mode=unset` = genuine task
  failure, not harness error).

### Limits — do not over-claim

- **n=10, 1 attempt, single model, single run.** Directional, NOT statistically conclusive.
  A 50→70% gap on 10 tasks has a wide confidence interval; `csv-to-parquet` even flipped
  pass/fail between two runs of the *same* config earlier (model nondeterminism). Needs
  `--n-attempts 3+` and a larger task set to firm up.
- **Tier B only.** The workflow runs as single-context role-play on one model. This is
  NOT real multi-worker routing across models/agents (the skills' Tier A). It tests
  the *protocol*, not a heterogeneous worker pool.
- **Cost.** The workflow arm spends more tokens/episodes per task (the role-play overhead);
  this run did not rigorously meter per-arm tokens. A fair "is it worth it" needs
  quality-per-token from Terminal-Bench runs, not repo-local fixtures.

### Reproduce

```sh
export PYTHONPATH="$PWD/docs/evals/tbench"
export OPENAI_API_KEY="<token for your OpenAI-compatible proxy>"
export OPENAI_API_BASE="<OpenAI-compatible proxy base URL>"; export OPENAI_BASE_URL="$OPENAI_API_BASE"
# Use a shell ARRAY (not a plain string) so it word-splits in both bash and zsh.
# A bare `$TASKS="--task-id a --task-id b"` does NOT split under zsh — tb sees one
# giant option and errors with `No such option`.
TASKS=(--task-id fix-permissions --task-id csv-to-parquet --task-id heterogeneous-dates --task-id fix-git --task-id configure-git-webserver --task-id fibonacci-server --task-id openssl-selfsigned-cert --task-id grid-pattern-transform --task-id chess-best-move --task-id nginx-request-logging)
# Run the arms SEQUENTIALLY (A then B). Running them concurrently races them on
# building the same per-task Docker image and yields spurious unknown_agent_error.
# A
uvx --from terminal-bench tb run --agent terminus --model openai/gpt-5.5 -k temperature=1 --dataset terminal-bench-core==0.1.1 "${TASKS[@]}" --n-concurrent 4 --global-agent-timeout-sec 600 --output-path /tmp/tb-wf/baseline
# B
uvx --from terminal-bench tb run --agent-import-path workflow_agent:WorkflowTerminus --model openai/gpt-5.5 -k temperature=1 --dataset terminal-bench-core==0.1.1 "${TASKS[@]}" --n-concurrent 4 --global-agent-timeout-sec 600 --output-path /tmp/tb-wf/workflow
```

Token refresh note: if your proxy token is short-lived, refresh mid-run or the tail
tasks can fail with auth expiry.
