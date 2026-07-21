#!/usr/bin/env python3
"""Pull one company's annual figures from SEC XBRL, with the traps closed by construction.

    python3 tools/xbrl_extract.py --ticker BHP --expect "BHP Group"
    python3 tools/xbrl_extract.py --selftest

WHY THIS EXISTS. On 2026-07-20 this extractor was hand-written three times in one session, and each
rewrite had to re-earn the same four lessons. Three of them were caught only because I happened to print
the candidates and look; the fourth was caught only because I happened to notice a date. "I will remember
to look" is not a mechanism, and Keaton's rule is the right one: a solution that can be mechanized gets
mechanized, not pushed onto a human.

The four traps, all measured on real filings that day:

1. WRONG COMPANY. Ticker "NEO" resolves cleanly to CIK 1077183 = NEOGENOMICS INC, a cancer diagnostics
   company; this repo's NEO is Neo Performance Materials (TSX, no SEC filings). The lookup SUCCEEDS and
   returns the wrong company. ⇒ --expect is REQUIRED, and the (cik, company) pair must already be an
   approved binding in shared/edgar_registrants.csv. Same map tools/check_identity.py enforces at gate
   time, so fetch time and commit time cannot disagree. An unapproved pair REFUSES and prints the
   registrant so a human can look once and approve it.

2. THE WRONG SIBLING CONCEPT. Net income has up to three tags with different values. BHP FY2025:
   ProfitLossAttributableToOwnersOfParent 9.019 vs ProfitLoss 11.143 -- taking the consolidated line
   overstates the bottom line by 24%. Where minority interest is NEGATIVE the attributable figure is the
   LARGER one (Vale, Yunnan Chihong), so "pick the smaller" is not a rule. ⇒ priority-ordered concept
   lists, first match wins. NEVER max-value, never first-namespace-wins.

3. A STALE PERIOD, INCLUDING AN INSTANT. A first pass pulled Vale's net income off a 2012 us-gaap filing
   because it searched us-gaap before ifrs-full. Worse, Ford's tagged EntityCommonStockSharesOutstanding
   is dated 2011 -- fifteen years stale -- and would have produced a confidently wrong market cap. Flows
   were being checked for staleness; instants were not. ⇒ both are rejected if older than the reporting
   period.

4. SILENCE ABOUT THE FORK. The three bugs above were all caught by printing every candidate and reading
   them. ⇒ candidates are ALWAYS printed. There is no quiet mode.
"""
import argparse, csv, datetime, json, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).parent.parent
BINDINGS = ROOT / "shared" / "edgar_registrants.csv"
UA = "keystone-atlas research scholarkeaton@protonmail.com"
ANNUAL = {"10-K", "20-F", "40-F", "10-K/A", "20-F/A", "40-F/A"}

REV = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
       "RevenueFromContractWithCustomerIncludingAssessedTax", "Revenue"]
NI = ["NetIncomeLoss", "ProfitLossAttributableToOwnersOfParent", "ProfitLoss"]
RD = ["ResearchAndDevelopmentExpense"]
CAP = ["PaymentsToAcquirePropertyPlantAndEquipment",
       "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities",
       "PaymentsToAcquireProductiveAssets",
       "AdditionsOtherThanThroughBusinessCombinationsPropertyPlantAndEquipment"]
SHARES = ["EntityCommonStockSharesOutstanding", "NumberOfSharesOutstanding"]
NAMESPACES = ("us-gaap", "ifrs-full", "dei")


def _days(a, b):
    try:
        return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
    except Exception:
        return -1


def candidates(facts, concepts, flow=True):
    """Every annual entry for these concepts, across namespaces. Unfiltered by year on purpose."""
    out = []
    for ns in NAMESPACES:
        for c in concepts:
            for unit, arr in facts.get(ns, {}).get(c, {}).get("units", {}).items():
                if unit not in ("USD", "shares"):
                    continue
                for e in arr:
                    if e.get("form") not in ANNUAL:
                        continue
                    if flow and (e.get("fp") != "FY"
                                 or not 330 <= _days(e.get("start", ""), e.get("end", "")) <= 400):
                        continue
                    out.append({"ns": ns, "concept": c, "unit": unit, "val": e["val"],
                                "end": e["end"], "accn": e.get("accn")})
    return out


def reporting_period(facts):
    """The latest annual revenue period end. None for a pre-revenue filer (Lithium Americas)."""
    c = candidates(facts, REV, flow=True)
    return max((x["end"] for x in c), default=None)


def pick(facts, concepts, period_end, flow=True):
    """Priority-ordered: the FIRST concept with a fresh entry wins. Never max-value.

    Freshness: a flow must land in the reporting year; an instant must not predate the reporting
    period end (cover-page share counts are dated after year end, which is fine; Ford's 2011 is not).
    """
    if not period_end:
        return None, []
    year = int(period_end[:4])
    allc = candidates(facts, concepts, flow=flow)
    for c in concepts:
        fresh = []
        for x in allc:
            if x["concept"] != c:
                continue
            if flow and int(x["end"][:4]) != year:
                continue
            if not flow and x["end"] < period_end:
                continue  # TRAP 3: a stale instant (Ford's 2011 share count)
            fresh.append(x)
        if fresh:
            return max(fresh, key=lambda x: x["end"]), allc
    return None, allc


def load_bindings():
    if not BINDINGS.exists():
        return {}
    with open(BINDINGS, newline="") as fh:
        return {((r.get("cik") or "").strip().lstrip("0"), (r.get("company") or "").strip()):
                (r.get("sec_registrant") or "").strip()
                for r in csv.DictReader(fh) if (r.get("approved") or "").strip().lower() == "yes"}


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.load(urllib.request.urlopen(req, timeout=60))


def resolve(ticker):
    d = _get("https://www.sec.gov/files/company_tickers.json")
    for v in d.values():
        if v["ticker"].upper() == ticker.upper():
            return str(v["cik_str"]), v["title"]
    return None, None


def report(facts, period_end, label):
    print(f"\n== {label} == reporting period end {period_end}")
    for name, concepts, flow in [("REVENUE", REV, True), ("NET_INCOME", NI, True),
                                 ("R&D", RD, True), ("CAPEX", CAP, True), ("SHARES", SHARES, False)]:
        chosen, allc = pick(facts, concepts, period_end, flow=flow)
        # TRAP 4: the fork is ALWAYS printed. There is no quiet mode.
        year = int(period_end[:4]) if period_end else None
        # newest-first, so the per-concept dedup keeps the CURRENT entry, not the oldest.
        # (Shipped backwards once: the selftest was green because every fixture had exactly one
        #  entry per concept, so ordering never mattered. The live BHP run printed 2016 rows.)
        seen = set()
        for x in sorted(allc, key=lambda x: x["end"], reverse=True):
            if x["concept"] in seen:
                continue
            seen.add(x["concept"])
            fresh = (int(x["end"][:4]) == year) if flow else (x["end"] >= period_end)
            mark = "<-- USED" if chosen and x["concept"] == chosen["concept"] and fresh else \
                   ("" if fresh else "(stale, rejected)")
            v = x["val"] / 1e9 if x["unit"] == "USD" else x["val"] / 1e6
            print(f"   {name:11} {v:>14.4f}{'B' if x['unit']=='USD' else 'M sh'} "
                  f"{x['end']}  [{x['ns']}:{x['concept']}] {mark}")
        if not allc:
            print(f"   {name:11} {'--':>14}   not reported -> leave EMPTY, do not write 0")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--expect", required=True,
                    help="the company name as it appears in companies.csv (REQUIRED: trap 1)")
    a = ap.parse_args(argv)
    cik, registrant = resolve(a.ticker)
    if not cik:
        print(f"REFUSED: ticker {a.ticker!r} is not in SEC's company_tickers.json.")
        return 2
    approved = load_bindings()
    if (cik.lstrip("0"), a.expect) not in approved:
        print(f"REFUSED: ticker {a.ticker!r} resolves to CIK {cik}, SEC registrant {registrant!r}.")
        print(f"  That is not an approved binding for {a.expect!r} in shared/edgar_registrants.csv.")
        print(f"  A lookup that resolves is not the entity you meant. Read the registrant above; if it")
        print(f"  really is {a.expect!r}, add the row and re-run. (Ticker NEO resolves to NEOGENOMICS.)")
        return 2
    facts = _get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik.zfill(10)}.json").get("facts", {})
    pe = reporting_period(facts)
    if not pe:
        print(f"  {a.expect}: no annual revenue tag (pre-revenue filer?). Revenue stays EMPTY, not 0.")
        return 0
    report(facts, pe, f"{a.expect} ({a.ticker}, CIK {cik})")
    return 0


def selftest():
    """Fixtures are the REAL shapes from 2026-07-20, kept as permanent regressions."""
    def flow(concept, ns, val, end, start=None):
        return {"form": "10-K", "fp": "FY", "start": start or f"{int(end[:4])}-01-01",
                "end": end, "val": val, "accn": "x"}

    # BHP carries a decade of history per concept. The 2016 rows are the regression: an earlier
    # build sorted ascending and surfaced THEM, and every single-entry fixture passed anyway.
    bhp = {"ifrs-full": {
        "Revenue": {"units": {"USD": [flow("", "", 28.567e9, "2016-06-30", "2015-07-01"),
                                      flow("", "", 51.262e9, "2025-06-30", "2024-07-01")]}},
        "ProfitLossAttributableToOwnersOfParent": {"units": {"USD": [
            flow("", "", -6.385e9, "2016-06-30", "2015-07-01"),
            flow("", "", 9.019e9, "2025-06-30", "2024-07-01")]}},
        "ProfitLoss": {"units": {"USD": [flow("", "", 11.143e9, "2025-06-30", "2024-07-01")]}}}}
    sqm = {"ifrs-full": {
        "Revenue": {"units": {"USD": [flow("", "", 4.5288e9, "2024-12-31")]}},
        "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities": {"units": {"USD": [flow("", "", 0.9718e9, "2024-12-31")]}},
        "AdditionsOtherThanThroughBusinessCombinationsPropertyPlantAndEquipment": {"units": {"USD": [flow("", "", 0.9851e9, "2024-12-31")]}}}}
    vale = {"ifrs-full": {
        "Revenue": {"units": {"USD": [flow("", "", 38.403e9, "2025-12-31")]}},
        "AdditionsOtherThanThroughBusinessCombinationsPropertyPlantAndEquipment": {"units": {"USD": [flow("", "", 5.469e9, "2025-12-31")]}}}}
    ford = {"us-gaap": {"Revenues": {"units": {"USD": [flow("", "", 187.267e9, "2025-12-31")]}}},
            "dei": {"EntityCommonStockSharesOutstanding": {"units": {"shares": [
                {"form": "10-K", "end": "2011-02-14", "val": 3_711_860_000, "accn": "x"}]}}}}
    tsla = {"us-gaap": {"Revenues": {"units": {"USD": [flow("", "", 94.827e9, "2025-12-31")]}}},
            "dei": {"EntityCommonStockSharesOutstanding": {"units": {"shares": [
                {"form": "10-K", "end": "2026-01-23", "val": 3_752_430_000, "accn": "x"}]}}}}

    cases = []
    def check(name, got, want):
        ok = got == want
        cases.append((name, ok, got, want))

    p, _ = pick(bhp, NI, reporting_period(bhp))
    check("BHP net income takes ATTRIBUTABLE 9.019, not consolidated 11.143",
          round(p["val"] / 1e9, 3), 9.019)
    p, _ = pick(sqm, CAP, reporting_period(sqm))
    check("SQM capex takes CASH-FLOW 0.972, not PP&E-additions 0.985",
          round(p["val"] / 1e9, 3), 0.972)
    p, _ = pick(vale, CAP, reporting_period(vale))
    check("Vale capex FALLS BACK to PP&E additions 5.469 when no cash-flow tag exists",
          round(p["val"] / 1e9, 3), 5.469)
    p, _ = pick(ford, SHARES, reporting_period(ford), flow=False)
    check("Ford's 2011 share count is REJECTED as a stale instant", p, None)
    p, _ = pick(tsla, SHARES, reporting_period(tsla), flow=False)
    check("NEGATIVE: Tesla's post-year-end cover-page share count is ACCEPTED",
          p["val"], 3_752_430_000)
    check("NEGATIVE: a pre-revenue filer yields no reporting period (revenue stays empty)",
          reporting_period({"us-gaap": {}}), None)
    # The display bug that actually shipped: pick() was correct the whole time, so every
    # selection fixture stayed green while report() printed BHP's 2016 rows and marked the
    # current ones absent. A test of the chooser could never have caught it; this reads the
    # rendered output, which is the surface that was wrong.
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        report(bhp, reporting_period(bhp), "fixture")
    out = buf.getvalue()
    check("REGRESSION: report() shows the CURRENT period, not the oldest (2016 must not appear)",
          "28.5670" in out, False)
    check("REGRESSION: report() marks the chosen attributable figure as USED",
          "9.0190" in out and "<-- USED" in out, True)
    check("the losing sibling is still SHOWN, so the fork stays visible",
          "11.1430" in out, True)

    b = load_bindings()
    check("CONTROL: (NeoGenomics CIK, Neo Performance Materials) is NOT an approved binding",
          ("1077183", "Neo Performance Materials") in b, False)
    check("NEGATIVE: (MP's CIK, MP Materials) IS an approved binding",
          ("1801368", "MP Materials") in b, True)

    fails = [n for n, ok, *_ in cases if not ok]
    for n, ok, got, want in cases:
        print(f"  {'ok  ' if ok else 'DEAD'}  {n}" + ("" if ok else f"   got={got!r} want={want!r}"))
    print()
    if fails:
        print("SELFTEST FAILED:", fails)
        return 1
    print(f"SELFTEST PASSED. {len(cases)} cases.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1:]))
