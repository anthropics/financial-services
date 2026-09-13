---
skill: customer-economics
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# Customer Economics

## Overview

Customers are the spending participants within the KAELUM closed-loop network.
They purchase KLM at the current price and spend it at Merchants and Creators
within the network. Customers cannot redeem KLM for fiat at any point.
Their value growth within the ecosystem comes through spending discounts,
TPR quarterly distributions, and KLM price appreciation.

## Minimum Active Balance

- **Requirement:** 400 KLM
- **Fiat equivalent at floor price:** £36.00
- **Fiat equivalent at current price:** Calculated at current KLM price
- **Purpose:** Participation threshold, not a fee. Ensures customers have
  a meaningful stake in the network.

## How Customers Grow Value

Since Customers cannot redeem KLM for fiat and KLM has no secondary market,
value growth occurs through three mechanisms:

1. **Spending Discount:** Minimum 6% discount on every KLM transaction at
   Merchants and Creator Paylinks. Customers receive more goods and services
   per pound spent than through any traditional payment method.

2. **TPR Quarterly Distribution:** 1.2% of every transaction is allocated to
   the KPR reserve and distributed quarterly in KLM. Customer balances grow
   through participation in the network.

3. **KLM Price Appreciation:** When K.A.T.E. determines network conditions
   warrant it, a 1.2% compounding appreciation is applied to the KLM price
   ecosystem-wide. Every KLM unit a Customer holds becomes worth more without
   any action required. The appreciation is one-directional — the price can
   only rise above the £0.09 floor, never fall below it.

## Customer Account Dashboard

The Customer dashboard must display:

- Current KLM balance (unit count)
- Current KLM price (live, updated on every appreciation event)
- Current balance value in fiat (units x current price, not floor price)
- Appreciation history showing how the value of their KLM has grown over time
- Spending discount received to date (total fiat equivalent saved)
- TPR distributions received to date
- Transaction history showing KLM price at time of each transaction

## KCR Account Tiers

| Tier | KLM Purchased | Minimum Discount |
|---|---|---|
| Bronze | £60K - £179,999 | 9% |
| Silver | £180K - £269,999 | 9% |
| Gold | £270K - £359,999 | 9% |
| Platinum | £360K - £999,999 | 9% |
| Diamond | £1M - £1.8M | 9% |

KCR holders receive enhanced KLMback rates from 1.0% (Bronze) to 5.0%
(Diamond). Maximum combined rate: 14%.

## Savings Vault

The Savings Vault allows Customers to designate KLM for structured holding.
The vault displays:

- KLM units held in vault
- Current value at current KLM price (not floor price)
- Appreciation events that have occurred since vault deposit
- Projected value at various appreciation scenarios

## Commands

- `/customer-economics:balance-value` — Return customer KLM balance value
  at current KLM price
- `/customer-economics:discount-summary` — Return total spending discount
  received to date
- `/customer-economics:appreciation-impact` — Return the impact of all
  appreciation events on the customer's current balance value
- `/customer-economics:tpr-history` — Return quarterly TPR distribution history