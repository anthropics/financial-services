---
name: cmbs-loan-tape-analysis
description: |
  Analyse Form ABS-EE **commercial-mortgage (CMBS)** loan-level data into a credit
  view — balance-weighted DSCR and debt yield, occupancy, LTV, property-type and
  geographic concentration, the maturity wall, and the largest loans. Tuned for
  conduit/SASB CMBS via the connector's extract_cmbs_loan_level tool.

  **Use when:** the user wants CMBS pool stratifications, debt-service/debt-yield
  metrics, property/geographic concentration, a maturity profile, or a cohort cut
  from an SEC CMBS ABS-EE tape.

  **Not for:** auto ABS (use loan-tape-analysis) or CLOs (no loan-level on EDGAR).
---

# CMBS Loan Tape Analysis (ABS-EE)

Extract a commercial-mortgage credit view with **`extract_cmbs_loan_level`**. The
tape streams record-by-record, so even a large conduit pool is processed with flat
memory; `mode="filter"` isolates a cohort to CSV.

## Key ABS-EE commercial-mortgage fields
| Concept | XML tag(s) |
|---|---|
| Current balance | `reportPeriodEndActualBalanceAmount` |
| Balance at securitisation | `scheduledPrincipalBalanceSecuritizationAmount` |
| NOI / NCF | `mostRecentNetOperatingIncomeAmount` / `mostRecentNetCashFlowAmount` |
| DSCR (NCF / NOI) | `mostRecentDebtServiceCoverageNetCashFlowPercentage` / …`NetOperatingIncome`… |
| Occupancy | `mostRecentPhysicalOccupancyPercentage` |
| Valuation / LTV | `mostRecentValuationAmount` / `securitizationLoanToValuePercentage` |
| Coupon | `reportPeriodInterestRatePercentage` |
| Maturity | `maturityDate`, `remainingTermNumber` |
| Property | `propertyTypeCode`, `propertyState`, `propertyName` |
| Servicing | `servicerWatchlistCode` |

## Metrics (the connector computes these)
- **Balance-weighted DSCR (NCF)** — the headline coverage measure; flag the share of
  pool below 1.25× and below 1.0×.
- **Pool debt yield** = aggregate NOI ÷ current balance — leverage-independent stress
  gauge.
- **WA occupancy**, **WA LTV**, **WA coupon**, **WA remaining term**.
- **Property-type** and **state** concentration (by balance).
- **Maturity profile** — balance by maturity year (the "maturity wall").
- **Largest loans** — top-10 by balance, with type, state, DSCR, occupancy.

## Stratifications
Pass `stratify_by` (one dimension, or two for a cross-tab):
`property_type`, `property_state`, `dscr_band`, `ltv_band`, `occupancy_band`,
`maturity_year`, `watchlist`. Each bucket carries loans, balance, % of pool, WA DSCR,
WA occupancy, WA LTV, and debt yield — e.g. `["property_type", "dscr_band"]` shows
coverage by sector.

## How to read it
- **Concentration:** call out single-property, single-sponsor, property-type
  (e.g. office), or MSA/state concentrations.
- **Credit:** low-DSCR and watchlisted loans, declining occupancy, high LTV.
- **Maturity/refinancing risk:** clustering in a single year, especially for lower-DSCR
  or office collateral.
- **Trends:** a single ABS-EE is point-in-time; pull consecutive monthly tapes via
  `get_deal_filings` (`form_type="ABS-EE"`) to track DSCR/occupancy migration and the
  watchlist over time.

## Output
A pool-metrics header, property-type and state tables, the maturity wall, the top-10
loans, and a concise credit-and-concentration note. Cite the filing and reporting
period; state that figures are point-in-time and balance-weighted. Analytical support
for a professional's review — not investment advice.
