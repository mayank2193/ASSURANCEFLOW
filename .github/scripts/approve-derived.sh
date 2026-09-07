#!/usr/bin/env bash
# Auto-approves every derived (unreviewed) node in the .context/ graph.
# Used in CI where nobody is present to walk the interactive review chat.
set -euo pipefail

INFERRED_FILE=$(mktemp)
kane-cli context list --inferred --json > "$INFERRED_FILE" 2>/dev/null || true

COUNT=$(wc -l < "$INFERRED_FILE" | tr -d ' ')
if [ "$COUNT" -eq 0 ]; then
  echo "approve-derived: nothing pending"
  exit 0
fi

VERDICTS_FILE=$(mktemp)
python3 - "$INFERRED_FILE" "$VERDICTS_FILE" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(src) if l.strip()]
verdicts = [{"ref": r["id"], "resolution": "approved"} for r in rows]
json.dump(verdicts, open(dst, "w"), indent=2)
print(f"approve-derived: approving {len(verdicts)} node(s)")
PY

kane-cli context review --mode agent --verdicts "$VERDICTS_FILE"
