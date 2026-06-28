# LSEG Financial Analytics Plugin

Price bonds, analyze yield curves, evaluate FX carry trades, value options, and build macro dashboards using LSEG financial data and analytics.

## What This Plugin Does

This plugin packages LSEG's financial analytics MCP tools into 8 high-level workflows that stitch together multiple tool calls for common financial analysis tasks. Instead of calling individual tools one at a time, each command orchestrates 4-5 tools into a cohesive analysis.

## Commands

| Command | Description |
|---------|-------------|
| `/analyze-bond-rv` | Analyze bond relative value with spread decomposition and scenario stress testing |
| `/analyze-fx-carry` | Evaluate FX carry trade opportunities with spot, forwards, vol surface, and historical context |
| `/research-equity` | Generate equity research snapshot with consensus estimates, fundamentals, and price performance |
| `/analyze-swap-curve` | Analyze the swap curve with government and inflation overlays for curve trade ideas |
| `/analyze-option-vol` | Analyze option volatility with vol surface, Greeks, and implied vs realized comparison |
| `/review-fi-portfolio` | Review a fixed income portfolio with pricing, cashflows, and scenario analysis |
| `/macro-rates` | Build a macro and rates dashboard with economic indicators, yield curves, and swap spreads |
| `/analyze-bond-basis` | Analyze bond futures basis with CTD identification and implied repo rate |

## Skills

Each command is backed by a corresponding skill that provides deep domain knowledge:

| Skill | Domain Knowledge |
|-------|-----------------|
| `bond-relative-value` | Spread frameworks, G-spread/Z-spread/OAS, rich-cheap analysis |
| `fx-carry-trade` | Carry mechanics, carry-to-vol ratios, G10 and EM carry dynamics |
| `equity-research` | IBES consensus interpretation, fundamental analysis, valuation metrics |
| `swap-curve-strategy` | Swap curve construction, curve trades, real rate analysis |
| `option-vol-analysis` | Vol surface interpretation, SABR model, Greeks, implied vs realized vol |
| `fixed-income-portfolio` | Portfolio analytics, key rate duration, cashflow analysis, scenario testing |
| `macro-rates-monitor` | Macro indicators, yield curve shapes, real rates, financial conditions |
| `bond-futures-basis` | CTD mechanics, basis calculation, implied repo, delivery options |

## Integrations

This plugin connects to the **LFA MCP Server** which provides access to LSEG financial data and analytics across these domains:

- **Bond Pricing** — Bond and bond future valuation
- **FX Pricing** — Spot and forward rates
- **Curves** — Interest rate, credit, inflation, and FX forward curves
- **Swaps** — Interest rate swap pricing
- **Options** — Option valuation with full Greeks
- **Volatility** — FX and equity implied volatility surfaces
- **Quantitative Analytics** — Analyst estimates, company fundamentals, equity prices, macro data
- **Time Series** — Historical pricing summaries
- **YieldBook** — Fixed income reference data, cashflows, scenarios, and risk analytics

See [CONNECTORS.md](CONNECTORS.md) for the complete tool reference.

## Installation

```
claude plugins add LSEG
```

## Requirements

- Access to the LSEG MCP Server with valid credentials
- LSEG data entitlements for the relevant product offerings
