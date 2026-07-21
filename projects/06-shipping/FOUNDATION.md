# Foundation brief: Maritime shipping

Written at the FOUNDATION burst. Chokepoint hypotheses and free data sources to guide the FINANCIALS and RELATIONSHIPS bursts that follow.

## A note on infrastructure nodes

`data/companies.csv` mixes real companies with a handful of non-company **infrastructure nodes**: the two canal authorities (Suez, Panama), four straits with no single governing authority (Hormuz, Malacca, Bab-el-Mandeb) or with one (Bosphorus/Turkey), and the London P&I insurance pool. These rows have blank ticker/exchange and will never get financials filled in during the FINANCIALS burst — they are chokepoints in their own right, not companies, and are flagged as such in their `notes` field. This is the one Keystone map where the biggest bottlenecks are physical geography, not corporate market share, so they belong in the graph even though they don't file annual reports.

## (a) Chokepoints ranked, with rationale

Ranked roughly by "how completely does losing this node stop the flow of goods," highest first. All are flagged `chokepoint=yes` in companies.csv except the three named alliances, which are discussed here but not flagged (see rationale below).

### Geographic (canals & straits)

1. **Suez Canal (Suez Canal Authority, Egypt)** — the Asia-Europe shortcut. Only alternative is the Cape of Good Hope, roughly 10-14 days longer and far more fuel. Egyptian state monopoly since 1956. The 2021 Ever Given grounding (single ship, six days) and the 2023-2025 Houthi-driven exodus of container traffic both proved real-world fragility, not just theoretical risk.
2. **Panama Canal (Panama Canal Authority / ACP)** — the Atlantic-Pacific shortcut, critical for US East Coast-Asia trade and US grain/LNG exports. 2023-2024 drought forced draft restrictions and cut daily transits, showing a *second* failure mode (water supply, not politics or attacks) that a purely corporate chokepoint could never have. Also a live 2025-2026 US political flashpoint (talk of "reclaiming" the canal, pressure over Hutchison Ports' Balboa/Cristobal terminal stakes).
3. **Strait of Hormuz (Iran/Oman)** — no governing authority at all, just international transit-passage law and naval patrols; roughly a fifth of world oil and a third of world LNG passes through a ~33km-wide gap that Iran has repeatedly threatened to close. Ranked just under Suez/Panama because it has never actually been closed, but the concentration of energy flows makes disruption here economically larger per day than either canal.
4. **Bab-el-Mandeb Strait (Yemen/Djibouti)** — feeds the Suez Canal from the Indian Ocean side; the 2023-2025 Houthi attacks are the closest thing to a live natural experiment this map has: losing this strait functionally closed Suez too, because ships had no reason to transit the canal if they still had to run the Bab-el-Mandeb gauntlet to reach it.
5. **Strait of Malacca (Indonesia/Malaysia/Singapore)** — an estimated 25%+ of world seaborne trade transits this strait between the Indian Ocean and South China Sea. Jointly policed (Malacca Strait Patrol) rather than governed by one state, which somewhat de-risks it politically compared to Hormuz, but the physical alternatives (Lombok, Sunda, Makassar) are longer and shallower, ill-suited to the largest ships.
6. **Bosphorus Strait (Turkey)** — the outlier in this list: it *does* have a single sovereign gatekeeper. The 1936 Montreux Convention gives Turkey the legal right to regulate and, in wartime, close the strait, which Ankara partially exercised after 2022 (restricting some warship and tanker transits tied to the Russia-Ukraine war). Ranked last because Black Sea trade volumes are smaller than the other five, but it is the cleanest example of a single-actor geographic chokepoint on this map.

### Industrial / corporate

7. **Shipbuilding concentration — China CSSC Holdings, HD Hyundai Heavy Industries, Samsung Heavy Industries, Hanwha Ocean** — between them, China and South Korea build the overwhelming majority of the world's large commercial vessels (China alone over half of gross tonnage in recent years), with multi-year order backlogs. Losing any one yard doesn't stop shipping today, but it constrains how fast the *entire* liner and tanker fleet can be replaced, decarbonized, or surged in a crisis — a slow-moving but very real chokepoint, which is why all four get `chokepoint=yes` individually rather than being treated as freely substitutable competitors.
8. **London-coordinated P&I insurance (International Group of P&I Clubs)** — a pooling and reinsurance agreement among the 12 mutual clubs that together cover roughly 90% of world merchant tonnage for pollution, cargo, crew and collision liability. A ship without valid P&I cover cannot get port access, canal transit, or classification renewal — this is a soft-power chokepoint that surfaced as real leverage in the sanctions fight over Russia's post-2022 "shadow fleet" (Western/G7 insurers refusing cover as an enforcement tool).
9. **The three liner alliances (Ocean Alliance: CMA CGM/COSCO/Evergreen/OOCL; Gemini Cooperation: Maersk/Hapag-Lloyd; Premier Alliance: ONE/Yang Ming/HMM)** — discussed but *not* individually flagged `chokepoint=yes`, following the same logic as "a large liner is not automatically a chokepoint": a shipper can move cargo to a rival alliance or to independent MSC (which now operates at alliance scale alone, >20% of global capacity, outside all three). What's worth tracking is the *systemic* fact that these three alliances plus MSC now control 80%+ of deployed capacity on the major East-West trades, which concentrates scheduling and pricing power even though no single carrier is irreplaceable. If a future RELATIONSHIPS burst finds evidence that alliance vessel-sharing agreements create real single points of failure (e.g. a shared hub terminal, a single dominant slot-charter), promote this to `yes`.

## (b) Free data sources

### Accounting (listed liner filings / investor relations)

- A.P. Moller-Maersk investor relations (Annual Report, interim reports): https://investor.maersk.com/
- Hapag-Lloyd investor relations: https://www.hapag-lloyd.com/en/company/ir.html
- COSCO Shipping Holdings HKEX filings: https://www.hkexnews.hk/ (search "COSCO SHIPPING Holdings", stock code 1919)
- ZIM Integrated Shipping Services SEC filings (foreign private issuer, files 20-F/6-K): https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001654126
- HMM investor relations (Korean and English financial statements): https://www.hmm21.com/ir/main
- Evergreen Marine (Taiwan) Market Observation Post System filings: https://mops.twse.com.tw/
- Yang Ming Marine Transport MOPS filings: https://mops.twse.com.tw/
- HD Hyundai Heavy Industries, Samsung Heavy Industries, Hanwha Ocean: DART (Korea's EDGAR equivalent) https://dart.fss.or.kr/
- China CSSC Holdings: Shanghai Stock Exchange disclosure site http://www.sse.com.cn/
- Kuehne+Nagel, DSV investor relations pages (Swiss/Danish equivalents of 10-Ks)

### Politics (trade policy, sanctions, regulation)

- USTR Section 301 investigation into China's targeting of maritime, logistics, and shipbuilding sectors (2024-2025 action, port fees on Chinese-built/operated vessels): https://ustr.gov/issue-areas/enforcement/section-301-investigations
- OFAC sanctions lists and shadow-fleet designations (Russian oil tanker "dark fleet"): https://ofac.treasury.gov/sanctions-list-service
- International Maritime Organization (IMO) — conventions, Red Sea security notices, decarbonization rules: https://www.imo.org/
- Suez Canal Authority official statistics and notices: https://www.suezcanal.gov.eg/English/Navigation/Pages/NavigationStatistics.aspx
- Panama Canal Authority (ACP) statistics: https://pancanal.com/en/statistics/

### Economics (industry-wide sizing and indices)

- UNCTAD Review of Maritime Transport (annual, free PDF): https://unctad.org/rmt
- Clarksons Research public notes and press releases (shipbuilding orderbook, fleet stats): https://www.clarksons.com/research/
- Drewry World Container Index and other public freight-rate indices: https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry
- Baltic Exchange indices (BDI, BCI etc., headline figures often free via news coverage): https://www.balticexchange.com/
- Lloyd's List (maritime trade press, some free articles): https://www.lloydslist.com/

## Starter roster verification notes

All 23 starter names were located and included, plus a small logistics layer (Kuehne+Nagel, DSV) and the marine-insurance/classification layer (Lloyd's Register, International Group of P&I Clubs) so every layer in the README onion has at least one concrete node. Key verification findings from this burst:

- Triton International (container leasing) was taken private by Brookfield Infrastructure in a completed September 2023 deal; no longer NYSE-listed. Kept in the roster with blank ticker and a note.
- China Shipbuilding Industry Co (601989.SS) merged into China CSSC Holdings (600150.SS) in August 2025; the roster uses the surviving listed entity.
- The liner alliance lineup changed in 2025: Maersk and Hapag-Lloyd left the old 2M/THE Alliance structure to form the Gemini Cooperation; Ocean Alliance (CMA CGM/COSCO/Evergreen/OOCL) and Premier Alliance (ONE/Yang Ming/HMM) are the other two. MSC remains outside all three, operating at alliance scale alone.
- DP World and PSA International are both state/sovereign-fund owned and not separately listed (Dubai World; Temasek).

## What would settle these

**Pre-registered 2026-07-20, before the burst, on purpose.** Each hypothesis above names the document
that would confirm or kill it. Stating the test in advance means a later burst cannot quietly redefine
what success looked like, and it starts with a shopping list instead of a search.

These are *not* `gaps.csv` rows. A gap records that we looked and the document declined to say; nothing
below has been looked for yet, and conflating "not yet tested" with "tested and undisclosed" would
destroy the one distinction the gaps model exists to protect. Rows get written when a burst runs and
comes back empty.

1. **Suez Canal.** WOULD SETTLE IT: the Suez Canal Authority's own monthly traffic and revenue statistics, against UNCTAD's Review of Maritime Transport for what share of world trade that represents.

2. **Panama Canal.** WOULD SETTLE IT: the Panama Canal Authority's monthly transit numbers and draft-restriction advisories. The 2023-24 drought restrictions are the natural experiment: transits fell and the world routed around it or did not.

3. **Strait of Hormuz.** WOULD SETTLE IT: the US EIA's world oil transit chokepoints series for barrels per day, plus UNCTAD RMT. There is no canal authority here, so the volume estimate is the only test.

4. **Bab-el-Mandeb.** WOULD SETTLE IT: the same EIA transit series, and Suez Canal Authority traffic, since a collapse here shows up as a Suez collapse. The 2024 Red Sea diversions are the natural experiment.

5. **Strait of Malacca.** WOULD SETTLE IT: EIA transit estimates and UNCTAD RMT. The specific test is whether the claimed alternatives (Lombok, Sunda) carry meaningful volume or are theoretical.

6. **Bosphorus.** WOULD SETTLE IT: Turkish straits transit statistics. This one has a single sovereign authority, so its own numbers are the primary source.

7. **Shipbuilding concentration.** WOULD SETTLE IT: Clarksons Research public orderbook notes, which give share by yard and country. The test is whether the orderbook is as concentrated as the capacity.

8. **P&I insurance.** WOULD SETTLE IT: the International Group of P&I Clubs' own published annual review and pooling agreement, which state the share of world tonnage covered.

9. **Liner alliances.** WOULD SETTLE IT: the carriers' own alliance announcements plus UNCTAD's liner shipping connectivity index. The 2025 Gemini reshuffle is the test of how fixed these blocs really are.
