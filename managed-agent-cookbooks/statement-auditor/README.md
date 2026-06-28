# Statement Auditor — managed-agent template

## Overview

Audits pre-generated LP statements before distribution. Same source as the [`statement-auditor`](../../plugins/agent-plugins/statement-auditor) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export NAV_MCP_URL=...
../../scripts/deploy-managed-agent.sh statement-auditor
```

## Steering events

See [`steering-examples.json`](./steering-examples.json).

## Security & handoffs

Generated statements are treated as untrusted (upstream system out of scope). Three-tier isolation:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`statement-reader`** | **Yes** | `Read`, `Grep` only | None |
| `reconciler` / Orchestrator | No | `Read`, `Grep`, `Glob`, `Agent` | nav (read-only) |
| **`flagger`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

`flagger` produces `./out/signoff-<batch>.xlsx`.

**Not guaranteed:** this agent recommends pass/hold; IR distributes after human sign-off.
