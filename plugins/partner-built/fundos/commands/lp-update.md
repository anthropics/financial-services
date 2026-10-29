---
description: Draft a formal LP update communication for a specific fund event or milestone
argument-hint: "[situation type, e.g. 'new investment in Acme Corp' or 'portfolio exit']"
---

# LP Update

> This command uses the FundOS MCP server. See the [README](../README.md) for connection requirements.

Draft a polished, ready-to-send LP communication for a specific situation — new investment, portfolio exit, write-down, fund close, market commentary, or ad-hoc update. Calibrated to the fund's voice and LP relationship type.

See the **lp-communications** skill for LP communication standards, tone guidance, and disclosure obligations.

## Workflow

### 1. Gather Inputs

Ask the user for:

- **Situation type** — choose one:
  - New investment announcement
  - Portfolio company exit / realization
  - Follow-on investment
  - Write-down or impairment notice
  - First close / subsequent close / final close
  - Fund milestone (deployment, DPI threshold, vintage anniversary)
  - Market commentary / macro update
  - Portfolio company material event (CEO change, acquisition, financing, distress)
  - Annual meeting invitation
  - Ad-hoc update

- **Key facts** for the situation:
  - Company name, sector, deal size, ownership %
  - For exits: realized proceeds, MOIC, IRR, hold period
  - For write-downs: new carrying value, reason, recovery outlook
  - For closes: total capital committed to date, target fund size

- **Tone** — formal (institutional LPs: pensions, endowments, sovereigns) or semi-formal (family offices, HNW, angels)

- **LP relationship context** — founding LP, new LP, difficult LP, LP who passed on prior fund

- **Send to** — all LPs, a single LP, or a subset

### 2. Select Template Structure

**New Investment**
```
Subject: [Fund Name] — New Investment: [Company Name]

We are pleased to announce that [Fund Name] has completed its investment in [Company Name],
a [description] based in [location].

INVESTMENT OVERVIEW
Company:           [Name]
Sector:            [Sector]
Round / Structure: [Series X / Debt / Equity]
Fund Investment:   $X,XXX,XXX
Total Round:       $XX,XXX,XXX (if disclosed)
Co-Investors:      [Names]

INVESTMENT THESIS
[3-5 bullet points on why we invested: team, market, product, traction, our edge]

This investment represents [Fund]'s [Xth] portfolio company and brings total deployed capital to
$XX,XXX,XXX ([XX]% of committed capital).

[Signature]
```

**Exit / Realization**
```
Subject: [Fund Name] — Exit: [Company Name]

We are pleased to report that [Fund Name] has realized its investment in [Company Name].

REALIZATION SUMMARY
Company:           [Name]
Buyer:             [Acquirer / IPO / Secondary]
Gross Proceeds:    $XX,XXX,XXX
Cost Basis:        $X,XXX,XXX
Gross MOIC:        X.Xx
Gross IRR:         XX.X%
Hold Period:       X.X years
Transaction Close: [Date]

DISTRIBUTION DETAILS
Total Distribution to LPs: $XX,XXX,XXX
Your Distribution:          $X,XXX,XXX (see capital account statement attached)
Wire Date:                  [Date]

[Investment thesis recap, why it worked, key value creation levers]

[Signature]
```

**Write-Down**
```
Subject: [Fund Name] — Portfolio Update: [Company Name]

We want to provide you with a transparent update on our investment in [Company Name].

During [quarter], the Fund marked down its investment in [Company Name] from $[X.Xm] to
$[X.Xm] (a write-down of $[Xm] or [XX]%). This reflects [reason: deteriorating performance /
failed fundraise / market conditions / impairment].

CURRENT STATUS
Carrying Value:    $X,XXX,XXX ([X]% of cost)
Reason:            [Clear, factual explanation]
Recovery Outlook:  [Honest assessment]
Actions Underway:  [Board changes / restructuring / sale process / bridge financing]

[1-2 paragraphs: what happened, what we're doing about it, honest outlook]

We remain committed to managing this position actively in the interests of the Fund.

[Signature]
```

### 3. Tone Calibration

**Formal (institutional)**: Use full fund name, legal titles, no contractions, passive voice where appropriate, formal salutation "Dear Limited Partner," and formal close.

**Semi-formal (family office / HNW)**: Use first names if relationship warrants, direct voice, brief and punchy, may use contractions, casual close "Best regards."

### 4. Output

Return:
1. **Draft communication** — formatted, ready to send, with placeholders in `[brackets]`
2. **Subject line options** — 2-3 variants
3. **Key facts checklist** — confirm before sending (amounts, dates, names)
4. **Legal/disclosure reminder** — any items that warrant counsel review (material non-public information, forward-looking statements, clawback references)

## Important Notes

- LP updates that reference specific returns or valuations constitute financial disclosures — have counsel review before sending material write-downs or realized returns
- Write-downs should be disclosed promptly and accurately — omission or delay erodes LP trust more than the write-down itself
- Exit announcements often have confidentiality restrictions from the buyer — confirm what can be disclosed before sending
- For all-LP distributions, attach the per-LP capital account statement or wire detail separately, not in the body
- Never include forward-looking performance projections as commitments — frame as plans or expectations
