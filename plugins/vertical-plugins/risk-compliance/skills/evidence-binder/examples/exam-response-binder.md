# Example: exam-response evidence binder for a state-DOI market-conduct exam

Public-source-derived. No named institution. The shape mirrors a common pattern: a P&C insurer's compliance team assembles the evidence binder for a state Department of Insurance market-conduct examination focused on claims-handling timeliness and unfair claims-settlement practices.

## Input

- **Binder purpose**: regulator-exam.
- **Scope**: state-DOI market-conduct exam, claims-handling segment. Period covered: 2024-01-01 to 2025-12-31.
- **Reviewer**: examiner-in-charge (external); internal sponsor is the chief compliance officer; the binder is being assembled by a market-conduct compliance manager.
- **Engagement scope supplied**: institution = P&C insurer, state-licensed; primary regulators = state DOI (lead), NAIC accreditation framework background; persona = chief compliance officer; source posture = public-plus-firm-policy-plus-evidence; sector overlay = insurance; cross-cutting overlays = privacy (claims data carries NPI and PHI on first-party medical-payments coverage), conduct (unfair-claims-practices and bad-faith exposure).
- **Inputs already on file**: examiner request list issued at exam open (47 items); claims-platform extracts; complaint log; state DOI complaint correspondence; the firm's claims handbook and procedure versions in force during the period; sample workpapers from the firm's prior internal market-conduct review.

## Output sketch

The skill produces an evidence binder. Headlines:

- **Scope and binder purpose** — regulator-exam, 24-month period, examiner-in-charge reviewer; source posture supports direct extracts from the claims platform (Guidewire ClaimCenter is the named system of record) and the complaint-management system.
- **Request list** — all 47 examiner items captured verbatim. Status reconciled: 38 `met`, 5 `partial`, 3 `gap`, 1 `not-applicable` (a request for a product line the firm does not write in the state).
- **Evidence index, sample rows**:
  - Claims-handling timeliness extract for the period (`system-extract`, system of record = Guidewire ClaimCenter, period = 2024-01-01 to 2025-12-31, `provenance.reproducible = true`).
  - Sample of 60 claim files selected by the firm's internal sampling protocol (`sample-workpaper`, system of record = the same, paired with the sampling-method memo as a `management-memo`).
  - Complaint log for the period (`system-extract`, system of record = complaint-management system).
  - State DOI complaint correspondence (`regulatory-correspondence`, sensitivity = `restricted`).
  - Claims handbook v6.1 and v6.2 in force during the period (`policy-version`, system of record = policy-management system).
  - Adjuster training records (`training-record`, system of record = LMS).
  - Three signed-attestation rows from claims operations leadership, paired with the underlying staffing reports (`signed-attestation` plus `system-extract`).
- **Evidence by finding** — populated for two open issues from the firm's prior internal review: an issue on first-contact letter timeliness (remediation evidence shows the letter-template change and the post-change timeliness metrics) and an issue on adjuster-training completion (remediation evidence shows the catch-up training records and revised quarterly attestation).
- **Provenance concerns** — one row flagged: a screenshot of the examiner's prior on-site question log, taken from the examiner portal during a working session, is in the binder for context. The `system_of_record_link` is the examiner portal record ID; the provenance concern notes that the firm cannot reproduce a portal screenshot if access changes.
- **Evidence gaps** — three items: an aged inventory of claims open more than 90 days at year-end 2024 (firm's reporting was rebuilt mid-period and the prior view is not reproducible), the staffing-ratio analysis the examiner asked for at the segment-by-line level (firm has the totals but not the segmentation), and the evidence of a bad-faith-handling training module the examiner expected (firm covers the topic in the broader claims-ethics module but not as a discrete module).
- **Evidence by control** — the firm's claims-timeliness control, complaint-handling control, and adjuster-training control each carry the supporting rows and a sufficiency call.
- **Custodian register** — claims operations director (claims-handling rows), complaint manager (complaint rows), HR L&D manager (training rows), compliance manager (policy and procedure rows). Compliance director signs the binder.
- **Reviewer questions** — should the screenshot row be removed before the binder is filed (provenance concern), or kept with the explicit caveat? Does the bad-faith-training gap warrant supplementary evidence (sample handling files showing the practice) or a remediation commitment with a deadline?
- **Confidence label**: `medium`. Posture is high and most rows are reproducible; the gaps and the screenshot pull confidence down.
- **Sign-off**: blank. The binder is a draft until the chief compliance officer signs and the examiner-in-charge accepts.

The binder is the index that the examiner works against; the firm does not take a litigation or settlement position from this artifact.

## Why this scenario matters

- **Practitioner trick line**: "a management memo is not a substitute for a system extract." The signed-attestation rows from claims-operations leadership pair with the underlying staffing reports; without the pairing, the binder would be carrying assertions as evidence.
- **Practitioner trick line**: "the examiner's request list is the binder's spine." Every request maps to evidence rows or to the gaps section; silent omissions are what trigger the supplementary-request loop the firm is trying to avoid.
- **Boundary check on sensitivity**: state DOI correspondence is `restricted` (regulator-confidential); the binder must not co-mingle restricted and lower-classification rows in shared review folders.
- **Boundary check on the screenshot rule**: the portal screenshot is in the binder because the examiner's question log lives in the examiner-controlled system, not in a firm-controlled system of record. The binder is honest about the provenance limit; it does not pretend the screenshot is reproducible firm-side evidence.
- **Boundary check on cross-overlays**: privacy applies (claims data, NPI and PHI in medical-pay segments), conduct applies (unfair-claims-practices statute). Both overlays load; the binder cites the relevant state UDAP and the NAIC Model Unfair Claims Settlement Practices Act anchors in the source trace.
- **Boundary check on the gap-versus-finding distinction**: a gap in the binder is not yet a finding. The examiner may treat it as one; the binder's job is to surface it honestly with an owner and a target close. The skill stops at the draft binder; the response posture is decided by counsel and the CCO.

## Anchors

- NAIC Model Audit Rule (Model #205), §16 internal control over financial reporting [verify section].
- NAIC Market Conduct Examiners Handbook, claims-handling examination standards [verify section].
- State Unfair Claims Settlement Practices Act (NAIC Model #900) [verify state-specific adoption].
- AICPA AU-C 500, audit evidence — sufficiency and appropriateness framing.
- IIA International Standards 2310 and 2410 [verify section labels].

See `references/source-anchors.md` for full citations.
