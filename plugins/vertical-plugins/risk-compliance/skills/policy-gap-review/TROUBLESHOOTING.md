# Troubleshooting: policy-gap-review

Recurring failure modes when a policy gap matrix looks complete but is not. The reviewer pass should catch these; the builder pass should preempt them.

## 1. The matrix has no external benchmark

Symptom: the matrix is full of gap rows, but the benchmark sources block is empty or names only the firm's own policies and standards.

Why it happens: the scope did not pin down the external benchmark, or the practitioner anchored on the firm's own framework documents because they are easier to cite.

Fix: the matrix has at least one named, dated external benchmark with section references. Reviewing a policy against itself or against generic guidance fragments without anchored sources is internal-consistency editing, not a gap review. The schema enforces `benchmark_sources` with `minItems: 1` and `section_references` with `minItems: 1`. Pull the benchmark from `obligation-mapping` output, or name the rule and guidance directly with section refs from `references/source-anchors.md`.

## 2. Severity assigned without rationale

Symptom: every row carries a severity rating; rationale fields are blank, or read "high because high impact."

Why it happens: severity feels obvious to the practitioner who built the matrix; rationale feels redundant.

Fix: severity is paired with rationale referencing materiality (against firm thresholds where they exist), supervisory exposure (active examination scope, MRA/MRIA-eligibility, recent enforcement against similar weaknesses), customer impact, operational risk, and compensating practice. Severity without rationale is opinion. The schema enforces `severity_rationale` as required. A reviewer who cannot challenge a severity rating cannot attest it.

## 3. Recommended edit just restates the gap

Symptom: row's recommended edit reads "add language on AI systems" or "address vendor monitoring."

Why it happens: the gap is identified, the next step feels obvious, the practitioner does not write the next step.

Fix: the recommended edit is declarative and at least summary-drafted. "Add §X.4 stating that AI systems are within the model inventory, tiered by use-case impact, and require validation evidence proportionate to use-case impact" is a recommended edit. "Add language on AI systems" is not. The summary draft does not have to be the final wording (that is the policy author's job), but it has to be a starting point.

## 4. Gap classification collapses missing into partial

Symptom: row's policy-text field reads "policy is silent" but the classification is `partial`.

Why it happens: `partial` feels softer than `missing`, and the practitioner softens.

Fix: the five classifications are not interchangeable. `missing` is silence on the requirement. `partial` is addressing some of the requirement but stopping short. Conflating the two understates the gap and makes the recommended edit harder to scope. The schema does not enforce the distinction; the reviewer has to. A row whose policy-text reads "silent" is `missing`, not `partial`.

## 5. Evidence-needed empty on partial-or-worse rows

Symptom: rows classified `partial`, `weak`, `inconsistent`, or `outdated` have empty `evidence_needed` arrays.

Why it happens: the practitioner focuses on the text fix and forgets the operational dimension. The text edit feels like the whole story.

Fix: evidence-needed is mandatory on rows classified `partial`, `weak`, `inconsistent`, or `outdated`. The text fix alone rarely closes an operational gap; the matrix surfaces the operational dimension explicitly. Evidence needed names the standards updates, training, workflow changes, attestations, or system configuration the firm would inspect to confirm closure.

## 6. Coverage summary as percentage, no counts

Symptom: coverage summary reads "we cover most of the rule" or "approximately 70% covered."

Why it happens: the practitioner has a sense of coverage but did not enumerate the benchmark items.

Fix: coverage summary fields are integer counts. Total benchmark requirements in scope, covered items, partial items, missing items. Percentages are derived for the surface artifact; the structured record carries counts. A summary like "most of the rule is covered" without counts fails the matrix's audit-defensibility test. The schema enforces integer counts.

## 7. Owner is a department, not a role

Symptom: owner field reads "Compliance," "TPRM," "the policy team."

Why it happens: the engagement has not pinned down the named accountable role at the section level, and the department-level label feels right at the level of generality the matrix was drafted at.

Fix: owner is a named role with accountability: Head of Model Risk, Head of Vendor Management, Chief Privacy Officer, BSA Officer, Head of Consumer Compliance. Where the role taxonomy is firm-specific, it lives in `references/firm-overlay.md`. "Compliance" is not an owner; "Head of Compliance Operations" is.

## 8. Cross-policy interactions buried in commentary

Symptom: the matrix body has rich commentary on how the gap relates to other firm policies; the `cross_policy_interactions` array is empty.

Why it happens: the commentary feels like enough; the structured field feels redundant.

Fix: most material gaps interact with at least one other firm policy. Vendor policy and information-security policy on subcontractor depth. MRM policy and AI governance committee charter. BSA/AML and consumer-compliance on customer-onboarding flows. The interaction is named (`dependency`, `conflict`, `overlap`) and described in the structured record so the cross-policy fix can route to the right co-owner. Burying interactions in commentary breaks the firm's overall governance architecture.

## 9. Outdated misclassified as partial when the benchmark refreshed

Symptom: row policy-text references SR 11-7 with no acknowledgement of OCC Bulletin 2026-13, or references OCC 2013-29 with no acknowledgement of the June 2023 interagency guidance. Classification is `partial`.

Why it happens: the practitioner reads the policy as substantively addressing the topic, classifies as `partial`, and misses that the policy reflects an obsolete benchmark.

Fix: `outdated` is the classification when the policy reflects a prior edition of the benchmark that has since been refreshed. The recommended edit names the refreshed benchmark; the gap is not just about content, it is about the version the policy traces to. The June 2023 TPRM guidance and OCC Bulletin 2026-13 both create a wave of `outdated` rows in policies that have not been refreshed; the matrix should call them by name.

## 10. Out-of-scope items unwritten

Symptom: `out_of_scope_items` is empty. The matrix benchmarks against a rule with multiple exemptions, threshold-based provisions, or institution-type carve-outs, but does not name them.

Why it happens: the practitioner did not document the rationale for skipping benchmark items the firm does not cover.

Fix: out-of-scope items name the benchmark item the firm deliberately does not cover and the rationale (threshold not met, institution-type exemption, deferred effective date, explicit carve-out). This is an audit-defence artefact; reconstructed rationale is harder than written rationale. A regulator who asks "why didn't you address §X" is happier with "we did, here is the rationale" than with silence.

## 11. The matrix is signed off without independent reviewer

Symptom: sign-off block names the practitioner who built the matrix and the policy owner; no independent severity reviewer is named.

Why it happens: the engagement compresses the review machinery, especially when the practitioner is the policy owner.

Fix: severity assignment always carries human review, and the severity reviewer is independent of the author for severity attestation. For 1.5-line-built matrices, the 2-line function reviews severity. For 2-line-built matrices, internal audit or an independent peer reviews. The policy owner concurs on the recommended edits but the severity reviewer is a separate seat; a single name in both seats fails the independence test.

## 12. The matrix tries to be the policy redline

Symptom: recommended edits read as full draft text, with markup-style annotations, and the matrix begins to look like a marked-up policy.

Why it happens: the recommended edit feels easier to write at full draft length than at summary-draft length, and the practitioner over-runs the boundary with the policy rewrite.

Fix: this skill produces the gap list and summary-draft recommended edits. The redline lives in the policy-rewrite cycle (which the policy owner runs, or which `regulatory-change-management/policy-diff` tracks once two versions exist). Recommended edit is declarative and at summary-draft level; the policy author works it up to final wording. The matrix that reads as a redline has overrun the boundary.

## 13. Boundary with policy-diff is unclear

Symptom: the engagement has both an old version and a new version of the same policy and is asking this skill to compare them.

Why it happens: the boundary between policy-gap-review (policy vs benchmark) and policy-diff (version vs version) is not always intuitive.

Fix: this skill compares one policy to an external benchmark (rule, guidance, obligation register). `regulatory-change-management/policy-diff` compares two versions of the same policy. If the engagement has v3.4 and v4.0 of the same policy and wants to know what changed and whether the changes address the benchmark, run policy-diff first (what changed) and policy-gap-review second (does what changed close the gaps). Confusing the two leads to a matrix that reads as a poor redline rather than a gap inventory.

## 14. Linked obligation IDs fabricated when register did not yet carry them

Symptom: `linked_obligation_ids` array is populated with IDs that do not exist in the obligation register.

Why it happens: the practitioner assumed the obligation register would carry the obligation, drafted an ID, and moved on.

Fix: where the obligation register did not yet carry the obligation, the gap row leaves `linked_obligation_ids` empty and routes a back-reference into `obligation-mapping`. The register reopens for the section the gap surfaced. Fabricating an obligation ID breaks the cross-skill foreign-key contract and creates phantom rows downstream.

## 15. The skill stops too late

Symptom: the matrix is "signed off" with severity ratings asserted and recommended-edit approvals claimed, without independent attestation.

Why it happens: builder over-runs the human-review gate.

Fix: the matrix is a draft until the named reviewer attests. Severity assignment always carries human review. The skill stops at the draft and surfaces the reviewer questions; it does not assert severity sign-off, distribute the matrix to committee, or post recommended edits to the policy management system. The `human_review_required` field is always true.
