# Semiconductor ecosystem map

A slow, evidence based map of the global chip industry: who the companies are, how big they are, and above all how they depend on each other. Built to unfold like an onion, one layer at a time.

## What this is (and is not)

The source infographic groups companies by the job they do (design, fabricate, package, sell). That is a value chain, not an ownership chart. No company here reports to another. The relationships are commercial: who licenses to whom, who fabricates for whom, who buys from whom. The point of this project is to fill in those edges with real evidence and then see where the true chokepoints are.

## Files

```
data/companies.csv       one row per company, plus financial fields to fill in
data/relationships.csv   one row per directed relationship (the crown jewel)
AGENT-RUNBOOK.md         exact instructions the scheduled agent follows each run
README.md                this file
```

## The onion (layers of work)

- Layer 0  Schema. DONE. Column shapes locked in the two CSVs.
- Layer 1  Roster and financials. Fill revenue, net income, market cap, R&D, capex for all 41 companies. Mostly automatable.
- Layer 2  Segment sizing. Split each company's revenue by business line.
- Layer 3  Relationship edges. Read each company's latest filing, extract named customers, suppliers and partners into relationships.csv with a citation. This is the slow core.
- Layer 4  Chokepoint analysis. Compute which single nodes, if removed, break the most paths.
- Layer 5  Visualization. Turn the graph into an interactive map.

## companies.csv schema

| column | meaning |
|---|---|
| company | display name |
| ticker | primary stock symbol |
| exchange | where it trades |
| hq_country | headquarters country |
| roles | one or more of: fabless-chip, fabless-system, ip-eda, foundry, equipment, component-supplier, osat, idm, oem (semicolon separated) |
| primary_segment | short plain description of what it mainly sells |
| revenue_usd_b | annual revenue in billions USD |
| net_income_usd_b | annual net income in billions USD |
| market_cap_usd_b | market capitalization in billions USD |
| rd_spend_usd_b | annual research and development spend in billions USD |
| capex_usd_b | annual capital expenditure in billions USD |
| fiscal_year | the fiscal year the figures come from |
| filing_source | url or document the figures came from |
| last_updated | date the row was last filled (YYYY-MM-DD) |
| chokepoint | yes if the whole industry has few or no alternatives to this company |
| notes | free text |

## relationships.csv schema

| column | meaning |
|---|---|
| from_company | the company that acts |
| to_company | the company acted upon |
| relationship_type | licenses-ip-to, provides-eda-to, fabricates-for, supplies-components-to, sells-equipment-to, is-customer-of, packages-for, invests-in, competes-with |
| description | one plain sentence on the specific relationship |
| evidence_source | url or filing where this was found |
| evidence_date | date of that evidence |
| confidence | high, medium, or low |
| last_updated | date the row was written |

Direction matters. "TSMC fabricates-for Nvidia" and "Nvidia is-customer-of TSMC" are the same fact from two sides. Prefer recording the supplier side (fabricates-for, supplies-components-to, sells-equipment-to, licenses-ip-to) so the graph reads as flows of goods and value.

## Chokepoint queue (research starts here)

The eight companies the rest of the industry has the fewest alternatives to. Work these first.

1. TSMC          leading edge foundry the world leans on
2. ASML          only maker of EUV lithography machines
3. Arm           instruction set inside almost every phone
4. Nvidia        dominant AI accelerator designer
5. Samsung       spans foundry, memory, components and devices
6. Intel         IDM turning into a foundry
7. Applied Materials   largest chip equipment maker
8. SK hynix      key supplier of HBM memory for AI

## Free data sources

- SEC EDGAR (US filers, has a free API): https://www.sec.gov/cgi-bin/browse-edgar
- Company investor relations pages and annual reports (for non US filers: TSMC, ASML, Samsung, SK hynix, Infineon, SMIC, Japanese suppliers)
- stockanalysis.com and similar aggregators for quick financial snapshots
- Company 10-K / 20-F risk factors and customer concentration sections for relationship edges
