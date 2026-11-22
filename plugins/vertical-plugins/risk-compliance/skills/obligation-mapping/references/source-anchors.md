# Source anchors: obligation-mapping

This file holds the named, dated regulatory and professional-standard sources the obligation-mapping skill anchors to. SKILL.md cites this file by path; the named anchors are not restated inline. Firm-specific anchors belong in `references/firm-overlay.md`.

`[verify section]` placeholders mark anchors where the precise section reference still needs verification against the current edition of the source. They are deliberate, not omissions. Fabricating a section reference is worse than leaving the placeholder.

## Risk-data and risk-reporting traceability

### BCBS 239 — Principles for Effective Risk Data Aggregation and Risk Reporting (Basel Committee on Banking Supervision, January 2013)

Anchor: Fourteen principles. The register relies most directly on Principle 2 (data architecture and IT infrastructure) for the source-trace expectation, Principle 3 (accuracy and integrity), and Principle 11 (distribution and reporting frequency) when the source being mapped is a risk-reporting requirement. G-SIBs were expected to comply by January 2016; D-SIB timelines follow national-supervisor decisions.

What this skill relies on: that traceability from a risk-reporting obligation back to the rule that imposes it is itself a regulatory expectation; that the register's source-trace block is a BCBS 239 artifact in spirit; that risk-reporting obligations carry frequency, distribution, and accuracy as named applicability dimensions.

- Link with section: https://www.bis.org/publ/bcbs239.htm — Principles 1 through 11 (G-SIB scope), Principles 12-14 (supervisory expectations).

## Internal-control and ERM framing

### COSO Enterprise Risk Management — Integrating with Strategy and Performance (June 2017)

Anchor: The five components (Governance and Culture; Strategy and Objective-Setting; Performance; Review and Revision; Information, Communication, and Reporting) and the twenty principles. ERM framing applies when the register supports risk-appetite or strategic-objective alignment.

What this skill relies on: that the register's applicability column maps obligations to in-scope strategic objectives where the engagement is ERM-anchored, and that the open-question summary feeds the COSO Review-and-Revision cycle when the firm runs one.

- Link with section: https://www.coso.org/enterprise-risk-management — Principles 1-20 across the five components.

### COSO Internal Control — Integrated Framework (May 2013)

Anchor: Five components (Control Environment, Risk Assessment, Control Activities, Information and Communication, Monitoring Activities) and seventeen principles. Many US financial-services firms anchor their internal-control framework on COSO 2013 for SOX 404 attestation purposes.

What this skill relies on: that obligations imposing controls roll up to one of the five components; that the register can carry COSO-component tags when the firm anchors on COSO 2013.

- Link with section: https://www.coso.org/internal-control — Principles 1-17.

## Information-security and IT obligation source

### FFIEC IT Examination Handbook — Information Security booklet (September 2016)

Anchor: §II.A (governance), §II.C.7 (logical security), §III (risk identification and assessment). [verify section labels against the currently posted edition; the FFIEC has issued booklet updates since 2016.]

What this skill relies on: that information-security obligations extracted from FFIEC IT material map cleanly to a process and a control objective, and that the cyber cross-cutting overlay loads when the source is FFIEC IT.

- Link with section: https://ithandbook.ffiec.gov/it-booklets/information-security/ — Booklet §II governance, §III risk assessment, [verify section] for incident management.

## Third-party risk obligation source

### Interagency Guidance on Third-Party Relationships: Risk Management (OCC / FRB / FDIC, June 6, 2023)

Anchor: §III.A (planning), §III.B (due diligence and selection), §III.C (contract negotiation), §III.D (ongoing monitoring), §III.E (termination). [verify section labels against the published guidance; the lifecycle phases are named explicitly in the text.]

What this skill relies on: that TPRM obligations align to the lifecycle phases the supervisors examine against; that obligations on the firm and obligations on the third party are extracted as separate rows when the source is the contract or SLA itself; that critical-vendor obligations carry tighter applicability than non-critical.

- Link with section: https://www.federalreserve.gov/supervisionreg/srletters/SR2304.htm — §III.A through §III.E lifecycle phases.

## Consumer-compliance management obligation source

### CFPB Compliance Management System guidance — Supervision and Examination Manual (current edition)

Anchor: The CMS chapter framing the four CMS pillars: board and management oversight; compliance program (policies and procedures, training, monitoring and corrective action); consumer complaint response; compliance audit. [verify chapter and section labels against the current CFPB Supervision and Examination Manual edition.]

What this skill relies on: that CFPB-supervised firms map UDAAP, Reg E, Reg Z, Reg DD, and ECOA obligations into a CMS-pillar applicability tag; that the register is readable by a CFPB examiner line by line; that complaint-handling obligations have evidence pointers naming the system of record.

- Link with section: https://www.consumerfinance.gov/compliance/supervision-examinations/ — CMS chapter, four pillars [verify pillar labels].

## Model-risk obligation source

### SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (Federal Reserve and OCC, April 4, 2011, superseded April 17, 2026)

Anchor: §IV (model development, implementation, and use), §V (validation), §VI (governance, policies, controls). Superseded by the joint April 2026 guidance below. Retained as historical anchor for obligations the firm extracted under the prior framing.

- Link with section: https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm — §IV, §V, §VI.

### Joint Interagency Revised Guidance on Model Risk Management — OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026 (April 17, 2026)

Anchor: Section II (scope and definitions), Section III (control environment, third-party model controls). The April 2026 joint guidance supersedes SR 11-7 (2011) and SR 21-8 (BSA/AML model risk, 2021). Most relevant to banking organizations with total assets over $30 billion; non-binding (does not set forth enforceable standards). Generative AI and agentic AI are explicitly out of scope (footnote 3); the principles cover traditional statistical and quantitative models and non-generative, non-agentic AI models.

What this skill relies on: refreshed model-risk obligation language for traditional statistical and quantitative models and non-generative, non-agentic AI models; third-party-model obligations where the model is vendor-developed or vendor-hosted; the developer-validator segregation expectation carried forward. For GenAI or agentic-AI obligation extraction, the register anchors on NIST AI RMF 1.0, NIST AI 600-1, ISO/IEC 42001, the EU AI Act, and the firm's AI governance policy rather than this bulletin.

- Link with section: https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html — Section II, Section III. Parallels: https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm, https://www.fdic.gov/news/financial-institution-letters/2026/agencies-revise-interagency-model-risk-management-guidance.

## Financial-crime obligation source

### FFIEC BSA/AML Examination Manual (current edition, 2024 update referenced)

Anchor: Customer Identification Program section, Customer Due Diligence section, Beneficial Ownership section, Suspicious Activity Reporting section, OFAC section. [verify section labels against the current online edition; the manual is web-published and revises in place.]

What this skill relies on: that BSA/AML obligations are extracted at the manual-section grain and cross-referenced to the underlying CFR (31 CFR 1010, 1020, 1021, 1022, 1023, 1024, 1025, 1026 by industry); that bank-side and fintech-side obligations under a sponsor arrangement extract as separate rows.

- Link with section: https://bsaexaminationmanual.ffiec.gov/ — CDD, BO, SAR, OFAC sections [verify chapter labels].

### 31 CFR 1010.230 — Beneficial Ownership Requirements for Legal Entity Customers (FinCEN)

Anchor: §1010.230(b)(1) identification, §1010.230(b)(2) verification, §1010.230(d) certification form requirement, §1010.230(e) covered financial institution definition.

What this skill relies on: that beneficial-owner obligations are extracted at the subsection level (identification distinct from verification distinct from recordkeeping), and that the rule's certification-form mechanic is itself an obligation row.

- Link with section: https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1010/subpart-D/section-1010.230 — §1010.230(b), (d), (e).

## Consumer-lending obligation source

### CFPB Section 1071 Final Rule — Small Business Lending Data Collection (12 CFR 1002.107)

Anchor: §1002.107(a) covered application identification, §1002.107(b) covered originations threshold, §1002.105 covered financial institution definition, Subpart B firewall provisions [verify subsection], §1002.110 reporting and §1002.111 recordkeeping. **§1071 revised final rule, May 1, 2026; 1,000 covered transactions; effective June 30, 2026; compliance January 1, 2028** — supersedes the 2023 tiered schedule.

What this skill relies on: that 1071 obligations are extracted at the lifecycle stage (application identification, data-point collection, firewall, recordkeeping, reporting, error correction) with the relevant CFR subsection on each row; that the single 1,000-transaction threshold and the June 30, 2026 effective / January 1, 2028 compliance dates from the May 2026 revised final rule are used (the 2023 tiered high-volume / moderate-volume / low-volume schedule is superseded); that the firewall obligation is treated as a design obligation requiring legal review where loan officers act in dual roles.

- Link with section: https://www.ecfr.gov/current/title-12/chapter-X/part-1002/subpart-B — §1002.107, §1002.110, §1002.111.

## EU operational-resilience obligation source

### DORA — Regulation (EU) 2022/2554 on Digital Operational Resilience for the Financial Sector

Anchor: Articles 5-14 (ICT risk management framework), Articles 15-23 (ICT-related incident management, classification, reporting), Articles 24-27 (digital operational resilience testing), Articles 28-30 (ICT third-party risk), Articles 31-44 (oversight of critical ICT third-party service providers). [verify article numbering against the published OJ text.]

What this skill relies on: that DORA-anchored registers carry ICT obligations against the named articles; that ICT-third-party obligations under Articles 28-30 are extracted as a separate cluster from internal ICT obligations; that the register-of-information requirement (Article 28) is itself an obligation row, not just a downstream artifact.

- Link with section: https://eur-lex.europa.eu/eli/reg/2022/2554/oj — Articles 5-30.

## State cybersecurity obligation source

### NYDFS 23 NYCRR Part 500 — Cybersecurity Requirements for Financial Services Companies (effective March 2017; amended November 2023)

Anchor: §500.2 cybersecurity program, §500.3 cybersecurity policy, §500.5 vulnerability management, §500.7 access privileges, §500.9 risk assessment, §500.11 third-party service-provider security policy, §500.17 notice of cybersecurity event. [verify the post-November-2023 amendment numbering for any covered-entity tier adjustments.]

What this skill relies on: that NYDFS-anchored registers cite the precise §500.x section on each row; that the §500.11 third-party obligation extracts separately from internal cybersecurity obligations; that incident-notice readiness (§500.17) is its own obligation row when the process is in scope.

- Link with section: https://www.dfs.ny.gov/industry_guidance/cybersecurity — §500.2, §500.3, §500.5, §500.11, §500.17.

## EU AI obligation source

### EU AI Act — Regulation (EU) 2024/1689

Anchor: Article 6 (high-risk classification), Articles 8-15 (requirements for high-risk AI systems), Articles 16-21 (provider obligations), Articles 26-29 (deployer obligations), Articles 50-55 (transparency and general-purpose AI). [verify article numbering against the published OJ text.]

What this skill relies on: that AI-anchored registers distinguish provider obligations from deployer obligations; that high-risk AI obligations extract as a separate cluster from general transparency obligations; that the obligation-by-article approach makes downstream change-management tractable as the AI Act's implementing acts roll out.

- Link with section: https://eur-lex.europa.eu/eli/reg/2024/1689/oj — Articles 6-29, Articles 50-55.

## Records-retention as cross-cutting source

### SEC and FINRA recordkeeping (capital-markets registers)

Anchor: 17 CFR §240.17a-3 and §240.17a-4 (broker-dealer recordkeeping), FINRA Rule 4511 (general books-and-records retention), 17 CFR §275.204-2 (Investment Advisers Act recordkeeping). [verify retention periods against the current rule text; the 2022 SEC amendment to 17a-4 adjusted the electronic-storage standard.]

What this skill relies on: that capital-markets registers carry retention obligations referencing the binding rule, not a firm policy summary; that the retention period drives the evidence-required column's expected window.

- Link with section: https://www.sec.gov/divisions/marketreg/mrrecordkeeping.htm — 17 CFR §240.17a-3, §240.17a-4; FINRA Rule 4511.

## Sector- and cross-cutting-specific anchors

The sector-overlay files (`references/sector-overlays/<sector>.md`) enumerate sector-specific anchors that load when the scope flags that sector. The cross-cutting overlays (`references/cross-cutting/<topic>.md`) enumerate cross-cutting anchors. This file is the foundational set; the overlays add what the scope requires.
