#!/usr/bin/env python3
"""Merge every *.evidence pack under given search dirs into one sealed
bundle - but only the packs that pass L1 validation.

kane-cli refuses the WHOLE merge ("packs.require_valid=L1") the moment any
one input pack fails validation (e.g. a run killed mid-flight, hit
--on-lock-conflict wait, or otherwise never sealed cleanly). Filtering first
means one bad pack doesn't block the evidence report for every good one -
it's reported separately (invalid-packs.json) instead of silently dropped
or fatal to the whole stage.

Usage: merge_evidence.py <run-id> <out-path> <search-dir> [search-dir...]
"""
import json
import subprocess
import sys
from pathlib import Path


def validate(pack: Path) -> dict:
    proc = subprocess.run(
        ["kane-cli", "evidence", "validate", str(pack), "--profile", "L1", "--json"],
        capture_output=True, text=True,
    )
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        report = {"valid": False, "error": (proc.stdout + proc.stderr).strip()}
    return report


def main() -> int:
    run_id, out_path, *search_dirs = sys.argv[1:]
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    all_packs = sorted(
        p for d in search_dirs for p in Path(d).rglob("*.evidence") if Path(d).exists()
    )
    print(f"merge-evidence: found {len(all_packs)} evidence pack(s) total")

    if not all_packs:
        print("::warning::no evidence packs found to merge")
        Path("merge-report.json").write_text(json.dumps({"merged": False, "reason": "no_packs_found"}, indent=2))
        Path("invalid-packs.json").write_text("[]")
        return 0

    valid_packs, invalid_rows = [], []
    for pack in all_packs:
        report = validate(pack)
        if report.get("valid") is True:
            valid_packs.append(pack)
        else:
            print(f"::warning::evidence pack failed L1 validation, excluding from merge: {pack}")
            invalid_rows.append({"pack": str(pack), "report": report})

    Path("invalid-packs.json").write_text(json.dumps(invalid_rows, indent=2))
    print(f"merge-evidence: {len(valid_packs)} valid, {len(invalid_rows)} invalid (see invalid-packs.json)")

    if not valid_packs:
        print("::error::every evidence pack failed L1 validation - nothing to merge")
        Path("merge-report.json").write_text(json.dumps({"merged": False, "reason": "all_packs_invalid"}, indent=2))
        return 1

    print(f"Merging {len(valid_packs)} valid evidence pack(s):")
    for p in valid_packs:
        print(f" - {p}")

    merge_cmd = [
        "kane-cli", "evidence", "merge", *[str(p) for p in valid_packs],
        "--run-id", run_id,
        "--title", f"Airbnb assurance run {run_id}",
        "--on-collision", "prefer-latest",
        "--json",
        "-o", str(out_path),
    ]
    proc = subprocess.run(merge_cmd, capture_output=True, text=True)
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    Path("merge-report.json").write_text(proc.stdout or json.dumps({"merged": False}))
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
