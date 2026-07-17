# Pharmaceuticals ecosystem map

A slow, evidence based map of the Pharmaceuticals value chain: who the players are, how big they are, and above all how they depend on each other, so the true chokepoints stand out.

Part of the Keystone atlas. This is educational market and industry research, not investment advice.

## What this is (and is not)

A value chain, not an ownership chart. Nodes are companies; the real work is the directed edges between them (who supplies, licenses, refines, fabricates, or sells to whom). The point is to fill those edges with real evidence and find where the chain cannot route around a single player.

## The onion (layers, top of chain to bottom)

- **Originators / patent holders** — branded R&D companies that discover a molecule and hold the patent and regulatory exclusivity that lets them price it.
- **API & key starting materials** — the chemical or biological manufacturers that make the active ingredient and its precursor chemicals, heavily concentrated in a handful of Indian and Chinese plants.
- **Formulation, finished dose & CDMO** — turns raw API into the actual pill, injection, or biologic, often outsourced to contract development and manufacturing organizations rather than done in-house.
- **Distribution / wholesale** — moves finished product from the manufacturer's dock to every pharmacy, hospital, and clinic in the country.
- **PBMs & payers** — pharmacy benefit managers and insurers who negotiate rebates, set formularies, and decide what a patient can actually get and at what price.
- **Pharmacy / dispensing** — the point of care where a patient receives the medicine: retail, specialty, mail order, or hospital pharmacy.

## Files

```
data/companies.csv       one row per company (18 col shared schema); financial fields fill later
data/relationships.csv   one row per directed edge (10 col shared schema); the crown jewel
data/sources.csv         provenance registry
FOUNDATION.md            the foundation brief: chokepoint hypotheses + free data sources
AGENT-RUNBOOK.md         instructions for one research burst
PROGRESS.log             append only log of each burst
```
