# EV batteries ecosystem map

A slow, evidence based map of the EV batteries value chain: who the players are, how big they are, and above all how they depend on each other, so the true chokepoints stand out.

Part of the Keystone atlas. This is educational market and industry research, not investment advice.

## What this is (and is not)

A value chain, not an ownership chart. Nodes are companies; the real work is the directed edges between them (who supplies, licenses, refines, fabricates, or sells to whom). The point is to fill those edges with real evidence and find where the chain cannot route around a single player.

## The onion (layers, top of chain to bottom)

- Layer 0  Raw metals extraction (mining). Lithium (brine and hard-rock spodumene), nickel, cobalt, natural graphite, manganese.
- Layer 1  Refining and precursor chemicals. Converts ore/brine into battery-grade compounds: lithium hydroxide/carbonate, nickel and cobalt sulfates, precursor cathode active material (pCAM).
- Layer 2  Active materials and components. Cathode active material (CAM), anode material (natural or synthetic graphite, increasingly silicon-blended), electrolyte (solvent + LiPF6 salt), separator film.
- Layer 3  Cell manufacturing. Assembles materials into finished cylindrical, prismatic, or pouch cells (the electrochemical core of the battery).
- Layer 4  Pack and module integration. Cells are grouped into modules and packs with a battery management system (BMS) and thermal/structural design; often done in-house by automakers or by the cell maker.
- Layer 5  Automakers / OEMs. Integrate packs into vehicles; a few (Tesla, BYD) also make their own cells.
- Layer 6  Recycling and second life. Recovers lithium, nickel, cobalt, copper, and graphite from end-of-life batteries and scrap, feeding back into Layer 1.

## Files

```
data/companies.csv       one row per company (18 col shared schema); financial fields fill later
data/relationships.csv   one row per directed edge (10 col shared schema); the crown jewel
data/sources.csv         provenance registry
FOUNDATION.md            the foundation brief: chokepoint hypotheses + free data sources
AGENT-RUNBOOK.md         instructions for one research burst
PROGRESS.log             append only log of each burst
```
