# Example: BCBS 239 risk-reporting completeness exception

## Input

The internal audit team at a $40B regional bank (foreign banking organization, US IHC) has tested the monthly market-risk pack against BCBS 239 Principle 4 (completeness) for the period 2026-01 through 2026-03. Two material counterparty exposures totalling $187M notional were excluded from the consolidated counterparty view on three reporting cycles because the upstream feed cutoff time preceded the source-system close on the affected days. The internal audit team has confirmed the condition with the Credit Risk Reporting team and is writing up the issue. Persona is the Internal Audit Senior Manager (3-line independent), audience is the firm's Audit Committee with a copy to the Board Risk Committee. Source posture is mixed: BCBS 239 (public) and the firm's risk-data-aggregation policy (firm-policy overlay).

## Why this scenario matters

This is the canonical CCCE construction on a risk-data finding. The condition is dated, scoped, and quantified. The criteria is BCBS 239 Principle 4 with a section reference, not "per BCBS 239 generally". The cause is the feed-orchestration cutoff time tied to a specific control attribute (the reconciliation control that did not catch the truncated population), not "feed timing issue". The effect quantifies the under-stated counterparty exposure and notes the downstream propagation into the executive risk pack distributed to the Board Risk Committee. The example also tests the discipline that severity is paired with rationale, that closure evidence is the artifact and not the verb, and that the source-source-anchors path is referenced rather than restated.

## Output sketch

```yaml
issue_id: ISS-2026-IA-BCBS239-007
title: "Counterparty exposure feed truncation excludes material exposures from monthly market-risk pack on three cycles"
engagement_id: ENG-2026-IA-BCBS239-MarketRisk
as_of_date: 2026-04-22
status: under-review

source:
  source_type: internal-audit
  source_id: IA-WP-2026-MR-014
  # regulator omitted; not examiner-issued

date_identified: 2026-04-15
period_start: 2026-01-01
period_end: 2026-03-31

condition: |
  On three monthly reporting cycles (2026-01, 2026-02, 2026-03), two material counterparty
  exposures totalling $187M notional were excluded from the consolidated counterparty view in
  the monthly market-risk pack. The upstream feed cutoff time (T+1 04:00 ET) preceded the
  source-system close (T+1 06:00 ET) on those three cycles because of a quarterly batch-window
  shift the feed-orchestration team applied without adjusting the downstream cutoff. The two
  exposures appeared in the counterparty source system before the source-system close but after
  the feed cutoff. The reconciliation control between the source-system extract and the pack
  input did not catch the truncated population because the reconciliation runs against the post-cutoff
  feed file, not against the source-system close.

criteria: |
  BCBS 239 Principle 4 (Completeness) — risk data aggregation capabilities should capture and
  aggregate all material risk data across the banking group, with exceptions identified and
  explained. BCBS 239 Principle 7 (Accuracy) — risk reports should accurately and precisely
  convey aggregated risk data. Firm Risk Data Aggregation and Reporting Policy v4.2 §3.2 on
  data-completeness controls and §3.4 on reconciliation discipline.
criteria_source_anchor: "references/source-anchors.md#bcbs-239 and references/firm-overlay.md#rdar-policy-v42"

cause: |
  The reconciliation control (C-CRR-001) is designed to compare the pack input file against
  the post-cutoff feed file rather than against the source-system close-of-day position. When
  the feed cutoff and the source-system close diverge, the reconciliation control passes against
  a truncated population without flagging the truncation. The control's design assumes the feed
  cutoff equals the source-system close; that assumption became false when the feed-orchestration
  team shifted the batch window without coordinating with the reconciliation control owner.

impact: |
  Financial: counterparty exposure under-stated by $187M notional on three reporting cycles in
  Q1 2026; the under-statement propagated into the monthly market-risk pack distributed to the
  Board Risk Committee on 2026-02-05, 2026-03-05, and 2026-04-05. Regulatory: the firm's
  compliance posture on BCBS 239 Principle 4 is impaired for the affected period; the open
  point will surface in the next OCC continuous-monitoring review of risk-data aggregation.
  Operational: re-issuance of the affected packs is required for the audit committee's record;
  the firm's BCBS 239 self-assessment for 2026-H1 will reflect a partially-effective rating on
  Principle 4. No customer or reputational impact identified.

severity: high
severity_rationale: |
  High because the condition is recurring (three cycles), the materiality is above the firm's
  published market-risk reporting threshold ($100M notional), the affected pack is consumed by
  the Board Risk Committee, and there is no compensating control that would have surfaced the
  truncation before pack distribution. Not critical because the under-statement is identified
  and quantifiable, the source data was correct (only the feed was truncated), and remediation
  is straightforward (re-align the feed cutoff with the source-system close).
compensating_controls: []

# mra_mria_classification omitted; source is internal-audit, not examiner-letter

population_size: 3
sample_size: 3
exceptions_observed: 3
sampling_methodology: population-based

linked_obligation_ids: [OBL-BCBS239-P04, OBL-BCBS239-P07]
linked_control_ids: [C-CRR-001]
linked_evidence_ids: [EV-2026-IA-MR-014-A, EV-2026-IA-MR-014-B, EV-2026-IA-MR-014-C]

recommendation: |
  The Head of Credit Risk Reporting must (1) re-align the upstream feed cutoff with the
  source-system close-of-day position and document the re-aligned cadence, (2) redesign the
  reconciliation control C-CRR-001 to compare against the source-system close rather than
  against the post-cutoff feed file, and (3) re-issue the three affected monthly packs to the
  Board Risk Committee with a corrected counterparty view and a written explanation of the
  truncation and remediation.

remediation: |
  Three-part remediation: feed-cutoff re-alignment, control redesign, and pack re-issuance.
  The control redesign is the structural fix; the re-alignment is the immediate operational
  fix; the re-issuance is the audit-trail closure.

owner: "Head of Credit Risk Reporting"
target_date: 2026-07-15
remediation_milestones:
  - {date: 2026-05-15, milestone: "Feed cutoff re-aligned and one-cycle reconciliation evidenced", owner: "Head of Credit Risk Reporting"}
  - {date: 2026-06-15, milestone: "Reconciliation control C-CRR-001 redesign signed off by Head of Market Risk Reporting", owner: "Head of Credit Risk Reporting"}
  - {date: 2026-07-15, milestone: "Three affected packs re-issued to Board Risk Committee", owner: "Head of Credit Risk Reporting"}

closure_evidence:
  - "Feed-orchestration runbook with revised cutoff schedule and documented coordination with reconciliation control owner"
  - "Two consecutive months of reconciled feed output against source-system close, with sign-off log retained in GRC platform"
  - "Re-issued monthly market-risk packs (2026-01, 2026-02, 2026-03) with corrected counterparty view and committee acknowledgement"
  - "Updated control documentation for C-CRR-001 reflecting redesigned reconciliation boundary"

interim_mitigation: |
  Manual completeness check by Credit Risk Reporting analyst against source-system close-of-day
  counterparty position before each pack distribution, until the structural fix is signed off.
  Evidenced by analyst sign-off log retained in the GRC platform. The interim check is not the
  remediation; it keeps risk down while the redesign lands.

evidence_gap: false

confidence_label: high

reviewer_questions:
  - "Should the reconciliation control redesign also cover the credit-risk pack and the liquidity-risk pack, or are those packs sourced via different feeds with different cutoff alignment? The audit work scoped the market-risk pack only."
  - "Does the firm's BCBS 239 self-assessment process surface this issue automatically into the next semi-annual self-assessment, or does the Head of Credit Risk Reporting need to file a separate input?"
  - "Is the 2026-07-15 target date acceptable to the Audit Committee given the three-cycle re-issuance scope, or should the re-issuance be accelerated?"

human_review_required: true

revisions:
  - {date: 2026-04-22, reason: initial write-up, delta: created from IA-WP-2026-MR-014, approved_by: "Internal Audit Senior Manager"}
```

## What the write-up surfaces

- The condition is dated, scoped, and quantified ("three monthly cycles", "$187M notional", "T+1 04:00 ET feed cutoff vs T+1 06:00 ET source-system close"). It reads as the observable state, not as a conclusion about the control.
- The criteria names BCBS 239 Principles 4 and 7 with section references and points back to `references/source-anchors.md` for the citation excerpt; the firm-policy criterion names the policy version and section and points to `references/firm-overlay.md`. The reviewer can read the criterion, not just take the author's word for it.
- The cause names the specific control attribute that failed (the reconciliation control's comparison boundary). It is not "feed timing issue" or "human error".
- The effect quantifies the under-statement, names the downstream pack, identifies the regulatory exposure (next OCC continuous-monitoring review), and explicitly notes no customer or reputational impact. The effect is not inflated past the evidence.
- Severity is paired with rationale referencing materiality (against the firm's $100M threshold), frequency (three cycles), audience (Board Risk Committee consumption), and the absence of compensating controls. The "not critical" reasoning is also given, which keeps the severity calibration defensible.
- Closure evidence is the artifact: the runbook, the reconciliation output, the re-issued packs, the updated control documentation. "Remediated" does not appear.
- Interim mitigation is named separately. The manual completeness check is the mitigation; it is not the remediation.
- Reviewer questions are tied to specific elements (scope of the redesign, BCBS 239 self-assessment seam, target-date defensibility), not generic prompts.
- The structured record consumes the upstream `obligation-mapping` IDs (OBL-BCBS239-P04, OBL-BCBS239-P07) and the `control-matrix` ID (C-CRR-001), so downstream skills (exception-analysis, risk-committee-pack, control-matrix) can pick the issue up by foreign key.

## Downstream uses

- The exception-analysis chain in `compliance-testing` consumes `severity`, `linked_control_ids`, and `closure_evidence` to ladder this exception into the testing program; control C-CRR-001 moves to the top of the next test cycle until the redesign is evidenced.
- `risk-committee-pack` reads `severity`, `mra_mria_classification`, `evidence_gap`, and `target_date` for the open-issues section of the next Board Risk Committee pack.
- `control-matrix` reads `linked_control_ids` to surface ISS-2026-IA-BCBS239-007 against the C-CRR-001 row in the credit-risk-reporting matrix; the open issue's severity downgrades the control's operating-effectiveness rating until closure.
- The Audit Committee response file references `issue_id`, `condition`, `criteria`, and `target_date` directly when responding to the audit committee's standing question on open material findings.
