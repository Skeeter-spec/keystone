#!/usr/bin/env python3
"""Check every map's CSVs against what the README promises about them.

    python3 tools/check_data.py            check the real data
    python3 tools/check_data.py --selftest prove these checks actually fire

THE SPLIT THAT MAKES THIS GATE SURVIVABLE. Incomplete does NOT fail. Incorrect does.

Nine of the ten maps are foundation briefs on purpose: seed companies with no financials, no edges,
no source tiers. Those are questions, not answers, and a gate that failed them would fail on ~everything
the day it shipped. A check that fails on everything gets bypassed, and a bypassed gate is worse than no
gate, because the repo still looks checked. So: a BLANK financial is fine forever. A financial figure with
no source behind it is not, because that is the one thing the README swears never happens.

The rules, each tied to the promise or the mechanism it protects:

  1. sourcing    A row carrying any financial figure carries a source_tier and a filing_source.
                 This is the README's "Sourced or it does not exist", asserted instead of hoped.
  2. tiers       source_tier is 1, 2 or 3. An unknown tier is an unranked claim.
  3. chokepoint  The value is exactly 'yes' or 'no'. NOT cosmetic: the artifact template tests
                 c.chokepoint==='yes', so a row saying 'TRUE' is not a chokepoint as far as the built
                 page is concerned. Six of the nine foundations shipped 'TRUE' from their research
                 agents. Build one of those maps with the 01 template and it renders "0 chokepoints
                 flagged" while the CSV plainly lists seven, and nothing errors. This rule exists
                 because that failure is SILENT, and a silent wrong number is the dangerous kind.
  4. edges       A relationship with a description carries evidence and a tier. The README calls the
                 edges the whole payoff; an unsourced edge is a rumour.
  5. timeseries  Every financial-history row carries its own source_url and tier.
  6. readme      The status table matches the data. "Mapped" must have edges; "Foundation only" must
                 not. A status typed in prose is a COPY of the truth, and copies rot.
  7. prose       Nothing an agent READS teaches it to write TRUE/FALSE for chokepoint. This rule gates
                 the GENERATOR, not the output. The TRUE/FALSE drift was not agent sloppiness:
                 projects/_kit/AGENT-RUNBOOK.md literally SAID "set chokepoint TRUE", shared/new-map.sh
                 copied the kit into all nine maps, and each research agent did as it was told. Fixing
                 the 163 rows without fixing the instruction would just have rebuilt the bug on the next
                 foundation burst. Rule 3 catches the symptom; this catches the cause.

                 WIDENED 2026-07-20, because the first version only looked at AGENT-RUNBOOK.md and the
                 vocabulary had survived everywhere else. The 2026-07-16 sweep normalised the chokepoint
                 COLUMN in 163 rows and left the PROSE alone, so six files still said TRUE/FALSE --
                 including 04's own FOUNDATION.md ("Six nodes are flagged chokepoint=TRUE in
                 data/companies.csv", which by then was false as well as banned) and two companies.csv
                 notes. A burst agent reads the foundation brief for context and the neighbouring rows
                 for style; both teach vocabulary just as effectively as the runbook does. So this rule
                 now covers AGENT-RUNBOOK.md, FOUNDATION.md, and the notes column of companies.csv.

Exit 0 = clean. Exit 1 = a real problem. Exit 2 = the checker itself is broken.
"""
import csv, glob, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent.parent
FINANCIAL_COLS = ("revenue_usd_b", "net_income_usd_b", "market_cap_usd_b",
                  "rd_spend_usd_b", "capex_usd_b")
VALID_TIERS = {"1", "2", "3"}
VALID_CHOKE = {"yes", "no"}


def g(row, key):
    return (row.get(key) or "").strip()


def has_financials(row):
    return any(g(row, c) for c in FINANCIAL_COLS)


def check_companies(rows, label):
    """Rules 1, 2, 3."""
    problems = []
    for i, r in enumerate(rows, start=2):  # header is line 1
        name = g(r, "company") or f"row {i}"
        if has_financials(r):
            if not g(r, "source_tier"):
                problems.append(f"{label}:{i} {name} carries a financial figure with no source_tier")
            if not g(r, "filing_source"):
                problems.append(f"{label}:{i} {name} carries a financial figure with no filing_source")
        tier = g(r, "source_tier")
        if tier and tier not in VALID_TIERS:
            problems.append(f"{label}:{i} {name} has source_tier {tier!r}, expected one of 1, 2, 3")
        choke = g(r, "chokepoint")
        if choke and choke not in VALID_CHOKE:
            problems.append(
                f"{label}:{i} {name} has chokepoint {choke!r}, expected 'yes' or 'no'. "
                f"The template tests chokepoint==='yes', so this row would render as NOT a chokepoint")
    return problems


def check_relationships(rows, label):
    """Rule 4."""
    problems = []
    for i, r in enumerate(rows, start=2):
        if not g(r, "description"):
            continue  # a bare seed edge with no claim yet is incomplete, not wrong
        edge = f"{g(r, 'from_company')} -> {g(r, 'to_company')}"
        if not g(r, "evidence_source"):
            problems.append(f"{label}:{i} edge {edge} makes a claim with no evidence_source")
        tier = g(r, "source_tier")
        if not tier:
            problems.append(f"{label}:{i} edge {edge} makes a claim with no source_tier")
        elif tier not in VALID_TIERS:
            problems.append(f"{label}:{i} edge {edge} has source_tier {tier!r}, expected 1, 2 or 3")
    return problems


def check_timeseries(rows, label):
    """Rule 5."""
    problems = []
    for i, r in enumerate(rows, start=2):
        who = f"{g(r, 'company')} FY{g(r, 'fiscal_year')}"
        if not has_financials(r):
            continue
        if not g(r, "source_url"):
            problems.append(f"{label}:{i} {who} has financials with no source_url")
        tier = g(r, "source_tier")
        if not tier:
            problems.append(f"{label}:{i} {who} has financials with no source_tier")
        elif tier not in VALID_TIERS:
            problems.append(f"{label}:{i} {who} has source_tier {tier!r}, expected 1, 2 or 3")
    return problems


def check_readme(readme_text, facts):
    """Rule 6. facts: {project_dir: {'edges': n, 'costed': n}}"""
    problems = []
    for slug, f in sorted(facts.items()):
        num = slug.split("-")[0]
        row = re.search(rf"^\|\s*{re.escape(num)}\s*\|(.+)$", readme_text, re.M)
        if not row:
            problems.append(f"README has no status row for project {slug}")
            continue
        status = row.group(1)
        # Three states, because a map earns them in order: no edges -> edges -> edges AND financials.
        # "Edges started" exists because 02 reached a state the first version of this rule could not
        # express, and the honest fix is a new label, not a looser check.
        mapped = "Mapped" in status
        foundation = "Foundation only" in status
        edges_started = "Edges started" in status
        if not (mapped or foundation or edges_started):
            problems.append(f"README row {num} has an unrecognised status, expected 'Mapped', 'Edges started' or 'Foundation only'")
        if mapped and f["edges"] == 0:
            problems.append(f"README calls {slug} 'Mapped' but it has 0 relationship edges")
        if mapped and f["costed"] == 0:
            problems.append(f"README calls {slug} 'Mapped' but not one company is costed")
        if foundation and f["edges"] > 0:
            problems.append(f"README calls {slug} 'Foundation only' but it has {f['edges']} edges, so it has outgrown the label")
        if edges_started and f["edges"] == 0:
            problems.append(f"README calls {slug} 'Edges started' but it has 0 relationship edges")
    return problems


CHOKE_PROSE_RE = re.compile(r"chokepoint[ =]*(TRUE|FALSE)", re.I)


def check_runbook(text, label):
    """Rule 7. The instruction that produced the drift, not the drift."""
    problems = []
    if CHOKE_PROSE_RE.search(text):
        problems.append(
            f"{label} tells research agents to write TRUE/FALSE for chokepoint. The template tests "
            f"chokepoint==='yes', so this instruction regenerates the silent-zero bug on the next burst")
    return problems


def check_notes_prose(rows, label):
    """Rule 7, in the notes column. A neighbouring row teaches vocabulary too."""
    problems = []
    for i, r in enumerate(rows, start=2):
        if CHOKE_PROSE_RE.search(g(r, "notes")):
            problems.append(
                f"{label}:{i} {g(r, 'company')} has TRUE/FALSE chokepoint vocabulary in its notes. The "
                f"column is right, but the next agent reads these rows for style and copies the words")
    return problems


def load(path):
    if not path.exists():
        return []
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def run(root):
    problems, facts = [], {}
    for data_dir in sorted(glob.glob(str(root / "projects" / "*" / "data"))):
        d = pathlib.Path(data_dir)
        slug = d.parent.name
        if slug == "_kit":
            continue  # the template project, deliberately empty
        companies = load(d / "companies.csv")
        rels = load(d / "relationships.csv")
        ts = load(d / "financials_timeseries.csv")
        problems += check_companies(companies, f"{slug}/companies.csv")
        problems += check_notes_prose(companies, f"{slug}/companies.csv")
        problems += check_relationships(rels, f"{slug}/relationships.csv")
        problems += check_timeseries(ts, f"{slug}/financials_timeseries.csv")
        facts[slug] = {"edges": len(rels), "costed": sum(1 for c in companies if has_financials(c))}
    # Rule 7 covers _kit too: it is the template every future map is stamped from, so it is the
    # one file where a wrong instruction costs the most. FOUNDATION.md is in scope because a burst
    # agent is handed the foundation brief as context, so it teaches vocabulary the same way.
    for pattern in ("AGENT-RUNBOOK.md", "FOUNDATION.md"):
        for rb in sorted(glob.glob(str(root / "projects" / "*" / pattern))):
            p = pathlib.Path(rb)
            problems += check_runbook(p.read_text(), f"{p.parent.name}/{pattern}")
    readme = (root / "README.md")
    if readme.exists():
        problems += check_readme(readme.read_text(), facts)
    return problems, facts


# ---------------------------------------------------------------------------
# selftest: break known-good data on purpose and prove each rule fires.
# A rule that stays silent on its own mutant is dead code, and a green from a
# dead check is indistinguishable from a green from a real one.
# ---------------------------------------------------------------------------
def selftest():
    good_company = {
        "company": "Fixture Corp", "revenue_usd_b": "10.0", "filing_source": "https://example.com/10-K",
        "source_tier": "1", "chokepoint": "yes",
    }
    good_edge = {
        "from_company": "A", "to_company": "B", "description": "A fabricates for B",
        "evidence_source": "https://example.com/src", "source_tier": "2",
    }
    good_ts = {
        "company": "Fixture Corp", "fiscal_year": "2025", "revenue_usd_b": "10.0",
        "source_url": "https://example.com/ar", "source_tier": "1",
    }
    cases = [
        # (name, fn, rows, expect_fire)
        ("control: clean company passes", check_companies, [dict(good_company)], False),
        ("control: clean edge passes", check_relationships, [dict(good_edge)], False),
        ("control: clean timeseries passes", check_timeseries, [dict(good_ts)], False),
        ("incomplete company (no financials at all) must NOT fire",
         check_companies, [{"company": "Seed Co", "chokepoint": "no"}], False),
        ("incomplete edge (no description) must NOT fire",
         check_relationships, [{"from_company": "A", "to_company": "B"}], False),
        ("rule 1: financial with no source_tier",
         check_companies, [{**good_company, "source_tier": ""}], True),
        ("rule 1: financial with no filing_source",
         check_companies, [{**good_company, "filing_source": ""}], True),
        ("rule 2: bogus tier",
         check_companies, [{**good_company, "source_tier": "9"}], True),
        ("rule 3: chokepoint TRUE (the real drift that renders as 0 chokepoints)",
         check_companies, [{**good_company, "chokepoint": "TRUE"}], True),
        ("rule 3: chokepoint FALSE",
         check_companies, [{**good_company, "chokepoint": "FALSE"}], True),
        ("rule 4: claimed edge with no evidence",
         check_relationships, [{**good_edge, "evidence_source": ""}], True),
        ("rule 4: claimed edge with no tier",
         check_relationships, [{**good_edge, "source_tier": ""}], True),
        ("rule 5: timeseries with no source_url",
         check_timeseries, [{**good_ts, "source_url": ""}], True),
        # Rule 7 in the notes column. The CONTROL is the real 2026-07-20 case: the row's chokepoint
        # value was already correct ('no'), so rule 3 was silent and only this catches the prose.
        ("rule 7: TRUE/FALSE vocabulary in a note whose column is already correct (the real case)",
         check_notes_prose,
         [{"company": "Alphabet", "chokepoint": "no",
           "notes": "routable-around at the cloud layer, so chokepoint=FALSE"}], True),
        ("rule 7: the 09-aerospace phrasing with a space",
         check_notes_prose,
         [{"company": "Spirit AeroSystems", "chokepoint": "no",
           "notes": "Not separately flagged chokepoint = TRUE because the bottleneck moved"}], True),
        ("NEGATIVE: a note that discusses chokepoints in the right vocabulary must NOT fire",
         check_notes_prose,
         [{"company": "Nvidia", "chokepoint": "yes",
           "notes": "Flagged chokepoint=yes; CUDA lock-in makes switching costly. TRUE sole source."}], False),
        ("NEGATIVE: a row with no notes at all must NOT fire",
         check_notes_prose, [{"company": "Groq", "chokepoint": "no"}], False),
    ]
    failures = []
    for name, fn, rows, expect_fire in cases:
        fired = bool(fn(rows, "selftest"))
        ok = fired == expect_fire
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(f"{name}: expected {'a finding' if expect_fire else 'silence'}, got {'a finding' if fired else 'silence'}")

    # Rule 6 needs a README fixture rather than rows.
    readme_cases = [
        ("control: honest table passes",
         "| 01 | x | Mapped. |\n| 02 | y | Foundation only |",
         {"01-a": {"edges": 48, "costed": 41}, "02-b": {"edges": 0, "costed": 0}}, False),
        ("rule 6: 'Mapped' with no edges",
         "| 01 | x | Mapped. |", {"01-a": {"edges": 0, "costed": 0}}, True),
        ("rule 6: 'Foundation only' that has grown edges",
         "| 02 | y | Foundation only |", {"02-b": {"edges": 12, "costed": 0}}, True),
        ("rule 6: missing row",
         "| 01 | x | Mapped. |", {"07-z": {"edges": 0, "costed": 0}}, True),
        ("control: 'Edges started' with edges but no financials passes",
         "| 02 | y | Edges started |", {"02-b": {"edges": 14, "costed": 0}}, False),
        ("rule 6: 'Edges started' with no edges",
         "| 02 | y | Edges started |", {"02-b": {"edges": 0, "costed": 0}}, True),
        ("rule 6: 'Mapped' with edges but nothing costed",
         "| 01 | x | Mapped. |", {"01-a": {"edges": 48, "costed": 0}}, True),
        ("rule 6: an invented status label",
         "| 02 | y | Mostly done |", {"02-b": {"edges": 3, "costed": 0}}, True),
    ]
    runbook_cases = [
        ("control: runbook saying yes/no passes",
         "set chokepoint yes for suspected chokepoints", False),
        ("rule 7: the exact kit text that caused the drift",
         "financials blank; set chokepoint TRUE\n  for suspected chokepoints", True),
        ("rule 7: the discipline heading variant",
         "## Chokepoint discipline (applies whenever chokepoint=TRUE is set)", True),
    ]
    for name, text, expect_fire in runbook_cases:
        fired = bool(check_runbook(text, "selftest"))
        ok = fired == expect_fire
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(f"{name}: expected {'a finding' if expect_fire else 'silence'}, got {'a finding' if fired else 'silence'}")

    for name, text, facts, expect_fire in readme_cases:
        fired = bool(check_readme(text, facts))
        ok = fired == expect_fire
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(f"{name}: expected {'a finding' if expect_fire else 'silence'}, got {'a finding' if fired else 'silence'}")

    print()
    if failures:
        print(f"SELFTEST FAILED, {len(failures)} check(s) do not do what they claim:")
        for f in failures:
            print(f"  - {f}")
        return 2
    print(f"SELFTEST PASSED. {len(cases) + len(readme_cases) + len(runbook_cases)} cases: every rule fires on its own mutant "
          f"and stays silent on clean and on merely-incomplete data.")
    return 0


def main():
    if "--selftest" in sys.argv:
        print("SELFTEST: does each check actually fire when the data is broken on purpose?")
        return selftest()
    problems, facts = run(ROOT)
    total_edges = sum(f["edges"] for f in facts.values())
    total_costed = sum(f["costed"] for f in facts.values())
    print(f"  {len(facts)} maps, {total_costed} costed companies, {total_edges} sourced edges")
    if problems:
        print(f"  {len(problems)} problem(s):")
        for p in problems:
            print(f"    - {p}")
        return 1
    print("  data clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
