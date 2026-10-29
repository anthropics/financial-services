# Payments and fintech sector overlay — issue-writeup

Loads when the scope `sector_overlay_set` includes `payments-fintech`. The overlay shapes the criteria block, the severity calibration, and the closure-evidence framing for issues at money transmitters, payments processors, sponsor-bank programs, fintech bank partners, and non-bank consumer-finance providers.

## Why the payments-fintech overlay matters

Payments and fintech sit across multiple regulator constellations: the CFPB on consumer-protection, FinCEN on BSA / AML, OCC / FRB / FDIC on bank-partnership oversight, state regulators on money transmitter licensing, and (for some firms) the Federal Trade Commission on UDAAP through the Gramm-Leach-Bliley Safeguards Rule. Findings come in via CFPB supervisory recommendations, OCC fintech bank-partnership supervisory letters, state money-transmitter examination findings, and FinCEN examination findings (often delivered through the IRS or the federal banking agencies on behalf of FinCEN). The criteria block, severity calibration, and closure-evidence framing differ from the federal banking convention, the state-DOI insurance convention, and the SEC / FINRA capital-markets convention.

## Source basis

- **CFPB Supervisory Highlights and supervisory recommendations** — published priorities and observed-deficiency categories. Severity calibration tracks whether a recommendation moves toward an enforcement matter.
- **CFPB Examination Manual** — module-by-module examination procedures; criteria citations frequently come from the Compliance Management Review module, the UDAAP module, the Fair Lending module, and the product-specific modules (mortgage origination, deposit-and-card products, debt collection, etc.).
- **OCC Fintech Bank-Partnership Supervisory Letters** — the OCC's published guidance on bank partnerships with non-bank fintech companies, including expectations on the bank's third-party risk management for the fintech relationship and the bank's responsibility for consumer-protection compliance through the partnership.
- **OCC Bulletin 2020-10 and 2024 fintech-related guidance** — bank-partnership supervisory framework. [verify current bulletin numbering for fintech-specific guidance; the OCC has updated its fintech framework multiple times.]
- **State money-transmitter examination conventions** — varies by state; the Conference of State Bank Supervisors (CSBS) coordinates the State Examination System (SES) for multi-state exams, but each state's examination report carries state-specific format.
- **FinCEN examination findings via the IRS or the federal banking agencies** — BSA / AML examination findings on money services businesses follow the FFIEC BSA / AML Examination Manual conventions when delivered through the federal banking agencies; FinCEN-direct enforcement actions follow the FinCEN consent order convention.
- **Reg E (12 CFR Part 1005)** — Electronic Fund Transfers; consumer-protection rules on prepaid accounts, P2P, ACH, and similar electronic transfers. Severity calibration ties to the unauthorized-transfer-resolution timing, error-resolution timing, and disclosure rules.
- **Reg Z (12 CFR Part 1026)** — Truth in Lending; consumer-protection rules on closed-end credit, open-end credit, credit cards, and HELOCs.
- **NACHA Operating Rules** — for ACH-active firms, NACHA findings on origination, returns, and risk-management.

## What the overlay adds to the write-up

### CFPB supervisory recommendation format

When the source type is examiner-letter and the regulator is CFPB, the criteria block follows the CFPB's supervisory recommendation format. CFPB findings typically structure as:
- A **Matter Requiring Attention (MRA)** — the CFPB uses the MRA label even though it is not a federal-banking MRA. CFPB MRAs name a corrective action and an expected completion date. The `mra_mria_classification` field is set to `MRA` and the regulator is recorded as CFPB.
- A **public enforcement action** — the artifact is the consent order; the issue write-up references the consent order but the public consent-order language often becomes the criteria citation in any related issue write-ups.

Severity calibration for CFPB MRAs is typically high because the CFPB's MRA is roughly comparable to a federal-banking MRA in seriousness, but the consumer-impact dimension is foregrounded.

### OCC fintech bank-partnership findings

When the source is an OCC supervisory letter on a fintech bank-partnership relationship, the finding is typically directed at the bank but carries operational implications for the fintech partner. The issue write-up at the bank cites the OCC bulletin and the interagency third-party guidance; the issue write-up at the fintech partner cites the bank's contractual remediation requirement and the underlying consumer-protection rule.

### State money-transmitter examination findings

For multi-state money transmitters, the same finding may surface via state-by-state examinations or via a coordinated CSBS-SES exam. The criteria block names the state-specific statute first (most states map to the Money Transmitter Modernization Act framework but with state-specific variations), then the firm's policy second. Severity calibration tracks state-specific consumer-protection severity ladders.

### FinCEN BSA / AML findings

When the source is a BSA / AML examination finding (delivered through the IRS for non-bank money services businesses or through the federal banking agencies for bank-partnered fintechs), the criteria block cites the Bank Secrecy Act, the relevant FinCEN regulation (31 CFR Chapter X), and the FFIEC BSA / AML Examination Manual section. Severity calibration for BSA / AML findings is typically high or critical because of the AML statutory framework's severity ladder; the consumer-impact dimension is replaced by the financial-crime-exposure dimension.

### Severity calibration

Payments-fintech severity calibration weighs (1) consumer-protection impact (UDAAP, Reg E, Reg Z, fair-lending), (2) AML / sanctions / financial-crime impact, (3) bank-partnership reputational impact for sponsor-bank programs, (4) state-licensing impact for multi-state operations, and (5) operational-resilience impact for payment processors. UDAAP findings with identifiable consumer harm carry critical or high severity; UDAAP findings without identified harm carry moderate or high severity.

### Closure-evidence framing

Closure evidence for CFPB MRAs names the corrective action plan, the implementation evidence (consumer-disclosure update, system change, policy update, training delivered, restitution paid where applicable), and the CFPB's expected continuous-monitoring touchpoint. For OCC fintech bank-partnership findings, closure evidence references both the bank-side remediation and the fintech-side remediation that satisfies the bank's contract. For state money-transmitter findings, closure evidence references state-specific remediation language.

## Common patterns

- **Multi-state replication**. A consumer-protection finding identified in one state often replicates across other states the firm is licensed in; the issue write-up names the state of identification and flags the multi-state replication scope.
- **UDAAP findings with restitution**. Restitution-eligible UDAAP findings carry customer-count and dollar-restitution closure evidence specifically; the closure-evidence field names the restitution program, the consumer-notification process, and the third-party restitution-administrator (where used).
- **Bank-partnership pass-through**. Consumer-protection findings at a fintech bank-partner often surface as an MRA at the sponsor bank rather than as a direct supervisory action against the fintech; the bank's MRA cascades into the fintech's contractual remediation. The fintech-side issue write-up references the sponsor bank's MRA and the contractual cascade.
- **Sanctions and OFAC findings**. OFAC findings on screening, blocking, or reporting violations carry critical severity; the criteria block cites 31 CFR Chapter V (OFAC regulations) and the OFAC FAQ guidance. Closure evidence names the corrective screening program, the look-back lookback file, and the OFAC submission where applicable.

## Implications for the CCCE

- **Criteria** for payments-fintech-overlay issues cite the federal consumer-protection rule first (Reg E, Reg Z, UDAAP, BSA / AML), then state-licensing or NACHA rule second, then firm policy third.
- **Cause** for consumer-protection findings ties to the specific operational control that failed (disclosure-generation control, error-resolution-timeliness control, credit-decision control, dispute-resolution-tracking control). For BSA / AML findings, cause maps to the specific AML control attribute (KYC / CIP control, transaction-monitoring control, SAR-filing-timeliness control, OFAC screening control).
- **Effect** for payments-fintech issues quantifies consumer-protection impact (consumer-count, dollar-restitution-scope, UDAAP exposure), AML / sanctions impact (transaction-volume, dollar-volume, geographic-exposure), and state-licensing implication distinctly.
- **Closure evidence** for CFPB MRAs and OCC fintech bank-partnership findings includes the corrective-action-plan response, the consumer-impact remediation (where applicable), and the readiness for the regulator's continuous-monitoring touchpoint.

## Anchors used by this overlay

- CFPB Supervisory Highlights. https://www.consumerfinance.gov/compliance/supervisory-highlights/
- CFPB Examination Manual. https://www.consumerfinance.gov/compliance/supervision-examinations/
- 12 CFR Part 1005 (Reg E — Electronic Fund Transfers). https://www.ecfr.gov/current/title-12/chapter-X/part-1005
- 12 CFR Part 1026 (Reg Z — Truth in Lending). https://www.ecfr.gov/current/title-12/chapter-X/part-1026
- OCC Bulletin 2020-10 — Third-Party Relationships: Frequently Asked Questions for fintech bank-partnership context. [verify currency; the OCC has issued FAQ updates and 2024 fintech guidance.]
- 31 CFR Chapter X — FinCEN regulations (BSA / AML for money services businesses). https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X
- 31 CFR Chapter V — OFAC regulations. https://www.ecfr.gov/current/title-31/subtitle-B/chapter-V
- FFIEC BSA / AML Examination Manual. https://bsaaml.ffiec.gov/manual
- NACHA Operating Rules and Guidelines. https://www.nacha.org/rules
- State-specific money transmitter licensing acts; CSBS State Examination System. https://www.csbs.org/state-examination-system
- Money Transmitter Modernization Act framework — model legislation adopted (with variations) by participating states. [verify state-by-state adoption status.]
