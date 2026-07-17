# AI compute ecosystem map

A slow, evidence based map of the AI compute value chain: who the players are, how big they are, and above all how they depend on each other, so the true chokepoints stand out.

Part of the Keystone atlas. This is educational market and industry research, not investment advice.

## What this is (and is not)

A value chain, not an ownership chart. Nodes are companies; the real work is the directed edges between them (who supplies, licenses, refines, fabricates, or sells to whom). The point is to fill those edges with real evidence and find where the chain cannot route around a single player.

## The onion (layers, top of chain to bottom)

This map sits directly on top of the semiconductor map (01-semiconductor) and deliberately shares a few nodes (Nvidia, TSMC, SK hynix, Samsung, Micron, Broadcom, Marvell, Intel). Those companies' fab/tool-level detail lives in the semiconductor map; here they appear only in their AI-compute role.

- Layer 1  Accelerator silicon. GPUs, custom ASICs and inference chips that do the actual math (Nvidia, AMD, Intel, Broadcom, Marvell, Cerebras, Groq).
- Layer 2  HBM memory. High-bandwidth memory stacked next to the accelerator die, supply-constrained industry-wide (SK hynix, Samsung, Micron).
- Layer 3  Advanced packaging & foundry. Leading-edge fabrication plus the CoWoS-class packaging that binds compute die to HBM (TSMC; Samsung/Intel as secondary packaging capacity).
- Layer 4  Networking & interconnect. The fabric that turns thousands of chips into one cluster: NVLink/InfiniBand, Ethernet switch silicon, PCIe/CXL retimers (Nvidia, Broadcom, Marvell, Arista, Astera Labs).
- Layer 5  Servers & systems integration. Racking, cabling and assembling accelerators into deployable systems (Supermicro, Dell, HPE, Foxconn/Hon Hai).
- Layer 6  Datacenter power & cooling. Electrical infrastructure, large transformers and liquid cooling that keep the racks running, an increasingly physical (not silicon) bottleneck (Vertiv, Schneider Electric, Eaton, Siemens Energy).
- Layer 7  Hyperscale cloud. The platforms that rent out the finished compute (Amazon/AWS, Microsoft/Azure, Google Cloud, Oracle, CoreWeave, Nebius).
- Layer 8  Foundation-model labs & deployed AI services. The software layer consuming all of the above to train and serve models (OpenAI, Anthropic, Google DeepMind, Meta AI).

## Files

```
data/companies.csv       one row per company (18 col shared schema); financial fields fill later
data/relationships.csv   one row per directed edge (10 col shared schema); the crown jewel
data/sources.csv         provenance registry
FOUNDATION.md            the foundation brief: chokepoint hypotheses + free data sources
AGENT-RUNBOOK.md         instructions for one research burst
PROGRESS.log             append only log of each burst
```
