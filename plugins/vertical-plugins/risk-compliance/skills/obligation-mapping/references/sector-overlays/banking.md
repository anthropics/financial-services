# Banking sector overlay: obligation-mapping

Loaded when the scope includes `banking` in `sector_overlay_set`. Adds banking-specific source labels and obligation patterns the practitioner expects to find when the register scopes a banking process. Does not change the row spine.

## Sources the register may cite

### Heightened standards and large-bank governance

- 12 CFR Part 30 Appendix D — OCC Heightened Standards for Large Insured National Banks. Standards I-V on the risk-governance framework, three-lines-of-defense, independent risk management, front-line-unit responsibilities. Threshold: covered banks at the OCC asset-size population. [verify the exact appendix-and-standard labels against the current Code of Federal Regulations text.]
  - Use for: enterprise-risk-governance obligations, risk-appetite-statement obligations, board-risk-committee oversight obligations at large national banks.
  - Link: https://www.ecfr.gov/current/title-12/chapter-I/part-30/appendix-Appendix%20D%20to%20Part%2030

### Insider lending and affiliate transactions

- Regulation O — 12 CFR Part 215 (Loans to Executive Officers, Directors, and Principal Shareholders of Member Banks). §215.4 (general prohibitions and lending limits), §215.5 (executive-officer loans), §215.8 (records), §215.11 (disclosure of loans by member banks).
  - Use for: insider-lending obligation rows where the register scopes commercial-lending or executive-officer credit processes.
  - Link: https://www.ecfr.gov/current/title-12/chapter-II/subchapter-A/part-215

- Regulation W — 12 CFR Part 223 (Transactions Between Member Banks and Their Affiliates). §223.11 (10% limit), §223.12 (20% limit), §223.13 (collateral requirements), §223.16 (low-quality assets). [verify subsection labels against current Part 223.]
  - Use for: affiliate-transaction obligations when the register scopes intercompany funding, asset transfers, or services.
  - Link: https://www.ecfr.gov/current/title-12/chapter-II/subchapter-A/part-223

### FRB SR letters as obligation source

- SR 16-11 — Supervisory Guidance for Assessing Risk Management at Supervised Institutions. [verify section labels.]
  - Use for: risk-management governance obligations at FRB-supervised institutions; the SR letter pattern is to extract the obligation by SR-letter number and section, then cross-reference to the underlying rule.
  - Link: https://www.federalreserve.gov/supervisionreg/srletters/sr1611.htm

- SR 20-15 / SR 13-19 — supervisory guidance on operational resilience and outsourcing. [verify section labels and current applicability.]
  - Use for: operational-resilience and outsourcing obligation rows when the register scopes a banking process touching critical operations.

### Bank-supervised information security and privacy

- Interagency Guidelines Establishing Information Security Standards (12 CFR Part 30 Appendix B for OCC; Part 208 Appendix D for FRB; Part 364 Appendix B for FDIC). §III (information security program elements), §III.C (assess risk), §III.D (manage and control risk).
  - Use for: bank-side information-security-program obligations when the register scopes information-security or vendor-information-security work; load alongside the cyber cross-cutting overlay where the engagement also includes NYDFS Part 500 or FFIEC IT.
  - Link: https://www.ecfr.gov/current/title-12/chapter-I/part-30/appendix-Appendix%20B%20to%20Part%2030

- 12 CFR Part 332 (FDIC Privacy of Consumer Financial Information) and 12 CFR Part 1016 (CFPB Reg P). §1016.4 (initial notice), §1016.10 (disclosure limits and exceptions). [verify FDIC Part 332 numbering against current Code.]
  - Use for: GLBA Privacy Rule obligation rows when the register scopes consumer-deposit or lending products at a bank; load alongside the privacy cross-cutting overlay.
  - Link: https://www.ecfr.gov/current/title-12/chapter-X/part-1016

## Obligation patterns the practitioner expects to find

- **Three-lines-of-defense obligation rows.** OCC Heightened Standards split into front-line, second-line independent risk, and third-line audit obligations; the register surfaces them as separate rows even when the underlying rule reads as one section, because the owner and the evidence are different on each line.
- **Capital and liquidity reporting obligations.** Reg YY enhanced prudential standards for $100B+ holding companies, FR Y-9C and FR Y-14 reporting cycles, LCR reporting under 12 CFR Part 249. The register treats each report as its own row when the scope includes regulatory reporting.
- **CRA and fair-lending obligation pair-up.** When the register scopes a lending process, expect Reg B (12 CFR Part 1002) ECOA obligations alongside CRA performance-evaluation obligations under 12 CFR Part 25 (OCC) / Part 228 (FRB) / Part 345 (FDIC). Load the conduct cross-cutting overlay.
- **BSA/AML obligations.** Use the FFIEC BSA/AML Examination Manual section structure; the bank-side rows extract from 31 CFR Part 1020 (CDD for banks), 31 CFR 1010.230 (BO), 31 CFR 1020.220 (CIP), 31 CFR 1020.320 (SAR).

## What does not belong here

- Sponsor-bank-fintech allocation language. That belongs on the contractual source row in the register itself, anchored on the sponsor agreement, with `payments-fintech` overlay loaded if the fintech side is in scope.
- Insurance-side obligations even where a bank holding company also owns an insurance subsidiary. Run a separate register for the insurance subsidiary with `insurance` overlay.
- Internal firm policy and taxonomy. That goes in `references/firm-overlay.md` regardless of sector.
