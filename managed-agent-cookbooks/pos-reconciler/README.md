# POS Reconciler — managed-agent template

## Overview

Pulls daily sales data from the POS system, reconciles cash takings against POS totals per location, flags discrepancies, and produces a clean verified dataset for the Month-End Closer.

Same source as the [`pos-reconciler`](../../plugins/agent-plugins/pos-reconciler) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export POS_MCP_URL=...    # read-only POS MCP (Square, Toast, or Lightspeed)
../../scripts/deploy-managed-agent.sh pos-reconciler
```

## Steering events

See [`steering-examples.json`](./steering-examples.json). Kick a session with a business date and optional location filter; follow-up events can re-investigate a specific variance or produce a week-to-date handoff.

## Security & handoffs

This agent reads cash-up sheets submitted by store staff — documents authored by internal but untrusted parties that may contain inconsistent or manipulated figures. The template is structured so a payload in one of those documents cannot reach a shell, a write tool, or a firm system:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`reader`** | **Yes** | `Read`, `Grep` only | None |
| **`critic`** | No | `Read`, `Grep` | Read-only POS MCP |
| **Orchestrator** | No | `Read`, `Grep`, `Glob`, `Agent` | Read-only POS MCP |
| **`resolver`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

The `reader` returns length-capped, schema-validated JSON only (validated by `scripts/validate.py`). The `critic` independently re-verifies each location's figures against the POS MCP before the orchestrator hands the set to `resolver`. The `resolver` writes the reconciliation report to `./out/`; it never opens a staff-submitted file.

**Handoff:** to feed verified weekly sales into Month-End Closer, the orchestrator emits a `handoff_request` for `month-end-closer` in its final output; `scripts/orchestrate.py` routes it as a new steering event.

**Not guaranteed:** none of this writes to a system of record. Ledger adjustments require human approval outside the agent.
