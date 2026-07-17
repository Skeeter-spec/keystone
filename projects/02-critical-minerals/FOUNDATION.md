# Foundation brief — critical minerals

Written at the FOUNDATION burst (2026-07-14). Seeds the chokepoint hypotheses this map will spend the
RELATIONSHIPS and FINANCIALS bursts trying to prove or disprove with evidence, plus the free data sources
those bursts should pull from.

## Chokepoints (ranked hypothesis, highest confidence first)

1. **China's rare earth separation & refining capacity.** China performs roughly 85-90% of world rare
   earth separation regardless of where the ore was mined (Lynas ships Mt Weld concentrate to Malaysia,
   but most of the rest of the world's mixed concentrate still has nowhere else to go). Separation
   chemistry, not the mining, is the hard step, and outside China only Lynas (Malaysia), Neo Performance
   Materials (Silmet, Estonia), and Energy Fuels (White Mesa, Utah, newly licensed) run commercial-scale
   plants. `China Northern Rare Earth`, `Shenghe Resources`, and `MP Materials` anchor this row.

2. **China's magnet manufacturing base.** Even rare earth oxide separated outside China largely still
   travels to China to become a sintered NdFeB magnet; `JL MAG Rare-Earth` alone is one of the world's
   largest magnet makers. Western challengers (`MP Materials`, `USA Rare Earth`, `VAC`, `Proterial`) are
   real but small relative to Chinese sintering capacity, and Chinese producers hold cost and scale
   advantages that are hard to route around inside a five-year horizon.

3. **China's export licensing on gallium, germanium and graphite.** Since August 2023 (gallium/germanium)
   and later graphite-related controls, China has used export permits as a lever independent of physical
   scarcity — the ore exists elsewhere, but China refines the overwhelming majority of germanium
   (`Yunnan Chihong Zinc & Germanium` is a top domestic producer) and dominates graphite anode processing.
   `Syrah Resources` (Mozambique ore, Louisiana anode plant) is one of the only non-Chinese natural
   graphite-to-anode chains and is worth tracking closely as the counter-example.

4. **DRC cobalt ore into Chinese refining.** The Democratic Republic of Congo supplies roughly 70% of
   mined cobalt, but the ore overwhelmingly flows to Chinese refiners for conversion to battery-grade
   sulfate and precursor cathode material. `CMOC Group` (mining) and `Zhejiang Huayou Cobalt` (refining)
   sit on either side of that ore-to-chemical handoff; `Glencore` is the largest non-Chinese miner/trader
   with real leverage over where DRC ore actually goes.

5. **Lithium refining/conversion concentration.** Mining is more geographically diverse (Australia hard
   rock, Chile/Argentina brine, emerging US projects), but conversion into battery-grade lithium
   carbonate/hydroxide is concentrated in a handful of players — `Albemarle`, `SQM`, `Ganfeng Lithium`,
   and `Tianqi Lithium` — with China holding the largest share of global conversion capacity even when the
   spodumene itself was mined in Australia.

## Free data sources

### Accounting (company filings / investor relations)
- SEC EDGAR (US filers: MP Materials, Albemarle, Energy Fuels, USA Rare Earth, Lithium Americas, Vale
  ADR): https://www.sec.gov/cgi-bin/browse-edgar
- ASX company announcements (Lynas, Pilbara Minerals/PLS Group, Iluka, BHP, Rio Tinto, Syrah Resources):
  https://www.asx.com.au/markets/trade-our-cash-market/announcements
- HKEX / SSE / SZSE disclosure portals for Chinese dual/A-share filers (Shenghe 600392, China Northern
  Rare Earth 600111, JL Mag 300748/06680, Ganfeng 002460/1772, Tianqi 002466/9696, CMOC 603993/03993,
  Zhejiang Huayou Cobalt 603799, Yunnan Chihong 600497): https://www.hkexnews.hk/ and
  http://www.sse.com.cn/disclosure/listedinfo/announcement/ and http://www.szse.cn/disclosure/listed/
- Company investor relations pages for non-EDGAR filers (Glencore, Rio Tinto, Umicore, Nornickel, SQM,
  Vacuumschmelze/Proterial where disclosed by parent)
- stockanalysis.com and similar aggregators for a quick financial snapshot before chasing the primary
  filing

### Politics (export controls, sanctions, strategic policy)
- US Bureau of Industry and Security (BIS) Entity List and export control rules:
  https://www.bis.gov/entity-list
- US OFAC sanctions list (relevant to Russian entities like Nornickel):
  https://ofac.treasury.gov/sanctions-list-search
- China Ministry of Commerce (MOFCOM) export control announcements (gallium, germanium, graphite,
  rare earth licensing): http://www.mofcom.gov.cn/ (English notices often mirrored by Reuters/S&P Global)
- EU Critical Raw Materials Act (CRMA) strategic projects and benchmarks:
  https://single-market-economy.ec.europa.eu/sectors/raw-materials/areas-specific-interest/critical-raw-materials/critical-raw-materials-act_en
- US Department of Energy loan and grant announcements (Lithium Americas, VAC/magnet reshoring):
  https://www.energy.gov/lpo/

### Economics (supply/demand, trade flows, commodity data)
- USGS Mineral Commodity Summaries (annual, free PDF, the standard reference for reserves/production by
  country for every mineral in this map): https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries
- USGS National Minerals Information Center commodity statistics:
  https://www.usgs.gov/centers/national-minerals-information-center
- IEA Critical Minerals Data Explorer and annual Critical Minerals Outlook:
  https://www.iea.org/data-and-statistics/data-tools/critical-minerals-data-explorer
- UN Comtrade for bilateral trade flows (ore, concentrate, refined metal HS codes):
  https://comtrade.un.org/
- US Census Bureau / USITC trade data for US import/export figures:
  https://www.census.gov/foreign-trade/statistics/product/

## Companies seeded

27 companies across mining, refining/separation, magnet-making, battery chemicals, recycling, and
trading. See `data/companies.csv`. 16 are flagged `chokepoint = TRUE` at this hypothesis stage; every
flag above still needs a RELATIONSHIPS-burst citation before it should be treated as confirmed rather
than a starting hunch.
