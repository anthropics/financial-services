# Loan-level output schemas (`extract_loan_level`)

Target output formats for the analyses that only the Form ABS-EE loan tape can produce. This is
a **build spec** — the shapes `extract_loan_level` (and the `loan-tape-analysis` skill) should
return — not extracted figures. Example rows are marked **illustrative**.

Every metric here derives from the Reg AB II **Schedule AL (automobile)** asset-level fields the
connector already maps in `regions/us/field_maps`. A field-provenance table is at the end.

---

## Implementation status

| Section | Status | Tool surface |
|---|---|---|
| §1 Pool summary | ✅ shipped | `extract_loan_level` — now adds delinquency buckets, 60+ %, and period net loss |
| §2 Single-dim stratification | ✅ shipped | `extract_loan_level(stratify_by=["fico_band"])` |
| §3 Cross-tab | ✅ shipped | `extract_loan_level(stratify_by=["fico_band","state"])` |
| §4 Roll-rate matrix | ✅ shipped | `extract_loan_timeseries(analysis="roll_rate")` |
| §5 Static-pool loss curve | ✅ shipped | `extract_loan_timeseries(analysis="static_pool_loss")` |
| §6 Prepayment | 🟡 best-effort | `extract_loan_timeseries(analysis="prepayment")` — pool paydown + voluntary-payoff tally; true voluntary SMM needs `scheduledPrincipalAmount`, not always on the tape |

Cumulative net loss is a deal-life figure, so it is produced by §5 (stacked tapes), not a single tape. All of the above are covered by offline tests in `connector/tests/test_connector.py` (40 checks).

## Conventions

- **Weighting** — averages are balance-weighted on `reportingPeriodActualEndBalanceAmount`
  (current loan balance) unless a column says `count`.
- **FICO bands** — `<550 / 550–599 / 600–649 / 650–699 / 700+`. Edges configurable; source is
  `obligorCreditScore` (only where `obligorCreditScoreType` is a comparable model — flag mixed types).
- **Delinquency** — from `currentDelinquencyStatus` (days past due) → buckets
  `current / 31–60 / 61–90 / 91+`; `60+` = 61+ combined.
- **Net loss** — `chargedoffPrincipalAmount − recoveredAmount` in the period; cumulative net loss
  `% = Σ net loss ÷ original pool balance`.
- **Prepayment** — voluntary payoff flagged by `zeroBalanceCode` = voluntary prepayment; report
  `SMM → CPR` (annualised) and auto-market `ABS`.
- **Period key** — `reportingPeriodEndingDate`; loans keyed across months on `assetNumber`.

---

## 1. Pool summary (header object)

Returned with every call as context.

```json
{
  "deal": "AMCAR 2024-1", "cik": "0002020251",
  "as_of_period": "2026-04-30", "transaction_month": 24,
  "n_loans": "‹tape›", "current_balance": "‹tape›", "pool_factor_pct": "‹tape›",
  "wa_apr_pct": "‹tape›", "wa_remaining_term": "‹tape›", "wa_original_term": "‹tape›",
  "wa_fico": "‹tape›", "avg_balance": "‹tape›",
  "cumulative_net_loss_pct": "‹tape›", "dq_60plus_pct": "‹tape›"
}
```

---

## 2. Single-dimension stratification

One row per bucket of a chosen `dimension`.

`dimension ∈ { fico_band, state, orig_term_band, new_used, vehicle_make, pti_band, model_year, income_verification }`

| Column | Type | Definition |
|---|---|---|
| `bucket` | string | The band/category value |
| `n_loans` | int | Count of loans in bucket |
| `current_balance` | number | Σ current balance |
| `pct_of_pool` | % | Bucket balance ÷ pool balance |
| `wa_apr` | % | Balance-weighted `originalInterestRatePercentage` |
| `wa_remaining_term` | months | Balance-weighted remaining term |
| `cum_net_loss_pct` | % | Cumulative net loss ÷ bucket original balance |
| `dq_60plus_pct` | % | 60+ dpd balance ÷ bucket balance |
| `cdr_annualised` | % | Annualised conditional default rate |

Illustrative (`dimension = fico_band`):

| bucket | n_loans | pct_of_pool | wa_apr | cum_net_loss_pct | dq_60plus_pct |
|---|---|---|---|---|---|
| <550 | _illus._ | 18% | 19.1% | 9.5% | 6.1% |
| 550–599 | _illus._ | 34% | 16.9% | 6.8% | 4.0% |
| 600–649 | _illus._ | 30% | 14.8% | 4.2% | 2.3% |
| 650–699 | _illus._ | 15% | 12.6% | 2.3% | 1.1% |
| 700+ | _illus._ | 3% | 10.9% | 1.1% | 0.4% |
| **Pool** | 73,190 | 100% | 16.18% | **5.83%** | — |

> The bottom row is the 10-D figure; every row above it is the differentiator.

---

## 3. Cross-tab (two dimensions)

A matrix of one `cell_metric` over `row_dimension × col_dimension`
(e.g. `fico_band × state`, `cell_metric = cum_net_loss_pct`).

```json
{
  "row_dimension": "fico_band", "col_dimension": "state",
  "cell_metric": "cum_net_loss_pct",
  "cols": ["TX","FL","OH","CA","other"],
  "rows": [
    { "bucket": "<550",    "cells": ["‹tape›", "...", "...", "...", "..."], "row_total": "‹tape›" },
    { "bucket": "550–599", "cells": ["‹tape›", "...", "...", "...", "..."], "row_total": "‹tape›" }
  ],
  "col_totals": ["‹tape›", "..."]
}
```

Answers questions the pool average cannot, e.g. *"is the Texas concentration low-FICO or
high-FICO?"* Also report each tail's **share of losses vs share of balance** (e.g. the <550
slice).

---

## 4. Roll-rate / transition matrix

Requires **two consecutive tapes**, joined on `assetNumber`. States:
`Current, 31–60, 61–90, 91+, Default/Charge-off, Prepaid`.

| Column | Type | Definition |
|---|---|---|
| `from_state` | string | Delinquency state at period *t* |
| `to_*` | % | Share (balance- or count-weighted) migrating to each state at *t+1* |

```json
{ "period_from": "2026-03-31", "period_to": "2026-04-30", "basis": "balance",
  "matrix": [
    { "from_state": "Current", "to_current": "‹tape›", "to_31_60": "‹tape›", "to_61_90": 0, "to_91plus": 0, "to_default": 0, "to_prepaid": "‹tape›" },
    { "from_state": "31–60",   "to_current": "‹tape›", "to_31_60": "‹tape›", "to_61_90": "‹tape›", "to_91plus": 0, "to_default": 0, "to_prepaid": "‹tape›" }
  ] }
```

The diagonal is "stayed"; the upper triangle is curing, the lower triangle is rolling worse. This
is the single most useful output a stacked tape produces and is **impossible** from any aggregate report.

---

## 5. Static-pool cumulative loss curve

From stacked tapes — cumulative net loss (and CDR) by **months-on-book**, for the whole pool or a
sub-cohort (any dimension bucket from §2).

| Column | Type | Definition |
|---|---|---|
| `month_on_book` | int | Seasoning since deal close |
| `cum_net_loss_pct` | % | Cumulative net loss ÷ original (cohort) balance |
| `cdr_annualised` | % | Period CDR, annualised |
| `pool_factor_pct` | % | Remaining balance ÷ original |

Enables cohort comparison (e.g. <550 vs 600–649 loss timing) and benchmarking one vintage against another.

---

## 6. Prepayment by cohort

`cohort_dimension × period → speeds`.

| Column | Type | Definition |
|---|---|---|
| `cohort` | string | Bucket (e.g. term band, FICO band) |
| `period` | date | Reporting period |
| `smm` | % | Single-month mortality |
| `cpr` | % | SMM annualised |
| `abs_speed` | % | Auto-market ABS prepayment speed |

---

## Field provenance

| Output | ABS-EE Schedule AL field(s) |
|---|---|
| FICO band, WA FICO | `obligorCreditScore`, `obligorCreditScoreType` |
| State | `obligorGeographicLocation` |
| APR | `originalInterestRatePercentage` |
| Term bands | `originalLoanTerm`, remaining = f(`loanMaturityDate`, period) |
| New/used, make, model-year | `vehicleNewUsedCode`, `vehicleManufacturerName`, `vehicleModelYear` |
| PTI band | `paymentToIncomePercentage` |
| Income/employment verification | `obligorIncomeVerificationLevelCode`, `obligorEmploymentVerificationCode` |
| Balance, pool factor | `reportingPeriodActualEndBalanceAmount`, `originalLoanAmount` |
| Delinquency states | `currentDelinquencyStatus` |
| Net loss, recoveries | `chargedoffPrincipalAmount`, `recoveredAmount`, `repossessedProceedsAmount` |
| Prepayment | `zeroBalanceCode`, `zeroBalanceEffectiveDate`, `actualPrincipalCollectedAmount` |

*Coverage caveat — loan-level tapes exist only for deals issued from late 2016 (Reg AB II) and
only for auto, CMBS, RMBS, and debt asset classes. Never credit cards or CLOs.*
