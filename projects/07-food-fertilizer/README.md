# Food and fertilizer ecosystem map

A slow, evidence based map of the Food and fertilizer value chain: who the players are, how big they are, and above all how they depend on each other, so the true chokepoints stand out.

Part of the Keystone atlas. This is educational market and industry research, not investment advice.

## What this is (and is not)

A value chain, not an ownership chart. Nodes are companies; the real work is the directed edges between them (who supplies, licenses, refines, fabricates, or sells to whom). The point is to fill those edges with real evidence and find where the chain cannot route around a single player.

## The onion (layers, top of chain to bottom)

- **Feedstock** — the raw physical inputs fertilizer manufacturing cannot substitute away from: natural gas (feeds nitrogen synthesis via the Haber-Bosch process), phosphate rock (mined, mostly in Morocco, China, Russia and the US), and potash ore (mined, concentrated in Belarus, Russia and Canada).
- **Fertilizer production (N/P/K)** — converting that feedstock into the three macronutrients crops need: nitrogen (ammonia, urea, nitrates), phosphate (DAP/MAP), and potash (muriate/sulphate of potash). This is where reserve geography and gas prices turn into genuine chokepoints.
- **Seeds & agrochemicals** — proprietary seed genetics and the crop protection chemistry (herbicides, insecticides, fungicides) sold alongside them; a small oligopoly (Bayer, Corteva, Syngenta, BASF) controls most of the world's commercial supply.
- **Farms** — millions of growers worldwide who buy fertilizer and seed/agrochem inputs and produce the raw crop; deliberately not itemized as company rows here, too fragmented to be a chokepoint.
- **Grain trading & logistics (ABCD)** — the handful of trading houses (Archer-Daniels-Midland, Bunge, Cargill, Louis Dreyfus, plus China's COFCO) that own the elevators, rail, barges and ports moving grain from farm to port and hold the pricing and logistics information farmers and importers depend on.
- **Processing** — crushing, milling and refining raw grain and oilseed into flour, vegetable oil, animal feed and other intermediate food ingredients.
- **Food** *(out of scope for company rows here)* — packaged food, retail and consumer brands that buy processed ingredients; tracked, if at all, in a separate Keystone map, not duplicated in this one.

## Files

```
data/companies.csv       one row per company (18 col shared schema); financial fields fill later
data/relationships.csv   one row per directed edge (10 col shared schema); the crown jewel
data/sources.csv         provenance registry
FOUNDATION.md            the foundation brief: chokepoint hypotheses + free data sources
AGENT-RUNBOOK.md         instructions for one research burst
PROGRESS.log             append only log of each burst
```
