# RiskModels Equity Risk Plugin

Decompose US equity and portfolio risk, pull point-in-time fundamentals, and compute a
CAPM cost of capital using the hosted **RiskModels** MCP — a subscription-light data
source that can stand in for a licensed-terminal connector in equity-risk and valuation
workflows.

## What This Plugin Does

This plugin packages the RiskModels MCP tools into equity-analysis skills that stitch
together multiple tool calls: decompose a name or book into market / sector / subsector /
stock-specific risk with tradeable ETF hedge ratios, build hedge legs scaled to
notionals, and compute cost of equity / WACC / economic profit from point-in-time
fundamentals. It is the equity-risk analog of this repo's fixed-income partner analytics.

## The swap thesis

Every data MCP elsewhere in this repo points at a licensed terminal
(`${FACTSET_MCP_URL}`, `${CAPIQ_MCP_URL}`, and peers). RiskModels is a single hosted
MCP — point a `.mcp.json` server entry (or a `data-puller` env var) at
`https://riskmodels.app/api/mcp/sse` to source equity risk decomposition, PIT
fundamentals, and cost of capital without an enterprise data license. Install is free;
usage is billed per call, from $0.005.

## Skills

| Skill | Domain knowledge |
|-------|-----------------|
| `equity-risk-decomposition` | ERM3 L1/L2/L3 cascade, explained-risk attribution, ETF hedge-ratio framing, residual (idiosyncratic) risk |
| `cost-of-capital` | CAPM cost of equity, book-weight WACC, economic profit, caller-supplied ERP and rf-tenor sensitivity |
| `portfolio-hedge` | ETF hedge-leg construction scaled to notionals, Lstar residual isolation, real-holdings resolution |

## Integrations

This plugin connects to the **RiskModels MCP Server**, which serves US equity
factor-risk, fundamentals, cost-of-capital, and hedging tools across these domains:

- **Risk Decomposition** — L1/L2/L3 market / sector / subsector / residual with ETF hedge ratios
- **Fundamentals** — point-in-time quarterly ratios, CAPM cost-of-capital layer, SEC-sourced raw line items
- **Hedging** — position and portfolio ETF hedge legs; Lstar residual isolation
- **Rankings & Signals** — cross-sectional ranks and the residual mean-reversion signal
- **Return Attribution** — daily return split into L1/L2/L3 factor + residual components

See [CONNECTORS.md](CONNECTORS.md) for the complete tool reference.

## Requirements

- A RiskModels API key (free tier available; usage billed per call). Get one at
  **https://riskmodels.app/get-key**.
- Set it in your environment before use:

  ```bash
  export RISKMODELS_API_KEY="rm_agent_live_..."
  ```

  The bundled `.mcp.json` reads `${RISKMODELS_API_KEY}` as a Bearer token.

## Data scope and disclaimers

- **PIT-normalized fundamentals derived from SEC filings and licensed sources.** Raw
  line items are exposed per cell only where the serving value is SEC XBRL (`sec_facts`);
  other cells are derived. The panel is not a full raw-fundamentals feed.
- **Cost of capital is CAPM** (risk-free at the chosen tenor + conditional market beta ×
  caller-supplied ERP); the ERP is never assumed. WACC uses book-value weights.
- **Realized/historical analytics only.** These skills report model outputs —
  decomposition, hedge ratios, ranks, cost of capital — as analyst work product staged
  for human sign-off. RiskModels is an analytical tool, **not an investment adviser**:
  nothing here is a recommendation, price target, or suitability assessment.
