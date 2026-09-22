# Human review gate matrix

Matrix ID: <GM-YYYY-XXX-NN>
As of: <YYYY-MM-DD>
Author / persona: <role>
Status: <draft / under-review / committee-adopted>
Confidence: <high | medium | low | unknown>

## Workflow in scope

| Field | Value |
|---|---|
| Workflow / artifact lifecycle | <e.g., AI use-case lifecycle for tier-1 retail credit; critical-vendor onboarding lifecycle; issue lifecycle for second-line findings; SAR-filing decision> |
| Scope notes | <sub-processes excluded, jurisdictions covered, line-of-business carve-outs> |
| Source posture | <public-only | firm-policy-overlay | mixed> |
| Engagement scope | <ENG ID if formal scope; otherwise "ad-hoc, see assumptions"> |

## Decision authority

| Field | Value |
|---|---|
| Primary committee | <named body that pass/fails the gates> |
| Escalation committee | <where a no-pass routes> |
| Dissent path | <how an individual reviewer's challenge gets recorded and adjudicated> |
| Board oversight | <board body and reporting cadence, when in scope of Heightened Standards / Reg YY / NAIC ORSA> |

## Source list

| Source type | Label | Section reference | URL |
|---|---|---|---|
| <regulator / rule / interagency-guidance / supervisory-letter / examination-manual / internal-policy / industry-standard> | <e.g., SR 11-7> | <section ref or `[verify section]` in source-anchors> | |

## The gate matrix

One row per gate. Compress freely on rows that warrant it; do not delete required columns.

| Gate ID | Gate name | Stage | Trigger | Required reviewers (with independence) | Required inputs | Decision criteria | Stop conditions | Escalation path | Documentation requirement | Frequency | Source anchor |
|---|---|---|---|---|---|---|---|---|---|---|---|
| <GATE-XXX-NN> | <operational-language name> | <intake / tiering / pre-prod / go-live / ongoing-monitoring / retirement; planning / due-diligence / contract / ongoing-monitoring / termination; identification / severity-rating / remediation / closure> | <event-based trigger or periodic cadence> | <named roles, with primary / backup, with `independence_required` flagged where source guidance demands> | <artifact IDs that must be present> | <declarative criteria, each traceable to source> | <declarative, binary blockers> | <escalation committee, time-to-escalate, escalation owner> | <decision, rationale, attesters, date, system of record> | <event-based / daily / weekly / monthly / quarterly / annual / ad-hoc> | <named source for the gate's existence> |

> Independence is named per reviewer. A gate where the artifact's producer is also the gate's decider is not a gate; it is self-attestation. Where source guidance demands independence (SR 11-7 validation independence, interagency TPRM line-1 / line-2 separation, EU AI Act Article 14 competent oversight), the matrix carries the independence requirement and the source anchor that grounds it.
>
> Stop conditions are declarative and binary. "Should be reviewed", "consider whether", and "as appropriate" are not stop conditions; "no pass if any open critical issue" is.
>
> Each gate names required inputs by artifact ID. A gate that reviews "what is available" is unauditable.

## Gate gaps

Gates implied by source guidance but not present in the current workflow, or present but under-specified. A clean-looking matrix with no gaps usually means the gaps were buried.

| Implied gate | Gap description | Source anchor | Recommended action |
|---|---|---|---|
| <e.g., annual review gate for tier-1 AI use cases> | <gate not present / no independent reviewer / no stop conditions / no escalation path / no documentation requirement> | <path to source anchor> | <design gate, name reviewers, specify stop conditions, etc.> |

## Recommended owner actions

Specific actions for the named owners surfaced above. Not a generic "improve oversight" list.

- <Owner role> — <action> — <by when, if a milestone is in view>

## Reviewer questions

Specific to this matrix. Tied to specific gates, gaps, or independence concerns. Generic prompts add nothing.

- <question tied to a named gate, gap, independence requirement, or escalation pattern>

## One-page narrative for committee adoption

A short narrative summarising the gate flow for the committee that adopts the matrix. Decision authority, gate sequence, escalation, documentation. Reads as readable prose for a board or committee that does not read matrices line by line.

> [Narrative — three to four short paragraphs, written in committee-pack voice. Names the workflow, the primary committee, the gate sequence, the escalation pattern, the documentation discipline, and the source basis. Optional; populated when the engagement is standing up or refreshing committee adoption material.]

## Recommended charter language

Suggested wording the committee charter or policy section can adopt directly. Reads as charter prose, not as matrix commentary.

> [Charter prose — typically a three-paragraph block. Paragraph 1: committee purpose and decision authority. Paragraph 2: gate sequence and stop-condition discipline. Paragraph 3: escalation, dissent, documentation, and review cadence. Optional; populated when the scope flags charter-refresh as in scope.]

## Source trace

Material claims in this matrix are sourced. `[evidence needed]` flags items that need follow-up; route to the engagement issue log rather than leaving silent in the matrix body.

| Claim | Source | Evidence pointer | Confidence |
|---|---|---|---|

## Sign-off

| Role | Name on file | Date |
|---|---|---|
| Practitioner / matrix author | <role> | |
| Independent reviewer (independent of matrix author; named for the dissent-path discipline) | <role> | |
| Primary-committee chair (the committee adopting the matrix) | <role> | |
| Sponsor (if scope names one) | <role> | |

> The matrix is a draft until the named reviewer attests. Gate architecture is committee-adopted; the skill stops here.

## Revision log

Append-only.

| Date | Reason | Delta | Approved by |
|---|---|---|---|
| <YYYY-MM-DD> | initial matrix | created | <persona> |
