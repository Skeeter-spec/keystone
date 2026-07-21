#!/usr/bin/env python3
"""Copy an already-sourced company's figures from one map into another, without retyping them.

    python3 tools/reuse_costed.py projects/01-semiconductor projects/04-ai-compute
    python3 tools/reuse_costed.py projects/01-semiconductor projects/04-ai-compute --apply
    python3 tools/reuse_costed.py --selftest

WHY THIS EXISTS. The atlas shares nodes on purpose. 04-ai-compute's own FOUNDATION.md says its overlap
with 01-semiconductor is deliberate -- "literally the same company viewed through a different lens" --
and twelve of its thirty companies are already costed in 01 from primary filings at tier 1, including
five of its six chokepoints. Retyping those figures by hand is the transcription step that has produced
every wrong number in this repo's history. So it gets mechanized, and the copy carries its provenance
(fiscal_year, filing_source, source_tier, last_updated) with it, because a figure without its source is
the one thing the README swears never ships.

WHY NAME MATCHING IS NOT ALLOWED TO BE CLEVER. While planning this, a throwaway substring matcher run
over the real CSVs confidently matched **Samsung SDI -> Samsung Electronics** and would have written
Samsung Electronics' $234.62B revenue onto Samsung SDI's row. Two different listed companies. That is
tools/check_identity.py's NEO -> NEOGENOMICS failure wearing a different hat: an identifier that resolves
is not the entity you meant.

So identity here is exact-string, or it is DATA approved once by a human in shared/company_aliases.csv.
There is no fuzzy path, no normalisation, no prefix rule -- the same decision check_identity.py made
after a normalised-name match cried wolf on four correct rows (AMD, TSMC, UMC, GM).

WHAT IT WILL NOT DO
  - overwrite a cell that already has a value (a costed row is never silently restated)
  - copy a row that carries no financials (nothing to reuse)
  - guess at a name it has not been told about (it prints the near-misses and refuses)

Exit 0 = clean (with --apply, the write succeeded). Exit 1 = nothing to do or a refusal. Exit 2 = broken.
"""
import argparse, csv, pathlib, sys

ROOT = pathlib.Path(__file__).parent.parent
ALIASES = ROOT / "shared" / "company_aliases.csv"

# The figures themselves.
FINANCIAL_COLS = ("revenue_usd_b", "net_income_usd_b", "market_cap_usd_b",
                  "rd_spend_usd_b", "capex_usd_b")
# The provenance that must travel with them, or the copy becomes an unsourced claim.
PROVENANCE_COLS = ("fiscal_year", "filing_source", "source_tier", "last_updated")


def g(row, key):
    return (row.get(key) or "").strip()


def has_financials(row):
    return any(g(row, c) for c in FINANCIAL_COLS)


def load_aliases(rows):
    """{name: {other names approved as the same legal entity}}. Symmetric."""
    out = {}
    for r in rows:
        if (r.get("approved") or "").strip().lower() != "yes":
            continue
        a, b = (r.get("name_a") or "").strip(), (r.get("name_b") or "").strip()
        if not a or not b:
            continue
        out.setdefault(a, set()).add(b)
        out.setdefault(b, set()).add(a)
    return out


def plan(src_rows, dst_rows, aliases):
    """Decide, for every destination row, whether a source row may fill it.

    Returns (copies, skipped) where copies is [(dst_name, src_name, {col: value})] and
    skipped is [(dst_name, reason)]. Pure: no I/O, so the selftest can drive it directly.
    """
    by_name = {g(r, "company"): r for r in src_rows if has_financials(r)}
    copies, skipped = [], []
    for d in dst_rows:
        name = g(d, "company")
        if has_financials(d):
            skipped.append((name, "already costed here; a copy never overwrites a figure"))
            continue
        src = by_name.get(name)
        matched_as = name
        if src is None:
            for other in sorted(aliases.get(name, ())):
                if other in by_name:
                    src, matched_as = by_name[other], other
                    break
        if src is None:
            skipped.append((name, "not costed in the source map, and no approved alias is"))
            continue
        vals = {c: g(src, c) for c in FINANCIAL_COLS + PROVENANCE_COLS if g(src, c)}
        # Underscore keys are metadata for the trail, never written as columns.
        vals["_src_notes"] = g(src, "notes")
        copies.append((name, matched_as, vals))
    return copies, skipped


def apply_copies(dst_rows, copies, src_label):
    """Write the values in, and leave a trail in notes saying where they came from.

    The source row's own note travels VERBATIM, because that is where the figure-level caveats live --
    TSMC's filed NT$ conversion rate, Samsung's attributable-to-parent line, Intel's capex being gross
    additions rather than cash-flow capex. shared/SOURCING-ROUTES.md requires those to be said in the
    row, so a copy that dropped them would turn a carefully qualified number into a bare one. It is
    carried, not retyped, and attributed so a reader can tell whose sentence it is.
    """
    by_name = {g(r, "company"): r for r in dst_rows}
    for dst_name, src_name, vals in copies:
        row = by_name[dst_name]
        for col, val in vals.items():
            if col.startswith("_"):
                continue
            row[col] = val
        via = "" if src_name == dst_name else f" (as {src_name!r} there)"
        trail = f"Figures reused from {src_label}{via}, same filing, not re-derived."
        carried = vals.get("_src_notes", "")
        if carried:
            trail += f" Carried from that row: {carried}"
        old = g(row, "notes")
        row["notes"] = f"{trail} {old}".strip()
    return dst_rows


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def read_csv(path):
    with open(path, newline="") as fh:
        r = csv.DictReader(fh)
        return r.fieldnames, list(r)


def run(src_dir, dst_dir, do_apply):
    src_path = pathlib.Path(src_dir) / "data" / "companies.csv"
    dst_path = pathlib.Path(dst_dir) / "data" / "companies.csv"
    for p in (src_path, dst_path, ALIASES):
        if not p.exists():
            print(f"  missing {p}")
            return 2
    _, src_rows = read_csv(src_path)
    dst_fields, dst_rows = read_csv(dst_path)
    with open(ALIASES, newline="") as fh:
        aliases = load_aliases(list(csv.DictReader(fh)))

    copies, skipped = plan(src_rows, dst_rows, aliases)
    src_label = pathlib.Path(src_dir).name

    print(f"  {len(copies)} row(s) can be filled from {src_label}:")
    for dst_name, src_name, vals in copies:
        via = "" if src_name == dst_name else f"  <- {src_name!r}"
        print(f"    {dst_name}{via}")
        print(f"      rev={vals.get('revenue_usd_b', '-')}  ni={vals.get('net_income_usd_b', '-')}  "
              f"tier={vals.get('source_tier', '-')}  {vals.get('fiscal_year', '-')}")
    print(f"\n  {len(skipped)} row(s) left alone:")
    for name, why in skipped:
        print(f"    {name}: {why}")

    if not copies:
        print("\n  nothing to do")
        return 1
    if not do_apply:
        print("\n  dry run. Re-run with --apply to write.")
        return 0

    # Re-read immediately before writing: another session may have touched the file since the plan.
    fresh_fields, fresh_rows = read_csv(dst_path)
    if fresh_fields != dst_fields or len(fresh_rows) != len(dst_rows):
        print("\n  REFUSING: the destination changed while this ran. Re-run and re-read the plan.")
        return 1
    copies2, _ = plan(src_rows, fresh_rows, aliases)
    if [(a, b) for a, b, _ in copies2] != [(a, b) for a, b, _ in copies]:
        print("\n  REFUSING: the destination changed while this ran. Re-run and re-read the plan.")
        return 1
    write_csv(dst_path, fresh_fields, apply_copies(fresh_rows, copies2, src_label))
    print(f"\n  wrote {len(copies2)} row(s) to {dst_path}")
    return 0


# ---------------------------------------------------------------------------
# selftest. BOTH polarities, on purpose.
#
# A matcher that matches NOTHING passes every positive control by failing everything, so the positive
# cases alone cannot tell a working tool from a dead one. The negatives are what catch that, and the
# sharpest negative is the real pair this tool exists because of: Samsung SDI must not become Samsung.
# ---------------------------------------------------------------------------
def selftest():
    SRC = [
        {"company": "Samsung Electronics", "revenue_usd_b": "234.62", "net_income_usd_b": "31.13",
         "fiscal_year": "FY2025", "filing_source": "https://example.com/samsung", "source_tier": "1",
         "last_updated": "2026-07-13", "notes": "attributable to owners of parent"},
        {"company": "Nvidia", "revenue_usd_b": "215.94", "fiscal_year": "FY2026",
         "filing_source": "https://example.com/nvda", "source_tier": "1", "last_updated": "2026-07-13"},
        {"company": "Groq", "notes": "private, never costed"},
    ]
    ALIAS_ROWS = [{"name_a": "Samsung", "name_b": "Samsung Electronics", "approved": "yes"},
                  {"name_a": "Nvidia", "name_b": "NVIDIA Corp", "approved": "no"}]
    aliases = load_aliases(ALIAS_ROWS)

    def names(dst):
        return sorted(n for n, _, _ in plan(SRC, dst, aliases)[0])

    cases = [
        ("POSITIVE: an exact name copies",
         [{"company": "Nvidia"}], ["Nvidia"]),
        ("POSITIVE: an approved alias copies (Samsung -> Samsung Electronics)",
         [{"company": "Samsung"}], ["Samsung"]),
        ("🔴 NEGATIVE (the real 2026-07-20 near miss): Samsung SDI must NOT take Samsung Electronics",
         [{"company": "Samsung SDI"}], []),
        ("NEGATIVE: an UNAPPROVED alias row must not be honoured",
         [{"company": "NVIDIA Corp"}], []),
        ("NEGATIVE: a destination row already costed is never overwritten",
         [{"company": "Nvidia", "revenue_usd_b": "1.00"}], []),
        ("NEGATIVE: a source row with no financials is not 'reused' as blanks",
         [{"company": "Groq"}], []),
        ("NEGATIVE: a substring of a costed name must not match",
         [{"company": "Samsung Heavy Industries"}], []),
        ("NEGATIVE: a name the source map has never heard of",
         [{"company": "Siemens Energy"}], []),
    ]
    failures, extra = [], 0
    for name, dst, expect in cases:
        got = names(dst)
        ok = got == expect
        print(f"  {'ok  ' if ok else 'DEAD'}  {name}")
        if not ok:
            failures.append(f"{name}: expected {expect}, got {got}")

    # The copy must carry provenance, not just the number. A figure that arrives without its
    # filing_source would pass this tool and then fail the gate -- catch it here instead.
    # Guarded, because a broken plan() returning nothing must report DEAD, not raise IndexError.
    # Measured 2026-07-20: an early mutant crashed here and exited 1, so the suite "went red" by
    # accident rather than by assertion. A control that reports failure via a traceback is a control
    # you cannot trust to report anything else.
    copies, _ = plan(SRC, [{"company": "Samsung"}], aliases)
    vals = copies[0][2] if copies else {}
    for col in ("filing_source", "source_tier", "fiscal_year"):
        extra += 1
        ok = bool(vals.get(col))
        print(f"  {'ok  ' if ok else 'DEAD'}  PROVENANCE: the copy carries {col}")
        if not ok:
            failures.append(f"copy dropped {col}")

    # And the trail must say where it came from, or the next reader cannot follow it back.
    rows = apply_copies([{"company": "Samsung", "notes": "seed note"}], copies, "01-semiconductor")
    note = (rows[0].get("notes") or "")
    extra += 1
    ok = "01-semiconductor" in note and "Samsung Electronics" in note and "seed note" in note
    print(f"  {'ok  ' if ok else 'DEAD'}  PROVENANCE: the note names the source map, the source row, and keeps the old note")
    if not ok:
        failures.append(f"trail note is wrong: {note!r}")

    # The figure-level caveat must survive the copy. Samsung's fixture note says the net income is the
    # attributable-to-parent line; dropping that turns a qualified figure into a bare one.
    extra += 1
    ok = "attributable to owners of parent" in note
    print(f"  {'ok  ' if ok else 'DEAD'}  PROVENANCE: the source row's figure caveat travels with the figure")
    if not ok:
        failures.append(f"figure caveat was dropped: {note!r}")

    # ...and the metadata key that carries it must never leak into the CSV as a column.
    extra += 1
    ok = not any(k.startswith("_") for k in rows[0])
    print(f"  {'ok  ' if ok else 'DEAD'}  NEGATIVE: the trail metadata key is not written as a column")
    if not ok:
        failures.append(f"metadata leaked into the row: {sorted(rows[0])}")

    print()
    if failures:
        print(f"SELFTEST FAILED, {len(failures)} case(s):")
        for f in failures:
            print(f"  - {f}")
        return 2
    print(f"SELFTEST PASSED. {len(cases) + extra} cases: it copies what it should, and stays silent on the "
          f"near-misses that would have written one company's figures onto another.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src", nargs="?", help="project dir to copy FROM, e.g. projects/01-semiconductor")
    ap.add_argument("dst", nargs="?", help="project dir to copy INTO")
    ap.add_argument("--apply", action="store_true", help="write; without this it is a dry run")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        print("SELFTEST: does it copy the right rows, and refuse the wrong ones?")
        return selftest()
    if not a.src or not a.dst:
        ap.error("need a source and a destination project dir")
    return run(a.src, a.dst, a.apply)


if __name__ == "__main__":
    sys.exit(main())
