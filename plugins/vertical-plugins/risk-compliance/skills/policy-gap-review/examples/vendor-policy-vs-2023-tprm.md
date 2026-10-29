# Example: pre-2023 vendor-management policy benchmarked against the June 2023 interagency TPRM guidance

## Input

A $40B regional bank's Third-Party Risk Management Office is reviewing the firm's Vendor Management Policy ahead of the FRB's planned safety-and-soundness examination of operational resilience. The policy was last refreshed in 2021 and was anchored on the legacy OCC Bulletin 2013-29. The June 2023 interagency third-party risk management guidance (jointly issued by OCC, FRB, and FDIC) replaced 2013-29 and the bank's TPRMO has been operating against the 2023 guidance informally; the policy refresh has been on the backlog for 18 months. Source posture is mixed: the June 2023 interagency guidance (public) plus the firm's Vendor Management Policy v3.4 (firm-policy overlay) and a supporting Vendor Lifecycle Standard v2.1 (firm-policy overlay). Sector overlay: banking. Cross-cutting overlay: cyber (the policy includes a §7 information-security section that benchmarks against NYDFS Part 500 §500.11 for the bank's NYDFS-licensed entities and against the cyber overlay's third-party-cyber expectations).

## Why this scenario matters

This is the canonical pre-2023-vs-2023 vendor-policy refresh. The June 2023 guidance reorganised the third-party lifecycle into five named phases (planning, due diligence and selection, contract negotiation, ongoing monitoring, termination), introduced explicit subcontractor-oversight expectations, and reframed exit planning from a periodic exercise to a tested capability. Policies anchored on 2013-29 typically miss four lifecycle dimensions: planning-phase criticality assessment as a discrete step (legacy policies move directly to due-diligence), ongoing-monitoring KRIs (legacy policies refer to "annual review" only), exit planning with periodic testing (legacy policies have no exit-plan-testing requirement), and subcontractor oversight (legacy policies are typically silent). The example tests gap classifications across the four dimensions and the cross-policy interaction with the bank's information-security policy on subcontractor cyber depth.

## Output sketch

```yaml
review_id: PGR-2026-TPRM-02
as_of_date: 2026-05-06
engagement_id: ENG-2026-OPRES-EXAM-PREP

policy_under_review:
  policy_name: "Vendor Management Policy"
  policy_version: "v3.4"
  effective_date: 2021-11-04
  owner_role: "Head of Vendor Management"
  document_identifier: "intranet:/policies/risk/vmp/v3.4"
  supporting_artefacts:
    - {artefact_name: "Vendor Lifecycle Standard", artefact_version: "v2.1", owner_role: "Head of Vendor Management"}

benchmark_sources:
  - {source_name: "Interagency Guidance on Third-Party Relationships: Risk Management",
     edition: "June 6, 2023",
     section_references: ["§III.A planning", "§III.B due diligence and selection", "§III.C contract negotiation", "§III.D ongoing monitoring", "§III.E termination"]}
  - {source_name: "OCC Bulletin 2014-39 — Risk Governance for Banks",
     edition: "2014",
     section_references: ["governance expectations on third-party risk under heightened standards"]}

scope_of_review:
  - {policy_section: "§2 Definitions and scope", benchmark_sources_used: ["June 2023 guidance §III.A"]}
  - {policy_section: "§3 Vendor lifecycle", benchmark_sources_used: ["June 2023 guidance §III.A through §III.E"]}
  - {policy_section: "§4 Criticality and risk tiering", benchmark_sources_used: ["June 2023 guidance §III.A"]}
  - {policy_section: "§5 Due diligence", benchmark_sources_used: ["June 2023 guidance §III.B"]}
  - {policy_section: "§6 Contracts", benchmark_sources_used: ["June 2023 guidance §III.C"]}
  - {policy_section: "§7 Information security and cyber", benchmark_sources_used: ["June 2023 guidance §III.B/§III.D", "NYDFS §500.11", "cyber overlay"]}
  - {policy_section: "§8 Ongoing monitoring", benchmark_sources_used: ["June 2023 guidance §III.D"]}
  - {policy_section: "§9 Termination and exit", benchmark_sources_used: ["June 2023 guidance §III.E"]}

source_posture: mixed

gaps:
  - gap_id: GAP-001
    benchmark_requirement: "Firm policy treats planning-phase criticality assessment as a discrete lifecycle step preceding due diligence."
    benchmark_source_anchor: {source_name: "Interagency Guidance June 2023", section: "§III.A planning"}
    policy_text_excerpt: "§3 Vendor lifecycle moves from 'engagement initiation' directly to 'due diligence'. §4 Criticality and risk tiering applies criticality scoring after due diligence completes."
    policy_location: "§3 Vendor lifecycle, §4 Criticality and risk tiering"
    gap_classification: partial
    severity: moderate
    severity_rationale: "Policy addresses criticality but in the wrong lifecycle position. June 2023 guidance §III.A expects criticality and risk-tiering to drive due-diligence depth; running tiering after due diligence inverts the expected flow. Compensating practice: TPRMO operating procedures already follow the June 2023 sequencing informally; the gap is policy-text rather than operational."
    recommended_edit: "Restructure §3 to introduce a §3.1 'Planning' step covering: (a) initial criticality assessment based on activity description, (b) preliminary risk tiering, (c) due-diligence scope determination based on tiering. Move existing §4 content into the planning step."
    evidence_needed:
      - "Refresh of Vendor Lifecycle Standard to mirror the policy structure"
      - "Refresh of GRC platform workflow sequencing"
      - "Training of vendor risk analysts on the planning-step framing"
    linked_obligation_ids: [OBL-TPRM-2023-IIIA]
    linked_control_ids: [C-VND-001]
    owner_role: "Head of Vendor Management"

  - gap_id: GAP-002
    benchmark_requirement: "Firm policy specifies named ongoing-monitoring KRIs and a documented review cadence proportionate to vendor criticality."
    benchmark_source_anchor: {source_name: "Interagency Guidance June 2023", section: "§III.D ongoing monitoring"}
    policy_text_excerpt: "§8 Ongoing monitoring requires 'annual review' for all vendors. KRIs are not named; cadence does not vary by criticality."
    policy_location: "§8 Ongoing monitoring"
    gap_classification: weak
    severity: high
    severity_rationale: "Policy addresses monitoring but at lower rigor than §III.D expects. Annual-review-only is the legacy 2013-29 framing; June 2023 guidance expects KRIs aligned to vendor criticality and a documented cadence varying by tier. Bank has 14 critical vendors and 9 of them have not had a sub-annual touchpoint in the last 12 months. Supervisory exposure on operational-resilience exam is concrete."
    recommended_edit: "Rewrite §8 to specify: (a) named ongoing-monitoring KRIs (financial health, performance SLAs, security posture, change events, complaint volume, sub-service-provider changes), (b) cadence varying by tier (critical: quarterly; high: semi-annual; moderate and low: annual), (c) escalation triggers when KRIs breach defined thresholds, (d) documented evidence of monitoring in the GRC platform."
    evidence_needed:
      - "KRI definitions and threshold framework"
      - "GRC platform configuration to track tier-specific cadence"
      - "Updated monitoring-evidence templates"
      - "Backfill of sub-annual touchpoints on critical vendors as interim mitigation"
    linked_obligation_ids: [OBL-TPRM-2023-IIID]
    linked_control_ids: [C-VND-008]
    owner_role: "Head of Vendor Management"

  - gap_id: GAP-003
    benchmark_requirement: "Firm policy requires exit planning with periodic testing for critical vendor relationships."
    benchmark_source_anchor: {source_name: "Interagency Guidance June 2023", section: "§III.E termination"}
    policy_text_excerpt: "Policy is silent on exit planning. §9 Termination and exit covers contractual termination clauses but does not require exit-plan documentation or testing."
    policy_location: "§9 Termination and exit"
    gap_classification: missing
    severity: high
    severity_rationale: "Operational-resilience expectations across multiple supervisor surfaces (FRB, OCC, FDIC under June 2023 guidance; UK PRA / EBA equivalents for the bank's London branch) treat exit planning as a foundational operational-resilience capability. The bank's three most-critical fintech-platform vendors have no documented exit plan; under stress, the bank would be reliant on contract termination clauses without an inventory of resumption alternatives. The FRB exam scope explicitly references operational resilience."
    recommended_edit: "Insert §9.2 Exit planning requiring: (a) documented exit plan for every critical vendor relationship covering trigger events, alternative-provider inventory, data-portability assessment, and customer-impact assessment; (b) periodic exit-plan testing on a documented cadence (typically annual for critical vendors); (c) board reporting on exit-plan readiness."
    evidence_needed:
      - "Exit-plan template"
      - "Exit plans for the 14 critical vendors"
      - "Annual exit-plan testing program design"
      - "Board reporting on exit-plan readiness"
      - "Cross-functional working session with Operational Resilience team and Business Continuity team"
    linked_obligation_ids: [OBL-TPRM-2023-IIIE]
    linked_control_ids: []
    owner_role: "Head of Vendor Management"

  - gap_id: GAP-004
    benchmark_requirement: "Firm policy addresses subcontractor oversight including identification of material subcontractors and risk-based depth of subcontractor due diligence."
    benchmark_source_anchor: {source_name: "Interagency Guidance June 2023", section: "§III.B due diligence and §III.D ongoing monitoring"}
    policy_text_excerpt: "Policy is silent on subcontractor oversight. §5 Due diligence and §8 Ongoing monitoring focus on the direct vendor; subcontractors are referenced once in §6 Contracts (notice-of-subcontracting clause) without due-diligence expectations."
    policy_location: "§5 Due diligence, §8 Ongoing monitoring"
    gap_classification: missing
    severity: high
    severity_rationale: "June 2023 guidance is explicit that institutions retain accountability for the activities performed by subcontractors. Bank uses cloud-hosted SaaS for several critical functions where the SaaS provider's hosting subcontractor is itself a material concentration risk. Subcontractor invisibility is a frequent enforcement trigger on operational-resilience and information-security findings. Cross-policy interaction with §7 Information security and cyber section is direct."
    recommended_edit: "Insert §5.4 Subcontractor due diligence requiring: (a) identification of material subcontractors at intake, (b) risk-based due-diligence depth on subcontractors based on criticality and information access, (c) ongoing monitoring of material subcontractor changes, (d) contract-level requirements for subcontractor disclosure and change notice. Cross-reference to Information Security Policy §4.2 for subcontractor cyber depth."
    evidence_needed:
      - "Material-subcontractor identification across the existing vendor portfolio"
      - "Refresh of due-diligence work-paper template to capture subcontractor due diligence"
      - "Updated contract template clauses on subcontractor disclosure and change notice"
      - "Cross-policy alignment with Information Security Policy on subcontractor cyber expectations"
    linked_obligation_ids: [OBL-TPRM-2023-IIIB, OBL-TPRM-2023-IIID]
    linked_control_ids: []
    owner_role: "Head of Vendor Management"

  - gap_id: GAP-005
    benchmark_requirement: "Firm cybersecurity expectations on third-party service providers (NYDFS §500.11 equivalent for non-NYDFS entities) are addressed at the rigor the cyber overlay expects."
    benchmark_source_anchor: {source_name: "23 NYCRR Part 500 (post-November 2023 amendment)", section: "§500.11 third-party service-provider security policy"}
    policy_text_excerpt: "§7 Information security and cyber requires vendors to 'maintain reasonable cybersecurity controls' and references the firm's Information Security Policy. §500.11 content elements (encryption, MFA, notice of cybersecurity events, due-diligence framework on cyber posture) are not directly addressed."
    policy_location: "§7 Information security and cyber"
    gap_classification: partial
    severity: moderate
    severity_rationale: "Policy addresses third-party cyber but at lower rigor than NYDFS §500.11 expects (and parallel expectations under FFIEC IT Handbook Information Security booklet for the bank's non-NYDFS entities). Information Security Policy §4 covers the cyber expectations in more detail, so cross-policy compensation exists; the gap is the cross-reference precision and the contract-clause linkage."
    recommended_edit: "Refresh §7 to: (a) cross-reference Information Security Policy §4.2 explicitly for third-party cyber depth; (b) require contract clauses on encryption, MFA on accounts accessing nonpublic information, cyber-incident notice within named timing (24-72 hours), and the due-diligence framework on cyber posture; (c) clarify that for NYDFS-licensed entities, §500.11 governs and Information Security Policy §4.2 implements it."
    evidence_needed:
      - "Cross-policy alignment with Information Security Policy §4.2"
      - "Contract template refresh on cyber-incident notice timing"
      - "Per-vendor inventory of contract compliance with refreshed cyber clauses"
    linked_obligation_ids: [OBL-NYDFS-500.11, OBL-TPRM-2023-IIIB]
    linked_control_ids: [C-VND-CYBER-001]
    owner_role: "Head of Vendor Management"
    row_confidence: high

coverage_summary:
  total_benchmark_items: 31
  covered_items: 22
  partial_items: 4
  missing_items: 3
  inconsistent_items: 1
  outdated_items: 1

out_of_scope_items:
  - item: "Non-ICT third parties (cleaning, catering, building services)"
    rationale: "Legacy policy intentionally excludes non-ICT third parties from the vendor-management framework. Documented in §2.1 of the policy and accepted by the firm's Operational Risk Committee in 2018; the June 2023 guidance does not mandate inclusion."

cross_policy_interactions:
  - other_policy: "Information Security Policy v5.2"
    interaction_type: dependency
    description: "GAP-004 and GAP-005 both depend on alignment with Information Security Policy §4.2 on subcontractor and third-party cyber expectations. Co-fix needed."
    linked_gap_ids: [GAP-004, GAP-005]
  - other_policy: "Information Security Policy v5.2"
    interaction_type: conflict
    description: "Information Security Policy §4.2 expects subcontractor due-diligence depth at a rigor that the Vendor Management Policy §5 does not provide for. The two policies disagree on subcontractor scoping. Resolution required at the level of policy ownership."
    linked_gap_ids: [GAP-004]
  - other_policy: "Operational Resilience Policy v1.3"
    interaction_type: dependency
    description: "GAP-003 (exit planning) requires alignment with the Operational Resilience Policy framework on critical operations and impact tolerances."
    linked_gap_ids: [GAP-003]
  - other_policy: "Business Continuity and Disaster Recovery Standard v2.0"
    interaction_type: overlap
    description: "GAP-003 (exit planning) overlaps with the BCDR Standard on critical-vendor scenario testing. Recommend coordinated test design rather than parallel testing programs."
    linked_gap_ids: [GAP-003]

recommended_next_steps:
  - "Draft revisions on §3 (lifecycle restructure), §5.4 (subcontractor due diligence), §7 (cyber alignment), §8 (ongoing-monitoring KRIs and cadence), §9.2 (exit planning) ready for legal review by 2026-06-30."
  - "Convene cross-policy working session with Head of Information Security, Head of Operational Resilience, and Head of Business Continuity by 2026-06-15 to resolve GAP-004 conflict and GAP-003 overlap."
  - "Backfill sub-annual touchpoints on the 14 critical vendors as interim mitigation pending §8 refresh; deadline 2026-07-31."
  - "Route to Risk Committee for tabling on 2026-08."
  - "Schedule training refresh for vendor risk analysts and vendor relationship managers within 60 days of approval."

confidence_label: high

reviewer_questions:
  - "GAP-002 severity is rated `high` partly because 9 critical vendors have not had a sub-annual touchpoint. If the interim backfill completes before exam fieldwork, does severity reduce to `moderate`?"
  - "GAP-003 (exit planning) names exit-plan testing as a benchmark expectation. The firm's Operational Resilience Policy is itself due for a refresh; should exit-plan testing live in the Vendor Management Policy or in the Operational Resilience Policy? The reviewer questions hand to the cross-policy working session."
  - "GAP-004 names a conflict with the Information Security Policy on subcontractor scoping. Which policy governs at the seam, and which is the operating policy that defers? The Compliance Committee tabling should resolve."
  - "GAP-005 row confidence is rated high because the cross-policy compensation in Information Security Policy §4.2 is verifiable. If the Information Security Policy is itself in scope of a separate refresh, does the matrix re-test?"

human_review_required: true

revisions:
  - {date: 2026-05-06, reason: "initial review", delta: "created during operational-resilience exam-prep engagement", approved_by: "Head of Vendor Management"}
```

## What the matrix surfaces

- The four lifecycle gap dimensions land cleanly: GAP-001 (planning) as `partial`, GAP-002 (ongoing monitoring) as `weak`, GAP-003 (exit planning) as `missing`, GAP-004 (subcontractor oversight) as `missing`. The classifications are not interchangeable; the matrix shows the discipline of picking the right one.
- Severity rationale on GAP-002 references the operational fact (9 of 14 critical vendors without sub-annual touchpoints) and pairs it with the supervisory exposure (operational-resilience exam scope). This is the kind of pairing that survives reviewer challenge.
- Cross-policy interactions are extensive (four other policies named, two linked-gap-ids cross-references). The matrix surfaces the dependencies and the one explicit conflict (GAP-004 with the Information Security Policy on subcontractor scoping). A vendor-policy refresh that ignored these interactions would create downstream inconsistency.
- Out-of-scope rationale is documented (non-ICT third parties, accepted by the Operational Risk Committee in 2018). This is the audit-defence artefact the matrix exists to surface.
- Coverage summary integer counts: 22 covered, 4 partial, 3 missing, 1 inconsistent, 1 outdated against 31 in-scope benchmark items. The matrix does not assert "we cover most of the rule" without the underlying counts.

## Downstream uses

- `issue-writeup` consumes GAP-002 (ongoing monitoring), GAP-003 (exit planning), and GAP-004 (subcontractor oversight) as findings to be papered into the firm's issue log; the operational-fact severity rationale carries directly into the CCCE structure.
- `obligation-mapping` confirms the obligation register carries OBL-TPRM-2023-IIIA through OBL-TPRM-2023-IIIE; if any are missing, the register reopens.
- `control-matrix` re-tests C-VND-001, C-VND-008, and C-VND-CYBER-001 in light of the policy fix; the operating-effectiveness ratings adjust for the refreshed policy text.
- `evidence-binder` consumes the `evidence_needed` arrays to scope the evidence pack the next operational-resilience exam will inspect, especially the exit-plan testing program and the material-subcontractor inventory.
- The cross-policy interactions feed parallel reviews of the Information Security Policy and the Operational Resilience Policy; both are scheduled for refresh and the gap matrix's interaction notes set the cross-policy working-session agenda.
