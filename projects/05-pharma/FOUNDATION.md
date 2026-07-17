# Foundation brief — Pharmaceuticals

## Chokepoints, ranked

The essential-medicines chain has thousands of participants but very few places where the whole system cannot route around a single player. These six are seeded with `chokepoint,TRUE` in `data/companies.csv`; the reasoning below is the hypothesis to test as relationship evidence comes in.

1. **API / precursor concentration in India and China** — represented here by **Zhejiang Huahai Pharmaceutical** and **Scientific Protein Laboratories**. A large share of the world's generic-drug active pharmaceutical ingredients, and nearly all crude heparin (an anticoagulant extracted from pig intestine with no synthetic substitute at scale), are made in a small number of Chinese and Indian plants. Huahai's 2018 valsartan/sartan API contamination triggered a global multi-country recall; SPL's Changzhou, China sourcing chain was the source of the 2007-2008 contaminated-heparin crisis that killed patients in the US. When one plant goes down (recall, inspection failure, export ban, geopolitical dispute), there is often no qualified second source ready to absorb volume, because switching an API supplier requires re-validating the drug with regulators, a process that takes months to years.
2. **Sterile-injectable and biologics CDMOs** — represented here by **Lonza Group** and **WuXi Biologics**. Originators increasingly do not own the sterile fill-finish or biologics manufacturing lines their own drugs need; that capacity sits with a handful of contract development and manufacturing organizations. Capacity is genuinely scarce (specialized cleanrooms, bioreactor trains, and inspected sites take years to build), so a shutdown or geopolitical restriction at one of these firms cannot be quickly absorbed elsewhere. WuXi Biologics carries an added geopolitical chokepoint: it is explicitly named in the proposed US BIOSECURE Act, which would bar federal contracts with the firm and force US biotech customers to re-source biologics manufacturing.
3. **The big-three US drug distributors** — represented here by **McKesson Corporation** (Cencora and Cardinal Health are seeded but not separately flagged, to keep the chokepoint list to genuinely singular nodes rather than triple-counting one structural fact). McKesson, Cencora, and Cardinal Health together move on the order of 90% of the pharmaceutical volume that reaches US pharmacies and hospitals. Almost every manufacturer routes through one of these three; there is no fourth-scale alternative.
4. **The PBM oligopoly** — represented here by **CVS Health (Caremark)** (Cigna's Express Scripts and UnitedHealth's OptumRx are seeded but not separately flagged, same reasoning as above). CVS Caremark, Express Scripts, and OptumRx together administer roughly 80% of US prescription-drug claims. They decide formulary placement and negotiate the rebates that determine a drug's real net price, giving this layer outsized leverage over both manufacturers and patients even though none of them touches a physical pill.

Deliberately not flagged as chokepoints: individual originators (Pfizer, Roche, etc.) are large and famous but each competes in a crowded therapeutic-area market with real substitutes; Samsung Biologics and Catalent are real CDMO capacity but currently more substitutable (Samsung Biologics is in fact the leading Western-aligned alternative to Chinese biologics CDMOs); Sun Pharma/Dr. Reddy's/Aurobindo/Cipla are large generics/API makers but operate in a more fragmented, higher-substitutability part of the API market than the sartan/heparin cases above.

## Free data sources

**Accounting (company financials)**
- SEC EDGAR full-text search and filings (US-listed and ADR filers: Pfizer, J&J, Merck, AbbVie, Lilly, McKesson, Cencora, Cardinal Health, CVS, Cigna, UnitedHealth, Teva, Dr. Reddy's): https://www.sec.gov/cgi-bin/browse-edgar
- Company investor-relations pages for non-US filers: Roche (roche.com/investors), Novartis (novartis.com/investors), AstraZeneca (astrazeneca.com/investor-relations), Sanofi (sanofi.com/en/investors), Novo Nordisk (novonordisk.com/investors), Lonza (lonza.com/investor-relations), Samsung Biologics (samsungbiologics.com/eng/investor), WuXi AppTec / WuXi Biologics (hkexnews.hk filings for HK-listed entities)
- stockanalysis.com and companiesmarketcap.com for quick market-cap and financial-statement snapshots (secondary, cross-check against filings)

**Politics / regulatory**
- FDA Drug Shortages database (current and resolved shortages, cause codes): https://www.accessdata.fda.gov/scripts/drugshortages/
- FDA facility inspection classifications and warning letters (Form 483s, Warning Letters): https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters
- FDA import alerts (identifies specific foreign API/finished-dose plants under import restriction): https://www.accessdata.fda.gov/cms_ia/importalert_list.html
- USTR Section 301 / tariff actions and BIS export-control rules affecting Chinese API and biologics manufacturers: https://ustr.gov and https://www.bis.doc.gov
- US BIOSECURE Act text and status (Congress.gov): https://www.congress.gov
- EU EMA shortages and availability catalogue: https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/medicine-shortages
- EU critical medicines / API sourcing policy pages (European Commission, DG SANTE): https://health.ec.europa.eu

**Economics / market structure**
- ASHP (American Society of Health-System Pharmacists) drug shortage list, with cause and therapeutic-category breakdowns: https://www.ashp.org/drug-shortages/current-shortages
- CMS Drug Spending Dashboards (Medicare Part B and Part D drug spending, by drug and manufacturer): https://www.cms.gov/medicare/data-analysis/drug-spending-dashboards
- IQVIA Institute public reports and press releases on drug spending and generic/API trends: https://www.iqvia.com/insights/the-iqvia-institute
- FTC reports on PBM market structure and rebate practices: https://www.ftc.gov/policy/reports/pharmacy-benefit-managers
- KFF (Kaiser Family Foundation) issue briefs on PBM concentration and drug pricing: https://www.kff.org

## Layer taxonomy used in roles

`originator`, `generics-maker`, `api-maker`, `cdmo`, `distributor`, `pbm`, `payer`, `pharmacy` (semicolon-separated where a company spans more than one).
