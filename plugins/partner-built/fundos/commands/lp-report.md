---
description: Generate a quarterly LP report with portfolio summary, performance metrics, and investor letter
argument-hint: "[fund name and reporting period, e.g. 'Acme Fund II Q1 2026']"
---

# LP Report

> This command uses the FundOS MCP server. See the [README](../README.md) for connection requirements.

Generate a complete quarterly LP report: investor letter, portfolio company summaries, fund-level performance metrics (DPI, RVPI, TVPI), capital account statement, and notable events.

See the **lp-communications** skill for LP reporting standards, ILPA guidelines, and investor communication best practices.

## Workflow

### 1. Gather Inputs

If FundOS MCP is connected, call `fundos_list_fund_accounts`, `fundos_list_lps`, and `fundos_get_pipeline` to pull live data. If not connected, ask for:

- **Fund name** and reporting period (e.g. Q1 2026, full year 2025)
- **Portfolio companies** — name, sector, ownership %, invested cost, current fair value, stage
- **Fund-level financials** — total committed capital, called capital, total NAV, distributions to date
- **Vintage year** and fund life (e.g. Fund III, 2022 vintage, 10-year fund)
- **Notable events** this quarter — new investments, follow-ons, exits, write-downs, portfolio news
- **Market commentary** — optional GP view on macro / sector environment
- **Tone preference** — formal (institutional LPs) or semi-formal (family offices, angels)

### 2. Compute Performance Metrics

Calculate fund-level KPIs:

| Metric | Value | Formula |
|--------|-------|---------|
| Committed Capital | $XXX,XXX,XXX | Sum of all LP commitments |
| Called Capital | $XXX,XXX,XXX | Total capital contributions received |
| Uncalled Capital | $XXX,XXX,XXX | Committed minus called |
| Total Cost Basis | $XXX,XXX,XXX | Sum of invested amounts at cost |
| Realized Proceeds | $XXX,XXX,XXX | Cash distributions from exits |
| Unrealized Fair Value | $XXX,XXX,XXX | Current portfolio NAV |
| Total Value | $XXX,XXX,XXX | Realized + unrealized |
| DPI | X.XXx | Realized / Called Capital |
| RVPI | X.XXx | Unrealized FV / Called Capital |
| TVPI | X.XXx | Total Value / Called Capital |
| Net IRR | XX.X% | Time-weighted return net of fees/carry |

For venture funds: also compute Ownership %, implied post-money at last round, and fair value methodology.

### 3. Portfolio Summary Table

| Company | Sector | Stage | Cost Basis | FV / Exit Price | MOIC | Status |
|---------|--------|-------|-----------|-----------------|------|--------|
| Co A    | SaaS   | Series B | $X.Xm | $XX.Xm | X.Xx | Active |
| Co B    | Fintech | Seed | $X.Xm | $X.Xm | X.Xx | Active |
| Co C    | Health | Exit | $X.Xm | $XX.Xm | X.Xx | Realized |

Highlight top performers, write-downs, and watch-list companies.

### 4. Draft the Investor Letter

Structure:

**[Fund Name] — [Quarter] Investor Update**

*Dear [LP Name / Limited Partners],*

**Fund Overview** (2-3 sentences — period highlights, where fund is in its life)

**Portfolio Activity** (bullet points — new investments, follow-ons, exits, key milestones)

**Portfolio Company Updates** (3-5 sentences each for material holdings — business progress, metrics, market context)

**Fund Performance** (DPI, RVPI, TVPI table; narrative on drivers of value change)

**Market Commentary** (optional — GP perspective on relevant sectors or macro themes)

**Upcoming Activity** (pipeline, expected calls, anticipated events next quarter)

**Closing** (thank LPs, contact info)

### 5. Output

Return:
1. **Investor letter** — formatted Markdown, one version with LP name placeholder `[LP Name]`
2. **Performance metrics table** — all KPIs with period-over-period comparison if prior period data provided
3. **Portfolio summary table** — all companies with cost/FV/MOIC
4. **Capital account statement** skeleton — contributions, distributions, NAV per LP unit

## Important Notes

- Fair values should follow ASC 820 (US) or IFRS 13 (international) — note the valuation methodology used (recent round, comparable transaction, DCF, etc.)
- Do not state forward-looking performance projections as fact — frame as expectations or plans
- Write-downs and watch-list companies should be disclosed accurately, not buried
- Provide data tables and the letter separately so the GP can adjust the letter narrative without re-running calculations
- ILPA Principles recommend quarterly reporting within 90 days of period end
