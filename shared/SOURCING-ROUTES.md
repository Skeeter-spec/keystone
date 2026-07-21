# Sourcing routes, by jurisdiction

Where a company's **audited annual figures** actually live, and what it costs to get them. Written
2026-07-20 after costing 02's five chokepoints across three different national filing systems.

**Why this file exists.** Costing 02 measured something the plan did not predict: extraction was never
the bottleneck. Once a route was known, a company took minutes. **Finding the route took the majority of
the time** -- the Shanghai trio burned most of a burst on `cninfo` with wrong params, then on `cninfo`
being the wrong exchange entirely, then on an SSE API that returns empty, before landing on a working
host. That cost is paid once per jurisdiction and then never again, which is exactly the shape of thing
that belongs in a file instead of in one session's memory.

⇒ **Before costing a batch, route it first.** One probe per company answering only "does an audited
filing exist, in what language, at what host?" Then batch the extraction by route. Costing companies
one at a time re-pays the discovery cost once per company.

## The routes

| Jurisdiction | Host | Format | Cost |
|---|---|---|---|
| **US** (10-K) and foreign private issuers (20-F/40-F) | `data.sec.gov` XBRL `companyfacts` | **structured JSON** | cheapest by far. No PDF, no rendering |
| **Mainland China, dual-listed** | `hkexnews.hk` | English audited PDF | one search + one PDF |
| **Shanghai A-shares** (600xxx/603xxx) | filed at SSE; retrievable via the eastmoney `pdf.dfcfw.com` **mirror** | Chinese PDF | most expensive: locate, render, read by eye |
| **Shenzhen A-shares** (000xxx/002xxx/300xxx) | `cninfo.com.cn` | Chinese PDF | untested here |
| **Germany / Xetra** (and EU issuers generally) | the company's own IR asset host, e.g. `assets.siemens-energy.com` | English audited PDF | cheap: one search, one PDF, English throughout |
| Market prices / FX | Yahoo `v8/finance/chart/<symbol>` | JSON | works |
| **EUR to USD conversion** | ECB `data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?startPeriod=&endPeriod=&format=csvdata` | CSV | free, no key, official. Average the dailies over the issuer's OWN fiscal year |

## Traps, each one measured here

- 🔴 **`cninfo.com.cn` serves SHENZHEN, not Shanghai.** Querying it for 600111 / 603799 / 600497
  returns `totalAnnouncement: 0` with **HTTP 200 and no error**. A zero result reads exactly like "this
  company has no annual report". It means "wrong exchange". This single wrong assumption cost the most
  time in the whole burst.
- **SSE's own query API returned an empty `pageHelp.data` array** for all three codes with the params
  tried. Not necessarily broken, but do not budget on it working.
- **Yahoo `quoteSummary` and `v7/finance/quote` are BLOCKED** (`Invalid Crumb` / `Unauthorized`). Only
  the `v8` chart endpoint works, and it returns **price only** -- no shares outstanding, no market cap.
  Share counts must come from the filing.
- **`pdf.dfcfw.com` is a MIRROR.** The document is the SSE-filed audited report, but you did not read it
  at the publisher. Say "mirror" in `sources.csv` and in the row note, and corroborate with an in-filing
  cross-check rather than pretending the host is authoritative.
- 🔴 **A COLUMN LABELLED "FY 2025" CAN BE THE QUARTER.** Measured on Siemens Energy's Q4 FY25 earnings
  release, 2026-07-20. Its statements carry four columns under two spanning headers, `Q4` over the first
  two and `Fiscal year` over the last two, so the columns read **FY 2025 | FY 2024 | 2025 | 2024** and the
  one that says "FY 2025" is **Q4**. Revenue there is €10,428M; the actual full year is €39,077M, 3.7x
  larger. Nothing about the wrong number looks wrong. Any European issuer's quarterly release can do this,
  and it is the second reason (after column interleaving) to READ THE RENDERED PAGE rather than the text
  layer: the spanning header is a visual fact that flattens away.

## Reading a filing you cannot get as XBRL

1. **Locate with the text layer; READ from a rendered image.** `page.get_text()` is for finding the page.
   Financial tables put the current and prior year in adjacent columns and the text layer can interleave
   them. Render the region and read it.
2. 🔴 **Anchor to the CONSOLIDATED statement.** A PRC annual report contains both 合并利润表 (consolidated)
   and 母公司利润表 (parent-company only), with **identical row labels and different numbers**. An
   unanchored search for 营业收入 finds the parent-only figure and nothing complains. This happened; the
   first extraction pass was thrown away.
3. **Read the units off the page** (单位：元 / 万元 / 千元). Do not assume.
4. **Cross-check inside the filing before the number leaves it.** Two that work on any issuer:
   - attributable profit + minority interest == total net profit (exact, to the cent)
   - attributable profit / basic EPS == the share count you expect

## Figures: which line, and why it is not the obvious one

- **Net income = attributable to the PARENT**, never consolidated. Measured gaps: Vale **2.352 vs 1.983**,
  BHP **9.019 vs 11.143** (24% overstatement). Where minority interest is **negative** the parent's share
  is LARGER than the consolidated total (Yunnan Chihong, Vale) -- so this is not a "pick the smaller one"
  heuristic, it is a "pick the right line" rule.
- **Capex = cash-flow capex first** (`PaymentsToAcquirePropertyPlantAndEquipment`,
  `PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities`, or PRC
  购建固定资产、无形资产和其他长期资产支付的现金). Fall back to PP&E additions only when no cash-flow tag
  exists (Vale, Rio Tinto), and say so in the row.
- **Never select a concept by max value or by first-namespace-wins.** Print every candidate at the
  reporting year and choose deliberately. That step caught three wrong figures in one session.
- **Reject stale periods, including instants.** Ford's tagged `EntityCommonStockSharesOutstanding` is
  dated **2011**; USA Rare Earth's predates its own FY2025 year end. A stale share count silently
  produces a confidently wrong market cap.
- **Leave it empty rather than approximate.** Market cap is omitted for dual-listed issuers (Ganfeng,
  JL MAG, BHP's 2:1 ADR, Rio's plc/Limited split) because a clean total is not available. Lithium
  Americas has **no revenue line at all** -- it is pre-revenue, so revenue is empty, **not zero**; zero
  would be a claim the filing does not make.

## Identity

Verify the **registrant name**, never just the identifier. Ticker `NEO` resolves to CIK 1077183 =
NEOGENOMICS INC, a cancer diagnostics company; this repo's NEO is Neo Performance Materials (TSX, no SEC
filings). Enforced by `tools/check_identity.py` against `shared/edgar_registrants.csv`.
