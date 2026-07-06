---
name: deal-comps
description: |
  Compare several ABS/CMBS deals side by side — capital structure, credit
  enhancement and subordination, collateral characteristics, pricing/coupon, and
  structural features (triggers, OC/turbo) — by running the single-deal parser
  across a shelf or a named set of deals and normalising the results into one table.

  **Use when:** the user wants a comps table, a shelf/vintage comparison, "how does
  deal X stack up against its peers", or CE/subordination benchmarking across deals.

  **Not for:** a single deal's summary (use abs-prospectus-analysis) or one pool's
  loan-level cut (use loan-tape-analysis / cmbs-loan-tape-analysis).
---

# Deal Comps (cross-deal comparison)

Comps are the single-deal parser applied across **N deals** and normalised into one
comparison. This skill orchestrates the primitives that already exist; the value it adds
is a **common schema** so unlike prospectuses line up.

## Workflow

### Step 1 — Assemble the deal set
- A **shelf / vintage**: use **`search_securitisation_deals`** (and
  **`get_deal_filings`**) to list the issuer's deals in the window (e.g. "AmeriCredit
  auto, last 4"; "Benchmark CMBS 2018–2020").
- An **explicit list**: take the deals the user named.
Resolve each to a CIK + the relevant prospectus (424B) accession.

### Step 2 — Parse each deal to a common schema
For every deal, run the single-deal chain — **`get_filing_document`** (the 424B) fed
through the **`abs-prospectus-analysis`** skill (for CMBS, **`cmbs-loan-tape-analysis`**
adds pool credit metrics). Extract the **same fields** for each:

- **Capital structure:** tranches, sizes, ratings, WAL, coupon/spread.
- **Credit enhancement:** subordination by tranche, OC, reserve account, XS spread;
  the total CE beneath each rated class.
- **Collateral:** pool balance, WA coupon, WA FICO/DSCR, WA term/seasoning, key
  concentrations (top states, property type for CMBS, new/used for auto).
- **Structure:** sequential vs pro-rata, triggers (cumulative-loss, delinquency, OC),
  turbo, revolving/prefunding.

### Step 3 — Normalise & tabulate
Line the deals up in **columns**, one metric per row, so differences pop: e.g. Class A
CE 6.25% vs 7.10% vs 5.90%; WA FICO 715 vs 702 vs 726; trigger thresholds. Flag where a
field is absent or defined differently rather than forcing a false match.

### Step 4 — Deliver
The comps table, then a short **"what changed across the shelf/peers"** narrative —
tightening or loosening CE, collateral drift, structural changes. Offer a CSV export.

## Honest limits (state them)
Prospectus fields are **semi-structured text**, so extraction is LLM-parsed and the
comps are **review-grade** — every figure should be verified against the source 424B
before it drives a decision. Definitions differ across issuers (e.g. how "credit
enhancement" is stated), so note the basis rather than comparing incomparable numbers.
This is analytical support, not investment advice.
