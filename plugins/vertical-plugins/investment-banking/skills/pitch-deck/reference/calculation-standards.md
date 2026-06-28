# Calculation Verification Reference

This file provides formulas and guidelines for verifying pre-calculated values in source data before populating templates. Source data should already contain calculated figures—use these formulas to verify accuracy.

## Contents

- [Key Verification Formulas](#key-verification-formulas)
- [Consensus Methodology](#consensus-methodology)
- [Rounding Guidelines](#rounding-guidelines)
- [Verification Checklist](#verification-checklist)
- [Red Flags to Investigate](#red-flags-to-investigate)

---

## Key Verification Formulas

### CAGR Projection

**Formula:**
```
Future Value = Present Value × (1 + CAGR)^n
```

**Variables:**
- Present Value: Current/base year market size
- CAGR: Compound Annual Growth Rate (as decimal, e.g., 16.4% = 0.164)
- n: Number of years between base and target year

**Verification example:**
```
Source claims: $22.1bn (2024) at 16.4% CAGR = $55.0bn (2030)

Verify: 22.1 × (1.164)^6 = 22.1 × 2.488 = 55.0 ✓
```

**Calculating n (years):** Count years between base and target year. Examples: 2024→2030 = 6 years, 2025→2030 = 5 years.

### Valuation Multiples

**EV/Revenue:**
```
EV/Revenue Multiple = Enterprise Value ÷ Revenue
Implied EV = Revenue × Multiple
```

**EV/EBITDA:**
```
EV/EBITDA Multiple = Enterprise Value ÷ EBITDA
Implied EV = EBITDA × Multiple
```

**Verification example:**
```
Source claims: $436m deal at 9.7x revenue multiple on $45m revenue

Verify: 436 ÷ 45 = 9.69 ≈ 9.7x ✓
```

### Market Share

**Formula:**
```
Market Share = (Segment Size ÷ Total Market Size) × 100
```

**Verification example:**
```
Source claims: Online segment ($18bn) is 28% of total market ($65bn)

Verify: 18 ÷ 65 = 0.277 = 27.7% ≈ 28% ✓
```

### Growth Rate

**Year-over-Year:**
```
YoY Growth = (Current Year - Prior Year) ÷ Prior Year × 100
```

**CAGR from endpoints:**
```
CAGR = (End Value ÷ Start Value)^(1/n) - 1
```

---

## Consensus Methodology

When source data contains multiple estimates, verify consensus calculations:

### Size Consensus (Range)

**Method:** Full min-max range across all sources

**Example:**
```
Sources: $14.9bn, $18.3bn, $21.1bn, $21.2bn, $22.1bn
Consensus: $15-22bn (rounded to nearest $1bn)
```

### CAGR Consensus (Central Cluster)

**Method:** Exclude outliers (highest and lowest), use central cluster range

**Example:**
```
Sources: 10.6%, 16.4%, 17.2%, 19.0%, 22.7%
Exclude outliers: 10.6% (low), 22.7% (high)
Central cluster: 16.4%, 17.2%, 19.0%
Consensus: 16-19% or 16-17% (conservative)
```

### Projection Consensus

**Method:** Apply consensus CAGR to midpoint of size range

**Example:**
```
Size range: $15-22bn → Midpoint: $18.5bn
CAGR consensus: 16-17%
At 16%: 18.5 × (1.16)^6 = $45.1bn
At 17%: 18.5 × (1.17)^6 = $47.5bn
Consensus projection: $45-48bn
```

---

## Rounding Guidelines

These are **typical conventions** — adjust based on the magnitude of values and template style:

| Value Type | Typical Rounding | Example |
|------------|------------------|---------|
| Large market sizes ($10bn+) | Nearest $1bn | 18.47 → $18bn |
| Smaller market sizes (<$10bn) | Nearest $0.5bn or $0.1bn | 2.3 → $2.5bn |
| Size ranges | Match precision of sources | 14.9-22.1 → $15-22bn |
| CAGR | Whole % or 0.5% | 16.4% → 16% or 16.5% |
| Market share | Nearest 5% or match source | 27.7% → 25% or 30% |
| Revenue ($m) | 1 decimal | 18.47 → $18.5m |
| Multiples | 1 decimal | 9.688 → 9.7x |

**Rounding principles:**
- Rounding should not materially change the figure — for smaller values, use finer precision
- Consistency matters more than precision — use same rounding across similar figures
- When creating ranges, round down for low end, round up for high end
- For summary statistics (mean, median), match precision of input data

---

## Verification Checklist

Before using any calculated value from source data:

### Formula Verification
- [ ] Projection uses correct CAGR formula: `PV × (1 + r)^n`
- [ ] Multiples calculated as EV ÷ Metric (not reversed)
- [ ] Growth rates use correct base year in denominator
- [ ] Percentage shares sum to ~100% where applicable

### Input Verification
- [ ] Base year figures match source documents
- [ ] CAGR/growth rates match stated source methodology
- [ ] Time periods (n) calculated correctly
- [ ] Currency and units consistent ($bn vs $m)

### Output Verification
- [ ] Calculated result matches source's stated figure
- [ ] If mismatch, investigate methodology difference
- [ ] Rounding applied consistently
- [ ] Results are plausible (no order-of-magnitude errors)

### Consensus Verification
- [ ] All sources included in range calculations
- [ ] Outlier exclusion methodology documented
- [ ] Midpoint calculations use correct averaging
- [ ] Range bounds represent actual min/max or documented subset

---

## Red Flags to Investigate

**Projection mismatches:**
- Calculated projection differs from source by >5%
- Likely cause: Different base year, different CAGR, or rounding

**Multiple mismatches:**
- Calculated multiple differs from source
- Likely cause: Different metric definition (LTM vs. NTM, Revenue vs. Net Revenue)

**Consensus mismatches:**
- Your consensus differs from source's consensus
- Likely cause: Source excluded certain data points, different outlier treatment

**When in doubt:** Note the discrepancy in a footnote and show your calculation methodology.
