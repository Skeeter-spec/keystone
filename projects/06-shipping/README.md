# Maritime shipping ecosystem map

A slow, evidence based map of the Maritime shipping value chain: who the players are, how big they are, and above all how they depend on each other, so the true chokepoints stand out.

Part of the Keystone atlas. This is educational market and industry research, not investment advice.

## What this is (and is not)

A value chain, not an ownership chart. Nodes are companies; the real work is the directed edges between them (who supplies, licenses, refines, fabricates, or sells to whom). The point is to fill those edges with real evidence and find where the chain cannot route around a single player.

## The onion (layers, top of chain to bottom)

- **Shipbuilding** — the yards that build the vessels; concentrated in China, South Korea and Japan, with multi-year order backlogs and very few qualified builders for specialized ship types (e.g. large LNG carriers).
- **Ship owners / lessors** — who actually owns the steel: liner-owned fleets, sale-and-leaseback financiers, and container-box lessors who lease the boxes (not the ships) to the lines.
- **Liner operators & alliances** — the container shipping lines that sell cargo space and run scheduled services, increasingly coordinated through vessel-sharing alliances (Ocean Alliance, Gemini Cooperation, Premier Alliance) that jointly control most East-West capacity.
- **Ports & terminals** — the loading docks: global terminal operators (state-owned, sovereign-fund-owned, or conglomerate-owned) that run container berths at the world's major hubs.
- **Canals & straits** — the geography itself: the handful of canals and narrow straits that ocean freight cannot route around without adding days or weeks of transit.
- **Forwarders & logistics** — the intermediaries who book cargo space on behalf of shippers and manage door-to-door multimodal delivery, without owning vessels themselves.
- **Marine insurance & classification** — the P&I clubs that insure liability risk and the classification societies that certify a ship is seaworthy; without both, a vessel cannot get port access or canal transit.

## Files

```
data/companies.csv       one row per company (18 col shared schema); financial fields fill later
data/relationships.csv   one row per directed edge (10 col shared schema); the crown jewel
data/sources.csv         provenance registry
FOUNDATION.md            the foundation brief: chokepoint hypotheses + free data sources
AGENT-RUNBOOK.md         instructions for one research burst
PROGRESS.log             append only log of each burst
```
