# Valuation Reviewer — managed-agent template

## Overview

Ingests GP packages, runs valuation template, stages LP reporting. Same source as the [`valuation-reviewer`](../../plugins/agent-plugins/valuation-reviewer) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export PORTFOLIO_MCP_URL=...
../../scripts/deploy-managed-agent.sh valuation-reviewer
```

## Steering events

See [`steering-examples.json`](./steering-examples.json).

## Security & handoffs

GP-provided valuation packages are untrusted. Three-tier isolation:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`package-reader`** | **Yes** | `Read`, `Grep` only | None |
| `valuation-runner` / Orchestrator | No | `Read`, `Grep`, `Glob`, `Agent` | portfolio (read-only) |
| **`publisher`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

`package-reader` returns length-capped, schema-validated JSON. `publisher` produces `./out/lp-pack-<fund>.xlsx`.

**Handoff:** to feed flagged portcos into GL Reconciler, emit a `handoff_request` for `gl-reconciler`; `scripts/orchestrate.py` routes it.

**Not guaranteed:** LP reports require IR and CCO sign-off outside this agent.
