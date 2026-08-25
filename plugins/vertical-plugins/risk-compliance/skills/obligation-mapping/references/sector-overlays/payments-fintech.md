# Payments and fintech sector overlay: obligation-mapping

Loaded when the scope includes `payments-fintech` in `sector_overlay_set`. Adds payments- and fintech-specific source labels and obligation patterns the practitioner expects to find when the register scopes a consumer-payments product, a money-transmission process, a bank-fintech sponsor arrangement, or a BaaS program. Does not change the row spine.

The register here often runs across two parties: a sponsor bank with the regulatory obligation and a fintech with the operational obligation under contract. The register treats those as separate rows, anchored on the rule for the bank side and on the sponsor agreement for the fintech side.

## Sources the register may cite

### Consumer-payments rules

- Regulation E — 12 CFR Part 1005 (Electronic Fund Transfers Act implementation).
  - §1005.6 (consumer liability for unauthorized transfers).
  - §1005.7 (initial disclosures).
  - §1005.8 (change-in-terms notices).
  - §1005.9 (receipts and periodic statements).
  - §1005.11 (procedures for resolving errors); §1005.11(c) (10-day provisional credit window).
  - §1005.18 (prepaid accounts).
  - Use for: EFT obligations on the bank holding the deposit; allocate operational components to the fintech via the sponsor agreement.
  - Link: https://www.ecfr.gov/current/title-12/chapter-X/part-1005

- Regulation Z — 12 CFR Part 1026 (Truth in Lending Act implementation).
  - §1026.6 (account opening disclosures for open-end credit).
  - §1026.7 (periodic statements for open-end credit).
  - §1026.13 (billing-error resolution).
  - §1026.40 (HELOCs); subpart G (credit cards).
  - Use for: TILA obligations on credit products, including BNPL where structured as open-end or closed-end credit under the rule. The CFPB BNPL interpretive rule (May 2024) was **nullified by Pub. L. 119-11 (May 9, 2025); historical only**; Reg Z applicability to BNPL is now an open question on the regulatory text.
  - Link: https://www.ecfr.gov/current/title-12/chapter-X/part-1026

- Regulation DD — 12 CFR Part 1030 (Truth in Savings Act implementation).
  - §1030.4 (account disclosures).
  - §1030.5 (subsequent disclosures).
  - Use for: deposit-account disclosure obligations on consumer-deposit products.

### Bank-fintech and BaaS expectations

- Interagency Guidance on Third-Party Relationships: Risk Management (OCC / FRB / FDIC, June 6, 2023). §III.A through §III.E lifecycle phases.
  - Use for: TPRM obligations on the bank when the bank is the sponsor; the fintech-side allocation flows through the sponsor agreement.
  - Link: https://www.federalreserve.gov/supervisionreg/srletters/SR2304.htm

- Joint Statement on Bank-Fintech Arrangements (FDIC / OCC / FRB, July 2024) and the related interagency RFI on bank-fintech arrangements. [verify exact title and citation; the joint statement names risk areas including end-user ledgering and FBO-account controls.]
  - Use for: BaaS-specific obligation rows that overlap with TPRM but go beyond standard third-party expectations: end-user ledgering integrity, FBO account governance, BaaS-program criticality classification.
  - Link: https://www.fdic.gov/news/financial-institution-letters/

### Open banking

- CFPB Section 1033 (Personal Financial Data Rights) Final Rule, 12 CFR 1033 [verify subpart and section numbers against the published Final Rule]. **§1033 compliance dates stayed as of October 29, 2025; CFPB-initiated reconsideration with ANPR** — verify current docket status before treating phased compliance dates as firm.
  - Use for: data-provider obligations to make covered data available to consumer-authorized third parties; cross-load with privacy overlay.
  - Link: https://www.consumerfinance.gov/rules-policy/final-rules/

### Money transmission

- State money-transmitter licenses and the NMLS-coordinated obligations under each state's money-transmitter act.
  - Use for: money-transmitter obligations when the fintech operates without a sponsor bank or operates licensed activities directly. The register names the licensing states explicitly.

- Bank Secrecy Act money-services-business obligations (31 CFR Part 1022). §1022.210 (AML program), §1022.310 (CTRs), §1022.320 (SARs), §1022.380 (registration as MSB).
  - Use for: MSB-side BSA obligations.
  - Link: https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1022

### Card-network and payment-rail obligations

- Card-network rules (Visa, Mastercard, Discover, Amex). Operating regulations and chargeback rules. Not regulator-issued, but contractually binding and treated as a contractual source row in the register.
- NACHA Operating Rules (ACH). Contractually binding on participating financial institutions.
- The Clearing House Real-Time Payments rules; FedNow operating circular (FRB Operating Circular 8 [verify circular number and current edition]).

## Obligation patterns the practitioner expects to find

- **Bank-side and fintech-side row pair-up.** Reg E error-resolution obligations land on the bank as the financial institution; the sponsor agreement allocates the operational handoff to the fintech (intake, investigation, communication). Both rows extract.
- **The 10-day provisional-credit obligation under §1005.11(c).** Empirically grounded number; the register names it explicitly when consumer-payment processes are in scope.
- **BaaS criticality classification rows.** When the bank's TPRM treats the BaaS program as a critical third-party relationship, expected obligation rows include continuous monitoring, exit planning, and regulator-notification obligations specific to the BaaS arrangement.
- **End-user ledgering and FBO account integrity.** The 2024 joint statement and subsequent supervisory commentary treat these as distinct obligation areas; the register surfaces them rather than collapsing into "vendor oversight."
- **State money-transmitter license obligations.** Each licensing state imposes net-worth, surety-bond, and reporting obligations; the register lists these as distinct rows or groups them with explicit state-by-state notes in `applicability_notes`.

## What does not belong here

- Capital-markets-side obligations on a fintech that operates a registered broker-dealer or investment adviser. Run with `capital-markets` overlay; the payments-fintech overlay covers the consumer-payments side.
- Bank-side obligations that do not interact with the fintech relationship (general capital, deposit insurance assessments, CRA). Run with `banking` overlay.
- Internal firm policy and taxonomy. That goes in `references/firm-overlay.md`.
