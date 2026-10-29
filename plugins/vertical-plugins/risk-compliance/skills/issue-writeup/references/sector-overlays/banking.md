# Banking sector overlay — issue-writeup

Loads when the scope `sector_overlay_set` includes `banking`. The overlay shapes the criteria block, the severity calibration, the MRA / MRIA / MRBA classification field, and the closure-evidence framing for issues at federally regulated US banks (national, state-member, state-non-member, savings, holding companies, and US IHCs of foreign banking organizations).

## Why the banking overlay matters

The federal banking supervisors (FRB, OCC, FDIC) have published, distinct frameworks for how findings are written, classified, and tracked. An issue write-up at a regulated bank that does not conform to the named framework is harder to defend in continuous monitoring and at the next examination cycle. The overlay is the contract between the CCCE artifact and the examiner's expected response register.

## Source basis

- **Federal Reserve SR 13-13 / CA 13-10** — Supervisory Considerations for the Communication of Supervisory Findings. MRA and MRIA framework, the firm-side expectation that issues are tracked through closure with documented remediation evidence.
- **OCC Bulletin 2014-39** — Matters Requiring Attention. Defines MRA criteria, the OCC's expectation that MRAs name a corrective action and target date, and the convention that MRA closure is evidenced for OCC inspection.
- **FDIC Risk Management Manual of Examination Policies and FDIC Compliance Examination Manual** — MRBA framing (Matters Requiring Board Attention) as the FDIC parallel to OCC and FRB MRAs; addressed to the board rather than to management alone.
- **12 CFR Part 30, Appendix D — OCC Heightened Standards for Large Insured National Banks** — Standards on risk governance framework, three lines of defense, and front-line-unit responsibilities. Severity calibration shifts when the issue concerns a Heightened-Standards-covered bank.
- **Reg YY (12 CFR Part 252)** — Enhanced prudential standards for large bank holding companies; risk management and risk committee requirements that frame governance findings.
- **FFIEC Uniform Rating System (CAMELS for banks; ROCA for FBOs)** — composite-rating implications for severity calibration; findings that move a CAMELS component carry higher severity rationale weight.

## What the overlay adds to the write-up

### MRA / MRIA / MRBA classification

When the source type is examiner-letter and the regulator is FRB, OCC, or FDIC, the `mra_mria_classification` field is populated:

- **MRIA** (FRB only) — Matter Requiring Immediate Attention. The most severe category; reserved for matters that have caused or threaten to cause significant harm or that are violations of law. Severity rating is typically critical or high; closure evidence is detailed; target date is short.
- **MRA** (FRB and OCC) — Matter Requiring Attention. Significant deficiency that requires correction. Severity is typically high or moderate; closure evidence is named; target date is set with the regulator's expected response register in mind.
- **MRBA** (FDIC) — Matter Requiring Board Attention. Addressed to the board rather than to management alone; severity is typically high; closure evidence emphasises board-level oversight artifacts (board minutes, board-approved remediation plan).

Issues sourced from a state-member bank's FRB letter and a state non-member bank's FDIC letter use different fields even though the underlying condition may be the same; the overlay ensures the artifact carries the regulator-correct framing.

### Severity calibration

Banking severity calibration leans on three axes the federal supervisors weigh: (1) impact on the bank's safety and soundness, (2) impact on consumers and the public, (3) violation-of-law dimension. Findings that touch CAMELS components (Capital, Asset quality, Management, Earnings, Liquidity, Sensitivity to market risk) carry severity-rationale weight tied to the specific component. A finding that would move the M (Management) rating is high or critical even if the operational impact is modest, because the rating consequence is itself the impact.

### Closure-evidence framing

The federal supervisors expect closure evidence to be inspectable at the next continuous-monitoring touchpoint or at the next examination cycle. The closure-evidence field for banking-overlay issues names:
- The artifact (board minutes, committee minutes, system-of-record output, sign-off log).
- The retention location (GRC platform, board-portal, document management system).
- The retention period (banking exam files typically run a five-year rolling retention; firm-overlay specifies the firm's actual cadence).

### Heightened Standards severity flavour

For OCC-Heightened-Standards-covered banks (12 CFR Part 30 Appendix D applicable, currently $50B+ at the OCC's discretion subject to the rule's threshold framework), findings on the risk-governance framework, three-lines-of-defense architecture, or independent risk management carry additional severity weight. The severity rationale references the specific Heightened Standard that the condition impairs.

### Reg YY governance findings

For BHCs covered by Reg YY enhanced prudential standards (currently $100B+), findings on the risk committee, the CRO independence, or the risk-appetite framework carry additional severity weight. The criteria block references the specific Reg YY section.

## Common patterns

- **Repeat MRA**. An MRA that has been issued twice on the same root cause moves to MRIA in the next exam cycle. The issue's severity rationale should reference any prior MRA on the same matter; the firm's GRC platform's MRA-history field is the source.
- **MRA closure with residual issues**. Closing an MRA with the regulator does not close the issue at the firm; the firm carries a residual issue at lower severity for the remediation tail. The issue write-up reflects the regulator-side closure and the firm-side residual separately.
- **Pre-emptive self-disclosure**. A bank that surfaces a deficiency to the FRB, OCC, or FDIC before the regulator finds it typically gets credit on severity calibration. The source type is `self-identified` rather than `examiner-letter`, but the regulator-engagement record is referenced in the source block.

## Implications for the CCCE

- **Criteria** for banking-overlay issues cite the regulator's published framework first (FRB SR letter, OCC bulletin, FDIC manual section), then the firm's policy second. The order matters; reviewers expect the regulatory criterion to lead.
- **Cause** for governance findings ties to the specific lines-of-defense element that failed (CRO independence, board risk committee oversight, first-line-unit risk responsibility). For Heightened-Standards-covered banks, the cause references the specific Standard.
- **Effect** for banking issues quantifies safety-and-soundness implications where possible (capital impact, liquidity impact, asset-quality impact, earnings impact) and consumer/public-impact distinctly.
- **Closure evidence** for examiner-issued findings includes the artifacts the regulator named in the supervisory letter as the expected response, which usually exceed the firm's standard closure pattern.

## Anchors used by this overlay

- FRB SR 13-13 / CA 13-10 — Supervisory Considerations for the Communication of Supervisory Findings. https://www.federalreserve.gov/supervisionreg/srletters/sr1313.htm
- OCC Bulletin 2014-39 — Matters Requiring Attention. https://www.occ.gov/news-issuances/bulletins/2014/bulletin-2014-39.html
- 12 CFR Part 30, Appendix D — OCC Heightened Standards (Standards I–V). https://www.ecfr.gov/current/title-12/chapter-I/part-30/appendix-Appendix%20D%20to%20Part%2030
- 12 CFR Part 252 (Reg YY) — Enhanced prudential standards for large BHCs. [verify current section labels for risk committee and risk-management requirements.]
- FDIC Risk Management Manual of Examination Policies. https://www.fdic.gov/regulations/safety/manual/
- FDIC Compliance Examination Manual. https://www.fdic.gov/resources/supervision-and-examinations/consumer-compliance-examination-manual/
- FFIEC Uniform Rating System (CAMELS / ROCA). [verify current edition references.]
