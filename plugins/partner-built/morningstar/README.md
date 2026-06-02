# Morningstar Plugin

Screen, summarize, and compare funds and ETFs using Morningstar ratings, risk metrics, holdings, and analyst research.

## What This Plugin Does

This plugin packages Morningstar's fund data MCP tools into 3 high-level workflows for common fund research tasks. Each skill orchestrates multiple tool calls into a cohesive analysis and serves as its own command — there is no separate commands layer.

## Skills

Each skill is both the trigger condition and the domain workflow. Describe what you want and the matching skill activates automatically.

| Skill | Trigger Condition | Domain Knowledge |
|-------|------------------|-----------------|
| `fund-screener` | Screening funds or ETFs by category, ratings, fees, assets, returns, or risk | Criteria normalization, Morningstar datapoints, result ranking, disclosure rules |
| `fund-summarizer` | Summarizing a fund or ETF with ratings, returns, risk, holdings, fees, and caveats | Medalist and star ratings, pillar ratings, performance context, HTML report rendering |
| `fund-comparison` | Comparing 2 to 4 funds or ETFs with ratings, returns, risk, and holdings data | Fund resolution, holdings overlap, broad-asset-class checks, side-by-side table formats |

## Integrations

This plugin connects to the **Morningstar MCP Server** which provides access to Morningstar fund data and analytics:

- **Fund Screening** — Filter ETFs, open-end funds, and closed-end funds by category, Morningstar ratings, expense ratio, assets, returns, and risk metrics
- **Fund Summaries** — Ratings, analyst research, performance, portfolio composition, sustainability data, and HTML report generation
- **Fund Comparisons** — Side-by-side metrics, holdings overlap for equity funds, and category-rank tables

## Installation

```
claude plugins add morningstar
```

## Requirements

- Access to the Morningstar MCP Server at `https://mcp.morningstar.com/mcp`
- Morningstar data entitlements for the relevant fund universes
