# Critical minerals ecosystem map

A slow, evidence based map of the Critical minerals value chain: who the players are, how big they are, and above all how they depend on each other, so the true chokepoints stand out.

Part of the Keystone atlas. This is educational market and industry research, not investment advice.

## What this is (and is not)

A value chain, not an ownership chart. Nodes are companies; the real work is the directed edges between them (who supplies, licenses, refines, fabricates, or sells to whom). The point is to fill those edges with real evidence and find where the chain cannot route around a single player.

## The onion (layers, top of chain to bottom)

- **Exploration & mining** — pulling ore, brine, or laterite out of the ground (rare earth ore, spodumene, DRC copper-cobalt, nickel laterite, natural graphite).
- **Concentration & beneficiation** — crushing and physically upgrading raw ore into a shippable concentrate (spodumene concentrate, mixed rare earth carbonate, graphite concentrate); usually bundled with the mine itself.
- **Refining & separation** — the chemically hard step: splitting mixed rare earth concentrate into 17 individual oxides, converting brine into battery-grade lithium carbonate/hydroxide, or smelting cobalt/nickel ore into sulfates. This is where China's lead is most extreme and where most chokepoints live.
- **Alloying, magnet-making & battery chemicals** — turning refined output into an intermediate a factory can actually use: NdFeB magnet alloy and sintered magnets, or precursor/cathode active material (pCAM/CAM) for battery cells.
- **Recycling & urban mining** — recovering rare earths, cobalt, nickel, and lithium from scrap magnets and end-of-life batteries, feeding back into the refining layer and slowly diluting the raw-ore chokepoint.
- **Trading, stockpiling & export policy** — state trading arms, quota systems, and export-license regimes (China's rare earth/gallium/germanium/graphite controls, national strategic stockpiles) that sit above the physical chain and can throttle it without touching a single mine.
- **Downstream integration** *(out of scope for company rows here)* — EV, wind turbine, defense, and electronics OEMs that consume magnets and battery chemicals; tracked in other Keystone maps, not duplicated in this one.

## Files

```
data/companies.csv       one row per company (18 col shared schema); financial fields fill later
data/relationships.csv   one row per directed edge (10 col shared schema); the crown jewel
data/sources.csv         provenance registry
FOUNDATION.md            the foundation brief: chokepoint hypotheses + free data sources
AGENT-RUNBOOK.md         instructions for one research burst
PROGRESS.log             append only log of each burst
```
