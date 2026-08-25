---
description: Compare several ABS/CMBS deals side by side — capital structure, credit enhancement, collateral, structure
argument-hint: "[shelf/issuer, or a list of deals]"
---

# Deal Comps (cross-deal comparison)

> Uses the bundled EDGAR connector — if its tools are missing or erroring, see [CONNECTOR.md](../CONNECTOR.md).

Run the single-deal parser across a shelf or a named set of deals and normalise the
results into one comparison table — capital structure, credit enhancement / subordination,
collateral, pricing, and structural features.

## Workflow

### Step 1 — Assemble the deal set
Use **`search_securitisation_deals`** / **`get_deal_filings`** to list a shelf or
vintage, or take the deals the user named. Resolve each to a CIK + 424B accession.

### Step 2 — Load the skill
Use `skill: "deal-comps"` for the common schema and normalisation rules.

### Step 3 — Parse each deal
For each deal, run **`get_filing_document`** (the 424B) through
`skill: "abs-prospectus-analysis"` (add `skill: "cmbs-loan-tape-analysis"` for CMBS pool
metrics). Extract the **same fields** every time.

### Step 4 — Deliver
A columns-are-deals comparison table (one metric per row), then a short "what changed
across the shelf/peers" narrative. Offer a CSV export. Flag missing or differently-defined
fields instead of forcing a match.

## Honest limit
Prospectus fields are semi-structured text — comps are **review-grade** and must be
verified against the source 424B. Not investment advice.
