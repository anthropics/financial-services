# Troubleshooting: control-matrix

Recurring failure modes when a control matrix looks complete but is not. The reviewer pass should catch these; the builder pass should preempt them.

## 1. Controls listed without an obligation source

Symptom: the matrix has thirty rows; ten of them have no entry in the obligation-source column. The reviewer cannot tell why those controls exist.

Why it happens: hygiene controls (data-quality housekeeping, internal sign-offs, "we always do this") get ported in because the team performs them, not because an obligation requires them. Or the obligation extraction is incomplete and the controls drift in ahead of their parent obligations.

Fix: every row carries an `obligation_id`. If the control is a hygiene control, move it out of the matrix into the firm's procedure documentation. If the control is real and the obligation is missing, the upstream `obligation-mapping` work is incomplete; flag it in `coverage_gaps` rather than improvise an obligation. The matrix is obligation-anchored; that is the discipline.

## 2. Control objective and control activity collapsed into one field

Symptom: the row's control objective reads "the team reconciles the warehouse extract monthly". That is not an objective; it is an activity.

Why it happens: practitioners write what the team does because it is concrete, and skip the underlying condition the activity is supposed to make true.

Fix: the objective is the condition that must be true ("source-system data feeding the credit-risk pack reconciles to the system of record at month-end with documented variance disposition"). The activity is who does what, how often, using what system. Both fields are required. Rows with one but not the other are not yet controls; they are placeholders. The schema enforces both fields on `control.schema.json`.

## 3. Policy listed as evidence

Symptom: the evidence pointer column reads "Risk Reporting Policy v4.2". The reviewer cannot test from a policy.

Why it happens: the policy is the easiest artifact to point at and is already approved by the committee. Pointing at it feels safer than pointing at the operational record.

Fix: policy is a control statement, not evidence of operation. The evidence pointer is a system-of-record output, a sample report ID, a sign-off log path, a reconciliation log entry. "Risk Reporting Policy v4.2 §3.2" can appear as the obligation-source label or as the firm-policy citation; it does not appear in the evidence column. If no operational evidence exists, the row is `not-tested`; that surfaces the gap honestly.

## 4. Control owner is a team, not a role

Symptom: owner column reads "Risk Team", "Compliance", "Operations".

Why it happens: the engagement has not yet pinned down the named accountable role, and the team-level label feels right at the level of generality the matrix was drafted at.

Fix: the owner is a named role with accountability: Head of Model Risk, Chief Privacy Officer, Head of Vendor Management, Head of Credit Risk Reporting, BSA Officer. "Risk team" is not an owner. If the role is genuinely contested or shared, name both ("Head of Decision Sciences for development; Head of Model Validation for validation") and add a reviewer question on the joint-ownership documentation.

## 5. Coverage gaps section is empty

Symptom: every obligation in scope has a mapped control. The matrix looks clean.

Why it happens: gaps were buried (the partial mapping was rated effective rather than partially-effective), or obligations were dropped from scope rather than admitted as uncovered.

Fix: a control matrix without coverage gaps is rare in real engagements. Either obligation extraction was over-narrow, or partial mappings were over-rated, or hygiene controls were treated as substantive. Re-walk the obligation list and ask "is the operating evidence sufficient that an examiner reading this row would call it covered?" If no, the row is a coverage gap or a partial-mapping with a downgraded effectiveness rating. Empty `coverage_gaps` should trigger a sign-off question, not a confidence boost.

## 6. Effectiveness ratings inflate over time

Symptom: third refresh of the matrix shows every control rated effective; the prior matrix showed three partially-effective rows. No remediation evidence appears in the revision log.

Why it happens: each refresh tends to refresh ratings without re-testing. The ratings drift to whatever the team thinks is reasonable rather than what the most recent test actually showed.

Fix: a rating change requires a test result that supports it. The `last_test_date` and the upstream test workpaper (from `compliance-testing` or internal audit) are the evidence. Without a refreshed test, the prior rating carries forward; the matrix does not invent improvements. The `revisions` section names what changed and why.

## 7. Cyber overlay loaded but ignored

Symptom: the scope flags `cyber` in the cross-cutting overlay set; the matrix has no cyber-tagged rows. The cyber overlay was loaded but did not land in the matrix.

Why it happens: the overlay is treated as background reading rather than as content that adds rows. Or the matrix author defers cyber to "the CISO's separate matrix" without surfacing the cyber-tagged rows the substantive process needs.

Fix: when `cyber` is in the cross-cutting set, the matrix carries cyber-tagged rows for the in-scope process: governance, identity-and-access, vulnerability, incident-response, third-party-cyber, data-protection. The CISO function is a co-owner or reviewer on those rows; it is not an excuse to leave them out of the substantive matrix. Same logic for the `privacy` overlay.

## 8. Sector overlay loaded but ignored

Symptom: banking sector overlay loaded but the matrix has no Heightened-Standards rows for a Heightened-Standards-covered bank; insurance overlay loaded but no MAR §16 rows for an ICFR-in-scope insurer; capital-markets overlay loaded but no annual-review-cycle rows for an adviser.

Why it happens: the overlay is treated as background framing rather than as a directive on what rows the matrix carries.

Fix: when the scope names a sector, the matching `references/sector-overlays/<sector>.md` content lands as named rows in the matrix. The overlay's "what changes" content is the contract; the matrix author honours it. Sector-specific reviewer questions go to the reviewer-question list.

## 9. Joint ownership left implicit

Symptom: a model-risk control row names "Head of Model Risk" as the owner; the underlying control is access-control on the model serving environment, which is operationally owned by the CISO function. The matrix does not surface the joint ownership.

Why it happens: the matrix author owns the matrix and writes the owner from their seat. The CISO function does not see the matrix until much later.

Fix: joint ownership is a row attribute. Name both roles when both are accountable; name the primary explicitly. Add a reviewer question on whether the joint ownership is papered in the firm's RACI or only in this matrix. Joint ownership is common; obscuring it is a finding waiting to happen.

## 10. The matrix is signed off without independent reviewer

Symptom: sign-off block names the practitioner who built the matrix and the sponsor; no independent reviewer is named.

Why it happens: smaller engagements compress the review machinery; larger engagements over-rely on the sponsor as the reviewer.

Fix: the reviewer is independent of the author. For 1.5-line-built matrices, the 2-line function reviews. For 2-line-built matrices, internal audit or an independent peer reviews. For advisory-built matrices, the engagement partner reviews. The sponsor signs off as accountable, not as the independent reviewer; a single name in both seats fails the independence test.

## 11. Test method is "inquiry" by default

Symptom: most rows show `test_method: inquiry`. Reviewer cannot tell whether the controls actually operate.

Why it happens: inquiry is the cheapest test method (talk to the owner, ask if it ran). It is also the weakest evidence on operating effectiveness.

Fix: inquiry alone is rarely sufficient for operating-effectiveness evidence on controls that produce inspectable artifacts. Match the test method to the control: inspection (sample artifacts), reperformance (re-run the control on a sample), observation (watch the control execute), data-analysis (population-level analytics), walkthrough (end-to-end transaction trace). Inquiry-only rows are flagged in reviewer questions.

## 12. The matrix tries to be the model card, the test workpaper, and the binder

Symptom: the matrix carries ten columns of model documentation, test sample listings, and evidence file contents. It is unreadable.

Why it happens: the matrix gets stretched because adjacent skills' outputs are not yet built and the team puts everything in the matrix as a stopgap.

Fix: the matrix lives upstream of `compliance-testing` (the test workpaper), `model-card-builder` (the model card), and `evidence-binder` (the binder). It carries the row-level summary; the upstream artifacts carry the depth. Cross-references via `control_id` and `obligation_id`. Pulling everything into the matrix breaks the contract with downstream skills.

## 13. The matrix stops too late

Symptom: the skill produces a "signed-off" matrix with effectiveness ratings asserted and remediation actions claimed as in-flight, without evidence.

Why it happens: builder over-runs the human-review gate.

Fix: the matrix is a draft until the named reviewer attests. The skill stops at the draft and surfaces the reviewer questions; it does not assert sign-off, distribute, or post to the GRC system. The `human_review_required` field is always true.
