# Troubleshooting: obligation-mapping

The obligation register is a foundational primitive: control-matrix, policy-gap-review, evidence-binder, exam-brief, and issue-writeup all read it. Defects in the register propagate downstream. This file walks the recurring defects and how to resolve them.

## 1. The source is a bare URL with no section reference

**Symptom**: A row's source citation is `https://www.federalreserve.gov/...` with no §, paragraph, article, or chapter. Downstream, control-matrix cannot anchor a control to it; exam-brief cannot answer "what part of the rule says this."

**Why it happens**: The practitioner pasted the rule's URL and moved on. Or the source is a long supervisory letter and the section feels like overhead.

**Resolution**:
- The source-citation column carries both URL and section. Mandatory.
- Where the section is genuinely unknown, the row carries `[verify section]`. The placeholder is a deliberate flag, picked up by the open-question summary, never silent.
- For exam manuals and supervisory letters, the section is usually a chapter or numbered subsection name; cite it as the source uses it.
- For SLAs and contracts, the section is the clause number. "§4.2(c)" is a citation; the contract title alone is not.

## 2. The requirement summary paraphrases away the substance

**Symptom**: A row reads "Firm must do CDD" or "Firm must have appropriate controls." Downstream, control-matrix cannot tell what the obligation actually requires.

**Why it happens**: The practitioner extracted the rule at headline level rather than at substance level. Or the rule was long and summary-fatigue set in.

**Resolution**:
- The summary states what specifically must be done and on whom. "The bank must obtain and verify the identity of each beneficial owner of a legal-entity customer at account opening" preserves substance. "Firm must do CDD" does not.
- Preserve the operative verb (must, shall, should, will). The strength of the obligation is in the verb.
- Preserve the operative object (each customer; each covered application; each material model change). Without the object, the obligation does not bind.
- One sentence is the target, but two sentences for compound obligations is fine. The constraint is substance, not length.

## 3. Applicability is "all operations"

**Symptom**: Multiple rows carry an applicability column reading "all operations," "the firm," or "every business unit." Downstream skills cannot tell which processes the obligation actually binds.

**Why it happens**: The rule applies broadly within the firm and the practitioner used a shorthand. Or the rule's applicability language was vague and the practitioner did not pin it down.

**Resolution**:
- Applicability names institution type, product, activity, geography, and threshold where the source defines them. Where the source does not, applicability says the source did not specify.
- For tier-dependent rules (1071 by origination volume, NYDFS Part 500 by covered-entity tier, DORA by significance class, Heightened Standards by asset size), capture the threshold and the firm's tier.
- "All operations" is the symptom of unfinished extraction. The rule almost always names a scope (a covered institution, a covered product, a covered activity); the row reflects that.
- For internal-policy sources, applicability is what the policy itself says, not what the practitioner thinks the policy ought to mean.

## 4. Owner is a department or a collective noun

**Symptom**: Owner column reads "Compliance," "Operations," "the team," or "Risk." Downstream, evidence-binder cannot route an evidence ask, and the human-review gate has no addressee.

**Why it happens**: The role taxonomy was unclear. Or the firm uses a department label as a shorthand for the accountable role.

**Resolution**:
- Owner is a named role with accountability. BSA Officer, Head of Vendor Management, Chief Privacy Officer, Head of Model Risk, ECOA officer, fund CCO, head of credit risk reporting.
- For firm-specific role labels (e.g., "Director, Enterprise Compliance Operations"), the role lives in `references/firm-overlay.md` and the register pulls from there.
- Where two roles share accountability (operational owner and regulatorily accountable owner in a sponsor-bank relationship), the column captures both with the relationship: "Fintech BSA Lead (operational); sponsor bank BSA Officer (regulatory accountability)."
- A row with no clear owner is a row that is not yet complete; flag it as `open-question` rather than ship with a department label.

## 5. Status pre-decided as approved

**Symptom**: Rows enter the register with `status: approved` directly from extraction.

**Why it happens**: The practitioner treated the extraction as a one-step process. Or the firm's existing register marked rows approved and the refresh inherited the value without re-review.

**Resolution**:
- Status enters at `draft` or `open-question`. Always.
- `approved` is reserved for rows the named reviewer has signed off on. The skill does not set that value itself; the human review gate does.
- For refreshes, inherited statuses are revisited where the source has changed; otherwise the refresh log notes that the prior status carries forward unless the refresh changed substance.
- `not-applicable` is a legitimate value with rationale; it is not a way to mark something approved-by-not-mattering.

## 6. The register mixes rule and firm policy without anchor

**Symptom**: Rows whose only source is the firm's own policy, with no external rule, supervisory guidance, or contract underneath.

**Why it happens**: The firm's policy library is comprehensive and the practitioner extracted at policy level. The output reads like a policy index rather than an obligation register.

**Resolution**:
- The register is rule-anchored. Internal policy can be a source on a row that also cites an external rule, supervisory guidance, or contract.
- Rows with policy-only sources belong in `policy-gap-review`'s output, not here. The register asks "what does the firm have to do"; the policy library captures "what the firm says it does about it."
- Where the firm has a policy that goes beyond the regulatory baseline (a self-imposed standard), that lives in the firm-overlay and surfaces as a control choice in `control-matrix`, not as an obligation row.

## 7. Open questions disappear into the row

**Symptom**: Rows carry `status: open-question` but the open-question summary at the tail of the artifact is empty or generic.

**Why it happens**: The practitioner captured the question in the row but did not aggregate it. Downstream legal review has nothing to route against.

**Resolution**:
- The open-question summary is grouped by reviewer (legal, compliance, function head, sponsor). Every `open-question` row appears in exactly one group.
- Each summary entry names the obligation IDs it covers, the question, the reviewer, and the target resolution date.
- A row whose status is `open-question` but whose question is not in the summary is a defect; the summary is the routing artifact, the row is the working content.

## 8. Confidence label as a single overall value

**Symptom**: The artifact carries one confidence label ("medium") without per-section detail. Downstream, exam-brief cannot tell which rows are pressure-test ready and which are interpretive.

**Why it happens**: The practitioner treated confidence as a summary judgment rather than a per-section discipline.

**Resolution**:
- Confidence tracks by section in the source-trace block, not as a single overall label. Most registers have high-confidence rows (unambiguous source) and low-confidence rows (interpretation involved or single secondary source) side by side.
- Per-row confidence on each obligation is also useful and supported by the schema (`obligation.confidence`).
- The overall `confidence_label` on the register is allowed to be `mixed` and usually is.

## 9. Effective dates with phase-in collapsed

**Symptom**: A row with a tiered effective date (1071 by volume tier, DORA by entity class, climate disclosure rules with phased-in scope) carries a single date and loses the phase-in.

**Why it happens**: The rule's phase-in language is dense and the practitioner picked the date that applied to the firm without flagging the broader schedule.

**Resolution**:
- `effective_date_phase_in` captures phase-in stages. The applicable-to-firm date sits in `effective_date`; the broader schedule sits in the phase-in field.
- Where the effective date is contingent (rule subject to litigation, guidance subject to revision, sunset awaiting reauthorisation), the row notes the contingency.
- Compliance-date schedules that the firm has not yet hit but will hit are still flagged so the firm sees them coming.

## 10. The register is built without scope

**Symptom**: Multiple registers across engagements use inconsistent jurisdiction labels, persona vocabulary, and overlay choices. Downstream skills load the wrong overlays or the wrong taxonomy.

**Why it happens**: The skill was invoked without an scope record on file, the practitioner declined the four scoping questions, and the defaults set the wrong tone.

**Resolution**:
- When `scope` is supplied, consume it. Sector overlays, cross-cutting overlays, persona, source posture, jurisdiction all key off the scope record.
- When it is not supplied, ask the four questions. If the practitioner declines, default to public posture and note in the artifact that scope was not formalised.
- For a firm running many registers, the scope record is what keeps them coherent across functions.
