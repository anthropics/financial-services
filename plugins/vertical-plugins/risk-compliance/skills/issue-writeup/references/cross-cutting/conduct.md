# Conduct cross-cutting overlay — issue-writeup

Loads when the scope `cross_cutting_overlay_set` includes `conduct`. The overlay shapes the criteria block, the severity calibration, and the closure-evidence framing for issues whose underlying condition involves customer-facing harm, sales-practice deficiencies, market-conduct exposure, or culture-and-conduct-risk patterns.

## Why the conduct overlay matters

Severity calibration shifts when customer harm is identifiable. A finding that the firm has a control gap in disclosure timeliness reads moderate at face value; the same finding with identifiable consumer harm (eroded customer benefit, restitution-eligible scope, repeated pattern) reads high or critical. The conduct overlay carries the discipline that makes that severity shift defensible: it names the harm, scopes the harm, identifies the population, and frames closure evidence around restitution and pattern remediation rather than around process fix alone.

## Source basis

- **CFPB UDAAP Examination Manual** — the unfair, deceptive, or abusive acts or practices framework. The manual's UDAAP module sets the criteria for unfairness (substantial injury not reasonably avoidable; not outweighed by benefits), deception (representation, omission, or practice that misleads a reasonable consumer; materiality), and abusive (interferes with a consumer's ability to understand or take action; takes unreasonable advantage).
- **CFPB Compliance Bulletins and Circulars** — published positions on UDAAP, fair lending, debt collection, mortgage servicing, deposit products, and other consumer-finance topics. CFPB Circulars are formal interpretive guidance that supervisors and enforcement teams apply.
- **FINRA Rule 2010** — standards of commercial honor and just and equitable principles of trade. The conduct framing for broker-dealer findings.
- **FINRA Rule 2111** — suitability rule (and Reg BI for accounts where Reg BI applies).
- **SEC EXAMS Risk Alerts on conduct** — published priorities on adviser fiduciary duty, suitability, churning, breach of fiduciary duty, fee transparency, and similar conduct-focused categories.
- **FCA Conduct Risk framework (UK reference)** — sometimes referenced in US firms with UK affiliates; the FCA's five conduct outcomes are a useful taxonomy but are not US-binding.
- **Reg E error-resolution and unauthorized-transfer rules** — consumer-conduct findings on electronic-fund-transfer disputes carry conduct-overlay severity.
- **State unfair-trade-practice statutes** — vary by state; multi-state replication of UDAAP findings frequently triggers state-level enforcement risk.
- **NAIC Market Regulation Handbook** — for insurers, the market-conduct-finding convention covers sales practices, claims handling, advertising, and producer oversight.

## What the overlay adds to the write-up

### Criteria block additions

When the underlying condition involves customer-facing harm, the criteria block layers a conduct criterion onto the substantive criterion. Examples:

- A disclosure-control finding takes the substantive criterion from Reg Z or Reg E and the conduct criterion from CFPB UDAAP (deception or unfairness).
- A sales-practice finding at a broker-dealer takes the substantive criterion from FINRA Rule 3110 (supervision) and the conduct criterion from FINRA Rule 2010 and Rule 2111.
- A claims-handling finding at an insurer takes the substantive criterion from the state insurance code's claims-handling-timeliness section and the conduct criterion from the NAIC Market Regulation Handbook's claims module.

### Harm-identification block

Conduct-tagged issues carry a distinct harm-identification block within the effect / impact section. The block names:
- **Population affected**: number of customers, customer segments, geographic distribution, time window.
- **Harm pattern**: financial (overcharge, missed credit, inappropriate fee), operational (denied service, delayed service, inappropriate adverse action), informational (disclosure deficiency, misleading communication), or relational (cancellation hurdle, dispute-resolution-friction).
- **Restitution scope**: dollars at stake, methodology for the calculation, third-party administrator (where applicable), and the consumer-notification path.
- **Pattern indicator**: whether the harm is one-off, intermittent, recurring, or systemic.

### Severity calibration

Conduct severity calibration leans on (1) consumer-harm scope, (2) population size, (3) pattern indicator, (4) reasonably-avoidable test, and (5) regulatory-priority alignment.

- **Identifiable systemic harm with restitution-eligible scope**: severity is critical or high.
- **Identifiable harm with limited population**: severity is high or moderate depending on the pattern indicator.
- **Disclosure or process deficiency without identified harm**: severity is moderate or low; the rationale notes that absence of identified harm does not foreclose harm and the firm's continuous-monitoring stance addresses the residual.
- **Cultural-pattern findings**: where multiple findings together suggest a culture-and-conduct-risk pattern (e.g., repeated UDAAP findings across product lines, repeated supervisory findings on sales-practice oversight), the issue write-up notes the pattern severity in the rationale even when the individual finding is moderate. The pattern dimension matters for fair-lending and CMS-program-effectiveness reviews.

### Closure-evidence framing

Conduct-tagged closure evidence emphasises restitution and pattern remediation, not just process fix. Examples:
- **Restitution-eligible findings**: closure evidence names the restitution program (consumer-notification process, dollar amount per consumer, third-party administrator engagement, completion attestation), the look-back scope (period covered, methodology), and the consumer-notification template approval.
- **Pattern findings**: closure evidence names the pattern-remediation actions across the product or function, not just the immediate finding's fix. Cultural-pattern remediation typically runs longer than process-fix remediation.
- **Disclosure findings**: closure evidence names the corrected disclosure, the consumer-impact assessment for affected past disclosures, and the disclosure-review-control redesign that prevents recurrence.

### Reasonably-avoidable test for unfairness

When the criteria block cites UDAAP unfairness, the reasonably-avoidable test is part of the analysis. The cause field on an unfairness finding ties to whether the consumer could have reasonably avoided the injury (typically not, when the firm controls the disclosure or process), whether the injury is outweighed by benefits to consumers or competition (typically the burden falls on the firm to evidence), and whether substantial injury is involved.

## Common patterns and pitfalls

- **Severity deflation when no harm yet identified**. A finding without identified harm is not the same as a finding with no harm; the overlay's discipline is to name the population, scope the look-back, and only conclude no-harm after the look-back is evidenced.
- **Treating UDAAP as a catchall**. UDAAP applies to specific circumstances; the criteria block must specify whether the finding is unfairness, deception, or abusive, with the test elements.
- **Conflating fair-lending with UDAAP**. Fair-lending findings (ECOA, Fair Housing Act, HMDA) have a distinct framework from UDAAP; they often co-occur. The criteria block separates them.
- **Pattern blindness**. A single moderate finding that is the third in a series of UDAAP findings carries different severity than a first-time finding. The severity rationale should reference the prior findings; the firm's GRC platform's issue-history field is the source.
- **Compensating-controls argument for harm**. A compensating control reduces the residual risk; it does not unwind identified harm. Restitution and consumer-notification stay in the closure evidence even when a compensating control is in place going forward.

## Joint-ownership patterns

Conduct-tagged issues often carry joint ownership between the substantive control owner and the consumer-compliance / fair-lending function (the CCO or Head of Compliance for UDAAP findings, the Fair Lending Officer for ECOA findings, the BSA Officer for AML / sanctions findings that carry consumer-impact). The owner field names the primary owner; the recommendation or remediation block names the joint owner.

## Anchors used by this overlay

- CFPB Examination Manual, UDAAP module. https://www.consumerfinance.gov/compliance/supervision-examinations/
- CFPB Compliance Bulletins and Circulars. https://www.consumerfinance.gov/compliance/circulars/
- FINRA Rule Book, Conduct Rules (Series 2000). https://www.finra.org/rules-guidance/rulebooks/finra-rules
  - Rule 2010 (Standards of Commercial Honor and Just and Equitable Principles of Trade)
  - Rule 2111 (Suitability)
  - Rule 2210 (Communications with the Public)
- 17 CFR §240.15l-1 (Regulation Best Interest) and 17 CFR §275.211 (Investment Adviser fiduciary-duty interpretation).
- 12 CFR Part 1005 (Reg E) error-resolution and unauthorized-transfer rules.
- 12 CFR Part 1026 (Reg Z) closed-end credit and credit-card rules.
- 12 CFR Part 1002 (Reg B / ECOA) for fair-lending findings that intersect with conduct.
- NAIC Market Regulation Handbook, claims-handling and sales-practice modules. https://content.naic.org/cmte_d_mar.htm [verify current edition section labels.]
- State unfair-trade-practice statutes — vary by state; firm-overlay names the state-specific anchors.
- FCA Conduct Risk framework (UK reference; not US-binding but useful taxonomy). https://www.fca.org.uk/firms/culture-and-governance
