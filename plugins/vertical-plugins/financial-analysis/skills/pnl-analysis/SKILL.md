---
name: pnl-analysis
description: Analyse a profit & loss statement — revenue breakdown, cost structure, margin trends, period-over-period movements. Triggers on "analyse P&L", "review income statement", "explain this profit and loss", "what's driving the margin", "P&L drill-down", "analyse revenue", "cost analysis", "why are we losing money", "profitability analysis".
---

# P&L Analysis

Structured analysis of a profit & loss statement from uploaded data, a file, or typed figures.

## Step 1: Understand the request

Clarify before diving in:
- **Time horizon**: single period, YoY, or multi-period trend?
- **Comparison base**: actual vs. budget, vs. prior period, vs. prior year, or standalone?
- **Depth**: headline KPIs only, or full line-item drill-down?

If the user uploaded a file (Excel, CSV, or PDF), parse it first.

---

## Step 2: Build the P&L summary

Structure output as a table with these standard sections:

| Line | Period | Prior | Δ (£/$/€) | Δ (%) | Notes |
|------|--------|-------|-----------|-------|-------|

**Standard sections:**

1. **Revenue** — by product/segment if available
2. **Cost of Sales / COGS**
3. **Gross Profit** → Gross Margin %
4. **Operating Expenses** — broken into SG&A, R&D, D&A where available
5. **EBITDA** → EBITDA Margin %
6. **EBIT / Operating Profit** → EBIT Margin %
7. **Interest & Financing Costs**
8. **PBT (Profit Before Tax)**
9. **Tax Charge** → Effective Tax Rate %
10. **Net Profit / (Loss)** → Net Margin %

---

## Step 3: Identify key drivers

For each material movement (>5% of revenue or >10% YoY/vs budget):
- **Quantify**: £X / X% impact
- **Categorise**: Volume, Price/Rate, Mix, FX, Cost inflation, One-off
- **Explain**: brief root-cause sentence

Flag any line items that are:
- **Losses**: negative gross profit, operating losses, net losses
- **Margin compression**: GM or EBITDA margin declining more than 2pp
- **Unusual items**: one-offs, write-downs, exceptional charges
- **Missing data**: expected line items not present in source

---

## Step 4: Trend analysis (if multi-period)

If 3+ periods are available:
- Identify revenue CAGR
- Margin expansion/compression trend
- Turning points — where did profit/loss inflect?
- Forward-looking commentary if guidance exists

---

## Step 5: Output

Deliver in this order:
1. **Headline read** (2–3 sentences): overall profit/loss position, key takeaway
2. **P&L summary table** (Step 2 format)
3. **Drivers section** (Step 3 format)
4. **Red flags**: any lines requiring management attention or further investigation
5. **Trend commentary** if multi-period

**Never fabricate missing figures.** Label gaps as `[N/A]` or `[not provided]`.

---

## Notes

- Follow whatever currency/unit convention is in the source document
- If the source data is inconsistent (mixed scales, missing periods), flag it before proceeding
- Distinguish **reported** vs **adjusted/underlying** figures — note which you're using
