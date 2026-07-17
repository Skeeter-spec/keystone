#!/usr/bin/env python3
"""Refetch every staged edge's evidence_source and check the document actually names both endpoints.

    python3 tools/verify_edges.py projects/02-critical-minerals
    python3 tools/verify_edges.py --selftest

WHY THIS EXISTS. Research agents propose; nothing they say is load-bearing. This tool goes to the
source itself, because two failure modes are invisible from a worker's summary:

  REACHABILITY IS NOT IDENTITY. A URL returning 200 proves a page exists, not that it is the document
  the row claims. The classic miss is a LANDING PAGE cited instead of the filing: it resolves fine,
  looks fine in a report, and does not contain the fact.

  AN HONEST GRADE IS NOT A CORRECT FACT. A worker can label a row tier 1, in good faith, off a
  document it half read. So the test is not "did the worker sound careful", it is "does the cited
  document contain both company names".

This check is DELIBERATELY WEAK and you must not oversell it. Finding both names in a filing does NOT
prove the stated relationship is real, only that the row is not citing an unrelated document. It is a
floor, not a verdict. A human still reads the sentence. What it reliably catches: fabricated URLs,
landing pages, and rows whose evidence names neither party.

Network-dependent, so it is NOT part of gate.sh. Run it after a research burst, before merging.
"""
import csv, glob, io, pathlib, re, sys, urllib.request, html as htmllib

UA = "Keystone research (contact: scholarkeaton@protonmail.com)"

# The token that must appear for a company to count as named. Full CSV names carry parentheticals
# and legal suffixes that no filing spells out, so match on the distinctive part.
KEY = {
    "MP Materials": "MP Materials",
    "Lynas Rare Earths": "Lynas",
    "Shenghe Resources Holding": "Shenghe",
    "China Northern Rare Earth (Group) High-Tech": "Northern Rare Earth",
    "JL MAG Rare-Earth": "JL MAG",
    "Proterial Ltd (formerly Hitachi Metals)": "Proterial|Hitachi Metals",
    "Vacuumschmelze (VAC)": "Vacuumschmelze",
    "Neo Performance Materials": "Neo Performance",
    "Energy Fuels Inc": "Energy Fuels",
    "USA Rare Earth Inc": "USA Rare Earth",
    "Iluka Resources": "Iluka",
    "Albemarle Corporation": "Albemarle",
    "SQM (Sociedad Quimica y Minera de Chile)": "SQM|Sociedad Qu",
    "Ganfeng Lithium Group": "Ganfeng",
    "Tianqi Lithium Corporation": "Tianqi",
    "Pilbara Minerals (PLS Group Limited)": "Pilbara",
    "Lithium Americas Corp": "Lithium Americas",
    "Glencore plc": "Glencore",
    "CMOC Group Limited": "CMOC",
    "Zhejiang Huayou Cobalt": "Huayou",
    "Nornickel (MMC Norilsk Nickel)": "Nornickel|Norilsk",
    "Vale S.A.": "Vale",
    "Umicore": "Umicore",
    "BHP Group": "BHP",
    "Rio Tinto": "Rio Tinto",
    "Syrah Resources": "Syrah",
    "Yunnan Chihong Zinc & Germanium": "Chihong",
}

# NOTE: use .search(), never .match(). match() anchors at position 0, so the mid-URL alternatives
# (/investors/, /news/) could never fire and every landing page would sail through as clean. The
# selftest caught exactly that, which is the entire reason the selftest has a landing-page fixture.
LANDING_SMELL = re.compile(r"^https?://[^/]+/?$|/investors/?$|/news/?$|/search|\?q=", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.getcode(), r.headers.get("Content-Type", "")


def to_text(raw, ctype, url):
    if "pdf" in ctype.lower() or url.lower().endswith(".pdf"):
        try:
            import fitz  # PyMuPDF
        except ImportError:
            return None, "PDF but PyMuPDF not installed"
        try:
            doc = fitz.open(stream=raw, filetype="pdf")
            return " ".join(p.get_text() for p in doc), None
        except Exception as e:
            return None, f"PDF parse failed: {e}"
    t = raw.decode("utf-8", errors="replace")
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", htmllib.unescape(t)), None


def named(text, company):
    pat = KEY.get(company, re.escape(company))
    return re.search(pat, text, re.I) is not None


def verify(project):
    root = pathlib.Path(project)
    staged = sorted(glob.glob(str(root / "data" / "_incoming" / "edges_*.csv")))
    if not staged:
        print(f"no staged edge files in {root}/data/_incoming/")
        return 1
    rows = []
    for p in staged:
        with open(p, newline="") as fh:
            for r in csv.DictReader(fh):
                r["_file"] = pathlib.Path(p).name
                rows.append(r)

    cache, verdicts = {}, []
    for r in rows:
        url = r["evidence_source"].strip()
        edge = f"{r['from_company']} -> {r['to_company']}"
        if LANDING_SMELL.search(url):
            verdicts.append(("LANDING", edge, url, "looks like a landing page, not a document"))
            continue
        if url not in cache:
            try:
                raw, code, ctype = fetch(url)
                text, err = to_text(raw, ctype, url)
                cache[url] = (code, text, err, len(raw))
            except Exception as e:
                cache[url] = (None, None, str(e), 0)
        code, text, err, nbytes = cache[url]
        if code != 200 or text is None:
            verdicts.append(("UNREACHABLE", edge, url, err or f"http {code}"))
            continue
        a, b = named(text, r["from_company"]), named(text, r["to_company"])
        if a and b:
            verdicts.append(("OK", edge, url, f"both named, {nbytes//1024} KB"))
        elif a or b:
            missing = r["to_company"] if a else r["from_company"]
            verdicts.append(("HALF", edge, url, f"document never names {missing!r}"))
        else:
            verdicts.append(("NEITHER", edge, url, "document names neither endpoint"))

    order = {"NEITHER": 0, "HALF": 1, "UNREACHABLE": 2, "LANDING": 3, "OK": 4}
    verdicts.sort(key=lambda v: order[v[0]])
    for v, edge, url, note in verdicts:
        print(f"  [{v:11}] {edge}")
        print(f"                {note}")
    bad = [v for v in verdicts if v[0] != "OK"]
    print()
    print(f"  {len(verdicts) - len(bad)}/{len(verdicts)} edges cite a reachable document naming both endpoints")
    print("  NOTE: this is a floor, not a verdict. Both names present does NOT prove the relationship;")
    print("        a human still reads the sentence. It catches fabricated URLs and landing pages.")
    return 1 if bad else 0


def selftest():
    """Prove the checks fire. No network: exercise the pure logic."""
    doc = "Energy Fuels and Lynas both process monazite. Iluka Resources and Rio Tinto are HMS producers."
    cases = [
        ("control: both endpoints named", ("Energy Fuels Inc", "Lynas Rare Earths"), True, True),
        ("control: full CSV name maps to its filing token", ("Iluka Resources", "Rio Tinto"), True, True),
        ("catches an endpoint the document never names", ("Energy Fuels Inc", "Ganfeng Lithium Group"), True, False),
        ("catches a document naming neither", ("Tianqi Lithium Corporation", "Ganfeng Lithium Group"), False, False),
    ]
    failures = []
    for name, (a, b), want_a, want_b in cases:
        got_a, got_b = named(doc, a), named(doc, b)
        ok = (got_a == want_a) and (got_b == want_b)
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(name)
    smells = [
        ("landing page: bare domain", "https://investors.mpmaterials.com", True),
        ("landing page: /investors/", "https://lynasrareearths.com/investors/", True),
        ("real document passes", "https://www.sec.gov/Archives/edgar/data/1385849/000138584925000004/efr-20241231.htm", False),
    ]
    for name, url, want in smells:
        got = bool(LANDING_SMELL.search(url))
        ok = got == want
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(name)
    print()
    if failures:
        print(f"SELFTEST FAILED: {failures}")
        return 2
    print(f"SELFTEST PASSED. {len(cases) + len(smells)} cases.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(verify(sys.argv[1]))
