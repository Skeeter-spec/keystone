#!/usr/bin/env python3
"""Regenerate the publishable semiconductor-map artifact from the CSVs.

Run this after any research burst grows the data, then republish
artifact/semiconductor-map.html to the SAME artifact URL (see the skill).

    python3 build_artifact.py 2026-07-13

The optional argument is the build date to stamp (defaults to a fixed string
so the script has no hidden nondeterminism). Pass today's date on each build.
"""
import csv, json, sys, pathlib

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
TPL  = ROOT / "artifact" / "template.html"
OUT  = ROOT / "artifact" / "semiconductor-map.html"

def load(name):
    with open(DATA / name, newline="") as f:
        return list(csv.DictReader(f))

def main():
    build_date = sys.argv[1] if len(sys.argv) > 1 else "unbuilt"
    companies = load("companies.csv")
    rels = load("relationships.csv")
    ts = load("financials_timeseries.csv") if (DATA / "financials_timeseries.csv").exists() else []
    filled = sum(1 for c in companies if c.get("revenue_usd_b"))
    meta = {"date": build_date, "total": len(companies), "filled": filled}

    html = TPL.read_text()
    html = html.replace("__BUILDMETA__", json.dumps(meta, ensure_ascii=False))
    html = html.replace("__COMPANIES__", json.dumps(companies, ensure_ascii=False))
    html = html.replace("__RELATIONSHIPS__", json.dumps(rels, ensure_ascii=False))
    html = html.replace("__TIMESERIES__", json.dumps(ts, ensure_ascii=False))

    # Safety: no unreplaced placeholders should survive.
    for token in ("__BUILDMETA__", "__COMPANIES__", "__RELATIONSHIPS__", "__TIMESERIES__"):
        assert token not in html, f"placeholder {token} was not replaced"

    OUT.write_text(html)
    print(f"Built {OUT.name}: {len(companies)} companies, "
          f"{filled} costed, {len(rels)} relationships, {len(ts)} timeseries rows, dated {build_date}")

if __name__ == "__main__":
    main()
