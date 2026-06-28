# Month-End Closer — managed-agent template

## Overview

Accruals, roll-forwards, variance commentary. Same source as the [`month-end-closer`](../../plugins/agent-plugins/month-end-closer) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export GL_MCP_URL=...
../../scripts/deploy-managed-agent.sh month-end-closer
```

## Steering events

See [`steering-examples.json`](./steering-examples.json).

## Security & handoffs

Supporting invoices and vendor statements are untrusted. Three-tier isolation:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`ledger-reader`** | **Yes** | `Read`, `Grep` only | None |
| `rollforward` / Orchestrator | No | `Read`, `Grep`, `Glob`, `Agent` | internal-gl (read-only) |
| **`poster`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

`poster` produces `./out/close-package-<entity>-<period>.xlsx`. JE drafts are staged, not posted to the GL.

**Handoff:** receives `handoff_request` events from `gl-reconciler` with verified breaks to fold into close commentary.
