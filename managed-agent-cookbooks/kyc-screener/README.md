# KYC Screener — managed-agent template

## Overview

Parses onboarding docs, runs the rules engine, screens sanctions/PEP, flags gaps. Same source as the [`kyc-screener`](../../plugins/agent-plugins/kyc-screener) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export SCREENING_MCP_URL=...
../../scripts/deploy-managed-agent.sh kyc-screener
```

## Steering events

See [`steering-examples.json`](./steering-examples.json).

## Security & handoffs

Onboarding documents are untrusted. Three-tier isolation:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`doc-reader`** | **Yes** | `Read`, `Grep` only | None |
| `rules-engine` / Orchestrator | No | `Read`, `Grep`, `Glob`, `Agent` | screening (read-only) |
| **`escalator`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

`doc-reader` returns length-capped, schema-validated JSON. `escalator` produces `./out/escalation-<packet>.xlsx`.

**Not guaranteed:** this agent recommends a risk rating; the compliance officer decides.
