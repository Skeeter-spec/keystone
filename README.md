# Keystone

A living atlas of the world's industrial value chains, mapped to find the chokepoints. Educational research, not investment advice.

In ecology a keystone species holds a whole system together. In an economy a keystone firm is the one a value chain cannot route around: the sole tool maker, the sole refiner, the sole foundry. Keystone hunts for those firms, one industry at a time, and shows the map behind them.

## What this is, and what it is not

Each project traces three things about an industry: **who does what** (design, fabricate, package, sell), **how big each player is** (audited financials), and above all **how they depend on each other** (who licenses, fabricates, supplies, and buys from whom). The payoff is the dependency edges and the chokepoints they reveal.

This is educational market and industry research, built in the open for learning. It is **not** personal financial advice and **not** investment guidance. Nothing here is a recommendation to buy or sell anything.

## The method

Every map follows the same shape, so the workflow carries from one industry to the next:

- **A graph, not a roster.** Companies are nodes; the real work is the directed relationship edges between them.
- **Three lenses.** Accounting (audited financial reality), politics (export controls, sanctions, subsidies), and economics (industry structure, concentration, cycles).
- **Sourced or it does not exist.** Every figure and edge carries a real source and a tier, from primary regulatory filings down to news. Volatile numbers get two independent sources.
- **Self contained artifacts.** Each map renders to a single offline page with the data baked in, so it stays honest and portable.

## Projects

| # | Map | Status |
|---|-----|--------|
| 01 | [Semiconductor ecosystem](projects/01-semiconductor/) | Foundation and financials done; relationships and the politics and economics lenses in progress |

More maps join as siblings under `projects/`. Candidates on deck: critical minerals, EV batteries, the AI compute stack, payment rails.

## How a project works

Each project folder is self driving:

```
data/          the CSVs that hold the map
build_artifact.py   turns the CSVs into the published page
AGENT-RUNBOOK.md    exact instructions for one research burst
PROGRESS.log        an append only log of what each burst did
```

The loop: run a research burst to grow the CSVs, rebuild the page, republish to the same place, log it.

## License

Released under AGPL 3.0. You may read, run, and build on this freely under those terms. For other licensing, contact the author.
