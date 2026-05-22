# S&P Global — managed-agent template

## Overview

Generates company tearsheets (four audience types), earnings previews, and M&A transaction summaries using S&P Capital IQ data via the Kensho LLM-Ready API MCP server.

Backed by the [`spglobal`](../../plugins/partner-built/spglobal) partner plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export SPGLOBAL_MCP_URL=...     # Kensho LLM-Ready API MCP server URL
../../scripts/deploy-managed-agent.sh spglobal
```

## Steering events

See [`steering-examples.json`](./steering-examples.json). Kick a session with a company name or sector; specify audience type for tearsheets.

## Security & handoffs

S&P Capital IQ data arrives via the Kensho MCP server. Write access is isolated to the doc-writer subagent:

| Tier | Touches Capital IQ data? | Tools | Connectors |
|---|---|---|---|
| **`data-reader`** | **Yes** | `Read` only | Kensho MCP (read) |
| **Orchestrator** | No | `Read`, `Grep`, `Glob`, `Agent` | Kensho MCP (read) |
| **`doc-writer`** (Write-holder) | No | `Read`, `Write` | None |

**Requirements:** S&P Global LLM-Ready API subscription and `SPGLOBAL_MCP_URL` pointing to a running Kensho MCP server instance. All outputs require human review before distribution.
