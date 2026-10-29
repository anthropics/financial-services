---
description: Draft a capital call notice with per-LP call amounts and wire instructions
argument-hint: "[fund name or call percentage, e.g. 'Acme Fund II 20%']"
---

# Capital Call

> This command uses the FundOS MCP server. See the [README](../README.md) for connection requirements.

Draft a formal capital call notice, calculate each LP's call amount from their commitment, and produce a summary table ready for distribution.

See the **capital-calls** skill for domain knowledge on notice formats, ILPA standards, and call mechanics.

## Workflow

### 1. Gather Inputs

If the FundOS MCP is connected, call `fundos_list_lps` and `fundos_list_fund_accounts` to pull live fund and LP data. If not connected, ask the user for:

- **Fund name** and vehicle (master fund, parallel, co-invest)
- **LP list** with name, commitment amount, and currency for each LP
- **Call percentage** — percentage of uncalled committed capital being called (e.g. 20%)
- **Call purpose** — investment name, fund expenses, management fee, or other
- **Notice date** — date the notice is issued
- **Due date** — wire due date (typically 10 business days from notice)
- **Wire instructions** — fund bank account name, bank, ABA/SWIFT, account number (or placeholder)
- **Fund administrator contact** — name and email for LP queries

### 2. Calculate Per-LP Call Amounts

For each LP, compute:

| LP Name | Total Commitment | Previously Called | Uncalled Balance | This Call % | This Call Amount |
|---------|-----------------|-------------------|-----------------|-------------|-----------------|
| LP 1    | $X,XXX,XXX      | $X,XXX,XXX        | $X,XXX,XXX      | XX%         | $XXX,XXX        |
| ...     | ...             | ...               | ...             | ...         | ...             |
| **Total** | **$X,XXX,XXX** | **$X,XXX,XXX**   | **$X,XXX,XXX**  | **XX%**     | **$XXX,XXX**    |

Validate: each LP's call amount = uncalled balance × call percentage. Flag any LP near or at their full commitment.

### 3. Draft the Capital Call Notice

Use formal LP notice format:

```
[Fund Name]
Capital Call Notice No. [X]
Notice Date: [Date]
Due Date: [Date]

Dear [LP Name],

Pursuant to Section [X] of the Limited Partnership Agreement dated [date], [Fund Name] (the "Fund")
hereby calls capital contributions from the limited partners of the Fund.

CAPITAL CALL DETAILS
Fund: [Fund Name]
Call Number: [X]
Notice Date: [Date]
Due Date: [Date]
Purpose: [Investment in / Management Fee / Fund Expenses]

YOUR CAPITAL CALL
Commitment Amount:     $[X,XXX,XXX]
Previously Called:     $[X,XXX,XXX]
Uncalled Balance:      $[X,XXX,XXX]
This Call ([XX]%):     $[XXX,XXX]
Remaining Balance:     $[XXX,XXX]

WIRE INSTRUCTIONS
Beneficiary Name:      [Fund Name]
Bank:                  [Bank Name]
ABA / Routing:         [Number]
Account Number:        [Number]
SWIFT (international): [Code]
Reference:             [LP Name] — Capital Call No. [X]

Please wire your contribution by [Due Date] to the above account. Please send confirmation of
payment to [admin contact email].

Questions: Contact [Fund Admin Name] at [email].

[GP Signature Block]
```

Generate one notice per LP, substituting their individual amounts.

### 4. Output

Return:
1. **Summary table** — all LPs, commitments, call amounts, due date
2. **Individual notices** — one formatted notice per LP (Markdown, ready to copy into PDF/email)
3. **Total call amount** — aggregate across all LPs

If FundOS MCP is connected, call `fundos_create_capital_call` for each LP after confirming with the user.

## Important Notes

- Capital call notices trigger real LP cash movements — always confirm amounts before issuing
- Wire instructions should be verified against the fund's actual banking details before sending
- ILPA 2025 format adds a standardized Excel attachment — mention this if the user has ILPA notices enabled in FundOS
- Overdue capital contributions typically accrue interest per the LPA — note this if due date is tight
- If LPs are in different currencies, convert at the spot rate on notice date and note the rate used
