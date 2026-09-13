# Source anchors: evidence-binder

This file holds the named, dated regulatory and professional-standard sources the evidence-binder skill anchors to. SKILL.md cites this file by path; the named anchors are not restated inline. Sector-specific anchors live in `references/sector-overlays/<sector>.md`; cross-cutting anchors live in `references/cross-cutting/<topic>.md`. Firm-specific evidence-handling rules belong in `references/firm-overlay.md` when the firm installs one.

`[verify section]` placeholders mark anchors where the precise section reference still needs verification against the current edition of the source. They are deliberate, not omissions. The discipline of the binder is the same discipline applied here: a screenshot is not evidence, the system-of-record link is.

## Risk-data evidence and traceability

### BCBS 239 — Principles for effective risk data aggregation and risk reporting (January 2013)

Anchor: Principles 3 (accuracy and integrity), 4 (completeness), and 7 (accuracy of risk reporting). [verify section labels under the BIS publication; these principles are stable since the 2013 issuance.]

What this skill relies on: the requirement that risk-data evidence in the binder is traceable to a system of record, complete against the population it claims to describe, and reconciled against the report that consumed it. The binder's `system_of_record`, `period_start`, `period_end`, and `provenance` fields exist to satisfy these principles. For G-SIBs and D-SIBs the principles bind directly; for other institutions they are influential rather than mandatory and the binder should not over-claim.

Link: https://www.bis.org/publ/bcbs239.htm

## Audit evidence — the underlying definitional framing

### AICPA AU-C 500 — Audit Evidence (clarified standard)

Anchor: AU-C 500 on the sufficiency and appropriateness of audit evidence. [verify exact paragraph references — .04 through .11 in the current edition cover the definitions of sufficient and appropriate audit evidence and the auditor's evaluation thereof.]

What this skill relies on: the foundational distinction between sufficiency (quantity of evidence) and appropriateness (relevance and reliability of evidence) that internal-audit, external-audit, and second-line testing functions all inherit. The binder's `completeness_flag`, `evidence_type`, and reviewer-sign-off fields are how these properties surface in the index. AU-C 500 also establishes that evidence from the entity's own information system is more reliable when controls over that system have been tested; the binder's provenance fields capture the conditions under which that reliability claim holds.

Link: https://us.aicpa.org/research/standards/auditattest/clarifiedsas

### AICPA AU-C 230 — Audit Documentation

Anchor: AU-C 230 on the form, content, and extent of audit documentation, and on the assembly and retention of the audit file. [verify paragraph references in the current edition.]

What this skill relies on: the discipline that documentation enables an experienced auditor with no previous connection to the audit to understand the work performed, the evidence obtained, and the conclusions reached. The binder is a second-line analogue, not an audit file, but the experienced-reviewer test is the same: another reviewer should be able to pick up the binder cold and follow what each row supports.

Link: https://us.aicpa.org/research/standards/auditattest/clarifiedsas

## Internal-audit evidence and engagement records

### IIA International Professional Practices Framework, Global Internal Audit Standards (effective January 2025)

Anchor: Standards on engagement-evidence sufficiency, engagement records, and reporting. Standard 14 (Conducting the Engagement), particularly the requirements on collecting sufficient, reliable, relevant, and useful information, and Standard 15 (Communicating Results), on supporting communications with engagement evidence. [verify section labels under the current 2025 IIA standard set; superseded the prior 2310/2330/2410 numbering used in the 2017 IPPF.]

What this skill relies on: the four-attribute test for engagement information (sufficient, reliable, relevant, useful) that an internal-audit binder must satisfy. The binder's `evidence_type`, `system_of_record`, and `provenance` columns are how these attributes surface for the binder's audience.

Link: https://www.theiia.org/en/standards/

## IT-audit evidence and recordkeeping

### FFIEC IT Examination Handbook — Audit Booklet (April 2012)

Anchor: §III on audit programs and procedures and §IV.B on workpapers and documentation. [verify section labels in the edition currently posted; the booklet has been republished with formatting changes since 2012 but the substantive expectations are stable.]

What this skill relies on: the booklet's framing of audit-evidence sufficiency for IT and third-party audit programs, and the workpaper-retention expectations the binder's row-level metadata supports. Bank examiners read the binder against this booklet when the binder covers IT-audit work; the binder cites the booklet section by reference rather than by excerpt.

Link: https://ithandbook.ffiec.gov/

## Model-validation evidence

### Joint Interagency Revised Guidance on Model Risk Management — OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026 (April 17, 2026)

Anchor: Section II (scope and definitions), Section III (control environment, third-party model controls, documentation, independent challenge). The April 2026 joint guidance supersedes SR 11-7 (2011) and SR 21-8 (BSA/AML model risk, 2021). Most relevant to banking organizations with total assets over $30 billion; non-binding (does not set forth enforceable standards). Generative AI and agentic AI are out of scope (footnote 3); the principles cover traditional statistical and quantitative models and non-generative, non-agentic AI models.

What this skill relies on: the model-validation evidence categories the binder organizes against (conceptual soundness, ongoing monitoring, outcomes analysis, benchmarking, independent challenge). A model-validation binder built without grouping rows by validation activity is unreviewable by the model-risk function. Where the validation binder lacks evidence of independent challenge, the gaps section names that absence directly. For GenAI or agentic AI evidence packs, the binder anchors on NIST AI RMF, NIST AI 600-1, ISO/IEC 42001, the EU AI Act, and the firm's AI governance policy rather than this bulletin.

Link: https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html (parallels: https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm, https://www.fdic.gov/news/financial-institution-letters/2026/agencies-revise-interagency-model-risk-management-guidance)

### SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management (April 4, 2011, superseded April 17, 2026)

Anchor: §V on model validation (conceptual soundness, ongoing monitoring, outcomes analysis, benchmarking) and §VI on governance, policies, and controls. Superseded by the joint April 2026 guidance above; retained as historical citation for binders that reach back to validation evidence produced under the prior framing.

Link: https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm

### FRB SR 13-19 — Guidance on Managing Outsourcing Risk (December 5, 2013)

Anchor: SR 13-19 on supervisory expectations for outsourced services and the documentation a firm should maintain to evidence its third-party risk-management program. [verify section labels — the letter addresses risk-assessment, due-diligence, contract, ongoing-monitoring, and termination evidence expectations.]

What this skill relies on: the evidence-pack expectations for vendor-review binders at FRB-supervised institutions. The 2023 interagency third-party-risk guidance superseded SR 13-19 for material it covers, but SR 13-19 remains the citation for the FRB's prior framing where the binder reaches back to pre-2023 vendor reviews.

Link: https://www.federalreserve.gov/supervisionreg/srletters/sr1319.htm

## Supervisory examination evidence

### Interagency Guidance on Third-Party Relationships: Risk Management (June 6, 2023, OCC / FRB / FDIC)

Anchor: §III on risk management throughout the third-party lifecycle (planning, due diligence and selection, contract negotiation, ongoing monitoring, termination), each step of which generates evidence the binder indexes for vendor-review work. [verify section labels under the published guidance.]

What this skill relies on: the lifecycle-aligned evidence categories for vendor-review binders. The binder's `request_list` for a vendor review typically tracks the lifecycle phases this guidance defines.

Link: https://www.federalreserve.gov/supervisionreg/srletters/SR2304.htm

### OCC Comptroller's Handbook — Bank Supervision Process and individual booklets

Anchor: Bank Supervision Process booklet for the examination scope-setting and evidence-request process; topical booklets (BSA/AML, Allowance for Credit Losses, Internal Controls, etc.) for scope-specific evidence expectations. [verify booklet name and section labels for the current editions.]

What this skill relies on: the request-list shapes the binder reconciles against for OCC-supervised institutions. The handbook is the reference; the binder is the artifact.

Link: https://www.occ.gov/publications-and-resources/publications/comptrollers-handbook/

## Recordkeeping floors that bear on the binder

### Bank Service Company Act — 12 USC §1867(c)

Anchor: §1867(c) on examiner access to records of services performed by third parties for insured depository institutions. The binder's vendor rows reference the contract clause that gives the examiner access; if the clause is missing, the binder surfaces a gap rather than asserting access exists.

Link: https://www.law.cornell.edu/uscode/text/12/1867

### FinCEN BSA recordkeeping — 31 CFR Part 1010 (general) and Part 1020 (banks)

Anchor: 31 CFR §1010.430 (general records to be made and retained) and the part-specific recordkeeping rules; five-year retention floor for most BSA records. [verify section labels for the current eCFR text.]

What this skill relies on: BSA-evidence rows in the binder carry a `period_start` that respects the five-year retention floor even when the supervisory window is shorter, because the underlying records must remain available.

Link: https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X

### SEC Rule 17a-4 / FINRA Rule 4511 — Books and records (broker-dealers)

Anchor: 17 CFR §240.17a-4 and FINRA Rule 4511, on the records that broker-dealers must preserve and the form and medium of preservation. [verify section labels; the SEC amended 17a-4 in 2022 with electronic-recordkeeping changes.]

What this skill relies on: capital-markets-binder rows reference the rule the underlying record is preserved under; sector-overlay carries the detail.

Link: https://www.sec.gov/rules/final/2022/34-96034.pdf

## Cyber, privacy, climate, conduct (when applicable)

When the engagement carries cyber, privacy, climate, or conduct overlay, the cross-cutting overlay files add the relevant anchors. The privacy overlay (`references/cross-cutting/privacy.md`) is the one currently shipped; cyber, climate, and conduct overlays may be added when scope demands.

Specifically:
- Cyber: NYDFS 23 NYCRR Part 500 §500.16 (incident response) and §500.17 (notice of cybersecurity event) [verify current section labels]; SEC Form 8-K Item 1.05 cyber disclosure [verify rule citation]; SEC Reg S-K Item 106 [verify].
- Privacy: covered in `references/cross-cutting/privacy.md`.
- Climate: not anchored.
- Conduct: CFPB Examination Manual UDAAP module [verify edition reference]; fair-lending exam evidence patterns under ECOA / Reg B and HMDA / Reg C.

These overlays load when the scope's `cross_cutting_overlay_set` includes the corresponding entry.
