# Example: legacy SR 11-7-aligned MRM policy benchmarked against the April 2026 joint guidance

## Input

A national bank's Model Risk Management Office is reviewing the firm's Model Risk Management Policy ahead of an OCC safety-and-soundness examination scheduled for the second half of 2026. The policy was last refreshed in 2019 and is anchored on SR 11-7. The Joint Interagency Revised Guidance on Model Risk Management (OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026, April 17, 2026) was published earlier in 2026 and the bank's Model Risk Committee directed the MRMO to identify gaps before the exam. The bank holds total assets above $30 billion, so the joint guidance is supervisor-relevant. Source posture is mixed: SR 11-7 and the April 2026 joint guidance (public) plus the firm's MRM policy v6.1 (firm-policy overlay) and a supporting Model Validation Standard v3.0 (firm-policy overlay). Sector overlay: banking. No cross-cutting overlays loaded; this matrix is policy-on-policy and does not run cyber rows.

The bank also has GenAI in production (customer-service summarisation, internal knowledge retrieval) and is piloting agentic-AI use cases in operations. GenAI and agentic-AI governance are explicitly out of scope of the April 2026 joint guidance (footnote 3); the gap matrix treats them as a separate workstream and does not benchmark MRM-policy sections against the bulletin for those uses. The Head of Model Risk has commissioned a parallel AI-policy gap review against NIST AI RMF 1.0, NIST AI 600-1, and the firm's draft AI Governance Framework; that review is referenced in this matrix's cross-policy-interactions section but is not this matrix's subject.

## Why this scenario matters

This is the canonical legacy-SR 11-7-vs-April-2026-joint-guidance application of the matrix for traditional models. The April 2026 joint guidance refreshes the SR 11-7 frame for traditional statistical and quantitative models and non-generative, non-agentic AI models; it also explicitly excludes GenAI and agentic AI from scope. Policies anchored only to SR 11-7 (which describes most US banks' MRM policies) typically carry `outdated` or `partial` rows when benchmarked against the April 2026 refresh on the traditional-model side. The example tests three things at once: the discipline of classifying gaps for traditional-model coverage, the severity rationale (supervisory exposure under an active 2026 exam cycle, the bank's scale above the $30 billion supervisory-relevance threshold), and the recommended-edit fragments at a level the policy-rewrite team can work from. The example also shows the discipline of routing GenAI / agentic-AI policy gaps to a separate workstream rather than collapsing them into the joint-guidance matrix.

## Output sketch

```yaml
review_id: PGR-2026-MRM-04
as_of_date: 2026-05-06
engagement_id: ENG-2026-MRM-EXAM-PREP

policy_under_review:
  policy_name: "Model Risk Management Policy"
  policy_version: "v6.1"
  effective_date: 2019-09-15
  owner_role: "Head of Model Risk"
  document_identifier: "intranet:/policies/risk/mrm/v6.1"
  supporting_artefacts:
    - {artefact_name: "Model Validation Standard", artefact_version: "v3.0", owner_role: "Head of Model Validation"}

benchmark_sources:
  - {source_name: "SR 11-7 / OCC Bulletin 2011-12 — Supervisory Guidance on Model Risk Management",
     edition: "April 4, 2011 (superseded April 17, 2026)",
     section_references: ["§IV development, implementation, and use", "§V validation", "§VI governance, policies, and controls"]}
  - {source_name: "Joint Interagency Revised Guidance on Model Risk Management — OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026",
     edition: "April 17, 2026",
     section_references: ["Section II (scope and definitions)", "Section III (control environment, third-party model controls)"]}

scope_of_review:
  - {policy_section: "§2 Definitions and scope", benchmark_sources_used: ["April 2026 joint guidance Section II"]}
  - {policy_section: "§3 Model lifecycle", benchmark_sources_used: ["SR 11-7 §IV", "April 2026 joint guidance Section III"]}
  - {policy_section: "§4 Validation", benchmark_sources_used: ["SR 11-7 §V"]}
  - {policy_section: "§5 Governance and roles", benchmark_sources_used: ["SR 11-7 §VI", "April 2026 joint guidance Section III"]}
  - {policy_section: "§6 Third-party models", benchmark_sources_used: ["April 2026 joint guidance Section III"]}

source_posture: mixed

gaps:
  - gap_id: GAP-001
    benchmark_requirement: "Firm policy reflects the April 2026 refreshed model definition and scope (statistical / quantitative models and non-generative, non-agentic AI models in scope; simple arithmetic / spreadsheet calculations, deterministic rule-based processes, GenAI and agentic AI explicitly out of scope)."
    benchmark_source_anchor: {source_name: "OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026", section: "Section II (scope and definitions)"}
    policy_text_excerpt: "§2 definitions cover statistical and machine-learning models; the definition predates the April 2026 refresh and does not articulate the inclusion of non-generative, non-agentic AI models or the explicit exclusion of GenAI and agentic AI from this policy's scope."
    policy_location: "§2 Definitions and scope"
    gap_classification: outdated
    severity: high
    severity_rationale: "Joint guidance was published April 17, 2026; an exam under the refreshed framing is scheduled for H2 2026. Bank holds assets above $30 billion (the joint guidance's supervisory-relevance threshold). The model definition in §2 has not been refreshed since 2019. No compensating practice in place. Distinguishing the in-scope traditional / non-generative-AI population from the out-of-scope GenAI / agentic-AI population in the policy itself is the cleanest way to avoid a supervisory finding that the firm's MRM policy is silent on the post-2026 frame."
    recommended_edit: "Refresh §2 with the joint guidance's model definition; articulate the inclusion of non-generative, non-agentic AI models within the model inventory; articulate the exclusion of GenAI and agentic AI from this policy and reference the firm's separate AI Governance Framework as the controlling policy for those uses; preserve the spreadsheet / deterministic-rule exclusions consistent with the joint guidance."
    evidence_needed:
      - "Refresh of Model Inventory taxonomy in the GRC platform to reflect refreshed definition"
      - "Training session for model owners on refreshed scope"
      - "Cross-reference between MRM policy and AI Governance Framework so the boundary between the two is unambiguous"
    linked_obligation_ids: [OBL-MRM-2026-DEF]
    linked_control_ids: [C-MRM-INV-001]
    owner_role: "Head of Model Risk"

  - gap_id: GAP-002
    benchmark_requirement: "Firm policy articulates the control environment refresh in Section III: roles for development, validation, use, and ongoing monitoring; segregation between developer and validator; material model change management triggers."
    benchmark_source_anchor: {source_name: "OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026", section: "Section III (control environment)"}
    policy_text_excerpt: "§5.2 names roles for development, validation, and use. Segregation between developer and validator is implicit in role definitions but not articulated. Material change management is in §3.4 but the trigger criteria are not named."
    policy_location: "§5.2 Roles, §3.4 Change management"
    gap_classification: weak
    severity: moderate
    severity_rationale: "Policy addresses the topics but at lower rigor than Section III expects. Segregation expectations are implicit rather than articulated; change-management triggers are unspecified. Compensating practice: MRMO operating procedures cover both, but operating procedures sit below the policy in the firm's hierarchy."
    recommended_edit: "Refresh §5.2 to articulate segregation between developer and validator as an explicit control attribute (validator is independent of development team and reports through the Model Risk function). Refresh §3.4 to name change-management triggers: feature change, training-window shift, score-cutoff change, performance-breach-driven re-fit."
    evidence_needed:
      - "Updated MRMO RACI consistent with refreshed §5.2"
      - "Change-management workflow refresh in the Model Inventory"
    linked_obligation_ids: [OBL-MRM-2026-CTRL, OBL-SR11-7-VI]
    linked_control_ids: [C-MRM-301]
    owner_role: "Head of Model Risk"

  - gap_id: GAP-003
    benchmark_requirement: "Firm policy addresses third-party model controls including vendor model documentation, validation expectations on vendor models, and ongoing monitoring of vendor-model performance."
    benchmark_source_anchor: {source_name: "OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026", section: "Section III (third-party model controls)"}
    policy_text_excerpt: "§6 Third-party models requires that vendor models be 'validated where feasible' and references the firm's Vendor Management Policy for ongoing monitoring."
    policy_location: "§6 Third-party models"
    gap_classification: partial
    severity: moderate
    severity_rationale: "Policy addresses vendor models but at lower rigor than the joint guidance's Section III expects. 'Validated where feasible' is a hedge that the joint guidance narrows; bank's vendor-model inventory includes three Tier-1 models on the lending side. Compensating practice: firm-side reduced-form testing on vendor model outputs is documented in the Validation Standard, but reduced-form testing alone does not satisfy the joint guidance's third-party-model expectations."
    recommended_edit: "Replace §6.2 'validated where feasible' with explicit expectations under the joint guidance's third-party-model controls: vendor-model documentation review, conceptual-soundness assessment, ongoing-performance monitoring with named KRIs, and a documented basis for any feasibility-based limitation on validation depth."
    evidence_needed:
      - "Refresh of Vendor Model Validation Standard"
      - "Per-vendor-model validation work papers reflecting the refreshed standard"
      - "Cross-policy alignment with Vendor Management Policy on monitoring KRIs"
    linked_obligation_ids: [OBL-MRM-2026-3P]
    linked_control_ids: [C-MRM-VND-002]
    owner_role: "Head of Model Risk"

  - gap_id: GAP-004
    benchmark_requirement: "Firm policy reflects the joint guidance's documentation expectations for the model-validation evidence pack at the supervisory-relevance threshold."
    benchmark_source_anchor: {source_name: "OCC Bulletin 2026-13 / FRB SR 26-2 / FDIC FIL-15-2026", section: "Section III (documentation expectations)"}
    policy_text_excerpt: "§4 Validation references SR 11-7 §V categories (conceptual soundness, ongoing monitoring, outcomes analysis, benchmarking) but does not reflect the documentation expectations articulated in the April 2026 refresh."
    policy_location: "§4 Validation, §4.6 Documentation expectations"
    gap_classification: outdated
    severity: moderate
    severity_rationale: "Policy reflects the prior framing. The joint guidance is non-binding (does not set forth enforceable standards), but supervisory examination teams have signalled they will read against the refreshed framing. Compensating practice: validation reports on Tier-1 models already reflect a richer documentation discipline than §4 prescribes."
    recommended_edit: "Refresh §4.6 to incorporate the joint guidance's documentation expectations for validation packs and tie them to the firm's Validation Standard so the actual evidence pack discipline is reflected at policy-tier."
    evidence_needed:
      - "Refresh of Model Validation Standard documentation section"
      - "Updated validation report template that surfaces the refreshed documentation expectations"
    linked_obligation_ids: [OBL-MRM-2026-DOC]
    linked_control_ids: [C-MRM-VAL-DOC-001]
    owner_role: "Head of Model Risk"

coverage_summary:
  total_benchmark_items: 22
  covered_items: 18
  partial_items: 1
  missing_items: 0
  inconsistent_items: 0
  outdated_items: 3

out_of_scope_items:
  - item: "Generative AI and agentic AI model governance"
    rationale: "Footnote 3 of the joint April 2026 guidance excludes GenAI and agentic AI from scope. GenAI and agentic-AI policy gaps are addressed in a separate workstream benchmarking the firm's draft AI Governance Framework against NIST AI RMF 1.0, NIST AI 600-1 (Generative AI Profile), and ISO/IEC 42001. Cross-referenced under cross-policy interactions."
  - item: "Bank Secrecy Act / Anti-Money Laundering model risk (formerly SR 21-8)"
    rationale: "SR 21-8 was superseded by the April 2026 joint guidance. The BSA/AML model population is covered by this matrix to the extent BSA/AML models are traditional statistical or quantitative models; BSA/AML-specific exam manual provisions remain a separate benchmark for sanctions-screening model tuning evidence and are addressed in the BSA/AML model-monitoring matrix."

cross_policy_interactions:
  - other_policy: "Vendor Management Policy v4.2"
    interaction_type: dependency
    description: "GAP-003 (third-party model controls) requires alignment with the Vendor Management Policy on monitoring KRIs and ongoing-performance review cadence. Co-fix needed; routing to Head of Vendor Management."
    linked_gap_ids: [GAP-003]
  - other_policy: "AI Governance Framework (draft, separate workstream)"
    interaction_type: dependency
    description: "GAP-001 names the boundary between MRM-policy scope (traditional / non-generative, non-agentic models) and AI Governance Framework scope (GenAI and agentic AI). The AI Governance Framework is being benchmarked separately against NIST AI RMF 1.0, NIST AI 600-1, and ISO/IEC 42001. Both refreshes need to land together so the boundary is unambiguous."
    linked_gap_ids: [GAP-001]

recommended_next_steps:
  - "Draft revisions on §2 (definitions and scope), §3.4 (change management), §4.6 (documentation), §5.2 (roles), §6.2 (third-party models) ready for legal review by 2026-06-15."
  - "Route to Compliance and Risk Committee for tabling on 2026-07."
  - "Schedule policy-owner working session with Head of Vendor Management on cross-policy alignment by 2026-06-01."
  - "Coordinate sequencing with the AI Governance Framework gap review so the MRM-policy / AI-policy boundary lands cleanly."
  - "Schedule training refresh on changed sections within 60 days of approval."

confidence_label: high

reviewer_questions:
  - "GAP-001 severity is rated `high` based on the published April 2026 timing and the H2 2026 exam scope. Should severity escalate to `critical` if the exam window opens before recommended-edit approval?"
  - "GAP-001's recommended edit references the firm's separate AI Governance Framework as the controlling policy for GenAI and agentic AI. The AI Governance Framework is currently in draft and not yet board-approved. Should the MRM-policy refresh wait, or should §2 carry a pointer to 'AI Governance Framework or its successor' for now?"
  - "GAP-003 references the Vendor Management Policy as a dependency. The Vendor Management Policy is itself due for refresh against the June 2023 interagency TPRM guidance; should the two refreshes be sequenced or coupled?"

human_review_required: true

revisions:
  - {date: 2026-05-06, reason: "initial review", delta: "created during MRM exam-prep engagement", approved_by: "Head of Model Risk"}
```

## What the matrix surfaces

- The `outdated` classification fires twice (GAP-001 — refreshed model definition and scope; GAP-004 — documentation expectations). The `weak` classification fires once (GAP-002 — articulation of segregation and change-management triggers). The `partial` classification fires once (GAP-003 — third-party models). The matrix discipline distinguishes the classifications rather than collapsing them.
- Severity rationale on each row references supervisory exposure (active H2 2026 exam cycle; supervisory-relevance threshold met at $30B), materiality (three Tier-1 vendor models, validation evidence on Tier-1 models), and compensating practice (operating procedures, firm-side reduced-form testing). Severity is paired with rationale, not asserted.
- Coverage summary is integer counts. The matrix does not assert "we cover most of the joint guidance"; it carries 18 covered, 1 partial, 0 missing, 2 outdated, 0 inconsistent against 22 in-scope benchmark items.
- Out-of-scope items name the GenAI / agentic-AI exclusion explicitly (per footnote 3) and route those gaps to a separate AI Governance Framework workstream. The matrix does not benchmark the MRM policy against the joint guidance for GenAI or agentic-AI uses; doing so would misrepresent the bulletin's scope.
- Cross-policy interactions are surfaced explicitly. The Vendor Management Policy interaction creates a dependency that the recommended-next-steps block routes to the head of vendor management. The AI Governance Framework dependency makes the MRM-policy / AI-policy boundary visible.
- Recommended edits are declarative and at summary-draft level. They name the policy section, the change, and what the changed text accomplishes.

## Downstream uses

- `issue-writeup` consumes GAP-001, GAP-002, and GAP-004 as findings to be papered with severity, owner, and target date for the firm's issue log; the supervisory exposure rationale carries directly into the severity_rationale field of the issue write-up.
- `obligation-mapping` consumes the gap rows whose `linked_obligation_ids` reference the April 2026 joint guidance to confirm the obligation register carries the refreshed-scope rows; if not, the obligation register reopens.
- `control-matrix` consumes GAP-002 and GAP-003 against C-MRM-301 and C-MRM-VND-002; the operating-effectiveness rating on those rows is re-tested in light of the policy fix.
- `evidence-binder` consumes the `evidence_needed` arrays to scope the evidence pack the next exam will inspect.
- The AI Governance Framework gap review (separate workstream) consumes the cross-policy-interactions row that names the MRM-policy / AI-policy boundary.
- The downstream `regulatory-change-management/policy-diff` skill (when the rewrite ships) compares v6.1 to v6.2 and confirms the recommended edits landed; the gap matrix sets the v6.2 acceptance criteria.
