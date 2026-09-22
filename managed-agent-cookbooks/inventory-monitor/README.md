# Inventory Monitor — managed-agent template

## Overview

Monitors stock levels across coffee shop locations against configured par levels, detects shortfalls, ranks them by urgency, and triggers reorder alerts to the Supplier Order Agent for CRITICAL items.

Same source as the [`inventory-monitor`](../../plugins/agent-plugins/inventory-monitor) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export INVENTORY_MCP_URL=...    # read-only inventory and par-level MCP
../../scripts/deploy-managed-agent.sh inventory-monitor
```

## Steering events

See [`steering-examples.json`](./steering-examples.json). Kick a session with a location scope and optional SKU filter; follow-up events can target a specific SKU or generate a weekly reorder list.

## Security & handoffs

This agent reads stock-count sheets submitted by store staff — documents authored by internal but untrusted parties. The template is structured so a payload in one of those documents cannot reach a shell, a write tool, or a firm system:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`reader`** | **Yes** | `Read`, `Grep` only | None |
| **Orchestrator** | No | `Read`, `Grep`, `Glob`, `Agent` | Read-only Inventory MCP |
| **`resolver`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

The `reader` returns length-capped, schema-validated JSON only (validated by `scripts/validate.py`). The `resolver` writes the shortfall report and reorder list to `./out/`; it never opens a staff-submitted count sheet.

**Handoff:** for CRITICAL shortfall items, the resolver emits a `handoff_request` for `supplier-order-agent`. `scripts/orchestrate.py` validates the payload against the supplier-order-agent steering schema before routing it as a new steering event. HIGH and MEDIUM items are included in the report for human-initiated ordering only.

**Not guaranteed:** this agent detects shortfalls and routes reorder requests; it does not guarantee orders are placed. The supplier-order-agent executes the actual WhatsApp dispatch, and amendments require human approval.
