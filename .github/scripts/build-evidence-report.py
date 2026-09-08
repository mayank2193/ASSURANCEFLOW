#!/usr/bin/env python3
"""Builds a static HTML evidence report (for GitHub Pages) out of this CI
run's JSON artifacts, and copies the merged .evidence pack alongside it so
it's downloadable straight from the published page.
"""
import argparse
import glob
import html
import json
import shutil
from pathlib import Path
from urllib.parse import quote


def load_json(path: str, default):
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return default
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return default


def load_test_summary(dirpath: str, filename: str):
    for p in Path(dirpath).rglob(filename):
        return load_json(str(p), [])
    return []


STATUS_BADGE = {
    "passed": ("#1a7f37", "PASSED"),
    "failed": ("#cf222e", "FAILED"),
}


def badge(status: str) -> str:
    color, label = STATUS_BADGE.get(status, ("#9a6700", (status or "unknown").upper()))
    return f'<span class="badge" style="background:{color}">{html.escape(label)}</span>'


def render_test_table(title: str, rows: list) -> str:
    if not rows:
        return f"<h3>{html.escape(title)}</h3><p class='muted'>No results.</p>"
    body = ""
    for r in rows:
        link = (
            f'<a href="{html.escape(r["share_url"])}" target="_blank" rel="noopener">Open report</a>'
            if r.get("share_url") else "-"
        )
        body += (
            "<tr>"
            f'<td><code>{html.escape(r.get("test", ""))}</code></td>'
            f'<td>{badge(r.get("status", "unknown"))}</td>'
            f"<td>{link}</td>"
            "</tr>"
        )
    passed = sum(1 for r in rows if r.get("status") == "passed")
    return (
        f"<h3>{html.escape(title)} <span class='muted'>({passed}/{len(rows)} passed)</span></h3>"
        "<table><thead><tr><th>Test</th><th>Status</th><th>Report</th></tr></thead>"
        f"<tbody>{body}</tbody></table>"
    )


def render_invalid_packs(rows: list) -> str:
    if not rows:
        return ""
    body = ""
    for r in rows:
        reason = r.get("report", {})
        msg = reason.get("error") if isinstance(reason, dict) else str(reason)
        if not msg and isinstance(reason, dict):
            diags = reason.get("diagnostics", [])
            msg = "; ".join(d.get("message", "") for d in diags) or "failed L1 validation"
        body += f"<tr><td><code>{html.escape(r.get('pack',''))}</code></td><td>{html.escape(str(msg))}</td></tr>"
    return (
        "<h3>Excluded from merge <span class='muted'>(failed L1 validation)</span></h3>"
        "<table><thead><tr><th>Pack</th><th>Reason</th></tr></thead>"
        f"<tbody>{body}</tbody></table>"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--run-output", required=True)
    ap.add_argument("--regression-output", required=True)
    ap.add_argument("--coverage-report", required=True)
    ap.add_argument("--merge-report", required=True)
    ap.add_argument("--invalid-packs", required=True)
    ap.add_argument("--validation-report", required=True)
    ap.add_argument("--evidence-glob", required=True)
    ap.add_argument("--pages-base-url", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--run-url", required=True)
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    run_rows = load_test_summary(args.run_output, "run-summary.json")
    regression_rows = load_test_summary(args.regression_output, "regression-summary.json")
    coverage = load_json(args.coverage_report, {})
    merge_report = load_json(args.merge_report, {})
    invalid_packs = load_json(args.invalid_packs, [])
    validation_report = load_json(args.validation_report, {})

    dc = coverage.get("design_completeness", {})

    # Copy the merged pack (if any) into the published site so it's
    # downloadable, and build a best-effort hosted-viewer link for it.
    evidence_files = sorted(glob.glob(args.evidence_glob))
    pack_html = "<p class='muted'>No merged evidence pack was produced this run.</p>"
    if evidence_files:
        pack_path = Path(evidence_files[0])
        dest_dir = out_dir / "evidence"
        dest_dir.mkdir(exist_ok=True)
        shutil.copy2(pack_path, dest_dir / pack_path.name)
        pack_url = f"{args.pages_base_url}/evidence/{pack_path.name}"
        viewer_url = f"https://evidence.lambdatest.com/?pack={quote(pack_url, safe='')}"
        valid = validation_report.get("valid")
        valid_badge = badge("passed" if valid else "failed") if valid is not None else ""
        diagnostics = validation_report.get("diagnostics", [])
        diag_html = ""
        if diagnostics:
            diag_html = "<ul class='muted'>" + "".join(
                f"<li>[{html.escape(d.get('severity',''))}] {html.escape(d.get('message',''))}</li>"
                for d in diagnostics
            ) + "</ul>"
        pack_html = (
            f"<p>{valid_badge} <a href='evidence/{html.escape(pack_path.name)}'>Download {html.escape(pack_path.name)}</a>"
            f" &nbsp;|&nbsp; <a href='{html.escape(viewer_url)}' target='_blank' rel='noopener'>Try the hosted evidence viewer &#8599;</a></p>"
            f"{diag_html}"
        )

    packs_meta = merge_report.get("packs", {})

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Airbnb Assurance Evidence — run {html.escape(args.run_id)}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1.25rem; line-height: 1.5; }}
  h1 {{ font-size: 1.5rem; }}
  h2 {{ margin-top: 2.5rem; border-bottom: 1px solid #8884; padding-bottom: .3rem; }}
  h3 {{ margin-top: 1.5rem; }}
  table {{ border-collapse: collapse; width: 100%; margin: .75rem 0; }}
  th, td {{ text-align: left; padding: .4rem .6rem; border-bottom: 1px solid #8883; font-size: .92rem; }}
  th {{ background: #80808014; }}
  code {{ font-size: .85em; }}
  .muted {{ color: #888; font-weight: normal; font-size: .85em; }}
  .badge {{ color: #fff; border-radius: 4px; padding: .12rem .5rem; font-size: .78rem; font-weight: 600; letter-spacing: .02em; }}
  .stat {{ display: inline-block; margin-right: 2rem; }}
  .stat b {{ font-size: 1.4rem; display: block; }}
  footer {{ margin-top: 3rem; color: #888; font-size: .82rem; }}
  a {{ color: #0969da; }}
</style>
</head>
<body>
<h1>Airbnb Assurance Evidence</h1>
<p>Run <a href="{html.escape(args.run_url)}" target="_blank" rel="noopener">#{html.escape(args.run_id)}</a></p>

<div>
  <div class="stat"><b>{dc.get('pct', '—')}%</b>design-complete</div>
  <div class="stat"><b>{dc.get('acs_designed', '—')}</b>ACs designed</div>
  <div class="stat"><b>{dc.get('usecases_complete', '—')}</b>use-cases complete</div>
  <div class="stat"><b>{len(packs_meta.get('eligible', []))}</b>packs merged</div>
  <div class="stat"><b>{len(invalid_packs)}</b>packs excluded</div>
</div>

<h2>Evidence pack</h2>
{pack_html}

<h2>Run (author &amp; replay) — stage 3</h2>
{render_test_table("Tests", run_rows)}

<h2>Maintain (rerun-regression) — stage 5</h2>
{render_test_table("Tests", regression_rows)}

<h2>Merge diagnostics</h2>
{render_invalid_packs(invalid_packs)}

<footer>Generated by the KaneAI Assurance Pipeline · <a href="{html.escape(args.run_url)}" target="_blank" rel="noopener">view this run on GitHub Actions</a></footer>
</body>
</html>
"""
    (out_dir / "index.html").write_text(html_doc)
    print(f"build-evidence-report: wrote {out_dir / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
