# Payments and fintech sector overlay — evidence-binder

Loads when the scope `sector_overlay_set` includes `payments-fintech`. Binds evidence-binder content to bank-partnership, money-transmitter, and payment-network supervisory expectations.

## Supervisory frame

The supervisory map for fintechs splits by structure. A direct-chartered bank is supervised under the bank overlay. A non-bank fintech operating through a sponsor-bank arrangement is examined indirectly through the sponsor (FFIEC interagency third-party guidance, June 2023; the OCC's bank-partnership focus); the binder carries both partner-bank evidence and the fintech's own evidence. A non-bank fintech holding state money-transmitter licenses faces state-by-state examinations under the NMLS framework. Card-network participants face PCI DSS, network operating rules (Visa, Mastercard, network-specific), and FinCEN obligations as money-services businesses where applicable.

## Recordkeeping and retention

- **Bank Secrecy Act** — for fintechs registered as MSBs: 31 CFR §1010.430 general recordkeeping, §1022 series MSB-specific. Five-year retention floor for BSA records.
- **Reg E** — 12 CFR §1005, electronic-fund-transfer evidence: error-resolution records must be retained two years.
- **Reg Z** — 12 CFR §1026: two-year retention for credit-disclosure evidence.
- **CFPB supervisory authority** — Dodd-Frank §1024 (larger participants of consumer-financial-services markets) extends CFPB exam reach to fintechs above the relevant size thresholds.
- **PCI DSS** — log retention typically one year online, with the most recent three months immediately available; binder cites the firm's PCI-DSS attestation and the QSA's findings.
- **Money-transmitter licensing** — state retention varies; typical pattern is the longer of three years or state-specific window, with NMLS-uploaded records as the canonical reference.

## Common request-list shapes

Sponsor-bank-side RFIs typically cover the bank's TPRM evidence on the fintech: criticality assessment, due-diligence pack, contract, ongoing-monitoring evidence, BSA-program evidence (the fintech-side program plus the bank's oversight), Reg E and Reg Z evidence on consumer-facing flows, complaint logs, and the bank's own remediation tracking.

Fintech-side RFIs (state DFS, CFPB exams, network audits) typically cover: licensing and registrations, BSA program (program description, risk assessment, transaction-monitoring evidence, SAR filings), consumer-protection evidence (Reg E, Reg Z, UDAAP), complaint logs, dispute-handling evidence, and compliance with the network's operating rules.

## Sign-off and review-gate norms

Sponsor-bank binders for fintech-partnership exams are signed by the sponsor-bank's BSA officer or chief compliance officer. Fintech-side binders are signed by the fintech's BSA officer (where MSB-registered) or chief compliance officer.

For BaaS arrangements, the binder may need to evidence both sides; the scope record names which side this binder represents.

## Anchors used by this overlay

- Interagency Guidance on Third-Party Relationships: Risk Management (OCC/FRB/FDIC, June 2023).
- 31 CFR §1010.430 — FinCEN general recordkeeping.
- 31 CFR §1022 series — MSB-specific FinCEN rules.
- 12 CFR §1005 — Reg E (Electronic Fund Transfers Act implementation).
- 12 CFR §1026 — Reg Z (Truth in Lending Act implementation).
- Dodd-Frank Act §1024 — CFPB supervisory authority over larger participants.
- PCI DSS v4.0 — current version of the Payment Card Industry Data Security Standard.
