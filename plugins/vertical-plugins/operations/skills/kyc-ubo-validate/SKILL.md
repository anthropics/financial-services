---
name: kyc-ubo-validate
description: Validate the beneficial ownership chain from kyc-doc-parse against the BODS (Beneficial Ownership Data Standard) conceptual model — detect circular ownership, missing intermediaries, control mismatches, incomplete UBO declarations, shell risk, and PEP intersections. Use after kyc-doc-parse and before kyc-rules.
---

# Validate the UBO chain

Input: the structured record from `kyc-doc-parse`, specifically `beneficial_owners`, `controllers`, `applicant_type`, and `nationality_or_jurisdiction`.

> This skill only validates structure and internal consistency of the declared ownership chain — it does not verify against an external register. For register-based verification, pair with a BODS data connector.

## What this skill checks

| Check | Red flag if… |
|---|---|
| **Total ownership** | Sum of declared `ownership_pct` < statutory threshold (entity: 25%, trust: 10%) and applicant is not publicly listed |
| **Circular ownership** | Chain contains a cycle (A → B → A, or A → B → C → A) |
| **Missing intermediaries** | Ownership chain jumps from top-level UBO directly to applicant with intermediate entities named but not documented |
| **Control mismatch** | `control_basis` is "ownership" but `ownership_pct` disagrees with stated voting/board control, or vice versa |
| **Shell risk** | Entity UBO has no registered address, uses a registered-agent address, or jurisdiction appears on high-risk list with no physical presence evidence |
| **PEP intersection** | Any `beneficial_owners[].name` or `controllers[].name` matches or resembles a `pep_declared: true` flag without individual disclosure |
| **Bearer share / nominee risk** | Ownership is declared via bearer shares, trust with no settlor/beneficiary names, or nominee directors with no principal disclosed |

## Step 1: Normalise the ownership chain

From the `beneficial_owners` array, build an ordered chain from the applicant upward:

```
Applicant ← Immediate parent ← Intermediate holding company ← Ultimate beneficial owner(s)
```

For each link, record:
- Entity name and jurisdiction
- Ownership percentage claimed
- Control basis (`ownership | voting | board_control | other`)
- Document evidence reference (from `documents_received`)

If the chain has more than 3 layers, flag it for opacity (each extra layer increases the opacity score by 1).

## Step 2: Run the checks

For each check in the table above, determine **pass / flag / insufficient data**.

Use BODS v0.4 conceptual rules:
- A **Person** is the ultimate beneficial owner — if a UBO is an entity, flag it and request its UBOs
- A **Relationship** must have both `subject` (who owns) and `interestedParty` (what is owned) — missing either is a gap
- Joint ownership (two persons each at 15%) still meets the 25% threshold if they act in concert — flag for clarification

## Step 3: Score and report

Produce a JSON report:

```json
{
  "ubo_count": 2,
  "chain_depth": 2,
  "checks": [
    {"check": "total_ownership", "result": "pass", "detail": "Sum = 100%", "evidence": "UBO declaration lines 3-4"},
    {"check": "circular_ownership", "result": "pass", "detail": "No cycle detected"},
    {"check": "missing_intermediaries", "result": "flag", "detail": "Golden Faith Ltd mentioned as parent but not documented in packet", "evidence": "UBO chart, page 2"},
    {"check": "control_mismatch", "result": "pass"},
    {"check": "shell_risk", "result": "insufficient_data", "detail": "BVI entity — no address proof in packet"},
    {"check": "pep_intersection", "result": "pass", "detail": "No UBO names match PEP declaration"},
    {"check": "bearer_nominee_risk", "result": "pass", "detail": "No bearer shares or nominee directors found"}
  ],
  "flags": 1,
  "opacity_score": 1,
  "recommended_action": "Request Golden Faith Ltd formation documents. If not provided within review window, escalate to senior analyst.",
  "bods_conformance": "partial",
  "bods_gaps": ["Missing intermediate entity record for Golden Faith Ltd"]
}
```

### Output fields

| Field | Meaning |
|---|---|
| `flags` | Count of checks that returned `flag` |
| `opacity_score` | `chain_depth` — 1, plus 1 per flag, plus 1 for `insufficient_data`. 0-2 = low, 3-4 = medium, 5+ = high |
| `recommended_action` | Concrete next step for the compliance analyst |
| `bods_conformance` | `full` (all checks pass with evidence), `partial` (some gaps), `non_conformant` (fatal structural issues) |
| `bods_gaps` | Specific BODS elements missing from the declaration |

## Step 4: Hand off to kyc-rules

Pass the `opacity_score` and `flags` count to `kyc-rules` as additional risk factors. The rules engine should:

- Add 1 to the risk score for each flag
- Escalate to `high` immediately if `bods_conformance` is `non_conformant`
- Treat `insufficient_data` on `shell_risk` + `high_risk_jurisdiction` as automatic escalation

## Guardrails

- **This skill validates structure, not truth.** It catches inconsistencies in what the applicant declared — it does not confirm identities against civil registers.
- **Never guess document contents.** If a UBO chart mentions an entity but no formation doc is in the packet, flag it as missing — do not assume it exists.
- **Thresholds are configurable.** The 25% entity / 10% trust defaults follow FATF guidance; firms may set stricter thresholds. Note the statutory basis in the output.
