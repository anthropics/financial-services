# Payments and fintech sector overlay — control-matrix

Loads when the scope `sector_overlay_set` includes `payments-fintech`. Binds matrix construction to bank-partnership, money-transmitter, and payment-network supervisory expectations.

## Supervisory frame

The supervisory map for fintechs splits by structure:

- **Direct-chartered fintech bank** — supervised under the bank overlay (use `banking.md` instead of or in addition to this file). The matrix is read by the bank's primary federal regulator and any state.
- **Sponsor-bank-partnership fintech** — examined indirectly through the sponsor bank under the interagency third-party guidance (June 2023). The matrix may need to evidence the partner-bank-side controls and the fintech-side controls; the scope names which side the matrix represents. The OCC's bank-partnership posture has tightened since 2023 and matrix rows for sponsor-bank oversight controls are increasingly examiner-probed.
- **Non-bank fintech with state money-transmitter licenses** — examined state-by-state under the NMLS framework. The matrix is read by state DFS examiners; common-state coordination via the NMLS State Coordinating Committee for multistate exams.
- **Card-network participant** — additional rule-set from network operating rules (Visa, Mastercard, Discover, Amex), PCI DSS, and (for MSBs) FinCEN.
- **CFPB larger-participant** — larger-participant rules under Dodd-Frank §1024 extend CFPB direct examination to fintechs above the size threshold for the relevant market (general-purpose consumer reporting, consumer-debt collection, student-loan servicing, international money transfer, automobile financing, larger-participant general-use prepaid card).

## Sponsor-bank-relationship controls

Where the matrix scopes a sponsor-bank-partnership process, the rows split between bank-side oversight controls and fintech-side operating controls:

Bank-side oversight controls (bank's TPRM matrix on this fintech):
- Criticality-determination control.
- Initial and ongoing due-diligence controls.
- Contract-clause controls (right to audit, examiner access via 12 USC §1867(c), data ownership, exit, BSA cooperation).
- Ongoing-monitoring controls (KRI review, complaint review, BSA-program oversight, periodic on-site or virtual reviews).
- Termination and exit-plan controls.

Fintech-side operating controls (fintech's own matrix):
- BSA program controls (where MSB-registered): four pillars, transaction monitoring, SAR filing, CTR.
- Reg E error-resolution controls (12 CFR §1005.11): timing (10 days for provisional credit, 45 or 90 days for resolution), notice content, recordkeeping (two-year retention).
- Reg Z disclosure controls for credit products (12 CFR §1026): TILA disclosures, periodic-statement controls, billing-error resolution.
- UDAAP controls: marketing-claim review, complaint-trigger response, fee-disclosure controls.
- Complaint-handling controls: intake, categorisation, response, root-cause review.
- PCI DSS attestation controls (where card data is handled): annual SAQ or ROC, QSA findings remediation, scope-creep monitoring.

## Money-transmitter-license controls

When the matrix scopes a state money-transmitter-licensed activity, the row set covers:

- Licensing maintenance controls: NMLS filings, state-specific reporting, surety-bond maintenance.
- Permissible-investment controls: state-specific permissible-investments rules, the matching to outstanding obligations, and the periodic attestation.
- Customer-fund safeguarding controls: segregation of customer funds, daily-reconciliation controls.
- BSA controls per the FinCEN MSB rules (31 CFR §1022 series).
- State-specific reporting controls (e.g., CDFI reporting, CRA-equivalent reporting for state-chartered MSBs in adopting states).

The Conference of State Bank Supervisors' Money Services Businesses Model Money Transmission Modernization Act (MTMA) is gradually adopted; check the binding-state version.

## Network and PCI controls

Card-network participants carry network-rule controls separate from regulator controls. The matrix may include rows for:

- Chargeback and dispute controls (network-specific timing and documentation rules).
- Tokenisation and authorisation controls (network-specific vault and token-service-provider relationships).
- PCI DSS v4.0 controls — the matrix references the firm's SAQ or ROC and the QSA's findings; the granular PCI control set typically lives in the firm's PCI-program documentation rather than the regulator-facing matrix.

## CFPB direct supervision

For larger-participant fintechs and for fintechs the CFPB has elected to supervise under §1024(a)(1)(C) (risk-based supervision), the matrix is read against the CFPB Supervision and Examination Manual chapters that apply. CMS pillars (board and management oversight, compliance program, complaint response, compliance audit) anchor the matrix; product-specific chapters drive substantive control rows.

## Recordkeeping and retention

- 31 CFR §1010.430 — FinCEN general recordkeeping (five-year floor for BSA records).
- 31 CFR §1022 series — MSB-specific FinCEN rules.
- 12 CFR §1005 — Reg E (two-year retention for error-resolution records).
- 12 CFR §1026 — Reg Z (two-year retention for credit-disclosure evidence).
- PCI DSS v4.0 — log retention typically one year online with three months immediately available; varies by control.
- State-specific retention varies; common pattern is the longer of three years or state-specific window.

## Sign-off and review-gate norms

Sponsor-bank matrices for fintech-partnership oversight are signed by the bank's BSA officer or chief compliance officer. Fintech-side matrices are signed by the fintech's BSA officer (where MSB-registered), CCO, or both depending on scope. Network-rule matrices are signed by the head of payments operations.

For BaaS arrangements specifically, the matrix may need to evidence both sides; the scope record names which side this matrix represents.

## Anchors used by this overlay

- Interagency Guidance on Third-Party Relationships: Risk Management (OCC/FRB/FDIC, June 2023).
- 31 CFR §1010.430 — FinCEN general recordkeeping.
- 31 CFR §1022 series — MSB-specific FinCEN rules.
- 31 CFR §1010.230 — FinCEN Customer Due Diligence Rule.
- 12 CFR §1005 — Reg E (Electronic Fund Transfers Act implementation).
- 12 CFR §1026 — Reg Z (Truth in Lending Act implementation).
- Dodd-Frank Act §1024 — CFPB supervisory authority over larger participants.
- 12 USC §1867(c) — Bank Service Company Act examiner access (operative for sponsor-bank fintech relationships).
- PCI DSS v4.0 — current version of the Payment Card Industry Data Security Standard.
- CSBS Money Services Businesses Model Money Transmission Modernization Act [verify state-specific adoption].
