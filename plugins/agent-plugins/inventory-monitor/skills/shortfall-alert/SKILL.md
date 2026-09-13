---
name: shortfall-alert
description: Calculate days-of-stock remaining for each shortfall item, rank by urgency, and format reorder recommendations for the resolver. Emits a handoff_request for supplier-order-agent when items fall below the critical threshold. Use after stock-check has produced the stock_status array.
---

# Rank shortfalls and format reorder recommendations

Given the `stock_status` array from `stock-check` and optionally the staff-submitted count cross-verified by the `reader` subagent, produce a prioritised shortfall report and a structured reorder list.

> **Only consume schema-validated data from the reader subagent and the inventory MCP.** Never read raw staff count sheets directly.

## Step 1: Segment by urgency tier

Divide shortfall items into three tiers based on `days_of_stock_remaining` and `status`:

| Tier | Condition | Response time |
|---|---|---|
| **CRITICAL** | `status=out_of_stock` OR `days_of_stock_remaining <= reorder_lead_days` | Same-day order required |
| **HIGH** | `status=critical` AND `days_of_stock_remaining <= 2 * reorder_lead_days` | Order today |
| **MEDIUM** | `status=below_par` | Order within 24 hours |

Items at `status=ok` are excluded from the shortfall report.

## Step 2: Calculate reorder quantities

For each shortfall item, calculate the recommended reorder quantity:

```
reorder_qty = par_qty - qty_on_hand + (avg_daily_usage * reorder_lead_days * 1.2)
```

The 1.2 factor is a 20% safety buffer. Round up to the nearest case size if `case_size` is available from the inventory MCP. If `avg_daily_usage` is unavailable, default to `par_qty - qty_on_hand` and flag the estimate.

## Step 3: Group by supplier

Use the inventory MCP's `mcp__inventory-system__get_sku_supplier_map` to look up the preferred supplier for each SKU. Group the reorder list by supplier so each purchase order contains all items from that supplier.

For each supplier group, produce a purchase order draft:

```json
{
  "supplier_name": "Coco Supplies",
  "urgency_tier": "CRITICAL",
  "items": [
    {
      "sku": "OAT-MILK-1L",
      "description": "Oat Milk 1L Cartons",
      "qty": 96,
      "unit": "carton",
      "locations_affected": ["loc_001", "loc_002", "loc_003"]
    }
  ],
  "notes": "Critical shortfall — same-day order required"
}
```

## Step 4: Format the shortfall report

Produce a human-readable shortfall summary with:

1. **Executive summary** — total SKUs checked, shortfall counts by tier, locations affected.
2. **Critical items table** — SKU, location, qty on hand, par level, days remaining, recommended action.
3. **Reorder list by supplier** — one purchase order draft per supplier.
4. **Items at risk** — items currently `below_par` that will reach critical within 48 hours at current usage rate.

## Step 5: Emit handoff_request for critical items

For every `CRITICAL` tier item, emit a `handoff_request` in the resolver's output:

```json
{
  "handoff_request": {
    "target_agent": "supplier-order-agent",
    "urgency": "critical",
    "payload": {
      "supplier_name": "Coco Supplies",
      "items": [...]
    }
  }
}
```

The `scripts/orchestrate.py` worker validates the payload and routes it to the `supplier-order-agent` as a new steering event. Only CRITICAL items trigger automatic handoff; HIGH and MEDIUM items are included in the report for human-initiated ordering.

Hand all output to the resolver to write to `./out/shortfall-report-{date}.csv` and `./out/reorder-list-{date}.json`. Never write directly from this skill.
