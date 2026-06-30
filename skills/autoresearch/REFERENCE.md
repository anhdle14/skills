# Autoresearch Reference

The upstream `karpathy/autoresearch` repo's concrete answers to the six setup questions in
[SKILL.md](SKILL.md). Use these only when working the upstream repo; a fork or port answers
the six questions for itself.

## Upstream defaults

- Metric: `val_bpb`, lower is better.
- Ground truth evaluator: `evaluate_bpb` in `prepare.py`.
- Editable file: `train.py` only.
- Read-only files: `prepare.py`, evaluation harness, dependency files.
- Experiment command: `uv run train.py`.
- Result log fields: `val_bpb` and `peak_vram_mb`.
