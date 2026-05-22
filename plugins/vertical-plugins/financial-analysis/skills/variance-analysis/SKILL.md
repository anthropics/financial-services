---
name: variance-analysis
description: Analyse actual vs budget/forecast/prior-period variances with root-cause attribution and waterfall bridge. Triggers on "variance analysis", "actual vs budget", "actual vs forecast", "why did we miss budget", "budget vs actual", "explain the variance", "what drove the miss", "performance vs plan", "bridge the difference".
---

# Variance Analysis

Compare actuals to a reference baseline (budget, forecast, or prior period) and attribute each variance to its root cause.

## Step 1: Establish the comparison

Determine:
- **Actual period** and **reference baseline** (budget / forecast / prior year / prior quarter)
- **Currency / unit** of measurement
- **Materiality threshold**: default to flagging variances >5% of the baseline line or >$50k — adjust if the user specifies

---

## Step 2: Build the variance table

| Line | Actual | Budget/PY | Variance (£) | Variance (%) | Favourable / Adverse | Root Cause |
|------|--------|-----------|-------------|--------------|---------------------|------------|

For each variance above the materiality threshold, populate the **Root Cause** column with one of:
- **Volume** — more or fewer units sold/produced
- **Price/Rate** — higher or lower price per unit / rate
- **Mix** — shift in product/segment/customer composition
- **Timing** — item is deferred or accelerated vs plan
- **FX** — currency movement
- **Cost inflation** — input cost change (labour, materials, energy)
- **One-off / exceptional** — restructuring, write-down, M&A, non-recurring
- **Scope change** — what was planned is different from what occurred
- **Unknown** — flag for management explanation

---

## Step 3: Waterfall bridge

For the key headline metric (e.g. EBITDA, Net Profit, Revenue), build a verbal waterfall:

> Starting point: Budget EBITDA £X
> + Volume uplift: £X
> − Price/rate headwind: £X
> + Cost saving: £X
> − FX headwind: £X
> = Actual EBITDA £X (£Y / Z% vs budget)

Quantify each bridge step precisely. List items largest-to-smallest impact.

---

## Step 4: Red flags

Flag:
- **Adverse variances >10%** on critical lines (revenue, EBITDA, cash)
- **Pattern variances**: same line is adverse for 2+ consecutive periods
- **Offsetting variances**: large positive and negative items netting to small total — may mask underlying issues
- **Re-forecasting indicators**: actual tracking so far below budget that a re-forecast is warranted

---

## Step 5: Output

1. **Headline** (2–3 sentences): total variance, Favourable or Adverse, key driver
2. **Variance table** (all material lines)
3. **Waterfall bridge** for the primary metric
4. **Red flags** list
5. **Recommended management actions** (if asked)

**All figures must trace to the source data provided.** Do not estimate or interpolate.
