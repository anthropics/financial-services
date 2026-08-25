# Cross-cutting overlay: conduct — obligation-mapping

Loaded when the scope includes `conduct` in `cross_cutting_overlay_set`, or when the source being mapped is conduct-anchored. Adds conduct-specific source labels and obligation patterns when the register scopes consumer-facing decisions, marketing, complaints, or fair-treatment processes. Does not change the row spine.

Conduct sits where consumer compliance, fair-lending, market-conduct, and product-governance overlap. The register often loads conduct alongside privacy when the process touches consumer decisioning, alongside `payments-fintech` when the product is a consumer payment, and alongside `insurance` when the engagement covers insurance market-conduct.

## Sources the register may cite

### CFPB and federal consumer-finance conduct

- Dodd-Frank Act §§1031, 1036 (UDAAP); CFPB UDAAP Examination Procedures (current edition of the CFPB Supervision and Examination Manual UDAAP module).
  - Use for: unfair, deceptive, abusive acts and practices obligations across consumer-financial-product processes; the register cites the manual section and the underlying statutory authority.
  - Link: https://www.consumerfinance.gov/compliance/supervision-examinations/

- Equal Credit Opportunity Act (ECOA), 15 U.S.C. §1691 et seq.; Reg B, 12 CFR Part 1002.
  - §1002.4 (general rules), §1002.5 (information about applicants), §1002.7 (rules concerning extensions of credit), §1002.9 (notifications), §1002.13 (information for monitoring purposes), §1002.14 (rules on appraisals).
  - Use for: fair-lending obligations including adverse-action notification, monitoring-information collection, and §1002.7 spousal-signature rules.
  - Link: https://www.ecfr.gov/current/title-12/chapter-X/part-1002

- Fair Housing Act, 42 U.S.C. §3601 et seq. and HUD's implementing regulations (24 CFR Part 100).
  - Use for: housing-related fair-lending obligations on dwelling-secured credit.

- Home Mortgage Disclosure Act; Reg C, 12 CFR Part 1003.
  - Use for: HMDA reporting obligations on covered institutions; the register cites the §1003.x reporting and recordkeeping sections.

- CFPB Section 1071, 12 CFR 1002.107 et seq.
  - Use for: small-business-lending data collection conduct obligations; pair with the §1002.108 firewall conduct row.

- Servicemembers Civil Relief Act and Military Lending Act (32 CFR Part 232).
  - Use for: military-borrower conduct obligations.

- Real Estate Settlement Procedures Act (RESPA), 12 CFR Part 1024.
  - §1024.7 (Loan Estimate via §1026.19(e)), §1024.17 (escrow accounts), §1024.30 et seq. (servicing).
  - Use for: mortgage-settlement and servicing conduct obligations.

- Fair Debt Collection Practices Act, 15 U.S.C. §1692 et seq.; Reg F, 12 CFR Part 1006.
  - Use for: third-party debt-collection conduct obligations.

### Capital-markets conduct

- Reg BI (Best Interest), 17 CFR §240.15l-1.
  - Care, conflict-of-interest, disclosure, and compliance obligations on broker-dealers serving retail customers.
  - Use for: retail-investor conduct obligations.

- IAA fiduciary duty (interpretation in IAA SEC Release 5248).
  - Use for: investment-adviser fiduciary conduct obligations on retail clients.

- FINRA Rule 2010 (standards of commercial honor) and FINRA Rule 2111 (suitability).
  - Use for: FINRA-imposed conduct obligations.

### Insurance conduct

- NAIC Suitability in Annuity Transactions Model Regulation (Model #275) and state best-interest adoptions (NY Reg 187, Iowa best-interest amendments, others).
  - Use for: annuity sales conduct obligations.
  - Link: https://content.naic.org/

- NAIC Unfair Trade Practices Act (Model #880) and state adoptions.
  - Use for: insurance unfair-trade-practice obligations.

### Complaint handling as conduct

- CFPB Complaint Handling expectations within the CMS framework.
  - Use for: complaint-intake, response, root-cause, and reporting obligations on CFPB-supervised firms.

- Functional-regulator complaint-handling expectations (OCC, FDIC, FRB consumer-affairs procedures).
  - Use for: bank-supervised complaint-handling obligations.

## Obligation patterns the practitioner expects to find

- **UDAAP obligations as design and conduct rows.** UDAAP risk attaches to product features and to operational practices; the register surfaces both kinds of rows (a fee-disclosure UDAAP row is a design row; an unauthorized-charge handling UDAAP row is a conduct row).
- **Adverse-action obligations across credit and insurance.** ECOA §1002.9 adverse action, FCRA §615 adverse-action notice, and state insurance adverse-underwriting notification obligations each impose distinct content and timing.
- **Suitability and best-interest rows.** Reg BI care obligation, IAA fiduciary duty, FINRA 2111 suitability, NAIC best-interest annuity rules. The register surfaces them as separate rows even when the same retail customer interaction triggers more than one.
- **Disclosure-timing rows.** RESPA Loan Estimate timing, TILA §1026.19 timing, ECOA §1002.9(a)(1) adverse-action 30-day window, Reg E §1005.7 prior-to-first-EFT timing. Each is a distinct row.
- **Complaint-handling rows.** Intake within X days, root-cause analysis, response to consumer, regulator-reporting where required (CFPB consumer-complaint database for CFPB-supervised firms, NYDFS Reg 218 [verify] for NYDFS insurance).
- **Servicing and collection conduct rows.** RESPA Subpart C servicing obligations, Reg F debt-collection limits, Mortgage Servicing Rules call requirements.

## What does not belong here

- Information-security obligations. Those go to the cyber overlay.
- Privacy notices and data-subject rights. Those go to the privacy overlay (notice content overlaps with conduct disclosure obligations; surface both rows with cross-references rather than collapsing).
- Internal firm policy and taxonomy. That goes in `references/firm-overlay.md`.
