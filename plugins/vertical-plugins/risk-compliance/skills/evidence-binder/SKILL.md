---
name: evidence-binder
description: |
  Assembles the evidence binder index for a regulatory exam, internal audit fieldwork pack, model-validation evidence pack, vendor-review pack, committee evidence pack, or issue-remediation file. One row per artifact, with system-of-record provenance, control and obligation linkage, sufficiency call, and reviewer sign-off. Reconciles a request list against the evidence on hand and surfaces the gaps before the reviewer does.

  Best for:
  - A compliance team building the response binder for a regulator exam against the examiner's request list (RFI).
  - An internal-audit lead assembling the fieldwork evidence pack for a control-test program.
  - A model-risk validator pulling the evidence pack for a model revalidation cycle under the firm's MRM frame (cadence per the firm's own policy, not assumed annual).
  - A TPRM team assembling the diligence evidence file for a critical or important vendor review.
  - A committee secretary compiling the evidence file behind a risk-committee or AI-risk-committee paper, where the committee will be asked "what supports this".
  - A second-line owner closing an issue and indexing the remediation evidence the issue-writeup will cite.

  Not the right tool when:
  - The work is producing the underlying evidence: running the source-system report, executing the control test, drafting the management memo. This skill indexes evidence; it does not generate it.
  - The work is drafting a finding from missing evidence (use `issue-writeup`).
  - The work is the committee narrative itself (use `risk-reporting/skills/risk-committee-pack`); this skill produces the evidence index the narrative cites.
  - The work is reviewing a vendor's published evidence pack against a deployment context (use `ai-governance-model-risk/skills/llm-vendor-evidence-review`).
argument-hint: "[binder purpose: exam, audit, validation, vendor, committee, issue. Plus the request list or evidence inventory if you have it.]"
---

# Evidence binder

The binder is what a senior reviewer reaches for when they want to know whether the work is supported. Compliance assembling for an examiner. Internal audit closing fieldwork. Model risk validating a model. TPRM signing off a critical vendor. A committee secretary preparing for the meeting where the question "what supports this" gets asked. The binder is the index they read; it is not the SharePoint folder of screenshots.

The discipline is sufficiency, not form. A screenshot is not evidence; the system-of-record link is. A management memo is an assertion, not testimony. A folder of artifacts without a request-list reconciliation is unauditable. The binder shows the seams between source evidence, management assertion, public-source obligation, and inference, because the reviewer's job is to credit each class differently.

The binder is the deliverable; the format is whatever the engagement and audience need. A model-validation pack is binder-natural and lands as Word with attachments or as a shared-drive folder structure with a Word index. An audit fieldwork binder runs Excel-natural for the row-by-row index plus Word for the cover narrative. The skill drafts against `templates/default-output.md` and emits the structured record at `schemas/evidence-binder.schema.json` for downstream consumers. The skill stops at the draft; the named reviewer signs.

## Ask first

Most binders answer these in the first conversation. If not, draft against what you have and flag the rest in the binder's reviewer questions.

- What is the binder for. Regulator exam, internal-audit fieldwork, model-validation pack, vendor diligence, committee evidence file, issue-remediation file. Purpose drives the request-list shape, the depth of provenance the reviewer expects, and the retention floor the rows must respect.
- Who reads it. An examiner-in-charge reads against a published handbook and the RFI they issued. An internal-audit lead reads against their fieldwork program. A validator reads against SR 11-7 §V activities. A committee reads against the meeting paper. The audience drives what the binder leads with.
- What is the period under review. Stale evidence is the most common rejection. Set `period_start` and `period_end` against the engagement window, not the date the artifact was first produced. Where a recordkeeping floor (BSA five years, broker-dealer books and records under 17a-4) extends past the engagement window, respect the floor at the row level.
- Is there a request list. An examiner RFI, an audit fieldwork ask, a validator evidence list, a committee paper agenda. If yes, the binder is built outward from the request list. If no (a remediation file, a self-initiated review), the binder is built from the obligation-control-evidence map the engagement maintains, and the reconciliation surface is implicit rather than explicit.

When the scope record from `risk-compliance-core/skills/scoping` is supplied, the skill consumes it for institution, persona, source posture, sector overlay, and cross-cutting overlay. Otherwise it asks the practitioner the few facts it needs and defaults to public posture if pressed.

## How the binder gets built

The binder has the same spine across purposes. The order below is roughly how a senior practitioner walks it; the structured object sorts itself regardless of conversation order.

The frame opens with binder purpose, scope (entity, process, period, reviewer role), and source posture. Source posture is what the engagement actually has access to today, not aspirationally. A binder assembled at public-only posture cannot index firm-system extracts; the gap section names what is unavailable rather than the body inventing it.

Where a request list exists, capture it next. Each request item carries a stable ID (the requester's, e.g., RFI-12, AUDIT-FW-04), the verbatim request text (do not paraphrase the requester), and a reconciliation status (`met`, `partial`, `gap`, `not-applicable`, `deferred`). Every request item resolves to evidence rows or to a gap row. Items in limbo are the failure mode; they are the hidden gaps reviewers find on inspection.

The evidence index is the body of the artifact. One row per artifact. The columns the binder reconciles against are `evidence_type`, `description`, `system_of_record`, `date_generated`, `period_start` and `period_end`, the linked obligation / control / issue / request IDs, `custodian_role`, `sensitivity`, the `provenance` block, and the `completeness_flag`. A row also carries an `evidence_class` (source evidence, management assertion, public-source obligation, generated inference) so the seams are visible. Reviewer sign-off at the row is for binders where the reviewer signs row by row (model validation, audit fieldwork); the binder-level sign-off is for the rest.

System of record is named, not "internal database". Workiva, Archer, ServiceNow GRC, Fiserv DNA, Guidewire ClaimCenter, Okta, Splunk, Jira. Generic labels do not survive challenge. Where the system has been pseudonymised in the artifact for sharing, the firm-overlay carries the mapping; the binder names the system, not "System A".

Provenance is the chain-of-custody record. `extract_method` describes how the artifact was produced (the SQL query, the report ID, the dashboard ID, the manual export path, the signed PDF emailed by the vendor). `extracted_by_role` is the role of the puller, not the named individual. `extracted_at` is an ISO datetime. `system_of_record_link` is the pointer back to the underlying record and is required for screenshot rows; without it, the screenshot is a screen state, not evidence. `reproducible` is the test the replay discipline cares about: another reviewer, six months later, with the binder in hand, should be able to re-pull the row.

Custodian is the named role accountable for the artifact's integrity, not a team. "Compliance" is not a custodian; "BSA Officer", "Head of Model Risk Reporting", "Director of Vendor Management", "Lead Underwriting Auditor" are. The custodian is who the reviewer goes back to with questions.

Sensitivity is set honestly at the row level. NPI, PHI, PCI, customer prompts, claim narratives, materiality memos, regulator correspondence, and similar content carry `confidential` or `restricted`, not the `internal` default. The sensitivity column drives downstream handling (redaction, segregation, distribution-list control); a binder that defaults every row to `internal` cannot support any of that.

Completeness flag is the row-level sufficiency call. `complete` means the artifact fully supports the request or control it is paired with. `partial` means it covers some but not all. `gap` means the row was placed but the artifact does not support what it was placed for; gap rows accumulate signal that the binder leans on weak evidence and the binder summary should reflect the cumulative weakness.

Sufficiency log entries are the audit trail when a sufficiency call is later challenged in fieldwork review or examiner debrief. Each entry names the date, the reviewer's role, the item, the call, and the reasoning. The log is the discipline; binders that skip it lose the trail and cannot defend the call later.

Gaps and provenance concerns close the body. Gaps are evidence missing or insufficient: a request item with no row, a control with no supporting artifact, an obligation with no evidence trail. Provenance concerns are evidence present but the source is unclear, the extract is non-reproducible, or the chain of custody is broken. The two are different and the binder records them in separate sections; collapsing them hides which is which.

Reviewer questions cluster the items the sponsor or reviewer needs to resolve, each tied to a specific gap, provenance concern, or sufficiency call. Generic questions add noise. "How is the firm reconciling the BCBS 239 lineage report against the stress-test data extract for the period" is specific; "Are the controls operating effectively" is filler.

The binder ends at the sign-off block. Reviewer is a named role: Chief Compliance Officer, Head of Internal Audit, Head of Model Risk, Head of TPRM, Audit Director. Multiple roles may sign for different sections; a model-validation binder routinely has the head of model risk signing the §V validation evidence and the model owner signing the development-data extracts. The binder is a draft until the named reviewer attests.

## Working with what you have

The skill does not block on missing input. If the engagement has a request list but no provenance discipline yet, draft the binder against the list and flag every row missing provenance in the provenance-concerns section; the binder reads honestly. If the engagement has evidence but no request list, build the index and note that the reconciliation surface is implicit. If the engagement is at public-only posture, the binder will lean on public obligations and management assertions and the confidence label drops to medium or low; the binder reads accurately.

A binder with named gaps and a remediation plan is stronger than a binder with hidden gaps. Reviewers credit honesty about gaps and discount binders that claim completeness and do not survive scrutiny.

## Quality bar

Every material claim cites a source from `references/source-anchors.md` (or a loaded overlay) by path. Unsupported claims are marked `[evidence needed]` and route to the engagement issue log. The seams between source evidence, management assertion, public-source obligation, and inference stay visible in the `evidence_class` column; RFP narrative is not evidence and management memos are assertions, not testimony.

No fabricated regulatory facts. No named institutions in narrative unless they are public defendants in a finalised enforcement action with a published consent order.

`[verify section]` markers belong in source-anchors verification, not the binder body. The binder stops at recommendation; the artifact is a draft until the named reviewer signs.

## Adaptation

Depth and length scale to purpose and audience. A vendor-review binder for a non-critical SaaS may run to ten rows and fit on a page; a regulator-exam binder reconciled against a 60-item RFI runs long, with the sufficiency log and gap section in full. A committee binder leads with headline sufficiency and pushes row-level detail into an appendix; an audit fieldwork binder leads with row-level detail because the auditor will read every row. A model-validation binder groups rows by validation activity (conceptual soundness, ongoing monitoring, outcomes analysis, benchmarking, independent challenge); a vendor-review binder groups rows by the interagency TPRM lifecycle phases. The sector overlay set drives which `references/sector-overlays/<sector>.md` is loaded. The cross-cutting overlay set follows the scope, with the rule that `references/cross-cutting/privacy.md` loads whenever the binder may carry NPI, PHI, PCI, or other regulated personal data, regardless of how the scope reads.

## Pointers

- `references/source-anchors.md` — citations and excerpts for the named anchors (BCBS 239, AU-C 500, AU-C 230, IIA Standards, FFIEC IT Audit booklet, SR 11-7, OCC 2026-13, the 2023 interagency third-party guidance, recordkeeping floors).
- `references/sector-overlays/banking.md`, `insurance.md`, `capital-markets.md`, `payments-fintech.md` — sector-specific supervisory frame loaded per scope.
- `references/cross-cutting/privacy.md` — loaded whenever the binder may carry regulated personal data; default-on for any binder touching NPI, PHI, PCI, or important-business-service controls.
- `references/cross-cutting/cyber.md` — loaded when the scope flags cyber or whenever the binder carries cyber-program evidence (NYDFS Part 500 attestations, IR workpapers, vulnerability-scan extracts, SOC 2 evidence, vendor cyber assessments, §500.17 / 36-hour banking notice / 8-K Item 1.05 filings).
- `references/firm-overlay.md` — firm-installed policy, taxonomy, named owners, system-of-record naming map (consumed when present).
- `templates/default-output.md` — binder template.
- `schemas/evidence-binder.schema.json` — structured-output contract.
- `examples/exam-response-binder.md`, `control-test-binder.md` — public-source-derived worked examples.
- `TROUBLESHOOTING.md` — recurring defects (screenshot-as-evidence, request-list-not-reconciled, custodian-set-to-team, stale period coverage, assertion-mixed-with-evidence, non-reproducible provenance, default-sensitivity, hidden gaps, function-level sign-off, skill-invoked-when-work-is-upstream).

## Output

Default to drafting against `templates/default-output.md`. The binder is binder-natural in practice; render the deliverable as Word with linked attachments via the `docx` skill in the `document-skills` plugin, or as a shared-drive folder structure with a Word index, or as Excel for the row-by-row index plus Word for the cover narrative when the auditor or examiner expects a workpaper-style index. PowerPoint for a committee distillation, markdown for a developer-touched artifact. Render to whatever the engagement and audience ask for. Produce the structured record at `schemas/evidence-binder.schema.json` when downstream automation or a registered consumer needs it.

Downstream consumers: `issue-writeup` reads `evidence_gaps` and `provenance_concerns` for findings rooted in evidence weakness; `risk-reporting/skills/risk-committee-pack` reads the binder summary and confidence label; `regulatory-reporting/skills/exam-response-pack` reads the request-list reconciliation and the linked-evidence trail; the firm's audit and exam workpaper systems read the structured record for the workpaper of record. The schema is the cross-skill contract; additive changes only. Add fields, do not rename or repurpose them. A breaking change is a versioned migration with the consumers told in advance.
