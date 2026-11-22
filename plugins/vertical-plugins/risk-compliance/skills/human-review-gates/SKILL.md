---
name: human-review-gates
description: |
  Builds the named-gate matrix for an artifact, decision, or workflow: gate name, stage in workflow, trigger, required reviewers (with independence), required inputs, decision criteria, stop conditions, escalation path, documentation requirement, frequency, and source anchor. Foundational primitive: every output-builder skill in the repo emits an artifact that runs through one or more of these gates, and the skill exists so the gates themselves get built once and reused. Output is a gate matrix plus a one-page narrative an AI governance committee, vendor onboarding committee, model risk committee, or issue-rating committee can adopt as charter language.

  Best for:
  - Standing up a new committee or governance gate (AI use-case approval, vendor onboarding, model release, issue rating, customer-impact action, SAR filing approval, regulator-response sign-off).
  - Auditing an existing workflow for missing or under-specified human-review gates ahead of an exam, an internal audit, or a Heightened-Standards readiness review.
  - Translating a regulator-driven oversight expectation (SR 11-7 effective challenge, OCC Heightened Standards three-lines-of-defense, EU AI Act human oversight, NIST AI RMF Govern function) into firm-specific gate architecture.

  Not the right tool when:
  - The work is the per-instance approval memo for a specific decision (gates define the recurring review structure; the per-instance memo is downstream of the gate).
  - The work is a control matrix for a process (use `control-matrix`; gates are a subset of controls but reviewed differently because the gate decision is itself the control).
  - The work is the underlying artifact being gated (use `issue-writeup`, `model-card-builder`, `vendor-diligence`, etc.).
  - The work is committee-meeting administration (agenda, minutes, action tracking) — that is a secretariat function, not a gate-architecture skill.
argument-hint: "[workflow or artifact in scope; e.g., 'AI use-case lifecycle for tier-1 retail credit', 'critical-vendor onboarding', 'issue-rating committee charter refresh']"
---

# Human review gates

A human-review gate is the named, role-anchored decision point where a workflow stops, a qualified reviewer reads what is in front of them, and the workflow proceeds, returns, or escalates based on stated criteria. Effective challenge in model risk. Human oversight under the EU AI Act. Govern under the NIST AI RMF. Three-lines-of-defense separation under the OCC's heightened-standards framing for large banks. Different framings, same artifact: a gate that names who decides, against what criteria, on what evidence, with what stop conditions, with what escalation, captured in what record.

The gate matrix is a primitive. Every output-builder skill in the repo names a sign-off block; this skill defines the review gates those sign-offs route through. Standing up an AI governance committee, refreshing a vendor onboarding workflow, separating model-development from model-validation, putting a customer-impact action behind a CCO sign-off, opening an issue-rating committee — each is a gate-matrix problem. The artifact reads as charter language for the committee that adopts it; the structured record feeds the firm's GRC platform.

Proportionality is part of the design, not a footnote. A tier-1 customer-impact AI use case earns committee machinery; a low-risk internal-productivity tool does not. Match the gate set to the artifact's risk: high-risk and high-impact decisions get full reviewer panels with independence and escalation; low-risk artifacts run through a lighter named-role check, sometimes a single reviewer with the authority to escalate. The matrix calls out which tier each gate fires for, so committee-level machinery does not get inherited by every workflow that mentions oversight.

The skill produces a matrix in `templates/default-output.md` shape and a structured record conforming to `schemas/review-gate-matrix.schema.json`. The artifact is a draft until a named reviewer attests; gate architecture itself is the kind of artifact a board risk committee or audit committee adopts, and the skill stops at draft.

## Ask first

A handful of facts settle before drafting. Most of them are on the table by the time someone is naming gates, but the discipline is to name them.

- What workflow, artifact, or decision is being gated. AI use-case lifecycle, vendor onboarding lifecycle, model lifecycle, issue lifecycle, customer-impact action, SAR filing, regulator-response sign-off, change-management gate. Scope tight; "the governance program" produces a matrix nobody can adopt.
- Who has decision authority. The primary committee (the body that pass / fails the gate), the escalation committee (where a no-pass routes), the dissent path (how an individual reviewer's challenge gets recorded and adjudicated). Without a named decision authority, the matrix reads as suggestion.
- What source posture the engagement runs at. Public-only sets the ceiling at named-role and decision-criteria description. Firm-policy-overlay or mixed lets named committees, internal-policy section references, GRC-platform record names, and committee charter references land in the body.
- Whether independence is regulatorily required, advisory, or absent. SR 11-7 demands validation independence from development. Interagency TPRM expects line-1 vs. line-2 separation on critical-vendor decisions. EU AI Act Article 14 expects human oversight by persons with the competence, authority, and resources to fulfil it. The matrix captures independence as a per-reviewer attribute, not a global one.
- Whether the engagement is standing up a new gate set or auditing an existing workflow. New gate set is a green-field design from the source guidance; audit of an existing workflow surfaces under-specified gates, missing independence, stop conditions that are not stops, and decision criteria that are not criteria.

When `scope` is supplied, the skill consumes it for institution, persona, source posture, sector overlay, and cross-cutting overlay. Otherwise it asks the questions above and defaults to public posture if the practitioner declines. The matrix notes scope was not formalised; it does not silently assume.

## How the matrix gets built

The matrix has the same spine across workflows. A senior practitioner builds it in roughly the order below, but the conversation surfaces gates in whatever order the workflow shows up; the structured record sorts itself.

The frame opens with the workflow in scope, the decision authority hierarchy, and the source posture. The workflow is named at the right scope (the AI use-case lifecycle, the critical-vendor lifecycle, the issue lifecycle for second-line findings) rather than at the program level. The decision authority block names the primary committee, the escalation committee, and the dissent path. Source posture and source list come from the scope or the four-question default.

Gates are workflow-anchored. Each row starts with a stable gate ID and works left to right across the named columns:

- **Gate name.** Operational-language: "Tier-1 AI use-case go-live gate", "Critical vendor onboarding pre-contract gate", "Issue severity-rating gate". A gate name that reads as a slogan ("Excellence Gate", "Innovation Gate") fails the namespace test.
- **Stage in workflow.** Where in the lifecycle the gate fires (intake, tiering, pre-prod, go-live, ongoing monitoring, retirement; planning, due diligence, contract, ongoing monitoring, termination; identification, severity rating, remediation, closure).
- **Trigger.** What brings a case to this gate. Event-based triggers name the event ("submission of completed model card with validation report"); periodic triggers name the cadence ("annual review of every tier-1 AI use case in production"). A gate without a clear trigger fires on aspiration; aspiration is not a trigger.
- **Required reviewers.** Named roles, with primary and backup, and with independence flagged per reviewer where the source guidance demands it. A "review" performed by the same team that produced the artifact is not a gate. The model-risk frame demands that the validator is not the developer; the interagency TPRM frame expects a line-2 reviewer concurrent with the line-1 sponsor; the EU AI Act expects competence, authority, and resources for human oversight. Where the firm's role taxonomy is firm-specific, it lands in `references/firm-overlay.md` and the matrix carries a label like `Head of Model Risk (firm-overlay path)`.
- **Required inputs.** Artifacts that must be present at the gate, by ID. The model card, the validation report, the vendor SOC 2 Type II, the due-diligence pack, the issue write-up, the closure-evidence binder. A gate that says "review what's available" is unauditable.
- **Decision criteria.** Named criteria, each traceable to source. Criteria are declarative ("validation independence is established", "no open critical or high issues against the model", "exit plan exists and has been tested in the last 12 months", "complaint volume is within risk-appetite tolerance"). A criterion that reads as guidance ("review for completeness") is not a criterion.
- **Stop conditions.** What blocks pass. Stop conditions are declarative and binary: "no go-live if any open critical issue", "no contract if no exit plan", "no SAR filing without BSA Officer attestation", "no customer-impact action without CCO sign-off". "Should be reviewed" is not a stop condition.
- **Escalation path.** Where a no-pass goes. The escalation committee, the time-to-escalate, and the escalation owner (the role that takes the case from the gate to the escalation forum). Without an escalation path, a no-pass strands.
- **Documentation requirement.** What gets captured. The decision (pass / fail / conditional), the rationale, the named attesters, the date, the artifact references, and the system of record that holds the record. "Minutes" is acceptable when the firm's minute discipline names attesters and decisions; "noted" is not.
- **Frequency.** Event-based or periodic. Event-based gates name the event; periodic gates name the cadence (daily, weekly, monthly, quarterly, annual).
- **Source anchor.** The named source for the gate's existence — model-risk effective-challenge framing for validation gates, the interagency TPRM lifecycle for vendor-onboarding gates, EU AI Act and NIST AI RMF for AI-governance scaffolding. Granular section refs live in `references/source-anchors.md`. Firm-policy-only gates source to the policy by version and section.

The tail of the matrix earns its keep by what it surfaces. Gate gaps are gates implied by source guidance but not present in the current workflow (an annual review gate that the firm has no calendar for; a validation-independence gate where the firm's developer also signs off the validation; an exit-plan gate where the firm's vendor onboarding has no exit-plan input). Recommended owner actions name the role and the action, with milestones where one is in view. Reviewer questions tie to specific gates, gaps, or independence concerns. The one-page narrative summarises the gate flow for committee adoption: decision authority, gate sequence, escalation, documentation. The recommended charter language is the wording the committee charter or policy section can adopt directly; it reads as charter prose, not as matrix commentary.

The source trace block and sign-off block close the artifact. Material claims cite `references/source-anchors.md` or a loaded overlay by path. `[evidence needed]` flags route to the engagement issue log rather than living silent in the matrix body.

### Sector and cross-cutting overlays

The same gate spine carries different decision authorities, different independence expectations, and different documentation conventions across sectors and cross-cutting topics. Load only the overlays the scope flags. The overlays change which sources the matrix cites and what the practitioner expects to find; they do not change the column structure.

- `references/sector-overlays/banking.md` carries large-bank heightened-standards expectations on board and risk-committee oversight, FRB supervisory expectations on senior-management oversight, and the enhanced-prudential-standards risk-committee shape for large BHCs.
- `references/sector-overlays/insurance.md` carries NAIC ORSA governance, the corporate-governance-disclosure model-act gate flavour, and state DOI committee-charter conventions including audit-committee requirements under state insurance-holding-company statutes.
- `references/sector-overlays/capital-markets.md` carries FINRA supervisory gate posture, the SEC advisers compliance-program annual-review gate framing, and the broker-dealer recordkeeping lens on gate-decision retention.
- `references/sector-overlays/payments-fintech.md` carries OCC bank-fintech partnership oversight for sponsor-bank gate structures and the money-transmitter state-licensing gate posture for non-bank money-services businesses.
- `references/cross-cutting/cyber.md` loads when gates cover incident-response decisions, materiality-determination for cyber events, or cyber-disclosure decisions. SEC public-company disclosure-committee posture, state cyber senior-governing-body responsibility, and FFIEC IT incident-response framing land here.
- `references/cross-cutting/conduct.md` loads when gates cover customer-facing decisions: product approval, fee-change approval, marketing approval, restitution approval, fair-lending second-look. CFPB UDAAP and ECOA second-review conventions land here.

Privacy and climate cross-cutting overlays follow the same pattern; this skill ships cyber and conduct as the cross-cutting files because they are the most frequent triggers. Granular citations (specific section labels, rule numbers) live in `references/source-anchors.md` and the overlay files; the body cites by path. Where firm policy or taxonomy applies (named committees specific to the firm, GRC-platform-specific decision-record fields, internal escalation ladders), it lives in `references/firm-overlay.md` and is consumed when present.

## Quality bar

Independence is named per reviewer. A gate where the artifact's producer is also the gate's decider is not a gate; the producer's review is self-attestation. Where the source guidance demands independence (SR 11-7 validation independence, interagency TPRM line-1 / line-2 separation, EU AI Act Article 14 oversight by competent persons), the `independence_required` field is true and the matrix names the independence boundary.

Stop conditions are declarative and binary. "Should be reviewed," "consider whether," and "as appropriate" are not stop conditions; "no pass if any open critical issue" is.

Each gate names required inputs by artifact ID. A gate that reviews "what is available" is unauditable; the inputs list is the contract between upstream artifact-builders and the gate.

Decision criteria are named and traceable to source. A criterion without a source anchor is policy commentary, not a gate criterion.

Documentation requirement names the record (decision, rationale, attesters, date, system of record). The gate's existence is evidenced by what the system of record holds; an unrecorded gate decision is not a gate decision.

Material claims cite a source. `[evidence needed]` flags route to the engagement issue log; the seams between source evidence, management assertion, public-source obligation, and inference stay visible. RFP narrative is not evidence. `[verify section]` markers belong in source-anchors verification, not the matrix body.

No named institutions in narrative unless they are public defendants in a finalised enforcement action with a published consent order. The matrix stops at recommendation; gate architecture is committee-adopted, and the skill stops at draft.

## Adaptation

Audience drives shape: a committee-adoption pack pulls the one-page narrative and the recommended charter language to the front; an audit-readiness review leads with the gap section and the recommended actions; an examiner-readiness file leads with the source-anchor trace. Source posture drives what the body can carry; public-only matrices sit at named-role and decision-criteria description, mixed and firm-policy-overlay let named committees, system-of-record names, and policy-version section references land. Sector and cross-cutting overlays load from the scope. Frequency, escalation cadence, and dissent-path mechanics track the firm's governance taxonomy where one exists.

## Output

The matrix in `templates/default-output.md` shape and the structured record per `schemas/review-gate-matrix.schema.json`. Downstream consumers: every output-builder skill in the repo references the gate matrix in its sign-off block (the model-card builder names the model-risk committee gate, the issue write-up names the severity-rating gate and the closure gate, the vendor-diligence pack names the pre-contract gate, the SAR-narrative builder names the BSA Officer gate); `risk-committee-pack` references `gate_id` and `gate_gaps` in the governance section; `compliance-testing` cross-references the matrix when designing committee-level testing of governance controls; the firm's GRC platform consumes the structured record to seed gate-decision workflows. The schema is the cross-skill contract; additive changes only, never silent renames. Breaking changes ship as a versioned migration with downstream skills told in advance.

## Pointers

- `references/source-anchors.md` — citations and excerpts for the named anchors.
- `references/sector-overlays/{banking,insurance,capital-markets,payments-fintech}.md` — sector overlays loaded from scope.
- `references/cross-cutting/{cyber,conduct}.md` — cross-cutting overlays loaded when the gates cover information-security or customer-facing decisions.
- `references/firm-overlay.md` — firm-installed taxonomy, named committees, GRC-platform decision-record fields, escalation ladders, dissent-path mechanics beyond the regulatory baseline; consumed when present.
- `templates/default-output.md` — gate matrix template.
- `schemas/review-gate-matrix.schema.json` — structured-output contract.
- `examples/` — AI use-case lifecycle gates for a regional bank; critical-vendor onboarding gates aligned to interagency TPRM guidance.
- `TROUBLESHOOTING.md` — recurring defects in gate matrices.
