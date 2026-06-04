#!/usr/bin/env sh
# hitl-loop.template.sh — Human-in-the-loop feedback loop template
# Use when automated reproduction is impossible and a human must perform steps.
# Replace TODO sections and run: sh hitl-loop.template.sh
set -eu

ITERATION=0
LOGFILE="/tmp/hitl-loop-$(date +%s).log"

echo "HITL loop started. Log: $LOGFILE"
echo "Press Ctrl+C to stop."

while true; do
  ITERATION=$((ITERATION + 1))
  echo ""
  echo "=== Iteration $ITERATION ==="
  echo "TODO: describe the manual steps the human must perform here"
  echo ""
  echo "Steps:"
  echo "  1. TODO: step 1"
  echo "  2. TODO: step 2"
  echo ""

  printf "Did the bug occur? [y/n/q]: "
  read -r RESULT

  TIMESTAMP=$(date +%H:%M:%S)
  echo "$TIMESTAMP  iter=$ITERATION  result=$RESULT" >> "$LOGFILE"

  case "$RESULT" in
    y) echo "Bug reproduced. Logged." ;;
    n) echo "No bug. Logged." ;;
    q) echo "Stopping. Log saved to $LOGFILE"; exit 0 ;;
    *) echo "Unknown input — logging as '?'" ; echo "$TIMESTAMP  iter=$ITERATION  result=?" >> "$LOGFILE" ;;
  esac
done
