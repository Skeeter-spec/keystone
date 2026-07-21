#!/usr/bin/env python3
"""Refetch the document under every FINANCIAL FIGURE, and check it names the company.

    python3 tools/verify_sources.py projects/01-semiconductor
    python3 tools/verify_sources.py --all
    python3 tools/verify_sources.py --selftest

WHY THIS EXISTS, AND WHY ITS ABSENCE WAS THE BIGGEST HOLE IN THE REPO. tools/verify_edges.py refetches
every relationship's cited URL and checks the document names both endpoints. Nothing did that for the
URL under a REVENUE LINE. Measured 2026-07-21: 84 citations across 71 distinct URLs, 62 of them SEC,
and not one had ever been fetched a second time. tools/check_data.py rule 1 asserts a costed row HAS a
filing_source; tools/check_identity.py asserts an EDGAR CIK is bound to the right company name. Neither
opens the document.

The asymmetry was arbitrary. "Sourced or it does not exist" is the README's promise about figures at
least as much as about edges, and a dead or wrong citation under a live number is exactly the silent
failure this repo keeps finding: the page renders, the figure looks sourced, and the link goes nowhere.

REUSE, DO NOT REIMPLEMENT. Everything hard here is already solved and already mutation-tested in
verify_edges.py, so this file imports it rather than growing a second copy that can drift:

  fetch()                browser-UA retry, because a corporate newsroom refuses a robot while SEC
                         refuses the browser string -- both are tried, in that order
  looks_like_error_page  an Akamai "Access Denied" body ECHOES THE REQUESTED URL, so a refusal page can
                         name the very company it is refusing and verify clean
  named()                word-bounded, because "Vale" matched "prevalent" and "Ford" matched
                         "Abbotsford" in this repo's real data
  KEY                    our roster name is not the document's name: nothing files as "Amazon (AWS)"
  to_text()              PDFs via PyMuPDF, which is most of the non-SEC citations
  LANDING_SMELL          an index page is not a filing

A row citing several URLs (Samsung cites two) passes if the set BETWEEN them names the company: the
figures were assembled from both documents, so requiring each one alone to carry the name would be a
stricter test than the row actually claims.

Network, so it is NOT in tools/gate.sh. The gate is offline on purpose -- a gate that needs wifi gives
different answers on different wifi, and a check that flakes gets bypassed. This runs at burst time,
next to verify_edges.py.

Exit 0 = every costed row's citation checked out. Exit 1 = at least one did not. Exit 2 = broken.
"""
import argparse, csv, datetime, glob, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import verify_edges as V  # noqa: E402 -- the shared, already-hardened fetch/parse/match machinery

ROOT = pathlib.Path(__file__).parent.parent
FIN = ("revenue_usd_b", "net_income_usd_b", "market_cap_usd_b", "rd_spend_usd_b", "capex_usd_b")


def g(row, key):
    return (row.get(key) or "").strip()


def urls_of(row):
    """A row may cite several documents, separated by ';'."""
    return [u.strip() for u in g(row, "filing_source").split(";") if u.strip()]


def judge(company, docs):
    """Pure, so the selftest can drive it without a network.

    docs: [(url, text_or_None, error_or_None)]. Returns (verdict, detail).
    """
    if not docs:
        return "NO-SOURCE", "costed row with no filing_source at all"
    reasons, named_anywhere = [], False
    for url, text, err in docs:
        if err:
            reasons.append(f"{url}: {err}")
            continue
        if V.LANDING_SMELL.search(url):
            reasons.append(f"{url}: looks like a landing or index page, not a filing")
            continue
        if V.looks_like_error_page(text):
            reasons.append(f"{url}: served a block or error page, not a document")
            continue
        if V.named(text, company):
            named_anywhere = True
        else:
            reasons.append(f"{url}: reachable, but never names {company!r}")
    if named_anywhere:
        return "OK", f"{len(docs)} document(s) fetched, company named"
    return "FAIL", "; ".join(reasons) or "no document named the company"


def verify(project, cache):
    root = pathlib.Path(project)
    rows = []
    p = root / "data" / "companies.csv"
    if p.exists():
        with open(p, newline="") as fh:
            rows = [r for r in csv.DictReader(fh) if any(g(r, c) for c in FIN)]
    results = []
    for r in rows:
        company = g(r, "company")
        docs = []
        for url in urls_of(r):
            if url not in cache:
                try:
                    raw, code, ctype = V.fetch(url)
                    if code != 200:
                        cache[url] = (None, f"http {code}")
                    else:
                        text, err = V.to_text(raw, ctype, url)
                        cache[url] = (text, err)
                except Exception as e:  # noqa: BLE001
                    cache[url] = (None, f"{type(e).__name__}: {e}")
            text, err = cache[url]
            docs.append((url, text, err if text is None else None))
        results.append((company, *judge(company, docs)))
    return results


def write_receipt(proj, results):
    """Leave a dated receipt so 'has anyone opened these documents?' is answerable by a command.

    Measured 2026-07-21: 82 costed rows carried citations nothing had EVER fetched, and the only
    reason anyone found out was that someone thought to ask. A gate can be green forever over
    unopened sources, because the gate is offline by design. So the fact of verification becomes
    DATA, and tools/review.py rule R7 reads it.
    """
    ok = sum(1 for _, v, _ in results if v == "OK")
    (pathlib.Path(proj) / "data" / "_verified.json").write_text(json.dumps({
        "tool": "verify_sources.py", "checked": len(results), "ok": ok,
        "verified_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }, indent=2) + "\n")


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("SELFTEST: does it pass a real document and refuse the near-misses?")
        return selftest()
    projects = ([pathlib.Path(p).parent.parent for p in
                 sorted(glob.glob(str(ROOT / "projects" / "*" / "data" / "companies.csv")))]
                if a.all or not a.project else [pathlib.Path(a.project)])
    cache, bad, total = {}, 0, 0
    for proj in projects:
        results = verify(proj, cache)
        if not results:
            continue
        write_receipt(proj, results)
        fails = [x for x in results if x[1] != "OK"]
        total += len(results)
        bad += len(fails)
        print(f"\n  {proj.name}: {len(results) - len(fails)}/{len(results)} costed rows cite a document "
              f"that names them")
        for company, verdict, detail in fails:
            print(f"    [{verdict}] {company}")
            print(f"        {detail}")
    print(f"\n  {total - bad}/{total} costed rows verified across {len(cache)} distinct documents.")
    if bad:
        print("  A failure is a FINDING, not a licence to delete the figure: record it as an")
        print("  'unreachable' gap row, or replace the citation with one that resolves.")
    return 1 if bad else 0


# ---------------------------------------------------------------------------
# selftest. Drives judge() directly: no network, and every fixture is a real shape from this repo.
# ---------------------------------------------------------------------------
def selftest():
    FILING = ("https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm",
              "NVIDIA Corporation reported record revenue for the fourth quarter " * 40, None)
    # The real Akamai body from 2026-07-20: it echoes the URL, so it NAMES the company it is refusing.
    DENIED = ("https://www.marvell.com/company/newsroom/marvell-expands-collaboration-aws.html",
              'Access Denied You don\'t have permission to access "marvell-expands-collaboration-aws" '
              'on this server. Reference #18.ab0c2e17 https://errors.edgesuite.net/18.ab0c2e17', None)
    LANDING = ("https://investors.mpmaterials.com", "MP Materials investor relations " * 200, None)
    DEAD = ("https://images.samsung.com/gone.pdf", None, "HTTP Error 404: Not Found")

    cases = [
        ("a real filing that names the company PASSES", "Nvidia", [FILING], "OK"),
        ("🔴 an error page that NAMES the company still FAILS", "Marvell Technology", [DENIED], "FAIL"),
        ("a landing page FAILS even though it is reachable", "MP Materials", [LANDING], "FAIL"),
        ("an unreachable document FAILS with its error", "Samsung", [DEAD], "FAIL"),
        ("🔴 a reachable filing that does NOT name the company FAILS",
         "Groq", [FILING], "FAIL"),
        ("multi-URL row passes if ANY document names it (Samsung cites two)",
         "Nvidia", [DEAD, FILING], "OK"),
        ("multi-URL row FAILS when none of them name it",
         "Groq", [DEAD, LANDING], "FAIL"),
        ("a costed row with no filing_source is its own verdict, not a pass",
         "Anthropic", [], "NO-SOURCE"),
    ]
    failures = []
    for name, company, docs, want in cases:
        try:
            got = judge(company, docs)[0]
            ok = got == want
        except Exception as e:  # a control that fails via traceback is not a control
            ok, got, name = False, f"RAISED {type(e).__name__}: {e}", name
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(f"{name}: wanted {want}, got {got}")

    # The alias table must reach this file too: nothing files as "Amazon (AWS)".
    AMZN = ("https://www.sec.gov/Archives/edgar/data/1018724/x.htm",
            "Amazon Web Services net sales increased " * 60, None)
    ok = judge("Amazon (AWS)", [AMZN])[0] == "OK"
    print(f"  {'ok  ' if ok else 'DEAD'}  KEY aliases apply here: 'Amazon (AWS)' matches 'Amazon Web Services'")
    if not ok:
        failures.append("KEY aliases are not reaching judge()")

    # End-to-end: is verify() actually wired to judge()? A rule that is never invoked reports exactly
    # what a clean repo reports -- measured on check_data.py this session, where deleting the call left
    # its whole suite green.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        proj = pathlib.Path(td) / "01-fixture"
        (proj / "data").mkdir(parents=True)
        with open(proj / "data" / "companies.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["company", "revenue_usd_b", "filing_source"])
            w.writeheader()
            w.writerow({"company": "Fixture Corp", "revenue_usd_b": "1.0",
                        "filing_source": "https://example.invalid/x.htm"})
        pre = {"https://example.invalid/x.htm": (None, "seeded: not fetched")}
        res = verify(proj, pre)
        wired = len(res) == 1 and res[0][1] == "FAIL"
        print(f"  {'ok  ' if wired else 'DEAD'}  WIRING: verify() reads companies.csv and judges each costed row")
        if not wired:
            failures.append(f"verify() did not reach judge(); got {res}")

    print()
    if failures:
        print(f"SELFTEST FAILED, {len(failures)} case(s):")
        for f in failures:
            print(f"  - {f}")
        return 2
    print(f"SELFTEST PASSED. {len(cases) + 2} cases: a real filing passes, and an error page that names "
          f"the company does not.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
