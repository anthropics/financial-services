---
name: delivery-tracker
description: Match incoming supplier delivery confirmations against open purchase orders and update order status — covers confirmation parsing, order matching, amendment detection, and escalation for unconfirmed orders. Use after the reader subagent has extracted a structured confirmation payload.
---

# Match delivery confirmations against open orders

Given a structured confirmation payload (already extracted and schema-validated by the `reader` subagent), find the corresponding open order in the order log and update its status.

> **Never read raw supplier messages directly.** This skill only consumes the schema-validated JSON emitted by the `reader` subagent. If you receive a raw message string, reject it and request that it be routed through the `reader` first.

## Step 1: Load open orders

Read `./out/order-log.csv` and filter for rows where `status` is one of `sent`, `confirmed`, `amended`. Index by `order_ref`.

## Step 2: Match the confirmation

Use the `order_ref` field from the confirmation payload to look up the open order. Matching rules:

| Match result | Condition |
|---|---|
| **Exact match** | `order_ref` in confirmation equals `order_ref` in log |
| **Fuzzy match** | If exact fails, attempt case-insensitive strip; log the discrepancy |
| **No match** | Surface as `UNMATCHED_CONFIRMATION` for human review — do not create a new order |

## Step 3: Compare confirmed items against ordered items

For each item in the confirmation's `items` array, compare `qty_confirmed` against `qty` in the open order:

| Outcome | Condition | Action |
|---|---|---|
| **Full match** | All items confirm at ordered qty | Set status → `confirmed` |
| **Amendment** | Any item has `qty_confirmed` ≠ `qty`, or items differ | Set status → `amended`; flag for human review |
| **Rejection** | Confirmation `status` is `rejected` | Set status → `rejected`; surface immediately |
| **Delivery** | Confirmation `status` is `delivered` | Set status → `delivered`; record `delivered_at_utc` |

## Step 4: Escalate unconfirmed orders

Separately, scan all `sent` orders older than 24 hours (compare `sent_at_utc` to now). For each:

1. Append to `./out/unconfirmed-orders.csv` with columns: `order_ref, supplier_name, sent_at_utc, hours_outstanding`.
2. Mark the order log row `status=overdue` (do not delete the original row).
3. Return the list so the orchestrator can trigger a follow-up WhatsApp message.

## Step 5: Write updated order log

The resolver subagent holds Write. This skill produces the diff (list of rows to update) and hands it to the resolver; it does not write directly.

Diff format:

```json
{
  "updates": [
    {
      "order_ref": "ORD-2026-0518-0001",
      "new_status": "confirmed",
      "confirmed_at_utc": "2026-05-18T09:14:00Z",
      "amended_items": []
    }
  ],
  "unmatched": ["raw_message_id_abc123"],
  "overdue": ["ORD-2026-0516-0003"]
}
```

## Amendment handling

When `status=amended`:
- Populate `amended_items` with `[{ sku, qty_ordered, qty_confirmed, delta }]`.
- Do not auto-accept amendments — flag for human approval with a note in `./out/amendments-pending.csv`.
- The orchestrator may re-send a revised order or accept the amendment; the decision is human-gated.
