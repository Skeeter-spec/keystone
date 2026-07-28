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
- 🔴 **Cameco (CCJ), NexGen (NXE), Denison (DNN) return "no annual revenue tag" from xbrl_extract, BUT
  Cameco's companyfacts carries `ifrs-full:Revenue` + `ProfitLossAttributableToOwnersOfParent` (Rio
  Tinto costed fine off those same ifrs-full tags).** Before defaulting to expensive PDF extraction,
  check whether xbrl_extract's annual-period selection is missing the ifrs-full annual instance for
  these 40-F filers -- a small tool fix may cost all three nearly free.
- **PDF / IR route, NOT yet costed (the next financials pass):** Orano (orano.group/en/finance, EUR,
  unlisted), Urenco (urenco.com results, EUR, unlisted), EDF (edf.fr finance, EUR, delisted 2023 --
  net income ATTRIBUTABLE TO OWNERS, minorities are large), Kazatomprom (kazatomprom.kz/en/investors,
  IFRS English, attributable), Cameco (fallback if the XBRL fix fails: cameco.com/invest or SEDAR+,
  CAD). FX + market-cap conventions per `shared/SOURCING-ROUTES.md`.
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
