---
skill: merchant-economics
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# Merchant Economics

## Overview

Merchants are the commerce backbone of the KAELUM closed-loop network.
They accept KLM as payment for goods and services and are one of two
participant types (alongside Creators) who can redeem KLM for fiat through
Kaelum Technologies Ltd. All Merchant KLM calculations use the current
KLM price, not the fixed floor price.

## Minimum Active Balance

- **Requirement:** 3,690 KLM
- **Fiat equivalent at floor price:** £332.10
- **Fiat equivalent at current price:** Calculated at current KLM price

## Merchant Benefits

- Zero chargebacks by design
- No Visa or Mastercard interchange fees
- Customers spend more per transaction due to 6% minimum discount incentive
- KLM accumulates in value through K.A.T.E.-governed appreciation
- Monthly KST commission if slot owner (2.5% of sub-token ecosystem
  transaction value)
- Access to K.A.T.E. Merchant Performance agent for daily intelligence

## Transaction Economics

For every KLM transaction a Merchant accepts:

- Merchant receives KLM at current KLM price per unit
- 1.2% TPR is allocated automatically to KPR reserve
- SENTINEL screens the transaction in real time
- Transaction is logged at the KLM price current at time of transaction

## KST Sub-Token Slot Ownership

Merchants (alongside Customers, Creators, and platforms) can own KST
Sub-Token slots:

- **Creation fee:** £180,000 per slot (fiat only)
- **Commission:** 2.5% of every transaction in the sub-token ecosystem
- **Payment:** Monthly in KLM at current KLM price at time of distribution
- **Slots available:** 9 KAELUM sub-tokens in marketplace
- **Appreciation trigger:** KST slot sales are one of the six signal
  categories monitored by K.A.T.E. for ecosystem-wide KLM appreciation

## KLM Price Appreciation Impact on Merchants

When K.A.T.E. applies appreciation:

- All KLM held by the Merchant increases in fiat-equivalent value
- Future transactions are settled at the new higher KLM price
- Redemptions after appreciation yield more fiat per KLM unit
- KST monthly commissions are paid at the appreciated price
- The Merchant's Active Balance of 3,690 KLM grows in fiat value

## Merchant Redemption

- Processed by Kaelum Technologies Ltd
- Current rail: Stripe
- Post-funding rail: Modulr BaaS (SEPA/SCT Inst, Faster Payments, SWIFT)
- Redemption value at current KLM price at time of redemption
- Subject to SENTINEL AML screening

## Merchant Dashboard Displays

- Current KLM balance at current KLM price (not floor price)
- Total fiat-equivalent value of KLM held
- Appreciation history and impact on balance value
- Transaction history with KLM price at time of each transaction
- KST commission earnings at current KLM price
- Daily K.A.T.E. Merchant Performance summary
- Bill Pay history

## Bill Pay

Merchants can use accumulated KLM to pay business expenses within the
KAELUM network, keeping KLM circulating within the closed loop and
contributing to network health signals monitored by K.A.T.E.

## Commands

- `/merchant-economics:balance-value` — Return Merchant KLM balance at
  current KLM price
- `/merchant-economics:redemption-value` — Return fiat value of a given
  KLM amount at current price
- `/merchant-economics:kst-commission` — Return KST commission earned
  at current KLM price
- `/merchant-economics:appreciation-impact` — Return impact of all
  appreciation events on Merchant balance value
- `/merchant-economics:transaction-summary` — Return transaction volume
  and KLM accumulation summary