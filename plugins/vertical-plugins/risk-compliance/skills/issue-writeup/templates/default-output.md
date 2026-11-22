# Issue write-up

Issue ID: <ISS-YYYY-XXX-NN>
Title: <one-line title; reads as the issue, not the cause>
As of: <YYYY-MM-DD>
Author / persona: <role>
Status: <draft / under-review / open / in-remediation / closed-pending-validation / closed>
Confidence: <high | medium | low | unknown>

## Source

| Field | Value |
|---|---|
| Source type | <internal-audit / compliance-testing / vendor-monitoring / model-validation / examiner-letter / self-identified / whistleblower / other> |
| Source identifier | <audit engagement ID, exam letter ID, control-test workpaper ID, vendor monitoring record ID, validation report ID> |
| Regulator (if examiner-issued) | <FRB / OCC / FDIC / SEC / FINRA / CFPB / NYDFS / state DOI / NAIC / FinCEN / OFAC / other> |
| Date identified | <YYYY-MM-DD> |
| Period covered | <YYYY-MM-DD to YYYY-MM-DD> |
| Source posture | <public-only | firm-policy-overlay | mixed> |
| Engagement scope | <ENG ID if formal scope; otherwise "ad-hoc, see assumptions"> |
| MRA / MRIA classification | <MRA | MRIA | n/a (populated when source type is examiner-letter)> |

## Condition

<The dated, scoped, observable state. Specific. What was observed, when, in what population or process. Avoid conclusions ("the control failed"), avoid commentary ("oversight is weak"). Quantify where possible.>

## Criteria

<Named source with section. Regulatory: rule and section reference, citing `references/source-anchors.md` or a loaded overlay by path. Internal: policy name and version and section, citing `references/firm-overlay.md` by path. Multiple criteria are allowed and common; list each with its source.>

- <Criterion 1 — source label, section, path to source-anchors entry or overlay file>
- <Criterion 2 — ...>

## Cause

<Root cause, tied to a specific control design or operation weakness. Names the control attribute that failed. Avoid "human error", "training gap", "system limitation" as the cause field; those are surface labels and the cause is what is underneath them. If root cause analysis is genuinely pending, write "root cause analysis pending" and add an open action; do not invent a cause.>

## Effect

<Impact, quantified where possible. Financial (dollar amount, exposure, capital impact), customer (number affected, harm pattern, restitution scope), regulatory (exam consequence, supervisory letter exposure, filing implication), operational (process disruption, downstream pack impact), reputational (where genuinely public-facing). Carries the unit and the time window.>

## Severity

| Field | Value |
|---|---|
| Severity rating | <low | moderate | high | critical> |
| Severity rationale | <reference materiality, frequency, customer impact, regulatory exposure, compensating controls> |
| Compensating controls in place | <none | named compensating controls> |
| Materiality reference | <firm threshold, regulatory threshold, or "judgmental — no published threshold"> |

> Severity always carries human review. The skill does not assign severity unilaterally; the rating is proposed and the named reviewer attests.

## Population and sample (when sample-based)

| Field | Value |
|---|---|
| Population size | <integer> |
| Sample size | <integer> |
| Exceptions observed | <integer> |
| Projected exception rate | <percentage or "not projected"> |
| Sampling methodology | <random / risk-based / judgmental / population-based test> |

## Linked artifacts

- Linked obligation IDs: <OBL-* foreign keys into obligation-mapping output>
- Linked control IDs: <C-* foreign keys into control-matrix output>
- Linked evidence IDs: <EV-* foreign keys into evidence-binder output>

## Recommendation

<Declarative voice. What the owner must do. Specific enough that closure is testable.>

## Remediation

| Field | Value |
|---|---|
| Owner role | <named role with accountability — Head of Vendor Management, Head of Model Risk, BSA Officer, etc.> |
| Target date | <YYYY-MM-DD> |
| Closure evidence | <the artifact the firm will inspect to confirm closure: system, report ID, sign-off log, reconciliation evidence, etc.> |
| Interim mitigation | <manual workaround or compensating control in flight; or "none">|
| Remediation milestones | <interim milestones with dates if remediation runs longer than 90 days> |

## Evidence gap

| Field | Value |
|---|---|
| Evidence gap flag | <yes | no> |
| Note | <one-line description if yes; routes to engagement issue log> |

## Reviewer questions

Specific to this issue. Tie to elements of the CCCE. Generic prompts add nothing.

- <question tied to condition, criteria, cause, effect, severity, or remediation>

## Source trace

Material claims in this write-up are sourced. `[evidence needed]` flags items that need follow-up; route to the engagement issue log rather than leaving silent in the body.

| Claim | Source | Evidence pointer | Confidence |
|---|---|---|---|

## Sign-off

| Role | Name on file | Date |
|---|---|---|
| Practitioner / write-up author | <role> | |
| Severity reviewer (always required) | <role, independent of author for severity attestation> | |
| Owner concurrence (the named role accepting remediation accountability) | <role> | |
| Sponsor (if scope names one) | <role> | |

> The artifact is a draft until the named reviewer attests. The skill stops here. Severity assignment always carries human review; an unattested severity is not yet a severity.

## Revision log

Append-only.

| Date | Reason | Delta | Approved by |
|---|---|---|---|
| <YYYY-MM-DD> | initial write-up | created | <persona> |
