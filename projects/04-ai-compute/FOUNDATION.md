# Foundation brief: AI compute & data centers

Part of the Keystone atlas, sitting above 01-semiconductor. This map covers the stack from accelerator silicon up through deployed foundation models: accelerators/HBM/networking, servers, datacenter power and cooling, hyperscale cloud, and model labs. It shares a handful of nodes with the semiconductor map (Nvidia, TSMC, SK hynix, Samsung, Micron, Broadcom, Marvell, Intel) by design; here they are scored on their AI-compute role, not their fab/tool role.

## Chokepoints, ranked

Six nodes are flagged chokepoint=TRUE in data/companies.csv: the ones the stack genuinely cannot route around. Ranked by how hard substitution would be. Several plausible candidates (hyperscalers, Broadcom, Vertiv, Eaton) are deliberately held as *themes* below rather than flagged, to keep the bar for "chokepoint" consistent across the Keystone maps.

1. **Nvidia** (accelerators + CUDA + NVLink/InfiniBand). The clearest chokepoint in the whole stack: dominant AI accelerator share, and the CUDA software ecosystem plus a decade of tooling lock-in means even customers who could get AMD or custom-ASIC silicon face high switching costs. Reinforced by its own networking stack (Mellanox/InfiniBand, NVLink) so a cluster can be Nvidia end to end.
2. **HBM trio (SK hynix, Samsung, Micron)** — flagged as three nodes. Only three companies on earth can make high-bandwidth memory at the volumes and yields modern accelerators require; there is no fourth supplier. HBM has been the binding supply constraint on AI chip output through 2024-2026 (Nvidia and AMD have both cited HBM allocation, not wafer starts, as the gating factor at times). No accelerator ships without it, so the whole trio is treated as a genuine supply chokepoint.
3. **TSMC CoWoS advanced packaging**. Leading-edge logic can theoretically be dual-sourced (Samsung, eventually Intel 18A), but CoWoS-class 2.5D/3D packaging that binds compute die to HBM stacks is overwhelmingly a TSMC-only capability at the volumes hyperscalers need. Packaging capacity, not wafer capacity, has repeatedly been the reported bottleneck on Nvidia's shippable GPU volume.
4. **Siemens Energy (large power transformers)**. The newest and most physical chokepoint. Gigawatt-scale data-center campuses need grid interconnection and large power transformers with multi-year lead times, and large transformers come from only a handful of makers worldwide. Siemens Energy is the best single case of a near-singular supplier; global transformer lead times have stretched to years, gating grid connection for new AI capacity. (Hitachi Energy, GE Vernova and Eaton share this constraint, which is why the broader grid-equipment squeeze is described as a theme, but Siemens Energy is flagged as the closest thing to an irreplaceable node.)

### Themes (real pressure, but routable — not flagged)
- **Hyperscaler concentration (Amazon/AWS, Microsoft/Azure, Google Cloud)**. Most AI training and inference runs through one of three clouds, and Microsoft's exclusive OpenAI relationship sharpens its position. But a buyer can and does route workloads between clouds, so the concentration is a structural theme, not a single point of failure. Google is the only hyperscaler with a mature in-house alternative to Nvidia (TPUs), itself a hedge against chokepoint #1.
- **Custom-ASIC design partner (Broadcom, with Marvell as second source)**. Every hyperscaler's non-Nvidia AI silicon program routes through a small set of design partners for SerDes, packaging IP and tape-out; Broadcom dominates today. But Marvell is a credible second source, so no single-point flag.
- **Datacenter power and cooling equipment (Vertiv, Schneider, Eaton, and the wider grid-equipment set)**. Liquid cooling is becoming structurally required as rack densities exceed air cooling, and switchgear/transformer backlogs are multi-year. The pressure is real and physical, but it is spread across several vendors, so only the single most-singular grid node (Siemens Energy, above) is flagged.
- **Foundation-model labs (OpenAI, Anthropic, Google DeepMind, Meta)**. Substitutable at the model layer relative to the physical layers above; open-weight models (Llama, Mistral, DeepSeek-class) further erode any single lab's leverage.

The chokepoints in this map are overwhelmingly in silicon and physical infrastructure, not in the clouds or the models on top.

## Free data sources by lens

### Accounting (company financials, filings, investor relations)
- SEC EDGAR full-text search and filings (Nvidia, AMD, Intel, Broadcom, Marvell, Micron, Arista, Astera Labs, Supermicro, Dell, HPE, Vertiv, Eaton, Amazon, Microsoft, Alphabet, Meta, Oracle, CoreWeave): https://www.sec.gov/cgi-bin/browse-edgar and https://www.sec.gov/edgar/search/
- TSMC investor relations (20-F filings, monthly revenue): https://investor.tsmc.com
- Samsung Electronics IR (quarterly earnings releases): https://www.samsung.com/global/ir/
- SK hynix IR (quarterly earnings, HBM commentary): https://www.skhynix.com/ir
- Siemens Energy IR (transformer/grid equipment order backlog): https://www.siemens-energy.com/global/en/home/investor-relations.html
- Schneider Electric IR: https://www.se.com/ww/en/about-us/investor-relations/
- Nebius Group IR (Nasdaq-listed, files 20-F/6-K): https://sec.gov and https://nebius.com/investors
- stockanalysis.com and companiesmarketcap.com for quick free financial/market-cap snapshots (secondary tier, cross-check against filings)

### Politics (export controls, national compute governance)
- US Bureau of Industry and Security (BIS), Commerce Dept: AI/advanced-computing chip export control rules and entity list updates: https://www.bis.gov/advanced-computing-and-semiconductors
- BIS Federal Register rule text (search "advanced computing" or "AI diffusion"): https://www.federalregister.gov/agencies/industry-and-security-bureau
- US CHIPS and Science Act program office (funding conditions tied to national security): https://www.nist.gov/chips
- European Commission AI Act and Chips Act pages (EU compute/data-center policy): https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence and https://digital-strategy.ec.europa.eu/en/policies/european-chips-act
- China MOFCOM and CAC public notices on chip export/import restrictions and data-center/AI governance (translated coverage via Reuters/Nikkei Asia when primary text is paywalled or Chinese-only)
- UK, Japan, South Korea, Netherlands government pages tracking coordinated export-control alignment with US BIS rules (each ministry of trade/economy site)

### Economics (electricity demand, data-center capacity, industry structure)
- IEA "Electricity 2026" and "Energy and AI" reports (free PDF, data-center electricity demand forecasts): https://www.iea.org/topics/electricity and https://www.iea.org/reports/energy-and-ai
- EPRI (Electric Power Research Institute) public reports on data-center load growth and grid impact: https://www.epri.com
- US EIA (Energy Information Administration) electricity demand and generation data, free API: https://www.eia.gov/opendata/
- US Department of Energy grid interconnection queue data and large-load studies (Berkeley Lab publishes free reports on interconnection queues): https://emp.lbl.gov/queues
- SemiAnalysis public/free blog posts (subscription gates deep-dives but many chokepoint-relevant notes on CoWoS, HBM, and power are summarized in free posts): https://www.semianalysis.com
- Synergy Research Group free press releases on hyperscale cloud market share: https://www.srgresearch.com
- Uptime Institute free data-center industry survey summaries: https://uptimeinstitute.com/resources

## Notes on methodology
- Foundation phase only: financial columns (revenue, net income, market cap, R&D, capex, fiscal_year, filing_source, source_tier) are intentionally left blank in data/companies.csv. Fill during a FINANCIALS burst per AGENT-RUNBOOK.md, chokepoints first.
- chokepoint = TRUE is a working hypothesis, not a final judgment; it should be revisited once relationships.csv edges are populated and customer-concentration disclosures are read.
- Overlap with 01-semiconductor is intentional: Nvidia, TSMC, SK hynix, Samsung, Micron, Broadcom, Marvell and Intel appear in both maps because the AI-compute chokepoints and the semiconductor chokepoints are, in several cases, literally the same company viewed through a different lens.
