#!/usr/bin/env bash
# Designs assurance (ACs, scenarios, 1:1 tests) for every use-case the
# coverage ribbon reports as needing scenarios or having unverified ACs.
# Follows kane-cli's own `ready_command` hints from `cover gaps`.
#
# Honors $MAX_TESTS (optional): caps scenario+test pairs designed per
# use-case via kane-cli's own `--max` flag. Blank/unset = no ceiling.
set -uo pipefail

MAX_PASSES=5
MAX_FLAG=""
if [ -n "${MAX_TESTS:-}" ]; then
  MAX_FLAG="--max $MAX_TESTS"
  echo "design-pending-use-cases: capping each use-case at $MAX_TESTS scenario+test pair(s)"
fi

for pass in $(seq 1 "$MAX_PASSES"); do
  GAPS=$(kane-cli cover gaps --mode ci --json 2>/dev/null | head -1)
  CMDS=$(echo "$GAPS" | python3 -c '
import json, sys
d = json.load(sys.stdin)
seen = set()
for uc in d.get("usecases", []):
    for p in uc.get("pending", []):
        cmd = p.get("ready_command", "")
        if cmd.startswith("kane-cli design tests") and cmd not in seen:
            seen.add(cmd)
            print(cmd)
')

  if [ -z "$CMDS" ]; then
    echo "design-pending-use-cases: nothing left to design (pass $pass)"
    break
  fi

  while IFS= read -r cmd; do
    [ -z "$cmd" ] && continue
    echo "design-pending-use-cases: running -> $cmd --mode ci $MAX_FLAG"
    if ! eval "$cmd --mode ci $MAX_FLAG"; then
      echo "design-pending-use-cases: retrying with --force -> $cmd --mode ci --force $MAX_FLAG"
      eval "$cmd --mode ci --force $MAX_FLAG" || echo "design-pending-use-cases: WARN - $cmd failed twice, continuing"
    fi
    bash "$(dirname "$0")/approve-derived.sh"
  done <<< "$CMDS"
done

kane-cli cover gaps --mode ci --json > coverage-after-design.json 2>/dev/null || true
echo "design-pending-use-cases: done"
