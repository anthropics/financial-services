---
description: Generate an equity research snapshot — fundamentals, ratios, peer comparables, valuation, and capital allocation for a single US ticker
argument-hint: "<ticker e.g. AAPL> [period e.g. annual|quarterly]"
---

# Research Equity

> This command uses Valuein's fundamentals, valuation, ratios, peer-comparable, and capital-allocation tools. See [CONNECTORS.md](../CONNECTORS.md) for the complete tool reference.

Generate a comprehensive equity research snapshot for a US-listed ticker. Combines standardized financial statements, pipeline-computed ratios, peer benchmarking, valuation metrics, and capital-allocation analysis into a structured research note. Every numeric value is cited to a specific SEC accession via the response's `lineage` envelope.

See the **equity-research** skill for domain knowledge on fundamental analysis, peer interpretation, and valuation framing.

## Workflow

### 1. Gather Input

Ask the user for:
- Ticker symbol (required) — e.g. AAPL, MSFT, NVDA. Case-insensitive; the tool normalises.
- Period type (optional, default annual) — `annual` or `quarterly`.
- Specific focus areas (optional) — e.g. earnings, margins, balance sheet, capital returns.

If the user supplies a company name instead of a ticker, call `search_companies` first to resolve.

### 2. Pull Historical Fundamentals

Call `get_company_fundamentals` with `ticker`, `period`. Request the last 5 fiscal periods.

Extract: revenue trajectory, gross / operating / net margins, EPS trend, total assets / liabilities / equity, cash + total debt, operating cash flow, capex (sign-aware).

Every row carries a `lineage` envelope — preserve the `source_filing` + `source_url` for citation in the output.

### 3. Pipeline Ratios

Call `get_financial_ratios` with `ticker`, `categories: ["profitability", "efficiency", "owner_earnings"]`, `fiscal_period: "FY"`, `limit: 5`.

Extract: ROE, ROIC, gross / operating / net margin trends, FCF yield, owner-earnings per share, days-sales-outstanding, cash conversion cycle.

### 4. Valuation Metrics

Call `get_valuation_metrics` with `ticker`. Returns merged fact-table profitability ratios + DCF inputs from `valuation.parquet` (WACC, terminal growth assumption, computed value per share if a DCF has been pre-run).

### 5. Peer Comparables

Call `get_peer_comparables` with `ticker`, `categories: ["profitability", "valuation", "leverage"]`, `limit: 10`.

Returns the subject + N sector peers with side-by-side ratios. Identify the subject's relative quality and valuation positioning.

### 6. Capital Allocation

Call `get_capital_allocation_profile` with `ticker`. Returns capex, R&D, M&A, dividends, buybacks, debt issuance / repayment plus deployment-mix percentages and red-flag booleans (`buybacks_exceed_fcf`, `debt_funded_distribution`).

### 7. Synthesize

Combine into a structured research note with the output format below.

## Output Format

### Investment Thesis (1-2 sentences)
Lead with the one-line summary of where the company is and why it matters.

### Fundamentals Trajectory
| Metric | FY-4 | FY-3 | FY-2 | FY-1 | FY0 (LTM) | Trend |
|--------|------|------|------|------|-----------|-------|
| Revenue (M) | ... | ... | ... | ... | ... | ... |
| Gross Margin | ...% | ...% | ...% | ...% | ...% | ... |
| Operating Margin | ...% | ...% | ...% | ...% | ...% | ... |
| EPS (diluted) | ... | ... | ... | ... | ... | ... |
| Net Debt / EBITDA | ... | ... | ... | ... | ... | ... |

Cite the SEC accession for the most recent fiscal year (from the lineage envelope on the FY0 row).

### Quality Ratios
| Ratio | Current | 5Y Avg | Trend |
|-------|---------|--------|-------|
| ROE | ...% | ...% | ... |
| ROIC | ...% | ...% | ... |
| FCF Yield | ...% | ...% | ... |
| Owner Earnings / Share | ... | ... | ... |
| Cash Conversion Cycle (days) | ... | ... | ... |

### Peer Comparables
| Metric | Subject | Peer Median | Peer Range | Position |
|--------|---------|-------------|------------|----------|
| Operating Margin | ...% | ...% | ...% – ...% | ... |
| ROIC | ...% | ...% | ...% – ...% | ... |
| Debt / Equity | ... | ... | ... – ... | ... |

### Capital Allocation Scorecard
| Use of Cash | % of OCF | Flag |
|-------------|----------|------|
| Capex | ...% | ... |
| R&D | ...% | informational |
| M&A | ...% | ... |
| Dividends | ...% | ... |
| Buybacks | ...% | ... |
| Debt Repayment | ...% | ... |

Surface the red-flag booleans explicitly if any are true:
- ⚠️ **Buybacks exceed FCF** in the latest period
- ⚠️ **Total returns (buybacks + dividends) exceed FCF**
- ⚠️ **Debt-funded distributions** (distributions exceed FCF AND debt was issued in the same period)

### Valuation Summary
| Metric | Current | Context |
|--------|---------|---------|
| Forward P/E | ... | vs sector / history |
| EV / EBITDA | ... | vs sector / history |
| Computed DCF Value / Share | $... | from valuation.parquet |
| Implied Equity Premium | ...% | (Computed DCF − current price) / current price |

### Bottom Line
- **Strengths** (2-3 bullets): durable margins, capital-return discipline, etc.
- **Risks** (2-3 bullets): leverage trajectory, peer-relative drift, red flags.
- **Conviction**: high / medium / low, with one-sentence justification.

### Sources
Always close with a list of cited filings: `[Accession ID]: <source_url>` for every fact_id surfaced above. Every number must trace back to a specific 10-K / 10-Q.
