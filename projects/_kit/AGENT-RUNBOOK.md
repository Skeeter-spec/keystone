# Agent runbook (one burst)

Shared schema across every Keystone map. Never invent figures; every number and edge needs a real source.

## Bursts
- FOUNDATION: lock the layer taxonomy (README onion), seed ~20 to 30 real companies into data/companies.csv
  (company,ticker,exchange,hq_country,roles,primary_segment filled; financials blank; set chokepoint yes
  for suspected chokepoints (the value must be exactly `yes` or `no`, never TRUE/FALSE:
  the artifact template tests chokepoint==='yes', so TRUE renders as NOT a chokepoint, silently); lens=accounting), and write FOUNDATION.md (chokepoint hypotheses + free sources).
- FINANCIALS: fill revenue/net income/market cap/R&D/capex for the next company with empty revenue_usd_b,
  from a primary filing URL; convert to USD billions and note the FX rate. Chokepoints first.
- RELATIONSHIPS: read a company's latest filing customer/supplier/risk sections; add supplier side edges to
  data/relationships.csv with a cited evidence_source.

## Before the fan-out: PILOT THE YIELD PATTERN ON ONE DOCUMENT YOURSELF

**Measured 2026-07-22 on 05-pharma, the first burst in this repo to come in UNDER its estimate.**
Before writing a single worker prompt, open ONE document by hand and find the sentence shape the whole
burst depends on. On 05 that was Pfizer's 10-K disclosing customer concentration by name:

> "The following summarizes revenue, as a percentage of Total revenues, from our three largest U.S.
> wholesaler customers... McKesson, Inc. 25% / Cencora, Inc. 16% / Cardinal Health, Inc. 13%"

That verbatim example, pasted into the prompts, produced **17 of the map's 47 edges**. One document of
your own time, and the fan-out stops being a gamble.

🔑 **THE GENERALISABLE FORM: FIND THE DISCLOSURE THE FILER IS REQUIRED TO MAKE.** A voluntary
disclosure says "our largest customer"; a MANDATORY one has to print the name. Pharma's is the >10%
customer-concentration rule. Every map has an equivalent, and identifying it is a cheap pre-registration
step that belongs in FOUNDATION.md before anyone spends a worker on it.

⚠ **And when you mint the vocabulary, walk the map's LAYER TAXONOMY and check every adjacent pair has a
term.** 05 shipped `distributes-for` (distributor -> the manufacturer whose product it moves) and missed
distributor -> pharmacy entirely, so a correct, well-sourced edge had to wear a wrong label until
`distributes-to` was added mid-burst. The layers are already written down in `map.json`; read them.

🔴 **A WORKER'S "I COULD NOT REACH IT" IS A QUEUE FOR YOU, NOT A CONCLUSION.** On 05, two of three
`unreachable` findings were wrong: the FTC PBM report was filed unreachable after two 404s and is live
at a different URL (it settles a whole chokepoint hypothesis), and congress.gov 403s a fetcher but loads
in a browser, where reading it showed the worker's premise was also wrong. Re-check every null before
it hardens into a gap row.

⚠ **Give each worker its OWN gap_id prefix.** Two workers on 05 independently numbered their rows
`g01..g11` and the ids collided on merge. `check_data.py` now fails the gate on duplicates, but the
cheap fix is upstream: say `gap-05-<worker>-<n>` in the prompt.

## Chokepoint discipline (applies whenever chokepoint=yes is set)
A chokepoint is a node the value chain genuinely CANNOT route around, not merely a big or important
player. Target roughly 15 to 25 percent of a map's nodes, no more.
- A DUOPOLY's two members can both qualify (Visa and Mastercard; Boeing and Airbus).
- A broad OLIGOPOLY (e.g. the 4 grain traders, the 3 hyperscale clouds, the seed/agrochem majors) is
  concentrated but ROUTABLE: a buyer can switch to a rival, so do NOT flag every member. Record the
  concentration as a theme in FOUNDATION.md instead of flagging individual firms.
- Genuine single points to flag: sole/near-sole suppliers, the one refiner/enricher/packager, a strait
  or canal with no bypass, a messaging/settlement rail everyone depends on.
- Sanity check before finishing: if more than ~1 in 4 nodes is yes, you are over-flagging; retighten.

## Provenance tiers (source_tier)
1 primary regulatory/audited filing or the company's own audited statements
2 official statistics / first party disclosure (newsroom, gov agency)
3 trackers / aggregators / think tanks
4 news

## Where the figures live

Before costing a batch, read `shared/SOURCING-ROUTES.md` and ROUTE the companies first (which host, which
language, structured or PDF). Extraction is cheap once the route is known; finding the route is what costs.
It also carries the traps: cninfo serves Shenzhen not Shanghai, consolidated vs parent-company statements
share row labels, net income means attributable-to-parent, and an identifier that resolves is not the
entity you meant.

## Record what you could NOT source (data/gaps.csv)

**A burst that finds nothing on a target has produced a result, not a blank.** On 04 the strongest
findings were absences: no hyperscaler names Nvidia anywhere in its own 10-K, and TSMC's 20-F will only
ever say "our largest customer". A map that records only what it could source draws those identically to
a relationship that does not exist, which is the opposite of what the reader should conclude.

So when you go looking for an edge or a figure and the document declines to say, write a row in
`data/gaps.csv` instead of dropping it:

```
gap_id,kind,subject,sought,searched,found_instead,blocks,would_close_it,status,last_checked
```

- `kind` is exactly one of `undisclosed` (the document exists and will not say), `unreachable` (a real
  source you could not read), `contradiction` (sources disagree, or the reported world contradicts the
  disclosed one), `unevidenced-flag` (this map claims something with no sourced edge behind it),
  `stale-evidence` (a SOURCED claim whose evidence predates a material change, so an existing edge
  becomes suspect), `out-of-scope` (the counterparty IS disclosed but is not on this map's roster, so
  the edge cannot be drawn). Anything else fails the gate.
- 🔴 **`out-of-scope` is the one that is usually YOUR MAP's bug, not the world's.** If a company returns
  no edges, check its counterparties against companies.csv before concluding anything: 02's Syrah looked
  unconnected purely because Ford, LG Energy Solution and POSCO were not on the roster.
- 🔴 **IF A GAP UNDERMINES ONE SPECIFIC EDGE, WRITE ITS `subject` AS `A -> B`.** That exact form is what
  lets `review.py`'s R8 and the renderer's edge badge find it, so the doubt reaches the reader instead of
  living only in the gaps tab. Measured 2026-07-22: 02 had three edges each named by their own open gap
  row, all rendering clean at confidence "high", including an offtake whose gap row said in plain words
  "The edge renders as a plain offtake and conveys none of this". A human wrote that and nothing read it.
  ⚠ Naming a COMPANY instead is still valid for a gap about the company, but it buys none of this: exact
  `A -> B` matching is deliberate, because the substring version of this check reported 57 of 57 edges
  atlas-wide and was pure noise.
- 🔴 **`searched` is what makes it evidence rather than a shrug, and the gate REJECTS a row without it.**
  Name the documents you actually opened: "TSMC FY2025 20-F, full text; Nvidia FY2026 10-K, full text".
  "Could not find anything" is unfalsifiable and worth less than silence.
- **`would_close_it`** must name the document or disclosure that would settle it, so the gap becomes the
  next burst's task rather than a permanent excuse.
- `found_instead` should quote the fudge where there is one. "Customer A through Customer G" and
  "our ten largest customers" are the actual findings.
- A `contradiction` must name at least two sources in `searched`, separated by `;`. One source cannot
  contradict anything.

These render on the map under **What the filings won't say**, with the open count on the front page.

## FOUNDATION bursts: pre-register the test

Every ranked chokepoint hypothesis must carry a **WOULD SETTLE IT** line naming the specific free
document that would confirm or kill it, drawn from the source list you are already writing. See any of
the existing FOUNDATION.md files for the shape.

Two reasons, both learned the hard way here. Stating the test in advance stops a later burst quietly
redefining what success looked like. And it makes that burst dramatically cheaper: it opens with a
shopping list instead of a search, and this repo has measured that FINDING THE ROUTE, not extracting the
figure, is what a burst actually spends its time on (see `shared/SOURCING-ROUTES.md`).

Pre-registering is **not** the same as writing a `gaps.csv` row, and the two must not be confused. A gap
records that someone looked and the document declined to say. A pre-registered test records that nobody
has looked yet. Collapsing those two states would destroy the distinction the gaps model exists to
protect, which is why foundation maps carry pre-registered tests and zero gap rows.

Where a hypothesis is expected to be DISCONFIRMED, say so in the line. 10-nuclear-fuel pre-registers
uranium mining as its counter-example, so a burst that finds mining concentrated has found something
genuinely surprising rather than something to quietly drop.

## Ending a burst: one heading for doubt, and rows in the same commit

Write everything you are unsure about under exactly this heading:

```
## HONEST WEAKNESSES
```

Not "fragilities", not "omissions", not "limits of this evidence". Those are all real headings used by
real bursts in this repo, and on 2026-07-21 a retroactive sweep that grepped for the phrases it expected
FOUND ONE BLOCK AND MISSED TWO. Sitting in the missed ones: an offtake whose counterparty had vanished
from the latest filing, and an edge under an active default notice whose cure deadline had already
passed. A convention beats a regex, because the regex is what failed.

Then, **in the same commit**, every item under that heading that is a claim about evidence becomes a row
in `data/gaps.csv`. A weakness described only in prose is invisible to a reader of the map, which is the
whole failure this repo spent 2026-07-20 fixing. The log explains; the CSV is what renders.

Before you finish, run both verifiers. They ask different questions:

```
python3 tools/verify_edges.py   <project>   does each EDGE's source name both endpoints?
python3 tools/verify_sources.py <project>   does each FINANCIAL FIGURE's source name the company?
```

Neither is in `gate.sh`, because both need the network and a gate that needs wifi gives different
answers on different wifi. `verify_sources.py` is what caught a tier-1 row in the flagship map citing a
different company's annual results: same name prefix, different listed company, different stock code.
