# Aerospace ecosystem map

A slow, evidence based map of the Aerospace value chain: who the players are, how big they are, and above all how they depend on each other, so the true chokepoints stand out.

Part of the Keystone atlas. This is educational market and industry research, not investment advice.

## What this is (and is not)

A value chain, not an ownership chart. Nodes are companies; the real work is the directed edges between them (who supplies, licenses, refines, fabricates, or sells to whom). The point is to fill those edges with real evidence and find where the chain cannot route around a single player.

## The onion (layers, top of chain to bottom)

- **Raw materials** — titanium and carbon-fiber composites: the aerospace-grade alloys and composite feedstock that everything else is built from, dominated by a handful of qualified mills (VSMPO-Avisma, ATI, Timet).
- **Components & systems** — avionics, landing gear, and structural castings: the tier-1 electronics, undercarriage, and precision-cast/forged parts (Honeywell, Thales, Safran, Howmet, Precision Castparts) that feed into both airframes and engines.
- **Engines** — the propulsion layer: a tight three-way oligopoly (GE Aerospace/CFM, Rolls-Royce, Pratt & Whitney/RTX) that no airframe can fly without.
- **Airframe OEMs** — the planemakers who integrate everything into a certified aircraft: a two-way duopoly for large jetliners (Boeing, Airbus), with regional and state-backed challengers (Embraer, COMAC) below that scale.
- **Airlines & lessors** — who actually flies and finances the fleet: the carriers that buy or lease aircraft (AerCap, Air Lease) to operate them commercially.
- **MRO** — maintenance, repair and overhaul: keeps the flying fleet airworthy, split between OEM aftermarket parts (TransDigm) and independent PMA competitors (HEICO) that erode OEM pricing power.

A parallel branch runs alongside this civil chain: **defense primes** (Lockheed Martin, Northrop Grumman, General Dynamics, BAE Systems, Leonardo) build military aircraft, missiles and defense electronics on government contracts, sharing some of the same materials and component suppliers but a mostly separate customer base and chokepoint structure.

## Files

```
data/companies.csv       one row per company (18 col shared schema); financial fields fill later
data/relationships.csv   one row per directed edge (10 col shared schema); the crown jewel
data/sources.csv         provenance registry
FOUNDATION.md            the foundation brief: chokepoint hypotheses + free data sources
AGENT-RUNBOOK.md         instructions for one research burst
PROGRESS.log             append only log of each burst
```
