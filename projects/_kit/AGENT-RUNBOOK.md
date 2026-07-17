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

## Chokepoint discipline (applies whenever chokepoint=yes is set)
A chokepoint is a node the value chain genuinely CANNOT route around, not merely a big or important
player. Target roughly 15 to 25 percent of a map's nodes, no more.
- A DUOPOLY's two members can both qualify (Visa and Mastercard; Boeing and Airbus).
- A broad OLIGOPOLY (e.g. the 4 grain traders, the 3 hyperscale clouds, the seed/agrochem majors) is
  concentrated but ROUTABLE: a buyer can switch to a rival, so do NOT flag every member. Record the
  concentration as a theme in FOUNDATION.md instead of flagging individual firms.
- Genuine single points to flag: sole/near-sole suppliers, the one refiner/enricher/packager, a strait
  or canal with no bypass, a messaging/settlement rail everyone depends on.
- Sanity check before finishing: if more than ~1 in 4 nodes is yes, you are over-flagging; retighten.

## Provenance tiers (source_tier)
1 primary regulatory/audited filing or the company's own audited statements
2 official statistics / first party disclosure (newsroom, gov agency)
3 trackers / aggregators / think tanks
4 news
