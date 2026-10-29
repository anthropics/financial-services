# Evidence binder

**Binder ID**: [stable identifier; reused by downstream workpapers, audit support packs, response files]
**Engagement ID**: [pointer to scope record, or "none — scope not formalised"]
**Binder purpose**: [regulator-exam | internal-audit | model-validation | vendor-review | committee-pack | issue-remediation | other]
**As of**: [date]
**Source posture**: [public-only | public-plus-firm-policy | public-plus-firm-policy-plus-evidence | connector-aware]
**Confidence label**: [high | medium | low | unknown]

## Scope

| Field | Value |
|---|---|
| Entity | |
| Process / control area / model / vendor / obligation | |
| Period start | |
| Period end | |
| Reviewer (role) | [examiner, auditor, validator, committee] |

## Request list

The examiner request list, audit fieldwork ask, or validator evidence list this binder reconciles against. Cite the request verbatim; do not paraphrase. Status reflects reconciliation against the evidence index below; an unmet request is a gap, not a silence.

| Request ID | Request text | Status | Linked evidence IDs | Owner (role) | Due |
|---|---|---|---|---|---|
| | | met / partial / gap / not-applicable / deferred | | | |

## Evidence index

The binder. One row per artifact. Cite system of record by name (not "internal database"). Mark `evidence_class` to distinguish source evidence from management assertion, public-source obligation, and generated inference; the binder shows the seams.

| Evidence ID | Type | Description | System of record | Date generated | Period covered | Linked obligations | Linked controls | Linked issues | Linked requests | Custodian (role) | Sensitivity | Provenance | Completeness | Reviewer sign-off |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-001 | [system-extract / system-screenshot / signed-attestation / external-confirmation / system-of-record-link / policy-version / contract / test-workpaper / sample-workpaper / training-record / meeting-minutes / sign-off-log / incident-record / regulatory-correspondence / third-party-report / management-memo / other] | | | | start - end | | | | | | public / internal / confidential / restricted | extract method, extracted by, extracted at, link back to source of record, reproducible? | complete / partial / gap | reviewer role, signed at |

A screenshot row carries a paired system-of-record link in the provenance column. Without it, the row is a screenshot of something that may or may not still match the underlying record; the binder cannot vouch for it.

A `management-memo` row is an assertion, not evidence; pair with a source-of-record item or surface the assertion as a reviewer question.

## Evidence by control

Group the index by control where the binder supports a control test or audit fieldwork program. Each control entry lists the evidence rows that support it and the residual sufficiency call.

| Control ID | Control description | Supporting evidence IDs | Sufficiency | Notes |
|---|---|---|---|---|

## Evidence by finding

Group the index by issue or finding where the binder supports remediation evidence. Each issue entry lists the evidence rows that support open or closed remediation status.

| Issue ID | Finding | Supporting evidence IDs | Remediation status | Notes |
|---|---|---|---|---|

## Evidence sufficiency log

Sufficiency calls in plain language: what was inspected, what stayed at assertion, what is partial, what is missing. The log is the audit trail when a sufficiency call is later challenged.

| Date | Reviewer (role) | Item | Call | Reasoning |
|---|---|---|---|---|

## Evidence gaps

Request items or expected evidence with no artifact, or with insufficient artifact. Cross-link to the issue log if a gap is itself a finding.

| Gap | Linked request | Linked obligation / control | Owner (role) | Target close |
|---|---|---|---|---|

## Provenance concerns

Items where the system of record is unclear, the extract method is non-reproducible, or the chain of custody is broken. A provenance concern is not the same as a gap; a gap is "evidence missing", a provenance concern is "evidence here, source unclear or non-reproducible".

| Evidence ID | Concern |
|---|---|

## Custodian and chain of custody

The roles accountable for evidence integrity in this binder. Custodian is a named role, not a team. The chain runs preparer → reviewer → filer; record handoffs in the row-level reviewer sign-off field.

| Custodian (role) | Domain |
|---|---|

## Reviewer questions

Questions surfaced for the sponsor or reviewer. Each ties to a specific gap, provenance concern, or sufficiency call. Generic challenge questions add noise; specific questions get answered.

- [Question, with the gap or row it ties to]

## Sign-off

| Field | Value |
|---|---|
| Reviewer (role) | |
| Signed at | |
| Comments | |

The binder is a draft until the named reviewer signs off. The skill stops at the draft.

## Source trace

| Claim | Source | Section | Date | URL or file ref |
|---|---|---|---|---|

Cite `references/source-anchors.md` for canonical citations. Use `[verify section]` if the section reference is unknown; do not invent.

---

*Binder depth scales to purpose.* A vendor-review binder for a non-critical SaaS may run to ten rows and fit on a page; a regulator-exam binder reconciled against a 60-item RFI runs long with sufficiency log and gap section in full. A committee-pack binder leads with the headline sufficiency and pushes the row-level detail into an appendix; an audit fieldwork binder leads with row-level detail because the auditor will read every row.
