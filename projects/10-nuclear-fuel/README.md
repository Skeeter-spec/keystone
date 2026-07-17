# Nuclear fuel ecosystem map

A slow, evidence based map of the Nuclear fuel value chain: who the players are, how big they are, and above all how they depend on each other, so the true chokepoints stand out.

Part of the Keystone atlas. This is educational market and industry research, not investment advice.

## What this is (and is not)

A value chain, not an ownership chart. Nodes are companies; the real work is the directed edges between them (who supplies, licenses, refines, fabricates, or sells to whom). The point is to fill those edges with real evidence and find where the chain cannot route around a single player.

## The onion (layers, top of chain to bottom)

- **Uranium mining.** Digging or in-situ leaching natural uranium ore into yellowcake (U3O8); the most geographically diverse layer (Kazakhstan, Canada, Australia, Namibia, US).
- **Conversion.** Refining and converting U3O8 into uranium hexafluoride (UF6), the feedstock enrichment plants need; only a handful of plants exist worldwide.
- **Enrichment.** Raising the U-235 concentration by centrifuge (or emerging laser methods); a tight four-player oligopoly, with Russia alone holding roughly 40% or more of global capacity.
- **Fuel fabrication.** Converting enriched UF6 back to UO2 and assembling it into fuel rods/assemblies built to each reactor design's exact specification.
- **Reactors and utilities.** The power plants and their operating companies that burn the fabricated fuel to generate electricity.
- **Reprocessing and waste.** Recycling spent fuel to recover usable uranium/plutonium (where practiced) and managing the resulting waste stream.

## Files

```
data/companies.csv       one row per company (18 col shared schema); financial fields fill later
data/relationships.csv   one row per directed edge (10 col shared schema); the crown jewel
data/sources.csv         provenance registry
FOUNDATION.md            the foundation brief: chokepoint hypotheses + free data sources
AGENT-RUNBOOK.md         instructions for one research burst
PROGRESS.log             append only log of each burst
```
