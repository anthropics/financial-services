# Policy gap review

Review ID: <PGR-YYYY-XXX-NN>
As of: <YYYY-MM-DD>
Author / persona: <role>
Status: <draft / under-review / signed-off>
Confidence: <high | medium | low | unknown>

## Policy under review

| Field | Value |
|---|---|
| Policy name | <e.g., Model Risk Management Policy> |
| Policy version | <e.g., v6.1> |
| Effective date | <YYYY-MM-DD> |
| Owner role | <named role; e.g., Head of Model Risk> |
| Document identifier | <internal doc ID, GRC platform record, intranet URL> |

> Where the policy under review is a set rather than a single document (a policy plus supporting standards), name each artefact with its version in this block.

## Benchmark sources

Each benchmark named with edition, date, and section references. A benchmark named without sections is the reviewer's problem to fix before the matrix carries rows.

| # | Benchmark source | Edition / date | Section references | URL |
|---|---|---|---|---|
| 1 | <e.g., OCC Bulletin 2026-13 — Revised Interagency Model Risk Management Guidance> | <publication date> | <e.g., §III.A control environment, §III.B third-party model controls> | |
| 2 | <obligation-register pointer, when applicable> | <register version> | <obligation IDs covered> | |

## Scope of review

The sections of the policy actually read against the benchmark.

| In-scope policy section | Benchmark sources used |
|---|---|
| <e.g., §3 Model lifecycle> | <e.g., OCC Bulletin 2026-13 §III> |
| <e.g., §6 Third-party models> | <e.g., interagency TPRM guidance §III.B> |

> Sections of the policy outside this list were not part of this review. They are not silently assumed compliant.

## Source posture

| Field | Value |
|---|---|
| Source posture | <public-only | firm-policy-overlay | mixed> |
| Engagement scope | <ENG ID if formal scope; otherwise "ad-hoc, see assumptions"> |
| Sector overlay set | <banking / insurance / capital-markets / payments-fintech> |
| Cross-cutting overlay set | <cyber / privacy / conduct / climate> |

## The gap matrix

One row per gap. Compress freely on rows that warrant compression; do not delete required columns.

| Gap ID | Benchmark requirement | Benchmark source (with section) | Policy text excerpt | Policy location | Gap classification | Severity | Severity rationale | Recommended edit | Evidence needed | Linked obligation IDs | Linked control IDs | Owner role |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GAP-001 | <one sentence: what the benchmark requires> | <named source §section> | <verbatim where wording is at issue; "policy is silent" where the issue is silence> | <policy section or heading> | <missing / partial / weak / inconsistent / outdated> | <low / moderate / high / critical> | <materiality, supervisory exposure, customer impact, operational risk, compensating practice> | <declarative: what the policy should say> | <operational artefacts, training, workflow updates, attestations> | <OBL-IDs from obligation-mapping; empty routes back to obligation-mapping> | <CTRL-IDs from control-matrix; empty when gap is purely textual> | <named role; firm-overlay if firm-specific> |

> Recommended edit is declarative and at least summary-drafted. "Add language on AI systems" is not a recommended edit.
>
> Evidence-needed is mandatory on rows classified `partial`, `weak`, `inconsistent`, or `outdated`. The text fix alone rarely closes an operational gap.

## Coverage summary

Integer counts. Percentages are derived, not asserted.

| Field | Value |
|---|---|
| Total benchmark requirements in scope | <integer> |
| Covered items | <integer> |
| Partial items | <integer> |
| Missing items | <integer> |
| Inconsistent items | <integer> |
| Outdated items | <integer> |

## Out-of-scope items

Benchmark items the firm deliberately does not cover, with rationale. This is an audit-defence artefact; reconstructed rationale is harder than written rationale.

| Item | Rationale |
|---|---|
| <e.g., 1071 obligation triggering at 100 originations> | <e.g., firm has 32 covered originations annually; threshold not met> |

## Cross-policy interactions

Most material gaps interact with at least one other firm policy. Name the interaction so the reader can route the cross-policy fix to the right co-owner.

| Other policy | Interaction type | Description |
|---|---|---|
| <e.g., Information Security Policy> | <dependency / conflict / overlap> | <one or two sentences on how this gap interacts with that policy> |

## Recommended next steps

Operational, not commentary.

- <e.g., Draft revisions on §3.4 ready for legal review by <YYYY-MM-DD>>
- <e.g., Route to Compliance Committee for tabling on <YYYY-MM-DD>>
- <e.g., Schedule policy-owner working session with Head of Vendor Management and CISO function>
- <e.g., Schedule training refresh on changed sections within 60 days of approval>

## Reviewer questions

Specific to this review. Generic prompts ("is this fit for purpose") add nothing.

- <question tied to a named gap, classification, severity rating, or cross-policy interaction>

## Source trace

Material claims in this review are sourced. `[evidence needed]` flags items that need follow-up; route to the engagement issue log rather than leaving silent in the matrix body.

| Claim | Source | Evidence pointer | Confidence |
|---|---|---|---|

## Sign-off

| Role | Name on file | Date |
|---|---|---|
| Practitioner / review author | <role> | |
| Severity reviewer (always required) | <role, independent of author for severity attestation> | |
| Policy owner concurrence | <role accepting recommended-edit accountability> | |
| Sponsor (if scope names one) | <role> | |

> The matrix is a draft until the named reviewer attests. Severity assignment always carries human review; an unattested severity is not yet a severity. The skill stops here.

## Revision log

Append-only.

| Date | Reason | Delta | Approved by |
|---|---|---|---|
| <YYYY-MM-DD> | initial review | created | <persona> |
