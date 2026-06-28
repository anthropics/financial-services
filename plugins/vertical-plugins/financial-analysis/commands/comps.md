---
description: Build a comparable company analysis with trading multiples
argument-hint: "[company name or ticker]"
---

# Comparable Company Analysis Command

Build an institutional-grade comparable company analysis with operating metrics, valuation multiples, and statistical benchmarking.

## Workflow

### Step 1: Gather Company Information

If a company name or ticker is provided, use it. Otherwise ask:
- "What company would you like to analyze?"

### Step 2: Load Comps Analysis Skill

Use `skill: "comps-analysis"` to build the analysis:

1. **Clarify the analysis purpose**:
   - "What's the key question?" (valuation, efficiency, growth comparison)
   - "Who is the audience?" (IC, board, quick reference)
   - "Do you have a preferred format or template?"

2. **Identify peer group** (4-6 comparable companies):
   - Similar business model
   - Similar scale/market cap range
   - Same industry/sector
   - Geographic comparability

3. **Gather data** (prioritize MCP sources if available):
   - Operating metrics: Revenue, Growth, Gross Margin, EBITDA, EBITDA Margin
   - Valuation: Market Cap, Enterprise Value, EV/Revenue, EV/EBITDA, P/E
   - Additional metrics based on industry (Rule of 40 for SaaS, etc.)

4. **Build the analysis**:
   - Operating Statistics section with company data + statistics (Max, 75th, Median, 25th, Min)
   - Valuation Multiples section with same statistical summary
   - Notes & Methodology documentation

### Step 3: Create Excel Output

Generate Excel file with:
- Header block (analysis title, companies, date, units)
- Operating Statistics & Financial Metrics section
- Valuation Multiples section
- Statistical summary for each metric
- Notes section documenting sources and methodology

### Step 4: Deliver Output

Provide:
1. **Excel file** (.xlsx) - the comps analysis
2. **Summary** highlighting:
   - Peer group selection rationale
   - Key insights (who trades at premium/discount)
   - Median multiples for reference

## Output Format Reference

```
┌─────────────────────────────────────────────────────────────────┐
│ [SECTOR] - COMPARABLE COMPANY ANALYSIS                          │
│ [Company 1] • [Company 2] • [Company 3] • [Company 4]          │
│ As of [Date] | All figures in USD Millions                      │
├─────────────────────────────────────────────────────────────────┤
│ OPERATING STATISTICS & FINANCIAL METRICS                        │
├──────────┬─────────┬─────────┬──────────┬─────────┬────────────┤
│ Company  │ Revenue │ Growth  │ Gross    │ EBITDA  │ EBITDA     │
│          │ (LTM)   │ (YoY)   │ Margin   │ (LTM)   │ Margin     │
├──────────┼─────────┼─────────┼──────────┼─────────┼────────────┤
│ [Data rows for each company]                                    │
│                                                                 │
│ Maximum  │ =MAX    │ =MAX    │ =MAX     │ =MAX    │ =MAX       │
│ 75th %   │ =QUART  │ =QUART  │ =QUART   │ =QUART  │ =QUART     │
│ Median   │ =MEDIAN │ =MEDIAN │ =MEDIAN  │ =MEDIAN │ =MEDIAN    │
│ 25th %   │ =QUART  │ =QUART  │ =QUART   │ =QUART  │ =QUART     │
│ Minimum  │ =MIN    │ =MIN    │ =MIN     │ =MIN    │ =MIN       │
├─────────────────────────────────────────────────────────────────┤
│ VALUATION MULTIPLES                                             │
├──────────┬──────────┬──────────┬──────────┬───────────┬────────┤
│ Company  │ Mkt Cap  │ EV       │ EV/Rev   │ EV/EBITDA │ P/E    │
├──────────┼──────────┼──────────┼──────────┼───────────┼────────┤
│ [Data rows + statistics]                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Industry-Specific Metrics

| Industry | Additional Metrics |
|----------|-------------------|
| Software/SaaS | ARR, Net Dollar Retention, Rule of 40 |
| Retail | Same-store sales, Inventory Turns |
| Financials | ROE, ROA, Efficiency Ratio |
| Manufacturing | Asset Turnover, CapEx/Revenue |
| Healthcare | R&D/Revenue, Pipeline Value |

## Quality Checklist

Before delivery:
- [ ] 4-6 truly comparable companies
- [ ] Consistent time periods (all LTM or all FY)
- [ ] All formulas reference cells (no hardcoded values)
- [ ] Cell comments on all hardcoded inputs with sources
- [ ] Statistics include Max, 75th, Median, 25th, Min
- [ ] Notes section documents sources and methodology
- [ ] Blue = inputs, Black = formulas
- [ ] Sanity checks pass (margins logical, multiples reasonable)
