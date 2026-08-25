# Example: control-test evidence binder for an SR 11-7 model validation

Public-source-derived. No named institution. The shape mirrors a common pattern: an in-house model risk team assembles the evidence binder for the annual revalidation of an internal credit-decisioning model, working from SR 11-7, OCC Bulletin 2026-13, and the firm's MRM policy.

## Input

- **Binder purpose**: model-validation.
- **Scope**: revalidation of an internal credit-decisioning model used in second-look review of declined small-business-loan applications. Period covered: 2025-04-01 to 2026-03-31.
- **Reviewer**: head of model validation (2-line); the binder is being assembled by a 1.5-line model risk reporting analyst on the model owner's team.
- **Engagement scope supplied**: institution = state member bank; primary regulators = FRB, state DFI; persona = head of MRM; source posture = public-plus-firm-policy-plus-evidence; sector overlay = banking; cross-cutting overlays = none for this binder (cyber, privacy, conduct not in scope of the validation cycle).
- **Inputs already on file**: prior validation report (2025); ongoing-monitoring dashboard extracts; the firm's MRM retention schedule; the firm's model inventory record for the model.

## Output sketch

The skill produces an evidence binder. Headlines:

- **Scope and binder purpose** — model-validation, 12-month period, head-of-MRV reviewer; source posture allows direct extracts from the model risk system of record (MRMS) and the credit-decisioning platform.
- **Request list** — populated from the head-of-MRV's evidence ask for the revalidation cycle: model documentation set, development-data extract, validation re-runs, ongoing-monitoring outputs, outcomes analysis, benchmarking against an external dataset, exception register, change log. Each item carries a status (`met`, `partial`, `gap`, `not-applicable`, `deferred`).
- **Evidence index, grouped by SR 11-7 §V validation activity**:
  - *Conceptual soundness*: model documentation v3.2 (`policy-version`, system of record = MRMS); design memo v2.0 (`management-memo` paired with the design-decision sign-off log from MRMS).
  - *Process verification*: code repository snapshot (`system-extract`, system of record = internal Git enterprise); training script run log (`system-extract`).
  - *Outcomes analysis*: development-data extract (`system-extract`, system of record = data warehouse Snowflake); validation re-run output (`system-extract`); back-test comparison (`test-workpaper`).
  - *Ongoing monitoring*: monthly monitoring dashboard exports for the period (`system-extract`, system of record = MRMS monitoring module); breach alerts (`incident-record`); response actions (`sign-off-log`).
  - *Benchmarking*: external dataset benchmark for the most recent vintage — **gap**.
- **Provenance concerns** — one row flagged: the development-data extract for the 2024 vintage was manually copied from a deprecated reporting tool to a spreadsheet during a system migration; reproducibility is `false` and the row's `completeness_flag` is `partial`. Reviewer questions surface the issue.
- **Evidence gaps** — benchmarking against the external dataset is missing for the most recent vintage; prior-cycle monitoring records are present but the firm's MRM retention schedule calls for seven years and current evidence runs back five.
- **Evidence by control** — the firm's three model-risk controls (independent validation, ongoing monitoring, change management) each carry the supporting evidence rows and a sufficiency call. Independent validation is `complete`; ongoing monitoring is `partial` (benchmarking gap); change management is `complete`.
- **Reviewer questions** — does the spreadsheet-extract row meet MRM's reproducibility expectation, or should the row be reclassified as `management-assertion` until the data warehouse re-pull is run? Should the binder hold open until the external benchmarking gap closes, or proceed with the gap explicitly noted?
- **Confidence label**: `medium`. Posture is high but the benchmarking gap and the provenance issue on the 2024 vintage extract pull confidence down.
- **Sign-off**: blank. The binder is a draft until the head of MRV signs.

The binder is the evidence index, not the validation conclusion. The validation report consumes the binder; the validator decides.

## Why this scenario matters

- **Practitioner trick line**: "screenshot is not evidence; the system-of-record link is." The benchmarking row could have been a screenshot of an external-dataset query result; the binder requires a paired `system_of_record_link` (the dataset query plus the run log) before the row counts as `complete`. The binder downgrades a confident-looking screenshot to `partial` if the link is missing.
- **Boundary check on evidence-class**: the design memo is a `management-memo` (an assertion), not source evidence. Pairing it with the sign-off log from MRMS makes the design-decision auditable; without the pairing, the memo is one person's claim.
- **Boundary check on retention**: the firm's MRM retention schedule (seven years) is the binding internal expectation; the binder surfaces the two-year shortfall as a gap even though SR 11-7 itself does not specify a duration.
- **Boundary check on provenance**: the spreadsheet extract is a real-world failure mode. The binder does not silently treat it as evidence; it carries the provenance concern and lets the reviewer call it.
- **Boundary check on the request list**: every request-list item maps to evidence rows or appears in the gaps section. A request list with silent omissions is unauditable.

## Anchors

- SR 11-7 / OCC Bulletin 2011-12 (April 4, 2011), §V Model Documentation.
- OCC Bulletin 2026-13, Revised Interagency Guidance on Model Risk Management, model-documentation refresh [verify section].
- AICPA AU-C 500, audit evidence — sufficiency and appropriateness framing carried by internal audit functions [verify section].
- IIA International Standards 2310 (Identifying Information) and 2410 (Communicating Results) [verify section labels].

See `references/source-anchors.md` for full citations.
