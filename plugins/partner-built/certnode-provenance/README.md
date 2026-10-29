# CertNode Provenance — Partner Plugin for Anthropic financial-services

Cryptographic provenance layer for Anthropic finance agents. Wraps any agent's deliverable with three-layer timestamped signing designed for **FRE 902(13)/(14)** self-authenticating digital evidence and **EU AI Act Article 50** disclosure.

## What this plugin does

Every output from a finance agent (pitch builder, earnings reviewer, IC memo, KYC screener, valuation reviewer, statement auditor, etc.) reaches a client, LP, regulator, auditor, or official record. Internal logging doesn't satisfy:

- **FRE 902(13) / 902(14)** admissibility when a deliverable becomes evidence
- **FINRA Rule 2241** recordkeeping for published research
- **BSA/AML** audit trail for KYC screening decisions
- **EU AI Act Article 50** machine-readable disclosure for AI-generated content (in force August 2026)

This plugin makes every output's cryptographic provenance a one-line addition:

```typescript
import { CertNode } from '@certnode/sdk'

const cert = new CertNode({ apiKey: process.env.CERTNODE_API_KEY! })
const signed = await cert.signAIOutput({
  output: pitchDeckContent,
  model: 'claude-opus-4-7',
  provider: 'anthropic',
})

// signed.receiptId — store with the deliverable in your CRM / DMS
// signed.verifyUrl — give to client / LP / regulator / counsel
// signed.timestamps.{certnode, rfc3161, bitcoin} — independent chain
```

## What the three timestamp layers prove

1. **Layer 1 (CertNode signature)** — ES256 JWS over content hash. Verifiable against CertNode's published public key. Reproducible by any opposing expert.
2. **Layer 2 (RFC 3161 timestamp)** — Countersignature from an independent Time Stamp Authority. The format cited in case law for self-authenticating digital evidence.
3. **Layer 3 (Bitcoin OpenTimestamps anchor)** — Merkle commitment to a Bitcoin block, confirmed within 1–2 hours. Strongest non-revocable proof-of-existence. Even if CertNode + the RFC 3161 TSA both disappear, the Bitcoin proof remains independently verifiable forever.

## Install

### As a Claude Code plugin

```bash
claude plugin marketplace add anthropics/claude-for-financial-services
claude plugin install certnode-provenance@claude-for-financial-services
```

### Via Cowork plugin UI

```
Settings → Plugins → Add plugin
Search for: certnode-provenance
```

### Direct npm install (for non-plugin usage)

```bash
npm install @certnode/sdk
```

## Auth

Get an API key at <https://certnode.io/dashboard/provenance>. Free tier: 100 receipts/month, no card required. Metered pricing above ($0.01/receipt with volume discounts down to $0.002).

Set in environment:

```bash
export CERTNODE_API_KEY=cn_live_...
```

The plugin's MCP server auto-reads this env var (see `plugin.json` → `mcpServers`).

## Privacy patterns for sensitive workflows

KYC screening, LP-statement audits, IC memos, and similar workflows touch PHI / PII / privileged content. CertNode supports a sealed-content pattern where raw content stays in your infrastructure and only a salted hash crosses the wire:

```typescript
const promptHash = crypto.createHash('sha256').update(SALT + sensitiveContent).digest('hex')

const signed = await cert.signAIOutput({
  output: `<sealed-content content-hash="${promptHash}" model="claude-opus-4-7" />`,
  model: 'claude-opus-4-7',
  provider: 'anthropic',
  promptHash,
})
```

CertNode receives only the sentinel + hash — no PHI, no privileged content, no client identifiers. See <https://certnode.io/docs/provenance/recipes/sign-user-prompts-privacy> for the full implementation.

## Verification

Anyone — client, LP, regulator, auditor, opposing counsel — can verify a receipt without a CertNode account:

```bash
# Public verify endpoint (no auth required)
curl -X POST https://certnode.io/api/v1/provenance/verify \
  -H "Content-Type: application/json" \
  -d '{"receiptId": "uuid-from-signed-deliverable"}'

# Or open in any browser:
# https://certnode.io/verify/uuid-from-signed-deliverable
```

For verification-only integrations (browser extensions, audit tooling, verification pipelines), use the lightweight verify-only SDK:

```bash
npm install @certnode/verify
```

## Compliance framing notes

- **"Designed for FRE 902(13)/(14)"** — not unqualified "court-admissible." No court has ruled on a CertNode receipt specifically. The underlying primitives (ES256, JWS, RFC 3161, OpenTimestamps) are well-precedented.
- **Independent verifiability** is the defensive cornerstone. Opposing experts run the same verification using open standards. Customers don't need to trust CertNode for the cryptography to hold.
- **Multi-model neutral** — works with Claude, OpenAI, Mistral, Llama, or any model. CertNode does not preference any AI provider.
- See <https://certnode.io/docs/provenance/compliance> for the full counsel-facing breakdown.

## Cross-references

- Recipe (end-to-end): <https://certnode.io/docs/provenance/recipes/sign-finance-agent-outputs>
- Solutions page (compliance mapping): <https://certnode.io/solutions/financial-services>
- API reference: <https://certnode.io/docs/provenance/api-reference>
- Compliance framing: <https://certnode.io/docs/provenance/compliance>
- npm SDK: <https://www.npmjs.com/package/@certnode/sdk>
- Verify-only SDK: <https://www.npmjs.com/package/@certnode/verify>
- MCP server: <https://www.npmjs.com/package/@certnode/mcp-server>

## License

Apache 2.0 (matches the parent anthropics/financial-services repo).

## About CertNode

CertNode provides cryptographic provenance APIs for AI outputs, chargeback evidence (Stripe Reflex), payment evidence vaults, and refund-abuse detection. <https://certnode.io>

For procurement / enterprise terms / SOC 2 evidence (in-flight): email <contact@certnode.io>.

**Important:** CertNode is not affiliated with or endorsed by Anthropic. This plugin is proposed as a community / partner integration to make finance-agent outputs compliance-defensible.
