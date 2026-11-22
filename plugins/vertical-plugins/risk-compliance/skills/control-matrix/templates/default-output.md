# Control matrix

Matrix ID: <CM-YYYY-XXX-NN>
As of: <YYYY-MM-DD>
Author / persona: <role>
Status: <draft / under-review / signed-off>
Confidence: <high | medium | low | unknown>

## Scope and source posture

| Field | Value |
|---|---|
| Process or product | <e.g., commercial real estate underwriting; vendor lifecycle for fraud-screening service; monthly board credit-risk pack> |
| Business unit | <named unit, not "the business"> |
| Jurisdiction | <US / US state-by-state / EU / UK / multi> |
| Lines of defense served | <1L / 1.5L / 2L / 3L> |
| Source posture | <public-only | firm-policy-overlay | mixed> |
| Engagement scope | <ENG ID if formal scope; otherwise "ad-hoc, see assumptions"> |

### Source list

| Source type | Label | Section reference | URL |
|---|---|---|---|
| <regulator / rule / interagency-guidance / supervisory-letter / examination-manual / internal-policy / industry-standard> | <e.g., OCC Bulletin 2026-13> | <section ref or `[verify section]` in source-anchors> | |

## The matrix

One row per control. Compress freely on rows that warrant compression; do not delete required columns.

| Obligation source | Control objective | Control activity | Control type | Control owner (role) | Frequency | Evidence pointer | Test method | Last test date | Last test result | Design effectiveness | Operating effectiveness | Open issues | Human review required |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| <obligation_id and source label> | <condition that must be true> | <who does what, how often, using what system> | <preventive / detective / response / compensating> | <named role, not a person> | <event-based / daily / monthly / quarterly / annual / ad-hoc> | <system of record output, report ID, file location, sign-off log> | <inquiry / inspection / observation / reperformance / data-analysis / walkthrough / hybrid> | <YYYY-MM-DD or "not yet tested"> | <pass / fail / partial / not tested> | <effective / partially-effective / ineffective / not-tested> | <effective / partially-effective / ineffective / not-tested> | <issue_id list> | yes / no |

> The objective is the condition that must be true. The activity is who does what, how often, using what system. Both fields are required; rows with only one are not yet a control.
>
> The owner is a named role with accountability (e.g., Head of Model Risk, Chief Privacy Officer, Head of Vendor Management). "Risk team" is not an owner.
>
> Evidence is a pointer to a system-of-record output, a sample report, or a sign-off log. The policy document is a control statement, not evidence of operation.

## Coverage gaps

Obligations in scope with no mapped control, or partial mappings. Empty section means gaps were not surfaced; gaps are normal and expected.

| Obligation ID | Source | Gap description | Recommended action |
|---|---|---|---|
| <obligation_id> | <source label and section> | <no control designed / no owner / no evidence pathway / never tested> | <design control, name owner, build evidence pathway, schedule test> |

## Redundancies

Controls mapped to no obligation (hygiene controls or evidence the obligation set is incomplete), or duplicate coverage of the same obligation without a designed-for defense-in-depth purpose.

| Control IDs | Redundancy description | Recommended action |
|---|---|---|

## Recommended owner actions

Specific actions for the named owners surfaced above. Not a generic "improve the control environment" list.

- <Owner role> — <action> — <by when, if a milestone is in view>

## Reviewer questions

Specific to this matrix. Generic prompts ("is this fit for purpose") add nothing.

- <question tied to a named obligation, control, or coverage gap>

## Source trace

Material claims in this matrix are sourced. `[evidence needed]` flags items that need follow-up; route to the engagement issue log rather than leaving silent in the matrix body.

| Claim | Source | Evidence pointer | Confidence |
|---|---|---|---|

## Sign-off

| Role | Name on file | Date |
|---|---|---|
| Practitioner / matrix author | <role> | |
| Control owners (one per material control where the sign-off forum requires) | <roles> | |
| Reviewer (independent of matrix author) | <role> | |
| Sponsor (if scope names one) | <role> | |

> The matrix is a draft until the named reviewer attests. The skill stops here.

## Revision log

Append-only.

| Date | Reason | Delta | Approved by |
|---|---|---|---|
| <YYYY-MM-DD> | initial matrix | created | <persona> |
