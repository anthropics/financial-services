---
name: issue-writeup
description: |
  Drafts a single issue write-up using the condition / criteria / cause / effect (CCCE) structure plus severity rationale, remediation, named owner, target date, closure evidence, and evidence-gap flag. Foundational primitive: exception-analysis chains it after a control-test exception, audit findings consume it as the issue artifact, regulator-response files cite it, and the issue log keys off it. The output is a one-issue artifact written in the shape an audit committee, regulator, or issue-tracking system will accept.

  Best for:
  - Drafting a finding from internal audit fieldwork, a compliance test exception, a vendor-monitoring exception, a model-validation finding, or a self-identified second-line observation.
  - Translating an MRA, MRIA, FINRA Letter of Caution, SEC EXAMS deficiency, NYDFS finding, or examiner-issued matter into the firm's internal issue format with traced criteria.
  - Re-papering a legacy issue whose criteria, cause, or closure evidence does not stand up to current review.

  Not the right tool when:
  - The work is the test that produced the exception. Use `compliance-testing/skills/workpaper-drafter`; the issue is downstream.
  - The work is a multi-issue summary or committee narrative. Assemble several issue-writeup outputs and use `risk-reporting/skills/risk-committee-pack`.
  - The condition is unconfirmed (an observation, not a finding). Issues require a confirmed condition; observations belong in the engagement notes until confirmed.
  - The work is policy-level gap analysis upstream of any specific exception. Use `policy-gap-review`.
argument-hint: "[exception or finding source: control-test workpaper, exam letter, vendor monitoring record, validation report, audit fieldwork note]"
---

# Issue write-up

A second-line issue is the artifact that turns a confirmed exception into something the firm tracks, owns, remediates, and answers for. The shape is old: condition, criteria, cause, effect, recommendation. Internal audit has used it since the IIA standardised the communication-of-results convention. AICPA AU-C 265 carries the same frame for financial-statement-related internal control matters. Federal supervisors lean on it whenever a matter requiring attention or matter requiring immediate attention lands in a supervisory letter. The reader on the other side of the artifact, whether audit committee, regulator, or remediation owner, expects to read it in that order, with severity, owner, and target date attached.

The issue write-up is a primitive. The exception-analysis chain calls it once a control-test exception is confirmed. Internal audit calls it as the deliverable shape for fieldwork findings. Vendor monitoring calls it when a SOC report or KPI threshold is breached. Model validation calls it for findings that warrant tracking outside the validation report. Regulator-response files call it when the firm restates an examiner-issued matter in its internal format. The artifact shape is the same; the source label, the severity calibration, and the reviewer machinery shift with the source.

The write-up is the deliverable; the format is whatever the engagement and audience need. An audit-committee read or regulator-response file is memo-natural and lands as Word; an internal remediation tracker may want formatted markdown that ports cleanly into a GRC platform. The skill drafts against `templates/default-output.md` and emits the structured record at `schemas/issue.schema.json`. The artifact is a draft until a named reviewer signs off; severity assignment always carries independent attestation.

## Ask first

A few facts settle before drafting. Most of them are on the table by the time someone is writing up an issue, but the discipline is to name them.

- What confirmed the condition. A test result with a sample, a failed reconciliation, a vendor SOC report opinion, an examiner letter, a self-disclosure. The source decides the source label, the severity ladder, and which reviewers attest. An unconfirmed observation is not yet an issue; it sits in engagement notes until the condition is confirmed.
- What rule, principle, standard, or policy the condition violates. Criteria is a named source with a section, not a generic "per firm policy". If the criterion is the firm's own policy, name the policy version and section; if the criterion is regulatory, name the rule and section and reference `references/source-anchors.md` or a sector-overlay file by path.
- What the source posture allows in the artifact. Public-only sets the ceiling at obligation, control objective, and observable condition; firm-policy-overlay or mixed lets named owners, system-of-record names, dollar amounts, and last-test results land in the body. Confidential-supervisory content (open MRA detail, MRIA scope, regulator correspondence) does not land in any artifact that will read at a lower posture.
- Who owns remediation, in role terms. The owner is the role accountable for closing the issue, not the team that found it. Where the role taxonomy is firm-specific, it lives in `references/firm-overlay.md`.
- Whether the issue source is an examiner letter. If yes, the MRA / MRIA classification field is populated and the closure-evidence framing matches the regulator's expected response register.

When `scope` is supplied, the skill consumes it for institution, persona, source posture, sector overlay, and cross-cutting overlay. Otherwise it asks the questions above and defaults to public posture if the practitioner declines. The artifact notes scope was not formalised; it does not silently assume.

## How the write-up gets built

The write-up has the same spine across sources. A senior practitioner builds it roughly in CCCE order, but the conversation surfaces the parts in whatever order the underlying work produced them; the structured record sorts itself.

The header opens with the issue identifier, title, source, date identified, period covered, and source posture. The source block names the source type (internal-audit, compliance-testing, vendor-monitoring, model-validation, examiner-letter, self-identified, whistleblower, other), the source identifier (audit engagement ID, exam letter ID, control-test workpaper ID, vendor monitoring record ID, validation report ID), and the regulator if the source is examiner-issued.

The body is the CCCE structure plus severity:

- **Condition.** The dated, scoped, observable state. Specific. "On three monthly reporting cycles between 2026-01 and 2026-03, two material counterparty exposures totalling $[amount] were excluded from the consolidated market-risk view because the upstream feed cutoff time preceded the source-system close." That is a condition. "The control failed" is not a condition; it is a conclusion. "Vendor oversight is weak" is not a condition; it is commentary.
- **Criteria.** The standard, rule, principle, or policy the condition is measured against, with a named source and section. A risk-reporting criterion lands as a named BCBS 239 principle; a third-party criterion as a named lifecycle phase from the interagency TPRM guidance; a state-cyber criterion as a named section of the relevant rule; a firm-policy criterion as the policy version and section. Granular cites live in `references/source-anchors.md` and the overlays. "Per firm policy" without a citation is not criteria; it is a placeholder.
- **Cause.** The root cause, tied to a specific control design or operation weakness. The feed-orchestration cutoff time is a cause; "human error" is not. A missing reviewer in the SOC-report-review workflow is a cause; "lack of training" usually is not. A control designed to fire only on a complete population that quietly drops short-population runs is a cause; "system limitation" is not. The cause names the control attribute that failed. Where root cause is genuinely unknown at write-up time, the field reads "root cause analysis pending" and the issue carries an open action to determine it; do not invent a cause to fill the field.
- **Effect.** The impact, quantified where possible. Financial (dollar amount, counterparty exposure, capital impact). Customer (number of customers affected, harm pattern, restitution scope). Regulatory (exam consequence, supervisory letter exposure, filing implication). Operational (process disruption, downstream pack impact). Reputational (where the issue is genuinely public-facing, not where the team is uncomfortable). The effect carries the unit and the time window. "Significant impact" is not an effect; "$X under-stated counterparty exposure on three cycles, propagated into the executive risk pack distributed to the board risk committee" is.
- **Severity.** Low, moderate, high, or critical. The severity field is paired with `severity_rationale` because severity without rationale is a number, not a finding. Rationale references materiality (against the firm's published thresholds where they exist), frequency (one-off, intermittent, recurring), customer impact (none, identifiable, quantified harm), regulatory exposure (no exam reference, ongoing exam scope, MRA / MRIA-eligible), and any compensating controls already in place. Severity is the field examiners and the audit committee key off; it always carries human review.

The remediation block names the recommended action in declarative voice (what the owner must do), the named role owner, the target date, the closure evidence the firm will inspect to confirm closure, and any interim mitigation in flight. The closure-evidence field is the artifact, not the verb. "Remediated" is not closure evidence; "two consecutive months of reconciled feed output reviewed by the Head of Market Risk Reporting with sign-off log retained in the GRC platform" is. Interim mitigation lives separately because it is not closure; a manual workaround keeps risk down while the structural fix is built.

Population and sample go in their own block when the issue arose from a sample-based test. Population size, sample size, exceptions observed, and projected exception rate where the firm projects. The population details support whoever has to defend the severity rating to a reviewer or a regulator.

Linked obligations, controls, and evidence go in their own block as foreign keys into `obligation-mapping`, `control-matrix`, and `evidence-binder` outputs. A finding without these links is a stranded artifact that downstream skills cannot consume.

The tail of the artifact carries the evidence-gap flag (yes / no with a one-line note), reviewer questions tied to specific elements of the CCCE rather than generic prompts, the source trace block citing `references/source-anchors.md` or the loaded overlays by path, and the sign-off block. `[evidence needed]` flags route to the engagement issue log rather than living silent in the body.

### Sector and cross-cutting overlays

The same CCCE spine carries different criteria sources, different severity calibrations, and different reviewer machinery across sectors and cross-cutting topics. Load only the overlays the scope flags. The MRA / MRIA labelling is banking-specific; insurance, capital-markets, and payments-fintech each carry their own finding-format conventions, so do not reach for MRA / MRIA when the source is, say, an SEC EXAMS deficiency letter.

- `references/sector-overlays/banking.md` carries the OCC / FRB / FDIC supervisory-finding framework (MRA, MRIA, MRBA) and large-bank heightened-standards severity flavour for federally regulated banks.
- `references/sector-overlays/insurance.md` carries the NAIC examination-findings format, state DOI MOU and consent-agreement language, and ORSA-driven enterprise-risk severity shading for insurer issues.
- `references/sector-overlays/capital-markets.md` carries the SEC EXAMS deficiency-letter format, FINRA Letter of Caution and examination-finding shape, and broker-dealer / investment-adviser remediation conventions.
- `references/sector-overlays/payments-fintech.md` carries OCC bank-fintech supervisory-letter conventions, CFPB UDAAP recommendation patterns, and money-transmitter state-by-state remediation flavour.
- `references/cross-cutting/cyber.md` is the most-loaded cross-cutting overlay. State cyber finding patterns, FFIEC IT conventions, SEC public-company disclosure-process patterns, and customer-information incident-notification severity shading land here. The overlay fires whenever the underlying condition touches information-security controls, which is most issues in practice.
- `references/cross-cutting/conduct.md` loads when the issue concerns customer-facing harm. UDAAP severity shifts when customer harm is identifiable; restitution scope drives the closure evidence.

Privacy and climate overlays follow the same pattern; this skill ships cyber and conduct because they are the most frequent triggers. Granular citations (specific section labels, rule numbers) live in `references/source-anchors.md` and the overlay files. Where firm policy or taxonomy applies (issue-rating ladders specific to the firm, named committee gates, GRC-platform status enums), it lives in `references/firm-overlay.md`.

## Quality bar

The condition is dated, scoped, and observable. A condition that reads as a conclusion or as commentary is not yet a condition; the write-up does not proceed until the condition is stated as the observable state.

Criteria is a named source with a section. Generic policy references without citation are not criteria. The reviewer must be able to read the criterion in `references/source-anchors.md`, in a loaded overlay, or in the firm-overlay.

Cause names the control attribute that failed. "Human error," "training gap," and "system limitation" are surface labels; the cause field reads as the design or operation weakness underneath.

Severity is paired with rationale referencing materiality, frequency, customer impact, regulatory exposure, and compensating controls. Severity assignment always carries independent attestation.

Closure evidence is the artifact, not the verb. The reviewer can name the system, the report, or the sign-off log they will inspect to confirm closure.

Owners are named roles with accountability. Where the role taxonomy is firm-specific, it comes from `references/firm-overlay.md`.

Issues sourced from examiner letters carry the MRA / MRIA classification field populated.

Material claims cite a source. `[evidence needed]` flags route to the engagement issue log; the seams between source evidence, management assertion, public-source obligation, and inference stay visible. RFP narrative is not evidence. `[verify section]` markers belong in source-anchors verification, not the write-up body.

No named institutions in narrative unless they are public defendants in a finalised enforcement action with a published consent order. The artifact stops at recommendation; it is a draft until the named reviewer signs off.

## Adaptation

Audience drives compression: an audit-committee read pulls severity, recommendation, and target date to the front; a regulator-response read leads with criteria and condition; an internal remediation tracker pulls owner and closure evidence forward. Source posture drives what the body can carry. Sector and cross-cutting overlays load from the scope. The CCCE order itself can rearrange in the surface artifact (a regulator response often opens with criteria; an internal pack often opens with severity and recommendation), but the structured record preserves the CCCE fields distinctly.

## Output

Default to drafting against `templates/default-output.md`. The write-up is memo-natural in practice; render the deliverable as Word via the `docx` skill in the `document-skills` plugin, or as formatted markdown that ports into a GRC platform. PowerPoint for an audit-committee summary slide, Excel for the structured row when the firm's issue log is spreadsheet-driven. Render to whatever the audience and workflow ask for. Produce the structured record at `schemas/issue.schema.json` when downstream automation or a registered consumer needs it.

Downstream consumers: the exception-analysis chain reads `issue_id`, `severity`, `linked_control_ids`, and `linked_evidence_ids` to ladder exceptions into the testing program; audit findings reference `issue_id` as the matter under audit; regulator-response files cite `issue_id` and the criteria block when responding to an examiner letter; the issue log keys off `issue_id`, `status`, `target_date`, and `owner`; `risk-committee-pack` aggregates `severity`, `mra_mria_classification`, and `evidence_gap` for the open-issues section; `control-matrix` reads `linked_control_ids` to surface open issues against rows. The schema is the cross-skill contract; additive changes only, never silent renames. Breaking changes ship as a versioned migration with downstream skills told in advance.

## Pointers

- `references/source-anchors.md` — citations and excerpts for the named anchors.
- `references/sector-overlays/{banking,insurance,capital-markets,payments-fintech}.md` — sector overlays loaded from scope.
- `references/cross-cutting/{cyber,conduct}.md` — cross-cutting overlays loaded when the issue touches information-security controls or customer-facing harm.
- `references/firm-overlay.md` — firm-installed taxonomy, named role labels, severity-rating ladder, GRC-platform status enums, named committee gates beyond the regulatory baseline; consumed when present.
- `templates/default-output.md` — write-up template.
- `schemas/issue.schema.json` — structured-output contract (plugin-level; shared with downstream skills).
- `examples/` — BCBS 239 risk-reporting completeness exception (internal audit source); TPRM critical-vendor SOC 2 qualified-opinion finding (vendor monitoring source).
- `TROUBLESHOOTING.md` — recurring defects in issue write-ups.
