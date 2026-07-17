#!/usr/bin/env python3
"""Render ANY Keystone map from its CSVs + its map.json. One renderer, ten maps.

    python3 shared/build_map.py projects/02-critical-minerals 2026-07-16
    python3 shared/build_map.py --selftest

WHY THIS EXISTS. The renderer used to live inside projects/01-semiconductor and was hardcoded to it,
so nine maps could hold real sourced data that NOTHING COULD DRAW. Measured before writing this:
running 01's builder against 02's data succeeded, exit 0, and rendered a map where **30 of 33
companies landed in no layer at all** and the value chain showed eight empty rows. It did not crash.
That is the point: a map-specific renderer fails SILENTLY on another map's data, which is the same
shape as the chokepoint TRUE/FALSE bug.

WHAT IS PER MAP, AND WHY IT IS DATA AND NOT CODE. Each project owns a `map.json`:
  title, subtitle, financials_note, chokepoints_note, notes_placeholder  -- the prose
  storage_key            -- the artifact's localStorage key. MUST be unique per map, or two maps
                            published from the same origin would share one watchlist.
  layers[]               -- the value chain: {role,label,desc}, in top-to-bottom order. THE ROLES
                            MUST MATCH the roles actually used in companies.csv. This is the exact
                            coupling that made 30 of 33 companies vanish, so build_map CHECKS it.
  chokepoint_why{}       -- one line per chokepoint company, keyed by the EXACT companies.csv name.

A map author edits data. They never hand-write JavaScript.
"""
import csv, json, pathlib, sys

ROOT = pathlib.Path(__file__).parent.parent
TPL = ROOT / "shared" / "map-template.html"
REQUIRED = ("title", "subtitle", "financials_note", "chokepoints_note",
            "notes_placeholder", "storage_key", "layers")


def load_csv(p):
    if not p.exists():
        return []
    with open(p, newline="") as fh:
        return list(csv.DictReader(fh))


def roles_of(row):
    return [r.strip() for r in (row.get("roles") or "").split(";") if r.strip()]


def check_coverage(companies, layers):
    """The coupling that renders a map empty WITHOUT erroring. Refuse to ship it."""
    known = {l["role"] for l in layers}
    orphans = [c["company"] for c in companies if not (set(roles_of(c)) & known)]
    unused = sorted(known - {r for c in companies for r in roles_of(c)})
    return orphans, unused


def check_choke_why(companies, choke_why):
    """The docstring promised 'keyed by the EXACT companies.csv name' and nothing enforced it.

    A key that matches no company is INCORRECT: the template looks its explanation up by name, so a
    typo'd or stale key renders that chokepoint with no reason and the page still looks fine. That is
    the same silent shape as the orphan bug. A chokepoint with no key is merely INCOMPLETE, which this
    repo tolerates by design, so it is a note and not an abort.
    """
    names = {c["company"] for c in companies}
    unknown = sorted(k for k in choke_why if k not in names)
    chokes = {c["company"] for c in companies
              if (c.get("chokepoint") or "").strip().lower() == "yes"}
    unexplained = sorted(chokes - set(choke_why))
    return unknown, unexplained


def build(project, date, strict=True):
    proj = pathlib.Path(project)
    cfg = json.loads((proj / "map.json").read_text())
    missing = [k for k in REQUIRED if k not in cfg]
    if missing:
        print(f"  ABORT: map.json is missing {missing}")
        return 2

    companies = load_csv(proj / "data" / "companies.csv")
    rels = load_csv(proj / "data" / "relationships.csv")
    ts = load_csv(proj / "data" / "financials_timeseries.csv")

    orphans, unused = check_coverage(companies, cfg["layers"])
    if orphans:
        print(f"  ABORT: {len(orphans)} of {len(companies)} companies have no role in map.json's layers,")
        print(f"         so they would render in NO layer and the page would look fine anyway.")
        print(f"         First few: {orphans[:5]}")
        print(f"         Fix map.json's layers to match the roles in companies.csv.")
        if strict:
            return 1
    if unused:
        print(f"  note: layers declared but unused by any company: {unused}")

    unknown, unexplained = check_choke_why(companies, cfg.get("chokepoint_why", {}))
    if unknown:
        print(f"  ABORT: {len(unknown)} chokepoint_why key(s) match NO company in companies.csv,")
        print(f"         so the template would find no explanation and render the chokepoint bare.")
        print(f"         {unknown}")
        print(f"         Keys must be the EXACT companies.csv name.")
        if strict:
            return 1
    if unexplained:
        print(f"  note: chokepoints with no chokepoint_why line: {unexplained}")

    filled = sum(1 for c in companies if c.get("revenue_usd_b"))
    meta = {"date": date, "total": len(companies), "filled": filled}

    html = TPL.read_text()
    repl = {
        "__TITLE__": cfg["title"],
        "__SUBTITLE__": cfg["subtitle"],
        "__FINANCIALS_NOTE__": cfg["financials_note"],
        "__CHOKEPOINTS_NOTE__": cfg["chokepoints_note"],
        "__NOTES_PLACEHOLDER__": cfg["notes_placeholder"],
        "__STORAGE_KEY__": cfg["storage_key"],
        "__LAYERS__": json.dumps(cfg["layers"], ensure_ascii=False),
        "__CHOKE_WHY__": json.dumps(cfg.get("chokepoint_why", {}), ensure_ascii=False),
        "__BUILDMETA__": json.dumps(meta, ensure_ascii=False),
        "__COMPANIES__": json.dumps(companies, ensure_ascii=False),
        "__RELATIONSHIPS__": json.dumps(rels, ensure_ascii=False),
        "__TIMESERIES__": json.dumps(ts, ensure_ascii=False),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    for k in repl:
        assert k not in html, f"placeholder {k} survived"

    out_dir = proj / "artifact"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{cfg['storage_key']}.html"
    out.write_text(html)
    # resolve() both sides: relative_to() raises when one path is relative and the other absolute,
    # and it did -- AFTER the file was already written, so the build "failed" with correct output.
    try:
        shown = out.resolve().relative_to(ROOT.resolve())
    except ValueError:
        shown = out
    print(f"  Built {shown}: {len(companies)} companies, {filled} costed, "
          f"{len(rels)} relationships, {len(ts)} timeseries rows, dated {date}")
    return 0


def selftest():
    """The orphan check is the whole reason this file exists. Prove it fires."""
    layers = [{"role": "foundry", "label": "F", "desc": "d"}, {"role": "oem", "label": "O", "desc": "d"}]
    cases = [
        ("control: every company lands in a layer -> silent",
         [{"company": "A", "roles": "foundry"}, {"company": "B", "roles": "oem;idm"}], 0),
        ("catches the REAL 02 case: mineral roles vs semiconductor layers",
         [{"company": "MP Materials", "roles": "miner;refiner"},
          {"company": "Lynas", "roles": "miner;separator"}], 2),
        ("catches a single orphan hiding among good rows",
         [{"company": "A", "roles": "foundry"}, {"company": "Ghost", "roles": "smelter"}], 1),
        ("a company with NO roles at all is an orphan, not a pass",
         [{"company": "Blank", "roles": ""}], 1),
    ]
    fails = []
    for name, comps, want in cases:
        orphans, _ = check_coverage(comps, layers)
        ok = len(orphans) == want
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            fails.append(f"{name}: expected {want} orphans, got {len(orphans)}")

    # chokepoint_why: an unknown key renders a bare chokepoint without erroring.
    comps = [{"company": "CATL", "roles": "cell-maker", "chokepoint": "yes"},
             {"company": "Tesla", "roles": "automaker", "chokepoint": "no"}]
    why_cases = [
        ("control: exact key on a real chokepoint -> silent",
         {"CATL": "x"}, 0, 0),
        ("catches a key matching no company (the typo/stale-name case)",
         {"CATL": "x", "Catl Inc": "x"}, 1, 0),
        ("NEGATIVE: a correct key must not be flagged just because another is wrong",
         {"Catl Inc": "x"}, 1, 1),
        ("an unexplained chokepoint is INCOMPLETE, not unknown: 0 aborts, 1 note",
         {}, 0, 1),
        ("a why-line for a non-chokepoint company is legal, not unknown",
         {"CATL": "x", "Tesla": "x"}, 0, 0),
    ]
    for name, why, want_unknown, want_unexpl in why_cases:
        unknown, unexplained = check_choke_why(comps, why)
        ok = len(unknown) == want_unknown and len(unexplained) == want_unexpl
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            fails.append(f"{name}: want {want_unknown}/{want_unexpl}, "
                         f"got {len(unknown)}/{len(unexplained)}")

    print()
    if fails:
        print("SELFTEST FAILED:", fails)
        return 2
    print(f"SELFTEST PASSED. {len(cases) + len(why_cases)} cases.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(build(sys.argv[1], sys.argv[2]))
