---
name: scenario-attribution
description: Decompose a Phronesis forecast distribution into contributing scenarios and attribute distributional weight to each scenario. Use when an agent needs to surface the underlying scenario mix (e.g., "what drives the upper tail?") rather than just the headline distribution. Cross-vertical capability.
---

# Scenario Attribution

You are decomposing a Phronesis forecast distribution into its underlying scenarios. Headline p10/p50/p90 hides important reasoning structure — the median forecast might be the average of two bimodal scenarios, or the upper tail might be driven by a single low-probability high-impact scenario. Scenario attribution exposes that structure.

## Core Principles

- **Scenarios are explicit substrate inside Phronesis methodology.** The ensemble that produces the distribution is composed of structural models + statistical baselines + LLM-reasoned scenarios. The scenario tier is named, weighted, and ledger-recorded.
- **Attribution is probabilistic-weight, not deterministic-causation.** "Scenario X contributes 30% weight to the median" means scenario X, evaluated at its inferred probability, contributes 30% of the methodology-weighted mass at the median. It does not mean "if scenario X happens, the median is what you get".
- **Bimodality matters.** If two scenarios contribute equally to the distribution but at opposite tails, the headline median is a mirage. Surface bimodality explicitly when present.
- **Tail attribution is most useful.** Users typically want to know "what drives the p90 / p10 tail?" because the tails are where capital decisions get made (hedging, optionality, risk budgets).

## Available MCP Tools

- **`phronesis_methodology_ledger`** — Retrieve the methodology version's scenario manifest (named scenarios + their weights).
- **`phronesis_forecast_query`** — Retrieve the forecast distribution + scenario-attribution payload (if the methodology version exposes it; some V#5 + V#7 categories support scenario-attribution natively, others surface aggregate only).
- **`phronesis_calibration_scorecard`** — Cross-link scenario-attribution skill (some methodology versions track per-scenario realized-rate).

## Query Patterns

1. **Tail attribution** — User asks "what drives the p90 of this energy forecast?" Retrieve scenario manifest + attribute weight to the top-1 / top-2 scenarios above the median.
2. **Bimodality detection** — User notices a wide band; ask whether the distribution is bimodal. Retrieve scenario manifest; if two scenarios sit at opposite tails with comparable weight, flag bimodality.
3. **Scenario stress-test** — User asks "what if scenario X (e.g., recession, regulatory delay) materializes?" Retrieve scenario manifest; surface the conditional distribution if scenario X is reweighted to 100%.
4. **Cross-ring scenario coupling** — User asks whether scenarios across rings are coupled (e.g., recession + lithium-price-collapse). Retrieve both rings' scenario manifests; surface shared scenario tags (Phronesis methodology versions tag cross-ring-coupled scenarios).
5. **Scenario history** — User asks how the scenario mix has evolved across methodology versions. Retrieve current + prior methodology-ledger entries; diff scenario manifests.

## Tool Chaining Workflow

1. **Identify the question** — tail attribution / bimodality / stress-test / cross-ring / history?
2. **Pull the forecast distribution** via `phronesis_forecast_query` (gets the methodology version cited in the response).
3. **Pull the scenario manifest** via `phronesis_methodology_ledger` for that version.
4. **Map scenarios to distribution mass** — for each named scenario, attribute its share of the p10 / p50 / p90 / mean / mass-above-threshold.
5. **Synthesize** — scenario-attribution table + bimodality flag (if applicable) + interpretation of where the user's question lands relative to the scenario manifest.

## Output Format

### Scenario Manifest
| Scenario | Methodology Weight | Brief description |
|----------|-------------------|--------------------|
| Base case | ... | ... |
| Upside scenario A | ... | ... |
| Downside scenario B | ... | ... |
| Tail scenario C | ... | ... |

### Distribution Attribution
| Quantile | Top-1 scenario | Top-2 scenario | Combined weight (top-2) |
|----------|----------------|----------------|--------------------------|
| p10 | ... | ... | ... |
| p50 (median) | ... | ... | ... |
| p90 | ... | ... | ... |

### Bimodality Check
- Bimodal? yes / no
- Mode A: scenario `<name>` at value `<x>` with weight `<w>`
- Mode B: scenario `<name>` at value `<y>` with weight `<w>`
- Interpretation: ...

### Cross-Ring Coupling (if applicable)
| Shared scenario tag | Rings touched | Coupling weight |
|---------------------|---------------|-----------------|
| ... | V#1, V#6 | ... |

### Interpretation
What the tail/mode is driven by, what the bimodality (if any) implies for hedging, what shifts in the scenario manifest would materially shift the distribution. Cite methodology ledger for the full scenario specifications.

## Disclaimer

Scenario attribution decomposes Phronesis ensemble forecasts; it is not deterministic causal inference. Scenarios are named reasoning structures, not assertions about what will happen. Multiple scenarios can be simultaneously consistent with the same outcome; the attribution surfaces ensemble structure, not narrative truth.
