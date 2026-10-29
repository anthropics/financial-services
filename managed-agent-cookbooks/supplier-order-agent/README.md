# Supplier Order Agent — managed-agent template

## Overview

Sends purchase orders to suppliers via the WhatsApp Business API, tracks inbound delivery confirmations, and maintains a running order log CSV. Flags amendments and unconfirmed orders for human review.

Same source as the [`supplier-order-agent`](../../plugins/agent-plugins/supplier-order-agent) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export WHATSAPP_MCP_URL=...           # WhatsApp Business API MCP
export SUPPLIER_CATALOG_MCP_URL=...   # read-only supplier/SKU catalog MCP
../../scripts/deploy-managed-agent.sh supplier-order-agent
```

## Steering events

See [`steering-examples.json`](./steering-examples.json). Kick a session with a supplier name and item list; follow-up events can check a specific order reference or sweep for overdue confirmations.

## Security & handoffs

This agent reads inbound WhatsApp messages from suppliers — content authored by external parties that may carry adversarial instructions. The template is structured so a payload in one of those messages cannot reach a shell, a write tool, or a firm system:

| Tier | Touches untrusted messages? | Tools | Connectors |
|---|---|---|---|
| **`reader`** | **Yes** | `Read`, `Grep` only | None |
| **Orchestrator** | No | `Read`, `Grep`, `Glob`, `Agent` | WhatsApp Business + Supplier Catalog MCPs |
| **`resolver`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

The `reader` returns length-capped, schema-validated JSON only (validated by `scripts/validate.py`). The `resolver` writes the order log and amendment flags to `./out/`; it never opens a supplier message directly.

**Handoff:** supplier orders triggered by the `inventory-monitor` agent arrive as steering events via `scripts/orchestrate.py`. The orchestrator's `handoff_request` payload is validated against the steering schema before dispatch.

**Not guaranteed:** this agent dispatches orders and records confirmations; it does not guarantee delivery. Human review is required for all amendments and overdue orders.
