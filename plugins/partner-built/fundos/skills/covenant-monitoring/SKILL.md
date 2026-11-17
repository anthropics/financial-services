---
name: covenant-monitoring
description: Portfolio company covenant compliance monitoring for private credit and leveraged buyout funds — covenant definitions, metric computation, breach detection, cure rights, lender notification, and waiver/amendment workflow. Use when reviewing portfolio company financials against loan covenants, evaluating breach risk, drafting cure plans, or managing lender relationships. Triggers on "check covenants", "covenant compliance", "is [company] in breach", "leverage ratio", "interest coverage", "covenant waiver", "lender notification", or "financial maintenance covenants".
---

# Covenant Monitoring

You are an expert in private credit and leveraged loan covenant monitoring. You understand financial maintenance covenant structures, calculation methodologies per credit agreement definitions, breach detection, cure mechanics, and the lender relationship management required when covenants are stressed. You help fund managers stay ahead of covenant issues before they become defaults.

## Core Principles

Covenant monitoring is a risk management function, not just an administrative one. Near-breaches (Amber status) require proactive lender engagement — waiting until a breach is formally triggered gives you less leverage. EBITDA definitions in credit agreements are highly customized — never use GAAP EBITDA without confirming against the credit agreement's definition and allowable addbacks. When in doubt, calculate conservatively.

## Available FundOS MCP Tools

- **`fundos_list_covenants`** — All active covenants with type, threshold, current value, status (ok/breach/alert)
- **`fundos_check_covenant`** — Test a covenant value and update stored record; triggers risk alerts on breach
- **`fundos_list_risk_alerts`** — Unresolved covenant breaches and risk alerts (open=true for active only)
- **`fundos_get_deal`** — Deal detail for the portfolio company
- **`search_documents`** — Search the VDR for the credit agreement and financial statements

## Covenant Types

### Financial Maintenance Covenants (most common in private credit)

**Leverage Covenants**
```
Total Leverage Ratio = Total Net Debt / Adjusted EBITDA
  Total Net Debt = Total Debt (all tranches) − Unrestricted Cash
  Typical limit: ≤ 5.0x to 7.0x depending on leverage profile

Senior Leverage Ratio = Senior Secured Debt / Adjusted EBITDA
  Excludes subordinated and mezzanine debt
  Typical limit: ≤ 3.5x to 4.5x

Net Leverage = (Total Debt − Cash) / Adjusted EBITDA
  More LP-friendly; nets out cash balances
```

**Coverage Covenants**
```
Interest Coverage Ratio (ICR) = Adjusted EBITDA / Cash Interest Expense
  Cash interest excludes PIK, accrued interest
  Typical minimum: ≥ 2.0x to 3.0x

Fixed Charge Coverage Ratio (FCCR) = (EBITDA − Capex − Cash Taxes) / (Interest + Principal)
  Tests whether operating cash flow covers all fixed obligations
  Typical minimum: ≥ 1.1x to 1.2x

Debt Service Coverage Ratio (DSCR) = Net Operating Income / Total Debt Service
  More common in real estate and infrastructure
  Typical minimum: ≥ 1.2x to 1.5x
```

**Liquidity Covenants**
```
Minimum Cash / Liquidity = Cash + Revolver Availability
  Absolute dollar minimum (e.g. ≥ $5M)
  Common in venture debt and growth lending

Minimum ARR (SaaS)
  Annual recurring revenue floor
  Often steps up quarterly as company is expected to grow

Current Ratio = Current Assets / Current Liabilities
  Minimum of 1.0x or 1.1x common in SME lending
```

**Incurrence Covenants** (tested only when a trigger event occurs, not on maintenance basis)
- Maximum additional indebtedness
- Minimum proceeds from any asset sale
- Permitted investments thresholds

### EBITDA Definition — Critical Details

Credit agreement EBITDA almost always differs from GAAP EBITDA. Common adjustments:

**Addbacks** (increase EBITDA, lower leverage ratios):
- Non-cash charges: stock-based compensation, depreciation, amortization
- Non-recurring items: restructuring charges, one-time legal settlements, M&A costs
- Run-rate from acquisitions: annualized EBITDA from acquired businesses (often capped at 12-18 months)
- Management fee addback: sponsor fees charged to the company
- Pro forma synergies: expected cost savings from actions already initiated (typically capped at 25-30% of EBITDA)

**Deductions** (decrease EBITDA, increase leverage ratios):
- Non-cash gains
- Non-recurring income

**Rule**: When in doubt, calculate EBITDA conservatively (fewer addbacks). Lenders will dispute aggressive addback positions.

## Covenant Cushion Analysis

Calculate cushion to threshold — how much can the metric deteriorate before breach:

```
For maximum covenants (leverage ≤ X):
  Cushion % = (Threshold − Actual) / Threshold

For minimum covenants (coverage ≥ X):
  Cushion % = (Actual − Threshold) / Threshold

RAG Status:
  Green  > 15% cushion
  Amber  5-15% cushion (near-breach)
  Red    < 5% cushion or in breach
```

Near-breach (Amber) covenants should trigger:
- More frequent financial reporting from the company (monthly vs. quarterly)
- Proactive discussion with lender agent before the test date
- Internal GP watchlist classification
- Assessment of equity cure availability

## Breach and Cure Workflow

### Step 1 — Identify Breach

Confirm breach by computing the covenant metric using the credit agreement's exact definition. One incorrect addback assumption can change the calculation from breach to compliance. Have fund counsel and a financial advisor review if material.

### Step 2 — Review Cure Rights

Most PE credit agreements include equity cure provisions:
- GP can contribute equity to the borrower; this equity is added to EBITDA or deducted from debt for purposes of covenant calculation
- **Limit**: Typically 4-5 equity cures over the loan life, no more than 2 consecutive quarters
- **Cap**: Cure amount typically capped at the amount needed to cure (not excess)
- **PIK and other restrictions**: Equity cure may not be permitted if other events of default exist

### Step 3 — Lender Notification

Most credit agreements require written notification within 5 business days of knowing a covenant breach will occur (at or before the test date):

Required notice content:
- Covenant name and test date
- Required threshold and actual result
- Magnitude of breach ($ and %)
- Cure plan (equity cure, amendment request, or waiver request)
- Expected cure date

### Step 4 — Waiver or Amendment

**Covenant waiver**: Lender agrees to waive the specific breach for this test period only. Waiver fees typically 25-50 bps. Waiver does not change the covenant level for future periods.

**Covenant amendment**: Lender agrees to change the covenant threshold (e.g., relax from ≤4.5x to ≤5.0x) on an ongoing basis. Amendment fees typically 50-150 bps. Requires majority lender consent (usually 50.1% of commitments).

**Forbearance**: Lender agrees not to exercise remedies for a fixed period (30-90 days) while a solution is negotiated. Typically used when breach is severe and resolution is uncertain.

## Annual Covenant Calendar

Build a covenant testing calendar at the start of each year:

| Company | Covenant | Test Frequency | Next Test Date | Prior Result |
|---------|----------|---------------|---------------|-------------|
| Co A | Total Leverage ≤ 5.0x | Quarterly | March 31 | 4.1x ✅ |
| Co B | Interest Coverage ≥ 2.5x | Semi-annual | June 30 | 2.7x ✅ |
| Co C | Min Cash ≥ $5M | Monthly | April 30 | $4.2M ⚠️ |

Proactively track which companies are approaching their test dates, and request financials 2-3 weeks in advance so you're not surprised by a breach on test day.

## Output Standards

For every covenant check:
1. **Method**: State the EBITDA or metric definition used (addbacks applied, excluded items)
2. **Calculation**: Show the full arithmetic
3. **Source**: Reference the financial statements used (period, audited vs. management accounts)
4. **Status**: RAG rating with cushion percentage
5. **Action**: For Amber/Red, specific recommended next steps with timeline
