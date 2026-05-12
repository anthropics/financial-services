# FundOS Plugin for Claude

AI-native fund operations for emerging VC and private credit managers — capital calls, LP reporting, waterfall calculations, covenant monitoring, and VDR workflow, powered by the FundOS MCP server.

## What FundOS Is

[FundOS by Kela](https://www.kela.com) is an AI-native operating system for fund managers. It gives emerging VC, private equity, and private credit managers the same fund operations infrastructure as large institutions: a deal CRM, LP investor portal, capital call engine, European waterfall calculator, covenant monitoring dashboard, and Virtual Data Room — all accessible through a unified MCP server so AI agents can read fund state and propose actions for human approval.

FundOS is built for the 4,000+ new emerging managers who launch funds every year and can't afford the enterprise fund admin stack. It handles the full fund lifecycle from first close to final distribution.

## What This Plugin Does

This plugin packages FundOS's core fund operations workflows into 7 slash commands and 6 background skills. Each command orchestrates multiple FundOS MCP tool calls into a complete, GP-ready output — a formal capital call notice, a quarterly LP letter, a distribution waterfall with full math, or a diligence document checklist.

Commands can run standalone (asking the user for inputs) or with live data pulled directly from FundOS when the MCP connector is configured.

## Commands

| Command | Description |
|---------|-------------|
| `/fundos:capital-call` | Draft a formal capital call notice with per-LP amounts and wire instructions |
| `/fundos:lp-report` | Generate a quarterly LP report with performance metrics, portfolio summary, and investor letter |
| `/fundos:waterfall` | Calculate fund distribution waterfall (European or American) with step-by-step math and sensitivity table |
| `/fundos:covenant-check` | Evaluate portfolio company covenant compliance and flag breaches or near-breaches with RAG status |
| `/fundos:lp-update` | Draft a formal LP communication for any fund event — exit, write-down, new investment, fund milestone |
| `/fundos:vdr-checklist` | Generate a VDR document checklist for a deal at a given diligence stage (initial / full / closing) |
| `/fundos:fund-snapshot` | Generate a one-page fund snapshot with capital metrics, DPI/RVPI/TVPI, and portfolio summary |

## Skills

Skills provide the background domain knowledge that Claude uses automatically when a relevant conversation is detected — no slash command required.

| Skill | Triggers Automatically When... |
|-------|-------------------------------|
| `fund-admin` | User asks about fund metrics, NAV, capital accounts, DPI/RVPI/TVPI |
| `lp-communications` | User wants to draft any communication to limited partners |
| `capital-calls` | User mentions issuing a capital call or LP hasn't funded |
| `waterfall-calculations` | User asks about distributions, carry, preferred return, or GP/LP split |
| `covenant-monitoring` | User reviews portfolio company financials against loan terms |
| `vdr-workflow` | User organizes a data room or generates a diligence document list |

## MCP Connector

This plugin connects to the **FundOS MCP server** which provides live access to fund data across all modules.

### Endpoint

```
https://mcp.kela.com/mcp
```

### Authentication

Authenticate using a FundOS API key:

```
Authorization: Bearer vdr_<your-api-key>
```

API keys are issued from your FundOS workspace at **Settings → API Keys** (requires Admin role). Each key is scoped to your organization and respects the FundOS permission model.

### Getting an API Key

1. Log in to [www.kela.com](https://www.kela.com)
2. Navigate to **Settings → API Keys**
3. Create a new key with a descriptive name (e.g. "Claude Plugin")
4. Copy the key immediately — it is only shown once

### What the MCP Server Exposes

The FundOS MCP server exposes 24+ tools across all fund operations modules:

| Module | Tools Available |
|--------|----------------|
| Deal CRM | `fundos_list_deals`, `fundos_get_deal`, `fundos_get_pipeline` |
| LP Investor Portal | `fundos_list_lps`, `fundos_get_lp`, `fundos_create_capital_call` |
| CFO Center | `fundos_list_fund_accounts`, `fundos_compute_pnl`, `fundos_compute_waterfall` |
| Risk / Covenants | `fundos_list_covenants`, `fundos_check_covenant`, `fundos_list_risk_alerts` |
| VDR | `list_deal_rooms`, `list_documents`, `search_documents`, `get_document_activity` |
| Transactions | `fundos_list_transactions`, `fundos_draft_transaction` |
| Pricer | `fundos_run_pricer` |

All write operations (capital calls, covenant updates, document uploads) require human approval in the FundOS UI before taking effect. Agents propose — humans approve.

## Installation

### From Claude Code CLI

```bash
# Add the Anthropic FSI marketplace if not already added
claude plugin marketplace add anthropics/financial-services-plugins

# Install the FundOS plugin
claude plugin install fundos@claude-for-financial-services
```

### Configure the MCP Connector

In your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "fundos": {
      "type": "http",
      "url": "https://mcp.kela.com/mcp",
      "headers": {
        "Authorization": "Bearer vdr_<your-api-key>"
      }
    }
  }
}
```

Or add via Claude Code settings for user-level access:

```bash
claude mcp add fundos https://mcp.kela.com/mcp
```

## Without the MCP Connector

All commands work without a live FundOS connection. Claude will ask for the required inputs (LP list, financials, covenant definitions, etc.) and perform all calculations locally. The MCP connector adds:

- Live fund data pull (no manual input needed)
- Capital call creation routing to FundOS approval queue
- Covenant breach alerts stored in FundOS risk dashboard
- Document gap analysis against actual VDR contents

## Example Usage

**Capital call for a new investment:**
```
/fundos:capital-call Fund II — new investment in Stripe, calling 15% of uncalled commitments
```

**Quarterly LP report:**
```
/fundos:lp-report Acme Ventures Fund II Q1 2026
```

**European waterfall:**
```
/fundos:waterfall $85M proceeds, $40M LP capital invested, 8% preferred return, 20% carry
```

**Covenant check on a private credit portfolio company:**
```
/fundos:covenant-check PortCo Corp Q1 2026 — Total Leverage ≤5.0x, ICR ≥2.5x, Min Cash $5M
```

**LP exit announcement:**
```
/fundos:lp-update portfolio exit — Acme acquired for $120M, 4.2x MOIC, semi-formal tone
```

**Diligence checklist:**
```
/fundos:vdr-checklist Series B SaaS company — full diligence stage
```

**Fund snapshot:**
```
/fundos:fund-snapshot Acme Ventures Fund II
```

## Support

- Documentation: [www.kela.com/llms.txt](https://www.kela.com/llms.txt) (LLM-optimized FundOS reference)
- Full API docs: [www.kela.com/api/docs](https://www.kela.com/api/docs)
- MCP server discovery: [www.kela.com/.well-known/mcp.json](https://www.kela.com/.well-known/mcp.json)
- Support: support@kela.com

## License

MIT — see [LICENSE](LICENSE) for details.
