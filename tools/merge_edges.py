#!/usr/bin/env python3
"""Merge staged research edges (data/_incoming/edges_*.csv) into a map's relationships.csv.

    python3 tools/merge_edges.py projects/02-critical-minerals            # dry run, prints what would change
    python3 tools/merge_edges.py projects/02-critical-minerals --apply    # write it
    python3 tools/merge_edges.py --selftest

Parallel research agents each write their own staging file so they never fight over the canonical CSV.
This merges them, and REFUSES rather than guesses:

  - an endpoint not in companies.csv is an ABORT, not a silent drop. A misspelled company name is how a
    real edge quietly becomes invisible: the renderer joins on the exact name, finds nothing, and shows
    a company with no relationships while the CSV looks fine.
  - a relationship_type outside the map's vocabulary is an ABORT. Same failure as the chokepoint
    TRUE/FALSE bug: agents agree on columns and silently disagree on values.
  - duplicates (same from+to+type) collapse to the best-tier row, so two agents finding the same edge
    is a confirmation rather than a double count.

Run tools/verify_edges.py first: it refetches each cited URL. This tool does no network work and
trusts nothing about the sources beyond their shape.
"""
import csv, glob, pathlib, shutil, sys

VOCAB = {"supplies-ore-to", "refines-for", "separates-for", "supplies-magnets-to",
         "supplies-chemicals-to", "distributes-for", "offtake-with", "invests-in",
         "competes-with", "recycles-for",
         # 01-semiconductor's vocabulary, kept valid so the tool works across maps
         "fabricates-for", "sells-equipment-to", "licenses-ip-to", "supplies-components-to",
         "packages-for"}
FIELDS = ["from_company", "to_company", "relationship_type", "description", "evidence_source",
          "evidence_date", "confidence", "last_updated", "lens", "source_tier"]


def key(r):
    return (r["from_company"], r["to_company"], r["relationship_type"])


def validate(staged, valid_companies):
    problems = []
    for r in staged:
        for side in ("from_company", "to_company"):
            if r[side] not in valid_companies:
                problems.append(f"{r[side]!r} is not a company in companies.csv (edge {key(r)})")
        if r["relationship_type"] not in VOCAB:
            problems.append(f"{r['relationship_type']!r} is outside the vocabulary (edge {key(r)})")
        if not r.get("evidence_source", "").strip():
            problems.append(f"edge {key(r)} has no evidence_source")
        if r.get("source_tier", "").strip() not in {"1", "2", "3"}:
            problems.append(f"edge {key(r)} has source_tier {r.get('source_tier')!r}, expected 1-3")
    return problems


def merge(existing, staged):
    """Later/better tier wins. Returns (rows, added, confirmed)."""
    by = {key(r): r for r in existing}
    added = confirmed = 0
    for r in staged:
        k = key(r)
        if k in by:
            confirmed += 1
            if int(r["source_tier"]) < int(by[k]["source_tier"]):
                by[k] = r  # better provenance wins
        else:
            by[k] = r
            added += 1
    return list(by.values()), added, confirmed


def run(project, apply):
    root = pathlib.Path(project)
    companies = {r["company"] for r in csv.DictReader(open(root / "data" / "companies.csv"))}
    rel_path = root / "data" / "relationships.csv"
    existing = list(csv.DictReader(open(rel_path))) if rel_path.exists() else []

    staged = []
    files = sorted(glob.glob(str(root / "data" / "_incoming" / "edges_*.csv")))
    for p in files:
        staged += list(csv.DictReader(open(p, newline="")))
    if not staged:
        print("no staged edges found")
        return 1

    problems = validate(staged, companies)
    if problems:
        print(f"ABORT. {len(problems)} problem(s) in the staged edges, nothing written:")
        for p in problems:
            print(f"  - {p}")
        return 1

    rows, added, confirmed = merge(existing, staged)
    print(f"  staged {len(staged)} edges from {len(files)} file(s)")
    print(f"  existing {len(existing)} -> merged {len(rows)}   (+{added} new, {confirmed} duplicate/confirmed)")
    if not apply:
        print("  DRY RUN. Pass --apply to write.")
        return 0
    with open(rel_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    arch = root / "data" / "_incoming" / "_merged"
    arch.mkdir(exist_ok=True)
    for p in files:
        shutil.move(p, arch / pathlib.Path(p).name)  # never double-apply a re-run
    print(f"  wrote {rel_path} and archived {len(files)} staging file(s) to _incoming/_merged/")
    return 0


def selftest():
    companies = {"A Corp", "B Corp"}
    good = {"from_company": "A Corp", "to_company": "B Corp", "relationship_type": "refines-for",
            "description": "d", "evidence_source": "https://x/doc.htm", "evidence_date": "2026-01-01",
            "confidence": "high", "last_updated": "2026-07-16", "lens": "accounting", "source_tier": "1"}
    cases = [
        ("control: a clean edge validates", good, False),
        ("catches an endpoint not in companies.csv", {**good, "to_company": "Ghost Ltd"}, True),
        ("catches a vocabulary violation", {**good, "relationship_type": "supplies_ore_to"}, True),
        ("catches a missing evidence_source", {**good, "evidence_source": ""}, True),
        ("catches a bogus tier", {**good, "source_tier": "9"}, True),
    ]
    failures = []
    for name, row, expect in cases:
        fired = bool(validate([row], companies))
        ok = fired == expect
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(name)

    # dedupe: same edge twice is a confirmation, not two rows; better tier wins
    rows, added, confirmed = merge([good], [{**good, "source_tier": "3"}])
    ok = len(rows) == 1 and added == 0 and confirmed == 1 and rows[0]["source_tier"] == "1"
    print(f"  {'ok  ' if ok else 'DEAD'}  duplicate collapses and the better tier survives")
    if not ok:
        failures.append("dedupe")
    rows, added, _ = merge([good], [{**good, "to_company": "A Corp"}])
    ok = len(rows) == 2 and added == 1
    print(f"  {'ok  ' if ok else 'DEAD'}  a genuinely different edge is added")
    if not ok:
        failures.append("add")
    print()
    if failures:
        print(f"SELFTEST FAILED: {failures}")
        return 2
    print(f"SELFTEST PASSED. {len(cases) + 2} cases.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(run(sys.argv[1], "--apply" in sys.argv))
