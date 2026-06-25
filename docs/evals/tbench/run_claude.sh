#!/usr/bin/env bash
# Re-run the orchestrate+trinity workflow A/B on Terminal-Bench with Claude
# through a Bedrock-compatible proxy. Arm A = stock terminus (plain loop); arm B =
# workflow-terminus (same loop + workflow preamble). sitecustomize.py
# (auto-loaded via PYTHONPATH) handles provider-proxy compat identically for both
# arms — token keep-alive, forced schema-in-prompt fallback, and fence stripping.
#
# Required env:
#   TB_BEDROCK_API_BASE       Bedrock-compatible proxy base URL
#   TB_BEDROCK_TOKEN_SCOPE    az access-token scope for that proxy
# Optional env:
#   TB_BEDROCK_MODEL          defaults to bedrock/global.anthropic.claude-opus-4-8
#   TB_BEDROCK_OUT            defaults to /tmp/tb-claude
#
# Usage: bash run_claude.sh [baseline|workflow|both]   (default: both)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$HERE"
export AWS_REGION="${AWS_REGION:-us-east-1}"
: "${TB_BEDROCK_API_BASE:?set TB_BEDROCK_API_BASE to your Bedrock-compatible proxy base URL}"
: "${TB_BEDROCK_TOKEN_SCOPE:?set TB_BEDROCK_TOKEN_SCOPE to your az access-token scope}"
export AWS_BEARER_TOKEN_BEDROCK="$(az account get-access-token --scope "$TB_BEDROCK_TOKEN_SCOPE" --query accessToken -o tsv)"

MODEL="${TB_BEDROCK_MODEL:-bedrock/global.anthropic.claude-opus-4-8}"
API_BASE="$TB_BEDROCK_API_BASE"
OUT="${TB_BEDROCK_OUT:-/tmp/tb-claude}"

# Same 10 tasks as the original run. Shell ARRAY so it word-splits in bash AND zsh
# (a bare string does not split under zsh — tb sees one giant option and errors).
TASKS=(--task-id fix-permissions --task-id csv-to-parquet --task-id heterogeneous-dates \
  --task-id fix-git --task-id configure-git-webserver --task-id fibonacci-server \
  --task-id openssl-selfsigned-cert --task-id grid-pattern-transform \
  --task-id chess-best-move --task-id nginx-request-logging)

run_baseline() {
  uvx --from terminal-bench --with boto3 tb run \
    --agent terminus --model "$MODEL" \
    -k temperature=1 -k "api_base=$API_BASE" \
    --dataset terminal-bench-core==0.1.1 "${TASKS[@]}" \
    --n-concurrent 4 --global-agent-timeout-sec 600 --output-path "$OUT/baseline"
}

run_workflow() {
  uvx --from terminal-bench --with boto3 tb run \
    --agent-import-path workflow_agent:WorkflowTerminus --model "$MODEL" \
    -k temperature=1 -k "api_base=$API_BASE" \
    --dataset terminal-bench-core==0.1.1 "${TASKS[@]}" \
    --n-concurrent 4 --global-agent-timeout-sec 600 --output-path "$OUT/workflow"
}

# Run the arms SEQUENTIALLY (A then B). Concurrent arms race on building the same
# per-task Docker image and yield spurious unknown_agent_error.
case "${1:-both}" in
  baseline) run_baseline ;;
  workflow) run_workflow ;;
  both)     run_baseline; run_workflow ;;
  *) echo "usage: $0 [baseline|workflow|both]" >&2; exit 2 ;;
esac
