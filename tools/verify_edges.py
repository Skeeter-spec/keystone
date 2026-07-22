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
    # Downstream buyer nodes, added 2026-07-16. Without these, `named()` falls back to the full CSV
    # name and a filing that simply says "Tesla" fails against the literal "Tesla Inc".
    "Tesla Inc": "Tesla",
    "Ford Motor Company": "Ford Motor|Ford",
    "Lucid Group": "Lucid",
    "LG Energy Solution": "LG Energy",
    "Samsung SDI": "Samsung SDI",
    "POSCO Future M": "POSCO Future|POSCO",
    # 04-ai-compute, added 2026-07-20. Ten of the map's first 42 edges failed verification purely
    # because THE ROSTER NAME IS OURS, NOT THE DOCUMENT'S. No filing on earth writes "Amazon (AWS)"
    # or "Foxconn (Hon Hai Precision)" -- those parentheticals are disambiguators this atlas added for
    # its own readers. Nvidia's 10-K says "Hon Hai Precision Industry Co., Ltd."; Vertiv's says
    # "Amazon Web Services". Without these entries the checker reports a clean, confident, and
    # completely wrong "document never names X" on a document that names X perfectly well.
    # Kept TIGHT on purpose: a false POSITIVE is this tool's worst failure mode, so each alternative
    # is a name the company actually trades under, never an abbreviation that could collide.
    "Amazon (AWS)": "Amazon|Amazon Web Services|AWS",
    "Alphabet (Google Cloud)": "Alphabet|Google",
    "Meta Platforms": "Meta Platforms|Meta",
    "Foxconn (Hon Hai Precision)": "Foxconn|Hon Hai",
    "Nebius Group": "Nebius",
    "Micron Technology": "Micron",
    "Marvell Technology": "Marvell",
    "Arista Networks": "Arista",
    "Astera Labs": "Astera",
    "Vertiv Holdings": "Vertiv",
    "Eaton Corporation": "Eaton",
    "Dell Technologies": "Dell",
    "Super Micro Computer": "Super Micro|Supermicro|SMCI",
    "Hewlett Packard Enterprise": "Hewlett Packard Enterprise|Hewlett-Packard Enterprise|HPE",
    "Samsung Electronics": "Samsung Electronics|Samsung",
    "TSMC": "TSMC|Taiwan Semiconductor",
    "SK hynix": "SK hynix|SK Hynix",
    "Siemens Energy": "Siemens Energy",
    "Schneider Electric": "Schneider Electric|Schneider",
    "Cerebras Systems": "Cerebras",
    # 01 spells some nodes differently from 04, and a name with a parenthetical never appears in a
    # filing. Found 2026-07-21 when Alphabet's own 10-K index "failed" to name Alphabet.
    "Alphabet (Google)": "Alphabet|Google",
    "Taiyo Yuden": "Taiyo Yuden|TAIYO YUDEN",
    # 🔴 A CHINESE-LANGUAGE FILING NEVER CONTAINS THE LATIN NAME. Yunnan Chihong's SSE annual report
    # is 203,790 chars and contains 云南驰宏 and 驰宏锌锗 -- and not one occurrence of "Chihong".
    # Every A-share citation this repo makes is unverifiable without the native-script name, so the
    # alias carries BOTH scripts. shared/SOURCING-ROUTES.md sends future bursts down these routes.
    "Yunnan Chihong Zinc & Germanium": "Chihong|驰宏锌锗|云南驰宏",
    "JL MAG Rare-Earth": "JL MAG|金力永磁",
    "China Northern Rare Earth (Group) High-Tech": "Northern Rare Earth|北方稀土",
    # 05-pharma, added 2026-07-21. Same failure as 04's, and it cost a wrong turn worth recording:
    # THIS REPO HAS TWO ALIAS TABLES AND NEITHER NAMES THE OTHER. shared/company_aliases.csv is read
    # by reuse_costed.py and check_identity.py; this KEY dict is read by named(), which is what
    # verify_sources.py and verify_edges.py actually match on. Seven 05 rows were "failing"
    # verification, the aliases were added to company_aliases.csv, and the count did not move at all,
    # because that file never reaches named(). Look at the consumer, not at the filename.
    # Five of the seven are this map's Parent (Arm) convention, which FOUNDATION.md uses to say WHY a
    # company is on a pharma map ("the PBM oligopoly, represented here by CVS Health (Caremark)").
    # No 10-K writes it. Kept TIGHT, per the 04 note: every alternative is a name the company
    # actually trades under.
    "Johnson & Johnson (Innovative Medicine)": "Johnson & Johnson|Johnson and Johnson",
    "CVS Health (Caremark)": "CVS Health|CVS Caremark|Caremark",
    # "Evernorth" added 2026-07-22, and it is an IDENTITY BINDING backed by two documents, not a guess.
    # Cencora's FY2025 10-K names its second-largest customer as "Evernorth Health Services" at ~13% of
    # revenue and NEVER says Cigna or Express Scripts (measured: 0 hits for either). Cigna's own FY2025
    # 10-K says, in prose, "We have two segments: Evernorth Health Services and Cigna Healthcare", and
    # tags it `ci:EvernorthMember` in its own XBRL -- so Evernorth is a name Cigna itself trades under,
    # which is exactly the bar the 04 note sets for this table. Without the alias the single strongest
    # cross-chokepoint edge on this map (a big-three distributor depending on a big-three PBM's parent)
    # is undrawable, and the two chokepoints render as unconnected when the filing connects them.
    "Cigna (Express Scripts)": "Cigna|Express Scripts|Evernorth",
    "UnitedHealth Group (OptumRx)": "UnitedHealth Group|UnitedHealth|OptumRx",
    "Cencora (formerly AmerisourceBergen)": "Cencora|AmerisourceBergen",
    # EDGAR prints the registrant without the apostrophe (DR REDDYS LABORATORIES LTD); the map keeps it.
    "Dr. Reddy's Laboratories": r"Dr\.? ?Reddy|REDDYS LABORATORIES|Reddy's Laboratories",
    # CJK, same rule as Yunnan Chihong: the SSE annual report is filed in Chinese and never prints the
    # Latin name. Both scripts carried, and the CJK alternative is matched as a plain substring
    # because \b can never fire between two Han characters.
    "Zhejiang Huahai Pharmaceutical": "Huahai|浙江华海药业|华海药业",
    # 05-pharma EDGE side, added 2026-07-22 before the relationships burst. The seven entries above
    # were added for verify_sources.py, which asks a WEAKER question: does this company's own filing
    # name this company? An EDGE needs its cited document to name BOTH endpoints, so every company
    # that can appear as a COUNTERPARTY needs its document-side name too, not just the ones whose own
    # citation was failing. Same root cause as 04's ten failures: the roster name is ours, not the
    # document's. Nothing files as "Teva Pharmaceutical Industries" in a sentence about a supplier.
    "McKesson Corporation": "McKesson",
    "Lonza Group": "Lonza",
    "Teva Pharmaceutical Industries": "Teva",
    "Roche Holding": "Roche Holding|Roche",
    "Eli Lilly": "Eli Lilly|Lilly",
    "Sun Pharmaceutical Industries": "Sun Pharmaceutical|Sun Pharma",
    "Aurobindo Pharma": "Aurobindo",
    # 🔴 NOT "SPL". In exactly the corpus this map reads, SPL is the FDA's own abbreviation for
    # Structured Product Labeling, so the alias that looks obvious would match FDA boilerplate on
    # documents that have never heard of this company. The whole point of the tool is to catch a row
    # citing a document that does not support it.
    "Scientific Protein Laboratories": "Scientific Protein",
    # CJK carried bare, same rule as Yunnan Chihong and Huahai above: \b cannot fire between Han
    # characters, so a wrapped CJK alternative silently never matches.
    "WuXi AppTec": "WuXi AppTec|药明康德",
    "WuXi Biologics": "WuXi Biologics|药明生物",
    # ⚠ "Merck & Co" gets NO bare "Merck" alias, deliberately. Merck KGaA is a different listed company
    # that trades as "Merck" across Europe and as EMD in the US, and this map's Merck is the US one.
    # A bare alias would verify a Merck & Co edge against a document about a company on another
    # continent -- the NEO -> NEOGENOMICS failure with better camouflage.
    "Merck & Co": "Merck & Co|Merck Sharp|MSD",
}

# NOTE: use .search(), never .match(). match() anchors at position 0, so the mid-URL alternatives
# (/investors/, /news/) could never fire and every landing page would sail through as clean. The
# selftest caught exactly that, which is the entire reason the selftest has a landing-page fixture.
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

LANDING_SMELL = re.compile(r"^https?://[^/]+/?$|/investors/?$|/news/?$|/search|\?q=", re.I)


# A corporate newsroom is not a filing portal and does not want a robot. Measured 2026-07-20: three
# 04 edges came back UNREACHABLE (connection reset, 403) against the project UA, and two of them
# returned HTTP 200 immediately under a browser UA -- real documents, 162KB and 98KB, refusing the
# label rather than the request. UNREACHABLE is a dangerous verdict to get wrong in EITHER direction:
# treat it as "citation is bad" and you delete a sound edge; wave it through and you keep an unchecked
# one. So the fetch retries once with a browser UA before anything is called unreachable.
# The project UA stays FIRST because SEC asks automated clients to identify themselves, and SEC in
# fact 403s the browser UA -- the two hosts want opposite things, which is exactly why both are tried.
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def fetch(url):
    last = None
    for ua in (UA, BROWSER_UA):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), r.getcode(), r.headers.get("Content-Type", "")
        except Exception as e:  # noqa: BLE001 -- any transport failure is worth one retry
            last = e
    raise last


# 🔴 AN ERROR PAGE CAN SATISFY A BOTH-NAMES CHECK. Measured 2026-07-20 on the one edge that stayed
# unreachable: marvell.com returns an Akamai "Access Denied" body that ECHOES THE REQUESTED URL, and
# that URL contains the slug "marvell-expands-strategic-collaboration-aws". So the 525-byte refusal
# names both "Marvell" and "AWS" and would verify CLEAN as the document it is denying access to.
# This tool is safe today only because a 403 raises before the body is read -- which means the
# protection is an accident of control flow, not a decision. Made explicit: a body too short to be a
# filing, or one that reads like an error page, is never evidence of anything.
ERROR_SMELL = re.compile(r"access denied|forbidden|are you a robot|enable javascript|"
                         r"request blocked|errors\.edgesuite\.net|cloudflare", re.I)
# 500, not 2000. Measured 2026-07-21: an EDGAR filing-index page is a LEGITIMATE 1,670-char document,
# and the 2000 floor rejected Oracle's citation as a block page. The Akamai refusal this guard exists
# for is caught by ERROR_SMELL, not by length, so the floor only has to exclude a fragment.
MIN_DOC_BYTES = 500


def looks_like_error_page(text):
    return len(text) < MIN_DOC_BYTES or bool(ERROR_SMELL.search(text[:4000]))


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
    """Is this company NAMED in the document? Word-bounded, and that is not a detail.

    🔴 A BARE SUBSTRING MATCH SILENTLY INVENTS EVIDENCE. Found 2026-07-16 by a research worker, not by
    me: it reported Ford as a Syrah counterparty off a case-insensitive hit on **"Abbotsford"**, the
    suburb in the share registry's postal address. My own checker had the same class of bug and I had
    already reported "14/14 verified" on it: `named("Vale S.A.", "cobalt is prevalent")` returned True,
    because "prevalent" contains "vale". A false POSITIVE here is the worst possible failure for this
    tool, because its entire job is to catch rows citing a document that does not support them.
    \b fixes both: "Abbotsford" has no word boundary before "ford", and "prevalent" none before "vale".
    """
    pat = KEY.get(company, re.escape(company))
    # 🔴 CJK HAS NO WORD BOUNDARIES. \b is defined against \w, and every character around a Chinese
    # company name is also a word character: in 云南驰宏锌锗股份有限公司 there is no boundary before
    # 驰 or after 锗, so \b驰宏锌锗\b can never match and a correct alias silently never fires.
    # Measured 2026-07-21. So each alternative is wrapped only if it is Latin script; a CJK
    # alternative is matched as a plain substring, which is safe here because the false positives \b
    # exists to stop ("Abbotsford" containing "ford", "prevalent" containing "vale") are artefacts of
    # alphabetic writing and have no CJK equivalent at these lengths.
    parts = []
    for alt in pat.split("|"):
        parts.append(alt if CJK_RE.search(alt) else rf"\b(?:{alt})\b")
    return re.search("|".join(parts), text, re.I) is not None


def verify(project):
    root = pathlib.Path(project)
    staged = sorted(glob.glob(str(root / "data" / "_incoming" / "edges_*.csv")))
    if not staged:
        print(f"no staged edge files in {root}/data/_incoming/")
        # SCOPE FOOTER. This tool verifies edges AT STAGING TIME only. Once merge_edges.py folds a
        # staged edge into relationships.csv, NOTHING re-reads it: this tool never looks there, and
        # it writes no _verified.json, so unlike figures there is no record of when, or whether, a
        # merged edge was ever checked against its document. On a finished map that makes the line
        # above mean "there was nothing here to look at", NOT "the edges are fine".
        print("\n  SCOPE: this checked ZERO edges. It reads data/_incoming/edges_*.csv only.")
        print("    NOT read:   relationships.csv, i.e. every edge already merged into the map.")
        print("    NOT stored: no _verified.json is written for edges, so there is no record of")
        print("                when any merged edge was last checked. Figures have that trail;")
        print("                edges do not. Re-checking a merged edge has no tool today.")
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
        if looks_like_error_page(text):
            verdicts.append(("UNREACHABLE", edge, url,
                             f"served a block/error page, not a document ({len(text)} chars). "
                             f"An error page that echoes the URL can name both endpoints"))
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

    # 🔴 REAL CASES, both of which actually happened on 2026-07-16. Keep them forever. A fixture
    # invented next to the code only proves you can restate your own regex; these two are the shapes
    # that really shipped, one of them in MY tool while I reported it green.
    substring_traps = [
        ("the worker's REAL case: 'Ford' must NOT match 'Abbotsford' (a suburb in a postal address)",
         "Ford Motor Company", "Share registry: Computershare, Abbotsford, Victoria 3067", False),
        ("MY OWN bug: 'Vale' must NOT match 'prevalent'",
         "Vale S.A.", "cobalt is prevalent in the DRC", False),
        ("...nor 'equivalent'", "Vale S.A.", "the equivalent tonnage was shipped", False),
        ("but a real mention of Vale still counts", "Vale S.A.", "Vale S.A. operates in Indonesia", True),
        ("and a real Ford mention still counts", "Ford Motor Company", "an MoU with Ford Motor Company", True),
        ("a filing saying just 'Tesla' matches the node 'Tesla Inc'", "Tesla Inc", "offtake with Tesla", True),
        # 04's roster names carry parenthetical disambiguators no filing uses. These must match the
        # real trading names, and must NOT match the near-collisions those short forms invite.
        ("'Amazon (AWS)' matches a filing that says 'Amazon Web Services'",
         "Amazon (AWS)", "customers include Amazon Web Services and others", True),
        ("'Foxconn (Hon Hai Precision)' matches the full legal name in Nvidia's 10-K",
         "Foxconn (Hon Hai Precision)", "Hon Hai Precision Industry Co., Ltd. assembles", True),
        ("'Meta Platforms' matches a filing that says just 'Meta'",
         "Meta Platforms", "sales to Meta increased", True),
        ("🔴 'Meta Platforms' must NOT match 'metadata'",
         "Meta Platforms", "the metadata was incomplete", False),
        ("🔴 'Meta Platforms' must NOT match 'metallurgical'",
         "Meta Platforms", "metallurgical coal prices rose", False),
        ("🔴 'Intel' must NOT match 'intelligence'",
         "Intel", "artificial intelligence workloads", False),
        ("🔴 'Dell Technologies' must NOT match 'Dellinger'",
         "Dell Technologies", "signed by A. Dellinger, counsel", False),
        ("🔴 'Eaton Corporation' must NOT match 'Eatonville'",
         "Eaton Corporation", "the Eatonville facility", False),
        ("🔴 'Arista Networks' must NOT match 'Aristarchus'",
         "Arista Networks", "Aristarchus Capital holds a stake", False),
        ("'TSMC' matches a filing that spells out Taiwan Semiconductor",
         "TSMC", "Taiwan Semiconductor Manufacturing Company fabricates", True),
        # 🔴 A Chinese-language filing never contains the Latin name. Yunnan Chihong's 203,790-char
        # SSE annual report has 云南驰宏 and 驰宏锌锗 and ZERO occurrences of "Chihong".
        ("🔴 a CJK filing matches on the native-script name",
         "Yunnan Chihong Zinc & Germanium", "云南驰宏锌锗股份有限公司 2025 年年度报告", True),
        ("🔴 ...and the Latin name alone still matches an English document",
         "Yunnan Chihong Zinc & Germanium", "Chihong Zinc reported output", True),
        ("NEGATIVE: an unrelated CJK document must NOT match",
         "Yunnan Chihong Zinc & Germanium", "宁德时代新能源科技股份有限公司", False),
    ]
    # 🔴 THE REAL AKAMAI BODY from 2026-07-20, verbatim. It names both endpoints and is not a document.
    denied = ('Access Denied Access Denied You don\'t have permission to access '
              '"http://www.marvell.com/company/newsroom/marvell-expands-strategic-collaboration-aws-'
              'enable-accelerated-infrastructure-ai-cloud.html" on this server. '
              'Reference #18.ab0c2e17 https://errors.edgesuite.net/18.ab0c2e17')
    page_traps = [
        ("🔴 the REAL Akamai 403 body names both endpoints via the echoed URL", denied, True),
        ("🔴 ...and it would otherwise pass named() for BOTH companies",
         denied, True),  # asserted explicitly below
        ("a short but legitimate snippet is still rejected as too short to be a filing",
         "Nvidia buys HBM from SK hynix.", True),
        ("a real document body is NOT flagged as an error page",
         "Nvidia " + ("audited consolidated financial statements and notes thereto. " * 80), False),
    ]
    for name, body, want in page_traps:
        got = looks_like_error_page(body)
        ok = got == want
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(name)
    # The trap only matters BECAUSE named() is satisfied by it. Assert that, or the case above is
    # just testing a string length and proves nothing about the danger it claims to guard.
    both = named(denied, "Marvell Technology") and named(denied, "Amazon (AWS)")
    print(f"  {'ok  ' if both else 'DEAD'}  🔴 confirms the danger is real: named() DOES match both on the 403 body")
    if not both:
        failures.append("the error-page fixture no longer demonstrates the false positive")
    for name, comp, doc2, want in substring_traps:
        got = named(doc2, comp)
        ok = got == want
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
    # +1 for the standalone named()-on-the-403-body assertion, which is not in any list.
    print(f"SELFTEST PASSED. {len(cases) + len(substring_traps) + len(smells) + len(page_traps) + 1} cases.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(verify(sys.argv[1]))
