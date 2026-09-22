# Source anchors: issue-writeup

This file holds the named, dated regulatory and professional-standard sources the issue-writeup skill anchors to. SKILL.md cites this file by path; the named anchors are not restated inline. Firm-specific anchors (internal issue-rating ladders, named committee sign-offs, GRC-platform-specific status enums) belong in `references/firm-overlay.md`.

`[verify section]` placeholders mark anchors where the precise section reference still needs verification against the current edition of the source. They are deliberate, not omissions. Fabricating a section reference is worse than leaving the placeholder.

## Internal-audit communication framework

### IIA International Professional Practices Framework, Standard 2410 — Criteria for Communicating

Anchor: Standard 2410 sets the named elements of an internal audit communication: objectives, scope, conclusions, recommendations, and action plans. Standards 2410.A1, 2410.A2, 2410.A3, and 2410.C1 add detail on opinion expression, acknowledgement of acceptable performance, distribution rules, and consulting-engagement reporting respectively. The CCCE structure (criteria, condition, cause, effect) is the IIA's recommended construction for individual observations; recommendations follow. [verify the current IPPF revision; the IIA released the Global Internal Audit Standards effective January 2025 which restate parts of the prior IPPF.]

What this skill relies on: the CCCE element order, the requirement that communications include conclusions and recommendations, and the convention that an issue write-up names the criteria, observed condition, cause, and effect distinctly rather than collapsing them into prose.

Link: https://www.theiia.org/en/standards/

### IIA Global Internal Audit Standards (effective January 2025)

Anchor: Domain V (Performing Internal Audit Services), specifically Standards 13.1 (Communicating Engagement Conclusions) and 13.2 (Engagement Communication). [verify current standard numbers; the 2024 release reorganised the prior 2410 series.]

What this skill relies on: continuity of the CCCE convention through the Standards refresh, and the explicit requirement that engagement communications include the relevant criteria and the conclusions reached.

Link: https://www.theiia.org/en/standards/2024-standards/

## AICPA financial-statement audit framework

### AICPA AU-C Section 265 — Communicating Internal Control Related Matters Identified in an Audit

Anchor: AU-C 265.07 defines material weakness and significant deficiency. AU-C 265.11 sets the written-communication requirement to those charged with governance and management. The Appendix carries indicators of material weaknesses. [verify section labels against the current AICPA Clarified Auditing Standards edition; the AU-C numbering is stable but supplemental interpretations refresh periodically.]

What this skill relies on: the formal definitions of material weakness, significant deficiency, and control deficiency, which feed the firm's severity calibration when the issue is financial-statement-related; the convention that the communication carries the deficiency, criteria, cause, effect, and recommendation; and the principle that written communication is the artifact, not an oral readout.

Link: https://us.aicpa.org/research/standards/auditattest/clarifiedsas

## Federal supervisory finding framework

### Federal Reserve SR 13-13 / CA 13-10 — Supervisory Considerations for the Communication of Supervisory Findings

Anchor: The letter sets out the framework for how Federal Reserve examiners communicate findings. It distinguishes Matters Requiring Immediate Attention (MRIAs) from Matters Requiring Attention (MRAs), and describes the expectation that institutions establish processes for tracking and remediating both. [verify section labels; the SR letter is short and uses unnamed paragraphs rather than numbered sections.]

What this skill relies on: the MRA / MRIA distinction as a severity calibration anchor when the issue is sourced from a Federal Reserve supervisory letter, and the firm-side expectation that the issue is tracked through closure with documented remediation evidence.

Link: https://www.federalreserve.gov/supervisionreg/srletters/sr1313.htm

### OCC Bulletin 2014-39 — Matters Requiring Attention

Anchor: The bulletin defines OCC's MRA framework, the criteria for issuing MRAs, and the expectations on management response and tracking. It distinguishes MRAs from violations of law and from suggestions; MRAs are deficiencies in policies, procedures, or operations that require remediation. [verify section labels; the bulletin uses numbered sections.]

What this skill relies on: the OCC-specific MRA definition (which is narrower than common usage suggests), the expectation that MRAs are written with a clear corrective action and target date, and the firm's responsibility to track MRA closure with evidence the OCC will inspect.

Link: https://www.occ.gov/news-issuances/bulletins/2014/bulletin-2014-39.html

### FDIC supervisory letter conventions

Anchor: FDIC issues findings via Reports of Examination and supervisory letters. The Risk Management Manual of Examination Policies and the Compliance Examination Manual carry the conventions for findings (Matters Requiring Board Attention — MRBAs, recommendations, and violations). [verify the current edition's section labels for MRBA criteria.]

What this skill relies on: the FDIC-specific MRBA framing as the parallel construct to OCC MRAs and FRB MRAs, and the convention that MRBAs are addressed to the board rather than to management alone.

Link: https://www.fdic.gov/regulations/safety/manual/

## IT-audit and information-security finding framework

### FFIEC IT Examination Handbook — Audit booklet (April 2012)

Anchor: §IV.C reportable conditions and §IV.D follow-up procedures. The Audit booklet sets the FFIEC convention for IT-audit reportable conditions, the categorisation of findings, and the expected follow-up cadence. [verify section labels; the booklet uses Roman-numeral sections and lettered subsections.]

What this skill relies on: the IT-audit-specific reportable-condition convention (which lines up with the IIA framing but adds IT-control-specific language), the follow-up cadence expectation that supports the closure-evidence field, and the Audit-booklet expectation that internal audit's IT findings are tracked to closure with evidence the next examination will inspect.

Link: https://ithandbook.ffiec.gov/it-booklets/audit/

## Internal-control framework

### COSO Internal Control – Integrated Framework (May 2013)

Anchor: The 17 underlying principles structured under the five components (Control Environment, Risk Assessment, Control Activities, Information and Communication, Monitoring Activities). The framework is the basis for SOX 404 attestation in many US financial-services firms; the cause field on a financial-control issue often maps to one of the 17 principles. [verify principle numbering against the current Framework edition.]

What this skill relies on: the COSO structure as the cause-analysis taxonomy when the issue is financial-control-related and the firm anchors its internal-control framework on COSO; the convention that root cause maps to a named principle rather than to a generic label.

Link: https://www.coso.org/internal-control

## Sector-specific and cross-cutting anchors

The sector-overlay files (`references/sector-overlays/<sector>.md`) enumerate sector-specific finding-format anchors (NAIC examination findings, SEC EXAMS deficiency letters, FINRA examination findings, CFPB supervisory recommendations, OCC fintech bank-partnership conventions, NYDFS Part 500 finding patterns where sector-tied). The cross-cutting overlays (`references/cross-cutting/<topic>.md`) enumerate cross-cutting anchors (NYDFS Part 500 cyber findings, SEC Reg S-K Item 106 disclosure-process findings, Reg S-P incident-notification findings, CFPB UDAAP customer-harm findings). This file is the foundational set; the overlays add what the scope requires.

## Risk-data, model-risk, third-party, and AI overlays (referenced when in scope)

When the issue is scoped to one of the cross-plugin overlays, this skill cites the criteria from the relevant primitive's source anchors:

- Risk-data and risk-reporting findings cite BCBS 239 principles via `risk-compliance-core/skills/control-matrix/references/source-anchors.md` (Principles 3, 4, 6, 7, 11 are the most-cited).
- Model-risk findings cite SR 11-7 / OCC Bulletin 2026-13 via `ai-governance-model-risk/skills/...` (when present) or via the control-matrix source anchors.
- Third-party findings cite the Interagency Guidance on Third-Party Relationships (June 2023) §III.A through §III.E lifecycle phases.
- AI-system findings cite the NIST AI Risk Management Framework 1.0 and AI 600-1 Generative AI Profile.

The principle: criteria for cross-plugin issue write-ups reference the upstream skill's source-anchors file rather than restating the citations here. Maintenance benefit, when the upstream regulator updates a source, the citation updates in one place.
