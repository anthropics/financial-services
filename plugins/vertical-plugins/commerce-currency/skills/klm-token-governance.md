---
skill: klm-token-governance
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# KLM Token Governance

## Overview

KLM is the commerce unit of the KAELUM closed-loop digital commerce currency,
issued and governed by Kaelum Technologies Ltd. KLM is not a cryptocurrency,
not blockchain-based, and not speculative. It is a fixed-floor commerce unit
governed exclusively by K.A.T.E. (Kaelum Audivo Triovus Engine).

## Core Properties

- **Floor price:** £0.09 per KLM unit (hardcoded, immutable, enforced by K.A.T.E.)
- **Price direction:** One-directional. KLM price can only rise above the floor,
  never fall below it.
- **Secondary market:** None. KLM cannot be traded, sold, or transferred outside
  the KAELUM network.
- **Redemption:** Only Merchants and Creators can redeem KLM for fiat currency
  through Kaelum Technologies Ltd. Customers cannot redeem KLM for fiat at
  any point.
- **VAT classification:** Multi-Purpose Voucher (MPV) under UK HMRC guidance.
  VAT deferred to point of merchant or creator redemption.
- **CARF status:** KLM is not a crypto-asset. CARF does not apply.

## Participant Types

KLM circulates across three participant types within the closed network:

- **Customers:** Purchase KLM at current price. Spend KLM at participating
  Merchants and Creators. Receive minimum 6% spending discount on every
  transaction. Cannot redeem KLM for fiat.
- **Creators:** Operate Social Paylinks and Commerce Drops priced in KLM.
  Purchasers receive minimum 6% discount. Can redeem accumulated KLM for
  fiat through Kaelum Technologies Ltd. Minimum Active Balance: 1,800 KLM
  (£162 at floor price).
- **Merchants:** Accept KLM as payment for goods and services. Can redeem
  accumulated KLM for fiat through Kaelum Technologies Ltd. Minimum Active
  Balance: 3,690 KLM (£332.10 at floor price).

## KLM Price Appreciation

### Governance

K.A.T.E. governs all KLM price appreciation. No appreciation event is
automatic or triggered by any single network event. K.A.T.E. continuously
monitors six signal categories and applies appreciation only when multiple
categories are trending positively simultaneously.

### Signal Categories

K.A.T.E. monitors the following six signal categories:

1. **Platform Usage** — Volume and frequency of activity across the platform
2. **KLM Sale Volume** — Total KLM purchased within a given assessment period
3. **Participant Activity** — Active Customer, Creator, and Merchant account
   engagement, new onboardings, and retention rates
4. **Transfers** — KLM transfers between participants within the network
5. **Purchases Using KLM** — Transaction volume and frequency at Merchant
   and Creator Paylink touchpoints
6. **Cross-Border Trade Settlement** — KXCS international transaction activity

### Appreciation Mechanic

When K.A.T.E. determines network conditions warrant appreciation:

- A **1.2% compounding appreciation** is applied to the KLM price ecosystem-wide
- The appreciation applies to all KLM in circulation simultaneously
- The new price becomes the active price for all subsequent transactions
- The floor price (£0.09) remains unchanged and immutable
- Every appreciation event is logged with: timestamp, previous price, new price,
  percentage applied, and K.A.T.E. signal summary

### Assessment Frequency

K.A.T.E. runs an appreciation assessment on a scheduled basis (minimum every
24 hours). The assessment produces a confidence score across all six signal
categories. Appreciation is applied only when the composite score meets the
K.A.T.E.-defined threshold. Every assessment is logged regardless of outcome,
creating a full audit trail.

### Incentive Purpose

The appreciation mechanic exists because:

- Customers cannot redeem KLM for fiat
- KLM has no secondary market and cannot be traded externally
- Appreciation provides a legitimate, non-speculative incentive for all three
  participant types to remain active and transact within the ecosystem
- The more the network grows, the more every unit of KLM already held is worth

### Regulatory Framing

KLM appreciation is:

- **Not market-driven** — determined solely by K.A.T.E. based on network signals
- **Not speculative** — one-directional, no risk of loss below the floor price
- **Not a financial instrument** — no secondary market, no transferability
  outside the network, no mechanism for speculative trading
- **Not a collective investment scheme** — participants join for commerce
  utility, not investment returns. Appreciation is a governance output of
  K.A.T.E., not a profit-sharing arrangement.

## KLM Reserve Framework (KRF)

Total hard cap: 96.3 billion KLM across three reserve tiers:

| Reserve Tier | Allocation | Purpose |
|---|---|---|
| Commerce Reserve | 36.9B KLM | KST Sub-Token deployments, merchant supply |
| Government and Institutional Reserve | 36.9B KLM | Sovereign and institutional use |
| Inter-Bloc Settlement Reserve | 22.5B KLM | Cross-border settlement (KXCS) |

KST Sub-Tokens are carved from the Commerce Reserve only. Never issued as
net new supply. At 2M KLM per KST, the Commerce Reserve supports
approximately 18,450 sub-token deployments.

## Transaction Participation Reward (TPR)

- **Rate:** 1.2% of every transaction value
- **Calculation basis:** Current KLM price at time of transaction (not floor price)
- **Allocation:** Automatically to the KPR (Kaelum Performance Reserve)
- **Distribution:** Quarterly in KLM to eligible participants

## KST Sub-Token Appreciation

KST Sub-Token slot sales are one of the six signal categories monitored by
K.A.T.E. for ecosystem-wide appreciation assessment. Sub-token activity
contributes to the composite appreciation signal but does not trigger
appreciation independently.

## Commands

- `/klm-token-governance:price-status` — Return current KLM price, floor price,
  and last appreciation event
- `/klm-token-governance:appreciation-history` — Return full appreciation log
- `/klm-token-governance:signal-status` — Return current status of all six
  K.A.T.E. appreciation signal categories
- `/klm-token-governance:tpr-calculation` — Calculate TPR for a given
  transaction value at current KLM price