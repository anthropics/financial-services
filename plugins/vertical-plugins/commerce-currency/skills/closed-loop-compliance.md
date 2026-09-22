---
skill: closed-loop-compliance
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# Closed-Loop Compliance

## Overview

KAELUM operates as a closed-loop digital commerce currency under the
self-assessed exemption provided by UK Electronic Money Regulations 2011
Regulation 3 and EU E-Money Directive 2009/110/EC Article 1(4). This skill
governs the compliance rules, structural requirements, and participant
obligations that maintain KAELUM's closed-loop status.

## The Three Participant Types

The KAELUM closed loop operates across three participant types. All three
are covered by the same closed-loop exemption framework:

**Customers**
- Purchase KLM at current price using fiat via TrueLayer or Stripe
- Spend KLM exclusively within the KAELUM network
- Receive minimum 6% spending discount on every transaction
- Cannot redeem KLM for fiat at any point
- Cannot transfer KLM outside the network

**Creators**
- Verified commerce professionals with active public profiles
- Operate Social Paylinks and Commerce Drops within the network
- Purchasers receive minimum 6% discount on all Creator transactions
- Can redeem accumulated KLM for fiat through Kaelum Technologies Ltd
- Creator transactions operate under the same closed-loop framework
  as Merchant transactions for regulatory purposes
- Cannot issue KLM or create supply outside the Commerce Reserve

**Merchants**
- Verified businesses onboarded and contracted with Kaelum Technologies Ltd
- Accept KLM as payment for goods and services within the network
- Can redeem accumulated KLM for fiat through Kaelum Technologies Ltd
- Cannot issue KLM or create supply outside the Commerce Reserve
- Must agree to KAELUM Merchant terms before accepting KLM

## Closed-Loop Structural Rules

The following rules are enforced by K.A.T.E. at all times and cannot
be overridden:

1. **No customer cash-out:** Customers cannot convert KLM to fiat
   at any point under any circumstance
2. **Network-only spending:** KLM can only be spent within the defined
   KAELUM network of verified Merchants and Creators
3. **Issuer-only redemption:** Fiat is only released by Kaelum
   Technologies Ltd. No third party can redeem KLM for fiat
4. **No secondary market:** KLM cannot be listed, traded, or sold
   on any external platform or exchange
5. **No external transfer:** KLM cannot be transferred to any wallet,
   account, or platform outside the KAELUM network
6. **Supply integrity:** All KLM supply comes from the KRF reserves.
   No net new supply can be created outside the reserve framework
7. **Floor price immutability:** The £0.09 floor price cannot be
   reduced under any circumstance. K.A.T.E. enforces this as a
   hard governance rule
8. **One-directional appreciation:** KLM price can only rise above
   the floor, never fall below it

## Redemption Rules

Only Merchants and Creators can redeem KLM for fiat. Redemption is
subject to:

- SENTINEL AML screening before processing
- KYC verification of the redeeming Merchant or Creator
- Kaelum Technologies Ltd approval
- Current KLM price at time of redemption (not floor price)
- Fiat processed via Stripe (current) or Modulr BaaS (post-funding)

Customers are explicitly excluded from redemption under any circumstance.
This exclusion is structural, not policy-based, and is enforced by
K.A.T.E. at the platform level.

## Exemption Criteria Compliance

KAELUM's closed-loop structure satisfies the UK EMR 2011 Regulation 3
exemption criteria as follows:

| Criterion | KAELUM Position |
|---|---|
| Limited network of service providers | Defined, contracted network of verified Merchants and Creators only |
| Specific range of goods or services | Goods and services from network participants across multiple categories (MPV classification) |
| No cash redemption by end user | Customers cannot redeem. Merchants and Creators redeem through issuer only |
| Issuer control of redemption | All fiat released exclusively by Kaelum Technologies Ltd |

## KLM Price Appreciation: Compliance Position

K.A.T.E.-governed KLM price appreciation does not affect the closed-loop
compliance position. Appreciation is:

- Governed internally by K.A.T.E., not by external market forces
- One-directional and non-speculative
- Not realisable by Customers through sale or external transfer
- Logged with a full audit trail for regulatory inspection

The appreciation mechanic does not create a secondary market, does not
give KLM characteristics of a tradeable financial instrument, and does
not alter the structural closed-loop rules listed above.

## VAT Compliance

KLM is classified as a Multi-Purpose Voucher (MPV) for UK VAT purposes:

- VAT is not accounted for at the point of KLM purchase by Customers
- VAT becomes due at the point of redemption by Merchants or Creators
- The applicable rate is determined by the goods or services supplied
  at point of redemption
- Kaelum Technologies Ltd maintains redemption records for VAT reporting

## CARF Non-Applicability

KLM is not a crypto-asset for the purposes of the Crypto-Asset Reporting
Framework (CARF). KLM has:

- No secondary market
- No blockchain or distributed ledger
- No speculative characteristics
- A fixed floor price enforced by Ai governance
- No external transferability

KAELUM is not subject to the crypto tax regime.

## MiCA Pre-Alignment

KAELUM has pre-aligned with EU Markets in Crypto-Assets Regulation (MiCA)
requirements. KLM does not fall within MiCA's asset-referenced token or
e-money token definitions due to its closed-loop structure and limited
network exemption.

## Commands

- `/closed-loop-compliance:exemption-status` — Return current closed-loop
  exemption compliance status across all structural rules
- `/closed-loop-compliance:redemption-check` — Verify a participant's
  eligibility to redeem KLM for fiat
- `/closed-loop-compliance:appreciation-audit` — Return appreciation event
  log for regulatory inspection
- `/closed-loop-compliance:participant-status` — Return compliance status
  for a given participant account