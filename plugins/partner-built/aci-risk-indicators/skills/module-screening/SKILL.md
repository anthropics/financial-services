---
name: module-screening
description: "Screen digital asset yield providers by ACI module and risk band through the Aethon Credit Intelligence connector. Use when the user wants the providers in a module, the providers in a given risk band, or a filtered list across the ACI universe. Shows rows exactly as the tools return them, in the order returned."
---

# ACI Module Screening

Filter digital asset yield providers by module and risk band through the Aethon Credit Intelligence connector (`https://mcp.aethoncredit.com/mcp`).

## Modules

ACI groups providers into nine modules. Use `list_modules` for the live codes, names and counts — quote counts from the tool, never from memory.

| Code | Name |
|---|---|
| `btc` | BTC Collateral Lending |
| `fiat` | Treasury Preferred Shares |
| `stablecoin` | Stablecoin Yield |
| `infrastructure` | Infrastructure |
| `market_neutral` | Market Neutral |
| `venture` | Venture |
| `tokenised_rwa` | Tokenised RWA |
| `volatility` | Volatility |
| `digital_asset_etp` | Digital Asset ETP |

`fiat` is the code for Treasury Preferred Shares; it has nothing to do with stablecoins. Never describe it as fiat yield.

## Risk bands

Every ACI Risk Indicator falls in one of four bands, returned in `risk_band`:

| Band | Indicator value |
|---|---|
| LOW | 80–100 |
| MEDIUM | 60–79 |
| ELEVATED | 40–59 |
| HIGH | 0–39 |

Report the band as returned. Never derive a band from a value yourself.

## Workflow

1. Call `list_modules` to get the module codes and their live counts.
2. Call `search_providers` with `module`, and `risk_band` if the user names one. Optional inputs: `query`, `subtype`, `limit` (1–100, default 25).
3. Show the rows as returned, in the order returned. Below the Professional plan, rows carry name, module and risk band only; on Professional and above they also carry `slug`, the indicator value and `subtype`.

Present the list without ranking, scoring commentary, or any view on which provider is stronger, weaker, or preferable. Order the rows as the tool returns them.

---

*ACI Framework v1.0 · aethoncredit.com · Quantitative risk analytics outputs for independent analysis*
