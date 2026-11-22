# Example: internal AI use-case intake at an SEC-registered investment adviser

## Input

A medium-sized RIA with $50B AUM has stood up an AI governance program and is running its first cycle of AI use-case intake reviews. The newly hired AI Governance Lead and the CCO want a structured engagement charter so every intake review follows a consistent scope, persona, and review-gate set. This is internal second-line work, not advisory. The deliverable is a recurring intake-review playbook anchored to a written charter.

## Why this scenario matters

This is the second canonical use of the skill: an internal 2-line function setting up its operating model. The persona is not an advisory partner; it is an AI Governance Lead with named review committees. Source posture is public-plus-firm-policy (no system-of-record connectors yet, model inventory forthcoming). The risk lens is broader than the advisory-bank example: model risk, operational, reputational, conduct, fiduciary. Sector overlay is capital-markets, not banking, so different regulator constellation and different review machinery downstream.

## Output sketch

```yaml
engagement_id: ENG-2026-AIG-INTAKE-01
engagement_summary: >
  Charter for the recurring AI use-case intake review cycle at an SEC-registered
  investment adviser. Establishes institution context, persona, review gates,
  and overlay set so each individual intake review runs against a consistent
  scope. Excludes vendor-side AI used by the firm's auditor and third-party-
  manager AI used by underlying funds.
as_of_date: 2026-05-06

institution:
  type: investment-adviser
  asset_size_band: not-applicable
  charter: Delaware LP general partner; investment adviser registered under
    Investment Advisers Act of 1940
  registrations: [SEC IARD (Form ADV), state notice filings in 12 states]
  geographic_footprint: [principal office NY, satellite offices in CA and CT]
  primary_regulators:
    - regulator: SEC EXAMS
      relationship_type: examiner
    - regulator: SEC Division of Investment Management
      relationship_type: rule-issuer
    - regulator: NYDFS
      relationship_type: functional-regulator
      notes: cyber regulation Part 500 applicability
  recent_supervisory_posture:
    - Most recent SEC exam closed in 2024 with no deficiency letter; one
      informal observation on marketing-rule disclosures

engagement:
  type: internal-review
  sponsor: Chief Compliance Officer
  audience: [AI Risk Committee, CCO, CRO, fund boards (informational)]
  timeframe:
    start: 2026-05-06
    target_completion: ongoing (charter reviewed annually)
    milestones:
      - {label: charter sign-off, date: 2026-05-20}
      - {label: first three intake reviews complete, date: 2026-07-01}
      - {label: first annual charter review, date: 2027-05-06}
  deliverable_shape: charter
  charter_reference: AIG-CHARTER-2026-V1

persona:
  role: AI-governance-lead
  function: AI governance (2-line, hybrid risk-and-compliance reporting line)
  decision_rights:
    - tier each intaked AI use case
    - approve or escalate model cards before pre-prod gate
  review_gates:
    - AI Risk Committee review for any use case tiered medium or above
    - CCO sign-off on any use case touching marketing, suitability, or
      adviser-client communications
    - CRO sign-off on any use case carrying model risk classification
    - Fund-board notification for any use case affecting fund operations

source_posture: public-plus-firm-policy
connectors_enabled: []
confidentiality_posture: firm-restricted

risk_lens: [model, operational, reputational, conduct, fiduciary]
risk_taxonomy_reference: firm risk taxonomy v2.1 (in references/firm-overlay.md)

sector_overlay_set: [capital-markets]
cross_cutting_overlay_set: [cyber, privacy]

out_of_scope:
  - vendor-side AI used by the firm's external auditor
  - AI used by third-party managers in the funds the adviser allocates to
  - personal-use AI tools by employees outside firm-issued endpoints

assumptions_and_dependencies:
  - Marketing-rule status quo for AI-generated marketing claims
  - SEC predictive-data-analytics rule current state [verify section]
  - Model inventory connector becomes available 2026-Q3

open_questions:
  - Whether NYDFS Part 500 cyber controls apply to all AI use cases or only
    those handling NPI [verify section]
  - Whether NAIC AI Bulletin applies indirectly via insurance-affiliated funds

revisions:
  - date: 2026-05-06
    reason: initial charter
    delta: created
    approved_by: AI Governance Lead, CCO
```

## Why the scope shape matters downstream

- `ai-use-case-intake` reads `persona.review_gates` to know which committees see each intake.
- `ai-risk-tiering` reads `risk_lens` and `cross_cutting_overlay_set` to load matching tiering criteria.
- `model-card-builder` reads `institution.type` to set documentation tone (adviser-relationship language, not bank-supervision language).
- The `out_of_scope` list is the firewall against the program being asked to opine on third-party-manager AI, which is a different review entirely.
- Source posture being `public-plus-firm-policy` (not `connector-aware`) keeps downstream skills from asking for evidence that the firm cannot yet produce.
