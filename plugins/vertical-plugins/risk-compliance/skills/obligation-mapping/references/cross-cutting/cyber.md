# Cross-cutting overlay: cyber — obligation-mapping

Loaded when the scope includes `cyber` in `cross_cutting_overlay_set`, or when the source being mapped is cyber-anchored. Adds cyber-specific source labels and obligation patterns the practitioner expects to find when the register scopes information-security or cybersecurity processes. Does not change the row spine.

The cyber overlay is the most-loaded cross-cutting overlay in this skill: most material processes touch information systems, and most multi-source registers carry at least one cyber-anchored row.

## Sources the register may cite

### State-issued cyber rules

- NYDFS 23 NYCRR Part 500 — Cybersecurity Requirements for Financial Services Companies (effective March 2017; amended November 2023).
  - §500.2 (cybersecurity program), §500.3 (cybersecurity policy), §500.4 (CISO), §500.5 (vulnerability management), §500.7 (access privileges), §500.9 (risk assessment), §500.11 (third-party service-provider security policy), §500.13 (asset management), §500.14 (training and monitoring), §500.16 (incident response and BCDR), §500.17 (notice of cybersecurity event).
  - Use for: NYDFS-covered entities; the register cites the precise §500.x section per row and notes covered-entity tier under the November 2023 amendment.
  - Link: https://www.dfs.ny.gov/industry_guidance/cybersecurity

### Federal cyber rules

- SEC cybersecurity disclosure rules (2023, 17 CFR Part 229 and Part 232).
  - Reg S-K Item 106 (cyber risk management, strategy, and governance disclosure).
  - Form 8-K Item 1.05 (material cybersecurity incident disclosure within four business days of materiality determination).
  - Use for: issuer-side cybersecurity disclosure obligations on registered companies; cross-load with `capital-markets` if the engagement includes issuer reporting.
  - Link: https://www.sec.gov/rules/final/2023/33-11216.pdf

### Federal supervisory expectations

- FFIEC Information Security booklet (September 2016; under current revision).
  - §II (governance), §III (risk identification and assessment), §IV (mitigation), §V (security operations), §VI (testing), §VII (incident response), §VIII (resilience). [verify section labels against currently posted edition.]
  - Use for: bank-supervised information-security obligations; the booklet is supervisory expectation rather than rule, and the register notes that distinction in the source-trace.
  - Link: https://ithandbook.ffiec.gov/it-booklets/information-security/

- Interagency Guidelines Establishing Information Security Standards (12 CFR Part 30 Appendix B / Part 208 Appendix D / Part 364 Appendix B).
  - §III (information security program), §III.C (assess risk), §III.D (manage and control risk).
  - Use for: bank-supervised information-security-program obligations under GLBA §501(b) implementation.

- Computer-Security Incident Notification Rule for banking organizations (12 CFR Part 53 OCC / Part 225 Appendix N FRB / Part 304 FDIC), effective May 2022.
  - 36-hour notification obligation to the primary federal regulator following determination of a notification incident.
  - Use for: incident-notification obligations on supervised banking organizations.
  - Link: https://www.ecfr.gov/current/title-12/chapter-I/part-53

- FFIEC Authentication and Access to Financial Institution Services and Systems guidance (August 2021).
  - Use for: customer-authentication and access-control obligations.

### EU cyber and ICT

- DORA — Regulation (EU) 2022/2554. Articles 5-14 (ICT risk management framework), Articles 17-23 (ICT-related incident management, classification, reporting), Articles 24-27 (digital operational resilience testing), Articles 28-30 (ICT third-party risk).
  - Use for: EU-anchored cybersecurity and ICT obligations; the register cites the named article on each row.
  - Link: https://eur-lex.europa.eu/eli/reg/2022/2554/oj

### Privacy adjacents (when scope edges into privacy)

- GLBA Safeguards Rule (FTC, 16 CFR §314.4 elements; functional regulator equivalents for bank-supervised institutions).
  - Use for: information-security-program elements when the privacy overlay is also loaded.

## Obligation patterns the practitioner expects to find

- **Section-precise rows.** NYDFS Part 500 obligations extract at the §500.x level; mapping a single Part 500 obligation to "the program in general" loses the rule. The register cites the section.
- **Tier-dependent applicability.** Part 500 amendments introduced covered-entity tiers; the row's applicability column carries the tier reasoning.
- **Incident-notification obligations as their own rows.** The 36-hour banking incident notification, NYDFS §500.17, SEC Form 8-K Item 1.05, and DORA Article 19 incident-classification windows all extract as separate rows because the trigger, recipient, and timing differ. The register does not collapse them.
- **Third-party cyber obligations.** NYDFS §500.11, the Interagency Guidelines third-party expectations, and DORA Article 28 each impose distinct third-party security obligations; the register surfaces them rather than rolling them into a generic "vendor security" row.
- **Authentication and customer-protection cyber overlap.** FFIEC authentication guidance interacts with Reg E error-resolution and unauthorized-transfer obligations; the register treats these as separate but cross-referenced rows.

## What does not belong here

- Bank capital and credit obligations. Cyber overlay is for information-security obligations; load `banking` for capital and credit.
- Privacy obligations beyond information security (notice and choice, data-subject rights, advertising-data use). Load the privacy cross-cutting overlay for those.
- Internal firm policy, security-control library, or specific control procedures. Those go in `references/firm-overlay.md` or in control-matrix output, not in the obligation register.
