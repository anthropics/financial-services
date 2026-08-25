---
description: Parse an ABS prospectus (424B) into a structured deal summary
argument-hint: "[deal name, CIK, or accession number]"
---

# Parse ABS Prospectus

> Uses the bundled EDGAR connector — if its tools are missing or erroring, see [CONNECTOR.md](../CONNECTOR.md).

Turn a registered ABS prospectus (Form 424B / 424H) into a structured, analyst-grade
summary: parties, capital structure, credit enhancement, collateral, triggers, and
the priority of payments.

## Workflow

### Step 1 — Locate the prospectus
- If given a CIK or accession, use it directly.
- If given a deal/issuer name, call **`search_securitisation_deals`**
  (`form_type="424B5,424B2,424H"`) to find it, then confirm the right one.

### Step 2 — Retrieve the document
Call **`get_filing_document`** with the CIK and accession. Prospectuses are long —
page through with `offset` / `max_chars` as needed, focusing on the capital
structure, credit enhancement, collateral, and priority-of-payments sections.

### Step 3 — Load the skill
Use `skill: "abs-prospectus-analysis"` for the section map and the fields to extract.

### Step 4 — Extract & structure
Produce: deal identity (issuer, shelf, closing date, asset class), the **tranche
table** (class, size, coupon/benchmark, expected WAL, rating, credit enhancement,
subordination), the **credit-enhancement stack** (subordination, OC, reserve
account, excess spread), the **collateral summary**, and the **performance triggers**.

### Step 5 — Deliver
A clean summary (tables for the capital structure and enhancement). Offer to follow
with `/extract-waterfall` or `/analyze-loan-tape` for the same deal.

Always cite the source filing URL. Never infer a number that isn't in the document —
mark anything not stated as "not disclosed".
