# Foundation brief — nuclear fuel cycle

Written at the FOUNDATION burst (2026-07-14). Seeds the chokepoint hypotheses this map will spend the
RELATIONSHIPS and FINANCIALS bursts trying to prove or disprove with evidence, plus the free data sources
those bursts should pull from.

## Chokepoints (ranked hypothesis, highest confidence first)

1. **The global enrichment oligopoly, with Russia the single largest node.** Only four groups run
   commercial centrifuge enrichment at scale: `Rosatom / TENEX` (Russia, roughly 40-46% of world
   capacity), `Urenco Group` (UK/Netherlands/Germany/US consortium), `Orano` (France), and `China National
   Nuclear Corporation (CNNC)` (mostly serving domestic Chinese demand). Enrichment, not mining, is the
   physically and technically hard step (gas centrifuge cascades are capital-intensive, export-controlled,
   and take years to license and build), so this is the deepest chokepoint in the cycle. Russia's share
   is now under partial pressure from the US Prohibiting Russian Uranium Imports Act (signed 2024,
   effective with case-by-case waivers through 2027-2028), which is the live test of how routable this
   layer really is.

2. **Conversion capacity is even thinner than enrichment.** Converting U3O8 into UF6 happens at only a
   handful of plants worldwide: `Orano` (Malvesi/Comurhex, France), `Honeywell International (Metropolis
   Works)` (the sole US conversion plant, Illinois), `Cameco Corporation` (Port Hope/Blind River, Canada),
   Rosatom/TVEL's Russian sites (Angarsk, Seversk), and CNNC's domestic Chinese plants. Any one of these
   going offline (as Metropolis briefly did in the 2010s, and as Western utilities feared when Russian
   conversion services were disrupted by sanctions-adjacent risk in 2022-2024) removes a meaningful slice
   of world capacity with no fast substitute, because new conversion lines take years to license.

3. **HALEU (high-assay low-enriched uranium) is close to a Rosatom monopoly, with `Centrus Energy Corp`
   the only emerging Western alternative.** Advanced/SMR reactor designs (TerraPower Natrium, X-energy,
   Kairos, etc.) need uranium enriched to 5-20% U-235, and until very recently Rosatom was the only
   supplier producing it at scale. Centrus restarted a small US HALEU cascade at Piketon, Ohio under a DOE
   contract, but volumes remain a fraction of what the advanced-reactor pipeline will need this decade;
   `Global Laser Enrichment (GLE)` and `Silex Systems Limited` are longer-shot laser-enrichment bets aimed
   partly at this gap. This is the chokepoint most likely to bind first because Western demand (new SMRs)
   is growing faster than Western HALEU supply.

4. **Fuel fabrication is chokepoint-like only for specific reactor designs, not fuel in general.**
   Western PWR/BWR fuel fabrication is reasonably competitive (`Westinghouse Electric Company`,
   `Framatome`, plus others), so it does not rank as a systemic chokepoint. But VVER-design reactors
   (the Soviet/Russian PWR variant operating across Ukraine, Hungary, Slovakia, Bulgaria, Finland and
   elsewhere) have for decades had only one qualified fuel supplier: `TVEL Fuel Company`, Rosatom's fuel
   arm. Westinghouse's post-2022 push to qualify VVER-440 and VVER-1000 fuel assemblies as a non-Russian
   alternative is the live case study for whether a fuel-fabrication chokepoint can actually be broken,
   and is worth tracking closely in the RELATIONSHIPS burst.

5. **Uranium mining is flagged as the counter-example, not a chokepoint.** `National Atomic Company
   Kazatomprom` (roughly 20% of world mined output) and `Cameco Corporation` are large, but ore is mined
   across Kazakhstan, Canada, Australia, Namibia and the US with multiple independent developers
   (`NexGen Energy`, `Paladin Energy`, `Denison Mines`, `Uranium Energy Corp`, `Energy Fuels Inc`) able to
   bring new supply online given enough lead time and price signal. No single miner or country is judged
   to have a genuinely unroutable grip on ore the way the enrichment oligopoly does on separative work.

## Free data sources

### Accounting (company filings / investor relations)
- SEC EDGAR (US filers: Centrus Energy, BWX Technologies, Uranium Energy Corp, Energy Fuels, Constellation
  Energy, Honeywell International): https://www.sec.gov/cgi-bin/browse-edgar
- SEDAR+ for Canadian filers (Cameco, NexGen Energy, Denison Mines): https://www.sedarplus.ca/
- ASX company announcements (Paladin Energy, Silex Systems): https://www.asx.com.au/markets/trade-our-cash-market/announcements
- Kazatomprom investor relations (LSE/AIX dual-listed, annual report and quarterly production reports):
  https://www.kazatomprom.kz/en/investors
- Orano investor/press pages (unlisted but publishes an annual activity/financial report):
  https://www.orano.group/en/finance
- Rosatom/TENEX/TVEL corporate and annual report pages (state corporation, publishes annual reports in
  English): https://www.rosatom.ru/en/ and https://www.tenex.ru/eng/
- CGN Mining Company Limited HKEX filings: https://www.hkexnews.hk/
- China National Nuclear Power (601985) SSE disclosure: http://www.sse.com.cn/disclosure/listedinfo/announcement/
- stockanalysis.com and similar aggregators for a quick financial snapshot before chasing the primary filing

### Politics (import bans, sanctions, national programs)
- US Prohibiting Russian Uranium Imports Act (Public Law 118-30, 2024) and DOE/NRC waiver process:
  https://www.congress.gov/bill/118th-congress/house-bill/1042 and https://www.energy.gov/ne/
- US DOE HALEU Availability Program and HALEU consortium: https://www.energy.gov/ne/haleu-availability-program
- US NRC licensing actions for enrichment, conversion and fuel-fabrication facilities:
  https://www.nrc.gov/materials/fuel-cycle-fac.html
- Euratom Supply Agency annual reports on EU enriched-uranium supply diversification and Russian-origin
  fuel dependence: https://euratom-supply.ec.europa.eu/
- US Treasury OFAC sanctions list (Rosatom-adjacent entities, though Rosatom itself is largely
  unsanctioned to preserve Western reactor fuel supply): https://ofac.treasury.gov/sanctions-list-search
- IAEA Power Reactor Information System (PRIS) for country-by-country reactor fleets and fuel-type mix:
  https://pris.iaea.org/PRIS/

### Economics (market data, production/demand, prices)
- World Nuclear Association market reports (uranium mining, enrichment, fuel fabrication overviews and
  the biennial Nuclear Fuel Report supply/demand outlook): https://world-nuclear.org/information-library
- WNA Uranium Enrichment and Conversion information pages (capacity tables by company/country):
  https://world-nuclear.org/information-library/nuclear-fuel-cycle/conversion-enrichment-and-fabrication
- US EIA uranium marketing annual report and domestic uranium data:
  https://www.eia.gov/uranium/marketing/
- IAEA/NEA "Uranium: Resources, Production and Demand" (the "Red Book," biennial, free PDF):
  https://www.oecd-nea.org/jcms/pl_14684
- UxC and TradeTech publish paid price indicators, but WNA and EIA reports summarize enough of their
  published price history for free directional tracking.

## Companies seeded

24 companies across mining, conversion, enrichment, fuel fabrication, reactor operation/vending, and
reprocessing. See `data/companies.csv`, which holds the roster and the `chokepoint = yes` flags; count
them there rather than trusting a number typed here
(Orano, Rosatom / TENEX, TVEL Fuel Company, Urenco Group, CNNC, Centrus Energy Corp, and Honeywell
International's Metropolis Works conversion plant); every flag above still needs a RELATIONSHIPS-burst
citation before it should be treated as confirmed rather than a starting hunch.

## What would settle these

**Pre-registered 2026-07-20, before the burst, on purpose.** Each hypothesis above names the document
that would confirm or kill it. Stating the test in advance means a later burst cannot quietly redefine
what success looked like, and it starts with a shopping list instead of a search.

These are *not* `gaps.csv` rows. A gap records that we looked and the document declined to say; nothing
below has been looked for yet, and conflating "not yet tested" with "tested and undisclosed" would
destroy the one distinction the gaps model exists to protect. Rows get written when a burst runs and
comes back empty.

1. **The enrichment oligopoly.** WOULD SETTLE IT: the World Nuclear Association's enrichment capacity tables by company and country, corroborated by the Euratom Supply Agency's annual report, which publishes EU enrichment purchases by origin. Two independent bodies counting the same SWU.

2. **Conversion capacity.** WOULD SETTLE IT: WNA's conversion capacity pages. The claim is that conversion is thinner than enrichment, so the test is simply whether the two capacity tables say that.

3. **HALEU near-monopoly.** WOULD SETTLE IT: US DOE and NNSA HALEU availability program documents, plus Centrus Energy's 10-K, which states its own HALEU output. If Centrus is producing at scale the monopoly claim weakens.

4. **Fuel fabrication.** WOULD SETTLE IT: WNA fuel fabrication pages plus Westinghouse and Framatome disclosures. This hypothesis is explicitly design-specific, so the test is per reactor type, not in aggregate.

5. **Uranium mining as the counter-example.** WOULD SETTLE IT: the IAEA and NEA Red Book plus the EIA uranium marketing annual report. This one is pre-registered to be DISCONFIRMED: if mining turns out to be concentrated, the map's ranking is wrong.
