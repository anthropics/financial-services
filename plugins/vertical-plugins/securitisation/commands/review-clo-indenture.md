---
description: Review a CLO indenture — waterfalls, coverage tests, and collateral quality
argument-hint: "[path to indenture / offering memorandum]"
---

# Review CLO Indenture

Review a CLO indenture or offering memorandum and extract the provisions that govern
the deal: the priority of payments, coverage tests, collateral quality tests,
concentration limits, the reinvestment regime, and call/redemption terms.

## Workflow

### Step 1 — Get the document
CLOs are issued under **Rule 144A and are not on SEC EDGAR**, so this command works
on a **document the user supplies** (the indenture or offering memorandum as a PDF or
text file). Ask for it if not provided. (If they instead have a registered ABS, use
`/parse-abs-prospectus`.)

### Step 2 — Load the skill
Use `skill: "clo-indenture-review"` for the provision checklist and market-standard
benchmarks to compare against.

### Step 3 — Extract the governance provisions
Work through: the **interest** and **principal** waterfalls; the **coverage tests**
(OC / IC, par value test, with cushions); the **collateral quality tests** (WARF,
WAS, WAL, diversity score, weighted-average coupon/recovery); **concentration
limitations** (single obligor, industry, CCC bucket, cov-lite, second lien);
**reinvestment criteria** and the reinvestment period; **events of default**; the
**fee structure**; and **non-call / redemption / reset** provisions.

### Step 4 — Deliver
A structured review with a tests table (test, trigger level, typical cushion) and a
**flagged-items** list highlighting anything off-market or borrower-favourable. Cite
the indenture section for each item; mark anything not found as "not located".

Use `/extract-waterfall` to render the priority of payments in detail.
