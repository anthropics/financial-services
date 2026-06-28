# Sector Seed Companies Reference

When the user specifies a sector but not specific companies, use these seed lists to bootstrap the company universe. These are starting points — always expand via `get_competitors_from_identifiers` and validate with `get_info_from_identifiers`.

> **All seeds below have been validated against S&P Global's identifier system.** If a seed fails to resolve, try the alias listed in parentheses before dropping it.

## Technology / Software

### AI / Machine Learning
Seeds: OpenAI, Anthropic, Databricks, Scale AI, Cohere, Hugging Face, Mistral AI, xAI, Perplexity AI, Runway ML (alias: "Runway AI, Inc."), Together AI (alias: "Together Computer, Inc."), Character.ai (alias: "Character Technologies, Inc."), Groq, Stability AI, Aleph Alpha, Magic AI

⚠️ **Excluded (do not use as seeds):**
- *Inflection AI* — Core team absorbed by Microsoft (Mar 2024). Historical rounds exist but no new activity.
- *Adept AI* — Largely absorbed by Amazon (2024). Same as above.
- *DeepMind* — Subsidiary of Alphabet. No independent funding rounds.

### Cybersecurity
Seeds: CrowdStrike, Palo Alto Networks, Wiz, Snyk, SentinelOne, Abnormal Security, Netskope

### Cloud Infrastructure / DevTools
Seeds: Snowflake, HashiCorp, Datadog, Confluent, Vercel, Supabase, PlanetScale

### Fintech
Seeds: Stripe, Plaid, Brex, Ramp, Mercury, Affirm, Marqeta, Navan

### Vertical SaaS
Seeds: ServiceTitan, Toast, Procore, Veeva Systems, Blend Labs

## Healthcare / Life Sciences

### Biotech / Pharma
Seeds: Moderna, BioNTech, Recursion Pharmaceuticals, Tempus AI, Insitro, AbCellera

### Digital Health
Seeds: Teladoc, Hims & Hers, Ro, Noom, Color Health

⚠️ **Excluded (do not use as seeds):**
- *Cerebral* — Still operating but has faced significant regulatory issues; include only if the user specifically requests it.

### Medical Devices
Seeds: Intuitive Surgical, Butterfly Network, Outset Medical

⚠️ **Excluded (do not use as seeds):**
- *Shockwave Medical* — Acquired by Johnson & Johnson (May 2024). Now a subsidiary with no independent funding rounds.

## Energy / Climate

### Climate Tech
Seeds: Redwood Materials, Form Energy, Commonwealth Fusion, Sila Nanotechnologies, Climeworks

### Clean Energy
Seeds: Enphase Energy, First Solar, Rivian, QuantumScape, Sunnova

## Consumer

### E-Commerce / Marketplace
Seeds: Shopify, Faire, Whatnot, Fanatics

⚠️ **Excluded (do not use as seeds):**
- *Temu (PDD Holdings)* — PDD Holdings is a massive public conglomerate; its funding activity is captured via equity markets, not venture rounds.

### Consumer Social / Media
Seeds: Discord, Reddit, Substack

⚠️ **Excluded (do not use as seeds):**
- *BeReal* — Acquired by Voodoo (Jun 2024). Now a subsidiary.
- *Lemon8* — The brand name "Lemon8" resolves in S&P Global to a small Dutch company (Lemon8 B.V.), **not** the ByteDance social media app. ByteDance's apps are subsidiaries and do not have independent funding rounds. Do not use.

## Industrials / Logistics

### Logistics / Supply Chain
Seeds: Flexport, Samsara, Project44, FourKites

⚠️ **Excluded (do not use as seeds):**
- *Convoy* — Shut down operations (Oct 2023). The identifier still resolves and historical rounds are available, but no new activity will appear.

### Robotics / Automation
Seeds: Figure AI, Agility Robotics, Locus Robotics, Symbotic, Covariant

### Space / Aerospace
Seeds: SpaceX, Relativity Space, Rocket Lab, Planet Labs, Astra

## Identifier Alias Reference

Some well-known brand names don't match S&P Global's legal entity names. If a brand name returns empty results from `get_info_from_identifiers`, try the alias:

| Brand Name | S&P Global Legal Name | company_id |
|---|---|---|
| Together AI | Together Computer, Inc. | C_1860042219 |
| Character.ai | Character Technologies, Inc. | C_1829047235 |
| Runway ML | Runway AI, Inc. | C_633706980 |
| Adept AI | Adept AI Labs Inc. | C_1780739313 |
| xAI | X.AI LLC | C_1863863313 |

> **Tip:** When a brand name fails, try `get_info_from_identifiers` with the legal name. If that also fails, the company may not be indexed yet. As a last resort, use the `company_id` directly as the identifier.

## Notes

- These lists skew toward US-based companies. For geographic filtering (Europe, Asia, etc.), the competitor expansion step is especially important.
- For niche sub-sectors not listed here, ask the user for 2–3 example companies to use as seeds.
- Always validate seeds are still active/relevant — companies pivot, merge, or shut down.
- **Refresh cadence:** These seeds should be reviewed quarterly. AI sector seeds in particular change rapidly due to acquisitions and new entrants.
- Seeds marked as subsidiaries or acquired will still resolve in `get_info_from_identifiers` (status = "Operating Subsidiary") but will return zero funding rounds. Skip these for funding queries.
