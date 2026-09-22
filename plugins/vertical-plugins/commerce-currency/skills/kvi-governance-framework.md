---
skill: kvi-governance-framework
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# KVI Governance Framework

## Overview

The KVI (Kaelum Value Index) is KAELUM's Ai-governed framework for monitoring
ecosystem health and producing KLM price appreciation recommendations for
K.A.T.E. The KVI does not trigger appreciation directly. It monitors, weighs,
and reports. K.A.T.E. makes the final appreciation decision.

## Role of the KVI Agent

The KVI Governance agent (claude-opus-4-7) is responsible for:

- Continuously monitoring all six KLM appreciation signal categories
- Weighting signals according to the KVI formula
- Producing a composite health score and appreciation confidence score
- Reporting to K.A.T.E. when composite conditions meet the appreciation threshold
- Logging every assessment with full signal data and confidence scores
- Alerting relevant participants when KLM price changes occur

## Six Signal Categories and Weighting

| Signal Category | Description | Weight |
|---|---|---|
| Platform Usage | Volume and frequency of platform activity | 20% |
| KLM Sale Volume | Total KLM purchased in assessment period | 20% |
| Participant Activity | Customer, Creator, Merchant engagement and onboardings | 20% |
| Transfers | KLM transfers within the network | 10% |
| Purchases Using KLM | Transaction volume at Merchants and Creator Paylinks | 20% |
| Cross-Border Settlement | KXCS international transaction activity | 10% |

Weights are indicative. K.A.T.E. may adjust weighting dynamically based on
ecosystem maturity and strategic priorities. Any weighting adjustment must be
logged and approved by Greggar Deterville (CEO).

## Assessment Workflow

1. KVI agent pulls current data for all six signal categories
2. KVI agent applies weighting formula and produces composite health score (0-100)
3. KVI agent produces appreciation confidence score (0-100)
4. If confidence score meets K.A.T.E. threshold, KVI agent sends appreciation
   recommendation to K.A.T.E. with full supporting data summary
5. K.A.T.E. reviews recommendation and applies 1.2% compounding appreciation
   if approved
6. Appreciation event logged in KLMPrice entity with full audit trail
7. Content and Notification agent sends appreciation notification to all active
   Customers, Creators, and Merchants

## KVI Score Interpretation

| Score Range | Status | Action |
|---|---|---|
| 0-39 | Weak | No appreciation. Monitor closely. |
| 40-59 | Stable | No appreciation. Network healthy but not growing. |
| 60-79 | Growing | Appreciation consideration. K.A.T.E. evaluates. |
| 80-100 | Strong | Appreciation recommended. K.A.T.E. applies if approved. |

## KVI Dashboards

### KST Treasury Dashboard (Slot Owner View)
- Current KLM price
- Floor price (£0.09)
- Appreciation history (date, previous price, new price, percentage)
- Current signal status across all six categories
- Projected commission value at current KLM price
- Next KVI assessment timestamp

### KVI Creator Dashboard
- Current KLM price and appreciation history
- Current network signal status (simplified view)
- Balance value at current KLM price

### Admin Control Panel (CEO View)
- Full KVI assessment log including all confidence scores
- Signal data at time of each assessment
- Appreciation event history
- K.A.T.E. recommendation log
- KLM price management panel (read-only below floor price)

## Threshold Alert System

The KVI agent monitors for threshold breaches across all signals and alerts
K.A.T.E. and the Admin panel when:

- Any single signal category drops below 30% of its baseline
- The composite KVI score drops below 40 for three consecutive assessments
- Platform transaction volume drops more than 20% week on week
- New merchant or creator onboarding rate drops to zero for seven consecutive days

## Commands

- `/kvi-governance-framework:current-score` — Return current KVI composite score
  and signal breakdown
- `/kvi-governance-framework:assessment-log` — Return last 10 KVI assessments
  with confidence scores
- `/kvi-governance-framework:signal-detail` — Return detailed data for all
  six signal categories
- `/kvi-governance-framework:appreciation-recommendation` — Run immediate
  KVI assessment and return recommendation without applying appreciation
