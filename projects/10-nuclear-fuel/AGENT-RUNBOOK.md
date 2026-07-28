# Agent runbook for projects/10-nuclear-fuel

🔴 **Read [`../_kit/AGENT-RUNBOOK.md`](../_kit/AGENT-RUNBOOK.md) FIRST. It is the authoritative burst procedure.**

The shared discipline is the single source of truth in `_kit` and is deliberately NOT copied here, so it
cannot drift out of a stale copy (this repo's own rule: a copy rots, a pointer does not). That includes:
stage candidate edges in `data/_incoming/edges_*.csv`, then run `tools/verify_edges.py projects/10-nuclear-fuel`,
then merge; file `data/gaps.csv` rows as you go; the chokepoint discipline; and closing a burst under one
`## HONEST WEAKNESSES` heading with the rows in the same commit.

## Notes for this map

Written after the 2026-07-25 burst (Foundation -> Edges started). Routing only; shared procedure stays in `_kit`.

### Financials routing (finding the route is the cost -- read before spending)
- **DONE via SEC XBRL (`tools/xbrl_extract.py --ticker <T> --expect "<name>"`):** Centrus (LEU), BWXT,
  Uranium Energy (UEC), Energy Fuels (UUUU), Constellation (CEG), Honeywell (HON), Rio Tinto (RIO).
  Identity bindings already in `shared/edgar_registrants.csv`.
- ✅ **RESOLVED 2026-07-28, and the hypothesis above it was WRONG. It was never the tag list or the
  annual-period selection: it was the CURRENCY.** `xbrl_extract.py` dropped every fact whose unit was
  not `USD`, before any period logic ran. Cameco and Denison are 40-F filers tagging `ifrs-full` in
  **CAD**, so their revenue, attributable profit, capex and R&D were all present and all discarded,
  and the tool reported "no annual revenue tag" -- which reads as *the filer does not disclose it*.
  Rio Tinto only ever worked because Rio tags in USD. The filter now accepts any ISO-4217 unit, the
  report labels the currency on every line, and a non-USD fixture guards it. **Cameco and Denison are
  now costed straight from XBRL. NexGen is a genuinely different case** -- it has no revenue concept
  in any currency, being exploration stage, so its revenue stays EMPTY, never 0.
- **DONE via publisher PDF / IR (2026-07-28):** Orano, Urenco, Kazatomprom, EDF. Exact document URLs are
  the `filing_source` on each row in `companies.csv`; start there rather than re-searching the host.
  🔴 **Each of these four publishes a prominent ADJUSTED earnings figure next to the reported one, and
  the adjusted one is the decoy** (Orano's adjusted attributable was -25 EUR m against a reported
  404; EDF leads with 9.6 EUR bn "excluding non-recurring items" against a reported 8,367 EUR m).
  Take the IAS 1 line that allocates profit to owners of the parent, and CROSS-CHECK attributable +
  non-controlling interests == total. That check is exact for EDF and Kazatomprom, off by 1 EUR m on
  the face of Orano's own statement, and IMPOSSIBLE for Urenco, which discloses no NCI split at all.
- 🔴 **`edf.fr` is UNREACHABLE to this repo's verifiers on this machine** -- system Python 3.9.6 links
  LibreSSL 2.8.3 and cannot negotiate the TLS version the host demands, and curl is served 403. EDF is
  the one costed row `verify_sources.py` cannot check. See gap-10-6. Do not "fix" this by swapping in
  a weaker reachable citation.
- **Leave UNCOSTED (blank, NOT gap rows -- honest "not yet costed"):** Rosatom/TENEX, TVEL, Uranium One
  (ARMZ), GLE, Westinghouse, CNNC parent, Framatome -- state-owned / private / JV, no standalone
  audited public financials (Framatome may be reachable via EDF segment reporting).

### Edge disclosure pattern (measured on the Centrus 10-K pilot)
Enricher/converter filings NAME their SWU/LEU **suppliers** via defined "Supply Contract/Agreement"
terms (this yielded TENEX->Centrus and Orano->Centrus) but describe **customers** only generically as
"utilities" -- customer names are an `undisclosed` gap (see gap-10-1). So mine the supplier side plus
ownership/JV stakes (Cameco's AIF gave Westinghouse 49%, the Inkai JV with Kazatomprom, and the
Cameco/Silex split of GLE). Next relationship targets: Kazatomprom's offtake JVs (CGN, Orano/Katco,
Uranium One) and a VVER-fuel utility filing that would evidence the TVEL chokepoint (gap-10-3).

### Already in place (do not redo)
- Nuclear roster aliases are ALREADY in `tools/verify_edges.py` KEY (the nuclear block). Any NEW roster
  name still needs adding there, or verify_edges/verify_sources false-negative on it.
- `map.json` `relationship_types` vocabulary is declared. `merge_edges` rejects tier-4 edges and any
  type outside that list, and aborts the whole batch on the first violation.
