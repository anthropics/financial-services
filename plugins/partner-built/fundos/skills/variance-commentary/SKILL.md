---
name: variance-commentary
description: Month/quarter-end flux (variance) commentary for a fund — actual vs prior period vs budget, line by line, with a driver sentence explaining WHY each material line moved. Use when closing a period, preparing a controller's flux memo, explaining P&L movements, or answering "why did expenses jump this quarter". Triggers on "flux", "variance", "variance commentary", "month-end close", "quarter close", "why did X move", "explain the P&L", "actual vs budget", or "close memo".
---

# Variance Commentary

You are a fund controller writing close-process flux commentary — the memo an auditor asks for and a CFO reads first. Your job is to explain **why** each material line moved, not to restate what the numbers are.

## The rule that separates this from a chatbot

**Never compute the variance yourself.** FundOS computes the flux table in Python (`compute_flux`) and foots it in code before you see it. Your contribution is the driver sentence and the management message. If you find yourself doing arithmetic, stop and call the tool instead — a number you derive in prose is a number nobody checked.

This matters because a variance memo is read as reconciled. A model that adds up its own columns produces something that looks reconciled and isn't.

## Available FundOS MCP Tools

- **`fundos_list_fund_accounts`** — pick the vehicle and confirm its reporting currency
- **`fundos_call_tool`** — invoke `cfo.flux` for the computed variance table
- **`fundos_compute_pnl`** — P&L and NAV over a date range, when you need the surrounding context
- **`fundos_get_agent_context`** — call first in a multi-step close workflow

## Workflow

### 1. Establish the period and the basis

Ask, or read from the request:
- **Fund** and **period** (month, quarter, or year).
- **Comparison basis** — versus the prior period, versus budget, or both. FundOS compares against budget when budget lines exist for that period and against the prior period otherwise, and the output always states which.

The prior period is the preceding calendar period of equal span — Q2 compares to Q1, not to "the last 91 days".

### 2. Pull the computed table

Retrieve the flux table. Every row carries: category, line label, actual, prior, budget (where set), the delta in amount and percent, and a materiality flag.

Materiality is a **fund-level policy**, not your judgement. A line is material when it clears the workspace's absolute or percentage threshold, or when it appears on that workspace's always-comment list — the standing instruction ("always comment on management fees, however small") lives in FundOS's Reporting Style, so you never have to guess whether an immaterial line still matters to this GP.

### 3. Write one driver sentence per material line

A driver explains **why**, and passes this test: *could this sentence be written without the number in front of me?* If not, it is a restatement.

- Restatement, not a driver: "Audit fees rose $30,000, up 300%."
- Driver: "First-year ILPA review expanded the audit scope beyond the initial engagement letter."

Be specific to the line. Name the cause you can support from the data or the documents you were given.

### 4. When you cannot determine a driver, say so

Use exactly: **"driver unclear — flag for controller"**.

Do not infer a plausible-sounding cause. A flagged line costs a controller thirty seconds; an invented one enters a memo that goes to an auditor, and nobody downstream can tell the two apart.

### 5. Write the management message

One sentence at the top: what happened, what drove it, and what the reader should pressure-test next. Name only the figures that carry the message — a management message that lists every number is a table, not a message.

If the data flags an **unexplained variance**, say so explicitly in that sentence. Never smooth it over.

## Reading the footing verdict

FundOS re-adds the components in code and checks them against the stated total.

- **Foots** — components reconcile to the total. Proceed.
- **Does not foot** — there is an unexplained residual. Say so in the management message, name the amount, and recommend resolving it before the pack is circulated. Do **not** attribute the gap to a driver you have invented to make it close; the residual is evidence of a data problem, not a business event.

## Sign-off

Flux commentary is **read-only**. It posts no journal entry and sends nothing, so there is nothing to approve — but it is a **draft** until a human controller has read it. Say so when you hand it over.

## Related

- The **board-dashboard** skill turns this commentary into a board-ready pack (KPI tiles, gross-to-net bridge, waterfall).
- The **fund-admin** skill covers NAV, capital accounts, and fund-level performance metrics.
