---
skill: kpr-tpr-distribution
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# KPR and TPR Distribution

## Overview

The KPR (Kaelum Performance Reserve) and TPR (Transaction Participation Reward)
are KAELUM's mechanisms for distributing value back to network participants.
All calculations use the current KLM price at the time of each transaction or
distribution event, not the fixed floor price of £0.09.

## Transaction Participation Reward (TPR)

- **Rate:** 1.2% of every transaction value
- **Calculation basis:** Current KLM price at time of transaction
- **Trigger:** Every KLM transaction within the network
- **Allocation:** Automatically credited to the KPR reserve
- **Distribution:** Quarterly in KLM to eligible participants
- **Governed by:** K.A.T.E. automatically. No manual intervention required.

### TPR Calculation Example

If the current KLM price is £0.095 (post-appreciation) and a transaction
value is 1,000 KLM:

- Transaction value in fiat: £95.00
- TPR at 1.2%: £1.14
- KLM equivalent at current price (£0.095): 12 KLM credited to KPR

All TPR calculations use the current KLM price at the moment of transaction,
ensuring participants benefit from price appreciation in their TPR accrual.

## KPR (Kaelum Performance Reserve)

The KPR is the central reserve pool funded by TPR allocations from every
transaction. It is governed exclusively by K.A.T.E.

- **Funded by:** 1.2% TPR from every network transaction
- **Reserve balance displayed at:** Current KLM price (not floor price)
- **Distribution frequency:** Quarterly (1 January, 1 April, 1 July, 1 October)
- **Distribution basis:** Current KLM price at date of distribution
- **Eligible participants:** All active Customers, Creators, and Merchants
  with qualifying transaction history in the preceding quarter

## Quarterly Distribution Mechanics

At each quarterly distribution:

1. K.A.T.E. calculates total KPR balance in KLM at current KLM price
2. K.A.T.E. identifies all eligible participants and their qualifying
   transaction volumes for the preceding quarter
3. Distribution is calculated proportionally based on participant transaction
   volume as a share of total network transaction volume
4. KLM is distributed directly to participant accounts at current KLM price
5. Full distribution log is generated and stored with timestamp, price used,
   total distributed, and per-participant allocation

## KST Sub-Token Commission

KST slot owners earn a separate commission structure, distinct from TPR/KPR:

- **Rate:** 2.5% of every transaction value within their sub-token ecosystem
- **Payment:** Monthly in KLM at current KLM price at time of distribution
- **Basis:** Current KLM price at time of distribution (not floor price)
- **Governed by:** K.A.T.E. KST Treasury Management system

## Price Appreciation Impact on KPR

When K.A.T.E. applies a KLM price appreciation event:

- The KPR reserve balance increases in fiat-equivalent value automatically
  (same KLM units, higher price per unit)
- All future TPR accruals are calculated at the new higher price
- Quarterly distributions are made at the price current at distribution date
- Participants already holding KLM see their balance value increase without
  any additional action required

## Commands

- `/kpr-tpr-distribution:kpr-balance` — Return current KPR reserve balance
  in KLM and fiat equivalent at current KLM price
- `/kpr-tpr-distribution:tpr-calculation` — Calculate TPR for a given
  transaction value at current KLM price
- `/kpr-tpr-distribution:quarterly-projection` — Project next quarterly
  distribution based on current KPR balance and eligible participant count
- `/kpr-tpr-distribution:distribution-history` — Return full quarterly
  distribution history