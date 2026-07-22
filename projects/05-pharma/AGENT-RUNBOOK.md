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

## 🔴 INVENTORY `tools/` BEFORE WRITING A WORKER PROMPT

Measured 2026-07-21 on this map, and it is the single most expensive mistake made here so far. The EDGAR
worker was not told `tools/xbrl_extract.py` exists, so it hand-rolled its own SEC extraction across **54
tool calls for 13 companies and 123592 tokens** -- on the route `SOURCING-ROUTES.md` calls "cheapest by
far", and after 04 had already costed eleven companies with that tool in one batch.

The three workers cost **123592, 130141 and 195955 tokens** against a 45000 estimate each. A worker cannot
know what it was not told, and it will always be able to reinvent a tool it does not know about.

⇒ **Every fan-out prompt names the tools the worker should use, by path:**
- `tools/xbrl_extract.py --ticker T --expect "Name"` -- US filers and foreign private issuers. Identity
  check is built in via `--expect`.
- `tools/reuse_costed.py <src> <dst>` -- run FIRST, before any research. Free rows, zero fetches.
- `tools/verify_sources.py`, `tools/check_identity.py` -- what will judge the output afterwards, so the
  worker knows what it is writing for.

## Naming, and the two alias tables

This map names some companies `Parent (Arm)` -- `CVS Health (Caremark)` -- to say WHY a company is on a
pharma map. That parenthetical is **not the reporting scope**: the figures are whole-company, exactly as
04 does with `Alphabet (Google Cloud)`. Say so in the row note.

🔴 A roster name like that appears in no filing, so `verify_sources.py` will fail the row until an alias
exists. **There are two alias tables and they are not interchangeable:**
- `shared/company_aliases.csv` → read by `reuse_costed.py` and `check_identity.py`.
- the `KEY` dict in `tools/verify_edges.py` → read by `named()`, which is what **both verifiers** match on.

Adding a verification alias to the CSV does nothing at all, silently. Look at the consumer, not the
filename.
