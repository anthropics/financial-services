# LSEG Analytics — managed-agent template

## Overview

Orchestrates LSEG MCP tools for capital markets analysis: bond relative value, FX carry, equity research, swap curves, options vol, fixed income portfolio review, macro/rates dashboards, and bond futures basis.

Backed by the [`lseg`](../../plugins/partner-built/lseg) partner plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export LSEG_MCP_URL=...         # LSEG LFA MCP server URL
../../scripts/deploy-managed-agent.sh lseg
```

## Steering events

See [`steering-examples.json`](./steering-examples.json). Kick a session with an instrument or portfolio; follow-up events can drill into a specific analysis type.

## Security & handoffs

Market data arrives via the LSEG LFA MCP server. The template ensures untrusted data cannot reach write tools:

| Tier | Touches market data? | Tools | Connectors |
|---|---|---|---|
| **`market-data-reader`** | **Yes** | `Read` only | LSEG LFA MCP (read) |
| **`analytics-runner`** | **Yes** | `Read` only | LSEG LFA MCP (read) |
| **Orchestrator** | No | `Read`, `Grep`, `Glob`, `Agent` | LSEG LFA MCP (read) |
| **`report-writer`** (Write-holder) | No | `Read`, `Write` | None |

**Requirements:** valid LSEG data entitlements and `LSEG_MCP_URL` pointing to a running LFA MCP server instance.
