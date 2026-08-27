---
skill: sentinel-aml-rules
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# SENTINEL AML Rules

## Overview

SENTINEL is KAELUM's Ai-powered AML and compliance layer, operating
within K.A.T.E. via the Triovus governance engine. SENTINEL screens
every transaction across all three participant types (Customers,
Creators, and Merchants) in real time. It also runs scheduled batch
compliance reports via the Managed Agents API.

## Scope

SENTINEL screens:

- Every KLM purchase by Customers
- Every KLM transaction at Merchants and Creator Paylinks
- Every Commerce Drop transaction
- Every Bill Pay transaction
- Every KLM transfer within the network
- Every KXCS cross-border settlement transaction
- Every Merchant and Creator redemption request
- Every KYC onboarding and refresh event
- KLM price appreciation events (audit logging)

## Real-Time Transaction Screening

Every transaction triggers an immediate SENTINEL assessment before
processing is confirmed. The assessment evaluates:

**Transaction-level signals:**
- Transaction amount relative to participant history
- Transaction frequency patterns
- Geographic location of transaction
- Merchant or Creator risk classification
- Customer risk profile and history
- Time of transaction relative to account activity patterns

**Network-level signals:**
- Structuring patterns (multiple small transactions to avoid thresholds)
- Smurfing detection (splitting transactions across multiple participants)
- Layering patterns (rapid sequential transactions)
- Round-tripping (KLM purchased and redeemed without genuine commerce)

**Outcome:**
- PASS: Transaction processed immediately
- REVIEW: Transaction held pending Compliance and Regulatory agent review
- BLOCK: Transaction blocked. Compliance and Regulatory agent and Legal
  Counsel agent notified. Participant account flagged.

## Scheduled Batch Compliance Reports

SENTINEL runs a monthly AML batch report via the Managed Agents API
(managed-agents-2026-04-01 beta header) on the 1st of each month at
02:00 UTC. The batch report covers:

- All transactions in the preceding month across all participant types
- Pattern analysis across the full transaction dataset
- Suspicious activity summary for Compliance and Regulatory agent review
- Participant risk profile updates
- Redemption pattern analysis for Merchants and Creators
- Cross-border settlement compliance review

## Creator-Specific AML Rules

Creator Social Paylink and Commerce Drop transactions are screened
identically to Merchant transactions. Additional Creator-specific rules:

- First redemption by a new Creator triggers enhanced SENTINEL screening
- Commerce Drop transactions above threshold trigger automatic review
- Creator accounts with no prior content sales history receive elevated
  initial risk classification, reduced after 90 days of clean transaction
  history
- Creator-to-Creator transfers are monitored for unusual patterns

## KLM Price Appreciation: AML Logging

Every KLM price appreciation event applied by K.A.T.E. is logged by
SENTINEL with:

- Timestamp of appreciation event
- Previous KLM price
- New KLM price
- Percentage applied
- K.A.T.E. signal summary that triggered the assessment
- All participant account balance changes resulting from appreciation

This log is maintained for regulatory inspection and forms part of
KAELUM's audit trail for the closed-loop exemption self-assessment.

## Redemption AML Rules

Before any Merchant or Creator redemption is processed, SENTINEL runs
a full pre-redemption AML screen:

- Source of KLM verified against transaction history
- Redemption amount assessed against account history and risk profile
- Unusually large redemptions flagged for Finance agent approval
- Redemptions from recently onboarded participants subject to enhanced
  screening for 90 days
- All redemptions logged with full SENTINEL assessment record

## Risk Classification

Participants are classified on a three-tier risk scale:

| Tier | Profile | Screening Level |
|---|---|---|
| Standard | Established participants, clean history | Standard real-time screening |
| Enhanced | New participants, elevated activity, geographic flags | Enhanced screening plus periodic manual review |
| High | Active flags, suspicious patterns, escalated transactions | Blocked pending Compliance and Regulatory review |

Risk classification is reviewed and updated by SENTINEL on each
transaction and on each monthly batch report cycle.

## SENTINEL and K.A.T.E. Integration

SENTINEL operates as a cross-system agent within K.A.T.E. It:

- Receives sentinel_batch_trigger events from Paperclip on schedule
- Sends REVIEW and BLOCK outcomes to the Compliance and Regulatory agent
- Sends escalations to the Legal Counsel agent for high-risk cases
- Feeds clean transaction rate data to Commerce Intelligence for KVI
  appreciation signal monitoring
- Logs all assessments to the platform audit trail

## Regulatory Framework

SENTINEL operates in compliance with:

- UK Money Laundering Regulations 2017
- FATF Recommendations for AML/CFT
- EU Anti-Money Laundering Directive (AMLD6) principles
- KAELUM's closed-loop exemption requirements under UK EMR 2011
  Regulation 3

## Commands

- `/sentinel-aml-rules:transaction-screen` — Run SENTINEL assessment
  on a given transaction before processing
- `/sentinel-aml-rules:participant-risk` — Return current risk
  classification for a given participant
- `/sentinel-aml-rules:batch-report` — Return latest monthly SENTINEL
  batch compliance report summary
- `/sentinel-aml-rules:flag-log` — Return all active SENTINEL flags
  across the platform
- `/sentinel-aml-rules:redemption-screen` — Run pre-redemption AML
  assessment for a given Merchant or Creator redemption request
