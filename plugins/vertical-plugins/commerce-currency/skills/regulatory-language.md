---
skill: regulatory-language
version: 2.0.0
vertical: commerce-currency
maintainer: kaelum@kaelum-financial-services
updated: 2026-05-09
---

# Regulatory Language

## Overview

This skill governs all approved regulatory language, prohibited terminology,
and framing rules for KAELUM across investor materials, platform copy,
public communications, legal documents, and partner submissions. All
K.A.T.E. agents and any content produced within the KAELUM ecosystem
must comply with these rules without exception.

## Mandatory Terminology

| Context | Approved Term | Never Use |
|---|---|---|
| The product | Commerce currency, Ai-governed currency | Cryptocurrency, crypto, token (standalone) |
| KLM units | KLM, KLM unit, commerce unit | Coin, token, crypto token |
| User accounts | Account, KLM account | Wallet |
| KLM creation | Issued, credited, allocated | Minted, mined |
| Transaction cost | Not applicable — no fees to users | Gas fee |
| Customer spend benefit | Spending discount, merchant-side discount | Cashback |
| Price floor | Fixed floor price, £0.09 floor | Pegged, backed |
| Ai reference (branded) | Ai (capital A, lowercase i) | AI |
| Intelligence layer | Claude, Anthropic Claude, specialised Claude instances | OpenAI, GPT, Gemini, multi-LLM |
| Network participants | Customers, Creators, Merchants | Users (generic), holders |

## Regulatory Positioning Statements

### Closed-Loop Exemption
Approved language:

> "KAELUM operates under the self-assessed closed-loop exemption under
> UK Electronic Money Regulations 2011 Regulation 3 and EU E-Money
> Directive 2009/110/EC Article 1(4). Kaelum Technologies Ltd is not
> required to hold FCA authorisation as an e-money institution."

Never claim the exemption has been formally approved by the FCA. It is
self-assessed. A formal written legal opinion is being obtained for
investor due diligence purposes.

### KLM Classification
Approved language:

> "KLM is classified as a Multi-Purpose Voucher (MPV) for UK VAT
> purposes. VAT is deferred to the point of merchant or creator
> redemption. KLM is not subject to the crypto tax regime. CARF
> does not apply."

### Not a Cryptocurrency
Approved language:

> "KAELUM is not a cryptocurrency. It is not blockchain-based,
> not speculative, and not subject to MiCA's cryptocurrency
> provisions. It is a genuinely new regulatory category:
> an Ai-governed closed-loop commerce currency."

### MiCA Position
Approved language:

> "KAELUM has pre-aligned with MiCA requirements. KLM does not
> fall within MiCA's asset-referenced token or e-money token
> definitions due to its closed-loop structure and limited
> network exemption."

## KLM Price Appreciation: Approved Regulatory Language

The following approved language must be used when describing the
KLM price appreciation mechanic in any regulatory, investor, or
public context:

### Describing the Mechanic
Approved language:

> "The KLM floor price is fixed at £0.09 and cannot fall below
> this level. K.A.T.E. monitors six network health signal categories
> and applies a 1.2% compounding appreciation to the KLM price
> ecosystem-wide when network conditions warrant it. Appreciation
> is one-directional and Ai-governed. It is not market-driven,
> not speculative, and not realisable by Customers through sale
> or external transfer."

### Not a Financial Instrument
Approved language:

> "KLM appreciation is determined solely by K.A.T.E. based on
> defined network health signals. It cannot be influenced by
> external market forces, individual participants, or speculative
> trading. KLM has no secondary market and cannot be transferred
> outside the network."

### Not a Collective Investment Scheme
Approved language:

> "Customers, Creators, and Merchants do not pool contributions
> with a view to receiving profits from appreciation. Appreciation
> is a governance output of K.A.T.E., not a return on investment.
> Participants join the network to access commerce utility, not
> to generate investment returns."

### Not Speculative
Approved language:

> "KLM appreciation is one-directional. The price can only rise
> above the floor, never fall below it. There is no volatility,
> no market cycle, and no risk of loss on the KLM price. A
> participant who purchases KLM at £0.09 will always hold KLM
> worth at least £0.09."

### Incentive Framing
Approved language:

> "The appreciation mechanic provides a legitimate, non-speculative
> incentive for all three participant types to remain active within
> the ecosystem, particularly given that Customers cannot redeem
> KLM for fiat and KLM is not a tradeable asset."

## Prohibited Phrases

Never use the following in any KAELUM context:

- "Invest in KLM" or "KLM investment"
- "KLM yields" or "KLM returns"
- "KLM staking" or "KLM rewards"
- "KLM price will rise" (use: "KLM price may appreciate subject
  to K.A.T.E. network assessment")
- "Guaranteed appreciation" (the floor is guaranteed, appreciation
  is not)
- "KLM is backed by fiat" (it is not backed, it has a floor price)
- "Deposit" when referring to KLM purchase
- "Interest" in any context relating to KLM holding
- "Profit" when describing participant value growth
- Any reference to OpenAI, GPT, Gemini, or competing AI models

## Em Dash Rule

Em dashes (—) are prohibited in all KAELUM content. Replace with
commas, semicolons, colons, or separate sentences. This applies to
all agents, all documents, all platform copy, and all public
communications without exception.

## Participant Language Rules

- Always reference all three participant types: Customers, Creators,
  and Merchants. Never refer to only two.
- Never use "users" as a generic term. Specify the participant type.
- Creator redemption: always clarify that Creators redeem through
  Kaelum Technologies Ltd, not directly to a bank account
- Merchant redemption: same rule as Creator redemption

## Commands

- `/regulatory-language:check` — Review a text input against all
  approved and prohibited language rules and return a compliance report
- `/regulatory-language:approved-statement` — Return the approved
  regulatory statement for a given topic (exemption, MPV, appreciation,
  CARF, MiCA)
- `/regulatory-language:terminology-audit` — Audit a document for
  prohibited terminology and return a corrected version
