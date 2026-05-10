---
name: obligation-mapping
description: |
  Converts any source document (rule text, supervisory guidance, exam manual, exam request list, supervisory letter, regulator speech, internal policy, third-party SLA, contract clause) into a structured obligation register: one row per obligation, traced to source by section, with applicability, control objective, evidence required, owner, status, and open questions. Foundational primitive: control-matrix anchors its rows on this output, policy-gap-review triangulates against it, evidence-binder pulls evidence asks from it, exam-brief reads it, and almost every downstream second-line skill reaches for an obligation register at some point.

  Best for:
  - Standing up or refreshing the obligation register for a process, product, function, or regulatory domain.
  - Converting an exam manual section or an examiner document-request list into an internal obligation set the firm can respond to row by row.
  - Translating a supervisory letter, regulator speech, or interagency statement into discrete obligations and open questions.
  - Mapping a third-party SLA, vendor contract, or sponsor-bank agreement to the obligations it imposes on each party.

  Not the right tool when:
  - Input is a discrete piece of net-new rule text being absorbed for change-management purposes (use `regulatory-change-management/skills/rule-to-obligation-extraction`; that skill is tuned for rule deltas, this one is tuned for any source).
  - The mapping is from obligation to control (use `control-matrix`; this skill ends at the obligation, that skill begins from it).
  - The work is a gap analysis between firm policy and obligations (use `policy-gap-review`).
  - The work is drafting a finding (use `issue-writeup`).
argument-hint: "[obligation source: rule text, exam request, policy, SLA, supervisory letter]"
---

# Obligation mapping

An obligation register is the row-anchored translation of a source document into the obligations that source imposes on the firm. One source document, many obligations; one row per obligation. The register is what every downstream second-line skill reads when it needs the answer to "what does the firm have to do here, and where does that obligation come from." Control-matrix anchors its rows on it. Policy-gap-review triangulates against it. Evidence-binder reads `evidence_required` to scope its asks. Exam-brief leans on it to answer "what obligation gives the rule the examiner is asking about." Issue-writeup cites it when it opens a finding.

The skill is source-agnostic by design. Rule text, supervisory guidance, exam manuals, exam request lists, supervisory letters, regulator speeches signaling enforcement priorities, interagency statements, internal policies, third-party SLAs, contract clauses, vendor questionnaires, industry technical standards. Each source carries obligations; the register makes them legible. The boundary with `regulatory-change-management/rule-to-obligation-extraction` is sharp: that skill is tuned for net-new rule deltas where the work is implementation pipeline; this skill is tuned for any source where the work is the register itself.

The output is a register in `templates/default-output.md` shape and a structured record per `schemas/obligation-register.schema.json`. It is a draft until a named reviewer (legal, compliance, or the function owner) attests.

## Ask first

Before drafting, settle a few things. The conversation usually surfaces them in the first exchange.

- What process, product, function, or domain is the register scoped to. "All BSA obligations" is too wide; "CDD obligations for the consumer-deposit account-opening process at the bank-sponsor side of a fintech partnership" is the kind of scope the register can be honest against.
- What sources are in scope, and at what edition. Rule text by CFR cite and effective date. Exam manual by edition year. Supervisory letter by SR or OCC bulletin number. Internal policy by version and approval date. SLA by execution date and amendment history. Mixed source posture is fine; the source list says what is in.
- Who reads the register, and what decision it supports. A 1.5-line BU controls tester reads it operationally. A 2-line head of compliance reads it for review-gate routing. An external auditor reads it as the universe to test against. A regulator reads it line by line.
- Whether the register is a fresh build, a refresh against an updated source, or a re-mapping after a process change. Fresh builds set every row's status at draft. Refreshes inherit prior status and surface deltas. Re-mappings re-test applicability.

When `scope` is supplied, the skill consumes it for institution, persona, source posture, sector overlay, and cross-cutting overlay. Otherwise it asks the four questions and defaults to public posture if the practitioner declines. The register notes scope was not formalised; it does not silently assume.

## How the register gets built

The register has the same spine across sources. A senior practitioner builds it in roughly the order below, but the conversation surfaces rows in whatever order the source reads.

The frame opens with scope and source posture: process or product, business unit, jurisdiction, period, source posture, and the source list itself (each source named with edition and date, plus URL). The source list is what the register is anchored on; if a source is not on the list, it is not a permitted citation in any row.

Rows are obligation-anchored. Each row carries the named columns:

- **Obligation ID.** Stable identifier scoped to the register. The control-matrix and policy-gap-review skills key off it.
- **Source citation.** Regulator or issuer, document, edition or date, section reference (CFR subsection, SR letter section, manual chapter, SLA clause, policy section), URL or document identifier. The section reference is mandatory; a bare URL is not a citation. Where the section is genuinely unknown, the row carries `[verify section]` rather than fabricated detail.
- **Requirement summary.** One sentence stating what specifically must be done and on whom. "Firm must do CDD" is not a requirement summary; "the bank must obtain and verify the identity of each beneficial owner of a legal-entity customer at account opening" is. Paraphrase preserves the operative verb and the operative object. If the source uses "shall," the summary uses must; if the source uses "should," the summary says should.
- **Applicability.** Institution type, product, activity, geography, threshold. The threshold matters: a 1071 obligation now triggers at 1,000 covered transactions per year under the May 1, 2026 final rule (effective June 30, 2026; first compliance date January 1, 2028); the obligation reads differently for a 600-transaction firm than for a 5,000-transaction firm. Where the source does not name a threshold, applicability says so. "All operations" is not applicability.
- **Effective date.** With phase-in stages where the source specifies them. Tier-by-tier compliance dates (1071, DORA implementation), deferred-effective-date provisions, sunset clauses, transition periods. Where the effective date is contingent (rule subject to litigation, guidance subject to revision, sunset awaiting reauthorisation), the row says so.
- **Impacted process or function.** Named: account opening, vendor onboarding, model deployment, transaction monitoring, marketing review, complaint handling, board reporting. The named process is what control-matrix will scope a row against.
- **Control objective.** One sentence on the condition that must be true for the obligation to be satisfied. "Beneficial owners of legal-entity customers are identified and verified at account opening, and the verification record is retained per the rule's retention period." Distinct from the requirement summary; the summary states what the rule says, the objective states what the firm has to make true.
- **Evidence required.** What proves operation. Named system-of-record outputs, records, sign-off logs, training rosters, model documentation, vendor file contents. A policy reference is a control statement, not evidence. The evidence-binder skill reads this column.
- **Owner.** A named role with accountability: BSA Officer, Head of Vendor Management, Chief Privacy Officer, Head of Model Risk, head of credit risk reporting, ECOA officer, fund CCO. "Compliance" is not an owner. "Operations" is not an owner. Where the firm's role taxonomy is firm-specific, it lands in `references/firm-overlay.md`.
- **Status.** One of `draft`, `in-review`, `approved`, `not-applicable`, `open-question`. New rows enter at `draft` or `open-question`. `approved` is reserved for rows the named reviewer has signed off on; the skill does not set that value itself. `not-applicable` carries a one-sentence rationale tied to the applicability column.
- **Open questions.** Items requiring legal or compliance review before status moves off `open-question`. Examples: whether a Reg E provisional-credit obligation extends to a particular product variant; whether a vendor's SOC 2 carve-out covers a specific control; whether a 1071 firewall design is sufficient when a single loan officer performs both intake and underwriting.
- **Linked controls.** Foreign keys into a control-matrix output. Optional at extraction time; populated when control-matrix runs against the register.

The tail of the register surfaces what the body cannot. The open-question summary lists every row carrying open questions, grouped by reviewer (legal, compliance, function head, sponsor) so the routing is one read away. Applicability scoping notes capture the rationale for `not-applicable` decisions and the threshold reasoning for tier-dependent obligations; this is where examiners and auditors pressure-test the register and where having written rationale beats having to reconstruct it. The source trace block records confidence by section: high where the source text is unambiguous, medium where interpretation is involved, low where the practitioner is reading between the lines or relying on a single secondary source. The sign-off block names the reviewer.

### Sector and cross-cutting overlays

The same row spine carries different source labels and different rigor expectations across sectors and across cross-cutting topics. Load only the overlays the scope flags. The overlays do not change the row structure; they change which sources the register is permitted to cite and which obligation patterns the practitioner expects to find.

- `references/sector-overlays/banking.md` carries insider-lending and affiliate-transactions rules, large-bank heightened standards, FRB SR letters as obligation sources, and the BSA/AML manual structure for banking processes.
- `references/sector-overlays/insurance.md` carries state-by-state insurance-code obligations (NAIC model laws as starting point), ORSA obligations, market-conduct exam manuals, and the federal-state interplay specific to insurance.
- `references/sector-overlays/capital-markets.md` carries SEC adviser and broker-dealer rules, the FINRA rule book, SEC EXAMS priorities as scoping input, and the registered-fund rule set for fund-side work.
- `references/sector-overlays/payments-fintech.md` carries Reg E / Reg Z / Reg DD obligations for consumer-payment products, OCC bank-fintech partnership expectations, CFPB open-banking obligations when applicable, and sponsor-bank allocation patterns.
- `references/cross-cutting/cyber.md` loads when source is cyber-anchored (state cyber rules, SEC cyber rules, FFIEC IT, GLBA Safeguards security-program obligations).
- `references/cross-cutting/privacy.md` loads when source is privacy-anchored (GLBA Privacy, state privacy laws, Reg P).
- `references/cross-cutting/conduct.md` loads when source is conduct-anchored (CFPB UDAAP, fair-lending rules, complaint-handling expectations).

Granular citations (CFR sections, SR letter numbers, NAIC model numbers) live in `references/source-anchors.md` and the overlay files. Firm policy or taxonomy lives in `references/firm-overlay.md` (consumed when present) and never in the register directly. The register carries the obligation source from the regulator and the firm's labelling from the overlay as distinct columns.

## Quality bar

The source citation carries both a URL and a section, paragraph, or chapter reference. A bare URL is not a citation. Where the section is genuinely unknown, the row carries `[verify section]` and the open-question summary picks it up; fabricating a section reference fails the bar.

The requirement summary preserves substance. Paraphrasing away the operative verb or the operative object loses the obligation. The summary is what the firm will be tested against; it has to read like the rule it came from.

Applicability names institution type, product, activity, geography, and threshold where the source defines them. Where the source does not, applicability says the source did not specify. "All operations" is not applicability and reads as an extraction defect.

Owner is a named role with accountability. Departments are not owners; "Compliance" is not an owner; "the team" is not an owner. Where the firm's taxonomy applies, it comes from `references/firm-overlay.md`.

Status starts at `draft` or `open-question`. The skill does not set rows to `approved`; only the named reviewer does, and that happens outside the skill.

The register is rule-anchored. Internal policy can be a source, but a row whose only source is the firm's own policy, with no external rule, supervisory guidance, or contractual anchor underneath, belongs in `policy-gap-review`'s output. The register is what the firm has to do; the policy library is what the firm says it does about it.

Material claims cite a source from the source list. `[evidence needed]` flags items needing follow-up and routes to the open-question summary. The register is a draft until a named reviewer attests; the skill stops at draft.

## Adaptation

Audience drives shape: a 1.5-line refresh reads operational, a 2-line register for committee challenge clusters open questions to the front, an audit support file pulls applicability rationale forward, an examiner-readiness pack sequences rows by source. Source posture drives what the row body can carry; public-only registers stop at obligation, control objective, and evidence type, while mixed and firm-policy-overlay let named owners and named systems land. Sector and cross-cutting overlays load from the scope. Confidence labels track by section, not as a single overall label, because most registers have high-confidence rows and low-confidence rows side by side.

## Output

The register in `templates/default-output.md` shape and the structured record per `schemas/obligation-register.schema.json`. Downstream consumers: `control-matrix` reads `obligations[*].obligation_id` to anchor its rows, `policy-gap-review` reads the register against the policy library to surface gaps, `evidence-binder` reads `obligations[*].evidence_required` to scope its evidence asks, `exam-brief` reads the register to answer "what obligation gives the rule the examiner is citing," `issue-writeup` cites obligations when opening findings, `regulatory-change-management/rule-to-obligation-extraction` consumes the schema for net-new rule deltas. The schema is the cross-skill contract; additive changes only, never silent renames. Breaking changes ship as a versioned migration with downstream skills told in advance.

## Pointers

- `references/source-anchors.md` — citations and excerpts for the named anchors.
- `references/sector-overlays/{banking,insurance,capital-markets,payments-fintech}.md` — sector overlays loaded from scope.
- `references/cross-cutting/{cyber,privacy,conduct}.md` — cross-cutting overlays loaded from scope.
- `references/firm-overlay.md` — firm-installed taxonomy, named role labels, system-of-record names, internal policy pointers, decision forums and sign-off conditions beyond the regulatory baseline; consumed when present.
- `templates/default-output.md` — register template.
- `schemas/obligation-register.schema.json` — structured-output contract.
- `examples/` — CFPB Section 1071 obligation register for a community bank; FFIEC BSA/AML CDD obligation register for a payments fintech bank-sponsor partnership.
- `TROUBLESHOOTING.md` — recurring defects in obligation registers.
