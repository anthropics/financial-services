---
description: Run month/quarter-end variance analysis and turn it into a board-ready pack — KPI tiles, gross-to-net bridge, and driver commentary
argument-hint: "[fund name and period, e.g. 'Acme Fund II Q2 2026']"
---

# Flux Pack

> This command uses the FundOS MCP server. See the [README](../README.md) for connection requirements.

Two steps, in order: compute the variance, then present it. The **variance-commentary** skill covers the analysis; the **board-dashboard** skill covers the layout.

## Workflow

### 1. Establish the scope

If FundOS MCP is connected, call `fundos_list_fund_accounts` to pick the vehicle and confirm its reporting currency. Otherwise ask for:

- **Fund** and **period** (month, quarter, or year)
- **Comparison basis** — prior period, budget, or both
- **Materiality** — the amount and/or percent threshold that makes a line worth commenting on
- **Always-comment lines** — any line the GP wants explained however small it moved

In FundOS the last two are workspace settings (**CFO Center → Flux → Reporting style**), so they do not need restating each quarter.

### 2. Compute the variance

Call `cfo.flux` via `fundos_call_tool`. **Do not compute the deltas yourself** — the table is built and footed in Python, and a number derived in prose is a number nobody checked.

Each row returns: category, line label, actual, prior, budget, delta in amount and percent, and a materiality flag.

### 3. Draft one driver per material line

One sentence explaining **why** the line moved, not what it moved to. If you cannot determine a driver from the data, use exactly `driver unclear — flag for controller`. Never invent a cause.

### 4. Assemble the pack

- **Management message** — one sentence: what happened, what drove it, what to pressure-test.
- **KPI tiles** — value, change, basis, and a `Source:` line on each.
- **Gross-to-net bridge** — opening basis, material movers largest first, immaterial tail as "Other", closing actual.
- **Line detail** — the full table with drivers.

### 5. State the footing verdict

If the bridge **foots**, show the check: components, stated total, residual.

If it **does not foot**, banner it, render the gap as its own labelled **Unexplained** bar, and say so in the management message. Never fold a residual into "Other" to make the waterfall close.

### 6. Mark it a draft and stop

Label the pack **DRAFT FOR HUMAN REVIEW**. Flux is read-only — it posts nothing and sends nothing — but a pack is a draft until a human controller signs it off. Do not send it to anyone.

In FundOS the finished pack lives at `/fundos/cfo/flux/pack/<run_id>`, and **Publish to room** files it as XLSX, PDF and self-contained HTML into the fund's reporting room.
