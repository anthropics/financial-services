# Example: AI use-case lifecycle gates for a regional bank

## Input

A US regional bank ($35B assets, OCC-supervised national bank, not yet at the Heightened Standards threshold but tracking towards it) is standing up an AI Governance Committee and needs a named gate matrix for the full AI use-case lifecycle. The bank already runs a Model Risk Committee for traditional models under SR 11-7; the AI committee will partner with the MRC for AI-extended models and stand alone for non-model AI use cases (operational AI, contact-center AI, document-extraction AI). Source posture is mixed: OCC Bulletin 2026-13, NIST AI RMF 1.0 and AI 600-1 Generative AI Profile, the firm's existing Model Risk Management Policy v4.1, and a draft AI Governance Policy v1.0. Risk tiering uses a tiered impact framework: T1 (high-impact, customer-facing or material financial-decision use cases), T2 (moderate-impact internal-decision use cases), T3 (low-impact operational use cases). Engagement scope is supplied: institution type national-bank, primary regulator OCC, persona Head of Model Risk Management, source posture mixed, sector overlay banking, cross-cutting overlay cyber. Audience is the AI Governance Committee adopting the matrix as charter language.

## Why this scenario matters

AI governance is one of the most-asked second-line topics in 2026 because the regulator constellation is unsettled (OCC 2026-13 plus NIST AI RMF plus EU AI Act for EU-touching firms plus state-DFS letters plus NAIC and state DOI bulletins for insurers). Banks frequently confuse AI governance with model risk governance and end up with one committee owning everything, which fails Heightened Standards-adjacent expectations on independent risk management and three-lines-of-defense. The example tests: distinct gates for distinct lifecycle stages; independence on a real specific control attribute (developer-validator separation under SR 11-7, layered for AI use cases); coordination with the Model Risk Committee for AI-extended models without collapsing the two committees; tier-driven gate intensity; the cyber overlay firing on customer-data-touching use cases; the gap where the firm has no formal annual review gate; and recommended charter language the committee can adopt.

## Output sketch (gate matrix excerpt)

```yaml
gate_matrix_id: GM-2026-AIGC-AI-Lifecycle-001
workflow_in_scope: "AI use-case lifecycle: intake, tiering, pre-prod, go-live, ongoing monitoring, retirement, for all AI use cases firm-wide."
scope_notes: "Includes AI-extended models (joint with Model Risk Committee). Excludes pure-research / sandbox-only AI work that has not exited research."
source_posture: mixed
engagement_id: ENG-2026-AIGC-Charter-Refresh

decision_authority:
  primary_committee: "AI Governance Committee (AIGC)"
  escalation_committee: "Operational Risk Committee, escalating to Board Risk Committee for material decisions"
  dissent_path: "Any AIGC member may record a dissent in the meeting minutes; a recorded dissent on a T1 go-live triggers automatic escalation to the Operational Risk Committee."
  board_oversight: "Annual report from AIGC chair to Board Risk Committee; quarterly summary of T1 use cases and material decisions."

gates:
  - gate_id: GATE-AI-001
    gate_name: "AI use-case intake gate"
    stage: intake
    trigger: "Submission of AI Use Case Intake Form by a business sponsor"
    required_reviewers:
      - role: "Head of AI Governance (firm-overlay path)"
        is_primary: true
        independence_required: false
      - role: "Business Sponsor (line 1)"
        is_primary: false
        independence_required: false
    required_inputs:
      - "AI Use Case Intake Form (firm-overlay-defined)"
      - "Business Sponsor attestation of intended use, data scope, model dependencies"
    decision_criteria:
      - criterion: "Use case is in scope of AI Governance (per firm-overlay AI definition; excludes traditional rule-based automation)"
        source_anchor: "references/firm-overlay.md#ai-definition"
      - criterion: "Sponsor has named accountable line-1 owner"
        source_anchor: "references/source-anchors.md#nist-ai-rmf-gv-2"
    stop_conditions:
      - "No proceed if no accountable line-1 owner is named"
      - "No proceed if intake form is incomplete on data scope or intended use"
    escalation_path:
      escalation_committee: "Operational Risk Committee"
      time_to_escalate: "Next scheduled AIGC meeting + 5 business days"
      escalation_owner: "Head of AI Governance"
    documentation_requirement:
      - "Intake decision in AIGC minutes"
      - "Intake form retained in GRC platform AI use-case record"
    frequency: event-based
    frequency_detail: "Submission of intake form by sponsor"
    source_anchor: "NIST AI RMF GV-2.1 (accountability structures); references/firm-overlay.md#aigc-charter"

  - gate_id: GATE-AI-002
    gate_name: "Risk tiering gate"
    stage: tiering
    trigger: "Completed intake; AIGC review of risk-tier classification within 10 business days of intake"
    required_reviewers:
      - role: "Head of AI Governance"
        is_primary: true
      - role: "Head of Model Risk Management"
        is_primary: false
        independence_required: true
        independence_basis: "SR 11-7 §VI; for AI-extended models, MRMO classification requires independence from developer"
      - role: "Head of Operational Risk"
        is_primary: false
      - role: "Chief Privacy Officer (when use case touches NPI)"
        is_primary: false
    required_inputs:
      - "Intake form with sponsor attestation"
      - "Data inventory (data sources, classification, NPI flag)"
      - "Use-case description with intended decision impact"
    decision_criteria:
      - criterion: "Tier classification (T1/T2/T3) is supported by the use-case impact assessment per firm tiering policy"
        source_anchor: "references/firm-overlay.md#ai-tiering-v2"
      - criterion: "Use case is or is not an AI-extended model (drives MRC coordination)"
        source_anchor: "OCC Bulletin 2026-13 §III.F; references/source-anchors.md#occ-2026-13"
    stop_conditions:
      - "No advance to pre-prod if tier classification is contested without resolution by the AIGC"
      - "No T1 classification without Chief Privacy Officer concurrence when NPI is in scope"
    escalation_path:
      escalation_committee: "Operational Risk Committee"
      time_to_escalate: "Within 10 business days of contested tiering"
      escalation_owner: "Head of AI Governance"
    documentation_requirement:
      - "Tiering decision with rationale in AIGC minutes"
      - "Tiering memorandum retained in GRC platform"
    frequency: event-based
    source_anchor: "OCC Bulletin 2026-13; NIST AI RMF MAP function; references/firm-overlay.md#ai-tiering-v2"

  - gate_id: GATE-AI-003
    gate_name: "Pre-prod gate (T1 and T2)"
    stage: pre-prod
    trigger: "Use case ready for pre-production deployment; T3 use cases skip this gate per firm tiering policy"
    required_reviewers:
      - role: "Head of AI Governance"
        is_primary: true
      - role: "Independent Validator (line 2; for AI-extended models, the Model Risk validator)"
        is_primary: false
        independence_required: true
        independence_basis: "SR 11-7 §V; OCC Bulletin 2026-13 §III.E; firm AI Governance Policy v1.0 §4.2"
      - role: "CISO (when cyber overlay loaded)"
        is_primary: false
        independence_basis: "NYDFS §500.4 (where covered); firm cyber policy"
      - role: "Head of Model Risk Management (for AI-extended models; joint MRC coordination)"
        is_primary: false
    required_inputs:
      - "Model card per `model-card-builder` skill"
      - "Validation report per `validation-report` skill (or model-validator equivalent)"
      - "Issue log status — no open critical or high issues against the use case"
      - "Cyber security architecture review for use cases touching customer data or privileged systems"
    decision_criteria:
      - criterion: "Validation independence is established (validator is not the developer; documented chain)"
        source_anchor: "references/source-anchors.md#sr-11-7"
      - criterion: "Model card is complete per firm template"
        source_anchor: "references/firm-overlay.md#model-card-template"
      - criterion: "No open critical or high issues against the use case"
        source_anchor: "references/source-anchors.md#sr-11-7"
      - criterion: "Cyber architecture review is complete with no unmitigated high-severity findings (when in scope)"
        source_anchor: "references/cross-cutting/cyber.md#architecture-review"
    stop_conditions:
      - "No advance to go-live with any open critical or high issue"
      - "No advance with missing model card or validation report"
      - "No advance with validator-developer overlap (independence violation)"
      - "No advance with unmitigated cyber high-severity findings"
    escalation_path:
      escalation_committee: "Operational Risk Committee (joint with Model Risk Committee for AI-extended models)"
      time_to_escalate: "Next scheduled committee meeting"
      escalation_owner: "Head of AI Governance"
    documentation_requirement:
      - "Pre-prod gate decision with attesters in AIGC minutes"
      - "Validation report and model card retained in GRC platform AI use-case record"
      - "Issue log snapshot retained as gate evidence"
    frequency: event-based
    source_anchor: "SR 11-7 §V, §VI; OCC Bulletin 2026-13 §III.E; references/source-anchors.md#sr-11-7"

  - gate_id: GATE-AI-004
    gate_name: "T1 production go-live gate"
    stage: go-live
    trigger: "T1 use case ready for production; T2 and T3 use cases pass through a lighter go-live workflow that does not require AIGC committee gate"
    required_reviewers:
      - role: "AI Governance Committee (committee decision; not individual reviewer)"
        is_primary: true
      - role: "Head of Model Risk Management (for AI-extended models)"
        is_primary: false
        independence_required: true
      - role: "Business Head (line 1 sponsor)"
        is_primary: false
      - role: "CISO (when cyber overlay loaded)"
        is_primary: false
      - role: "Chief Privacy Officer (when NPI in scope)"
        is_primary: false
    required_inputs:
      - "All pre-prod gate evidence"
      - "Production-readiness assessment (operations, monitoring, incident-response)"
      - "Business owner attestation of go-live readiness"
      - "Annual-review schedule populated in GRC platform"
    decision_criteria:
      - criterion: "All pre-prod gate criteria continue to be satisfied"
        source_anchor: "references/source-anchors.md#sr-11-7"
      - criterion: "Production monitoring plan is complete with named monitoring owner and named thresholds"
        source_anchor: "NIST AI RMF MEASURE function; references/firm-overlay.md#monitoring-plan"
      - criterion: "Annual-review date is scheduled in GRC platform"
        source_anchor: "OCC Bulletin 2026-13 §III.E; firm AI Governance Policy v1.0 §6.1"
    stop_conditions:
      - "No go-live without unanimous AIGC concurrence on T1 use case"
      - "No go-live without scheduled annual-review date"
      - "No go-live for AI-extended models without Model Risk Committee concurrence"
    escalation_path:
      escalation_committee: "Board Risk Committee (for T1 go-live; AIGC dissent or split vote escalates)"
      time_to_escalate: "Next Board Risk Committee meeting; emergency convening for material delay"
      escalation_owner: "AI Governance Committee Chair"
    documentation_requirement:
      - "Go-live decision in AIGC minutes with named attesters and any recorded dissents"
      - "Production-readiness assessment retained in GRC platform"
      - "Cross-reference to MRC minutes for AI-extended models"
    frequency: event-based
    source_anchor: "SR 11-7 §VI; OCC Bulletin 2026-13 §III.E and §III.F; references/source-anchors.md#occ-2026-13"

  - gate_id: GATE-AI-005
    gate_name: "Annual review gate"
    stage: ongoing-monitoring
    trigger: "Annual review date for any in-production AI use case (cadence per tier: T1 annual; T2 annual or 18-month per AIGC discretion; T3 every 24 months or on material change)"
    required_reviewers:
      - role: "Head of AI Governance"
        is_primary: true
      - role: "Independent Validator (refresh validation for T1)"
        is_primary: false
        independence_required: true
      - role: "Business Owner"
        is_primary: false
      - role: "CISO (refresh cyber review when applicable)"
        is_primary: false
    required_inputs:
      - "Production monitoring history since last review"
      - "Issue log against the use case"
      - "Refresh validation report (T1) or refresh assessment (T2/T3)"
      - "Updated model card with any material changes"
    decision_criteria:
      - criterion: "Use case continues to perform within established tolerances"
        source_anchor: "NIST AI RMF MEASURE/MANAGE; firm monitoring policy"
      - criterion: "No accumulated open critical or high issues unresolved"
        source_anchor: "references/source-anchors.md#sr-11-7"
      - criterion: "Use case continues to fit firm tiering classification (re-tier if necessary)"
        source_anchor: "references/firm-overlay.md#ai-tiering-v2"
    stop_conditions:
      - "No continued production if material drift in performance is unmitigated"
      - "No continued production with unresolved critical issues"
      - "Re-tier required if use case has materially changed since last review"
    documentation_requirement:
      - "Annual review decision in AIGC minutes"
      - "Refresh validation / assessment retained in GRC platform"
      - "Updated model card retained"
    frequency: annual
    frequency_detail: "Annual for T1 and T2 (T2 may extend to 18 months at AIGC discretion); 24-month or on-material-change for T3"
    source_anchor: "OCC Bulletin 2026-13 §III.E; NIST AI RMF MANAGE function; firm AI Governance Policy v1.0 §6.1"

gate_gaps:
  - implied_gate_name: "Annual review gate"
    gap_description: "Current workflow has no formal annual-review gate for in-production AI use cases. SR 11-7 §V (model validation refresh) and OCC Bulletin 2026-13 §III.E (refreshed effective challenge) imply periodic refresh; firm has been performing ad-hoc refresh on a use-case-by-use-case basis without a calendar mechanism."
    source_anchor: "references/source-anchors.md#sr-11-7; references/source-anchors.md#occ-2026-13"
    recommended_action: "Adopt GATE-AI-005 as drafted; populate annual-review schedule in GRC platform for all in-production AI use cases within 90 days of charter adoption."
  - implied_gate_name: "Third-party AI / vendor-AI gate"
    gap_description: "Current workflow does not separately gate vendor-provided AI use cases (vendor models, vendor-AI-extended platforms). NIST AI RMF GV-6 (third-party considerations) and OCC Bulletin 2026-13 §III.G (third-party model gate expectations) imply vendor-AI use cases require coordinated AIGC and Vendor Risk Committee gates."
    source_anchor: "references/source-anchors.md#nist-ai-rmf; references/source-anchors.md#occ-2026-13"
    recommended_action: "Add vendor-AI specific intake and onboarding gate that coordinates AIGC and VRC; align documentation cadence with TPRM ongoing-monitoring."

recommended_charter_language: |
  The AI Governance Committee (the Committee) is the firm's primary governance body for artificial intelligence use cases across the AI lifecycle from intake through retirement. The Committee operates with decision authority on use cases at all tier levels, with specific gating responsibility for tier-1 production go-live decisions.

  The Committee carries five named gates. Intake gates ensure every AI use case is registered with named line-1 ownership before development proceeds. Tiering gates classify use cases by impact, with the Committee's classification driving downstream gate intensity. Pre-production gates apply to tier-1 and tier-2 use cases and require complete model documentation, independent validation, and (where applicable) cyber and privacy concurrence before any production deployment. Tier-1 production go-live gates require unanimous Committee concurrence with a scheduled annual-review date in the firm's governance system; tier-1 dissents escalate to the Operational Risk Committee with onward escalation to the Board Risk Committee at the Chair's discretion. Annual review gates apply to in-production use cases with cadence by tier and are the mechanism through which the Committee maintains effective challenge over the production AI portfolio.

  For AI-extended models, the Committee coordinates with the Model Risk Committee with both committees concurring on tier-1 production go-live. The Committee reports to the Board Risk Committee annually on the AI use-case portfolio, the gate-decision history, and any material exceptions or dissents. The Committee's gate decisions are documented in the meeting minutes with named attesters and any recorded dissents; documentation is retained in the firm's governance system per the firm's records-retention schedule.

reviewer_questions:
  - "Should the AIGC and the Model Risk Committee adopt joint quorum requirements for AI-extended-model T1 go-live decisions, or is sequential sign-off sufficient?"
  - "For T2 use cases, is annual review the right cadence or should the firm adopt an 18-month cadence with on-material-change triggers as the default?"
  - "Does the firm need to separately stand up a third-party AI gate as recommended in the gap section, or is the existing Vendor Risk Committee sufficient with a charter amendment that flags vendor-AI as a distinct category?"
  - "Where the AIGC has Chief Privacy Officer concurrence required, is the CPO function staffed at sufficient stature to act as a true independent reviewer, or does this need a structural lift before charter adoption?"

confidence_label: medium
human_review_required: true
```

## What the matrix surfaces

- **Five distinct gates with real spine**. Intake, tiering, pre-prod, go-live, annual review. Each has a real trigger, named reviewers with independence flagged where source guidance demands, declarative stop conditions, and named documentation. Not ten gates padded for comprehensiveness.
- **Tier-driven gate intensity**. T1 use cases hit all five gates; T2 skips the formal go-live committee gate but still hits pre-prod and annual review; T3 skips pre-prod but is annual-reviewed at lighter cadence. The matrix encodes the firm's risk-based proportionality.
- **Validator independence on AI-extended models**. The independence_required flag fires on the Independent Validator slot at pre-prod and annual review, with the source anchor citing SR 11-7 §V and the firm's AI Governance Policy. The matrix names the structural separation explicitly.
- **MRC coordination without committee collapse**. AI-extended models flow through both the AIGC and the MRC; the matrix names the coordination without collapsing the two committees. The gap section does not flag this as a redundancy because the AIGC's scope is broader (non-model AI) and the MRC's scope is narrower (model risk).
- **Cyber overlay firing on customer-data use cases**. The CISO is named as a required reviewer at pre-prod and annual review when the cyber overlay is loaded; the source anchor cites the cyber overlay file path.
- **Real gap surfaced**. The annual-review gate is implied by source guidance but does not exist in the firm's current workflow; the gap is explicit with the source anchor and the recommended action. A clean-looking matrix with no gap usually means the gap was buried.
- **Recommended charter language as adoptable prose**. Three paragraphs that read as charter language, not as matrix commentary. The committee can adopt the language directly into its terms of reference.
- **Reviewer questions that point to live decisions**. Joint quorum, T2 cadence, third-party AI gate, CPO stature. Each question points to a specific decision the committee will need to make.

## Downstream uses

- `model-card-builder` references GATE-AI-003 (pre-prod) and GATE-AI-004 (T1 go-live) in the model card's sign-off block; T1 model cards trace through both AIGC and MRC.
- `vendor-diligence` references the third-party-AI gap and (post-remediation) the vendor-AI specific gate.
- `risk-committee-pack` for the next AIGC reads GATE-AI-005 (annual review) and surfaces overdue annual reviews; for the next Board Risk Committee reads the AIGC quarterly summary and flags any T1 dissent escalations.
- `issue-writeup` for any issue against an AI use case links to the relevant gate via the issue's linked-control-id, and the issue's severity drops the use case's "current effective challenge" rating until closure.
