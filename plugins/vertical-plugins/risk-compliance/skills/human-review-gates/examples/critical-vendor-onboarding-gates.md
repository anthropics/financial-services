# Example: Critical-vendor onboarding gates aligned to interagency TPRM guidance

## Input

A mid-sized US bank ($12B assets, FRB- and FDIC-supervised state-member, sub-Heightened-Standards but with a material vendor footprint) is refreshing its critical-vendor onboarding gate matrix to align with the Interagency Guidance on Third-Party Relationships (June 2023). The current onboarding workflow has a single "vendor approval" gate that compresses planning, due diligence, contract review, and operational confirmation into one Vendor Risk Committee decision; the bank's own internal audit raised this as a finding in the most recent audit cycle. The refresh is also responsive to a recent FDIC supervisory letter that cited insufficient documentation of ongoing-monitoring decisions. Source posture is mixed: Interagency TPRM Guidance (June 2023), the firm's existing Third-Party Risk Management Policy v3.5, and the audit-finding remediation memorandum. Engagement scope is supplied: institution type state-member bank, primary regulators FRB and FDIC, persona Head of Vendor Risk Management, source posture mixed, sector overlay banking, no AI cross-cutting overlay (vendor portfolio is conventional). Audience is the Vendor Risk Committee adopting the matrix as charter language, with copy to the Operational Risk Committee.

## Why this scenario matters

Vendor risk management is the most-examined second-line function at most US banks because the Interagency Guidance is explicit and the federal supervisors have prioritised vendor oversight in recent exam cycles. A common failure mode (one-committee monoculture compressing all vendor decisions into one gate) is exactly what this engagement is correcting. The example tests: distinct gates aligned to TPRM lifecycle phases (planning, due diligence, contract, ongoing monitoring, termination); criticality-driven gate intensity; line-1 / line-2 separation under the interagency guidance; documentation that survives an FDIC examination; the gap where an exit-plan gate is implicit but not yet operationally gated; and recommended charter language for the Vendor Risk Committee.

## Output sketch (gate matrix excerpt)

```yaml
gate_matrix_id: GM-2026-VRC-Critical-Vendor-Lifecycle-001
workflow_in_scope: "Critical-vendor onboarding lifecycle: planning, due diligence, contract, ongoing monitoring, termination. Critical vendors only; non-critical vendors flow through a lighter workflow not in scope of this matrix."
scope_notes: "Critical vendor definition per firm TPRM policy v3.5 §2.1: vendors providing services material to operational resilience, vendors with access to NPI, vendors providing critical-platform technology. Excludes intra-group affiliates supervised under separate enterprise-resilience framework."
source_posture: mixed
engagement_id: ENG-2026-VRC-Charter-Refresh

decision_authority:
  primary_committee: "Vendor Risk Committee (VRC)"
  escalation_committee: "Operational Risk Committee, escalating to Risk Committee of the Board for material termination or material onboarding"
  dissent_path: "Any VRC member may record a dissent in the meeting minutes; recorded dissents on critical-vendor gates trigger automatic escalation to the Operational Risk Committee."
  board_oversight: "Quarterly summary of critical-vendor portfolio status to Board Risk Committee; annual report on TPRM program effectiveness."

gates:
  - gate_id: GATE-VEN-001
    gate_name: "Critical-vendor planning gate"
    stage: planning
    trigger: "Business sponsor proposes engagement of a critical vendor (per firm criticality definition); planning gate fires before any due-diligence work begins"
    required_reviewers:
      - role: "Head of Vendor Risk Management (line 2)"
        is_primary: true
        independence_required: true
        independence_basis: "Interagency TPRM §III.A; firm TPRM Policy v3.5 §3.1"
      - role: "Business Sponsor (line 1)"
        is_primary: false
      - role: "Head of Procurement (operational coordination)"
        is_primary: false
    required_inputs:
      - "Business case with named line-1 owner"
      - "Strategic alignment statement"
      - "Initial criticality classification"
      - "Initial risk assessment (data sensitivity, operational dependence, customer-impact)"
    decision_criteria:
      - criterion: "Engagement aligns with firm strategy and risk appetite"
        source_anchor: "Interagency TPRM §III.A; references/source-anchors.md#interagency-tprm"
      - criterion: "Initial criticality classification is supported"
        source_anchor: "references/firm-overlay.md#criticality-definition"
      - criterion: "Named line-1 owner accepts ongoing-monitoring accountability"
        source_anchor: "references/source-anchors.md#interagency-tprm"
    stop_conditions:
      - "No advance to due-diligence without line-1 owner acceptance of monitoring accountability"
      - "No advance if business case lacks strategic-alignment rationale"
    escalation_path:
      escalation_committee: "Operational Risk Committee"
      time_to_escalate: "Next scheduled VRC meeting"
      escalation_owner: "Head of Vendor Risk Management"
    documentation_requirement:
      - "Planning decision in VRC minutes"
      - "Business case and initial assessment retained in GRC platform vendor record"
    frequency: event-based
    source_anchor: "Interagency TPRM Guidance §III.A; references/source-anchors.md#interagency-tprm-2023"

  - gate_id: GATE-VEN-002
    gate_name: "Pre-contract due-diligence gate"
    stage: due-diligence
    trigger: "Due-diligence work substantially complete; vendor identified as preferred candidate; gate fires before contract negotiation begins"
    required_reviewers:
      - role: "Head of Vendor Risk Management (line 2)"
        is_primary: true
        independence_required: true
        independence_basis: "Interagency TPRM §III.B; firm TPRM Policy v3.5 §4.1"
      - role: "Business Sponsor (line 1)"
        is_primary: false
      - role: "CISO (cyber due diligence)"
        is_primary: false
        independence_basis: "Interagency TPRM §III.B; FFIEC IT Booklet"
      - role: "General Counsel (legal due diligence)"
        is_primary: false
      - role: "Chief Privacy Officer (when NPI is in scope)"
        is_primary: false
      - role: "Operational Risk Committee (concurrence required for highest-criticality vendors per firm policy)"
        is_primary: false
    required_inputs:
      - "Due-diligence pack covering financial condition, business reputation, technology and infrastructure, information security, business resilience, fee structures and incentives, qualifications and experience of key personnel, risk management"
      - "SOC 2 Type II report or equivalent, with firm review of qualifying opinions"
      - "Cybersecurity assessment and any third-party penetration-test attestations"
      - "Resolution of any high-residual-risk findings or documented mitigation"
      - "Initial draft exit plan (criticality-driven; required for highest-criticality vendors)"
    decision_criteria:
      - criterion: "Due diligence covers each named area in TPRM §III.B"
        source_anchor: "Interagency TPRM §III.B; references/source-anchors.md#interagency-tprm"
      - criterion: "Identified residual risks are mitigated, documented, or accepted by VRC"
        source_anchor: "Interagency TPRM §III.B"
      - criterion: "SOC 2 report covers the relevant Trust Services Criteria for the services in scope; qualified opinions are reviewed and addressed"
        source_anchor: "references/cross-cutting/cyber.md (loaded if cyber overlay flagged)"
      - criterion: "Exit-plan readiness is documented for highest-criticality vendors"
        source_anchor: "Interagency TPRM §III.E; references/firm-overlay.md#exit-plan-policy"
    stop_conditions:
      - "No proceed to contract gate without resolution of high-residual-risk findings"
      - "No proceed without SOC 2 Type II (or equivalent) where applicable to the service"
      - "No proceed without initial exit plan for highest-criticality vendors"
      - "No proceed without CISO concurrence on cyber-due-diligence completeness"
    escalation_path:
      escalation_committee: "Operational Risk Committee"
      time_to_escalate: "Next scheduled meeting; emergency convening for material delays"
      escalation_owner: "Head of Vendor Risk Management"
    documentation_requirement:
      - "Due-diligence decision in VRC minutes with named attesters"
      - "Due-diligence pack retained in GRC platform vendor record (system: GRC-Vendor-Records)"
      - "SOC 2 report and attestation retained in GRC platform"
      - "Cyber assessment retained per firm cyber-records retention"
    frequency: event-based
    source_anchor: "Interagency TPRM Guidance §III.B (due diligence and selection); references/source-anchors.md#interagency-tprm-2023"

  - gate_id: GATE-VEN-003
    gate_name: "Contract gate"
    stage: contract
    trigger: "Contract substantially negotiated; gate fires before contract execution"
    required_reviewers:
      - role: "Head of Vendor Risk Management (line 2)"
        is_primary: true
      - role: "General Counsel"
        is_primary: false
      - role: "Business Sponsor"
        is_primary: false
      - role: "Head of Operational Risk (concurrence on critical contracts)"
        is_primary: false
        independence_basis: "Interagency TPRM §III.C"
      - role: "CISO (concurrence on contracts with cyber implications)"
        is_primary: false
    required_inputs:
      - "Negotiated contract with all material terms"
      - "Risk-management terms summary (information rights, audit rights, performance metrics, fourth-party considerations, exit terms)"
      - "Service-level commitments aligned to firm operational-resilience requirements"
      - "Updated exit plan reflecting contract terms"
    decision_criteria:
      - criterion: "Contract addresses each TPRM-named risk-management area appropriately for the criticality"
        source_anchor: "Interagency TPRM §III.C; references/source-anchors.md#interagency-tprm"
      - criterion: "Information and audit rights enable firm-side oversight at the criticality level"
        source_anchor: "Interagency TPRM §III.C"
      - criterion: "Exit terms are workable and align with the exit-plan readiness"
        source_anchor: "Interagency TPRM §III.E"
    stop_conditions:
      - "No execution without complete risk-management terms"
      - "No execution if information or audit rights are not commensurate with criticality"
      - "No execution if exit terms render exit plan unexecutable"
    escalation_path:
      escalation_committee: "Operational Risk Committee, escalating to Risk Committee of the Board for materially long-tail contracts"
      time_to_escalate: "Within 5 business days of contested terms"
      escalation_owner: "General Counsel and Head of Vendor Risk Management"
    documentation_requirement:
      - "Contract gate decision in VRC minutes"
      - "Final contract retained in contract management system"
      - "Risk-management terms summary retained in GRC platform"
    frequency: event-based
    source_anchor: "Interagency TPRM Guidance §III.C (contract negotiation); references/source-anchors.md#interagency-tprm-2023"

  - gate_id: GATE-VEN-004
    gate_name: "Post-onboarding 90-day operational confirmation gate"
    stage: ongoing-monitoring
    trigger: "90 days post-go-live with the vendor; first formal ongoing-monitoring touchpoint"
    required_reviewers:
      - role: "Head of Vendor Risk Management"
        is_primary: true
      - role: "Business Sponsor"
        is_primary: false
      - role: "Vendor Relationship Manager (firm-side single point of contact)"
        is_primary: false
    required_inputs:
      - "First 90 days of operational performance against SLAs"
      - "First 90 days of monitoring evidence (SOC report cycle status, incident history, complaint history if applicable)"
      - "Confirmation that contracted controls are operating as designed"
    decision_criteria:
      - criterion: "Vendor performance meets contracted SLAs and risk-management commitments at 90 days"
        source_anchor: "Interagency TPRM §III.D; firm TPRM Policy v3.5 §5.1"
      - criterion: "No material monitoring exceptions in the 90-day window"
        source_anchor: "references/source-anchors.md#interagency-tprm"
      - criterion: "Annual ongoing-monitoring schedule is populated in GRC platform"
        source_anchor: "references/firm-overlay.md#monitoring-cadence"
    stop_conditions:
      - "No advance to standard ongoing monitoring if material SLA failures are unresolved"
      - "Re-engagement of due-diligence gate if unforeseen material risks have surfaced"
    escalation_path:
      escalation_committee: "Operational Risk Committee"
      time_to_escalate: "Next VRC meeting"
      escalation_owner: "Head of Vendor Risk Management"
    documentation_requirement:
      - "90-day decision in VRC minutes"
      - "Performance pack retained in GRC platform"
    frequency: event-based
    frequency_detail: "90 days post-go-live; one-time gate"
    source_anchor: "Interagency TPRM Guidance §III.D (ongoing monitoring); references/source-anchors.md#interagency-tprm-2023"

  - gate_id: GATE-VEN-005
    gate_name: "Annual ongoing-monitoring gate"
    stage: ongoing-monitoring
    trigger: "Annual ongoing-monitoring cycle for each critical vendor"
    required_reviewers:
      - role: "Head of Vendor Risk Management"
        is_primary: true
      - role: "Business Sponsor"
        is_primary: false
      - role: "CISO (when cyber-relevant)"
        is_primary: false
      - role: "Operational Risk Committee (concurrence on highest-criticality vendors)"
        is_primary: false
    required_inputs:
      - "Annual SOC report review"
      - "Annual cyber assessment refresh (when cyber-relevant)"
      - "Year of monitoring evidence (SLAs, incidents, complaints, financial-condition signals)"
      - "Updated exit plan reflecting any year-on-year changes"
      - "Refreshed criticality classification"
    decision_criteria:
      - criterion: "Vendor continues to meet contracted commitments and risk-management expectations"
        source_anchor: "Interagency TPRM §III.D"
      - criterion: "No accumulated monitoring exceptions unresolved"
      - criterion: "Exit plan remains workable and tested within last 12 months for highest-criticality vendors"
        source_anchor: "Interagency TPRM §III.E"
    stop_conditions:
      - "Re-engagement of full due-diligence if vendor's financial condition or business has materially changed"
      - "Acceleration to termination gate if material risk-management failures are unresolved"
    documentation_requirement:
      - "Annual ongoing-monitoring decision in VRC minutes"
      - "Refresh pack retained in GRC platform"
      - "Cross-reference to any related issue write-ups"
    frequency: annual
    source_anchor: "Interagency TPRM Guidance §III.D; references/source-anchors.md#interagency-tprm-2023"

  - gate_id: GATE-VEN-006
    gate_name: "Termination gate"
    stage: termination
    trigger: "Decision to terminate critical-vendor relationship (firm-initiated, vendor-initiated, or contract-end)"
    required_reviewers:
      - role: "Head of Vendor Risk Management"
        is_primary: true
      - role: "Business Sponsor"
        is_primary: false
      - role: "General Counsel"
        is_primary: false
      - role: "Head of Operational Risk"
        is_primary: false
      - role: "Operational Risk Committee (full committee concurrence on termination of highest-criticality vendors)"
        is_primary: false
        independence_basis: "Interagency TPRM §III.E"
    required_inputs:
      - "Exit plan with named milestones, owners, and dates"
      - "Customer-impact analysis"
      - "Data-return and data-destruction plan"
      - "Service-continuity plan (replacement vendor, in-house substitute, customer notification if applicable)"
    decision_criteria:
      - criterion: "Exit plan is workable and addresses each TPRM-named termination area"
        source_anchor: "Interagency TPRM §III.E; references/source-anchors.md#interagency-tprm"
      - criterion: "Customer impact is assessed and any customer-notification or transition obligations are met"
        source_anchor: "Interagency TPRM §III.E; CFPB CMS framework"
      - criterion: "Data-return and data-destruction plan addresses all NPI and other firm data"
        source_anchor: "Interagency TPRM §III.E; GLBA Safeguards Rule"
    stop_conditions:
      - "No termination execution without OpRC concurrence for highest-criticality vendors"
      - "No termination execution without confirmed customer-impact analysis"
      - "No termination execution if exit plan is not workable on stated timeline"
    escalation_path:
      escalation_committee: "Risk Committee of the Board"
      time_to_escalate: "Within the termination notice window; emergency convening if termination is regulator-driven"
      escalation_owner: "Head of Vendor Risk Management; General Counsel for legal-driven terminations"
    documentation_requirement:
      - "Termination decision in VRC and OpRC minutes"
      - "Exit plan execution evidence retained in GRC platform"
      - "Data-return and data-destruction attestation retained"
    frequency: event-based
    source_anchor: "Interagency TPRM Guidance §III.E (termination); references/source-anchors.md#interagency-tprm-2023"

gate_gaps:
  - implied_gate_name: "Exit-plan readiness gate (separate from termination gate)"
    gap_description: "Current workflow assumes the exit plan exists if the termination gate fires; the Interagency TPRM Guidance §III.E and the firm's own audit finding (memo IA-2026-Q1-014) both point to exit-plan readiness as a continuous obligation rather than a termination-gate input. Implies a periodic exit-plan readiness assessment with a named gate, distinct from the termination gate that consumes the exit plan when terminating."
    source_anchor: "Interagency TPRM §III.E; firm internal audit memo IA-2026-Q1-014"
    recommended_action: "Add an exit-plan tabletop / readiness gate at criticality-driven cadence (annual for highest criticality, biennial otherwise). The annual-monitoring gate can incorporate the exit-plan readiness check, but the testing of the plan (tabletop) is a separate gate with named participants."
  - implied_gate_name: "Fourth-party risk gate for material subcontractors"
    gap_description: "Current workflow does not separately gate the firm's exposure to the vendor's material subcontractors. Interagency TPRM §III.D names fourth-party risk as part of ongoing monitoring; some firms gate it as a distinct decision."
    source_anchor: "Interagency TPRM §III.D"
    recommended_action: "At due-diligence and at annual monitoring, identify material subcontractors and assess fourth-party risk; document in vendor record. A separate gate may not be necessary if the existing gates explicitly address fourth-party considerations."

recommended_charter_language: |
  The Vendor Risk Committee (the Committee) is the firm's primary governance body for critical-vendor relationships across the third-party-risk lifecycle from planning through termination. The Committee operates with decision authority on critical-vendor onboarding, contract approval, ongoing monitoring, and termination, with the Operational Risk Committee as the named escalation body for highest-criticality decisions and recorded dissents.

  The Committee carries six named gates: planning, pre-contract due diligence, contract, post-onboarding 90-day operational confirmation, annual ongoing monitoring, and termination. Each gate has named decision criteria sourced from the Interagency Guidance on Third-Party Relationships (June 2023) and the firm's Third-Party Risk Management Policy. Stop conditions are declarative; the gates are not advisory. The Committee's gate decisions are documented in the meeting minutes with named attesters and the documentation is retained in the firm's governance system per the firm's records-retention schedule (typically 7-year retention aligned to federal banking exam-file expectations).

  For highest-criticality vendors, contract gates and termination gates require Operational Risk Committee concurrence; the Committee reports to the Board Risk Committee on the critical-vendor portfolio quarterly with material decisions surfaced for board-level oversight. Cyber considerations engage the Chief Information Security Officer as a required reviewer at due-diligence, contract, and annual monitoring gates whenever the vendor's services touch firm information assets, customer data, or privileged-system access.

reviewer_questions:
  - "Should the firm adopt a separate exit-plan readiness gate as recommended in the gap section, or fold the testing into the annual ongoing-monitoring gate? Operational risk and audit views may differ."
  - "For the Operational Risk Committee concurrence requirement on highest-criticality contract and termination gates, what is the firm's escalation cadence (next scheduled meeting vs. emergency convening) and is the OpRC charter aligned with this expectation?"
  - "Does the firm's current critical-vendor population permit annual SOC report review for every critical vendor, or does the cadence need adjustment based on vendor SOC reporting cycles?"
  - "For fourth-party risk, is a separate gate necessary or do the existing gates' decision criteria (fourth-party language at due diligence and annual monitoring) suffice?"

confidence_label: medium
human_review_required: true
```

## What the matrix surfaces

- **Six distinct gates aligned to TPRM lifecycle**. Planning, due diligence, contract, 90-day operational confirmation, annual monitoring, termination. Each ties directly to a TPRM section. Not the one-committee monoculture the audit flagged.
- **Independence on line-2 and CISO slots**. Head of Vendor Risk Management has independence flagged at planning and due-diligence with the source anchor; CISO independence flagged at due-diligence with the FFIEC and TPRM anchors. Operational Risk Committee independence flagged at contract and termination for highest-criticality.
- **OpRC concurrence on highest-criticality**. The matrix names OpRC concurrence as a required reviewer at the contract gate and termination gate for highest-criticality vendors, distinct from VRC quorum. This addresses the FDIC supervisory-letter concern about insufficient documentation of material vendor decisions.
- **Documentation discipline tied to FDIC examination posture**. Retention named at 7 years; system of record named (GRC-Vendor-Records); board reporting cadence named.
- **Real gap surfaced**. The exit-plan readiness gate is implicit in TPRM §III.E and explicit in the firm's own audit finding; the gap section names this with the source anchor and the recommended action. Fourth-party risk also surfaced, with the recommendation to fold into existing gates rather than create a new one (right-sized).
- **Recommended charter language as committee-adoptable**. Three paragraphs, names the gates, the criticality-driven OpRC concurrence pattern, and the cyber-CISO engagement.
- **Reviewer questions tie to live decisions**. Exit-plan readiness gate scope, OpRC escalation cadence, SOC review cadence for the vendor portfolio, fourth-party gate scope. Each is a real call the committee needs to make.

## Downstream uses

- `vendor-diligence` references GATE-VEN-002 (due diligence) in its sign-off block; the diligence pack maps to required_inputs.
- `exit-plan` references GATE-VEN-003 (contract; exit terms) and GATE-VEN-006 (termination); the exit plan is a required input.
- `compliance-testing` for the TPRM control test reads the gates as the named decision points; the test workpaper samples gate-decision documentation.
- `risk-committee-pack` for the next OpRC reads termination-gate decisions and material onboarding decisions; for the next Board Risk Committee reads the quarterly summary.
- `issue-writeup` for any vendor-monitoring exception links to the relevant gate; the issue's severity drops the vendor's effective-monitoring rating until closure.
