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

## Pick up here

```
./tools/gate.sh                       does the repo still match what it claims? run this first
tail -3 projects/*/PROGRESS.log       what each map actually did last, and what it needs next
```

Deliberately a pointer, not a summary. Every status written in prose is a copy of something the data
already knows, and copies rot: this README once called 01 "in progress" two phases after it shipped,
and a map's own log once told a reader to build a renderer that already existed. **`PROGRESS.log` is
append only, so the newest entry wins. Read it bottom up.** The table below is the one exception, and
only because `tools/gate.sh` fails if it stops matching the data.

The open work, in rough order of leverage: fill financials and relationship edges for the maps that are
still foundation only (03 to 10), cost 02's remaining non-chokepoint companies, and add the politics lens to 01.
All ten maps now render: each has a `map.json`, so a foundation map draws its value chain the moment its
data lands.

## Projects

| # | Map | Status |
|---|-----|--------|
| 01 | [Semiconductor ecosystem](projects/01-semiconductor/) | **Mapped.** 41 companies costed, 48 sourced relationship edges, 8 chokepoints, five year financials for every chokepoint. Politics and economics lenses next |
| 02 | [Critical minerals](projects/02-critical-minerals/) | **Edges started.** 17 sourced relationship edges, 9 of them real dependencies, and all 5 chokepoints costed from FY2025 audited filings (10 of 33 companies costed). No timeseries or politics lens yet |
| 03 | [EV batteries](projects/03-ev-batteries/) | Foundation only |
| 04 | [AI compute stack](projects/04-ai-compute/) | Foundation only |
| 05 | [Pharmaceuticals](projects/05-pharma/) | Foundation only |
| 06 | [Shipping](projects/06-shipping/) | Foundation only |
| 07 | [Food and fertilizer](projects/07-food-fertilizer/) | Foundation only |
| 08 | [Payment rails](projects/08-payment-rails/) | Foundation only |
| 09 | [Aerospace](projects/09-aerospace/) | Foundation only |
| 10 | [Nuclear fuel](projects/10-nuclear-fuel/) | Foundation only |

**What "foundation only" means, precisely.** A foundation brief is a taxonomy, a ranked set of chokepoint
*hypotheses*, and the list of free filing portals a later burst should pull from. Its seed companies carry
roles and notes but **no financials and no per row source tier**. They are the questions the map intends to
answer, not answers. Only a map marked **Mapped** has cleared the sourcing bar described above. Treat every
foundation row as unverified until its relationship and financial bursts land.

## How a project works

Each project folder is self driving:

```
data/               the CSVs that hold the map
map.json            this map's prose, storage key, and value chain layers
AGENT-RUNBOOK.md    exact instructions for one research burst
PROGRESS.log        an append only log of what each burst did
artifact/           the built page (generated, never hand edited)
```

One renderer serves every map:

```
python3 shared/build_map.py projects/02-critical-minerals 2026-07-16
```

`shared/build_map.py` + `shared/map-template.html` turn any map's CSVs into its page. What differs
between maps is **data, not code**: `map.json` carries the title, the notes, the storage key, and the
value chain layers. A map author never writes JavaScript.

The layers are the part that matters. Each declares a `role` that must match the roles used in that
map's `companies.csv`, and the builder **aborts** if any company has no matching layer. That check
exists because the failure is otherwise invisible: running the old semiconductor renderer against the
minerals data succeeded, exit 0, and drew a map where 30 of 33 companies appeared in no layer at all.

The loop: run a research burst to grow the CSVs, verify every cited source with
`tools/verify_edges.py`, merge with `tools/merge_edges.py`, rebuild the page, republish to the same
place, log it.

## The gate

```
./tools/gate.sh     run this before every commit
```

A rule that lives only in a README is a wish. `tools/check_data.py` asserts the promises above against
the actual CSVs: no financial figure without a source behind it, no source tier outside 1 to 3, no
unsourced relationship edge, and a status table that still matches the data it describes.

Incomplete does not fail the gate. Incorrect does. A foundation map with no financials is a question
waiting for a burst, not an error, and a gate that failed on every foundation would simply get bypassed.

The gate checks itself first. `python3 tools/check_data.py --selftest` breaks known good data on purpose
and proves every rule fires on its own mutant, because a check that has quietly stopped working reports
exactly the same clean result as a repo that is genuinely clean.

## License

Released under AGPL 3.0. You may read, run, and build on this freely under those terms. For other licensing, contact the author.
