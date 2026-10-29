---
skill: commerce-intelligence
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# Commerce Intelligence

## Overview

Commerce Intelligence is K.A.T.E.'s analytical layer for monitoring,
interpreting, and acting on data signals across the KAELUM ecosystem.
It feeds directly into the KVI Governance Framework and provides the
data foundation for KLM price appreciation assessments.

## Primary Data Signals Monitored

Commerce Intelligence continuously monitors all six KLM appreciation
signal categories on behalf of K.A.T.E.:

| Signal | Data Points Monitored |
|---|---|
| Platform Usage | DAU, MAU, session frequency, feature engagement |
| KLM Sale Volume | Daily/weekly/monthly KLM purchase volume, average purchase size |
| Participant Activity | New onboardings, active accounts, retention rate, churn rate |
| Transfers | Internal KLM transfer volume and frequency |
| Purchases Using KLM | Transaction count, average transaction value, merchant and creator coverage |
| Cross-Border Settlement | KXCS transaction volume, currency pairs, settlement speed |

## Secondary Signals (Supplementary)

Commerce Intelligence also monitors the following supplementary signals
which may be considered by K.A.T.E. in appreciation assessments:

- New merchant onboarding rate
- New creator onboarding rate
- KST Sub-Token slot sales
- CLD registration volume
- NFT marketplace transaction activity
- Savings Vault deposit rates
- KPR reserve balance growth
- Bill Pay utilisation rate
- SENTINEL clean transaction rate (low fraud rate signals healthy network)
- KVI composite score trend over rolling 30-day period
- Redemption float growth (gap between KLM purchased and KLM redeemed)
- Geographic spread of transactions (new regions signal organic growth)

## Intelligence Outputs

Commerce Intelligence produces the following outputs for K.A.T.E.:

1. **Daily Signal Report** — All six primary signals with current values,
   7-day trend, and 30-day baseline comparison
2. **KVI Input Data Package** — Formatted signal data for KVI Governance
   agent assessment
3. **Anomaly Alerts** — Real-time alerts when any signal drops below
   threshold or spikes unexpectedly
4. **Appreciation Readiness Score** — A daily composite score indicating
   how close the network is to appreciation threshold conditions
5. **Participant Intelligence Reports** — Segmented by Customer, Creator,
   and Merchant for K.A.T.E. agent-specific use

## Integration Points

- **KVI Governance Agent** — Receives daily signal data package
- **K.A.T.E. Orchestrator** — Receives anomaly alerts and appreciation
  readiness score
- **Merchant Performance Agent** — Receives merchant-segmented intelligence
- **Creator Studio Agent** — Receives creator-segmented intelligence
- **Transaction Insights Agent** — Shares transaction-level data
- **Fraud and Scam Detection Agent** — Shares SENTINEL clean rate data

## Commands

- `/commerce-intelligence:daily-report` — Return current day signal report
  across all six primary categories
- `/commerce-intelligence:appreciation-readiness` — Return current
  appreciation readiness score with signal breakdown
- `/commerce-intelligence:trend-analysis` — Return 30-day trend for all
  primary signals
- `/commerce-intelligence:anomaly-check` — Return any active anomaly alerts
- `/commerce-intelligence:participant-report` — Return segmented intelligence
  by participant type