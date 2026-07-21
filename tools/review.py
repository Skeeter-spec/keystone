#!/usr/bin/env python3
"""Advisory triage: where does a map CLAIM more than it can show?

    python3 tools/review.py                          every map, ranked
    python3 tools/review.py projects/02-critical-minerals
    python3 tools/review.py --selftest

WHAT THIS IS FOR. tools/check_data.py asks "is the data internally correct?" and fails the gate when it
is not. This asks a different and softer question: "is anything here presented as more settled than its
evidence supports?" Those findings are judgement calls, so this NEVER fails the gate and NEVER writes
gaps.csv. It proposes; a person or a burst confirms. A gap row needs `searched` and `would_close_it`,
and only someone who actually opened the documents can write those honestly.

🔴 THE ONE IDEA THE WHOLE FILE RESTS ON:

    A GAP IS A CLAIM WHOSE EVIDENCE IS WEAKER THAN ITS PRESENTATION.

Not "a thing we have not done yet". That distinction decides every rule below, and getting it wrong
would have killed the tool on day one. Measured 2026-07-20: the seven foundation maps hold 51
chokepoints with ZERO edges between them. A rule that flagged "chokepoint with no edge" would fire 51
times on maps that are doing nothing wrong -- a foundation brief presents hypotheses AS hypotheses and
over-claims nothing. It would then be switched off, and this repo's oldest lesson is that a check which
fires on everything gets bypassed, after which it reports exactly what a clean repo reports.

So every rule is SCOPED BY THE README STATUS LABEL. The same data shape is a finding on a map that calls
itself Mapped and silence on one that calls itself Foundation only, because the label is the claim.
02-critical-minerals is labelled Mapped with 3 of its 5 chokepoints carrying no edge at all; that is the
Siemens Energy case three times over, and it sat unreported for four days.

SUPPRESSION IS WHAT MAKES IT CONVERGE. A candidate whose subject is already named in that map's
gaps.csv is not reported again. Without it the list never shrinks, every run looks identical, and the
tool becomes wallpaper. With it, working the list down is visible progress.

Exit 0 always when the data is readable: findings here are advice, not failure. Exit 2 = broken.
"""
import argparse, csv, collections, glob, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent.parent
FIN = ("revenue_usd_b", "net_income_usd_b", "market_cap_usd_b", "rd_spend_usd_b", "capex_usd_b")
TRACKERS = ("stockanalysis", "companiesmarketcap", "tracker")
# A map that presents findings. "Foundation only" and "Costed" make no claim about relationships.
CLAIMS_EDGES = ("Mapped", "Edges started")
COMPETES_SHARE_LIMIT = 0.34   # the README calls dependencies the payoff; 02 shipped at 47%
STALE_YEARS = 3               # relative to that map's OWN newest evidence, never to today's clock


def g(row, key):
    return (row.get(key) or "").strip()


def load(p):
    if not p.exists():
        return []
    with open(p, newline="") as fh:
        return list(csv.DictReader(fh))


def status_of(readme_text, num):
    """The label a map claims, read off the FRONT of the last table cell.

    Same parsing as check_data.py rule 6, and for the same reason: a substring match over the whole row
    reads a claim out of prose. 04's honest status says "...not yet Mapped".
    """
    row = re.search(rf"^\|\s*{re.escape(num)}\s*\|(.+)$", readme_text, re.M)
    if not row:
        return ""
    cells = [c.strip() for c in row.group(1).split("|")]
    last = next((c for c in reversed(cells) if c), "")
    return last.lstrip("*").strip()


def claims_edges(status):
    return any(status.startswith(s) for s in CLAIMS_EDGES)


def degrees(rels):
    d = collections.Counter()
    for r in rels:
        d[g(r, "from_company")] += 1
        d[g(r, "to_company")] += 1
    return d


def already_recorded(gaps, subject):
    """Suppression. A subject named in any open gap row is considered triaged."""
    for gap in gaps:
        if (g(gap, "status") or "open") == "closed":
            continue
        if subject and subject in g(gap, "subject"):
            return True
    return False


def review(slug, status, companies, rels, gaps):
    """Pure. Returns [(priority, rule, subject, message)]. Lower priority sorts first."""
    out = []
    deg = degrees(rels)
    costed = [c for c in companies if any(g(c, x) for x in FIN)]

    # R1 -- the Siemens Energy shape. Only a map claiming edges can under-evidence one.
    if claims_edges(status):
        for c in companies:
            if g(c, "chokepoint") != "yes" or deg[g(c, "company")]:
                continue
            if already_recorded(gaps, g(c, "company")):
                continue
            out.append((1, "R1 unevidenced-flag", g(c, "company"),
                        f"flagged a chokepoint but has NO sourced edge, on a map presented as {status.split('.')[0]!r}"))

    # R2 -- the rule that carries this forward. Any future map promoted to Mapped without a gaps pass
    # trips it, and promotion is exactly when over-claiming happens.
    if claims_edges(status) and not gaps:
        out.append((1, "R2 no-gaps-recorded", slug,
                    "presents findings but records ZERO gaps. A burst that found no absences at all is "
                    "rare; more often nobody wrote them down"))

    # R3 -- stale evidence, judged against this map's OWN newest evidence so the verdict does not
    # change with the wall clock.
    dated = sorted(g(r, "evidence_date") for r in rels if g(r, "evidence_date"))
    if dated:
        newest_year = int(dated[-1][:4])
        for r in rels:
            d = g(r, "evidence_date")
            if not d or newest_year - int(d[:4]) < STALE_YEARS:
                continue
            subj = f"{g(r, 'from_company')} -> {g(r, 'to_company')}"
            if already_recorded(gaps, g(r, "from_company")) or already_recorded(gaps, subj):
                continue
            out.append((2, "R3 stale-evidence", subj,
                        f"evidence dated {d}, {newest_year - int(d[:4])}y older than this map's newest. "
                        f"Re-check before anyone leans on it"))

    # R4 -- a quality signal, not a gap. The README says dependencies are the payoff.
    if claims_edges(status) and rels:
        cw = sum(1 for r in rels if g(r, "relationship_type") == "competes-with")
        if cw / len(rels) > COMPETES_SHARE_LIMIT:
            out.append((2, "R4 competes-with-heavy", slug,
                        f"{cw} of {len(rels)} edges ({100*cw//len(rels)}%) are competes-with, which is "
                        f"not a dependency. The payoff of this map is thinner than the edge count suggests"))

    # R5 -- mixed provenance inside one tier. NOT auto-fixable: source_tier is a ROW-level column and
    # the row holds figures from different sources. Reported once per map, not once per row, because
    # 39 identical lines is noise and the finding is structural.
    mixed = [c for c in costed if g(c, "source_tier") == "1" and g(c, "market_cap_usd_b")
             and any(t in (g(c, "notes")).lower() for t in TRACKERS)]
    if mixed:
        out.append((3, "R5 mixed-provenance", slug,
                    f"{len(mixed)} of {len(costed)} costed rows are labelled source_tier 1 while their "
                    f"market cap came from a tracker. The notes say so; the tier column does not"))

    # R6 -- informational. An isolated node is not wrong, but on a map whose product is the edges it is
    # worth seeing the count.
    if claims_edges(status):
        iso = [g(c, "company") for c in companies if not deg[g(c, "company")]]
        if iso:
            out.append((4, "R6 isolated-nodes", slug,
                        f"{len(iso)} of {len(companies)} companies have no edge at all"))
    return out


def run(root):
    readme = (root / "README.md")
    text = readme.read_text() if readme.exists() else ""
    findings = []
    for data_dir in sorted(glob.glob(str(root / "projects" / "*" / "data"))):
        d = pathlib.Path(data_dir)
        slug = d.parent.name
        if slug == "_kit":
            continue
        status = status_of(text, slug.split("-")[0])
        findings.append((slug, status, review(slug, status,
                                              load(d / "companies.csv"),
                                              load(d / "relationships.csv"),
                                              load(d / "gaps.csv"))))
    return findings


def report(findings):
    total = 0
    for slug, status, items in findings:
        if not items:
            continue
        total += len(items)
        label = status.split(".")[0] or "?"
        print(f"\n  {slug}  [{label}]")
        for prio, rule, subject, msg in sorted(items):
            mark = {1: "!!", 2: " !", 3: "  ", 4: "  "}[prio]
            print(f"   {mark} {rule:24} {subject}")
            print(f"        {msg}")
    # Two populations, and conflating them is how a list like this dies. !! items are RESOLVABLE: a map
    # claims something it cannot show, and recording or dismissing it makes the line go away. The rest
    # are STANDING SIGNALS about the shape of the data -- isolated nodes and a row-level source_tier
    # holding mixed-provenance figures do not "get fixed" by writing a gap row, and pretending they
    # should would leave a permanently non-zero list that everyone learns to ignore.
    must = sum(1 for _, _, items in findings for p, _, _, _ in items if p == 1)
    review_ = sum(1 for _, _, items in findings for p, _, _, _ in items if p == 2)
    print()
    if total:
        print(f"  {total} advisory finding(s): {must} must resolve, {review_} worth reviewing, "
              f"{total - must - review_} standing. None fail the gate.")
        print("  !! MUST RESOLVE  a map claims more than it can show. Record it in that map's")
        print("                   data/gaps.csv, or dismiss it; either way it stops being reported.")
        print("   ! WORTH A LOOK  evidence that may have aged out, or a map whose edges are thinner")
        print("                   than their count suggests. Recordable, but may legitimately stand.")
        print("     STANDING      the shape of the data. These do not go away by writing a gap row,")
        print("                   and treating them as a to-do list is how a list like this gets ignored.")
    else:
        print("  No advisory findings: nothing is presented as more settled than its evidence supports.")
    return 0


# ---------------------------------------------------------------------------
# selftest. The load-bearing case is the NEGATIVE: identical data, different label.
# ---------------------------------------------------------------------------
def selftest():
    choke = {"company": "Siemens Energy", "chokepoint": "yes"}
    other = {"company": "Vertiv", "chokepoint": "no"}
    edge = {"from_company": "Vertiv", "to_company": "Microsoft",
            "relationship_type": "sells-equipment-to", "evidence_date": "2026-02-01"}
    gap = {"subject": "Siemens Energy -> data centre operators", "kind": "unevidenced-flag",
           "status": "open", "searched": "x", "would_close_it": "y"}

    def rules(*a, **k):
        return {r.split()[0] for _, r, _, _ in review(*a, **k)}

    cases = [
        # The gaps list here must NOT name Siemens Energy: an earlier version of this fixture passed
        # the suppressing row AND expected R1 to fire, so the case failed on its own contradiction.
        # Worth keeping the note -- it is easy to write a positive case that silently tests suppression.
        ("R1 fires: chokepoint with no edge on a Mapped map",
         lambda: "R1" in rules("m", "Mapped.", [choke, other], [edge], [{**gap, "subject": "something else"}])),
        ("🔴 R1 SILENT on IDENTICAL data labelled 'Foundation only' (the 51-flag case)",
         lambda: "R1" not in rules("m", "Foundation only", [choke, other], [], [])),
        ("🔴 R1 SILENT on 'Costed' -- financials in, no claim about edges yet",
         lambda: "R1" not in rules("m", "Costed.", [choke, other], [], [])),
        ("🔴 SUPPRESSION: R1 silent once a gap row names that subject",
         lambda: "R1" not in rules("m", "Mapped.", [choke], [edge], [gap])),
        ("suppression does NOT apply to a CLOSED gap row",
         lambda: "R1" in rules("m", "Mapped.", [choke], [edge], [{**gap, "status": "closed"}])),
        ("R2 fires: a Mapped map with no gaps.csv at all",
         lambda: "R2" in rules("m", "Mapped.", [other], [edge], [])),
        ("R2 SILENT once any gap exists",
         lambda: "R2" not in rules("m", "Mapped.", [other], [edge], [gap])),
        ("R2 SILENT on a foundation map",
         lambda: "R2" not in rules("m", "Foundation only", [other], [], [])),
        ("R3 fires: an edge 5y older than this map's newest",
         lambda: "R3" in rules("m", "Mapped.", [other],
                               [edge, {**edge, "from_company": "Glencore", "evidence_date": "2019-05-29"}], [gap])),
        ("R3 SILENT when every edge is recent",
         lambda: "R3" not in rules("m", "Mapped.", [other], [edge], [gap])),
        ("🔴 R3 judges against the MAP's newest date, not the wall clock",
         lambda: "R3" not in rules("m", "Mapped.", [other],
                                   [{**edge, "evidence_date": "2019-01-01"},
                                    {**edge, "evidence_date": "2019-05-29"}], [gap])),
        ("R4 fires: competes-with over the limit",
         lambda: "R4" in rules("m", "Mapped.", [other],
                               [{**edge, "relationship_type": "competes-with"}], [gap])),
        ("R4 SILENT: a dependency-heavy map",
         lambda: "R4" not in rules("m", "Mapped.", [other], [edge] * 3, [gap])),
        ("R5 fires: tier-1 row whose market cap came from a tracker",
         lambda: "R5" in rules("m", "Mapped.",
                               [{**other, "revenue_usd_b": "1", "market_cap_usd_b": "2",
                                 "source_tier": "1", "notes": "cap from stockanalysis.com"}], [edge], [gap])),
        ("R5 SILENT when the market cap is not tracker-sourced",
         lambda: "R5" not in rules("m", "Mapped.",
                                   [{**other, "revenue_usd_b": "1", "market_cap_usd_b": "2",
                                     "source_tier": "1", "notes": "shares from the filing cover page"}],
                                   [edge], [gap])),
        ("a clean Mapped map produces NOTHING",
         lambda: not rules("m", "Mapped.", [{**other, "company": "A"}],
                           [{**edge, "from_company": "A", "to_company": "A"}], [gap])),
    ]
    failures = []
    for name, fn in cases:
        try:
            ok = bool(fn())
        except Exception as e:  # a control that reports failure via a traceback is not a control
            ok, name = False, f"{name}  [RAISED {type(e).__name__}: {e}]"
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(name)

    # End-to-end: is run() actually wired to the rules? A rule that is never invoked reports exactly
    # what a clean repo reports. Measured this session on check_data.py, where deleting the call left
    # its whole suite green.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        d = root / "projects" / "02-fixture" / "data"
        d.mkdir(parents=True)
        with open(d / "companies.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["company", "chokepoint"]); w.writeheader()
            w.writerow({"company": "Fixture Corp", "chokepoint": "yes"})
        (d / "relationships.csv").write_text("from_company,to_company,relationship_type\n")
        (root / "README.md").write_text("| 02 | Fixture | **Mapped.** done |\n")
        wired = any(items for _, _, items in run(root))
        print(f"  {'ok  ' if wired else 'DEAD'}  WIRING: run() reaches the rules on a real tree")
        if not wired:
            failures.append("run() never reaches the rules")

    print()
    if failures:
        print(f"SELFTEST FAILED, {len(failures)} case(s):")
        for f in failures:
            print(f"  - {f}")
        return 2
    print(f"SELFTEST PASSED. {len(cases) + 1} cases: each rule fires on its own shape, stays silent when "
          f"the map does not claim that much, and stops once a gap records it.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project", nargs="?", help="one project dir; omit for every map")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        print("SELFTEST: does each rule fire on its own shape, and stay quiet otherwise?")
        return selftest()
    findings = run(ROOT)
    if a.project:
        want = pathlib.Path(a.project).name
        findings = [f for f in findings if f[0] == want]
        if not findings:
            print(f"  no such project: {a.project}")
            return 2
    print("REVIEW: where does a map claim more than it can show?")
    return report(findings)


if __name__ == "__main__":
    sys.exit(main())
