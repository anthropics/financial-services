---
name: scoping
description: |
  Produces a scoping charter and a structured scope record that downstream second-line skills consume. The charter sets institution, engagement, persona, source posture, risk lens, and overlay context so other skills do not reinvent these facts each time they are called.

  Best for:
  - An advisory engagement starting up and the lead needs a written scope before review work begins.
  - An internal review being charted (annual model risk review, periodic third-party risk review, audit support, exam-readiness sprint, regulatory-change implementation, board-pack cycle).
  - A practitioner joining an engagement mid-flight and needing the context in one place.
  - A downstream skill called with contested or unclear scope.

  Not the right tool when:
  - A current scope is already on file and the downstream skill is scope-aware (pass the existing record).
  - The work is a one-off question rather than a scoped review.
  - The institution and persona are already encoded in a `references/firm-overlay.md` the firm has installed.
argument-hint: "[institution and engagement type, or pointer to existing scope]"
---

# Scoping

The first thing a senior reviewer does on any non-trivial second-line engagement is set the scope. Who is the institution. What is the engagement. Who is the persona running it. What evidence is actually available. Which risks are in scope. Which sector and cross-cutting overlays apply. What is excluded. What is being assumed. What is left to clarify.

This skill produces that scope as a written charter for the engagement to carry, and as a structured record that downstream skills consume. Both 1.5-line embedded teams and 2-line independent reviewers benefit; advisory engagements run the charter formally, internal teams run it lighter.

Scoping runs in two situations. At kickoff, the engagement lead calls it to set the charter before any review work begins. Mid-flight, another skill calls it because that skill has hit contested or unclear scope (the source posture is too low for the evidence ask, the persona review gates are unnamed, the sector overlay is ambiguous). Both entries produce the same artifact; the mid-flight version focuses the revision on the contested section and hands back to the calling skill.

## Ask first

Before drafting, get plain answers to a few things. Most engagements answer them in the first conversation; if not, default and flag the default in the charter.

- Who reads the deliverable. The audience drives tone, depth, and which review gates matter.
- What this engagement is not covering. Naming exclusions up front prevents drift.
- What evidence the engagement actually has access to today, not aspirationally. Source posture is what you can deliver against, not what you wish you had.
- What decision the engagement supports and who owns the sign-off. The persona and review machinery flow from this.
- What the time horizon is. An exam-readiness sprint and an open-ended program review need different pacing.

## How the charter gets built

The charter has the same spine across engagement types. Walk it in the order the conversation surfaces; the structured record sorts itself. Cite a source for every material claim, and where a claim has no source attached, mark it `[evidence needed]` rather than letting it pass.

The institution profile names the type, asset size band, charter, registrations, geographic footprint, and the regulators this engagement is actually addressing. Asset size matters because the supervisory expectations binding on a regional bank differ from those on a GSIB or a mid-size insurer. Recent supervisory posture (open MRAs, MRIAs, consent orders, examination outcomes) goes here when it is known and the source posture allows; private items stay out of any artifact that will read at a lower posture than the engagement. Do not name institutions in examples or narrative unless they are public defendants in a finalized enforcement action with a published consent order.

The engagement profile names the type, sponsor (a role, not a person), audience, timeframe with milestones, and the deliverable shape. Type drives which downstream skills the engagement will use; deliverable shape drives how the artifacts roll up. The audience shapes everything that follows: a partner-facing brief is not a board minute is not an examiner-response file.

The persona profile names the role running the engagement day-to-day and, where it differs, the accountable executive who owns sign-off. 1.5-line is the embedded business risk officer, the regional risk lead, the BU controls tester (accountable to the business, but with a risk mandate). 2-line is the independent function: CRO, head of model risk, head of TPRM, head of operational resilience, CCO, BSA officer, AI governance lead, head of regulatory affairs. On most CCO/CRO-sponsored engagements the running-lead is not the executive; it is a Compliance Risk Lead, a senior model-risk officer, an AI-governance lead reporting to the CRO, or similar. Capture the running-lead in `persona.role` and the executive in `persona.accountable_executive_role` when they differ; collapsing them forces a CCO-vs-1.5L choice that misreads the day-to-day pattern. Audit support and advisory engagements layer their own review machinery on top, including partner approval, independent QA, internal audit sign-off. CRO-led engagements run on ERM machinery, CCO-led on compliance committee, AI-governance-led on AI risk committee. Capture which line and which review gates; downstream skills key off both.

Source posture is one of public-only, public-plus-firm-policy, public-plus-firm-policy-plus-evidence, or connector-aware. Set it at what the engagement has today, not at what it would prefer. The same engagement may run at public-only for an early scoping conversation and shift up once firm access lands; that shift goes in the revision log.

Risk lens is the list of risk types in scope, drawn from the firm's taxonomy when the firm has one or from the named risks the engagement targets when it does not. Match the lens to the engagement; an exam-readiness sprint covering credit and BSA does not need the full enterprise taxonomy. Firm-specific taxonomy, owners, and system-of-record paths do not get encoded directly in the charter. Those live in `references/firm-overlay.md` when the firm has installed one; the charter consumes them.

Sector overlay set is which of {banking, insurance, capital-markets, payments-fintech} apply. Usually one. Multi-entity engagements may need two; flag the choice. Cross-cutting overlay set is which of {cyber, privacy, climate, conduct} apply, driven mostly by the risk lens. Both sets are directives to downstream skills, telling them which `references/sector-overlays/<sector>.md` and `references/cross-cutting/<topic>.md` to load. Loading only what the engagement names keeps context clean for the regulators actually in play.

Primary regulators is who this engagement is actually addressing, not every regulator that touches the institution. Conceivable-but-secondary regulators go in `assumptions_and_dependencies`. Where a regulator's section reference is not known, leave it for verification rather than fabricate; the named regulatory anchors and their citations live in `references/source-anchors.md`.

Out of scope, assumptions, and open questions close the spine. Out of scope is what the engagement explicitly will not cover and is the firewall against drift. Assumptions are facts being treated as fixed. Open questions are items flagged for sponsor or counsel. Separate evidence from inference throughout: source-cited facts, management assertions, public-source obligations, generated inferences, and open legal or compliance questions each carry their own line so the artifact shows the seams.

The skill does not block on missing input. If the practitioner has only partial context (institution type, perhaps engagement type, no persona yet), draft against what is given, default the rest using the institution profile and engagement type, and flag the defaults. The first charter is a working draft; revisions are normal. The skill stops at draft. The sponsor signs the charter; downstream skills consume the record.

The revision log is append-only. The first row is the initial scope, every material change adds a row, and the log is the audit trail when scope is later contested in steering, in court, or with a regulator. The structured record is the cross-skill contract; additive changes only. Add fields, do not rename or repurpose them. A breaking change is a versioned migration with the downstream skills told in advance.

## Pointers

- `references/source-anchors.md` — citations and excerpts for the named anchors.
- `references/firm-overlay.md` — firm-installed taxonomy, machinery, and policy pointers; consumed when present.
- `templates/default-output.md` — content spec for the charter (named sections, fields).
- `schemas/scope.schema.json` — structured-output contract consumed by every downstream second-line skill.
- `examples/` — advisory exam-readiness sprint at a regional bank; internal AI use-case intake review at a registered investment adviser.
- `TROUBLESHOOTING.md` — recurring defects in scope records.

## Output

Two artifacts. The charter is the human-readable memo against the named sections in `templates/default-output.md`; render it Word-natural for advisory engagements that want a signed deliverable, markdown for internal use, or whatever the sponsor expects. The `docx` skill in the `document-skills` plugin handles Word rendering when called for. The structured scope record conforms to `schemas/scope.schema.json`; this is the cross-skill contract every other skill in the second-line repo consumes, and it is the canonical case where a schema genuinely helps downstream automation. Both emit together; the sponsor signs the charter and the structured record flows to whichever skill the engagement calls next.
