# Payment rails ecosystem map

A slow, evidence based map of the Payment rails value chain: who the players are, how big they are, and above all how they depend on each other, so the true chokepoints stand out.

Part of the Keystone atlas. This is educational market and industry research, not investment advice.

## What this is (and is not)

A value chain, not an ownership chart. Nodes are companies; the real work is the directed edges between them (who supplies, licenses, refines, fabricates, or sells to whom). The point is to fill those edges with real evidence and find where the chain cannot route around a single player.

## The onion (layers, top of chain to bottom)

- **Card networks** — Visa, Mastercard, and the smaller closed-loop/state networks (Amex, Discover/Capital One, UnionPay) that set the rules and route authorization messages for card transactions.
- **Issuers & acquirers** — banks and fintechs that issue cards to cardholders (issuers) or sign up and fund merchants to accept them (acquirers), taking the credit and fraud risk on each side.
- **Processors** — the back-office engines (Fiserv, FIS, Global Payments) that run authorization, clearing, and settlement logic on behalf of issuers and acquirers.
- **Gateways** — the checkout-facing layer (Stripe, Adyen, PayPal) that captures a payment and routes it into the card or bank rails, often bundling acquiring and processing underneath.
- **Interbank messaging** — SWIFT, the cooperative standard that lets banks tell each other to move money across borders, without itself moving a cent.
- **Clearing & settlement** — where money actually changes hands for good: central banks (Federal Reserve/Fedwire), bank-owned clearinghouses (The Clearing House/CHIPS, RTP), and their peers abroad.
- **Alternative rails** — routes that bypass the card/bank stack entirely: ACH-style bank transfers, wallets and P2P networks (PayPal, Zelle, Wise), and stablecoins (Circle/USDC, Tether/USDT).

## Files

```
data/companies.csv       one row per company (18 col shared schema); financial fields fill later
data/relationships.csv   one row per directed edge (10 col shared schema); the crown jewel
data/sources.csv         provenance registry
FOUNDATION.md            the foundation brief: chokepoint hypotheses + free data sources
AGENT-RUNBOOK.md         instructions for one research burst
PROGRESS.log             append only log of each burst
```
