---
description: Analyse a CMBS (commercial-mortgage) ABS-EE tape — DSCR, debt yield, property mix, maturity wall
argument-hint: "[deal name, CIK, or accession number]"
---

# Analyse CMBS Loan Tape

> Uses the bundled EDGAR connector — if its tools are missing or erroring, see [CONNECTOR.md](../CONNECTOR.md).

Turn a conduit/SASB CMBS Form ABS-EE loan tape into a commercial-mortgage credit
view: debt-service coverage, debt yield, occupancy, leverage, property-type and
geographic concentration, the maturity profile, and the largest loans.

## Workflow

### Step 1 — Locate the CMBS ABS-EE filing
- With a CIK: call **`get_deal_filings`** with `form_type="ABS-EE"` and pick the
  reporting period.
- With a deal name (e.g. "BMARK 2022-B1", "Benchmark"): find it first with
  **`search_securitisation_deals`** (`asset_class="cmbs"`).

### Step 2 — Load the skill
Use `skill: "cmbs-loan-tape-analysis"` for the metric definitions and the
stratification framework.

### Step 3 — Extract
Call **`extract_cmbs_loan_level`** with the CIK and accession:
- Default (`mode="summary"`) → pool balance, balance-weighted **DSCR (NCF)**,
  occupancy, LTV and coupon, **pool debt yield**, property-type and state mix,
  the **maturity_profile**, and the **largest_loans**.
- `stratify_by` one or two of: `property_type`, `property_state`, `dscr_band`,
  `ltv_band`, `occupancy_band`, `maturity_year`, `watchlist`
  (e.g. `["property_type", "dscr_band"]` for a cross-tab).
- `mode="filter"` with `filters` → isolate a cohort (e.g. low-DSCR or watchlist
  loans) and write it to CSV.

### Step 4 — Deliver
A pool header (balance, WA DSCR, debt yield, occupancy, LTV, WA coupon), the
property-type and state concentration tables, the **maturity wall**, the top-10
loans, and a short credit note (e.g. low-DSCR or watchlisted exposure, maturity
clustering). Cite the filing and reporting period; figures are point-in-time.

## Note
Use this for **commercial mortgages (CMBS)**; use `/analyze-loan-tape` for auto ABS.
Both read Form ABS-EE — there is still **no loan-level data for credit-card ABS or
CLOs** on EDGAR.
