# Troubleshooting: human-review-gates

Recurring failure modes when a gate matrix looks complete but is not. The reviewer pass should catch these; the builder pass should preempt them.

## 1. One committee owns everything

Symptom: the same committee owns intake, tiering, pre-prod, go-live, ongoing monitoring, and retirement. The decision-authority block reads as a single committee with no escalation path.

Why it happens: the firm has not yet stood up the differentiated governance the source guidance assumes. Smaller firms run with one committee out of pragmatism; larger firms accumulate gates onto an existing committee without splitting.

Fix: a single committee owning the full lifecycle is one committee, not a gate matrix. The matrix's `gate_gaps` section flags this with the specific source-guidance citation that implies separation (Heightened Standards Standard II for line-1/line-2 separation; SR 11-7 §V/§VI for developer/validator separation; Interagency TPRM §III for TPRM-lifecycle differentiation). The recommended action either splits the committee, names sub-committees with charter clarity, or defines an escalation path through which one committee's decisions are reviewed by another. One committee is acceptable when the firm's scale genuinely fits it; one committee with no escalation is not.

## 2. Stop conditions that are not stops

Symptom: stop conditions read "should be reviewed", "consider whether", "as appropriate", or "review for completeness". The gate's decision criteria are advisory rather than declarative.

Why it happens: the practitioner is uncomfortable with binary stops because real production decisions involve judgement, and writing a binary stop feels rigid.

Fix: stop conditions are declarative and binary. "No go-live if any open critical or high issue against the use case" is a stop. "Should be reviewed for open issues" is not. The gate's decision criteria carry the judgement (the criteria are evaluated by the named reviewers); the stop conditions are the binary blockers that fire when criteria fail. If the gate genuinely has no binary stops, the gate is advisory, not gating; the matrix's gap section flags this and recommends adding declarative stops.

## 3. Required reviewers are committees, not roles

Symptom: required_reviewers reads "Risk Committee", "Compliance Function", or "Senior Management" without naming individual roles.

Why it happens: the engagement has not yet specified which named roles within the committee carry the decision; the practitioner writes the committee name as a placeholder.

Fix: the required reviewers are named roles. "Head of Model Risk Management", "Independent Validator", "CISO", "Chief Compliance Officer", "Business Sponsor", "General Counsel". Where the gate is a committee-level decision (the AI Governance Committee renders the T1 go-live decision), the matrix can name the committee as the decision authority but still name the required individual roles whose attestation forms the committee record. Pure committee-named reviewers without role-named members fail the audit-trace test; an examiner cannot tell who attested.

## 4. Independence flag missing where source guidance demands it

Symptom: a model-risk gate has no `independence_required` flag on the validator slot; a third-party gate has no independence flag on the line-2 reviewer; an audit-committee gate has no independence flag on the audit committee.

Why it happens: the matrix builder did not yet pull the source-anchor file into the construction; independence is a per-reviewer attribute that is easy to miss at first pass.

Fix: every gate's required_reviewers list is reviewed against the source anchor. SR 11-7 §V demands validation independence from development. Interagency TPRM §III.B demands line-2 independence on critical-vendor due diligence. EU AI Act Article 14 demands competent oversight by persons with authority. NAIC Model Audit Rule demands audit committee member independence. Where the source guidance demands independence, the `independence_required` field is true and `independence_basis` cites the source. The check is mechanical; the source-anchors file enumerates the demands.

## 5. Required inputs read as "what is available"

Symptom: required_inputs reads "review what's available", "current state of the artifact", or "any relevant documentation".

Why it happens: the matrix builder is uncertain what artifacts will be available at the gate, or wants to leave room for flexibility.

Fix: required inputs are named artifacts, by ID where the artifact is a structured record produced by a sibling skill (model card from `model-card-builder`, validation report from `validation-report` or model-validator equivalent, due-diligence pack from `vendor-diligence`, issue write-up from `issue-writeup`, exit plan from `exit-plan`). Where the artifact is a regulatory deliverable, name the deliverable (SOC 2 Type II report, attestation letter, supervisor-correspondence record). Flexibility is fine on the artifact's content; the gate is firm on its presence.

## 6. Documentation requirement reads as "minutes"

Symptom: documentation_requirement reads "minutes" or "noted" without naming what gets captured.

Why it happens: minute-taking discipline varies; the matrix builder is unsure what the firm's minutes actually carry.

Fix: documentation requirement names what gets captured: the decision (pass / fail / conditional), the rationale, the named attesters, the date, the artifact references, and the system of record that holds the record. "Minutes" is acceptable when the firm's minute discipline is robust and the minutes name attesters and decisions; it is not acceptable when the minutes are summary-only. The matrix's documentation requirement carries the granularity needed for the named system of record (board portal, GRC platform, regulator filing). For board-committee gates, named attesters and recorded dissents are explicit; for line-2 committee gates, the GRC-platform record is named.

## 7. Frequency conflated with cadence

Symptom: frequency is set to "annual" but the gate is actually event-based (fires when a use case reaches that lifecycle stage); or frequency is "event-based" but the gate is actually periodic (fires on a calendar regardless of use cases moving through the workflow).

Why it happens: practitioners conflate the gate's firing pattern with the gate's review cadence.

Fix: frequency is event-based or periodic, with the periodic gate naming the cadence (daily, weekly, monthly, quarterly, annual). A gate that fires on go-live is event-based; a gate that fires on the annual review cycle for in-production use cases is annual. Some workflows have both: a use case has an event-based pre-prod gate (fires once when the use case is ready) and an annual review gate (fires every year while the use case is in production). The matrix carries them as two distinct gates with distinct frequencies.

## 8. Recommended charter language reads as matrix commentary

Symptom: the recommended_charter_language section is a bulleted list of gate-matrix observations rather than charter prose.

Why it happens: the matrix builder uses the same voice for the matrix and the charter language; the charter is a different artifact with a different audience.

Fix: charter language reads as committee charter prose: declarative, named, committee-voice. Three paragraphs typically: (1) the committee's purpose and decision authority; (2) the gate sequence and stop-condition discipline; (3) the escalation, dissent, documentation, and reporting cadence. The charter language is the language the committee adopts; the matrix is the operational reference. Voice shift; not a copy of the matrix bullets.

## 9. Gap section is empty

Symptom: gate_gaps is an empty array.

Why it happens: the matrix builder has not stress-tested the matrix against the source-guidance expectations, or has buried gaps in narrative commentary.

Fix: a clean-looking matrix with no gaps usually means the gaps were buried. Stress-test the matrix: does every source-guidance gate have a corresponding matrix gate? Does every reviewer-independence demand have a flag? Does every gate have stop conditions? Does the workflow have an annual-review gate where the source guidance implies one? Does the workflow have a termination / exit gate where the source guidance demands one? The gap section names the implied gates that are missing or under-specified; if the gap section is empty after stress-testing, it stays empty, but the test should run.

## 10. Validator-as-developer (or equivalent) buried in role overlap

Symptom: the matrix names "Independent Validator" as a required reviewer but the firm's actual organizational structure has the validator role reporting to the developer's chain.

Why it happens: the matrix is constructed against the source guidance without reconciling against the firm's current role assignments. The gate matrix says "independent validator"; the firm's reality is that the only validator is in the development team.

Fix: the matrix names independence as a structural requirement; the gap section flags any current organizational reality that fails the requirement. SR 11-7 demands developer/validator independence; if the firm's current state does not satisfy this, the gate is gating on a fiction. The matrix surfaces the structural-independence gap, recommends a structural fix (separate validator role, third-party validation, or escalation to model-risk function outside development), and notes that the gate is not yet operationally enforceable until the structural gap closes.

## 11. SAR / regulator-filing gates without BSA Officer or compliance-officer attestation

Symptom: a SAR-filing gate or regulator-filing gate names a committee or general role as the decision-holder without naming the BSA Officer (for SAR) or the named compliance officer (for other regulator filings) as the attester.

Why it happens: SAR and regulator-filing gates often inherit a generic "compliance approval" framing rather than naming the regulatory-officer-of-record.

Fix: SAR-filing gates name the BSA Officer as the attester (FinCEN BSA program-officer requirement). Regulator-filing gates name the compliance officer or general counsel of record. The decision criteria reference the BSA Officer's attestation as the regulator-recognised sign-off. The documentation requirement names the SAR record, the BSA Officer attestation, and the FinCEN filing record.

## 12. The matrix tries to be the runbook

Symptom: the matrix runs to many pages of process detail (how the gate fires operationally, who hands off to whom, what the screen-share looks like in the meeting).

Why it happens: the matrix builder is documenting the gate as a process rather than as a decision architecture.

Fix: the matrix is the gate-decision architecture. The runbook is downstream, the operational documentation that names how the gate fires day-to-day. The matrix names the gate, the trigger, the reviewers, the criteria, the stop conditions, the escalation, the documentation, the frequency, the source. The runbook (or the firm's GRC platform workflow) carries the operational detail. Cross-reference the runbook in the firm-overlay; do not pull the runbook into the matrix.

## 13. The matrix stops too late

Symptom: the skill produces a matrix asserting committee adoption, charter language signed off, and decision authority finalized, without the named reviewer having attested.

Why it happens: builder over-runs the human-review gate.

Fix: gate architecture is committee-adopted; the skill stops at draft. The matrix is a draft until the named reviewer attests. The `human_review_required` field is always true; committee adoption is the named gate (the gate matrix's own meta-gate). The skill surfaces reviewer questions and recommended charter language; it does not assert sign-off, distribute, or post the matrix as adopted.
