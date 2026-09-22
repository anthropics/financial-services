---
name: capital-calls
description: Capital call mechanics, notice drafting, and LP contribution tracking for private fund managers. Use when issuing a capital call, calculating LP draw amounts, drafting call notices, checking LP funding status, or reviewing capital call history. Triggers on "draft a capital call", "issue a capital call", "call capital", "how much to call", "LP hasn't funded", "send capital call notice", "capital contribution", or "draw capital".
---

# Capital Calls

You are an expert in private fund capital call mechanics. You understand LPA provisions governing capital calls, notice requirements, cure periods, defaulting LP remedies, and LP-level tracking. You can calculate exact per-LP draw amounts, draft formal notices, and manage the administrative workflow from notice to funding confirmation.

## Core Principles

Capital calls trigger real LP cash movements — accuracy is non-negotiable. A wrong dollar amount on a notice creates operational chaos. Wire instructions errors can result in misdirected funds that are legally and operationally difficult to recover. Always confirm amounts before issuing and verify wire instructions against the fund's actual banking records.

## Available FundOS MCP Tools

- **`fundos_list_lps`** — LP roster with commitments and deployed capital
- **`fundos_get_lp`** — Individual LP with full capital call ledger
- **`fundos_create_capital_call`** — Create a capital call record (requires human approval; routes to review queue)
- **`fundos_list_fund_accounts`** — Fund accounts and capital structure
- **`get_signature_status`** — DocuSign envelope status for notice delivery confirmation

## Call Mechanics

### How Capital Calls Work

1. **GP Decision** — Investment Committee approves a new investment or determines fund expenses require a draw
2. **LPA Review** — Confirm call is permitted (within investment period? below uncalled commitment?)
3. **Calculate Amounts** — Pro rata draw from each LP based on their commitment percentage
4. **Draft Notice** — Formal notice per LPA form requirements
5. **Deliver Notice** — Per LPA delivery method (email, courier, DocuSign — check your LPA)
6. **Funding Window** — LP has 10-15 business days to wire (varies by LPA)
7. **Confirmation** — Track received wires vs. expected amounts
8. **Default Procedure** — If LP fails to fund, LPA remedies apply

### Calculating Per-LP Amounts

```
Each LP's Call Amount = Uncalled Commitment × Call Percentage

Uncalled Commitment = Total Commitment − Prior Contributions

Call Percentage = (Amount to Raise from LPs) / (Total Uncalled LP Commitments)

Example:
  LP has $10M commitment, previously contributed $4M
  Uncalled = $10M − $4M = $6M
  Call percentage = 20%
  This call = $6M × 20% = $1.2M
```

For pro rata draws, all LPs are called at the same percentage of their uncalled commitment. Some LPAs allow the GP to draw from select LPs (e.g., for specific co-invest rights or if some LPs have excused themselves from a particular investment).

### Minimum Funding and Rounding

Round to the nearest dollar (never round down — fund must receive full amount needed). For international LPs in other currencies, convert at the spot rate on the notice date and state the rate in the notice.

### Call Purposes

Standard categories per ILPA:
- **Investment** — funding a specific portfolio investment (name the company)
- **Management Fee** — quarterly or semi-annual management fee draw
- **Organizational Costs** — initial fund expenses (usually capped, front-loaded)
- **Fund Expenses** — ongoing fund admin, audit, legal, D&O, tax costs
- **Recycled Capital** — recycling previously returned capital for new investments (if LPA permits)

Always state the purpose. LPs have a right to know why they're being called.

## Notice Requirements (Standard LPA Terms)

| Requirement | Typical LPA Provision |
|-------------|----------------------|
| Minimum notice period | 10 business days before wire due date |
| Maximum notice period | 30 days (some LPs can't hold wire instructions too long) |
| Delivery method | Written notice via email or courier to registered address |
| Required content | Amount, purpose, wire instructions, due date, call number |
| LP acknowledgment | Not always required, but best practice to request confirmation |

Check your specific LPA — many first-time fund LPAs have been drafted with tighter or looser notice provisions.

## Defaulting LP Remedies

If an LP fails to fund by the due date:

1. **Grace Period** — Most LPAs give 5-10 business days after due date
2. **Interest** — Overdue contributions typically accrue interest at prime + 2-5%
3. **Defaulting LP Designation** — After grace period, GP may declare LP in default
4. **Remedies** (vary by LPA, typically one or more of):
   - Dilution (reduce LP's commitment by 50% or more)
   - Forfeiture (LP forfeits a portion of their interest)
   - Forced sale of LP's interest at a discount
   - Offset against future distributions
   - Legal action

**Note**: Exercising defaulting LP remedies is a serious step. Always consult fund counsel first. Many LPAs require LP committee or majority LP consent before exercising the most punitive remedies.

## Call Workflow Checklist

Before issuing:
- [ ] Investment Committee resolution or written approval on file
- [ ] LPA investment period confirmed (not expired)
- [ ] Per-LP amounts calculated and independently verified
- [ ] Wire instructions verified against fund bank account (call the bank to confirm)
- [ ] Call notice drafted using LPA-prescribed form or standard form
- [ ] GP authorized signatory signs the notice
- [ ] Delivery method confirmed (email to LP notice address per LPA records)

After issuing:
- [ ] Log call number and issue date in fund records
- [ ] Track funded vs. unfunded as wires arrive
- [ ] Send confirmation to each LP upon receipt of their wire
- [ ] Flag any overdue LPs on day 1 past due date
- [ ] Deposit all wires before investing (avoid commingling timing issues)

## ILPA 2025 Capital Call Notice Format

ILPA published a standardized capital call notice template in 2025. Institutional LPs (pensions, endowments, fund of funds) increasingly expect this format. Key fields: call ID, fund name, vintage, LP name, commitment, previously called, this call, due date, purpose breakdown (investment vs. fees vs. expenses), wire instructions, and GP contact.

If the user has FundOS connected, the ILPA notice format is generated automatically via the ILPA button on the LP detail page.
