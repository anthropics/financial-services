# Payments and fintech sector overlay — human-review-gates

Loads when the scope `sector_overlay_set` includes `payments-fintech`. The overlay shapes the decision-authority block and the gate framing for sponsor-bank arrangements, money-services-business state-licensing, and consumer-payment-product oversight at fintechs and the banks that sponsor them.

## Why the payments-fintech overlay matters

The governance architecture in payments and fintech is shaped by two distinct regimes that often coexist: the sponsor-bank arrangement (where a bank charters or partners with a fintech to deliver bank products and the OCC, FRB, FDIC, and CFPB have specific expectations on the bank's oversight of the fintech) and the money-services-business framework (where a non-bank money transmitter is regulated state-by-state under MSB licensing, with FinCEN BSA/AML registration on top). A gate matrix at a fintech or sponsor bank must reflect both regimes when both apply.

## Source basis

- **Interagency Guidance on Third-Party Relationships: Risk Management (OCC / FRB / FDIC, June 2023)**. The base third-party-risk framework that applies to bank-fintech partnerships from the bank side. The lifecycle phases (planning, due diligence, contract, ongoing monitoring, termination) frame the sponsor-bank gate matrix.
- **OCC, FRB, FDIC Bank-Fintech Partnership Guidance**. The federal banking supervisors have published joint and individual guidance on bank-fintech partnerships. The specific guidance includes: OCC guidance on bank operations through bank service company arrangements; FRB SR letters on third-party relationships including fintech-specific addenda; FDIC bank-fintech guidance issued through FILs.
- **CFPB Supervision and Examination Manual — relevant chapters**. The CFPB asserts supervisory authority over banks and over larger participants in certain consumer-financial markets; CFPB's CMS framework and product-specific exam manual chapters frame consumer-product gates.
- **NACHA Operating Rules**. ACH originator and ODFI obligations; gate-anchoring for ACH-product launches and ongoing monitoring.
- **Reg E (12 CFR Part 1005) and Reg Z (12 CFR Part 1026)**. Consumer protections on electronic fund transfers and consumer credit; specific rules drive product-level gates (Reg E error-resolution timelines, Reg Z disclosure requirements, Reg Z ability-to-repay for credit products).
- **State money-transmitter licensing (varies by state; harmonized in many states by the Conference of State Bank Supervisors' Money Transmission Modernization Act)**. State licensing requirements include named permissible-investment requirements, surety-bond requirements, and ongoing reporting; gate-anchoring for state-licensed money transmitters.
- **FinCEN BSA/AML registration (31 CFR Chapter X, Part 1022 for MSBs)**. AML program requirements for non-bank MSBs, including designated AML compliance officer, training, independent review, and SAR/CTR filing obligations.

## What the overlay adds to the matrix

### Decision authority — sponsor-bank dual structure

For a sponsor-bank-and-fintech arrangement, the matrix often names two coordinated decision authorities:

- **Sponsor bank side**: the bank's risk committee, vendor risk committee, and (for products subject to CFPB supervision) the consumer compliance committee. The bank carries primary regulatory responsibility for the fintech's activities under the bank's charter and so the bank's gates govern the partnership.
- **Fintech side**: the fintech's own compliance and risk function, with a designated officer (CCO, BSA Officer, or both) responsible for fintech-side execution. The fintech's gates feed the bank's gates; a gate at the fintech that does not produce evidence the bank can inspect creates an oversight gap on the bank side.

The matrix names both structures and the coordination mechanism (typically a joint operating committee or a sponsor-bank oversight forum) where decisions affecting both flow through.

### MSB-only structures

For non-bank MSBs without a sponsor-bank arrangement (typical for some money transmitters and some payments processors), the matrix names: the firm's executive risk committee, the BSA Officer (FinCEN BSA program requirement), the AML compliance officer (often the same person), the designated state-licensing officer (the named individual on state licenses), and the board oversight mechanism (varies by state). The state-by-state variation lands in `firm-overlay.md`.

### Sponsor-bank gate sequence

A canonical sponsor-bank gate matrix names:
1. **Fintech onboarding gate** at the bank (interagency TPRM §III.B due-diligence gate adapted for fintech-specific risks: business-model viability, regulatory licensing, technology stack, financial condition).
2. **Contract gate** at the bank (interagency TPRM §III.C contract gate, with named bank-side approvers for risk-management terms, exit terms, and information rights).
3. **Product-launch gate** at the bank (a product-specific gate where the consumer compliance, BSA, fraud, and risk functions concur on go-live; often distinct from the broader fintech onboarding gate).
4. **Ongoing-monitoring gate** at the bank (interagency TPRM §III.D, with cadence aligned to the criticality of the fintech relationship; typically quarterly to annual depending on criticality).
5. **Issue-rating gate** when fintech-originated issues land at the bank (the bank's issue-rating committee gate fires on fintech-monitoring exceptions).
6. **Termination gate** at the bank (interagency TPRM §III.E, with named bank-side approvers and exit-plan attestation).

The fintech side mirrors several of these with internal coordination (product-launch concurrence, monitoring evidence production, exit-plan execution).

### Consumer-product gates

Gates touching consumer products carry the conduct cross-cutting overlay automatically (load `references/cross-cutting/conduct.md`). The matrix references specific rule-anchored gates:
- Reg E error-resolution-timeline gate (10-business-day provisional-credit decision, 45-day final resolution; specific rule-anchored stop conditions and documentation).
- Reg Z disclosure-review gate (annual percentage rate accuracy, TILA-required disclosures, ability-to-repay decisions for covered loans).
- CFPB UDAAP risk-review gate for product changes (fee-change approval, marketing-change approval, terms-and-conditions changes affecting consumers).
- Restitution-decision gate where a consumer-impact issue surfaces.

### MSB-specific BSA gates

For MSB-licensed entities, the matrix names BSA-specific gates: the SAR-filing decision gate (BSA Officer attestation; FinCEN's 30-day filing window from initial detection of facts that may constitute a basis for filing, with up to 30 additional days for identifying a suspect); the CTR-filing operational gate; the OFAC-screening match-review gate; the periodic AML risk-assessment refresh gate; the AML independent review gate (annual or biennial, depending on size and complexity, performed by an independent reviewer per FinCEN expectations).

## Common patterns

- **Bank-side oversight gap on fintech-side execution**. The bank's gates exist; the fintech's gates exist; but the evidence pipeline that lets the bank inspect the fintech's execution does not. The matrix's gap section flags this as a critical oversight gap; the recommended action names a specific evidence-pipeline (typically a monthly or quarterly fintech-monitoring pack with named reviewers on both sides).
- **Product-launch gate compressed into the fintech onboarding gate**. Banks sometimes treat the fintech's products as part of the fintech's onboarding rather than as separate product-launch gates. This compresses the consumer-compliance and BSA review into the onboarding diligence; the matrix flags this and recommends separating product-launch gates per product.
- **MSB BSA program treated as a single gate**. The BSA program for an MSB is a set of distinct gates (SAR filing, CTR filing, OFAC review, training cadence, independent review); some firms run a single "BSA review" gate that compresses these into one decision. The matrix surfaces the under-specified gate and recommends a gate per BSA program element.
- **State-licensing renewal gate buried in operations**. State money-transmitter renewal is annual or biennial in most states with named documentation requirements. Firms sometimes run renewal as an operational task without committee oversight; the matrix elevates the renewal as a named gate with the licensing officer as the named attester.

## Implications for gate construction

- Decision authority for payments-fintech matrices typically names: the bank's risk committee (sponsor-bank case), the bank's consumer compliance committee (consumer-product case), the bank's vendor risk committee (TPRM case), the fintech's executive risk committee, the BSA Officer (designated under FinCEN regs for any BSA-covered entity), the named state-licensing officer (per state), and the board oversight body (varies by state and by structure).
- Independence on payments-fintech gates is grounded in: the interagency TPRM line-1 / line-2 separation (sponsor-bank case); the FinCEN-required AML independent review (MSB case); CFPB CMS framework's compliance-audit independence (consumer-product case).
- Documentation requirement names the system of record at the bank (GRC platform), the fintech-side system, the regulator-submission cadence (Form FFIEC reporting if applicable, Reg E/Reg Z compliance records, BSA filing records, state regulator filings), and the cross-firm coordination record (typically a shared committee minutes archive accessible to both bank and fintech).
- The gap section explicitly checks for: missing fintech-side evidence pipeline to bank-side gates; product-launch gates compressed into onboarding; BSA program treated as a single gate; state-licensing renewal not gated at committee level; consumer-product change gates without conduct-overlay alignment.

## Anchors used by this overlay

- Interagency Guidance on Third-Party Relationships: Risk Management (June 2023). https://www.federalreserve.gov/supervisionreg/srletters/SR2304.htm
- OCC, FRB, FDIC bank-fintech partnership guidance — varies by agency and date; firm-overlay names the specific bulletins, FILs, and SR letters in scope.
- CFPB Supervision and Examination Manual. https://www.consumerfinance.gov/compliance/supervision-examinations/
- NACHA Operating Rules (annual). https://www.nacha.org/rules
- 12 CFR Part 1005 — Reg E. https://www.ecfr.gov/current/title-12/chapter-X/part-1005
- 12 CFR Part 1026 — Reg Z. https://www.ecfr.gov/current/title-12/chapter-X/part-1026
- 31 CFR Part 1022 — FinCEN MSB rules including SAR and CTR filing, AML program requirements. https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1022
- CSBS Money Transmission Modernization Act and state money-transmitter licensing — varies by state. https://www.csbs.org/
