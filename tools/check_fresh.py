#!/usr/bin/env python3
"""Is every committed artifact still what its CSVs would build today?

The gate checks the CSVs against the README, and build_map.py checks the CSVs against map.json.
Nothing checked the last link: the built artifact/*.html against the CSVs. So a map whose
companies.csv was edited but never rebuilt shipped a STALE page and the gate passed it (measured
2026-07-17: added a CSV row, skipped the rebuild, gate exit 0). The gate note punted this to "a
browser and a human eye" -- but drift is a pure rebuild-and-diff, no browser needed, which matters
because the Browser pane hangs 300s on a local file:// anyway.

Method: for each project that HAS a built artifact, re-render from the current CSVs + map.json using
the artifact's OWN declared build date (the one thing allowed to differ without a data change), and
compare byte for byte. A mismatch means the on-disk artifact no longer reflects its data.

    python3 tools/check_fresh.py            # exit 1 if any artifact is stale, silent if all fresh
    python3 tools/check_fresh.py --selftest # induce staleness on a copy, prove the check catches it
"""
import json, re, sys, pathlib, tempfile, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "shared"))
import build_map  # noqa: E402  -- shares render() so this check cannot drift from the builder

DATE_RE = re.compile(r'const BUILD = (\{.*?\});')


def declared_date(html):
    m = DATE_RE.search(html)
    return json.loads(m.group(1))["date"] if m else None


def check_one(proj):
    """Return None if fresh (or no artifact yet), else a reason string."""
    cfg_path = proj / "map.json"
    if not cfg_path.exists():
        return None
    cfg = json.loads(cfg_path.read_text())
    art = proj / "artifact" / f"{cfg['storage_key']}.html"
    if not art.exists():
        return None  # foundation map with no artifact yet is incomplete, not stale
    on_disk = art.read_text()
    date = declared_date(on_disk)
    if date is None:
        return f"{art.name}: no baked BUILD date found; cannot verify freshness"
    # load_project(), not a second hand-kept list of CSVs. This file used to keep its own and it
    # drifted the day gaps.csv was added. render() now has no default for gaps either, so a caller
    # that forgets new data fails loudly instead of rendering a quietly different page.
    companies, rels, ts, gaps = build_map.load_project(proj)
    fresh = build_map.render(cfg, companies, rels, ts, date, gaps)
    if fresh != on_disk:
        return f"{art.name}: STALE -- the CSVs no longer render to the committed artifact (rebuild it)"
    return None


def main():
    stale = []
    for proj in sorted((ROOT / "projects").glob("*/")):
        r = check_one(proj)
        if r:
            stale.append(r)
    if stale:
        print("STALE ARTIFACTS (data edited without a rebuild):")
        for s in stale:
            print(f"  {s}")
        return 1
    return 0


def selftest():
    """Induce the exact fault measured on 2026-07-17: edit a CSV, do not rebuild, expect a catch.
    Operates on a temp copy so the real tree is never touched."""
    # pick any project that has a built artifact
    victim = None
    for proj in sorted((ROOT / "projects").glob("*/")):
        cfg_p = proj / "map.json"
        if cfg_p.exists():
            cfg = json.loads(cfg_p.read_text())
            if (proj / "artifact" / f"{cfg['storage_key']}.html").exists():
                victim = proj
                break
    assert victim, "selftest needs at least one project with a built artifact"

    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td) / victim.name
        shutil.copytree(victim, tmp)

        # CONTROL: an untouched copy must read as FRESH (silent).
        assert check_one(tmp) is None, "control failed: a freshly-built artifact was called stale"
        print("  ok    control: untouched artifact reads as fresh")

        # INDUCE: append a company row to the CSV, leave the artifact alone.
        csv_p = tmp / "data" / "companies.csv"
        lines = csv_p.read_text().splitlines()
        lines.append(lines[-1].split(",", 1)[0] + "_STALE_INDUCED" + "," + lines[-1].split(",", 1)[1])
        csv_p.write_text("\n".join(lines) + "\n")
        reason = check_one(tmp)
        assert reason and "STALE" in reason, f"INDUCED fault not caught: {reason!r}"
        print(f"  ok    induced: edited CSV without rebuild -> caught ({reason.split(':')[0]})")

        # NEGATIVE precision: rebuild the tmp artifact, it must go silent again.
        build_map.build(str(tmp), declared_date((tmp / "artifact" / f"{cfg['storage_key']}.html").read_text()))
        assert check_one(tmp) is None, "after a correct rebuild the artifact should read fresh again"
        print("  ok    negative: after rebuild, reads fresh again (no false positive)")

    print("SELFTEST PASSED. 3 cases.")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
