# Banking sector overlay — policy-gap-review

Loads when the scope `sector_overlay_set` includes `banking`. Binds policy gap reviews to bank-supervisory expectations on the firm's policy framework.

## Supervisory frame

US bank examiners (OCC, FRB, FDIC) read policies as evidence of the firm's governance posture. The policy is rarely the sole evidence for any control rating, but a policy gap is a finding the supervisor will probe in fieldwork because it is the cheapest finding to issue: the policy text is the artefact, the benchmark text is the source, the gap reads itself. Policy refreshes ahead of examination cycles are routine; the gap matrix is the reviewer's sequencing tool.

State-member banks share supervision between the FRB and the state banking department; policy gap reviews may need to evidence both supervisor's frames. National banks and federal savings associations sit with the OCC. State non-member banks sit with the FDIC and the state.

## Heightened standards architecture

For OCC large-bank populations covered by 12 CFR Part 30 Appendix D, the matrix benchmarks the firm's risk-governance policy and the suite of risk-type policies against the heightened-standards framework:

- The risk governance framework (RGF) policy. Standards II and III set expectations on the framework's content (risk taxonomy, risk-appetite linkage, three-lines-of-defense roles, board oversight architecture).
- The risk-appetite-statement (RAS) policy. Standard III.E expects the RAS to set quantitative limits and qualitative tolerances aligned with the strategic plan; gap-matrix rows on RAS-policy content are common in pre-2014 RAS policies that have not been refreshed.
- The strategic plan policy. Standard III.D expects a comprehensive written strategic plan covering at least three years.
- Independent-risk-management coverage policies. Standard IV expects the second-line function to be independent, sufficiently resourced, and have authority that the firm-wide policy makes explicit.
- Front-line-unit responsibilities policy. Standard IV.A expects the front-line unit to assess and address risks; gap rows fire on policies that delegate risk responsibility entirely to the second line.

Heightened-standards rows do not appear in policy gap reviews for non-Heightened-Standards banks; the scope's institution profile drives the inclusion.

## OCC Bulletin 2014-39 framing

OCC Bulletin 2014-39 (Risk Governance for Banks) is the prudential supervisor's expectations document on policy-framework content for covered banks. The matrix benchmarks against the bulletin's expectations on:

- Board approval cadence and documentation.
- Policy-version control and document-management hygiene.
- Policy-to-RAS linkage and breach-and-escalation protocols.
- Policy ownership at the named-role level.

A policy gap matrix for a covered bank that does not benchmark against 2014-39 expectations is incomplete; the supervisor reads with the bulletin in hand.

## Consumer-compliance and CRA triggers

When the policy in scope is a lending or consumer-facing policy, three banking-specific benchmark families enter:

- **Fair-lending and ECOA / Reg B** — adverse-action notice content (12 CFR §1002.9), prohibited-basis monitoring policy expectations, exception-and-override review policy expectations, comparator-file analysis policy expectations where the firm runs them. Comment 9(b)(2)-3 of the Official Staff Commentary requires the cited reasons to relate to and accurately describe the factors actually considered or scored, and is the operative anchor for adverse-action notices on AI/algorithmic decisioning. (CFPB Circular 2022-03, which restated this point for complex algorithms, was **withdrawn May 12, 2025; historical only**.) ML-decisioning policies remain a frequent gap site.
- **CRA** — for banks subject to CRA, the matrix benchmarks against CRA performance evaluation policy expectations, assessment-area policy expectations, and small-business / small-farm / community-development data accuracy policy expectations. The scope of CRA expectations varies by the bank's CRA size category.
- **HMDA** — Reg C policy expectations on data accuracy, scrubbing and validation, LAR submission and resubmission. The FFIEC HMDA Examiner Transmittal sets the supervisory expectations on data-quality controls and policy-framework anchoring.
- **Section 1071** — Reg B Subpart B (12 CFR Part 1002, Subpart B) small-business data collection policy expectations. **§1071 revised final rule, May 1, 2026: 1,000 covered transactions; effective June 30, 2026; compliance January 1, 2028** — supersedes the 2023 tiered phase-in schedule. The matrix benchmarks against the revised rule and against the firm's covered-FI status.

## BSA / AML triggers

When the policy in scope is a BSA, AML, OFAC/sanctions, or financial-crime policy, the matrix benchmarks against:

- The four pillars (board-approved BSA program, designated BSA officer, training, independent testing) — explicit in the FFIEC BSA/AML Examination Manual.
- CDD / EDD policy expectations under FinCEN's CDD Rule (31 CFR §1010.230). Beneficial-ownership policy expectations are the most-cited 2018-onwards gap for legacy AML policies that pre-date the rule.
- SAR-filing policy expectations (timeliness, supervisory review, narrative quality) under 31 CFR §1020.320. SAR confidentiality under 31 USC §5318(g) constrains how the policy describes filing decisions; gap rows fire when the policy improperly references SAR contents in non-SAR sections.
- CTR policy expectations under 31 CFR §1010.310.
- OFAC sanctions screening policy expectations (the OFAC Framework for Compliance Commitments, May 2019).

The BSA/AML policy gap review is sometimes scoped as its own engagement; the matrix can carry a separate `review_id` cross-referenced to the parent enterprise policy gap review.

## Sign-off and review-gate norms

Bank-side policy gap reviews are reviewed by a named role keyed to the matrix scope: the BSA officer for BSA/AML policies, the chief compliance officer for consumer-compliance policies, the chief risk officer (or the head of model risk under SR 11-7 / 2026-13 matrices) for risk-management policies, the chief credit officer for credit-risk policies, the CISO for cybersecurity policies. The compliance committee or the relevant board committee tables the recommended edits at the cadence the firm's framework requires.

## Anchors used by this overlay

- 12 CFR Part 30 Appendix D — OCC Heightened Standards [verify section labels].
- OCC Bulletin 2014-39 — Risk Governance for Banks [verify section labels].
- FFIEC BSA/AML Examination Manual — current edition [verify chapter and section labels].
- 31 CFR §1010.230 — FinCEN Customer Due Diligence Rule.
- 31 CFR §1010.310 — FinCEN CTR rule.
- 31 CFR §1020.320 — FinCEN SAR rule for banks.
- 31 USC §5318(g) — SAR confidentiality.
- 12 CFR Part 1002 — Regulation B (ECOA implementation), including §1002.9 adverse-action notices.
- 12 CFR Part 1002 Subpart B — Section 1071 small-business data collection (**§1071 revised final rule, May 1, 2026: 1,000 transactions; effective June 30, 2026; compliance January 1, 2028** — supersedes the 2023 tiered schedule).
- 12 CFR Part 1003 — Regulation C (HMDA implementation).
- 12 CFR Part 25 / Part 228 / Part 345 — CRA implementing regulations (OCC / FRB / FDIC).
- CFPB Circular 2022-03 — Adverse Action Notice Requirements in Connection with Credit Decisions Based on Complex Algorithms (**withdrawn May 12, 2025; historical only**; Reg B §1002.9 and Comment 9(b)(2)-3 carry the obligation).
- OFAC Framework for OFAC Compliance Commitments (May 2019).
