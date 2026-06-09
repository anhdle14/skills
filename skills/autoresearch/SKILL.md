---
name: autoresearch
description: Sets up and runs Karpathy-style autoresearch with metric-first clarification and the upstream experiment protocol. Use when user wants to set up autoresearch, run autonomous research experiments, optimize a training metric, or mentions karpathy/autoresearch.
tags: [engineering, plan, analyze]
args: "<run tag, metric, or repo path (optional)>"
---

# Autoresearch

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Set up and run the `karpathy/autoresearch` protocol. The goal is not "try random ML changes"; the goal is to optimize the agreed metric under the agreed harness.

## Before Setup

Clarify these before touching git:

1. Is this repo the upstream autoresearch repo, a fork, or a port of the protocol?
2. What is the metric, where is it computed, and is lower or higher better?
3. What file is the agent allowed to edit?
4. What files are read-only because they define data prep, evaluation, or constants?
5. What command runs one fixed-budget experiment?
6. What log fields prove success, memory usage, and crash status?

For the upstream repo, defaults are:

- Metric: `val_bpb`, lower is better.
- Ground truth evaluator: `evaluate_bpb` in `prepare.py`.
- Editable file: `train.py` only.
- Read-only files: `prepare.py`, evaluation harness, dependency files.
- Experiment command: `uv run train.py`.
- Result log fields: `val_bpb` and `peak_vram_mb`.

If the repo differs, write down the equivalent answers before proceeding.

## Setup Protocol

Work with the user to:

1. Agree on a run tag based on today's date or the user's label.
2. Confirm `autoresearch/<tag>` does not already exist.
3. Create `autoresearch/<tag>` from the current mainline branch.
4. Read the full in-scope context before editing:
   - repo `README.md`
   - evaluation/data-prep file such as `prepare.py`
   - editable experiment file such as `train.py`
   - local instruction file such as `program.md`, if present
5. Verify required data and tokenizer artifacts exist. For upstream, check `~/.cache/autoresearch/`; if missing, tell the user to run `uv run prepare.py`.
6. Create `results.tsv` with exactly:

```text
commit\tval_bpb\tmemory_gb\tstatus\tdescription
```

Here `\t` means real tab characters.

1. Confirm the metric, edit scope, branch, data, command, and results file with the user before starting experiments.

## Experiment Rules

The first experiment is always the unmodified baseline. For baseline, skip editing and committing; run the current commit and log it as `keep`.

Allowed:

- Modify only the editable experiment file.
- Change architecture, optimizer, hyperparameters, batch size, model size, or training loop if still inside the fixed harness.

Forbidden:

- Modify data prep, constants, evaluator, or metric code.
- Add dependencies or install packages.
- Change the fixed time budget or make results incomparable.
- Commit `results.tsv`; keep it untracked.

## Loop

Once the user confirms setup, run autonomously until interrupted. Do not pause to ask whether to continue.

1. Record current branch and commit.
2. Make one experimental change to the editable file.
3. Commit the change.
4. Run the experiment with output redirected to a log, e.g. `uv run train.py > run.log 2>&1`.
5. Extract metric and memory, e.g. `grep "^val_bpb:\|^peak_vram_mb:" run.log`.
6. If output is missing, inspect the crash with `tail -n 50 run.log`.
7. Append one TSV row with short commit hash, metric, memory GB, status, and description.
8. Keep the commit only if the metric improves. Reset to the prior commit if equal, worse, or fundamentally crashed.

Treat a run over twice the expected time budget as failure. Fix trivial crashes and rerun; log fundamentally broken ideas as `crash`.

## Decision Criteria

Optimize the metric first, but apply the simplicity criterion:

- Lower upstream `val_bpb` wins.
- Similar score with simpler code wins.
- Tiny gains with ugly complexity usually lose.
- Tiny gains from deletion or simplification usually win.
- Meaningful metric gains may justify moderate memory growth; large memory growth needs a large metric win.
