# Troubleshooting: issue-writeup

Recurring failure modes when an issue write-up looks complete but is not. The reviewer pass should catch these; the builder pass should preempt them.

## 1. Condition reads as a conclusion

Symptom: the condition field reads "the control failed" or "the control is ineffective" or "vendor oversight is weak". The reviewer cannot tell what was actually observed.

Why it happens: practitioners write what they have concluded because it is the bottom line. The CCCE structure asks for the observable state first, the conclusion later (it ends up split across cause and effect).

Fix: the condition is the dated, scoped, observable state. "On three monthly reporting cycles between 2026-01 and 2026-03, two material counterparty exposures totalling $187M notional were excluded from the consolidated counterparty view." That is the condition. "The control failed" is the cause analysis sitting in the wrong field. The schema validates that condition is non-empty; the discipline is to write the observation in present-tense observable terms.

## 2. Criteria reads as "per firm policy" without citation

Symptom: the criteria field reads "per firm policy", "per applicable regulation", or "per industry best practice". The reviewer cannot read the criterion.

Why it happens: the practitioner knows the firm has a policy on this and has not yet gone back to the policy or the regulation to pull the section reference.

Fix: criteria is a named source with a section. If the criterion is regulatory, name the rule and section and reference `references/source-anchors.md` or a loaded overlay file by path. If the criterion is the firm's own policy, name the policy version and section and reference `references/firm-overlay.md` by path. "Per firm policy" without citation is a placeholder; the criteria_source_anchor field carries the path the reviewer can follow. Multiple criteria are allowed and common; list each with its source.

## 3. Cause reads as "human error" or "training gap" or "system limitation"

Symptom: the cause field is a one-line surface label that does not name the control attribute that failed.

Why it happens: surface labels are easy to write and feel correct because the underlying behaviour did involve a person, a training opportunity, or a system constraint. The control-design or operation weakness underneath is the part that has not yet been thought through.

Fix: name the control attribute that failed. "Human error" is replaced by "the reconciliation control's design assumes the feed cutoff equals the source-system close; that assumption became false when the feed-orchestration team shifted the batch window without coordinating with the reconciliation control owner". "Training gap" is replaced by "the SOC-report-review workflow does not include a downstream trigger from qualified-opinion-noted to compensating-control-evaluated". "System limitation" is replaced by "the population query in the controls-testing platform truncates records older than the 90-day window without flagging the truncation in the test result". If root cause analysis is genuinely pending, write "root cause analysis pending" and add an open action; do not invent a cause to fill the field.

## 4. Effect is generic ("significant impact")

Symptom: the effect / impact field reads "significant impact", "material implication", or "meaningful exposure" without quantification or specific identification.

Why it happens: the practitioner writes the effect as commentary because the quantification is hard or the harm is not yet quantified.

Fix: the effect names the unit, the time window, and the population where applicable. "$X under-stated counterparty exposure on three reporting cycles, propagated into the executive risk pack distributed to the Board Risk Committee" is an effect. "Significant impact" is commentary. Where the effect is across multiple dimensions (financial, customer, regulatory, operational, reputational), name each separately. Where a dimension genuinely has no impact (e.g., reputational impact on an internal-control finding with no public-facing element), say so explicitly rather than omitting the dimension.

## 5. Severity without rationale

Symptom: severity is set to "high" or "critical" with no rationale field, or a rationale field that reads "given the nature of the finding".

Why it happens: severity assignment under time pressure tends to default to high or critical, and the rationale gets deferred.

Fix: severity is paired with rationale referencing materiality, frequency, customer impact, regulatory exposure, and any compensating controls in place. The rationale is also defensible against the next-lower severity ("not critical because [...]") and the next-higher severity ("higher than moderate because [...]"). Severity assignment carries human review; the unattested severity is not yet a severity.

## 6. Closure evidence is the verb, not the artifact

Symptom: closure evidence reads "remediated", "control updated", "policy revised", or "issue closed".

Why it happens: the closure evidence field is filled at write-up time when remediation has not yet happened; the practitioner writes the verb because the artifact does not yet exist.

Fix: closure evidence names the artifact the firm will inspect to confirm closure. "Two consecutive months of reconciled feed output reviewed by the Head of Market Risk Reporting with sign-off log retained in the GRC platform" is closure evidence. "Remediated" is not. The artifact may be a system-of-record output, a sample report, a sign-off log, a board minute, a tabletop after-action report, a third-party administrator's restitution-completion attestation, or any other inspectable record. The closure evidence is testable; the closure verb is not.

## 7. Owner is a team, not a role

Symptom: owner field reads "Risk Team", "Compliance", "Operations", or a person's name.

Why it happens: the engagement has not yet pinned down the named accountable role, or the owner was filled in with the person who happened to be in the room.

Fix: the owner is a named role with accountability: Head of Market Risk Reporting, Head of Vendor Risk Management, Head of Model Risk, BSA Officer, Chief Privacy Officer, Chief Compliance Officer. "Risk team" is not an owner; "Risk Director" is, even though the role exists across multiple individuals over time. The role outlives the incumbent; the issue follows the role.

## 8. MRA / MRIA classification missing on examiner-issued findings

Symptom: source_type is examiner-letter and the regulator is FRB, OCC, or FDIC, but the mra_mria_classification field is empty or set to n/a.

Why it happens: the practitioner does not know whether the regulator labelled the finding as MRA, MRIA, MRBA, or as a comment / suggestion.

Fix: read the supervisory letter or examination report for the explicit label. The federal banking supervisors are explicit in their letters; CFPB also uses the MRA label (with regulator field set to CFPB). For SEC EXAMS deficiency letters, FINRA findings, and state DOI findings, mra_mria_classification is set to n/a because those regulators do not use the MRA / MRIA framework. The schema enforces that examiner-letter source types name a regulator; the classification field should be populated when the regulator uses the framework.

## 9. Linked artifact IDs are missing

Symptom: linked_obligation_ids, linked_control_ids, and linked_evidence_ids are empty arrays.

Why it happens: the upstream `obligation-mapping`, `control-matrix`, and `evidence-binder` outputs were not consulted, or the linkage step was skipped.

Fix: each issue write-up should link to at least one obligation (the criterion the condition violates) and at least one control (the control whose design or operation weakness is the cause). Evidence IDs link to the evidence the source-test relied on. A standalone issue write-up that does not link to upstream artifacts is a stranded artifact; downstream consumers cannot pick it up by foreign key. If the upstream artifact does not yet exist, flag in the evidence-gap field and route to the engagement issue log.

## 10. Severity inflation on cyber-tagged issues

Symptom: a cyber-tagged finding with no identified customer-data exposure is rated critical or high without rationale support.

Why it happens: cyber issues attract reflexive high severity because cyber breaches have visible reputational tail.

Fix: cyber severity calibration overlays on the substantive calibration; it does not replace it. A logging gap on a non-production system with no customer data is moderate even though it is a cyber issue. The severity rationale must specify the cyber-specific weight (identifiable exposure, privileged-access scope, vulnerability dwell time, etc.). The cyber overlay's severity-calibration section is the reference; pull the specific weight, do not generalise.

## 11. Customer-harm severity deflation

Symptom: a UDAAP finding with population-level scope is rated moderate because the firm is uncomfortable with the harm framing.

Why it happens: identifying customer harm has restitution and supervisory implications; the practitioner under-weights the harm to keep the severity at a level the firm is more comfortable with.

Fix: severity calibration on customer-impact issues weighs the population, the pattern, and the reasonably-avoidable test. A UDAAP finding with identifiable systemic harm and restitution-eligible scope is high or critical. The conduct cross-cutting overlay's severity-calibration section is the reference; the severity rationale must specify the consumer-harm weight.

## 12. Closure evidence that closes the verb without closing the structural fix

Symptom: closure evidence names a manual workaround (the interim mitigation) as the primary closure evidence; the structural fix is deferred.

Why it happens: the manual workaround is in place and feels closure-shaped; the structural fix takes longer.

Fix: interim mitigation is named separately from closure evidence. The interim mitigation reduces residual risk while the structural fix is built; the structural fix is what the closure evidence inspects. An issue closed on interim mitigation alone reopens the next time the workaround lapses. Where remediation runs longer than 90 days, milestones are set; the closure evidence inspects the milestone artifacts.

## 13. The write-up tries to be the test workpaper, the binder, and the committee narrative

Symptom: the write-up runs to multiple pages of test sample listings, evidence file contents, and committee-pack-style executive summary.

Why it happens: the issue write-up gets stretched because adjacent skills' outputs are not yet built and the team puts everything in the issue as a stopgap.

Fix: the issue write-up lives downstream of `compliance-testing` (the test workpaper) and `evidence-binder` (the binder), and upstream of `risk-committee-pack` (the narrative). It carries the issue-level summary; the upstream artifacts carry the test depth and the evidence depth; the downstream artifact carries the committee narrative. Cross-references via `linked_evidence_ids`, `linked_control_ids`, and `linked_obligation_ids`. Pulling everything into the write-up breaks the contract with adjacent skills.

## 14. The write-up is signed off without an independent severity reviewer

Symptom: sign-off block names the practitioner who built the write-up and the owner accepting remediation; no independent severity reviewer is named.

Why it happens: smaller engagements compress the review machinery; the owner often functions as the de-facto severity reviewer because they are the most-named role in the room.

Fix: severity assignment always carries human review by a reviewer independent of the author. For 1.5-line-built write-ups, the 2-line function reviews. For 2-line-built write-ups, internal audit, the chief compliance officer, or an independent peer reviews. For advisory-built write-ups, the engagement partner reviews. The owner concurs with remediation accountability but is not the severity reviewer; an owner who rates the severity on their own issue fails the independence test.

## 15. The write-up stops too late

Symptom: the skill produces a write-up with severity asserted as final, status set to in-remediation, and closure evidence claimed as in-flight, without evidence.

Why it happens: builder over-runs the human-review gate.

Fix: the write-up is a draft until the named reviewer attests. The skill stops at draft and surfaces the reviewer questions; it does not assert sign-off, distribute, post to the GRC system, or move the status past under-review. The `human_review_required` field is always true; severity attestation is the named gate.
