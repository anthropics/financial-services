---
skill: kst-sub-token-mechanics
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# KST Sub-Token Mechanics

## Overview

KST (KAELUM Sub-Token) is the sub-token framework within the KAELUM
closed-loop ecosystem. KST Sub-Tokens are created by platforms, merchants,
customers, and any verified KAELUM participant. Each KST Sub-Token operates
as a branded commerce currency within the KAELUM network, carved exclusively
from the Commerce Reserve. KST slot sales contribute to the six signal
categories monitored by K.A.T.E. for ecosystem-wide KLM price appreciation.

## Core Specifications

| Property | Value |
|---|---|
| Minimum supply | 2,000,000 KLM per sub-token |
| Price per token | From £0.09 (current KLM price at time of creation) |
| Creation fee | £180,000 per slot (fiat only, not KLM) |
| Commission rate | 2.5% of every transaction in the sub-token ecosystem |
| Commission payment | Monthly in KLM at current KLM price at time of distribution |
| Slots in marketplace | 9 KAELUM sub-tokens |
| Owners per sub-token | 1 (one owner per slot) |
| Maximum slots | 9 per sub-token at £180,000 each |

## Supply Architecture

KST Sub-Tokens are carved from KAELUM's Commerce Reserve (36.9B KLM).
They are never issued as net new supply. This is a hard rule enforced
by K.A.T.E.

- Commerce Reserve: 36.9B KLM
- KLM per KST: 2,000,000
- Maximum KST deployments from Commerce Reserve: approximately 18,450

## Slot Ownership

- One ownership slot per sub-token at £180,000
- The £180,000 is a creation and ownership fee, not a fiat valuation
  of the 2M KLM tokens received
- Tokens are issued unfunded. Slot owners function as currency operators
  within their sub-token ecosystem
- Slots 2-9 are open to Customers and any verified KAELUM participant,
  not just Merchants
- The Founding Merchants Campaign offers 10 slots at £180,000 each as
  the primary non-dilutive revenue channel for Kaelum Technologies Ltd

## Commission Structure

KST slot owners earn:

- **2.5% commission** on every transaction value within their sub-token
  ecosystem
- Paid **monthly in KLM** at the current KLM price at time of distribution
- As the KLM price appreciates above the £0.09 floor, monthly commission
  payments increase in fiat-equivalent value automatically
- Full commission goes to the single slot owner. There is no commission
  splitting.

### Commission Calculation Example

If current KLM price is £0.095 (post-appreciation) and monthly sub-token
transaction volume is 500,000 KLM:

- Transaction volume in fiat: £47,500
- Commission at 2.5%: £1,187.50
- KLM equivalent at current price (£0.095): 12,500 KLM paid to slot owner

## KLM Appreciation and KST

KST slot sales are **one of six signal categories** monitored by K.A.T.E.
for ecosystem-wide KLM price appreciation assessment. They do not trigger
appreciation independently. K.A.T.E. weighs KST activity alongside all
other signal categories before determining whether to apply the 1.2%
compounding appreciation.

Benefits of KLM appreciation for KST slot owners:

- The 2M KLM received on slot purchase increases in fiat-equivalent value
- Monthly commission payments are worth more in fiat terms
- Sub-token transaction volumes may increase as participants are incentivised
  to remain active in the appreciating ecosystem

## KST Treasury Management

KST slot owners access treasury management through the KST Treasury
Management dashboard, which displays:

- Current KLM price (live, not floor price)
- Sub-token transaction volume (daily, weekly, monthly)
- Commission earned to date at current KLM price
- Commission projection at various appreciation scenarios
- KLM appreciation history and impact on treasury value
- KST Revenue Calculator (live data bridge, 60-second refresh)
- Next commission distribution date

## Quarterly Circulation Growth Bonuses

In addition to monthly commissions, KST slot owners receive quarterly
Circulation Growth Bonuses based on sub-token ecosystem growth metrics
monitored by K.A.T.E.

## Regulatory Position

KST Sub-Tokens operate within the same closed-loop exemption as the
main KAELUM network under UK EMR 2011 Regulation 3 and EU E-Money
Directive 2009/110/EC Article 1(4). KST tokens are carved from the
existing KLM Commerce Reserve and do not constitute new e-money issuance.
All KST transactions are SENTINEL-screened by K.A.T.E. in real time.

## Commands

- `/kst-sub-token-mechanics:commission-calculation` — Calculate monthly
  commission for a given transaction volume at current KLM price
- `/kst-sub-token-mechanics:treasury-value` — Return current treasury
  value of slot owner KLM holdings at current price
- `/kst-sub-token-mechanics:appreciation-impact` — Return fiat-equivalent
  impact of all appreciation events on slot owner holdings
- `/kst-sub-token-mechanics:supply-check` — Confirm Commerce Reserve
  capacity for new sub-token deployment