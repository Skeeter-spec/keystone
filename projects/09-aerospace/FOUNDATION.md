# Foundation brief: Aerospace

Written at the FOUNDATION burst. Chokepoint hypotheses and free data sources to guide the FINANCIALS and RELATIONSHIPS bursts that follow.

## (a) Chokepoints ranked, with rationale

Ranked roughly by "how completely does losing this node stop the flow of finished aircraft," highest first. `chokepoint=yes` is set on 8 rows in `data/companies.csv` (Boeing, Airbus, GE Aerospace, Rolls-Royce, RTX, VSMPO-Avisma, Precision Castparts, Howmet Aerospace) — slightly above the usual 4-7 target because two of the categories below are themselves duopolies where both members independently qualify, mirroring how Boeing and Airbus are both flagged.

1. **Boeing (BA) and Airbus (AIR) — large civil airframe duopoly.** No third manufacturer builds and certifies 150+ seat jetliners at commercial scale. Airlines cannot route around either one for large narrowbody/widebody orders; COMAC's C919 has not broken this duopoly as of 2026 and still leans on Western engines/avionics. Boeing's completed (Dec 8, 2025) acquisition of Spirit AeroSystems concentrates the 737/787 fuselage bottleneck inside Boeing itself.

2. **Jet-engine oligopoly — GE Aerospace (GE, via the 50/50 CFM International JV with Safran), Rolls-Royce (RR.), and RTX's Pratt & Whitney.** Exactly three companies make large civil jet engines, and specific programs are sole-sourced to one of them (CFM56/LEAP on most 737s and many A320s; Pratt & Whitney's geared turbofan sole-source on the A220; Rolls-Royce Trent variants on many 787/A350 builds). Losing any one of the three would ground programs with no substitute powerplant available on short notice. Safran co-owns the CFM chokepoint but is not separately flagged, to avoid double-counting the same joint venture.

3. **Aerospace-grade titanium — Russia's VSMPO-Avisma (MOEX: VSMO), with Timet and ATI (NYSE: ATI) as the Western hedge.** VSMPO-Avisma historically supplied roughly a third of world aerospace titanium, with direct sourcing/JV ties to both Boeing and Airbus. Western buyers have been derisking since the 2022 invasion of Ukraine and partial sanctions on parent Rostec, but global titanium sponge/ingot melt capacity is limited and full substitution takes years — this is a live, not theoretical, chokepoint. Timet and ATI are the qualified Western alternatives and are not themselves flagged, since they are the release valve rather than the bottleneck.

4. **Single-source structural castings and forgings — Precision Castparts (private, Berkshire Hathaway) and Howmet Aerospace (HWM).** Between them these two firms are the qualified source for many of the largest titanium and superalloy structural castings and forgings used in both Boeing and Airbus airframes and in most jet engines. Part qualification for castings of this size and complexity takes years, so airlines and OEMs cannot simply switch suppliers if either firm has a quality escape or capacity problem (as Boeing/Airbus programs experienced with forging and casting shortages in 2023-2024). Precision Castparts will likely never get financials filled in the FINANCIALS burst (private since 2016); it stays in the roster anyway because it is economically real, following the precedent set in the shipping map for unlisted/state-owned infrastructure nodes.

5. **Spirit AeroSystems — fuselage bottleneck (not separately flagged).** For decades the sole builder of the 737 fuselage and major 767/777/787 structures out of a single Wichita, KS facility — a genuine single-point-of-failure risk (a strike or quality escape there has repeatedly disrupted Boeing's whole production line). Acquired by Boeing in a deal completed Dec 8, 2025 (~$8.3B including debt); the Airbus-linked sites/programs (A220/A320/A350 structures in the US, Morocco, France, UK) were concurrently divested to Airbus per an FTC order. Kept as its own row and discussed here because the facility-level physical bottleneck persists regardless of which OEM owns it, but not flagged `chokepoint=yes` in the CSV since that risk is now folded into Boeing's own row.

Explicitly **not** flagged despite being large: Embraer and COMAC (substitutable at their scale), Honeywell/Thales/Leonardo/BAE (avionics/defense electronics has multiple qualified suppliers), TransDigm (a portfolio of many small proprietary-part monopolies rather than one chain-wide node — "big is not the same as chokepoint"), HEICO and the lessors (competitive, substitutable layers), and the defense primes Lockheed Martin/Northrop Grumman/General Dynamics (each dominant in a narrow program — F-35, B-21, Gulfstream — but that is a niche, not a chain-wide bottleneck; Lockheed's F-35 monopoly is the strongest candidate to promote later if the RELATIONSHIPS burst shows allied air forces truly have no substitute).

## (b) Free data sources

### Accounting (SEC filings / investor relations)

- SEC EDGAR full-text search and company filings (Boeing, RTX, GE Aerospace, Lockheed Martin, Northrop Grumman, General Dynamics, Howmet Aerospace, TransDigm, HEICO, ATI, AerCap, Air Lease, Embraer as a 20-F foreign filer): https://www.sec.gov/cgi-bin/browse-edgar
- Boeing investor relations (10-K, quarterly deliveries/orders reports): https://investors.boeing.com/
- RTX Corporation investor relations: https://www.rtx.com/investors
- GE Aerospace investor relations: https://www.geaerospace.com/investor-relations
- Airbus investor relations (annual report, order book, delivery figures — French issuer, not SEC): https://www.airbus.com/en/investors
- Safran investor relations: https://www.safran-group.com/investors
- Rolls-Royce Holdings investor relations (LSE-listed, UK annual report/RNS filings): https://www.rolls-royce.com/investors.aspx
- MTU Aero Engines investor relations (German Wertpapierhandelsgesetz filings): https://www.mtu.de/investor-relations/
- Embraer investor relations (dual SEC 20-F + CVM/B3 filer): https://ri.embraer.com.br/
- Moscow Exchange disclosure for VSMPO-Avisma (MOEX: VSMO), limited given sanctions-era disclosure gaps: https://www.moex.com/en/issue.aspx?board=TQBR&code=VSMO

### Politics (export controls, sanctions, defense budgets)

- US State Department Directorate of Defense Trade Controls — ITAR regulations and the US Munitions List: https://www.pmddtc.state.gov/
- US Commerce Department Bureau of Industry and Security — export control classifications and the Entity List (relevant to VSMPO-Avisma/Rostec-linked sanctions): https://www.bis.gov/
- US Treasury OFAC sanctions list search (Rostec, Russian defense-industrial sanctions): https://ofac.treasury.gov/sanctions-list-service
- US Department of Defense budget documents (comptroller "Green Book" and program-level budget justifications for F-35, B-21, etc.): https://comptroller.defense.gov/Budget-Materials/
- SIPRI Arms Industry Database (public summary tables on the largest defense contractors): https://www.sipri.org/databases/armsindustry
- FTC press releases and consent order on the Boeing-Spirit AeroSystems merger and Airbus divestiture: https://www.ftc.gov/news-events/news/press-releases

### Economics (order books, traffic, market sizing)

- Boeing Commercial Market Outlook (annual, free PDF): https://www.boeing.com/commercial/market/commercial-market-outlook
- Airbus Global Market Forecast (annual, free PDF): https://www.airbus.com/en/products-services/commercial-aircraft/market
- Boeing monthly/quarterly orders and deliveries data: https://www.boeing.com/commercial/#/orders-deliveries
- Airbus monthly orders and deliveries data: https://www.airbus.com/en/newsroom/press-releases
- IATA economic and traffic reports (free summaries; some detail paywalled): https://www.iata.org/en/publications/economics/
- Teal Group public commentary and press-cited market-share estimates (used for civil/business aviation forecasting context, often reported second-hand in trade press since the full reports are paid): https://www.tealgroup.com/

## Starter roster verification notes

All 24 starter names were located and included, plus Timet (Precision Castparts' titanium subsidiary) and Air Lease Corporation (second listed pure-play lessor) to round out the titanium and lessor sub-layers, for 26 total rows. Key verification findings from this burst:

- Boeing completed its acquisition of Spirit AeroSystems on December 8, 2025 (~$8.3B including assumed debt); Spirit's Airbus-linked sites (US, Morocco, France, UK — A220/A320/A350 structures) were concurrently divested to Airbus per FTC order. Spirit kept in the roster with blank ticker (formerly NYSE: SPR, now delisted) since the physical fuselage-build bottleneck is still worth tracking independent of ownership.
- GE Aerospace trades under the unchanged ticker "GE" on NYSE — it is what remained of the old General Electric conglomerate after the GE HealthCare (2023) and GE Vernova (2024) spinoffs, not a new company.
- Airbus SE is incorporated in the Netherlands (a Dutch SE) but headquartered and operationally run from Toulouse, France; trades on Euronext Paris under ticker AIR.
- VSMPO-Avisma trades on the Moscow Exchange under ticker VSMO; it has so far avoided direct entity-level sanctions even though parent Rostec and its CEO are sanctioned, and continued exporting several hundred million dollars of titanium to Western buyers through 2023 — a genuinely live and unresolved chokepoint rather than a fully closed one.
- Precision Castparts and Timet are both private subsidiaries under Berkshire Hathaway (via the 2016 Precision Castparts acquisition); neither will produce public financials for the FINANCIALS burst, which is expected and handled the same way the shipping map handled unlisted/state infrastructure nodes.
