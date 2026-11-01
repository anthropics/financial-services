# Software Revenue Forecasting Methodologies

Five methodologies for projecting subscription revenue in software / SaaS models. Choose the **primary methodology** based on data availability; use 1–2 others as cross-checks.

---

## How to Choose a Methodology

| Methodology | Best when… | Data required |
|---|---|---|
| 1. ARR Bridge | Company discloses ARR components; high-growth, land-and-expand model | Beginning ARR, NLB ARR, expansion, churn — or at least ARR + NRR |
| 2. NRR-Based | NRR disclosed; company does not break out ARR bridge components | Beginning ARR, NRR %, new logo ARR estimate |
| 3. Customer Cohort | Company discloses customer tier counts and they're the key growth driver | Customers by ACV tier, avg ACV per tier, tier retention rates |
| 4. RPO-Anchored | Strong RPO/cRPO disclosure; revenue visibility is the key investment debate | cRPO balance, historical recognition rate, RPO growth % |
| 5. Top-Down Growth | Insufficient granular data; early-stage or SMB-focused company | Revenue growth % assumption; calibrated vs. peers and guidance |

**Default recommendation:** Use Method 1 (ARR Bridge) when ARR is disclosed, since it ties to the most fundamental SaaS growth drivers. Method 2 (NRR-Based) is a close second when ARR bridge components are not separately available.

---

## Method 1: ARR Bridge / Waterfall

### Mechanics

Model each ARR component separately, then derive revenue from the ARR bridge.

```
STEP 1: Build the ARR Bridge

Beginning ARR[T]         = Ending ARR[T-1]         (green link to prior year)
+ New Logo ARR[T]        = New Customers × Avg ACV at signing
+ Expansion ARR[T]       = Beginning ARR × Expansion Rate %
- Contraction ARR[T]     = Beginning ARR × Contraction Rate %   (enter as negative)
- Churned ARR[T]         = Beginning ARR × Gross Churn Rate %   (enter as negative)
= Ending ARR[T]          = Beginning + New Logo + Expansion + Contraction + Churn

STEP 2: Derive Subscription Revenue from ARR

Average ARR[T]           = (Beginning ARR[T] + Ending ARR[T]) / 2
Billing Timing Factor    = 1.0 (annual upfront) | 0.95-0.98 (partial arrears) | varies
Subscription Revenue[T]  = Average ARR[T] × Billing Timing Factor

STEP 3: Implied NRR Check
Implied NRR[T]  = (Ending ARR[T] - New Logo ARR[T]) / Beginning ARR[T]
```

### Assumption Drivers (in Assumptions tab)

```
New Logo ARR Growth %   [per year] — derived from: New Logo ARR[T] = New Logo ARR[T-1] × (1 + growth)
Expansion Rate %        [per year] — % of beginning ARR from existing customer upsells
Contraction Rate %      [per year] — % of beginning ARR lost to downgrades (enter negative in formula)
Gross Churn Rate %      [per year] — % of beginning ARR lost to cancellations (= 1 - GRR)
Billing Timing Factor   [per year] — typically 0.97–1.00 for enterprise SaaS
```

### Excel Formulas (row references are examples; adjust to actual layout)

```excel
' revenue_build tab, projection columns (E = FY+1, F = FY+2, G = FY+3)

' E5: Beginning ARR = prior year ending ARR
E5 = "=D10"

' E6: New Logo ARR = prior year new logo × (1 + growth)
E6 = "=D6*(1+Assumptions!$B$[new_logo_growth_row])"

' E7: Expansion ARR = beginning ARR × expansion rate
E7 = "=E5*Assumptions!$B$[expansion_rate_row]"

' E8: Contraction ARR = -beginning ARR × contraction rate
E8 = "=-E5*Assumptions!$B$[contraction_rate_row]"

' E9: Churn ARR = -(beginning ARR × gross churn rate)  where gross churn = 1 - GRR
E9 = "=-E5*(1-Assumptions!$B$[GRR_row])"

' E10: Ending ARR
E10 = "=E5+E6+E7+E8+E9"

' E41: Subscription Revenue (the IS link cell)
E41 = "=((E5+E10)/2)*Assumptions!$B$[billing_timing_row]"
```

### Sanity Checks

```
Implied NRR   = (Ending ARR - New Logo ARR) / Beginning ARR   → should ≈ disclosed NRR
GRR           = 1 - (ABS(Churn ARR) / Beginning ARR)          → should ≈ disclosed GRR
ARR growth    = Ending ARR / Beginning ARR - 1                → compare to management guide
```

---

## Method 2: NRR-Based Method

### Mechanics

Use NRR as the single driver of existing base ARR growth, then add a new logo layer.

```
STEP 1: Split ARR into existing base and new logos

Existing Base ARR[T]     = Beginning ARR[T] × NRR[T]
New Logo ARR[T]          = New logo ARR estimate (from Assumptions tab)
Ending ARR[T]            = Existing Base ARR[T] + New Logo ARR[T]

STEP 2: Derive revenue (same as Method 1)

Average ARR[T]           = (Beginning ARR[T] + Ending ARR[T]) / 2
Subscription Revenue[T]  = Average ARR[T] × Billing Timing Factor
```

**Key advantage:** This method requires only NRR and a new logo estimate — both more commonly disclosed than full ARR bridge components.

**Key limitation:** NRR is a single compound metric; it obscures whether strong NRR comes from high expansion or simply low churn. Use GRR as a cross-check.

### Assumption Drivers

```
NRR %               [per year]
New Logo ARR ($M)   [per year — either absolute or as % of beginning ARR]
Billing Timing      [per year]
```

### Excel Formulas

```excel
' Existing base ARR
E[existing_base_row] = "=E5*Assumptions!$B$[NRR_row]"

' New logo ARR
E6 = "=Assumptions!$B$[new_logo_ARR_row]"

' Ending ARR
E10 = "=E[existing_base_row]+E6"

' Subscription Revenue
E41 = "=((E5+E10)/2)*Assumptions!$B$[billing_timing_row]"
```

### Cross-Check: Implied GRR

```
Implied GRR      ≈ NRR - Net Expansion Rate
Net Expansion %  = NRR - GRR
If NRR = 115% and Expansion Rate = 20%, then implied GRR ≈ 95%
Flag if implied GRR < 80% or > 100%
```

---

## Method 3: Customer Cohort / Tier-Based Method

### Mechanics

Model revenue from the bottom up by customer tier: count of customers at each ACV threshold multiplied by implied average ACV, accounting for tier-specific retention.

```
STEP 1: Project customer counts by tier

Customers_>$1M[T]    = Customers_>$1M[T-1] × (1 + tier_growth_rate_$1M[T])
Customers_>$500K[T]  = Customers_>$500K[T-1] × (1 + tier_growth_rate_$500K[T])
Customers_>$100K[T]  = Customers_>$100K[T-1] × (1 + tier_growth_rate_$100K[T])
Total Customers[T]   = Total_Customers[T-1] × (1 + total_customer_growth[T])

STEP 2: Estimate ARR contribution per tier

ARR_>$1M tier   = Customers_>$1M × Avg_ACV_$1M_tier × (1 + ACV_escalation)
ARR_>$500K tier = (Customers_>$500K - Customers_>$1M) × Avg_ACV_$500K_tier × (1 + ACV_escalation)
ARR_>$100K tier = (Customers_>$100K - Customers_>$500K) × Avg_ACV_$100K_tier × (1 + ACV_escalation)
ARR_SMB tier    = (Total - Customers_>$100K) × Avg_ACV_SMB × (1 + ACV_escalation)
Total ARR       = Sum of all tier ARR

STEP 3: Derive subscription revenue

Subscription Revenue = Average ARR × Billing Timing Factor
```

**Key advantage:** Directly models upmarket motion and tier mix shift — important when the investment thesis is about moving to enterprise.

**Key limitation:** Requires tier-level ACV assumptions that are rarely fully disclosed. Often requires management commentary or investor day presentations.

### Assumption Drivers

```
Customers >$1M Growth %     [per year]
Customers >$500K Growth %   [per year]
Customers >$100K Growth %   [per year]
Total Customer Growth %     [per year]
Avg ACV — >$1M tier ($M)    [base period, then escalate]
Avg ACV — >$500K tier ($K)  [base period, then escalate]
Avg ACV — >$100K tier ($K)  [base period, then escalate]
Avg ACV — SMB tier ($K)     [base period, then escalate]
ACV Escalation % per year   [applies to all tiers]
```

### Excel Formulas

```excel
' Tier customer projections (rows 30–34 in revenue_build)
E30 = "=D30*(1+Assumptions!$B$[cust_100K_growth])"   ' >$100K customers
E31 = "=D31*(1+Assumptions!$B$[cust_500K_growth])"   ' >$500K customers
E32 = "=D32*(1+Assumptions!$B$[cust_1M_growth])"     ' >$1M customers
E33 = "=D33*(1+Assumptions!$B$[cust_5M_growth])"     ' >$5M customers
E34 = "=D34*(1+Assumptions!$B$[total_cust_growth])"  ' total customers

' Tier ARR calculations (in Methodology section, rows 55–65)
E55 = "=E33*Assumptions!$B$[avg_ACV_5M]*(1+Assumptions!$B$[ACV_esc])"   ' >$5M tier ARR
E56 = "=(E32-E33)*Assumptions!$B$[avg_ACV_1M]*(1+Assumptions!$B$[ACV_esc])"  ' $1M–$5M band
E57 = "=(E31-E32)*Assumptions!$B$[avg_ACV_500K]*(1+Assumptions!$B$[ACV_esc])"
E58 = "=(E30-E31)*Assumptions!$B$[avg_ACV_100K]*(1+Assumptions!$B$[ACV_esc])"
E59 = "=(E34-E30)*Assumptions!$B$[avg_ACV_SMB]*(1+Assumptions!$B$[ACV_esc])"
E60 = "=SUM(E55:E59)"   ' Total ARR from cohort build

' Subscription Revenue
E41 = "=((D60+E60)/2)*Assumptions!$B$[billing_timing]"
```

---

## Method 4: RPO-Anchored Method

### Mechanics

Use cRPO (current Remaining Performance Obligations) as the anchor for near-term subscription revenue, since cRPO represents contracted revenue to be recognized in the next 12 months.

```
STEP 1: Project total RPO

RPO[T]       = RPO[T-1] × (1 + RPO_growth[T])

STEP 2: Project cRPO

cRPO[T]      = RPO[T] × cRPO_pct[T]
                (cRPO % of total RPO typically 55–70% for ~2-year avg contract terms)

STEP 3: Estimate revenue from cRPO

Recognition Rate[T]         = % of beginning cRPO that converts to revenue next year
                              (typically 85–100%; use 90–95% as base case)
Subscription Revenue[T]     = Beginning_cRPO[T] × Recognition_Rate[T]
                              + residual_revenue_from_new_deals_closed_in_year[T]

Simplified version:
Subscription Revenue[T]     = cRPO[T-1] × Recognition_Rate[T]
```

**Key advantage:** RPO is a GAAP-audited number disclosed quarterly under ASC 606. It provides the highest confidence near-term revenue anchor available.

**Key limitation:** RPO reflects contracts signed, not necessarily future billing; ramp deals and multi-year contracts can complicate the mapping to annual revenue.

**When to use:** Best for mature, contract-heavy enterprise software companies (ServiceNow, Salesforce, Workday) where multi-year contracts dominate and RPO backlog is large relative to revenue.

### Assumption Drivers

```
RPO Growth %            [per year]
cRPO as % of Total RPO  [per year]
Revenue Recognition %   [per year — % of beginning cRPO recognized as revenue]
```

### Excel Formulas

```excel
' RPO roll-forward (rows 22–23 in revenue_build)
E22 = "=D22*(1+Assumptions!$B$[RPO_growth])"
E23 = "=E22*Assumptions!$B$[cRPO_pct]"

' Subscription revenue from RPO
E41 = "=D23*Assumptions!$B$[recog_rate]"
```

### RPO Coverage Cross-Check (row 26)

```excel
' cRPO as % of next-year projected revenue — measures backlog coverage
E26 = "=E23/F41"   ' Current period cRPO / next year's projected revenue
' Flag if coverage < 60% (low confidence) or > 130% (very high visibility)
```

---

## Method 5: Top-Down Growth Rate

### Mechanics

Apply a direct revenue growth rate assumption to total or subscription revenue. Simplest method; used when granular KPI data is unavailable or as a final cross-check on complexity.

```
Subscription Revenue[T]  = Subscription Revenue[T-1] × (1 + sub_growth_rate[T])
PS Revenue[T]            = Subscription Revenue[T] × PS_pct[T]
Total Revenue[T]         = Subscription Revenue[T] + PS Revenue[T]
```

**Calibration:** Set growth rates using:
1. Management guidance range (typically the anchor)
2. Sell-side consensus (Bloomberg, FactSet, Visible Alpha)
3. Historical growth rate trajectory (decelerate 5–10 ppts/year as scale increases)
4. Peer group growth rates at comparable scale

### Assumption Drivers

```
Subscription Revenue Growth %  [per year]
PS Revenue as % of Sub Revenue [per year]
```

### Excel Formulas

```excel
E41 = "=D41*(1+Assumptions!$B$[sub_growth])"
E42 = "=E41*Assumptions!$B$[PS_pct]"
E43 = "=E41+E42"
```

---

## Linking Revenue to the IS Tab

Regardless of which methodology drives Row 41 in `revenue_build`, the IS subscription revenue projection cells must reference `revenue_build` as green cross-sheet links.

### IS Tab Formula Pattern

```excel
' IS subscription revenue projection cells
IS!E[sub_row] = "=revenue_build!E41"   ' green font
IS!F[sub_row] = "=revenue_build!F41"   ' green font
IS!G[sub_row] = "=revenue_build!G41"   ' green font

' IS professional services projection cells
IS!E[ps_row] = "=revenue_build!E42"   ' green font
IS!F[ps_row] = "=revenue_build!F42"   ' green font
IS!G[ps_row] = "=revenue_build!G42"   ' green font

' IS Total Revenue remains a formula (no change from base model)
IS!E[rev_row] = "=IS!E[sub_row]+IS!E[ps_row]"  ' black font (same-sheet formula)
```

### Methodology Selector Logic (Assumptions Tab)

If the model implements all five methodologies, use the Assumptions tab selector to route the correct methodology's output into Row 41:

```excel
' In Assumptions tab: dropdown with Data Validation
' Cell = Methodology Selector: 1 = ARR Bridge, 2 = NRR-Based, 3 = Cohort, 4 = RPO, 5 = Top-Down

' In revenue_build Row 41 (the master output row):
E41 = "=CHOOSE(Assumptions!$B$[selector],
        E[ARR_bridge_rev],
        E[NRR_based_rev],
        E[cohort_rev],
        E[RPO_anchored_rev],
        E[top_down_rev])"
```

If simplicity is preferred, hardcode the primary methodology's formula directly in Row 41 and show alternatives in the cross-check section only.

---

## Cross-Check Comparison Table

In the revenue_build cross-check section (rows 72–77), compare all methodologies for each projection year:

```
                        FY[T+1]E   FY[T+2]E   FY[T+3]E
Method 1: ARR Bridge    $X,XXX     $X,XXX     $X,XXX
Method 2: NRR-Based     $X,XXX     $X,XXX     $X,XXX
Method 3: Cohort        $X,XXX     $X,XXX     $X,XXX
Method 4: RPO-Anchored  $X,XXX     $X,XXX     $X,XXX
Method 5: Top-Down      $X,XXX     $X,XXX     $X,XXX

vs. Primary (delta %)
  Method 2 delta        XX%        XX%        XX%
  Method 3 delta        XX%        XX%        XX%
  Method 4 delta        XX%        XX%        XX%
  Method 5 delta        XX%        XX%        XX%

Flag: if any delta > ±15%, review and reconcile assumptions
```

**Formula pattern for delta check:**
```excel
E75 = "=E73/E70-1"    ' Method 2 vs. Primary
E76 = "=E74/E70-1"    ' Method 3 vs. Primary
```

**Conditional formatting on delta rows:** apply light red fill when `ABS(delta) > 15%` to flag divergence automatically.

---

## Billing Timing Adjustment Reference

The relationship between ARR (a balance-sheet snapshot) and Revenue (a flow) depends on billing terms:

| Billing Model | Timing Factor | Notes |
|---|---|---|
| Annual upfront (Jan 1) | ≈ 1.00 | ARR ≈ Revenue for full-year subscribers |
| Annual upfront (mid-year mix) | 0.97–1.00 | Slight timing difference on additions |
| Monthly billing | Variable | Revenue = actual MRR earned; ARR overstates near-term cash |
| Multi-year upfront | > 1.00 in Year 1 | Deferred revenue front-loaded; normalize via avg |
| Quarterly billing | ≈ 0.99 | Minor difference |
| Usage-based (consumption) | < 1.00 | ARR = committed minimum; revenue can exceed if usage > commitment |

**Default assumption for pure enterprise SaaS:** Billing Timing Factor = 1.00 unless disclosed otherwise.

**Usage-based businesses (Snowflake, Datadog, Fastly):**
- Committed ARR (from contracts) understates revenue when consumption exceeds minimums
- Model consumption revenue separately as: Committed Revenue + Usage Overage (% above minimum × overage rate)
- NRR can exceed 150%+ for usage-based models with high consumption growth
