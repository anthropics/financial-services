# Cross-cutting overlay: privacy — obligation-mapping

Loaded when the scope includes `privacy` in `cross_cutting_overlay_set`, or when the source being mapped is privacy-anchored. Adds privacy-specific source labels and obligation patterns when the register scopes processes that touch nonpublic personal information, consumer financial information, or other regulated personal data. Does not change the row spine.

The privacy overlap with cyber is real but distinct: cyber covers information-security obligations on the system, privacy covers obligations on the data and the consumer relationship. Both overlays often load together; each carries its own rows.

## Sources the register may cite

### Federal financial-services privacy

- Gramm-Leach-Bliley Act privacy provisions, 15 U.S.C. §6801 et seq., implemented through:
  - CFPB Reg P, 12 CFR Part 1016. §1016.4 (initial privacy notice), §1016.5 (annual notice), §1016.10 (limits on disclosure to nonaffiliated third parties), §1016.13 (exception for service providers), §1016.15 (other exceptions).
  - FTC Privacy Rule (16 CFR Part 313) for non-bank financial institutions under FTC jurisdiction.
  - Functional-regulator equivalents (12 CFR Part 332 FDIC, 12 CFR Part 216 FRB, 12 CFR Part 1016 CFPB).
  - Use for: notice obligations, opt-out obligations, third-party-sharing limits.
  - Link: https://www.ecfr.gov/current/title-12/chapter-X/part-1016

- GLBA Safeguards Rule (FTC, 16 CFR Part 314 amended 2021/2023). §314.4 (information security program elements including encryption, MFA, vendor oversight). [verify section labels against current edition.]
  - Use for: information-security-program obligations under privacy framing; cross-load with cyber overlay where the engagement also covers cyber.
  - Link: https://www.ftc.gov/legal-library/browse/rules/safeguards-rule

- Fair Credit Reporting Act, 15 U.S.C. §1681 et seq.; Reg V, 12 CFR Part 1022.
  - §1022.20 (FCRA accuracy and integrity), §1022.40 (Affiliate Marketing Rule), §1022.80 (Disposal Rule), §1022.90 (Address Discrepancy Rule), §1022.123 (Identity Theft Red Flags Rule).
  - Use for: consumer-report-related privacy obligations; the Disposal Rule and Red Flags Rule are the most-cited rows.
  - Link: https://www.ecfr.gov/current/title-12/chapter-X/part-1022

### State privacy laws

- California Consumer Privacy Act / California Privacy Rights Act (Cal. Civ. Code §1798.100 et seq., as amended by CPRA).
  - §1798.100 (right to know), §1798.105 (right to delete), §1798.106 (right to correct), §1798.110 (right to access), §1798.120 (right to opt out of sale or sharing), §1798.121 (right to limit use of sensitive personal information).
  - Use for: California-resident-data obligations; covered businesses determined by §1798.140 thresholds.
  - Note: financial-information exemption under §1798.145(e) for data subject to GLBA; the exemption has limits, particularly for breach-notification obligations and pixel-tracking guidance.
  - Link: https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5

- Other state privacy laws. Virginia VCDPA (Va. Code §59.1-575 et seq.), Colorado CPA, Connecticut CTDPA, Utah UCPA, Texas TDPSA, and the additional state laws enacting in 2024-2026.
  - The register names each state where the entity has covered residents and notes the GLBA-data exemption posture per state.

### Health and other adjacents

- HIPAA for health-affiliated financial entities (45 CFR Parts 160, 162, 164).
  - Use for: PHI obligations on health insurers, FSAs, HSAs administered by financial institutions.

- Children's Online Privacy Protection Act, 16 CFR Part 312.
  - Use for: COPPA obligations where the financial institution offers a child-directed service.

### EU and UK privacy

- General Data Protection Regulation (Regulation (EU) 2016/679).
  - Articles 5 (principles), 6 (lawfulness of processing), 13-14 (information to data subjects), 17 (erasure), 28 (processor obligations), 30 (records of processing), 32 (security of processing), 33-34 (breach notification).
  - Use for: EU-personal-data obligations; the register names the controller and processor relationships per row.

- UK GDPR and Data Protection Act 2018.
  - Equivalent obligation set with UK-specific implementation.

## Obligation patterns the practitioner expects to find

- **Notice and choice rows.** GLBA Reg P initial and annual notices; CCPA notice-at-collection; GDPR Articles 13-14 information requirements. Each is a distinct obligation row with its own trigger and content requirement.
- **Data-subject-rights rows.** CCPA rights, GDPR Articles 15-22 rights, and FCRA dispute and access rights extract as separate rows because the response timeline and substantive scope differ.
- **Third-party data-sharing rows.** GLBA §1016.10 disclosure limits, CCPA opt-out-of-sale-or-sharing, and GDPR Article 28 processor terms each impose distinct third-party-related obligations.
- **Breach- and incident-notification rows.** State breach-notification laws (covering both financial and non-financial data depending on exemption posture), GDPR Articles 33-34, NYDFS §500.17, the federal banking 36-hour rule. Each row names the trigger, recipient, and window.
- **Records-of-processing and assessment rows.** GDPR Article 30 records, CCPA risk-assessment provisions [verify under CPRA regulations], and GLBA Safeguards Rule §314.4(d) risk-assessment requirements.
- **Sensitive-data and special-category rows.** CPRA sensitive personal information (§1798.121), GDPR Article 9 special categories. The register surfaces these as their own rows because the lawful-processing or use-limitation analysis is distinct.

## What does not belong here

- Information-security control specifics. Those belong in cyber overlay rows or in control-matrix output. Privacy overlay covers what data must be protected and disclosed; cyber overlay covers how the system protects it.
- Marketing-conduct obligations beyond data-driven marketing. Those go to the conduct cross-cutting overlay.
- Internal firm policy and taxonomy. That goes in `references/firm-overlay.md`.
