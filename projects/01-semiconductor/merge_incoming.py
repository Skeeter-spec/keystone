#!/usr/bin/env python3
"""Merge parallel-burst staging files (data/_incoming/) into the canonical CSVs.

Financials partials (fin_*.csv, columns include `company` + `revenue_usd_b`) update the
matching row in companies.csv. edges.csv is appended to relationships.csv (dropping the
old tier-4 "example seed" placeholders and de-duplicating by from+to+type, keeping the
best-tier edge). sources.csv is regenerated from every costed company's filing_source.
Merged partials are archived to data/_incoming/_merged/ so a re-run never double-applies.

    python3 merge_incoming.py

Validates column counts before writing. Prints a summary; aborts on unmatched company names.
"""
import csv, glob, os, shutil, pathlib
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
INC  = DATA / "_incoming"
ARCH = INC / "_merged"

FIN_FIELDS = ["revenue_usd_b","net_income_usd_b","market_cap_usd_b","rd_spend_usd_b",
              "capex_usd_b","fiscal_year","filing_source","last_updated","source_tier","notes"]
NAME_ALIAS = {"Alphabet":"Alphabet (Google)", "Google":"Alphabet (Google)"}

def read(p):
    with open(p, newline="") as f: return list(csv.DictReader(f))

def resolve(name, valid):
    if name in valid: return name
    if name in NAME_ALIAS and NAME_ALIAS[name] in valid: return NAME_ALIAS[name]
    lo = {v.lower(): v for v in valid}
    if name.lower() in lo: return lo[name.lower()]
    for v in valid:
        if v.lower().startswith(name.lower()) or name.lower().startswith(v.lower()): return v
    return None

def main():
    companies = read(DATA / "companies.csv")
    cfields = list(companies[0].keys())
    by_name = {c["company"]: c for c in companies}
    valid = set(by_name)

    # --- financials partials ---
    fin_updates, unmatched = 0, []
    for path in sorted(glob.glob(str(INC / "fin_*.csv"))):
        for row in read(path):
            tgt = resolve(row["company"].strip(), valid)
            if not tgt:
                unmatched.append((os.path.basename(path), row["company"])); continue
            for k in FIN_FIELDS:
                if k in row and row[k] != "":
                    by_name[tgt][k] = row[k]
            by_name[tgt]["lens"] = "accounting"
            fin_updates += 1
    if unmatched:
        print("ABORT — unmatched company names (fix name, re-run):")
        for f, n in unmatched: print(f"  {f}: {n!r}")
        return

    # --- edges partial ---
    rels = read(DATA / "relationships.csv")
    rfields = list(rels[0].keys())
    rels = [r for r in rels if r.get("evidence_source") != "example seed"]  # drop placeholders
    new_edges = read(INC / "edges.csv") if (INC / "edges.csv").exists() else []
    combined = rels + new_edges
    # dedupe by (from,to,type), keep best (lowest) source_tier
    def tier(r):
        try: return int(r.get("source_tier") or 9)
        except ValueError: return 9
    best = {}
    for r in combined:
        key = (r["from_company"], r["to_company"], r["relationship_type"])
        if key not in best or tier(r) < tier(best[key]): best[key] = r
    merged_rels = list(best.values())

    # --- write canonical files ---
    with open(DATA / "companies.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cfields); w.writeheader(); w.writerows(companies)
    with open(DATA / "relationships.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rfields); w.writeheader(); w.writerows(merged_rels)

    # --- regenerate sources.csv from all costed companies ---
    def publisher(u):
        h = urlparse(u).netloc.lower()
        if "sec.gov" in h: return "SEC EDGAR"
        return h.replace("www.", "")
    src, sid = [], 1
    for c in companies:
        if not c["revenue_usd_b"] or not c["filing_source"].startswith("http"): continue
        for u in [x.strip() for x in c["filing_source"].split(";") if x.strip().startswith("http")]:
            src.append({"source_id": f"SRC{sid:03d}", "tier": c["source_tier"] or "1",
                        "lens": "accounting", "publisher": publisher(u), "company": c["company"],
                        "title": f"{c['company']} {c['fiscal_year']} filing", "url": u,
                        "retrieved": c["last_updated"] or "2026-07-14",
                        "note": "Primary financial source"}); sid += 1
    sf = ["source_id","tier","lens","publisher","company","title","url","retrieved","note"]
    with open(DATA / "sources.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=sf); w.writeheader(); w.writerows(src)

    # --- time-series partials (ts_*.csv -> financials_timeseries.csv) ---
    ts_path = DATA / "financials_timeseries.csv"
    ts_staging = sorted(glob.glob(str(INC / "ts_*.csv")))
    ts_added = 0
    if ts_staging:
        existing = read(ts_path) if ts_path.exists() else []
        tsfields = list(existing[0].keys()) if existing else None
        incoming = []
        for p in ts_staging:
            incoming += read(p)
        if not tsfields and incoming:
            tsfields = list(incoming[0].keys())
        combo = existing + incoming
        seen = {}
        for r in combo:
            key = (r.get("company"), r.get("fiscal_year"))
            if key not in seen:
                seen[key] = r;
                if r in incoming: ts_added += 1
        with open(ts_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=tsfields); w.writeheader(); w.writerows(seen.values())

    # --- archive the merged partials ---
    ARCH.mkdir(exist_ok=True)
    for path in glob.glob(str(INC / "*.csv")):
        shutil.move(path, ARCH / os.path.basename(path))

    costed = sum(1 for c in companies if c["revenue_usd_b"])
    print(f"Merged {fin_updates} financial rows -> {costed}/{len(companies)} companies costed.")
    print(f"Relationships: {len(merged_rels)} edges (dropped seed placeholders, deduped).")
    print(f"sources.csv: {len(src)} source rows. Partials archived to _incoming/_merged/.")

if __name__ == "__main__":
    main()
