# Troubleshooting: evidence-binder

The binder is a reconciliation surface, not a folder. When it fails (the regulator's request list does not square with what the binder shows, the reviewer cannot tell what supports what, the audit working paper review bounces it back), the cause is almost always one of the recurring defects below. Practitioner trick line that captures the discipline: a screenshot is not evidence; the system-of-record link is.

## 1. The binder is a folder of unlabeled screenshots

**Symptom**: Reviewer or examiner asks "where did this come from", and the answer is "from the system" without a system-of-record name, an extract method, or a date the extract was taken. The binder reads as a screenshot dump rather than an indexed evidence pack.

**Why it happens**: The team treated the binder as storage rather than as an index. Screenshots were captured in the moment without recording provenance, then dropped into a SharePoint folder named after the exam.

**Resolution**:
- Every row carries `system_of_record` (a named system, not "internal database"), `provenance.extract_method`, `provenance.extracted_by` (a named role), and `provenance.extracted_at` (an ISO datetime).
- A screenshot is a row attribute, not a row in itself. The row records what the screenshot shows; the screenshot is an attachment that proves the screen state. The system-of-record reference is the actual evidence.
- If the system of record cannot be named, the row is not evidence yet. It belongs in `evidence_gaps` until the source is identified.

## 2. The request list and the evidence index do not reconcile

**Symptom**: Examiner or audit lead reviews the binder and finds RFI items that have no corresponding evidence row, or evidence rows that do not map to any RFI item. Both directions of the gap are common.

**Why it happens**: The binder was assembled by walking the evidence the team already had rather than by walking the request list. The mapping was never built explicitly.

**Resolution**:
- Build the binder from the request list outward. Each `request_list` item gets either a populated `evidence_items` row (or rows) or a populated `evidence_gaps` row. No request item ends in limbo.
- Evidence rows that do not map to a request item belong in their own section (often a "supplementary evidence" group) with an explanation of why they are in the binder. Otherwise they are noise to the reviewer.
- The reconciliation is itself a deliverable. A clean binder with `request_list` populated, every item resolved, and gaps named is more credible than a fat binder with no reconciliation.

## 3. The custodian field is set to a team

**Symptom**: Custodian column reads "Compliance" or "Risk" or "Operations" across many rows. When the binder is challenged on a specific row, no individual is accountable for the integrity of that piece of evidence.

**Why it happens**: The team set the field to a team name as a default. The role-level discipline was not enforced.

**Resolution**:
- Custodian is a named role accountable for the integrity of that evidence (Head of Model Risk Reporting, BSA Officer, Director of Vendor Management, Lead Underwriting Auditor). Not a team name. Not a person name (the role outlasts the person).
- The custodian is the role the reviewer goes back to with questions. If the role does not exist or does not have the standing to answer, the row's provenance is weaker than it appears.
- For multi-source evidence (e.g., a reconciliation that pulls from two systems), name a primary custodian and reference the contributing roles in the description.

## 4. Period coverage is stale

**Symptom**: Evidence rows have `date_generated` six months before the period under review, or `period_start` / `period_end` that do not align to the supervisory or audit window. The reviewer rejects the row on timeliness grounds.

**Why it happens**: Stock evidence (last quarter's BCBS 239 lineage report, last year's vendor-tier list) was carried into the binder without checking that the dates fit the current scope.

**Resolution**:
- Set `period_start` and `period_end` against the engagement's actual window, not against the date the evidence was first generated. Re-pull stock evidence when the period has moved.
- For evidence that does not have a period (a policy version, a contract, a charter), `date_generated` and `period_covered` collapse into the effective-date and effective-period of the document. Capture the document version explicitly.
- Where the supervisory window is short but the underlying recordkeeping floor is longer (BSA: five years; broker-dealer books and records: three to six years depending on rule), the binder's row-level metadata respects the floor even if the engagement window is shorter.

## 5. Assertions are mixed with evidence

**Symptom**: A management memo asserting "controls are operating effectively as of period end" appears in the evidence index alongside system extracts and test results, with no flag distinguishing the two.

**Why it happens**: The team did not draw the line between evidence (something that exists in the world and can be inspected) and assertion (something a person or function says). Both are useful; they are not the same.

**Resolution**:
- Use `evidence_type` honestly. A management memo is `attestation` or `other`, not `system report` or `sample workpaper`.
- For attestation rows, the description names who attested, on what basis, and against what underlying evidence (which other binder rows). An attestation that does not point at underlying evidence is an opinion, not testimony.
- The reviewer can choose to credit an attestation; they cannot credit an attestation dressed up as a system extract.

## 6. The binder cannot be re-pulled

**Symptom**: A year later, the binder is referenced in a regulator follow-up or an internal-audit replay. The team cannot reproduce the evidence because the source systems have changed, the queries were not preserved, or the extract method was undocumented.

**Why it happens**: Provenance was captured as a snapshot, not as a method. The binder records what was extracted but not how to extract the same thing again.

**Resolution**:
- For system-extract rows, `provenance.extract_method` names the query, the report ID, the dashboard ID, or the file path that produces the extract. Where a SQL query was hand-written, the query text is attached. Where a vendor system produced the report, the report name and report parameters are recorded.
- For ad-hoc extracts (a one-off pull from a system that does not have a standing report), the binder flags this in the provenance description and the gap section notes the operational risk of non-reproducibility.
- The replay test is the discipline: another team member, six months later, with the binder in hand, should be able to re-pull every system-extract row.

## 7. Privacy posture is set to "internal" by default

**Symptom**: Every row carries `sensitivity: internal` regardless of content. The binder includes NPI samples, PHI narratives, or restricted-classification material at the same posture as a published policy. When the binder is shared with external counsel or a regulator, the firm has no row-level control.

**Why it happens**: The team did not load the privacy overlay when the binder warranted it, or loaded it but did not apply row-level classification.

**Resolution**:
- Load `references/cross-cutting/privacy.md` whenever the binder may carry NPI, PHI, PCI, or other regulated personal data. The overlay is mandatory by content, not optional by preference.
- Classify rows honestly. Sample claim files with NPI are `confidential` or `restricted`, not `internal`. Materiality memos under legal privilege are `restricted`. Public policies are `public`.
- Sensitivity drives downstream handling: redaction, segregation, distribution-list control. A binder that defaults every row to `internal` cannot support any of that.

## 8. Gaps are hidden

**Symptom**: The binder reads clean (no rows in `evidence_gaps`) but the reviewer or examiner finds gaps anyway. The team's claim that the binder is complete collapses on inspection.

**Why it happens**: Gaps were filled with weak evidence to avoid an empty `evidence_gaps` section, or the gap analysis was never run because a clean binder felt better.

**Resolution**:
- Every `request_list` item that is not unambiguously met by an `evidence_items` row generates an `evidence_gaps` row. Partial coverage is partial; mark it.
- A binder with named gaps and a remediation plan is stronger than a binder with hidden gaps. Reviewers credit honesty about gaps; they discount binders that claim completeness and do not survive scrutiny.
- The completeness flag on a row (`complete`, `partial`, `gap`) is the row-level analogue. Rows flagged `partial` accumulate; if too many rows are partial, the binder summary acknowledges the cumulative weakness.

## 9. The binder is signed by a function rather than a role

**Symptom**: The sign-off block reads "Reviewed by Compliance" with no named role. When the binder is later challenged, no individual function head is on record as accountable for the binder's integrity.

**Why it happens**: The sign-off was treated as a courtesy line rather than as the accountability act it is.

**Resolution**:
- The reviewer is a named role (Chief Compliance Officer, Chief Risk Officer, Audit Director, Head of Model Risk, Head of TPRM). The sign-off captures the role, the date, and any caveats the reviewer wants on record.
- Multiple roles may sign for different sections. A model-validation binder may carry the head of model risk for §V evidence and the model owner for the development-data extract section.
- The sign-off block is the contract between the binder and the audience. Without it, the binder is a draft.

## 10. The skill is invoked when the work is upstream

**Symptom**: The team called evidence-binder when the actual work was generating the evidence (running the source-system report, executing the test, drafting the memo). The binder produced is empty or tautological because there is no evidence to index yet.

**Why it happens**: The team conflated "we need an evidence pack" with "we need to build the evidence." Different work, different skills.

**Resolution**:
- The "Not the right tool when" section of the SKILL.md is the contract. Producing the underlying evidence is upstream of this skill; this skill indexes existing evidence.
- If the team needs the evidence built, the upstream work belongs in the source-system team, the testing function, or the relevant control-owner team. Evidence-binder catches the artifacts those teams produce.
- For drafting findings from missing evidence, hand off to `issue-writeup`. For committee narratives, hand off to `risk-committee-pack`. The binder is the source of truth those skills consume; it is not the narrative they produce.
