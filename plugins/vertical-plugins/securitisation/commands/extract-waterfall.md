---
description: Extract the priority of payments (waterfall) from a deal document
argument-hint: "[deal name, CIK/accession, or document path]"
---

# Extract Payment Waterfall

> Uses the bundled EDGAR connector — if its tools are missing or erroring, see [CONNECTOR.md](../CONNECTOR.md).

Extract the **priority of payments** from an ABS prospectus, a CLO indenture, or a
10-D investor report, and render it as an ordered, condition-aware sequence.

## Workflow

### Step 1 — Get the source
- Registered ABS: find/fetch the 424B or 10-D via **`search_securitisation_deals`**
  + **`get_filing_document`**.
- CLO or other private deal: use the document the user supplies.

### Step 2 — Load the skill
Use `skill: "payment-waterfall-extraction"` for the standard waterfall structures
and the trigger logic that reorders them.

### Step 3 — Extract the waterfall
Identify the "Priority of Payments" / "Application of Funds" section. Capture each
step **in order**, with its **condition** (e.g. *only if the Cumulative Net Loss
Trigger is not breached*). For CLOs, capture the **interest** and **principal**
waterfalls separately, including coverage-test diversions. Note **sequential vs
pro-rata** principal logic and any **turbo** features and trigger switches.

### Step 4 — Deliver
Render the waterfall as a numbered list (and, where useful, a simple top-to-bottom
diagram), with a short note on each trigger that changes the order. Cite the source
section. If the document defines pre- and post-trigger (or pre-/post-EOD) waterfalls,
present **both**.
