# Source anchors: control-matrix

This file holds the named, dated regulatory and professional-standard sources the control-matrix skill anchors to. SKILL.md cites this file by path; the named anchors are not restated inline. Firm-specific anchors belong in `references/firm-overlay.md`.

`[verify section]` placeholders mark anchors where the precise section reference still needs verification against the current edition of the source. They are deliberate, not omissions. Fabricating a section reference is worse than leaving the placeholder.

## Internal-control framework foundation

### COSO Internal Control – Integrated Framework (May 2013)

Anchor: The five components (Control Environment, Risk Assessment, Control Activities, Information and Communication, Monitoring Activities) and the seventeen underlying principles. Many US financial-services firms anchor their internal-control framework on COSO 2013 for SOX 404 attestation purposes; the matrix taxonomy frequently mirrors the COSO components even when the regulator anchor is not COSO itself. [verify principle numbering against the current Framework edition; COSO has issued supplemental guidance since 2013.]

What this skill relies on: that "control objective" and "control activity" are distinct concepts, that controls roll up to one of five recognised components, and that the matrix can carry component-level coverage views when the firm anchors on COSO.

Link: https://www.coso.org/internal-control

## Risk-data and risk-reporting controls

### BCBS 239 — Principles for Effective Risk Data Aggregation and Risk Reporting (Basel Committee on Banking Supervision, January 2013)

Anchor: Fourteen principles. The matrix relies most directly on Principles 3 (accuracy and integrity), 4 (completeness), 6 (adaptability), 7 (accuracy of risk reporting), and 11 (distribution). G-SIBs were expected to comply by January 2016; D-SIBs follow national-supervisor timelines.

What this skill relies on: that risk-reporting matrices map principle-by-principle to data-quality, completeness, and timeliness controls; that uncontrolled principles are surfaced explicitly in the coverage-gaps section rather than buried.

Link: https://www.bis.org/publ/bcbs239.htm

## Model-risk controls

### SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (Federal Reserve and OCC, April 4, 2011)

Anchor: §IV (model development, implementation, and use), §V (validation), §VI (governance, policies, controls). [verify section labels against the published letter; the interagency text uses Roman-numeral sections.]

What this skill relies on: that model-risk control matrices distinguish development controls from validation controls from ongoing-monitoring controls, that segregation between developer and validator is itself a control attribute, and that material model changes route to a documented change-management gate.

Link: https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm

### Joint Interagency Revised Guidance on Model Risk Management — OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026 (April 17, 2026)

Anchor: Section II (scope and definitions), Section III (control environment, third-party model controls). The April 2026 joint guidance supersedes SR 11-7 (2011) and SR 21-8 (BSA/AML model risk, 2021). Most relevant to banking organizations with total assets over $30 billion; non-binding (does not set forth enforceable standards). Generative AI and agentic AI are explicitly out of scope (footnote 3); the principles cover traditional statistical and quantitative models and non-generative, non-agentic AI models.

What this skill relies on: refreshed control-environment language for traditional statistical / quantitative models, third-party-model control coverage where the model is vendor-developed or vendor-hosted, and the developer-validator segregation expectations in the joint guidance. For GenAI, agentic AI, or other AI-system scope outside the bulletin, the matrix anchors on NIST AI RMF 1.0, NIST AI 600-1, ISO/IEC 42001, the EU AI Act, and the firm's AI governance policy rather than this bulletin.

Link: https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html (parallels: https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm, https://www.fdic.gov/news/financial-institution-letters/2026/agencies-revise-interagency-model-risk-management-guidance)

## Information-security and IT controls

### FFIEC IT Examination Handbook — Information Security booklet (September 2016)

Anchor: §II.A (governance), §II.C.7 (logical security), §III (risk identification and assessment). [verify section labels against the currently posted edition; the FFIEC has issued booklet updates since 2016.]

What this skill relies on: that cyber-relevant controls in matrices for processes touching information systems carry the FFIEC framing for governance and logical security, and that the matrix can accept cyber-tagged controls cleanly via the cross-cutting overlay.

Link: https://ithandbook.ffiec.gov/it-booklets/information-security/

## Third-party risk controls

### Interagency Guidance on Third-Party Relationships: Risk Management (OCC / FRB / FDIC, June 6, 2023)

Anchor: §III.A (planning), §III.B (due diligence and selection), §III.C (contract negotiation), §III.D (ongoing monitoring), §III.E (termination). [verify section labels against the published guidance; the lifecycle phases are named explicitly in the text.]

What this skill relies on: that vendor-process control matrices align rows to the lifecycle phases the supervisors examine against, that critical-vendor controls are scoped at higher rigour than non-critical, and that termination and exit-plan controls are evidenced (not assumed).

Link: https://www.federalreserve.gov/supervisionreg/srletters/SR2304.htm

## Bank governance and risk-appetite controls

### 12 CFR Part 30, Appendix D — OCC Heightened Standards for Large Insured National Banks

Anchor: Standards I-V on the risk governance framework, three-lines-of-defense, independent risk management, and front-line-unit responsibilities. Threshold for application: covered banks at the OCC asset-size population. [verify the exact appendix and standard labels; Part 30 Appendix D is the operative text.]

What this skill relies on: that large-bank matrices for risk-governance processes carry rows for the heightened-standards architecture (CRO independence, board-risk-committee oversight, risk-appetite-statement controls, limits-framework controls) and that the matrix surfaces these as obligation-anchored rather than as policy-anchored.

Link: https://www.ecfr.gov/current/title-12/chapter-I/part-30/appendix-Appendix%20D%20to%20Part%2030

## Cybersecurity controls (state and federal)

### NYDFS 23 NYCRR Part 500 — Cybersecurity Requirements for Financial Services Companies (effective March 2017; amended November 2023)

Anchor: §500.3 (cybersecurity policy), §500.5 (vulnerability management), §500.11 (third-party service-provider security policy), §500.17 (notice of cybersecurity event). [verify the post-November-2023 amendment numbering for any covered-entity tier adjustments.]

What this skill relies on: that cyber-tagged control rows for NYDFS-covered entities reference the section that gives the obligation, that third-party cyber controls (§500.11) layer onto the TPRM matrix via the cross-cutting cyber overlay, and that incident-notice readiness is itself a control row when the process is in scope of §500.17.

Link: https://www.dfs.ny.gov/industry_guidance/cybersecurity

## Consumer-compliance management controls

### CFPB Compliance Management System guidance — Supervision and Examination Manual (current edition)

Anchor: The CMS chapter framing the four CMS pillars: board and management oversight, compliance program (policies and procedures, training, monitoring and corrective action), consumer complaint response, and compliance audit. [verify chapter and section labels against the current CFPB Supervision and Examination Manual edition.]

What this skill relies on: that consumer-compliance matrices for in-scope products carry rows for the four CMS pillars, that complaint-handling controls are evidenced (not assumed from the existence of an inbox), and that the matrix is readable line-by-line by a CFPB examiner.

Link: https://www.consumerfinance.gov/compliance/supervision-examinations/

## Records-retention controls (cross-cutting)

### SEC and FINRA recordkeeping (capital-markets matrices)

Anchor: 17 CFR §240.17a-3 and §240.17a-4 (broker-dealer recordkeeping), FINRA Rule 4511 (general books-and-records retention), 17 CFR §275.204-2 (Investment Advisers Act recordkeeping). [verify retention periods against the current rule text; the 2022 SEC amendment to 17a-4 adjusted the electronic-storage standard.]

What this skill relies on: that capital-markets matrices carry retention controls referencing the binding rule, not the firm's policy summary of the rule, and that the retention obligation drives the evidence pointer's expected window.

Link: https://www.sec.gov/divisions/marketreg/mrrecordkeeping.htm

## Privacy controls (cross-cutting, when in scope)

### GLBA Safeguards Rule — 16 CFR Part 314 (FTC, amended 2021/2023)

Anchor: 16 CFR §314.4 on the elements of an information security program. [verify section labels against the post-amendment edition; the 2021 amendment added specific control elements including encryption and MFA.]

What this skill relies on: that privacy-flagged matrices for processes touching nonpublic personal information carry §314.4 element-level rows, and that functional-regulator equivalents (interagency Safeguards rule for banks) substitute where the institution is bank-supervised rather than FTC-supervised.

Link: https://www.ftc.gov/legal-library/browse/rules/safeguards-rule

## AI-system controls (when AI overlay flagged)

### NIST AI Risk Management Framework 1.0 (NIST AI 100-1, January 2023) and NIST AI 600-1 Generative AI Profile (July 2024)

Anchor: AI RMF Core functions (Govern, Map, Measure, Manage); AI 600-1 risk subcategories specific to generative AI. [verify subcategory numbering against the current Profile edition.]

What this skill relies on: that AI-system control matrices can map AI-RMF-aligned obligations to firm controls when the scope flags AI as in scope; the AI overlay is consumed via the AI-governance plugin's references, not duplicated here.

Link: https://www.nist.gov/itl/ai-risk-management-framework

## Sector-specific anchors

The sector-overlay files (`references/sector-overlays/<sector>.md`) enumerate sector-specific anchors. The cross-cutting overlays (`references/cross-cutting/<topic>.md`) enumerate cross-cutting anchors. This file is the foundational set; the overlays add what the scope requires.
