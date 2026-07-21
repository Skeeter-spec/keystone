# Foundation brief — Payment rails

Educational industry research. Not investment or financial advice.

## Chokepoints (ranked)

Discipline: `chokepoint=yes` is reserved for nodes the system genuinely cannot route around, not
merely large or famous companies. Six nodes qualify at foundation.

1. **Visa & Mastercard (duopoly)** — Together the two networks clear the large majority of the
   world's card transactions. Any bank, merchant, or country that wants global card acceptance has
   to plug into one or both; there is no third network with comparable reach. Amex and Discover
   prove the point in reverse — they are large, well-known brands, but neither is a chokepoint
   because merchants and cardholders can and do route around them.
2. **SWIFT** — The de facto sole global standard for interbank payment messaging. It does not move
   money itself, only instructions, but almost every cross-border bank transfer is coordinated
   through it. Its chokepoint status is demonstrated in practice: cutting a country's banks off from
   SWIFT (used against major Russian banks in 2022 and against Iranian banks under earlier sanctions
   regimes) functions as a de facto financial blockade. That a messaging cooperative can be wielded
   as a geopolitical weapon is the clearest evidence that no substitute exists at the scale needed.
3. **UnionPay** — China's domestic card switch is mandatory for RMB-denominated card transactions;
   no competing domestic network is permitted to operate at scale inside China. By transaction
   value it is also the largest card network in the world, making it a chokepoint both domestically
   (monopoly) and globally (unavoidable for anyone doing business with Chinese cardholders).
4. **NPCI / UPI (India)** — The National Payments Corporation of India is a nonprofit utility
   owned by Indian banks and the RBI that operates UPI, now the rail that essentially all Indian
   retail digital payments route through. Like UnionPay, this is a government-anchored domestic
   monopoly rather than a competitive market outcome.
5. **Federal Reserve / Fedwire** — The literal end of the line for US-dollar settlement. Every
   private USD rail (CHIPS, card networks, ACH, correspondent banking) ultimately settles through
   central-bank reserve accounts, and only the Fed can create those. This is a sovereign monopoly,
   not a market position, and it has no private alternative by design.
6. *(Runner-up, not flagged yes)* **The Clearing House / CHIPS** — handles the bulk of large-value
   USD interbank clearing by dollar value, and is privately run by the largest US banks, but Fedwire
   is a real, functioning alternative for final settlement, so CHIPS does not meet the "cannot route
   around" bar the way Fedwire does. Worth re-checking as the graph fills in — if CHIPS volume
   concentration deepens relative to Fedwire, this could flip to yes in a later burst.

Explicitly **not** chokepoints, despite scale or fame: American Express and Discover/Capital One
(substitutable, minority-share networks); Fiserv, FIS, Global Payments, and other processors
(competitive, multi-vendor market); Stripe and Adyen (large but merchants multi-home); PayPal, Wise,
Zelle (convenient, not structurally unavoidable); Circle/USDC and Tether/USDT (dominant today, but a
competitive and fast-changing stablecoin field, and regulated entrants are arriving).

## Free data sources

### Accounting (company financials — SEC filings, investor relations)

- SEC EDGAR full-text and filing search (10-K/10-Q/8-K for all US filers: Visa, Mastercard, Amex,
  Capital One, Fiserv, FIS, Global Payments, PayPal, Block, ACI Worldwide, Marqeta, JPMorgan,
  Circle): https://www.sec.gov/cgi-bin/browse-edgar and https://www.sec.gov/edgar/search/
- Visa Investor Relations (10-K, earnings decks): https://investor.visa.com
- Mastercard Investor Relations: https://investor.mastercard.com
- PayPal Investor Relations: https://investor.pypl.com
- Block Investor Relations: https://investors.block.xyz
- Circle Internet Group Investor Relations (post-2025 IPO): https://investors.circle.com
- Adyen annual reports (Dutch filer, reports in EUR): https://www.adyen.com/investor-relations
- Worldline universal registration documents (AMF, France): https://worldline.com/en/home/investors
- Nexi annual financial reports (Borsa Italiana / Euronext Milan filer):
  https://www.nexigroup.com/en/investors/
- Wise plc annual report and results (Nasdaq primary listing from 2026-05-11, UK Companies House
  filings historically): https://wise.com/investor-relations
- stockanalysis.com and companiesmarketcap.com for quick market-cap/revenue snapshots
  (secondary/tertiary source, cross-check against the primary filing)

### Politics (sanctions, antitrust, central bank / CBDC policy)

- US Treasury OFAC sanctions list and SWIFT-related sanctions actions:
  https://ofac.treasury.gov/sanctions-list-search
- SWIFT's own statements on compliance with sanctions regimes:
  https://www.swift.com/about-us/legal/compliance-swift
- US DOJ antitrust division (card-network and processor merger reviews, e.g., Capital
  One/Discover): https://www.justice.gov/atr
- Federal Reserve press releases on bank merger approvals (Capital One/Discover order, April 2025):
  https://www.federalreserve.gov/newsevents/pressreleases.htm
- Bank for International Settlements Committee on Payments and Market Infrastructures (CPMI) —
  covers cross-border payment policy, sanctions-related payment system reports, and CBDC surveys:
  https://www.bis.org/cpmi/
- Central bank CBDC trackers: Atlantic Council CBDC tracker (free, public):
  https://www.atlanticcouncil.org/cbdctracker/
- RBI (Reserve Bank of India) press releases on UPI and NPCI governance:
  https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx
- People's Bank of China / State Council notices on UnionPay and domestic clearing policy (English
  summaries via PBOC site): http://www.pbc.gov.cn/en/

### Economics (industry structure, volumes, and macro cycle)

- BIS CPMI "Red Book" statistics on payment, clearing, and settlement systems across major
  economies (free, downloadable): https://www.bis.org/cpmi/publ/index.htm and the CPMI statistics
  portal at https://data.bis.org/topics/CPMI
- Federal Reserve triennial "Federal Reserve Payments Study" (US check/ACH/card volumes):
  https://www.federalreserve.gov/paymentsystems/fr-payments-study.htm
- Nilson Report public press releases and rankings (subscription report, but summary rankings and
  market-share figures are periodically released free via press release):
  https://nilsonreport.com/publication_newsletter_archive_issue.php
- NPCI public UPI transaction statistics (monthly volumes/values, free):
  https://www.npci.org.in/statistics
- CLS Group (FX settlement utility) public volume statistics:
  https://www.cls-group.com/about/cls-by-numbers/
- World Bank Global Findex database (financial inclusion / payment access, free):
  https://www.worldbank.org/en/publication/globalfindex

## What would settle these

**Pre-registered 2026-07-20, before the burst, on purpose.** Each hypothesis above names the document
that would confirm or kill it. Stating the test in advance means a later burst cannot quietly redefine
what success looked like, and it starts with a shopping list instead of a search.

These are *not* `gaps.csv` rows. A gap records that we looked and the document declined to say; nothing
below has been looked for yet, and conflating "not yet tested" with "tested and undisclosed" would
destroy the one distinction the gaps model exists to protect. Rows get written when a burst runs and
comes back empty.

1. **Visa and Mastercard duopoly.** WOULD SETTLE IT: both companies' 10-Ks for purchase volume, against Nilson Report public rankings for the share not captured by either.

2. **SWIFT.** WOULD SETTLE IT: SWIFT's own published monthly traffic statistics, plus the BIS CPMI Red Book. The live test is whether CIPS and SPFS volumes are growing fast enough to matter.

3. **UnionPay.** WOULD SETTLE IT: the BIS CPMI Red Book China chapter and the PBoC's payment system reports, which publish domestic card switch volumes.

4. **NPCI and UPI.** WOULD SETTLE IT: NPCI's own public UPI transaction statistics, published monthly and free. The test is whether any competing rail has non-trivial share.

5. **Federal Reserve and Fedwire.** WOULD SETTLE IT: the Federal Reserve Payments Study and published Fedwire funds transfer statistics. This is close to definitionally true, so the real question is whether it belongs as a chokepoint at all.
