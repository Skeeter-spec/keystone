#!/usr/bin/env python3
"""Rule 7. Every EDGAR filing a company cites must actually BE that company's filing.

WHY THIS EXISTS. On 2026-07-20 a financials burst built its candidate list by matching this repo's
`ticker` column against SEC's company_tickers.json. Ticker "NEO" resolved cleanly to CIK 1077183 --
NEOGENOMICS INC, a cancer diagnostics company. This repo's NEO is Neo Performance Materials, a
rare-earth magnet maker listed in Toronto that does not file with the SEC at all. The lookup SUCCEEDED
and returned the wrong company.

That row would have landed complete, sourced, source_tier 1, and entirely wrong, and NOTHING here would
have caught it: check_data.py rule 1 asserts a costed row HAS a filing_source, never that the filing is
ABOUT that company. An identifier that resolves is not the entity you meant. (The sibling repo
industrial-index learned the same lesson with URLs -- "reachability is not identity" -- and built
check_titles.py. This is keystone's equivalent, and it is late.)

WHY AN EXPLICIT MAP AND NOT NAME MATCHING. The obvious implementation compares the company name to the
SEC registrant name and complains when they differ. Measured against the 40 real rows, a
normalised-prefix match flagged FOUR legitimate bindings: AMD/ADVANCED MICRO DEVICES, TSMC/TAIWAN
SEMICONDUCTOR MANUFACTURING, UMC/UNITED MICROELECTRONICS, GM/General Motors. SQM's registrant is
"CHEMICAL & MINING CO OF CHILE INC", which shares no words with "SQM" at all. A check that cries wolf on
four correct rows gets tuned out, and a tuned-out check is worse than none because everyone believes it
is working.

So the binding is DATA, not a guess: shared/edgar_registrants.csv records (cik, sec_registrant, company)
approved once by a human. This check asserts membership, exactly. A new or changed CIK is not silently
accepted -- it fails until someone looks at the registrant name and approves the pair, which is precisely
the moment the NEO error would have died.
"""
import csv, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent.parent
MAP_PATH = ROOT / "shared" / "edgar_registrants.csv"
EDGAR_RE = re.compile(r"sec\.gov/Archives/edgar/data/(\d+)/")


def cik_of(url):
    m = EDGAR_RE.search(url or "")
    return m.group(1).lstrip("0") if m else None


def load_map(rows):
    """{cik: {company: registrant}} for approved bindings only."""
    out = {}
    for r in rows:
        if (r.get("approved") or "").strip().lower() != "yes":
            continue
        out.setdefault((r.get("cik") or "").strip().lstrip("0"), {})[
            (r.get("company") or "").strip()] = (r.get("sec_registrant") or "").strip()
    return out


def check(company_rows, bindings, label):
    problems = []
    for i, r in enumerate(company_rows, start=2):
        company = (r.get("company") or "").strip()
        cik = cik_of(r.get("filing_source") or "")
        if not cik:
            continue  # not an EDGAR citation; HKEX/SSE/other routes are out of scope for this rule
        known = bindings.get(cik)
        if not known:
            problems.append(
                f"{label}:{i} {company} cites EDGAR CIK {cik}, which has no approved binding in "
                f"shared/edgar_registrants.csv. Look up the registrant and add the pair before trusting it")
        elif company not in known:
            owner = ", ".join(sorted(known)) or "another company"
            reg = list(known.values())[0] if known else "?"
            problems.append(
                f"{label}:{i} {company} cites EDGAR CIK {cik}, but that CIK is registrant {reg!r}, "
                f"bound here to {owner}. A lookup that resolves is not the entity you meant")
    return problems


def run(root):
    if not MAP_PATH.exists():
        print(f"  missing {MAP_PATH}")
        return 1
    with open(MAP_PATH, newline="") as fh:
        bindings = load_map(list(csv.DictReader(fh)))
    problems = []
    for p in sorted(root.glob("projects/*/data/companies.csv")):
        with open(p, newline="") as fh:
            problems += check(list(csv.DictReader(fh)), bindings, p.parent.parent.name)
    for msg in problems:
        print("  " + msg)
    return 1 if problems else 0


def selftest():
    """Control = the REAL 2026-07-20 case. Negative = a clean tree must stay silent."""
    NEO_URL = "https://www.sec.gov/Archives/edgar/data/1077183/000107718326000011/"
    MP_URL = "https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/"
    bindings = load_map([
        {"cik": "1801368", "sec_registrant": "MP Materials Corp. / DE",
         "company": "MP Materials", "approved": "yes"},
        {"cik": "1077183", "sec_registrant": "NEOGENOMICS INC",
         "company": "NeoGenomics Inc", "approved": "yes"},
    ])
    cases = [
        # (name, rows, must_flag)
        ("CONTROL (real): Neo Performance Materials cites NeoGenomics' CIK",
         [{"company": "Neo Performance Materials", "filing_source": NEO_URL}], True),
        ("CONTROL: an EDGAR CIK with no approved binding at all",
         [{"company": "Lynas Rare Earths",
           "filing_source": "https://www.sec.gov/Archives/edgar/data/9999999/x/"}], True),
        ("NEGATIVE: a correctly bound row must NOT flag",
         [{"company": "MP Materials", "filing_source": MP_URL}], False),
        ("NEGATIVE: a non-EDGAR source (HKEX) is out of scope, must NOT flag",
         [{"company": "Ganfeng Lithium Group",
           "filing_source": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0331/x.pdf"}], False),
        ("NEGATIVE: an uncosted row with no source must NOT flag",
         [{"company": "Umicore", "filing_source": ""}], False),
    ]
    fails = []
    for name, rows, must_flag in cases:
        got = bool(check(rows, bindings, "fixture"))
        ok = got == must_flag
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            fails.append(name)
    print()
    if fails:
        print("SELFTEST FAILED:", fails)
        return 1
    print(f"SELFTEST PASSED. {len(cases)} cases.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run(ROOT))
