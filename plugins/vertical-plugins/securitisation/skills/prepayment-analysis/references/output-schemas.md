# Output schemas — multi-tape analyses (`extract_loan_timeseries`)

The shapes `extract_loan_timeseries` returns and the shapes this skill's deliverables
should follow. Example values are placeholders (`‹tape›`) — never present them as
extracted figures. Single-tape shapes (pool summary, stratifications, cross-tabs) live
with the single-tape skill:
[`skills/loan-tape-analysis/references/output-schemas.md`](../../loan-tape-analysis/references/output-schemas.md).

## Conventions

- **Net loss** — `chargedoffPrincipalAmount − recoveredAmount` in the period; cumulative net loss
  `% = Σ net loss ÷ original pool balance`. Cumulative net loss is a **deal-life** figure and is
  only produced from stacked tapes.
- **Prepayment** — voluntary payoff flagged by `zeroBalanceCode` = voluntary prepayment; report
  `SMM → CPR` (annualised) and the auto-market `ABS` speed.
- **Period key** — `reportingPeriodEndingDate`; loans are joined across months on `assetNumber`.
  That join is only as reliable as the identifier — reconcile joined loan counts to each
  period's pool count before trusting roll-rate or static-pool output (see the skill's
  data-quality caveat).

## 1. Roll-rate / transition matrix (`analysis="roll_rate"`)

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

## 2. Static-pool cumulative loss curve (`analysis="static_pool_loss"`)

From stacked tapes — cumulative net loss (and CDR) by **months-on-book**, for the whole pool or a
sub-cohort (any single-tape stratification bucket).

| Column | Type | Definition |
|---|---|---|
| `month_on_book` | int | Seasoning since deal close |
| `cum_net_loss_pct` | % | Cumulative net loss ÷ original (cohort) balance |
| `cdr_annualised` | % | Period CDR, annualised |
| `pool_factor_pct` | % | Remaining balance ÷ original |

Enables cohort comparison (e.g. <550 vs 600–649 loss timing) and benchmarking one vintage against another.

## 3. Prepayment by cohort (`analysis="prepayment"`)

`cohort_dimension × period → speeds`.

| Column | Type | Definition |
|---|---|---|
| `cohort` | string | Bucket (e.g. term band, FICO band) |
| `period` | date | Reporting period |
| `smm` | % | Single-month mortality |
| `cpr` | % | SMM annualised |
| `abs_speed` | % | Auto-market ABS prepayment speed |

**Best-effort caveat:** the tool reports pool paydown speed plus a voluntary-payoff
tally. A true voluntary-only SMM needs `scheduledPrincipalAmount`, which is not always
populated on the tape — say which basis the output used.

*Coverage caveat — loan-level tapes exist only for deals issued from late 2016 (Reg AB II) and
only for auto, CMBS, RMBS, and debt asset classes. Never credit cards or CLOs.*
