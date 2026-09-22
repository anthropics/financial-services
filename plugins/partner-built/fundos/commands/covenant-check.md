---
description: Evaluate portfolio company covenant compliance and flag breaches or near-breaches
argument-hint: "[company name, e.g. 'Acme Corp Q1 2026 financials']"
---

# Covenant Check

> This command uses the FundOS MCP server. See the [README](../README.md) for connection requirements.

Evaluate a portfolio company's current financial metrics against all loan covenants. Produce a RAG (Red / Amber / Green) compliance dashboard, flag any breaches or near-breaches, and draft a breach notice if required.

See the **covenant-monitoring** skill for domain knowledge on covenant structures, cushion analysis, and cure rights.

## Workflow

### 1. Gather Inputs

If FundOS MCP is connected, call `fundos_list_covenants` to retrieve active covenants for the portfolio company. If not connected, ask for:

- **Portfolio company name**
- **Reporting period** (e.g. Q1 2026, LTM ended March 31 2026)
- **Covenant definitions** — for each covenant:
  - Covenant name (e.g. Total Leverage Ratio)
  - Threshold (e.g. ≤ 5.0x)
  - Direction (maximum or minimum)
  - Test frequency (quarterly, semi-annual, annual)
  - Cure rights (equity cure permitted? how many times per LPA/credit agreement?)
- **Current financials** to compute actuals:
  - Total debt (current + long-term)
  - EBITDA (LTM, adjusted per credit agreement definition)
  - Cash interest expense (LTM)
  - Cash and liquid assets
  - Revenue (LTM)
  - Any credit agreement-defined adjustments (addbacks, run-rate, synergies)

### 2. Compute Covenant Metrics

For each standard covenant type:

**Leverage Covenants**
```
Total Leverage Ratio = Total Net Debt / Adjusted EBITDA
Senior Leverage Ratio = Senior Debt / Adjusted EBITDA
```

**Coverage Covenants**
```
Interest Coverage Ratio (ICR) = Adjusted EBITDA / Cash Interest Expense
Fixed Charge Coverage Ratio (FCCR) = (EBITDA - Capex - Taxes) / (Interest + Debt Service)
```

**Liquidity Covenants**
```
Minimum Liquidity = Cash + Revolving Credit Facility Availability
Current Ratio = Current Assets / Current Liabilities
```

**Other Common Covenants**
```
Maximum Capex = Actual Capex vs. Annual Limit
Revenue Run-Rate = LTM Revenue vs. Minimum Threshold
ARR (SaaS) = Annualized Recurring Revenue vs. Minimum Threshold
```

### 3. RAG Compliance Dashboard

For each covenant, assign status:
- **Green** — actual is within covenant with >15% cushion
- **Amber** — actual is within covenant but within 15% of the threshold (near-breach)
- **Red** — actual breaches the covenant threshold

| Covenant | Threshold | Actual | Cushion | Status |
|----------|-----------|--------|---------|--------|
| Total Leverage | ≤ 5.0x | X.Xx | XX% | 🟢 Green |
| Interest Coverage | ≥ 2.5x | X.Xx | XX% | 🟡 Amber |
| Minimum Liquidity | ≥ $5M | $X.XM | XX% | 🔴 Red |
| Total Capex | ≤ $5M | $X.XM | XX% | 🟢 Green |

### 4. Breach Analysis

For each Red or Amber covenant:

- **Breach severity**: Threshold miss by X% / $Xm
- **Cure rights**: Equity cure available? Number of cures remaining per credit agreement
- **Grace period**: How many days from test date to cure deadline
- **Lender notification**: When must the borrower notify lenders
- **Potential consequences**: Default, acceleration risk, fee implications
- **Recommended action**: Cure, waiver request, amendment, or lender discussion

### 5. Draft Breach Notice (if applicable)

If a covenant breach is confirmed, draft a formal lender notification:

```
[Date]

[Lender Name / Agent]
[Address]

Re: [Company Name] — [Credit Agreement Name] — Covenant Compliance Notice

Dear [Agent],

Pursuant to Section [X] of the Credit Agreement dated [date], [Company Name] hereby notifies you
that it has identified a breach of the [Covenant Name] covenant for the test period ended [date].

BREACH DETAILS
Covenant:          [Name]
Required Threshold: [e.g. Total Leverage ≤ 5.0x]
Actual Result:      [e.g. Total Leverage 5.6x]
Cure Deadline:      [Date per credit agreement]

[Company Name] is evaluating its options under the Credit Agreement, including the equity cure
provisions under Section [X]. We will provide a further update by [date].

[Signature Block]
```

### 6. Output

Return:
1. **RAG compliance dashboard** — all covenants with status, actual vs. threshold, cushion
2. **Breach analysis** — detail on any Red/Amber covenants with cure options
3. **Breach notice draft** — if any Red covenants, a ready-to-review lender notification
4. **Trend table** — if prior quarter data provided, show covenant metric trends

## Important Notes

- EBITDA definition varies by credit agreement — addbacks for non-cash items, restructuring, run-rate acquisitions, and management fees must match the credit agreement definition exactly
- Equity cure rights are limited — track cure count carefully (most agreements allow 4-5 over the life, no more than 2 consecutive quarters)
- If FundOS MCP is connected, call `fundos_check_covenant` with `covenant_id` to update stored values and trigger risk alerts automatically
- Lender notification deadlines are typically 5 business days from the covenant test date — breach notices filed late can themselves constitute an event of default
- Near-breach (Amber) covenants warrant proactive lender engagement — don't wait for a breach
