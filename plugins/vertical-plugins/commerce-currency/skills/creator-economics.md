---
skill: creator-economics
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# Creator Economics

## Overview

Creators are verified commerce professionals within the KAELUM closed-loop
network. They operate Social Paylinks and Commerce Drops priced in KLM,
earning KLM through purchaser transactions. Creators can redeem KLM for
fiat through Kaelum Technologies Ltd. All Creator KLM calculations use the
current KLM price, not the fixed floor price.

## Onboarding Requirements

- Active public profile with content history (required for verification)
- Minimum Active Balance: 1,800 KLM (£162 at floor price)
- Social profile verification completed
- Creator terms agreed with Kaelum Technologies Ltd

## Creator Tools

| Tool | Description |
|---|---|
| Creator Studio | Central dashboard governed by K.A.T.E. |
| Social Paylinks | Direct commerce links priced in KLM |
| Commerce Drops | Time-limited releases moderated by K.A.T.E. |
| Creator Advisor | K.A.T.E.-powered commerce intelligence |
| Bill Pay | Pay business expenses using accumulated KLM |
| Savings Vault | Designate KLM for structured holding |
| KST Revenue Calculator | Live KST data bridge |
| KVI Creator Dashboard | Network health and appreciation visibility |
| Research Scout | K.A.T.E. research agent access |
| Referral Hub | Network growth tools |

## Social Paylinks

- Purchasers receive minimum **6% spending discount** on every transaction
- Discount applies on top of the current KLM price
- Fiat equivalent displayed to purchasers at current KLM price
- All transactions SENTINEL-screened by K.A.T.E. in real time
- Creator accumulates KLM at current price per transaction

## Commerce Drops

- Time-limited product or content releases priced in KLM
- Automatically moderated by K.A.T.E. Commerce Drop agent
- Purchasers receive minimum 6% discount
- Drop pricing set by Creator in KLM at current price

## Creator Redemption

Creators are one of two participant types (alongside Merchants) who can
redeem KLM for fiat:

- Redemption processed by Kaelum Technologies Ltd
- Current rail: Stripe
- Post-funding rail: Modulr BaaS
- Redemption value calculated at current KLM price at time of redemption
- Redemption subject to SENTINEL AML screening

## KLM Price Appreciation Impact on Creators

When K.A.T.E. applies appreciation:

- All KLM held by the Creator increases in fiat-equivalent value
- Future Paylink and Commerce Drop transactions are priced at the new
  higher KLM price
- Redemptions after appreciation yield more fiat per KLM unit
- The Creator's Active Balance of 1,800 KLM grows in fiat value
  automatically

## Creator Dashboard Displays

- Current KLM balance at current KLM price (not floor price)
- Appreciation history and impact on balance value
- Total KLM earned through Paylinks and Commerce Drops
- Total fiat redeemed to date
- Current network signal status (simplified KVI view)
- Bill Pay history
- Savings Vault balance at current KLM price

## Bill Pay

Creators can use accumulated KLM to pay business expenses within the
KAELUM network. This keeps KLM circulating within the closed loop rather
than triggering fiat redemption, which benefits the network health signals
monitored by K.A.T.E. for appreciation assessments.

## Commands

- `/creator-economics:balance-value` — Return Creator KLM balance at
  current KLM price
- `/creator-economics:paylink-earnings` — Return total KLM earned through
  Paylinks and Commerce Drops
- `/creator-economics:redemption-value` — Return fiat value of a given
  KLM amount at current price
- `/creator-economics:appreciation-impact` — Return impact of all
  appreciation events on Creator balance value