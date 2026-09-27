# ACI Risk Indicators

Counterparty risk analytics for digital asset yield providers, from Aethon Credit Intelligence (ACI). The plugin declares the ACI connector (`https://mcp.aethoncredit.com/mcp`) and adds skills that tell Claude how to read ACI Risk Indicators: which tool to call at each plan, and to report only the fields the tools return.

ACI Risk Indicators are model-derived quantitative analytics outputs produced under the ACI Framework v1.0 using defined inputs and publicly available data. They are designed to support independent analysis within professional and institutional decision-making processes. They are not a credit rating, not advice, and not a recommendation.

## Tools

The ACI connector exposes six read-only tools.

| Tool | What it returns |
|---|---|
| `list_modules` | The modules, each with `code`, `name`, `description`, and live `provider_count` / `criteria_count`. |
| `search_providers` | Providers filtered by `query`, `module`, `risk_band`, `subtype`. Name, module and risk band for every plan; where the plan includes them, also `slug`, indicator value and `subtype`. |
| `get_risk_score` | One provider's indicator value, `risk_band`, `hard_caps_applied`, `confidence_level`, `last_certified`, `methodology_version`. |
| `get_provider_detail` | The full per-criterion breakdown for one provider. |
| `compare_providers` | A side-by-side matrix for 2–5 providers. |
| `assess_portfolio_risk` | A composite assessment across 2–20 weighted positions. |

## Access by plan

The connector checks the user's plan on every call.

| Tool | No sign-in | Sandbox | Analyst | Professional | Enterprise |
|---|---|---|---|---|---|
| `list_modules` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `search_providers` | band only | band only | band only | ✓ | ✓ |
| `get_risk_score` | sign-in | — | — | ✓ | ✓ |
| `get_provider_detail` | sign-in | — | — | ✓ | ✓ |
| `compare_providers` | sign-in | — | — | ✓ | ✓ |
| `assess_portfolio_risk` | sign-in | — | — | ✓ | ✓ |

"band only" means `search_providers` returns name, module and risk band, without the indicator value. "sign-in" means calling the tool starts sign-in to an Aethon Credit Intelligence account. "—" means the tool returns a refusal that names the plan it needs. Free band-only search is available to every user; full Risk Indicators are available to subscribers. Plans and prices: https://aethoncredit.com/pricing.

## Install

```
claude plugin install aci-risk-indicators@claude-for-financial-services
```

The connector can also be added directly:

```
claude mcp add --transport http aethon-credit-intelligence https://mcp.aethoncredit.com/mcp
```

No sign-in is needed to connect. The first time Claude calls a tool that needs an account, the user is asked to sign in.

## Skills

- `risk-check` — look up one provider's Risk Indicator or its breakdown.
- `module-screening` — filter providers by module and risk band.
- `portfolio-risk` — a composite assessment across a set of weighted positions.
- `methodology` — what the methodology fields mean, and where the methodology is published.

## Links

- Developers: https://aethoncredit.com/developers
- Plans: https://aethoncredit.com/pricing
- Methodology: https://aethoncredit.com/methodology
- Public plugin repo: https://github.com/aethon-credit/aci-claude-plugin

---

*ACI Framework v1.0 · aethoncredit.com · Quantitative risk analytics outputs for independent analysis*
