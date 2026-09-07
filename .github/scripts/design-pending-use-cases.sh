#!/usr/bin/env bash
# Designs assurance (ACs, scenarios, 1:1 tests) for every use-case the
# coverage ribbon reports as needing scenarios or having unverified ACs.
# Follows kane-cli's own `ready_command` hints from `cover gaps`.
set -uo pipefail

MAX_PASSES=5

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
    echo "design-pending-use-cases: running -> $cmd --mode ci"
    if ! eval "$cmd --mode ci"; then
      echo "design-pending-use-cases: retrying with --force -> $cmd --mode ci --force"
      eval "$cmd --mode ci --force" || echo "design-pending-use-cases: WARN - $cmd failed twice, continuing"
    fi
    bash "$(dirname "$0")/approve-derived.sh"
  done <<< "$CMDS"
done

kane-cli cover gaps --mode ci --json > coverage-after-design.json 2>/dev/null || true
echo "design-pending-use-cases: done"
