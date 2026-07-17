# Foundation brief — food and fertilizer

Written at the FOUNDATION burst (2026-07-14). Seeds the chokepoint hypotheses this map will spend the
RELATIONSHIPS and FINANCIALS bursts trying to prove or disprove with evidence, plus the free data sources
those bursts should pull from.

## Chokepoints (ranked hypothesis, highest confidence first)

1. **Morocco's phosphate rock reserves (OCP Group).** Morocco holds roughly 70% of the world's known
   phosphate rock reserves, and state-owned `OCP Group` is the dominant miner and processor of that rock
   into phosphate fertilizer. Unlike potash or nitrogen, there is no comparable second country to route
   around Morocco's reserve base over any multi-decade horizon; this is the single hardest physical
   chokepoint in the food/fertilizer chain.

2. **Belarus + Russia potash concentration.** Three producers — `Belaruskali` (Belarus, state-owned),
   `Uralkali` (Russia, MOEX: URKA, majority controlled via Uralchem), and `Nutrien` (Canada, NYSE/TSX:
   NTR, the world's largest single potash producer) — account for the large majority of globally traded
   potash. Since 2022, EU/US sanctions, the closure of the Lithuanian rail line to Klaipeda, and
   Belarusian/Russian export licensing have repeatedly disrupted the Belarus+Russia leg specifically,
   making that half of the trio a live supply chokepoint rather than a diversified market.

3. **Nitrogen production tied to natural gas.** Ammonia/urea synthesis (Haber-Bosch) is gas-intensive, so
   nitrogen fertilizer cost and availability move with regional gas prices and gas access. `CF Industries`
   (US, advantaged by cheap shale gas) and `Yara International` (Norway, exposed to European gas prices)
   anchor this hypothesis; the 2021-2023 European gas price spike that curtailed Yara's own ammonia output
   is the clearest evidence this chokepoint is real, not theoretical.

4. **The seed and agrochemical "Big Four" oligopoly.** `Bayer`, `Corteva`, `Syngenta Group` (wholly owned
   by China's Sinochem Holdings), and `BASF` between them hold the large majority of the world's
   commercial seed genetics (traits, germplasm) and crop protection chemistry (herbicides, insecticides,
   fungicides). Farmers in most major grain-growing regions have very few sources of patented seed and
   matched agrochemical outside this group.

5. **The ABCD grain traders (plus COFCO).** `Archer-Daniels-Midland`, `Bunge Global` (which absorbed
   Viterra on July 2, 2025), `Cargill` (private), and `Louis Dreyfus Company` (private) — the historic
   "ABCD" quartet — own the elevators, rail, barge and port infrastructure that most of the world's traded
   grain and oilseed physically moves through, along with the market information advantage that comes with
   it. China's state-owned `COFCO International` (built via the Noble Agri and Nidera acquisitions) has
   grown into a fifth top-tier trader and is increasingly described as "ABCD+C," but is not yet as
   structurally entrenched as the original four; it is tracked here as `chokepoint = FALSE` pending
   evidence of comparable market share.

Companies not on this list — Mosaic, ICL Group, K+S, PhosAgro, EuroChem, OCI N.V., Uralchem, Compass
Minerals, FMC, Wilmar International, Olam Agri — are real, sizeable players but each has substitutes or
is small enough relative to its category that flagging it `chokepoint = TRUE` would overstate how
irreplaceable any single one of them is. A large farm-belt or fertilizer company is not automatically a
chokepoint; the flag is reserved for nodes the rest of the chain genuinely cannot route around.

## Free data sources

### Accounting (company filings / investor relations)
- SEC EDGAR (US filers: Nutrien, Mosaic, CF Industries, Corteva, FMC, ADM, Bunge, Compass Minerals):
  https://www.sec.gov/cgi-bin/browse-edgar
- Company investor relations pages for non-EDGAR filers (Yara, ICL Group also files 20-F with SEC, K+S,
  Bayer, BASF, OCI N.V.)
- Moscow Exchange (MOEX) disclosure for Russian filers (PhosAgro PHOR, Uralkali URKA):
  https://www.moex.com/en/listing/discl-list.aspx
- Singapore Exchange (SGX) filings for Wilmar International and Olam Group:
  https://www.sgx.com/securities/company-announcements
- OCP Group publishes voluntary annual/sustainability reports (not SEC/SGX/MOEX filed, state-owned,
  Morocco): https://www.ocpgroup.ma/investors
- stockanalysis.com and similar aggregators for a quick financial snapshot before chasing the primary
  filing

### Politics (export controls, sanctions, trade policy)
- US OFAC Specially Designated Nationals (SDN) list and sanctions programs relevant to Belarus and Russia
  potash/fertilizer entities: https://ofac.treasury.gov/sanctions-list-search
- EU sanctions map (Belarus and Russia regimes, including the Belaruskali/Belarusian Potash Company
  listings): https://www.sanctionsmap.eu/
- US Bureau of Industry and Security (BIS) export control rules:
  https://www.bis.gov/entity-list
- India Ministry of Commerce and other importer-country fertilizer/food export-import policy notices
  (India has repeatedly restricted rice, wheat and onion exports; DAP/urea import subsidy policy also
  matters here): https://commerce.gov.in/trade-old/international-trade/press-release/
- Indonesian and Argentine export tax/quota announcements for palm oil, soybeans and grain (affects
  Wilmar and the ABCD traders) — tracked via Reuters/S&P Global Commodity Insights coverage in the absence
  of a single free government portal

### Economics (supply/demand, trade flows, commodity prices)
- USDA World Agricultural Supply and Demand Estimates (WASDE), monthly, free: https://www.usda.gov/oce/commodity/wasde
- USDA Production, Supply and Distribution (PSD) online database (country-level grain/oilseed
  stocks and trade): https://apps.fas.usda.gov/psdonline/
- FAO Food Price Index, monthly: https://www.fao.org/worldfoodsituation/foodpricesindex/en/
- World Bank Commodity Markets ("Pink Sheet") monthly price data, including fertilizers:
  https://www.worldbank.org/en/research/commodity-markets
- International Fertilizer Association (IFA) statistics on nitrogen/phosphate/potash production, trade
  and consumption: https://www.ifastat.org/
- USGS Mineral Commodity Summaries (phosphate rock and potash reserves/production by country):
  https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries
- UN Comtrade for bilateral trade flows (fertilizer and grain HS codes): https://comtrade.un.org/

## Companies seeded

26 companies across feedstock/mining, N/P/K fertilizer production, seed and agrochemicals, and grain
trading/processing. See `data/companies.csv`. 14 rows are flagged `chokepoint = TRUE` at this hypothesis
stage, grouped under the 5 ranked categories above (phosphate reserves, Belarus+Russia potash, gas-linked
nitrogen, the seed/agrochem Big Four, and the ABCD grain traders); every flag still needs a
RELATIONSHIPS-burst citation before it should be treated as confirmed rather than a starting hunch.
