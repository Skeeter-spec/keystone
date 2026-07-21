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
