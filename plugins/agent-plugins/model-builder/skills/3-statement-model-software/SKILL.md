---
name: 3-statement-model-software
description: Build or complete a 3-statement financial model for SaaS and software companies. Extends the base 3-statement-model skill with a revenue_build tab containing software-specific KPIs (ARR, NRR, GRR, RPO, cRPO, customer cohort tiers) and multiple revenue forecasting methodologies. Use when the company is a software or SaaS business and you need to model subscription / recurring revenue dynamics. Triggers include requests to model a SaaS company, build a software model, populate ARR or NRR metrics, or forecast subscription revenue.
---

# 3-Statement Model — Software / SaaS Extension

This skill **extends** the base [`3-statement-model`](../3-statement-model/SKILL.md) skill. All principles, formatting conventions, validation checks, and step-by-step verification workflow defined there apply here without exception. Read that skill first, then return here for the software-specific additions.

## What This Skill Adds

1. **`revenue_build` tab** — software KPIs for the last 3 historical years + forward projections using one of five forecasting methodologies
2. **Multiple revenue forecast methodologies** — the user or model selects the best fit based on available data (see [references/revenue-forecasting.md](references/revenue-forecasting.md))
3. **IS linkages** — subscription and professional services revenue on the IS tab are **formula-linked** from `revenue_build`; the IS never contains hardcoded revenue figures in projection columns
4. **Extended Assumptions tab** — software-specific drivers (NRR, GRR, new logo ARR, tier mix, price escalation) added below the standard IS/CF/WC drivers

---

## ⚠️ Critical Rules for Software Models

1. **Revenue always flows from `revenue_build` → IS.** Never hardcode projected revenue in the IS projection columns. The IS subscription revenue cell must be `=revenue_build!<ref>`.
2. **Historical KPIs are hardcoded inputs (blue font)** in `revenue_build`. All projection KPIs are formulas referencing the Assumptions tab.
3. **ARR ≠ Revenue.** ARR is an annualized snapshot of contracted recurring revenue at a point in time. Revenue is earned over the period. For a pure subscription business: Revenue ≈ Average ARR during the period (beginning ARR + ending ARR) / 2 × (1 if annual billing, or use billing timing adjustment). Always document the billing timing assumption.
4. **NRR includes expansion; GRR excludes expansion.** GRR ≤ 100% by definition (contraction + churn only). NRR can exceed 100% if expansion outpaces churn.
5. **Choose one primary methodology** to drive IS revenue; show other methodologies as cross-checks in a separate section of `revenue_build`.

---

## Tab Structure

Add `revenue_build` to the standard tab set. Insert it **before** the IS tab so the dependency chain is clear:

| Tab | Contents |
|-----|----------|
| **revenue_build** | SaaS KPIs, ARR bridge, forecasting, IS revenue linkage |
| IS | Income Statement — subscription revenue **linked from revenue_build** |
| BS | Balance Sheet |
| CF | Cash Flow Statement |
| WC | Working Capital |
| DA | D&A / PP&E Schedule |
| Debt | Debt Schedule |
| Assumptions | All drivers — base + software-specific |
| Checks | Integrity checks + software-specific validations |

---

## `revenue_build` Tab Layout

### Column Structure

| Col | A | B | C | D | E | F | G |
|-----|---|---|---|---|---|---|---|
| | Labels | FY[T-2]A | FY[T-1]A | FY[T]A | FY[T+1]E | FY[T+2]E | FY[T+3]E |

Hardcoded inputs = blue font. Formula cells = black. Cross-sheet links = green.

---

### Section 1 — KPI Dashboard (Historical Actuals + Projections)

Populate with 3 years of historical actuals (hardcoded, blue) and project each KPI forward (formulas, black/green).

```
Row 1:  [COMPANY] — REVENUE BUILD & SOFTWARE KPIs          (dark blue header, merged A1:G1)
Row 2:  ($ in millions, unless noted)                      (subtitle)
Row 3:  [Column headers: FY[T-2]A … FY[T+3]E]             (light blue)

Row 4:  ANNUAL RECURRING REVENUE (ARR)                     (dark blue section)
Row 5:    Beginning ARR                                    (green link to prior year Row 8)
Row 6:    + New Logo ARR                                   (hist: blue input; proj: formula)
Row 7:    + Expansion ARR                                  (hist: blue; proj: formula)
Row 8:    - Contraction ARR                                (hist: blue; proj: formula — negative)
Row 9:    - Churned ARR                                    (hist: blue; proj: formula — negative)
Row 10:   Ending ARR                                       (formula: =B5+B6+B7+B8+B9; MED_BLUE total)
Row 11:   ARR Growth %                                     (formula; italic)
Row 12:   Implied ARR per Customer                         (formula: =B10/B37; italic, $K format)

Row 13: [blank]

Row 14: RETENTION METRICS                                  (dark blue section)
Row 15:   Gross Revenue Retention (GRR) %                  (hist: blue; proj: formula)
Row 16:   Net Revenue Retention (NRR) / Net Dollar Ret. %  (hist: blue; proj: formula)
Row 17:   Gross Churn Rate %                               (formula: =1-B15; italic)
Row 18:   Net Expansion Rate %                             (formula: =B16-B15; italic)
Row 19:   Logo Churn Rate %                                (hist: blue; proj: formula)

Row 20: [blank]

Row 21: REMAINING PERFORMANCE OBLIGATIONS (RPO)            (dark blue section)
Row 22:   Total RPO                                        (hist: blue; proj: formula)
Row 23:   Current RPO (cRPO)                               (hist: blue; proj: formula)
Row 24:   Non-Current RPO                                  (formula: =B22-B23)
Row 25:   cRPO / Total RPO %                               (formula: =B23/B22; italic)
Row 26:   cRPO as % of Next-Year Revenue (coverage)        (formula: =B23/C47; italic — forward-looking)
Row 27:   Total RPO Growth %                               (formula; italic)

Row 28: [blank]

Row 29: CUSTOMER METRICS — BY ACV TIER                     (dark blue section)
Row 30:   Customers > $100K ACV                            (hist: blue; proj: formula)
Row 31:   Customers > $500K ACV                            (hist: blue; proj: formula)
Row 32:   Customers > $1M ACV                              (hist: blue; proj: formula)
Row 33:   Customers > $5M ACV                              (hist: blue; proj: formula)
Row 34:   Total Active Customers                           (hist: blue; proj: formula)
Row 35:   YoY Growth — Customers >$100K                    (formula; italic)
Row 36:   YoY Growth — Customers >$500K                    (formula; italic)
Row 37:   Implied Avg ACV — All Customers ($K)             (formula: =B10/B34; italic)
Row 38:   Implied Avg ACV — >$100K Tier ($K)               (formula: =B10*B39/B30 if tier ARR % known)

Row 39: [blank]

Row 40: REVENUE METRICS                                    (dark blue section)
Row 41:   Subscription Revenue                             (hist: blue; proj: formula — PRIMARY DRIVER)
Row 42:   Professional Services Revenue                    (hist: blue; proj: formula)
Row 43:   Total Revenue                                    (formula: =B41+B42; MED_BLUE total)
Row 44:   Subscription Revenue Growth %                    (formula; italic)
Row 45:   Subscription Revenue as % of Total               (formula; italic)
Row 46:   Implied Billings                                 (formula: =B10-B5+B41; see note)
Row 47:   Billings Growth %                                (formula; italic)
```

**Row 41 (Subscription Revenue) is the anchor cell.** The IS tab references it: `IS!E[sub_row] = "=revenue_build!E41"`.

**Billings formula note:** Billings ≈ Revenue + ΔDeferred Revenue, or alternatively Ending ARR × billing term factor. Use the deferred revenue delta from BS when available: `=B41+(BS!B[def_rev]-BS!A[def_rev])`.

---

### Section 2 — Primary Forecast Methodology

Below the KPI dashboard, add a clearly labeled section for the **selected primary methodology** (chosen in the Assumptions tab). Show the mechanism that produces the Row 41 subscription revenue projection.

Structure for each methodology is detailed in [references/revenue-forecasting.md](references/revenue-forecasting.md).

```
Row 50: [blank]
Row 51: PRIMARY FORECAST METHODOLOGY: [methodology name]   (dark blue header — value from Assumptions)
Row 52:   [Methodology-specific rows — see revenue-forecasting.md]
...
Row 70: Projected Subscription Revenue (primary)           (MED_BLUE total — feeds Row 41 projections)
```

**Row 41 projection formula:** `=revenue_build!B70` (or equivalent row from selected methodology).

---

### Section 3 — Cross-Check Methodologies

Run 1–2 alternative methodologies as sanity checks; compare outputs vs. the primary.

```
Row 72: CROSS-CHECK METHODOLOGIES                          (light blue section header)
Row 73: Method A Output                                    (formula)
Row 74: Method B Output                                    (formula)
Row 75: vs. Primary (Method A delta %)                     (formula: =B73/B70-1; italic)
Row 76: vs. Primary (Method B delta %)                     (formula: =B74/B70-1; italic)
Row 77: [Note: flag if delta > ±15%]
```

---

## Assumptions Tab — Software-Specific Drivers

Add a software section below the standard IS/CF/WC drivers. All cells are blue inputs.

```
[SECTION HEADER: SOFTWARE REVENUE DRIVERS]

Forecast Methodology Selector        [dropdown: ARR Bridge / NRR-Based / Cohort / RPO-Anchored / Top-Down]

--- ARR Bridge Assumptions ---
New Logo ARR Growth % YoY            [FY+1, FY+2, FY+3]
Expansion Rate (% of beginning ARR)  [FY+1, FY+2, FY+3]
Gross Revenue Retention (GRR) %      [FY+1, FY+2, FY+3]
Contraction as % of beginning ARR    [FY+1, FY+2, FY+3]

--- Retention-Based Assumptions ---
Net Revenue Retention (NRR) %        [FY+1, FY+2, FY+3]
Logo Churn Rate %                    [FY+1, FY+2, FY+3]

--- Customer Tier Assumptions ---
Customers >$100K Growth %            [FY+1, FY+2, FY+3]
Customers >$500K Growth %            [FY+1, FY+2, FY+3]
Customers >$1M Growth %              [FY+1, FY+2, FY+3]
Customers >$5M Growth %              [FY+1, FY+2, FY+3]
Avg ACV Escalation %                 [FY+1, FY+2, FY+3]

--- RPO / Backlog Assumptions ---
cRPO Recognition Rate (% recognized next year)  [FY+1, FY+2, FY+3]
RPO Growth %                                     [FY+1, FY+2, FY+3]

--- Professional Services ---
PS Revenue as % of Subscription Revenue         [FY+1, FY+2, FY+3]
```

---

## IS Tab Modifications

**Subscription Revenue projection cells must be green-font cross-sheet links:**

```excel
IS!E[sub_row]  = "=revenue_build!E41"   ← green font
IS!F[sub_row]  = "=revenue_build!F41"   ← green font
IS!G[sub_row]  = "=revenue_build!G41"   ← green font

IS!E[ps_row]   = "=revenue_build!E42"   ← green font
IS!F[ps_row]   = "=revenue_build!F42"   ← green font
IS!G[ps_row]   = "=revenue_build!G42"   ← green font
```

**Total Revenue** on IS remains a formula summing its components (`=E[sub]+E[ps]`), unchanged.

All other IS projection drivers (COGS %, R&D %, S&M %, G&A %, etc.) continue to reference the standard Assumptions tab as in the base skill — only revenue is now sourced from `revenue_build`.

---

## Step-by-Step Build Workflow (Software-Specific Extension)

Follow the base skill's 6-step verification workflow, adding these software checkpoints:

**Before Step 1 (new):** Confirm which KPIs are available from filings/management disclosure:
- Which metrics does the company report publicly? (ARR, NRR, cRPO, etc.)
- Which tier breakpoints does the company use for customer cohorts?
- What billing model applies — annual upfront, monthly, usage-based, or mixed?
- Identify the primary forecasting methodology appropriate for available data

**After Step 1 (template mapping):** Also identify the `revenue_build` tab structure (or confirm it will be created).

**After populating revenue_build:** Show the user:
- Historical KPI table with 3 years of data
- Year-over-year trends in NRR, GRR, ARR growth, customer cohort growth
- Forecast methodology and key assumption sensitivities
- Confirm before proceeding to IS

**After IS projections:** Confirm that:
- IS subscription revenue cells are green links from `revenue_build`
- Revenue growth implied by the model is directionally consistent with KPI trends
- NRR trajectory implies credible expansion vs. churn dynamics

---

## Checks Tab — Software-Specific Additions

Add these checks below the standard integrity checks:

| Check | Formula | Expected |
|-------|---------|----------|
| IS Sub Revenue = revenue_build Sub Revenue | `=IS!E[sub]-revenue_build!E41` | = 0 |
| IS PS Revenue = revenue_build PS Revenue | `=IS!E[ps]-revenue_build!E42` | = 0 |
| ARR Bridge balances (Ending ARR) | `=revenue_build!E10-(revenue_build!E5+revenue_build!E6+revenue_build!E7+revenue_build!E8+revenue_build!E9)` | = 0 |
| GRR ≤ 100% | `=IF(revenue_build!E15>1,"FALSE","TRUE")` | TRUE |
| NRR ≥ GRR | `=IF(revenue_build!E16>=revenue_build!E15,"TRUE","FALSE")` | TRUE |
| cRPO ≤ Total RPO | `=IF(revenue_build!E23<=revenue_build!E22,"TRUE","FALSE")` | TRUE |
| Methodology cross-check delta < 15% | `=IF(ABS(revenue_build!E75)<0.15,"TRUE","FALSE")` | TRUE |

---

## Key KPI Definitions

See [references/software-kpis.md](references/software-kpis.md) for precise definitions of each metric, common disclosure variations, and how to handle non-standard reporting.

## Revenue Forecasting Methodologies

See [references/revenue-forecasting.md](references/revenue-forecasting.md) for detailed mechanics, Excel formula patterns, and when to use each methodology.
