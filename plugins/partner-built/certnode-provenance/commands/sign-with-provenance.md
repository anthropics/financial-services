---
name: sign-with-provenance
description: Sign any AI-generated output with CertNode cryptographic provenance. Returns a public verify URL anyone can use to confirm the content existed in this exact form at the signing time. Designed for FRE 902(13)/(14) admissibility + EU AI Act Article 50 disclosure. Use after producing a deliverable that will reach a client, LP, regulator, or official record.
---

# /sign-with-provenance

Sign the current document, conversation transcript, or any AI-generated content with CertNode three-layer cryptographic provenance.

## Usage

```
/sign-with-provenance
```

Run after producing content you want to verifiably preserve. The command will:

1. Call the `sign-output` skill with the current context
2. Display the receipt id + public verify URL
3. Suggest where to embed the verify URL (deck footer, email signature, report appendix, CRM record)

## Prerequisites

- `CERTNODE_API_KEY` set in environment (get one at <https://certnode.io/dashboard/provenance>)
- Free tier: 100 signings/month, no card

## Example output

```
✓ Signed
  Receipt ID:    7e3a9b2f-4c5d-4e6f-8a9b-1c2d3e4f5g6h
  Verify URL:    https://certnode.io/verify/7e3a9b2f-4c5d-4e6f-8a9b-1c2d3e4f5g6h
  Signed at:     2026-05-11T03:42:18Z
  RFC 3161:      ✓ countersigned by independent TSA
  Bitcoin:       ⏳ queued (confirms in 1-2 hours)

Suggested next steps:
  - Embed verify URL in your deliverable's footer / signature
  - Persist receipt id with the deliverable in your CRM / DMS
  - For LP / regulator / counsel delivery, include verify URL + "Designed for
    FRE 902(13)/(14) self-authenticating digital evidence" framing
```

## Related

- Skill: `sign-output` (the underlying implementation)
- Recipe: <https://certnode.io/docs/provenance/recipes/sign-finance-agent-outputs>
- Compliance: <https://certnode.io/docs/provenance/compliance>
