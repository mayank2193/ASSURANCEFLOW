#!/usr/bin/env bash
# Runs (authors on first sight, replays afterwards) a set of *_test.md files,
# collects a pass/fail summary, and stages every evidence pack it produced
# into ./evidence-packs/ so the caller can upload it.
#
# Usage: run-all-tests.sh <summary-json-path>
#
# Which tests run is resolved in this order:
#   1. $TEST_LIST_FILE, if set and the file exists - run exactly the test
#      paths listed in it, one per line (this is how stage 5 reruns the
#      identical set stage 3 planned, instead of re-selecting/re-globbing).
#   2. Otherwise, every *_test.md under .testmuai/tests, sorted, capped to
#      the first $TEST_LIMIT of them if that's set (blank/unset = no cap).
#
# Whichever set is resolved, it's written to ./selected-tests.txt so the
# caller can upload it and hand it to a later stage via $TEST_LIST_FILE.
set -uo pipefail

SUMMARY_PATH="${1:-run-summary.json}"
SELECTED_PATH="selected-tests.txt"
mkdir -p evidence-packs

if [ -n "${TEST_LIST_FILE:-}" ] && [ -s "$TEST_LIST_FILE" ]; then
  echo "run-all-tests: using the fixed test list from $TEST_LIST_FILE"
  cp "$TEST_LIST_FILE" "$SELECTED_PATH"
else
  find .testmuai/tests -name '*_test.md' | sort > "$SELECTED_PATH.all"
  if [ -n "${TEST_LIMIT:-}" ]; then
    echo "run-all-tests: capping at the first $TEST_LIMIT test(s) (no fixed list supplied)"
    head -n "$TEST_LIMIT" "$SELECTED_PATH.all" > "$SELECTED_PATH"
  else
    cp "$SELECTED_PATH.all" "$SELECTED_PATH"
  fi
  rm -f "$SELECTED_PATH.all"
fi

TOTAL_AVAILABLE=$(find .testmuai/tests -name '*_test.md' | wc -l | tr -d ' ')
TOTAL_SELECTED=$(wc -l < "$SELECTED_PATH" | tr -d ' ')
echo "run-all-tests: running $TOTAL_SELECTED of $TOTAL_AVAILABLE available test(s)"

BEFORE_MARK=$(mktemp)
touch "$BEFORE_MARK"

echo "[]" > "$SUMMARY_PATH"
OVERALL_EXIT=0

while IFS= read -r test_file; do
  [ -z "$test_file" ] && continue
  if [ ! -f "$test_file" ]; then
    echo "run-all-tests: WARN - $test_file no longer exists, skipping"
    continue
  fi

  echo "=================================================================="
  echo "run-all-tests: $test_file"
  echo "=================================================================="

  OUT=$(mktemp)
  kane-cli testmd run "$test_file" \
    --agent --headless \
    --variables-file .testmuai/variables/airbnb.json \
    --on-lock-conflict wait \
    --retry \
    > "$OUT" 2>&1
  EXIT_CODE=$?

  DONE_LINE=$(grep -m1 '"type":"test_md_done"' "$OUT" || true)
  STATUS=$(echo "$DONE_LINE" | python3 -c 'import json,sys
try:
    print(json.load(sys.stdin).get("overall_status","unknown"))
except Exception:
    print("unknown")' 2>/dev/null || echo "unknown")
  SHARE_URL=$(echo "$DONE_LINE" | python3 -c 'import json,sys
try:
    print(json.load(sys.stdin).get("share_url",""))
except Exception:
    print("")' 2>/dev/null || echo "")

  python3 - "$SUMMARY_PATH" "$test_file" "$STATUS" "$EXIT_CODE" "$SHARE_URL" <<'PY'
import json, sys
path, test_file, status, exit_code, share_url = sys.argv[1:6]
rows = json.load(open(path))
rows.append({
    "test": test_file,
    "status": status,
    "exit_code": int(exit_code),
    "share_url": share_url,
})
json.dump(rows, open(path, "w"), indent=2)
PY

  tail -c 4000 "$OUT"
  rm -f "$OUT"

  if [ "$EXIT_CODE" -ne 0 ]; then
    OVERALL_EXIT=1
  fi
done < "$SELECTED_PATH"

# Stage every evidence pack produced since this script started.
find "$HOME/.testmuai/kaneai/sessions" -name '*.evidence' -newer "$BEFORE_MARK" -print0 2>/dev/null \
  | xargs -0 -I{} cp {} evidence-packs/ 2>/dev/null || true

rm -f "$BEFORE_MARK"

echo "run-all-tests: summary written to $SUMMARY_PATH"
python3 -c "
import json
rows = json.load(open('$SUMMARY_PATH'))
passed = sum(1 for r in rows if r['status'] == 'passed')
failed = sum(1 for r in rows if r['status'] != 'passed')
print(f'run-all-tests: {passed} passed, {failed} failed, {len(rows)} total')
"

exit $OVERALL_EXIT
