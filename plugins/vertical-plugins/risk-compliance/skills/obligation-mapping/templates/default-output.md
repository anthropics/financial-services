# Obligation register

Register ID: <REG-YYYY-XXX-NN>
As of: <YYYY-MM-DD>
Author / persona: <role>
Status: <draft / in-review / attested>
Engagement scope reference: <ENG-YYYY-XXX-NN or "scope not formalised">

## 1. Scope

| Field | Value |
|---|---|
| Process / product / function | <named scope, tight enough to be honest against> |
| Business unit | <named, not "the business"> |
| Jurisdiction | <federal, state, country, multi> |
| Period | <start> to <end> |
| Register type | <fresh-build / refresh / re-mapping> |
| Source posture | <public-only / public-plus-firm-policy / public-plus-firm-policy-plus-evidence / connector-aware> |

## 2. Source list

Each source named with edition or date, plus URL. Sources not on this list are not permitted citations in any row.

| # | Source | Issuer | Edition / date | Type | URL |
|---|---|---|---|---|---|
| 1 | <document name> | <regulator / agency / counterparty> | <edition or date> | <rule-text / supervisory-guidance / exam-manual / supervisory-letter / SLA / internal-policy / other> | <URL or document ID> |

## 3. Obligation register

One row per obligation. Section reference is mandatory; a bare URL is not a citation.

| ID | Source citation (with section) | Requirement summary | Applicability | Effective date / phase-in | Impacted process | Control objective | Evidence required | Owner | Status | Confidence | Open questions | Linked controls |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OBL-001 | <issuer, doc, §section, URL> | <one sentence: what specifically must be done and on whom> | <institution type, product, activity, geography, threshold> | <date / phase-in stages> | <named process> | <one sentence: condition that must be true> | <named system-of-record output, records, sign-off logs> | <named role> | <draft / in-review / approved / not-applicable / open-question> | <high / medium / low> | <items requiring legal or compliance review> | <CTRL-IDs from control-matrix, when populated> |

> Status enters at `draft` or `open-question`. The skill does not set rows to `approved`; the named reviewer does, outside the skill.

## 4. Open-question summary

Grouped by reviewer so routing is one read away.

### Legal review
- <OBL-IDs>: <question, with the rule cite and the specific factual ambiguity>

### Compliance review
- <OBL-IDs>: <question>

### Function head review
- <OBL-IDs>: <question>

### Sponsor review
- <OBL-IDs>: <question>

## 5. Applicability scoping notes

Rationale for `not-applicable` decisions and threshold reasoning for tier-dependent obligations. This is where examiners and auditors pressure-test the register.

- <OBL-ID>: <one paragraph on why the obligation does or does not apply, citing the source's threshold language>

## 6. Source trace and confidence

Confidence is recorded by section, not as a single overall label.

| Section | Confidence | Rationale |
|---|---|---|
| <source name §section> | <high / medium / low> | <unambiguous source text / interpretation involved / reading between the lines> |

## 7. Sign-off

- Practitioner: <role>
- Named reviewer: <role>, <review status>, <date>
- Independent reviewer (advisory or internal QA): <role>, <date>

> The register is a draft until the named reviewer attests. Material claims cite a source from the source list. `[evidence needed]` flags items needing follow-up; they route to the open-question summary.

## 8. Revision log

Append-only.

| Date | Reason | Delta | Approved by |
|------|--------|-------|-------------|
| <YYYY-MM-DD> | initial register | created | <persona> |
