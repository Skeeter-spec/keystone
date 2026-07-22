# Roadmap — toward a Bloomberg-level, three-lens dashboard

No rush. Built one step at a time. This document is the compass; the CSVs are the truth; the
artifact is the view. Read alongside `README.md` (schema + onion) and the `semiconductor-ecosystem`
skill (the refresh loop).

Guardrail that never changes: this is public company and market research for **learning and
reference**. It is not investment advice. Every professional-grade number carries a primary source.

## The three lenses

The same company graph, read three ways. Every data point we add belongs to one lens and carries a
source tier (below). This is what turns a roster into a terminal.

1. **Accounting** — what each company actually is, financially. The audited reality.
2. **International politics** — the policy, trade, and sanctions forces acting on each node and edge.
3. **Economics** — the industry structure and macro cycle the whole board sits inside.

## Artifact structure review (where we are, honestly)

What is right today:
- Data-as-truth in versionable CSVs; artifact is a regenerated view (good separation).
- Self-contained, durable (authored watchlist/notes export; data regenerable).
- One template + `build_artifact.py` makes republishing one command.

Three structural facts that shape everything ahead:
- **A) The financial schema is a single snapshot per company.** Bloomberg-level needs *time series*
  (quarterly). Trend charts, margin history, capex cycles, and the semiconductor cycle all require a
  separate `financials_timeseries.csv` (one row per company per fiscal period), not more columns.
- **B) Provenance is thin.** We have `filing_source` + `confidence`. We need every row tagged with a
  **source tier** and a **lens** so the dashboard can show "how do we know this" and filter by lens.
- **C) One artifact view will not hold three lenses.** The target is a tabbed terminal: a per-company
  "terminal" view that stacks all three lenses, plus per-lens analytics tabs. The build pipeline
  (template + baked JSON) scales to this; it just feeds from more CSVs.

## Target data model (grow into this, do not rebuild)

```
companies.csv               identity + roles + latest-snapshot headline figures (have)
relationships.csv           directed edges, the graph (have)
financials_timeseries.csv   company, period, revenue, margins, rd, capex, segment... (have, Accounting)
segments.csv                company, period, segment, revenue, share (NEW, Accounting/Economics)
policies.csv                action, agency, date, targets[], type, status, source (NEW, Politics)
market_stats.csv            metric, segment, period, value, unit, source (NEW, Economics)
sources.csv                 source_id, tier, publisher, url, retrieved  (have, provenance registry)
```

Add two columns to every data table over time: `lens` (accounting|politics|economics) and
`source_tier` (1-4, below). **Both are live on `companies.csv` and on `relationships.csv` already**, so
what remains is carrying them into the tables that do not exist yet. The relationship table's tier
column is named `source_tier` rather than `evidence_tier`.

---

## Lens 1 — Accounting

**Sources (free first).**
- SEC EDGAR — 10-K, 20-F, 40-F, 8-K, 6-K, F-1, DEF 14A; plus the XBRL Financial Statement Datasets and
  the `frames`/`companyconcept` APIs for structured, machine-readable line items.
- Home-country regulators for non-US filers (primary, authoritative):
  - Taiwan: MOPS / TWSE Market Observation Post System (TSMC, UMC, MediaTek, ASE, Unimicron).
  - South Korea: DART, run by the FSS (Samsung, SK hynix).
  - Japan: EDINET (FSA) and TDnet (TSE timely disclosure) — Murata, TDK, Ibiden, Taiyo Yuden.
  - Netherlands: AFM / Euronext Amsterdam (ASML) — also files a US 20-F.
  - Germany: Bundesanzeiger + BaFin (Infineon, BMW).
  - Hong Kong: HKEXnews (SMIC, Lenovo).
  - Mainland China: SSE / SZSE disclosure (JCET).
  - UK: Companies House (Arm's UK entity) — also files a US 20-F.
- Company investor-relations pages, annual reports, and earnings-call transcripts.

**Analytics to run.**
- Normalize to USD and a common calendar; record the FX rate and the accounting standard (US GAAP vs
  IFRS vs local) — comparability caveats are part of the output.
- Core ratios: gross / operating / net margin, R&D intensity (R&D ÷ revenue), capex intensity
  (capex ÷ revenue — the fabless-vs-fab signal), ROIC, free cash flow, inventory days.
- Segment mix: revenue by business line (how much of Samsung is memory vs foundry vs devices).
- Customer concentration: mine the "customer concentration" and "risk factors" disclosures for named
  buyers and their revenue share — this feeds the relationship graph with weighted edges.
- Time series: revenue / margin / capex by quarter once `financials_timeseries.csv` exists.

**Verification steps.**
- Every figure reconciles to a primary filing line item (prefer the XBRL-tagged value over prose).
- Reconcile any press-reported number against the audited statement; keep the audited one, note the other.
- Record the FX rate and standard used; flag GAAP/IFRS differences that break comparability.
- Two-source rule for volatile figures (market cap especially).

**Public records to fact-check against.**
SEC EDGAR · Taiwan MOPS/TWSE · Korea DART (FSS) · Japan EDINET (FSA) · Netherlands AFM · Germany
Bundesanzeiger · HKEXnews · SSE/SZSE · UK Companies House.

---

## Lens 2 — International politics

**Sources.**
- US export control + trade: BIS (Bureau of Industry and Security) Entity List and the advanced-
  computing / semiconductor export rules; the Federal Register (rule text + amendments); OFAC
  sanctions lists (Treasury); CFIUS actions (Treasury-chaired); USITC (tariffs, Section 337).
- US subsidies: the CHIPS Program Office at NIST (CHIPS for America) award announcements and terms.
- Independent US analysis: Congressional Research Service (crsreports.congress.gov) and GAO reports.
- EU: the European Chips Act; European Commission trade-defense actions.
- National export licensing that binds specific firms: the Dutch government's licensing of ASML EUV/DUV
  to China; Japan METI controls; Korea MOTIE; Taiwan MOEA.
- China: MOFCOM and MIIT policy; the National IC Industry Investment Fund ("Big Fund") disclosures;
  China's own export controls (e.g. gallium / germanium).
- Industry context: SIA (Semiconductor Industry Association) policy briefs; CSIS and similar think-tank
  trackers (Tier 3 — corroborate, don't treat as primary).

**Analytics to run.**
- Policy-exposure flags on nodes and edges: which company/relationship is touched by which control
  (e.g. SMIC on the Entity List; ASML EUV barred to China; Nvidia's China-specific SKUs).
- Subsidy map: CHIPS Act and EU/Japan/Korea/China incentive dollars per company/fab, with award dates.
- Geographic concentration risk: share of leading-edge capacity in Taiwan, overlaid on the chokepoints
  — the single most important geopolitical number in this industry.
- Timeline: policies are dated and amended; track effective dates and revisions.

**Verification steps.**
- Cite the primary regulatory document (Federal Register entry, BIS rule, official award release), never
  a news paraphrase, for anything consequential.
- Date-stamp every policy and note supersessions — export rules change often.
- Separate "announced" from "in effect" from "awarded but not disbursed."

**Public records to fact-check against.**
BIS (bis.doc.gov) · Federal Register · NIST CHIPS Program Office · OFAC (Treasury) · CFIUS/Treasury ·
USITC · GAO · CRS · European Commission · Dutch government export-licensing notices · METI · MOTIE · MOEA.

---

## Lens 3 — Economics

**Sources.**
- Industry sales + structure: WSTS (World Semiconductor Trade Statistics) official releases; the SIA
  factbook. Note: Gartner / IDC / TrendForce carry granular share and pricing data but are largely
  **paid** — mark anything sourced from them lower-confidence unless corroborated by a free primary.
- Equipment demand: SEMI billings and book-to-bill press releases (the World Fab Forecast is paid).
- Macro: FRED (St. Louis Fed), BEA, the Federal Reserve, IMF, World Bank, OECD.
- Trade flows: US Census trade data and UN Comtrade (HS codes for ICs, equipment, wafers).
- Inputs / commodities: prices for neon, palladium, gallium, germanium (supply shocks hit fabs).

**Analytics to run.**
- Market share by layer and a Herfindahl-Hirschman Index (HHI) per layer — this *quantifies* the
  chokepoints economically (foundry, EDA, lithography, HBM all score as highly concentrated).
- Cyclicality: the semiconductor cycle vs macro indicators; inventory-correction signals.
- Leading indicators: equipment book-to-bill and hyperscaler capex as forward demand signals for chips.
- Demand decomposition: AI/datacenter vs mobile vs auto vs industrial.
- Pricing dynamics where free: memory and HBM price trends.

**Verification steps.**
- Prefer WSTS/SIA official figures; distinguish estimates from actuals and mark estimate confidence lower.
- Explicitly flag any analytic that depends on paid data we cannot independently verify for free — say so
  in the dashboard rather than presenting it as fact.

**Public records to fact-check against.**
WSTS · SIA · SEMI (partial/free) · US Census Bureau (trade) · UN Comtrade · FRED / Federal Reserve ·
BEA · IMF · World Bank · OECD.

---

## Cross-cutting: the verification framework

**Source tiers** (stored on every row as `source_tier`):
- Tier 1 — primary regulatory + audited filings (SEC/DART/MOPS/EDINET/AFM; Federal Register; BIS; award
  terms). Treat as fact.
- Tier 2 — official statistics agencies (WSTS, SIA, Census, FRED, IMF, OECD, UN Comtrade). Treat as
  authoritative estimate/actual as labeled.
- Tier 3 — reputable trackers and think tanks (CSIS, TrendForce, Gartner, IDC). Corroborate; often paid.
- Tier 4 — news and commentary. Lead-generation only; must be upgraded to Tier 1-2 before it ships as fact.

**Rules.** Two independent sources for any volatile or contested figure. Record retrieved-date on
everything (data ages). Never let a Tier 4 claim appear without a Tier 1-2 backstop. Keep a `sources.csv`
registry so any number in the dashboard is one click from its origin.

## Phased plan (independently useful stages, do in order, ship value each burst)

- **Phase A — foundation (in progress).** Finish Layer 1 headline financials for all 41; map the
  chokepoint relationship edges. Add `lens` + `source_tier` columns and a `sources.csv` registry.
- **Phase B — Accounting depth.** Stand up `financials_timeseries.csv` (quarterly) for the 8 chokepoints;
  compute the ratios; add a Financials analytics tab with margin/capex trend charts (reuse the
  `timeseries-dashboard` component; self-contained SVG).
- **Phase C — Politics lens.** Build `policies.csv` (Entity List, export controls, CHIPS/EU awards) keyed
  to companies; add a Geopolitics tab with exposure flags, a subsidy map, and the Taiwan-concentration number.
- **Phase D — Economics lens.** Build `market_stats.csv` (segment shares, WSTS cycle, book-to-bill); add a
  Markets tab with per-layer HHI gauges and a cycle chart.
- **Phase E — Terminal polish.** A per-company cross-lens "terminal" view; enriched watchlist; alerting on
  policy/earnings changes; the Bloomberg-grade layout pass.

## Cost discipline

Free-first, always. Everything in Tiers 1-2 is free. Where an analytic truly needs paid data (fine-grained
market share, fab forecasts), we either approximate from free primaries or label it clearly as
unverified-because-paid. Research bursts stay cost-routed (Sonnet for filing/policy reading, one or two
items per run). See the `semiconductor-ecosystem` skill and `prefers-cost-conscious-model-routing`.
