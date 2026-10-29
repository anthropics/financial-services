# Portfolio Analyst — managed-agent template

## Overview

Investor profile → holdings review → stock checkups → position sizing → staged rebalancing plan. Same source as the [`portfolio-analyst`](../../plugins/agent-plugins/portfolio-analyst) Cowork plugin. This directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export MORNINGSTAR_MCP_URL=...
../../scripts/deploy-managed-agent.sh portfolio-analyst
```

## Steering events

See [`steering-examples.json`](./steering-examples.json). Kick from a quarterly schedule, a new brokerage export landing in `./in/`, or a cash deposit event.

## Security & handoffs

Brokerage statements are untrusted and contain personal financial data. Three-tier isolation:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`statement-reader`** | **Yes** | `Read`, `Grep` only | None |
| `analyst` / Orchestrator | No | `Read`, `Grep`, `Glob`, `Agent` | Morningstar (read-only) |
| **`report-writer`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

`statement-reader` returns length-capped, schema-validated JSON. `report-writer` produces `./out/portfolio-review-<date>.md` and, when requested, `./out/rebalance-<date>.xlsx` labelled as staged for investor review.

**No execution.** No worker has brokerage access, and the agent never places orders or asks for credentials.

**Handoff:** for a full sector primer on an underweight sleeve, emit a `handoff_request` for `market-researcher`; for a full model on a single name, emit one for `model-builder`. `scripts/orchestrate.py` routes it as a new steering event.
