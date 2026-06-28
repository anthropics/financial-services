---
name: abs-prospectus-analysis
description: |
  Parse a registered ABS prospectus (Form 424B/424H) into a structured, analyst-grade
  summary — transaction parties, capital structure (tranches), credit enhancement,
  collateral pool, performance triggers, and servicing.

  **Use when:** the user wants a deal summary, tranche table, or credit-enhancement
  breakdown from an SEC-registered ABS prospectus (auto, CMBS, consumer, etc.).

  **Not for:** CLOs (use clo-indenture-review) or loan-level tapes (use
  loan-tape-analysis).
---

# ABS Prospectus Analysis

Read a 424B/424H prospectus and extract the structure that matters. Fetch the text
with **`get_filing_document`**; prospectuses are long, so page through with `offset`,
concentrating on the summary, capital-structure, credit-enhancement, collateral, and
priority-of-payments sections.

## What to extract

### 1. Deal identity
Issuer/trust, sponsor, depositor, shelf, asset class, closing date, collateral
cut-off date, aggregate securitised amount, governing prospectus date.

### 2. Transaction parties
Sponsor, depositor, **issuing entity (trust)**, **servicer** (and backup servicer),
**indenture trustee**, owner trustee, originator(s), underwriters/initial purchasers,
asset representations reviewer, custodian.

### 3. Capital structure — the tranche table
For every class/note: **class** (A-1, A-2a/b, A-3, A-4, B, C, D), **principal
amount**, **% of capital structure**, **interest rate** (fixed, or benchmark + margin;
note SOFR vs fixed), **expected WAL**, **payment window**, **expected final** and
**legal final** maturity, **initial ratings** (Moody's / S&P / Fitch / DBRS-Morningstar),
and price/yield if shown. Note money-market tranche (A-1) and any pre-funding.

### 4. Credit enhancement stack
Quantify each layer and the **total initial enhancement per class**:
- **Subordination** (the sum of junior classes beneath each note)
- **Overcollateralization (OC)** — initial, target, and floor (as % of pool)
- **Reserve account** — initial deposit and required floor
- **Excess spread** (annualised, approximate)
- **Yield-supplement overcollateralization amount (YSOA)** for auto, if present

### 5. Collateral / pool summary
Aggregate principal balance, number of receivables, **WA APR**, **WA original &
remaining term**, **WA / non-zero WA FICO**, **seasoning**, **new/used mix**, top
**geographic** concentrations, obligor concentration, and any pool eligibility limits.

### 6. Performance triggers
The **cumulative net loss trigger** schedule (by months-since-closing), the
**delinquency trigger**, and **OC target step-ups** — plus the **consequence** of a
breach (switch to sequential pay, accelerate OC build, trap cash).

### 7. Mechanics
Priority-of-payments summary (hand off to payment-waterfall-extraction for detail),
**optional redemption / clean-up call** (e.g. 10% of the initial pool balance),
**events of default**, and representation-and-warranty **repurchase** obligations.

## Output
Lead with a one-paragraph deal description, then: a **tranche table**, a
**credit-enhancement table** (layer → amount → % → which classes it supports), a
**collateral table**, and a **triggers** list. Cite the source filing URL. Mark any
field the prospectus does not state as **"not disclosed"** — never infer a number.
Offer `/extract-waterfall` and `/analyze-loan-tape` as follow-ups.
