# Foundation brief: EV batteries

Written at the FOUNDATION burst. Chokepoint calls here are hypotheses to test with real edges
(data/relationships.csv) and real financials (data/companies.csv), not conclusions.

## Chokepoints, ranked

1. **CATL** (300750.SZ / 3750.HK, China) — cell-maker. Over a third of global EV cell
   output on its own; GM, Ford, Tesla (China), and most non-Chinese automakers rely on it
   for at least one platform. The single hardest node to route around in the whole chain.
2. **BYD** (1211.HK / 002594.SZ, China) — cell-maker;automaker. Second largest cell maker,
   and the only player that is *also* a top-3 global automaker, so it does not need the rest
   of the chain the way every other cell maker does. Its blade-LFP design and in-house
   vertical integration make it a chokepoint on both the supply and demand side at once.
3. **China's separator duopoly-ish cluster** — Yunnan Energy New Material (SEMCORP,
   002812.SZ) and Shenzhen Senior Technology (300568.SZ), with Asahi Kasei (3407.T, Japan,
   via Celgard/Hipore) as the main non-Chinese alternative. Separator film is a
   low-margin, capital-intensive, precision-coating business; entry is slow and capacity
   is concentrated in a handful of firms. If any one of these three has a quality or export
   problem, cell output stalls industry-wide.
4. **BTR New Energy Materials** (835185.BJ, China) — anode-maker. World's largest graphite
   anode producer. Natural graphite anode processing (purification + graphitization) is
   almost entirely a Chinese industrial capability today; China's late-2023 graphite
   export permit requirement demonstrated how exposed the rest of the world is here.
5. **Guangzhou Tinci Materials** (002709.SZ, China) — electrolyte-maker. Largest electrolyte
   producer and a major source of the LiPF6 salt nearly every electrolyte formulation uses;
   LiPF6 production is itself concentrated among a small number of Chinese chemical makers.
6. **Glencore** (GLEN.L, Switzerland/DRC) and **CMOC Group** (603993.SS, China/DRC) —
   miners. Global cobalt supply is dominated by a handful of mines in the Democratic
   Republic of Congo; these two firms control most of that output between them,
   making DRC political and infrastructure risk a chain-wide risk.
7. **Cathode/precursor concentration in China and Korea** (Ronbay, Ningbo Shanshan,
   POSCO Future M, Umicore as the main non-Chinese counterweight) — not yet a single
   chokepoint company, but a layer where alternatives outside China and Korea are thin.
   Worth watching as relationship edges get filled in; Umicore is the node to test first
   since it is one of the few Western-aligned CAM/precursor producers at scale.

Working hypothesis for Layer 4/5 (research burst target): pack/module integration and
automaker demand are NOT chokepoints in themselves — there are many automakers and the
skill is not scarce — but automaker *purchasing decisions* (who they single-source from)
propagate chokepoint risk upstream. That linkage is exactly what relationships.csv should
capture next.

## Free data sources by lens

### Accounting (company filings, investor relations)

- SEC EDGAR full text search, for US filers (Tesla, Albemarle, GM, Li-Cycle):
  https://www.sec.gov/cgi-bin/browse-edgar
- CATL investor relations (Shenzhen exchange disclosure + annual report):
  https://www.catl.com/en/about/investor/
- BYD investor relations (HKEX filings + annual report):
  https://www.byd.com/en/investor
- LG Energy Solution IR (KRX disclosures + English annual report):
  https://www.lgensol.com/en/investor-information
- Samsung SDI IR: https://www.samsungsdi.com/investor-relations.html
- Panasonic Holdings IR (segment data for Panasonic Energy):
  https://holdings.panasonic/global/corporate/investors.html
- Umicore IR (annual report has clean segment breakout for battery materials/recycling):
  https://www.umicore.com/en/investors/
- Albemarle IR (10-K has lithium segment detail):
  https://investors.albemarle.com/
- SQM 20-F and IR (Chile, files with SEC as foreign private issuer):
  https://www.sqm.com/en/investors/
- Glencore annual report and production report (cobalt volumes by mine):
  https://www.glencore.com/investors
- Toyota, Volkswagen Group annual reports (BEV volume and battery sourcing disclosed
  in sustainability/integrated reports): https://global.toyota/en/ir/ ,
  https://www.volkswagen-group.com/en/investor-relations-13908
- stockanalysis.com and companiesmarketcap.com for quick market cap / ticker cross-checks
  on non-US filers (secondary source, use tier 2-3, not tier 1)

### Politics (policy and trade rules that reshape the chain)

- US Treasury/IRS guidance on the IRA Section 30D clean vehicle credit and Foreign Entity
  of Concern (FEOC) battery-material rules: https://home.treasury.gov/policy-issues/tax-policy/inflation-reduction-act
- US Department of Energy FEOC guidance: https://www.energy.gov/policy/foreign-entity-concern
- EU Batteries Regulation (2023/1542) — carbon footprint, due diligence, and recycled
  content requirements: https://eur-lex.europa.eu/eli/reg/2023/1542/oj
- China Ministry of Commerce export control notices on graphite (and related battery
  materials) — announcements page: http://www.mofcom.gov.cn/ (English coverage via
  Reuters/Bloomberg trade desks when primary text is Chinese-only)
- US Section 232/301 tariff actions affecting battery materials and EVs, via USTR:
  https://ustr.gov/issue-areas/enforcement/section-301-investigations
- DRC Ministry of Mines and cobalt export policy context (for Glencore/CMOC exposure):
  https://www.mines.gouv.cd/

### Economics (industry-level sizing and trade data)

- IEA Global EV Outlook (annual, free PDF, has cell/material demand and chokepoint framing):
  https://www.iea.org/reports/global-ev-outlook-2025
- BNEF (BloombergNEF) public summaries and press releases on battery pricing and
  lithium-ion supply chain: https://about.bnef.com/electric-vehicle-outlook/ (full report
  is paywalled; press releases and executive summaries are free)
- USGS Mineral Commodity Summaries (lithium, cobalt, nickel, graphite — global production
  and reserves by country, free annual PDF): https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries
- UN Comtrade for bilateral trade flows of battery materials and cells (free tier with
  usage limits): https://comtradeplus.un.org/
- IRENA and IEA critical minerals reports for supply concentration figures:
  https://www.iea.org/reports/the-role-of-critical-minerals-in-clean-energy-transitions
- SNE Research and Adamas Intelligence public press releases on monthly global EV battery
  cell market share by maker (paid full reports, but market-share headlines are freely
  syndicated in trade press)

## Next bursts

- FINANCIALS: fill revenue/net income/market cap/R&D/capex for chokepoint rows first
  (CATL, BYD, BTR, Yunnan Energy/SEMCORP, Tinci, Glencore, CMOC, Asahi Kasei), citing a
  primary filing URL for each.
- RELATIONSHIPS: start from automaker 10-Ks/annual reports (Tesla, GM, VW, Toyota) and
  cell-maker annual reports (CATL, LGES, Samsung SDI) — their supplier/customer
  concentration and risk-factor sections name the edges directly.

## What would settle these

**Pre-registered 2026-07-20, before the burst, on purpose.** Each hypothesis above names the document
that would confirm or kill it. Stating the test in advance means a later burst cannot quietly redefine
what success looked like, and it starts with a shopping list instead of a search.

These are *not* `gaps.csv` rows. A gap records that we looked and the document declined to say; nothing
below has been looked for yet, and conflating "not yet tested" with "tested and undisclosed" would
destroy the one distinction the gaps model exists to protect. Rows get written when a burst runs and
comes back empty.

1. **CATL cell share.** WOULD SETTLE IT: SNE Research's monthly global EV battery installation releases give share by maker; CATL's own Shenzhen annual report carries capacity and customer concentration. Two independent sides of the same number.

2. **BYD.** WOULD SETTLE IT: the same SNE Research share table, plus BYD's HKEX annual report segment split, which is what separates cells sold to others from cells consumed by its own vehicles.

3. **China's separator cluster.** WOULD SETTLE IT: SEMCORP's and Shenzhen Senior's own Shenzhen annual reports for nameplate capacity, against UN Comtrade separator-film flows for how much of the world actually depends on it.

4. **BTR anode.** WOULD SETTLE IT: USGS Mineral Commodity Summaries (graphite) for production by country, plus BTR's Beijing SE annual report. If USGS shows graphite anode capacity outside China at scale, the flag weakens.

5. **Guangzhou Tinci electrolyte.** WOULD SETTLE IT: Tinci's Shenzhen annual report capacity and share disclosure. A single-company claim needs that company's own filing.

6. **Glencore and CMOC cobalt.** WOULD SETTLE IT: USGS Mineral Commodity Summaries (cobalt) for DRC share and producer split, corroborated by both companies' annual reports.

7. **Cathode and precursor concentration.** WOULD SETTLE IT: SNE Research and Adamas Intelligence public share releases, plus Ronbay's and Ningbo Shanshan's filings. Watch for the Korean makers, whose presence would kill the concentration claim.
