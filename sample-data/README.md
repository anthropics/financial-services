# Sample Data

This directory contains small, fully synthetic datasets for trying the
financial-services agents and skills without connecting proprietary systems.
The records are fictional and are intended for demos, smoke tests, and prompt
development only.

## Files

| File | Use case | Suggested workflows |
|---|---|---|
| `portfolio_holdings.csv` | Wealth or asset-management portfolio review | `/client-review`, `/rebalance`, portfolio-monitoring |
| `public_company_financials.csv` | Equity research and market-analysis examples | `/comps`, `/earnings`, `/sector`, initiating coverage |
| `vendor_payment_risk.csv` | Finance operations and payment-control review | KYC screening, variance commentary, risk assessment |

## Notes

- All company names, account IDs, client names, and values are synthetic.
- The values are intentionally compact so examples can be inspected manually.
- These files are not investment, accounting, tax, or compliance advice.
- Replace the sample records with your firm's approved demo data before using
  the workflows for client-facing or production review.
