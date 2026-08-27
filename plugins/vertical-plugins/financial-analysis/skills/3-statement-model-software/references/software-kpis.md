# Software / SaaS KPI Reference

Precise definitions, disclosure variations, and model treatment for each KPI tracked in the `revenue_build` tab.

---

## Annual Recurring Revenue (ARR)

**Definition:** The annualized value of contracted recurring subscription revenue at a single point in time (typically end of period). Excludes one-time, professional services, and usage-based fees unless those have a contractually committed minimum.

**Formula:**
```
ARR = (Monthly Recurring Revenue) × 12
    = Sum of all active subscription contract values annualized
```

**ARR Bridge (waterfall):**
```
Beginning ARR
+ New Logo ARR          (net new customers)
+ Expansion ARR         (upsells, seat additions, tier upgrades from existing customers)
- Contraction ARR       (downgrades, seat reductions from existing customers)
- Churned ARR           (cancellations and non-renewals)
= Ending ARR
```

**Disclosure variations:**

| Company term | Model treatment |
|---|---|
| ARR | Direct input |
| MRR (Monthly Recurring Revenue) | × 12 = ARR |
| Annualized revenue run rate | Use if ARR not disclosed; treat as approximate ARR |
| Subscription revenue × 4 (quarterly filer) | Rough ARR proxy for non-ARR reporters |

**Model notes:**
- ARR is a balance-sheet-like snapshot (point in time), not a flow. The ARR bridge is the flow that explains the change.
- Subscription Revenue ≈ (Beginning ARR + Ending ARR) / 2 for annual billing cycles, or more precisely: integrate ARR over the period accounting for when revenue is earned.
- For companies with significant monthly or quarterly billing, Revenue < Ending ARR (because some customers billed in arrears have not yet paid for the full year).
- For companies with annual upfront billing, Deferred Revenue increases at renewal = ARR backlog.

---

## Gross Revenue Retention (GRR)

**Definition:** The percentage of prior-period ARR retained from the existing customer base, **excluding any expansion**. Captures the base renewal / retention quality.

**Formula:**
```
GRR = (Beginning ARR - Churned ARR - Contracted ARR) / Beginning ARR
    = 1 - Gross Churn Rate

GRR = (Beginning ARR + Expansion + Contraction + Churn) / Beginning ARR
    = Ending ARR excl. new logos / Beginning ARR

GRR ≤ 100% always (expansion is excluded by definition)
```

**Interpretation benchmarks:**
| GRR | Signal |
|---|---|
| > 95% | Best-in-class enterprise SaaS |
| 90–95% | Good enterprise retention |
| 85–90% | Acceptable; churn is manageable |
| < 85% | Elevated churn; growth headwind |
| < 80% | Structural problem; model carefully |

**Disclosure variations:**
- Some companies report "gross retention" on a logo (customer count) basis, not dollar basis — **logo GRR ≠ dollar GRR**. Always confirm the basis.
- If only NRR is disclosed, GRR cannot be derived without additional detail on expansion rates.

---

## Net Revenue Retention (NRR) / Net Dollar Retention (NDR)

**Definition:** The percentage of prior-period ARR retained from the existing customer base, **including expansion** (upsells, cross-sells, seat growth) and **net of** contraction and churn. Also called Net Dollar Retention (NDR) — the two terms are interchangeable.

**Formula:**
```
NRR = (Beginning ARR + Expansion + Contraction + Churn) / Beginning ARR
    = (Ending ARR excl. new logos) / Beginning ARR

NRR can exceed 100% when expansion > churn + contraction
NRR ≥ GRR always (expansion only adds to NRR)
Net Expansion Rate = NRR - GRR
```

**Calculation from component data (if available):**
```
NRR = (Beginning ARR + Expansion - Contraction - Churn) / Beginning ARR
```

**Interpretation benchmarks:**
| NRR | Signal |
|---|---|
| > 130% | Exceptional (Snowflake, early HubSpot) — land-and-expand working |
| 120–130% | Best-in-class enterprise |
| 110–120% | Strong; organic growth engine from installed base |
| 100–110% | Adequate; growth requires new logos |
| < 100% | Shrinking installed base ARR; new logos just to stay flat |

**Key insight:** If NRR > 100%, the existing customer base grows even without new customers. This is a powerful organic growth engine that creates compounding effects.

**ARR projection using NRR:**
```
Ending ARR = Beginning ARR × NRR + New Logo ARR
```

**Disclosure notes:**
- NRR is often calculated on a trailing 12-month basis for cohorts that were customers at the start
- Some companies exclude customers below a certain ACV threshold from NRR calculations — note this
- Snowflake, Datadog, and other usage-based businesses may have NRR > 130%; pure seat-licensed businesses typically 100–120%

---

## Remaining Performance Obligations (RPO)

**Definition:** The total contracted revenue not yet recognized — the backlog of future revenue from existing signed contracts. Defined under ASC 606. Includes both the current portion (cRPO, recognized in the next 12 months) and the non-current portion (beyond 12 months).

**Formula:**
```
Total RPO = Current RPO (cRPO) + Non-Current RPO

RPO Growth % = (Ending RPO / Prior RPO) - 1
```

**Relationship to revenue:**
```
cRPO is the best leading indicator of next-12-months subscription revenue.
Revenue recognized in next year ≤ cRPO (some cRPO may slip or be amended).
Typical recognition rate: 85–100% of cRPO converts to revenue.

Implied Revenue = cRPO × recognition_rate_assumption
```

**Why RPO matters for modeling:**
- RPO is disclosed quarterly (10-Q/10-K) under ASC 606 and provides high-confidence near-term revenue visibility
- Strong RPO growth → validated pipeline for the next 1–2 years
- Billings growth > Revenue growth → RPO growing (positive); Billings < Revenue → drawing down backlog (negative)

**Billings formula:**
```
Billings = Revenue + ΔDeferred Revenue
         = Revenue + (Ending Deferred Revenue - Beginning Deferred Revenue)

Alternatively:
Billings ≈ Ending ARR - Beginning ARR + Revenue  (approximate, annual billing basis)
```

**Disclosure variations:**
- Not all companies disclose cRPO separately; some only disclose total RPO. In this case, assume cRPO ≈ 50–65% of total RPO for typical 2-year weighted average contract terms.
- Some companies use "backlog" or "transaction price allocated to remaining performance obligations" as the equivalent term.

---

## Customer Cohort Tiers by ACV

**Definition:** ACV (Annual Contract Value) is the annualized value of a single customer's subscription contract. Companies commonly disclose the number of customers above certain ACV thresholds to illustrate upmarket motion and enterprise penetration.

**Standard tier breakpoints used by most SaaS companies:**

| Tier | Minimum ACV | Typical reporters |
|---|---|---|
| >$100K | $100,000 / year | Salesforce, ServiceNow, HubSpot, Workday |
| >$500K | $500,000 / year | ServiceNow, Veeva, Snowflake |
| >$1M | $1,000,000 / year | ServiceNow, Workday, Palantir |
| >$5M | $5,000,000 / year | ServiceNow (>$20M), Palantir (>$10M) |

**Note:** Tier breakpoints vary by company. Always use the company's actual disclosed tiers, not assumed ones. Common alternatives: >$50K, >$250K, >$10M.

**Modeling customer cohorts:**

```
Customers_tier[T+1] = Customers_tier[T] × (1 + tier_growth_rate[T+1])

Implied ARR from tier (if disclosed):
  ARR_tier = Customers_tier × Avg_ACV_tier

Cross-check:
  Total ARR ≈ Σ (Customers_tier × implied_avg_ACV_per_tier)
```

**Implied ACV formulas:**
```
Avg ACV — All customers     = ARR / Total Customers
Avg ACV — >$100K tier       = requires ARR split by tier (rarely disclosed)
Upmarket motion indicator   = YoY growth in >$1M customers vs. total customers
```

**Interpretation:**
- Faster growth in higher ACV tiers = successful upmarket motion (higher NRR, lower churn)
- Slower growth in >$1M vs. >$100K = enterprise penetration stalling
- Tier mix shift upward increases implied NRR because large customers churn less

**Forecasting customer tier growth:**
- Typically 10–25% YoY growth in the large customer tiers for high-growth SaaS
- Tier growth rates generally converge to total customer growth rates as companies mature
- Use management commentary and investor day targets where available

---

## Additional KPIs — Secondary Metrics

### Logo Churn Rate

```
Logo Churn Rate = Customers Lost / Beginning Customer Count
Logo Churn is NOT the same as Dollar Churn (GRR)
A lost large customer may be 10× the revenue impact of a lost small customer
```

### Implied Billings and Billings Growth

```
Billings = Revenue + ΔDeferred Revenue (from BS)
Billings Growth % is a leading indicator of next-quarter revenue growth
Billings > Revenue → growing backlog (bullish)
Billings < Revenue → drawing down backlog (bearish)
```

### Magic Number / Sales Efficiency

```
Magic Number = (Incremental ARR × 4) / Prior-Quarter S&M Expense
> 0.75: Efficient growth; scale S&M
0.5–0.75: Adequate efficiency
< 0.5: Sales efficiency deteriorating; investigate before scaling
```

### Rule of 40

```
Rule of 40 Score = Revenue Growth % + FCF Margin %
> 40: Healthy SaaS business balancing growth and profitability
< 40: Growth-profitability trade-off needs attention
```

### LTV / CAC Ratio

```
LTV = (ARPU × Gross Margin %) / Logo Churn Rate
CAC = S&M Expense / New Customers Added
LTV / CAC > 3x: Efficient acquisition model
LTV / CAC < 3x: Acquisition costs may not justify lifetime value
```

---

## Data Extraction from SEC Filings for Software KPIs

Software KPIs are not presented in standard GAAP financial statements. Extract from:

1. **Earnings press release** — most KPIs disclosed here first; check the supplemental metrics table
2. **10-K / 10-Q** — RPO in Notes to Financial Statements (ASC 606 disclosures), typically Note 2 or Note 3 (Revenue); customer count tiers may appear in MD&A
3. **Investor Day / supplemental slides** — ARR bridge components often only fully disclosed here
4. **Earnings call transcripts** — management commentary on NRR and GRR ranges

**Mapping common disclosure locations:**

| KPI | Location in 10-K | Typical Note |
|---|---|---|
| Remaining Performance Obligations (RPO) | Notes to Financial Statements | Note: Revenue Recognition |
| cRPO | Same as RPO | Note: Revenue Recognition |
| Deferred Revenue | Balance Sheet + Notes | Balance Sheet line item |
| Customers > threshold ACV | MD&A | Business metrics section |
| ARR | MD&A or press release | Business metrics; not required by GAAP |
| NRR / GRR | MD&A or press release | Business metrics; voluntary disclosure |

**If a KPI is not disclosed:**
- NRR: Use deferred revenue trends + billings growth as proxies. Estimate range using peer benchmarks.
- ARR: Estimate as 4× most recent quarter subscription revenue (run-rate method).
- GRR: Cannot be precisely derived without NRR + expansion split. Use peer comps (90–95% for enterprise SaaS).
- Customer tiers: Use disclosed total customer count + any tier disclosed; estimate others from percentage-of-ARR assumptions.
