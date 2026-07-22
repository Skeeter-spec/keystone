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
import csv, glob, json, pathlib, shutil, sys

VOCAB = {"supplies-ore-to", "refines-for", "separates-for", "supplies-magnets-to",
         "supplies-chemicals-to", "distributes-for", "offtake-with", "invests-in",
         "competes-with", "recycles-for",
         # 01-semiconductor's vocabulary, kept valid so the tool works across maps
         "fabricates-for", "sells-equipment-to", "licenses-ip-to", "supplies-components-to",
         "packages-for",
         # 04-ai-compute. Added BEFORE its burst rather than after, because the lesson from the
         # chokepoint TRUE/FALSE drift is that a fan-out's vocabulary has to exist before the fan-out
         # writes, not once its output has already been rejected.
         "provides-compute-to", "assembles-for",
         # 05-pharma, added 2026-07-22, again BEFORE the burst. Four terms, and only four, because the
         # rest of this map's edges are already sayable: a distributor-to-originator edge is
         # "distributes-for", which 02 already defined. A new term per map is how a union vocabulary
         # becomes unreadable; reuse first, and only mint a word for a relation the atlas cannot
         # already express.
         "supplies-api-to",           # API maker -> originator / generics maker
         "manufactures-for",          # CDMO makes a product the customer owns (Lonza, WuXi, Catalent)
         "negotiates-rebates-with",   # manufacturer <-> PBM. The money in this chain moves along it
         "administers-benefits-for",  # PBM -> payer / plan sponsor
         # Added mid-burst 2026-07-22, and the reason is a direction bug worth keeping. A worker
         # correctly found that CVS Health is McKesson's largest customer at 24% of revenue, and had
         # to file it as `distributes-for`, whose direction is from=distributor to=THE MANUFACTURER
         # WHOSE PRODUCT IT MOVES. CVS is a pharmacy, not a manufacturer, so the row was true and the
         # label was wrong -- the edge points the other way down the chain. A distributor's two sides
         # are genuinely two relations: it distributes FOR the maker and TO the pharmacy.
         "distributes-to"}            # distributor -> pharmacy / retail customer
# DESIGN DEBT, deliberate and recorded rather than fixed here: this vocabulary is a UNION across every
# map, so 02's "supplies-ore-to" is technically legal in the AI compute map. The right home is a
# relationship_types list in each map's map.json, alongside the layers, which is where this repo already
# keeps per-map data. Not done now because it is a refactor and the burst needed the two types above.
FIELDS = ["from_company", "to_company", "relationship_type", "description", "evidence_source",
          "evidence_date", "confidence", "last_updated", "lens", "source_tier"]


def key(r):
    return (r["from_company"], r["to_company"], r["relationship_type"])


def allowed_types(root):
    """The vocabulary THIS map may use. Returns (set, declared?).

    🔴 A UNION IS NOT A VOCABULARY. VOCAB above is every term any map has ever needed, and it grew to
    23 across five maps. Measured 2026-07-22: a `supplies-api-to` edge -- a PHARMA term -- staged onto
    06-shipping between two real Maersk/MSC nodes merged CLEANLY, exit 0, "+1 new". Nothing was wrong
    with the file; the checker simply had no idea which map it was looking at. That is the chokepoint
    TRUE/FALSE bug again: workers agree on the column and disagree on the value, and the union made
    every map's disagreement legal everywhere.

    So a map declares `relationship_types` in its own map.json, beside `layers`, which is where this
    repo already keeps per-map data. An UNDECLARED map falls back to the union and says so loudly.
    An EMPTY declaration is deliberate and means "nobody has decided this map's vocabulary yet" -- it
    refuses every edge until a burst author declares one, which mechanizes the rule 04 wrote into this
    file's own comments: the vocabulary must exist BEFORE the fan-out, not after its output is rejected.
    """
    mj = root / "map.json"
    if mj.exists():
        cfg = json.loads(mj.read_text())
        if "relationship_types" in cfg:
            return set(cfg["relationship_types"]), True
    return VOCAB, False


def validate(staged, valid_companies, vocab=None, declared=True):
    problems = []
    vocab = VOCAB if vocab is None else vocab
    if declared and not vocab and staged:
        problems.append("this map's map.json declares relationship_types: [] -- no vocabulary has been "
                        "decided for it yet. Add the types this burst needs to map.json before merging.")
    for r in staged:
        for side in ("from_company", "to_company"):
            if r[side] not in valid_companies:
                problems.append(f"{r[side]!r} is not a company in companies.csv (edge {key(r)})")
        if r["relationship_type"] not in vocab:
            where = "this map's declared relationship_types" if declared else "the shared vocabulary"
            problems.append(f"{r['relationship_type']!r} is outside {where} (edge {key(r)})")
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

    vocab, declared = allowed_types(root)
    if not declared:
        print(f"  NOTE: {root.name}/map.json declares no relationship_types; falling back to the "
              f"shared {len(VOCAB)}-term union, which is not this map's vocabulary.")
    problems = validate(staged, companies, vocab, declared)
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

    # --- per-map vocabulary. THE REAL CASE, kept as a permanent fixture: a `supplies-api-to` edge
    # (05-pharma's term) staged onto 06-shipping between two real Maersk/MSC nodes merged CLEANLY on
    # 2026-07-22, exit 0, "+1 new", because the shared VOCAB is a union and knew nothing about maps.
    pharma_on_shipping = {**good, "from_company": "A Corp", "to_company": "B Corp",
                          "relationship_type": "supplies-api-to"}
    vocab_cases = [
        ("🔴 the REAL case: a pharma type on a shipping map is REFUSED",
         pharma_on_shipping, {"sails-for", "charters-to"}, True, True),
        ("...and the SAME row is accepted by the map that owns the term",
         pharma_on_shipping, {"supplies-api-to", "manufactures-for"}, True, False),
        ("an EMPTY declaration refuses every edge until someone decides",
         good, set(), True, True),
        ("NEGATIVE: an undeclared map still merges on the union, so nothing breaks",
         good, VOCAB, False, False),
    ]
    for name, row, vocab, declared, expect in vocab_cases:
        fired = bool(validate([row], companies, vocab, declared))
        ok = fired == expect
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(name)

    # END-TO-END over run(), because a rule that is never CALLED reports exactly what a clean repo
    # reports: a mutant that deleted the call site once survived a fully green suite in this repo.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        proj = pathlib.Path(td) / "99-fake"
        (proj / "data" / "_incoming").mkdir(parents=True)
        with open(proj / "data" / "companies.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["company"]); w.writeheader()
            w.writerow({"company": "A Corp"}); w.writerow({"company": "B Corp"})
        (proj / "map.json").write_text(json.dumps({"relationship_types": ["refines-for"]}))
        with open(proj / "data" / "_incoming" / "edges_x.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS); w.writeheader()
            w.writerow(pharma_on_shipping)
        rc = run(str(proj), False)
        ok = rc == 1
        print(f"  {'ok  ' if ok else 'DEAD'}  end-to-end: run() itself refuses the foreign type (exit {rc})")
        if not ok:
            failures.append("end-to-end run() vocabulary")

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
    # Counted, not typed: this line said "7 cases" while 12 ran, because the total was a hand-kept
    # copy of the case list. A suite that misreports its own size is the smallest possible version of
    # the bug this repo keeps hitting -- a copy rots, a pointer does not.
    print(f"SELFTEST PASSED. {len(cases) + len(vocab_cases) + 3} cases.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(run(sys.argv[1], "--apply" in sys.argv))
