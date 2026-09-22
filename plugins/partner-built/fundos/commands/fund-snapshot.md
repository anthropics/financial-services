---
description: Generate a one-page fund snapshot with capital metrics, DPI/RVPI/TVPI, and portfolio summary
argument-hint: "[fund name, e.g. 'Acme Fund II']"
---

# Fund Snapshot

> This command uses the FundOS MCP server. See the [README](../README.md) for connection requirements.

Generate a concise one-page fund snapshot covering all key fund-level metrics: capital committed, called, deployed, returned, NAV, DPI, RVPI, TVPI, portfolio composition, and recent activity. If the FundOS MCP is connected, pulls live data automatically.

See the **fund-admin** skill for domain knowledge on fund-level reporting, NAV calculation, and ILPA performance reporting standards.

## Workflow

### 1. Pull Live Data (if FundOS MCP connected)

Call in sequence:
1. `fundos_list_fund_accounts` — get fund vehicles and current NAV
2. `fundos_list_lps` — get committed capital and LP roster
3. `fundos_get_pipeline` — get portfolio company list by stage
4. `fundos_list_transactions` — get recent closings and exits
5. `fundos_compute_pnl` (if fund_account_id available) — get period P&L

If MCP is not connected, ask the user for:

- **Fund name**, vintage year, fund life (years), strategy (VC / PE / PC / Real Estate)
- **Capital metrics**: total commitments, total called, management fee, GP commitment
- **Portfolio**: list of companies/assets with cost basis and current FV (or book value for credit)
- **Realizations**: any exits, partial sales, or distributions to date
- **Reporting date**

### 2. Compute Fund Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Total Committed Capital | $XXX,XXX,XXX | Sum of all LP + GP commitments |
| GP Commitment | $X,XXX,XXX | GP co-invest, typically 1-2% |
| Total Called | $XXX,XXX,XXX | All capital calls to date |
| Uncalled / Dry Powder | $XXX,XXX,XXX | Committed minus called |
| % Called | XX.X% | Called / Committed |
| Management Fees (cumulative) | $X,XXX,XXX | Fee paid on committed or invested capital |
| Net Invested Capital | $XXX,XXX,XXX | Called minus fees and fund expenses |
| Realized Proceeds | $XX,XXX,XXX | Cash returned from exits, dividends, coupons |
| Unrealized NAV | $XXX,XXX,XXX | Current FV of remaining portfolio |
| Total Value | $XXX,XXX,XXX | Realized + Unrealized |
| **DPI** | **X.XXx** | Realized / Called (distributions to paid-in) |
| **RVPI** | **X.XXx** | Unrealized / Called (residual value to paid-in) |
| **TVPI** | **X.XXx** | Total Value / Called (total value to paid-in) |
| **Net IRR** | **XX.X%** | Net of fees and carry, since inception |
| Fund Life Elapsed | X.X years | From first close to reporting date |
| Projected End of Investment Period | [Date] | Typically year 5-6 from vintage |

### 3. Portfolio Summary

**By Status**
| Status | Count | Cost Basis | Fair Value | MOIC |
|--------|-------|-----------|-----------|------|
| Active | XX | $XXX,XXX,XXX | $XXX,XXX,XXX | X.Xx |
| Realized | XX | $XX,XXX,XXX | $XX,XXX,XXX | X.Xx |
| Watch List | XX | $X,XXX,XXX | $X,XXX,XXX | X.Xx |
| Written Off | XX | $X,XXX,XXX | $0 | 0.0x |

**By Sector** (top 5)
| Sector | # Companies | % of NAV |
|--------|------------|---------|
| SaaS / Cloud | X | XX% |
| Fintech | X | XX% |
| ...  | ... | ... |

**Top Holdings** (by fair value, top 5)
| Company | Stage | Cost | FV | MOIC | % of Portfolio |
|---------|-------|------|----|------|---------------|
| Co A | Series C | $Xm | $XXm | X.Xx | XX% |
| ...  | ... | ... | ... | ... | ... |

### 4. Recent Activity (last 90 days)

List: new investments, follow-ons, exits, capital calls, notable portfolio events.

### 5. Fund Health Indicators

- **Concentration risk**: Top 3 holdings as % of NAV (flag if >50%)
- **Deployment pace**: % of capital deployed vs. fund age (flag if behind/ahead of typical pace)
- **Follow-on reserves**: Undeployed capital available for follow-ons vs. estimated need
- **Fee drag**: Management fees as % of called capital (benchmark: 1.8-2.0% annually)

### 6. Output

Return:
1. **One-page fund snapshot** — all metrics in a clean summary format
2. **Portfolio tables** — by status, sector, and top holdings
3. **Recent activity** — last 90 days
4. **Health indicators** — concentration, pace, reserves flags

## Important Notes

- NAV for private equity and VC follows ASC 820 / IFRS 13 fair value hierarchy — confirm valuation methodology and date of last mark
- DPI is the most credible metric for mature funds — LPs will focus on this above TVPI in years 6+
- Net IRR requires exact cash flow dates — if dates are approximate, note this in the output
- For private credit funds, replace RVPI/TVPI with yield-based metrics: current yield, realized yield, net IRR, loss rate
- If reporting to an LPAC or institutional LP, follow ILPA Performance Reporting Standards for metric definitions
