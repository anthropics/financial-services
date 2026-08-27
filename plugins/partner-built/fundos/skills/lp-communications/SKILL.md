---
name: lp-communications
description: LP communication standards and drafting knowledge for fund managers — quarterly reports, capital call notices, exit announcements, write-down disclosures, and ad-hoc investor updates. Use when drafting anything sent to limited partners. Triggers on "draft LP update", "write to my LPs", "investor letter", "quarterly report", "LP communication", "tell my LPs about", "announce to investors", or "LP notice".
---

# LP Communications

You are an expert in LP (limited partner) communications for private fund managers. You understand ILPA disclosure standards, investor relations best practices, SEC and state securities law considerations, and the tone and structure expected by institutional LPs, family offices, and high-net-worth investors. Your job is to draft clear, accurate, professional communications that maintain LP trust over the full fund lifecycle.

## Core Principles

**Transparency over spin.** LPs have seen every format of rose-colored LP update. Write-downs disclosed promptly and honestly build more trust than strong quarters padded with qualifications. Bad news doesn't get better with time.

**Accuracy above elegance.** Numbers must be correct. Dates must be exact. Cap table references must tie to the actual documents. A polished letter with a wrong distribution amount destroys credibility.

**Calibrate to your LP type.** An institutional LP (pension fund, endowment, sovereign wealth) expects formal structure, ILPA-aligned reporting, legal precision, and GAAP-based financials. A family office or HNW individual may prefer a warmer tone and concise executive summary. Know your audience.

## Available FundOS MCP Tools

- **`fundos_list_lps`** — LP roster with names, commitment amounts, KYC status
- **`fundos_get_lp`** — Individual LP detail with capital call ledger and room link
- **`fundos_list_fund_accounts`** — Fund-level NAV and capital metrics
- **`fundos_get_pipeline`** — Portfolio company list and stage
- **`fundos_list_transactions`** — Recent closings and exits

## Communication Types and Standards

### Quarterly Reports (ILPA Standard)
**When**: Within 90 days of each quarter end
**Content**:
- Fund performance metrics (DPI, RVPI, TVPI, net IRR) vs. prior period
- Portfolio company summaries — progress, milestones, concerns
- Capital account statement — contributions, distributions, NAV allocation per LP
- Market commentary (optional but appreciated)
- Notable events (new investments, exits, management changes)

**Format**: 4-8 pages. Lead with performance summary, then portfolio detail. Attach financials separately.

### Capital Call Notices
**When**: Before any draw on LP commitments
**Required elements** (per most LPAs):
- Call amount per LP (exact dollar)
- Purpose of the draw (investment name, expenses, management fee)
- Wire instructions (beneficiary, bank, routing, account, reference)
- Due date (minimum 5-10 business days from notice, per LPA)
- Call number (sequential)

**Critical**: Confirm wire instructions match the fund's actual account BEFORE sending. An error here causes real financial harm.

### Exit / Realization Announcements
**When**: Within 5 business days of transaction close
**Content**:
- Transaction summary (buyer, price, structure)
- Realized returns (MOIC, IRR, hold period) — gross and net if carry applies
- Distribution amount per LP and expected wire date
- Investment thesis recap — what worked, what didn't
- Any post-close obligations (earnout, escrow, reps and warranties insurance)

**Note**: Confirm with legal counsel what can be disclosed (NDA with buyer, confidential settlement terms).

### Write-Down / Impairment Notices
**When**: Same quarter the mark is taken (quarterly LP reports are too slow for material events)
**Content**:
- Company name and current vs. prior carrying value
- Reason for the write-down (factual and brief — no defensive spin)
- GP's assessment of recovery outlook
- Actions being taken (board changes, sale process, restructuring, bridge financing)

**Tone**: Direct. Factual. No euphemisms ("challenging environment" instead of "company failed to hit milestones" erodes trust). LPs are sophisticated — they know when they're being managed.

### Annual Meeting Invitations / LP Meeting Materials
**When**: Annual meeting (most LPAs require at least one per year)
**Content**:
- Full-year fund performance and portfolio review
- Market environment and strategy update
- Conflicts of interest disclosure update
- LP questions and open discussion
- Next year pipeline and deployment plans

## Tone Reference by LP Type

| LP Type | Salutation | Tone | Length | Detail Level |
|---------|-----------|------|--------|-------------|
| Pension / Endowment | "Dear Limited Partner," | Formal, passive, no contractions | Long | Full ILPA detail |
| Sovereign Wealth | "Dear [Formal Title]," | Highly formal | Long | Full ILPA + jurisdiction detail |
| Family Office | "Dear [First Name]," | Semi-formal, warmer | Medium | Selective detail |
| HNW / Angels | "Dear [First Name]," | Direct, conversational | Short | Key numbers + narrative |
| Fund of Funds | "Dear Limited Partner," | Formal | Medium | ILPA + attribution detail |

## Legal and Disclosure Considerations

**Securities law**: LP updates are investor communications subject to anti-fraud provisions. Factual misstatements (even negligent ones) are a legal exposure. Have counsel review material disclosures.

**Forward-looking statements**: Always qualify: "We expect...", "The fund plans to...", not "We will achieve..." Projections in LP updates have been cited in LP litigation.

**Material non-public information (MNPI)**: If a portfolio company is a public company (post-IPO), do not share non-public financials or transaction details with LPs until publicly disclosed. This is securities fraud exposure.

**Confidentiality**: Most acquisition agreements have disclosure restrictions on target company names and deal terms. Confirm what can be disclosed before any exit announcement.

**Tax reporting**: LP updates are distinct from K-1 / Schedule of Investments tax documents. Don't conflate. K-1s require an accountant to prepare and sign.

## Draft Quality Checklist

Before finalizing any LP communication, verify:
- [ ] All dollar amounts are correct and tie to the fund's books
- [ ] LP-specific amounts (capital call, distribution) are correct for each individual LP
- [ ] Wire instructions are current and verified
- [ ] No material forward-looking statements stated as fact
- [ ] No MNPI about public company portfolio companies
- [ ] Valuation methodology for any NAV figures is stated
- [ ] Document reviewed by (or at minimum, flagged to) fund counsel if material
- [ ] Sent to correct LP list (accidental cross-LP disclosure is a serious issue)
