---
description: Search SEC EDGAR for securitisation deals and pull a deal's filing history
argument-hint: "[issuer, shelf, or asset class]"
---

# Search Securitisation Deals

> Uses the bundled EDGAR connector — if its tools are missing or erroring, see [CONNECTOR.md](../CONNECTOR.md).

Find SEC-registered ABS / structured-finance deals on EDGAR and retrieve their
filings — prospectuses (424B), investor reports (10-D), and loan-level tapes
(ABS-EE) — using the free SEC EDGAR connector.

## Workflow

### Step 1 — Understand the request
Use the supplied issuer / shelf / asset class if given. Otherwise ask one short
question: *"What are you looking for — an issuer or shelf name (e.g. 'AmeriCredit',
'BMARK'), an asset class (auto, CMBS, RMBS), or a specific deal?"*

### Step 2 — Load the skill
Use `skill: "deal-search"` for EDGAR search technique, form-type meanings, and
coverage limits.

### Step 3 — Search
Call the **`search_securitisation_deals`** tool. Translate the request into:
- `query` — issuer / shelf text
- `asset_class` — one of auto, cmbs, rmbs, credit card, clo (optional helper)
- `form_type` — e.g. `424B5,424H` for prospectuses, `10-D` for investor reports,
  `ABS-EE` for loan-level tapes
- `date_from` / `date_to` — to bound the period

### Step 4 — Retrieve a deal's filings
When the user picks a deal, call **`get_deal_filings`** with its CIK to list the
full lifecycle (424H → FWP → 424B → 8-K → monthly 10-D + ABS-EE → 10-K). Filter
with `form_type` when they only want, say, the prospectus or the latest tape.

### Step 5 — Deliver
Return a clean table — issuer, CIK, form, filing date, report period, and a link
to each document. Offer the natural next step (`/parse-abs-prospectus`,
`/analyze-loan-tape`, or `/extract-waterfall`).

## Coverage note (state this if relevant)
EDGAR covers **registered** ABS. Strong for **auto** and **conduit CMBS**. There is
**no loan-level data for credit-card ABS** (excluded by rule) and **essentially no
EDGAR presence for CLOs** (144A) — for a CLO, ask the user to supply the offering
document or indenture and use `/review-clo-indenture`.
