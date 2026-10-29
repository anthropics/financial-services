# Banking sector overlay — control-matrix

Loads when the scope `sector_overlay_set` includes `banking`. Binds matrix construction to bank-supervisory expectations.

## Supervisory frame

US bank examiners (OCC, FRB, FDIC) read control matrices line-by-line during safety-and-soundness, BSA/AML, and consumer-compliance examinations. The matrix is rarely the sole evidence for a control rating, but it is the navigation device that organises everything else (policies, procedures, sample testing, exception logs, committee minutes). A matrix that an examiner cannot follow row-by-row is a finding waiting to happen.

State-member banks share supervision between the FRB and the state banking department; the matrix may need to evidence both supervisor's frames. National banks and federal savings associations sit with the OCC. State non-member banks sit with the FDIC and the state. The matrix author knows which constellation applies.

## Heightened standards architecture

For OCC large-bank populations covered by 12 CFR Part 30 Appendix D, the matrix carries rows for:

- The CRO independence model (named role, reporting line to the board risk committee, dual reporting if the firm uses it).
- The risk governance framework documentation (current version, approval history, board attestation).
- The risk-appetite-statement controls (board approval, breach-and-escalation framework, KRI alignment).
- The limits framework (front-line-unit, line-of-business, and aggregate limits, breach-and-escalation evidence).
- The independent-risk-management coverage map (what the second line independently challenges, what is read-only oversight, what is co-developed).

These rows do not appear in matrices for non-Heightened-Standards banks; the scope's institution profile drives the inclusion.

## FFIEC IT booklet integration

When the matrix scopes a process touching information systems (most do), the FFIEC IT Examination Handbook booklets frame the technology-control rows. Information Security booklet (governance, logical access, change management); Audit booklet (independence and audit-program design); Outsourcing Technology Services / Third-Party booklets (where the technology service is provided by a third party). The cyber cross-cutting overlay is the substantive content; this sector overlay simply confirms the FFIEC frame is the bank-side reading.

## Consumer-compliance and CRA triggers

When the matrix scopes a lending process, two banking-specific control families enter:

- **Fair-lending and ECOA / Reg B controls** — adverse-action notice content and timing (12 CFR §1002.9), prohibited-basis monitoring, exception-and-override review, comparator-file analysis where the firm performs it. The CFPB and the prudential supervisor both probe these.
- **CRA controls** — for banks subject to CRA, the matrix carries rows on CRA performance evaluation evidence, assessment-area controls, and small-business / small-farm / community-development data accuracy. The scope of CRA controls varies by the bank's CRA size category.
- **HMDA controls** — data accuracy, scrubbing and validation, LAR submission and resubmission controls. HMDA is Reg C; the matrix references the rule and the FFIEC HMDA Examiner Transmittal.

Consumer-compliance rows live in their own matrix block under a CMS lens (board-and-management oversight, compliance program, complaint response, compliance audit), keyed to the CFPB CMS framing.

## BSA / AML controls

When the matrix scopes a process where BSA applies (which is most customer-facing processes at most banks), the matrix carries rows for:

- The four pillars (board-approved BSA program, designated BSA officer, training, independent testing).
- CDD / EDD controls under FinCEN's Customer Due Diligence Rule (31 CFR §1010.230).
- Transaction-monitoring scenario-tuning and disposition controls.
- SAR-filing controls (timeliness, supervisory review, narrative quality), with the SAR filing itself excluded from the matrix evidence (SAR confidentiality under 31 USC §5318(g) prohibits documenting that a SAR was filed).
- CTR controls.
- OFAC / sanctions screening controls.

The BSA / AML control block is sometimes sufficiently large that it carries its own matrix (separate `matrix_id`) cross-referenced to the parent.

## Recordkeeping and retention

- Bank Service Company Act, 12 USC §1867(c): examiner-access expectations for third-party-provided services. Vendor-control rows reference the contract clause that gives the examiner access; if the clause is missing, the matrix surfaces a coverage gap.
- 12 CFR Part 1010 (FinCEN BSA recordkeeping): five-year retention floor for BSA records. The evidence-pointer expected window respects the five-year floor.

## Sign-off and review-gate norms

Bank-side matrices are reviewed by a named role keyed to the matrix scope: the BSA officer for BSA matrices, the chief compliance officer for consumer-compliance matrices, the chief risk officer (or the head of model risk under SR 11-7 matrices) for risk matrices, the chief credit officer for credit-risk matrices. Internal-audit reviews the matrix as part of its own scoping and references it in the audit workpapers; internal audit does not own the matrix.

## Anchors used by this overlay

- 12 CFR Part 30 Appendix D — OCC Heightened Standards [verify section labels].
- FFIEC IT Examination Handbook (Information Security, Audit, Outsourcing Technology Services booklets) [verify booklet revision dates].
- 12 CFR Part 1002 — Regulation B (ECOA implementation).
- 12 CFR Part 1003 — Regulation C (HMDA implementation).
- 12 CFR Part 25 / Part 228 / Part 345 — CRA implementing regulations (OCC / FRB / FDIC).
- 31 CFR §1010.230 — FinCEN Customer Due Diligence Rule.
- 31 CFR §1020 series — FinCEN bank-specific BSA rules.
- 31 USC §5318(g) — SAR confidentiality.
- 12 USC §1867(c) — Bank Service Company Act examiner access.
- CFPB Supervision and Examination Manual — CMS chapter [verify section labels].
