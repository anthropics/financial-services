---
name: policy-gap-review
description: |
  Reviews a firm policy or procedure (or a small set of related policy artefacts) against a named, dated benchmark of obligations or supervisory expectations and produces a gap matrix. One row per gap, with classification (missing / partial / weak / inconsistent / outdated), severity with rationale, declarative recommended edit, evidence needed beyond the text, and named owner. Foundational primitive: the gap matrix routes into `issue-writeup` for findings, into `obligation-mapping` when missing obligations surface, and into `control-matrix` when the operational dimension of the gap is a control rather than text. Audience is policy owners, compliance, and internal audit; the artifact is the gap list, not the policy redline.

  Best for:
  - Refreshing a policy ahead of a regulator exam, internal audit, post-enforcement uplift, or scheduled triennial review.
  - Comparing a legacy policy against a newly published rule or refreshed guidance (legacy SR 11-7-anchored MRM policy against the joint April 2026 model-risk guidance; pre-2023 vendor-management policy against the June 2023 interagency TPRM guidance; legacy AI policy against NIST AI RMF 1.0 plus AI 600-1).
  - Reviewing a draft policy before approval to surface gaps against the named benchmark before it goes to committee.
  - Converting an examiner-cited policy weakness into a structured gap inventory the firm can remediate row by row.

  Not the right tool when:
  - The work is extracting obligations from source. Use `obligation-mapping`; this skill consumes its output as the benchmark.
  - The work is mapping obligations to controls. Use `control-matrix`; this skill triangulates against it but does not build it.
  - The work is comparing two versions of the same policy. Use `regulatory-change-management/skills/policy-diff` (version-to-version), not this skill (policy-to-obligation).
  - The work is drafting a finding from a single policy gap that has already been confirmed. Use `issue-writeup`.
  - The work is the policy rewrite itself. The skill ends at the gap list and the recommended edit fragments; the redline lives elsewhere.
argument-hint: "[policy under review and benchmark source: policy doc plus rule, guidance, or obligation-register]"
---

# Policy gap review

A policy gap review is the row-anchored translation of "this policy says X, the benchmark says Y, and here is where they diverge" into something a policy owner, a compliance function, or internal audit can act on. The artifact is a gap matrix: one row per gap, with the policy text on one side, the benchmark requirement on the other, and the diagnosis in between. The output is a remediation list, not a marked-up policy. Whoever owns the rewrite reads the gap list and produces the redline; this skill stops at the gap list.

The skill is one of the foundational primitives in this plugin. It runs against an obligation set extracted by `obligation-mapping` (or against a policy plus a freshly issued rule, where the benchmark is the rule itself). Gaps that read as findings route into `issue-writeup`. Gaps that surface obligations the obligation register did not yet have route back into `obligation-mapping`. Gaps where the policy says the right thing but the operational evidence is thin route into `control-matrix` and `evidence-binder`. The policy text lives where the firm keeps it; this skill produces the gap inventory and the recommended-edit fragments that whoever rewrites the policy will work from.

The boundary with `regulatory-change-management/policy-diff` is sharp. That skill compares two versions of the same policy (v3.4 vs v4.0). This skill compares one policy to an external benchmark (the policy vs the rule, the guidance, or the obligation register). The two skills feed different downstream work; an agent should not invoke both for the same job.

The matrix is the deliverable; the format is whatever the engagement and audience need. A gap matrix is matrix-natural — the rows want a register layout — so most engagements render Excel for the matrix plus a Word narrative for the cover summary, recommended edits, and out-of-scope rationale. The skill drafts against `templates/default-output.md` and emits the structured record at `schemas/policy-gap-matrix.schema.json`. The artifact is a draft until a named reviewer signs off; severity assignment always carries independent attestation.

## Ask first

Before drafting, settle a few things. Most are on the table by the time someone reaches for a gap review.

- What policy is under review, and at what version. Policy name, version, effective date, and the named role that owns it. A gap review against an unsigned draft reads differently from one against a board-approved policy in production; the artifact carries the version so the reviewer knows which it is. Where the policy is a set rather than a single document (an MRM policy plus a model-validation standard plus an adverse-action notice standard), name each artefact with its version.
- What benchmark the policy is being reviewed against. A named, dated source with section references is mandatory. Pointer into an `obligation-mapping` register, or the rule and guidance directly named (with edition, date, and section refs from `references/source-anchors.md`). A review with no external benchmark is internal-consistency editing, not a gap review; the skill refuses to proceed without a benchmark.
- What sections of the policy are in scope of the review. Policies of any size accumulate sections that are not in scope of the current refresh (cross-referenced standards living elsewhere, sections governed by a separate review cycle, sections recently uplifted). Naming the in-scope section list keeps the matrix honest about what was actually reviewed.
- Who reads the matrix and what decision it supports. A 1.5-line policy-owner pre-read reads operational. A 2-line compliance-committee pre-read clusters severity and recommended edits to the front. Internal audit reads it as input to fieldwork scoping. A regulator-exam pre-read leans on coverage summary and out-of-scope rationale.
- What source posture the engagement runs at. Public-only sets the ceiling at obligation, control objective, and observable text comparison. Firm-policy-overlay or mixed lets named owners, named systems of record, and operational evidence references land in the body.

When `scope` is supplied, the skill consumes it for institution, persona, source posture, sector overlay, and cross-cutting overlay. Otherwise it asks the questions above and defaults to public posture if the practitioner declines. The matrix notes scope was not formalised; it does not silently assume.

## How the gap matrix gets built

The matrix has the same spine across reviews. A senior practitioner builds it in roughly the order below, but the conversation surfaces gaps in whatever order the reading produced them; the structured record sorts itself.

The header opens with policy under review (name, version, effective date, owner role, document identifier), benchmark sources (each named with edition, date, and section references), scope of review (which sections of the policy were actually read against the benchmark), and source posture. The benchmark-sources block is mandatory and the section-references list is mandatory inside it; a benchmark named without sections is the reviewer's problem to fix before the matrix can carry rows.

Rows are gap-anchored. Each row carries the named columns:

- **Gap ID.** Stable identifier scoped to the matrix. Downstream `issue-writeup` rows that paper a gap key off this ID; recommended edits fed back to the policy author key off it; the obligation register's `linked_gaps` array carries it when the gap is benchmark-traced.
- **Benchmark requirement.** One sentence stating what the benchmark requires. Paraphrase preserves the operative verb and operative object, mirroring the discipline the obligation register applies. The benchmark requirement is paired with `benchmark_source_anchor` (named source, section, date, URL) so the reviewer can read the requirement in context.
- **Policy text excerpt and policy location.** The policy's actual wording on the topic (verbatim where the wording itself is at issue, paraphrased where the issue is silence or scope) and a section or heading reference within the policy. Where the policy is silent on the benchmark requirement, the policy-text field reads "policy is silent" and the location field names the section the topic should sit under.
- **Gap classification.** One of `missing`, `partial`, `weak`, `inconsistent`, or `outdated`. The five values are not interchangeable; the matrix discipline is to pick the one that matches.
  - `missing` when the policy does not address the benchmark requirement at all.
  - `partial` when the policy addresses some of the requirement but stops short. Vendor policy mentions due diligence but not termination planning; AI policy mentions model inventory but not GenAI prompt governance.
  - `weak` when the policy addresses the requirement but at lower rigor than the benchmark expects. Policy says "monitor vendor performance" where the benchmark expects named KRIs and a documented cadence.
  - `inconsistent` when the policy contradicts the benchmark or contradicts another section of itself or another firm policy. MRM policy says all material models require independent validation; the AI governance standard exempts agentic AI from validation.
  - `outdated` when the policy reflects a prior edition of the benchmark that has since been refreshed. Policy cites SR 11-7 with no reference to OCC Bulletin 2026-13; vendor policy references the 2013 OCC bulletin without acknowledging the June 2023 interagency guidance.
- **Severity.** Low, moderate, high, or critical, paired with `severity_rationale`. Severity without rationale is opinion. Rationale references materiality (against the firm's published thresholds where they exist), supervisory exposure (active examination scope, MRA / MRIA-eligibility, recent enforcement against similar weaknesses), customer impact (where the policy gap affects customer-facing decisions), operational risk (where the gap exposes the firm to incident or loss), and any compensating control or operational practice that reduces the practical exposure pending the policy fix.
- **Recommended edit.** Declarative voice. What the policy should say. Not "add language on AI systems" but "add §X.4: Models classified as AI systems under the firm's tiering taxonomy are within the inventory, are tiered by use-case impact rather than statistical complexity, and require validation evidence proportionate to use-case impact." A recommended edit that just restates the gap is not yet a recommended edit; the skill drafts at summary level so the policy author has a starting point.
- **Evidence needed.** What would close the gap operationally beyond the text edit. The text fix alone is rarely sufficient; the firm also has to update standards, run training, change a workflow, refresh an attestation. Evidence-needed names the operational artefacts the firm would inspect to confirm closure, picking up downstream into `evidence-binder`. For gaps classified `partial`, `weak`, or worse, evidence-needed is mandatory.
- **Linked obligation IDs.** Foreign keys into `obligation-mapping`'s output for the obligation the benchmark requirement carries. Where the obligation register did not yet carry the obligation, the gap row generates an open question routed back to obligation-mapping rather than fabricating an obligation ID.
- **Linked control IDs.** Foreign keys into `control-matrix`'s output for controls the policy section governs. Empty when the gap is purely textual; populated when the gap has a control dimension.
- **Owner.** A named role with accountability for the policy section. Where the role taxonomy is firm-specific, it lives in `references/firm-overlay.md`. "Compliance" is not an owner; "the policy team" is not an owner; "Head of Vendor Management" or "Chief Privacy Officer" or "Head of Model Risk" is.

The tail of the matrix earns its keep by what it surfaces:

- **Coverage summary.** Integer counts: total benchmark requirements in scope, covered items, partial items, missing items. A coverage summary like "we cover most of the rule" is unverifiable; the field requires counts. Percentages are derived, not asserted.
- **Out-of-scope items.** Benchmark items the firm deliberately does not cover, with rationale. The threshold-based exception (a 1071 obligation that does not bind firms below 100 originations); the institution-type exemption (a Heightened-Standards expectation that does not apply to a community bank); the deferred-effective-date item (a rule whose effective date sits beyond the next review cycle). Out-of-scope is an audit-defence artefact; reconstructed rationale is harder than written rationale.
- **Cross-policy interactions.** Most material gaps interact with at least one other firm policy. Vendor policy and information-security policy on subcontractor due-diligence depth. MRM policy and AI governance committee charter. BSA/AML policy and consumer-compliance policy on customer-onboarding flows. The interaction is named (`dependency`, `conflict`, `overlap`) and described, so the reader can route the cross-policy fix to the right co-owner.
- **Recommended next steps.** Operational, not commentary. Draft revisions ready for legal review. Route to compliance committee for tabling on a date. Schedule policy-owner working session with named other-policy owners. Schedule training refresh on changed sections.
- **Source trace and confidence.** Material claims cite `references/source-anchors.md` or a loaded overlay by path. `[evidence needed]` flags route to the engagement issue log rather than living silent in the matrix. Confidence is assigned at the matrix level, with per-row confidence available where the practitioner is reading between the lines.
- **Sign-off.** Named practitioner, severity reviewer (independent of author for severity attestation), policy-owner concurrence, sponsor where scope names one.

### Sector and cross-cutting overlays

The same row spine carries different benchmark sources and different severity calibrations across sectors and across cross-cutting topics. Load only the overlays the scope flags. The overlays do not change the row structure; they change which sources the matrix benchmarks against and which gap patterns the practitioner expects to find.

- `references/sector-overlays/banking.md` carries large-bank heightened-standards policy expectations, FRB SR letters and FDIC FILs as policy guidance, and the BSA/AML manual policy-pillar expectations.
- `references/sector-overlays/insurance.md` carries NAIC Model Audit Rule, ORSA, and state DOI conduct-of-business policy expectations.
- `references/sector-overlays/capital-markets.md` carries the SEC advisers and fund compliance-program rules and FINRA supervisory-procedures expectations.
- `references/sector-overlays/payments-fintech.md` carries OCC bank-fintech partnership and CFPB consumer-compliance policy expectations for sponsor-bank arrangements.
- `references/cross-cutting/cyber.md` is the most-loaded overlay. State cyber policy content elements, FFIEC IT information-security framing, and the SEC public-company governance-disclosure expectations land here. The overlay fires whenever the policy in scope is a cybersecurity policy or includes a cybersecurity section.
- `references/cross-cutting/privacy.md` loads for privacy or data-handling policies. GLBA Safeguards, state privacy laws, Reg P, and the post-2024 Reg S-P customer-information safeguards land here.
- `references/cross-cutting/conduct.md` loads for customer-facing policies (product approval, marketing, complaints, fair lending). CFPB UDAAP benchmarks land here.

For GenAI, agentic AI, or other AI-system policy scope, the matrix benchmarks against NIST AI RMF 1.0, NIST AI 600-1, ISO/IEC 42001, the EU AI Act, and the firm's AI governance framework — those are out of scope of the joint April 2026 model-risk guidance and route to a separate workstream. Climate overlay follows the same pattern; this skill ships cyber, privacy, and conduct. Granular citations (CFR sections, rule paragraphs) live in `references/source-anchors.md` and the overlay files. Firm-specific severity ladders, named committees, and firm-specific role titles live in `references/firm-overlay.md`.

## Quality bar

The matrix has at least one named, dated benchmark source with section references. Reviewing a policy against itself or against generic guidance fragments without anchored sources is internal-consistency editing, not a gap review. The skill refuses to proceed without `benchmark_sources` populated.

Severity is paired with rationale referencing materiality, supervisory exposure, customer impact, operational risk, and compensating practice. Severity without rationale is opinion; severity assignment always carries independent attestation.

Gap classification picks one of the five values and the row carries the value that fits. Conflating `missing` with `partial` is a common defect; the skill prompts when a row's policy-text field reads "silent" but the classification is `partial` rather than `missing`.

Recommended edit is declarative and at least summary-drafted. "Add language on AI systems" is not a recommended edit; "add §X.4 stating that AI systems are within the model inventory, tiered by use-case impact, and require validation evidence proportionate to use-case impact" is.

Evidence needed is mandatory on rows classified `partial`, `weak`, `inconsistent`, or `outdated`. The text fix alone rarely closes an operational gap; the matrix surfaces the operational dimension explicitly.

Coverage summary fields are integer counts. A summary like "most of the rule is covered" without counts fails the matrix's audit-defensibility test.

Owners are named roles with accountability. Where the role taxonomy is firm-specific, it comes from `references/firm-overlay.md`. Departments and collective nouns are not owners.

Cross-policy interactions are surfaced when the gap interacts with another firm policy. Burying the interaction in commentary or assuming the other-policy owner will figure it out is how policy refreshes break the firm's overall governance architecture.

Material claims cite a source. `[evidence needed]` flags route to the engagement issue log; the seams between source evidence, management assertion, public-source obligation, and inference stay visible. RFP narrative is not evidence. `[verify section]` markers belong in source-anchors verification, not the matrix body. No named institutions in narrative unless they are public defendants in a finalised enforcement action with a published consent order. The matrix stops at recommendation; it is a draft until the named reviewer signs off.

## Adaptation

Audience drives compression: a policy-owner pre-read reads operational; a compliance-committee read pulls severity and recommended edits to the front; an internal-audit read leans on coverage summary and out-of-scope rationale. Source posture drives what the body can carry. Sector and cross-cutting overlays load from the scope. The order of gap rows in the surface artifact can sequence by severity, by policy section, or by benchmark source depending on audience; the structured record preserves the columns distinctly.

## Output

Default to drafting against `templates/default-output.md`. The artifact is gap-matrix-natural — render Excel for the matrix itself via the `xlsx` skill in the `document-skills` plugin, with Word for the narrative cover summary, recommended-edit fragments, and out-of-scope rationale via the `docx` skill. PowerPoint for a compliance-committee tabling, markdown for a developer-touched artifact. Render to whatever the engagement and audience ask for. Produce the structured record at `schemas/policy-gap-matrix.schema.json` when downstream automation or a registered consumer needs it.

Downstream consumers: `issue-writeup` consumes `gaps[]` rows whose severity warrants tracking as findings, lifting `gap_id`, `benchmark_requirement`, `severity`, and `recommended_edit` into the CCCE structure; `obligation-mapping` consumes gap rows whose `linked_obligation_ids` is empty (the gap implies an obligation the register did not yet carry) and reopens the register for that section; `control-matrix` consumes gap rows whose `linked_control_ids` is populated and re-tests the operational-effectiveness rating in light of the policy fix; `evidence-binder` reads `evidence_needed` to scope its evidence asks for the operational dimension. The schema is the cross-skill contract; additive changes only, never silent renames. Breaking changes ship as a versioned migration with downstream skills told in advance.

## Pointers

- `references/source-anchors.md` — citations and excerpts for the named anchors.
- `references/sector-overlays/{banking,insurance,capital-markets,payments-fintech}.md` — sector overlays loaded from scope.
- `references/cross-cutting/{cyber,privacy,conduct}.md` — cross-cutting overlays loaded from scope.
- `references/firm-overlay.md` — firm-installed taxonomy, named role labels, severity-rating ladder, named committee sign-offs, firm-specific section labels; consumed when present.
- `templates/default-output.md` — gap-matrix template.
- `schemas/policy-gap-matrix.schema.json` — structured-output contract.
- `examples/` — legacy SR 11-7-aligned MRM policy benchmarked against OCC Bulletin 2026-13; pre-2023 vendor-management policy benchmarked against the June 2023 interagency TPRM guidance.
- `TROUBLESHOOTING.md` — recurring defects in policy gap reviews.
