# Agent runbook (one burst)

Shared schema across every Keystone map. Never invent figures; every number and edge needs a real source.

## Bursts
- FOUNDATION: lock the layer taxonomy (README onion), seed ~20 to 30 real companies into data/companies.csv
  (company,ticker,exchange,hq_country,roles,primary_segment filled; financials blank; set chokepoint yes
  for suspected chokepoints (the value must be exactly `yes` or `no`, never TRUE/FALSE:
  the artifact template tests chokepoint==='yes', so TRUE renders as NOT a chokepoint, silently); lens=accounting), and write FOUNDATION.md (chokepoint hypotheses + free sources).
- FINANCIALS: fill revenue/net income/market cap/R&D/capex for the next company with empty revenue_usd_b,
  from a primary filing URL; convert to USD billions and note the FX rate. Chokepoints first.
- RELATIONSHIPS: read a company's latest filing customer/supplier/risk sections; add supplier side edges to
  data/relationships.csv with a cited evidence_source.

## Provenance tiers (source_tier)
1 primary regulatory/audited filing or the company's own audited statements
2 official statistics / first party disclosure (newsroom, gov agency)
3 trackers / aggregators / think tanks
4 news

## Where the figures live

Before costing a batch, read `shared/SOURCING-ROUTES.md` and ROUTE the companies first (which host, which
language, structured or PDF). Extraction is cheap once the route is known; finding the route is what costs.
It also carries the traps: cninfo serves Shenzhen not Shanghai, consolidated vs parent-company statements
share row labels, net income means attributable-to-parent, and an identifier that resolves is not the
entity you meant.

## Record what you could NOT source (data/gaps.csv)

**A burst that finds nothing on a target has produced a result, not a blank.** On 04 the strongest
findings were absences: no hyperscaler names Nvidia anywhere in its own 10-K, and TSMC's 20-F will only
ever say "our largest customer". A map that records only what it could source draws those identically to
a relationship that does not exist, which is the opposite of what the reader should conclude.

So when you go looking for an edge or a figure and the document declines to say, write a row in
`data/gaps.csv` instead of dropping it:

```
gap_id,kind,subject,sought,searched,found_instead,blocks,would_close_it,status,last_checked
```

- `kind` is exactly one of `undisclosed` (the document exists and will not say), `unreachable` (a real
  source you could not read), `contradiction` (sources disagree, or the reported world contradicts the
  disclosed one), `unevidenced-flag` (this map claims something with no sourced edge behind it),
  `stale-evidence` (a SOURCED claim whose evidence predates a material change, so an existing edge
  becomes suspect), `out-of-scope` (the counterparty IS disclosed but is not on this map's roster, so
  the edge cannot be drawn). Anything else fails the gate.
- 🔴 **`out-of-scope` is the one that is usually YOUR MAP's bug, not the world's.** If a company returns
  no edges, check its counterparties against companies.csv before concluding anything: 02's Syrah looked
  unconnected purely because Ford, LG Energy Solution and POSCO were not on the roster.
- 🔴 **`searched` is what makes it evidence rather than a shrug, and the gate REJECTS a row without it.**
  Name the documents you actually opened: "TSMC FY2025 20-F, full text; Nvidia FY2026 10-K, full text".
  "Could not find anything" is unfalsifiable and worth less than silence.
- **`would_close_it`** must name the document or disclosure that would settle it, so the gap becomes the
  next burst's task rather than a permanent excuse.
- `found_instead` should quote the fudge where there is one. "Customer A through Customer G" and
  "our ten largest customers" are the actual findings.
- A `contradiction` must name at least two sources in `searched`, separated by `;`. One source cannot
  contradict anything.

These render on the map under **What the filings won't say**, with the open count on the front page.
