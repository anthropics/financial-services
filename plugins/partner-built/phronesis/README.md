# Phronesis Plugin

This plugin connects Claude to **Phronesis**, a verified-correctness forecasting substrate built for AI-agent-native consumption. Where most financial-data plugins surface point-in-time observations, Phronesis surfaces **forward-looking forecasts with calibration evidence** — every forecast is backed by an auditable methodology ledger and a public Brier-score history.

Phronesis is built MCP-primary. Its design assumption is that an agent — not a human analyst — is the primary consumer. Skills and tool surfaces follow naturally; the MCP server is the source of truth.

## Substrate scope

Phronesis spans eight verticals (Pythia rings) where forecast quality compounds with substrate access:

| # | Vertical | Forecast surface |
|---|---|---|
| V#1 | Energy | Generation, consumption, LMP, capacity factor, dispatch stack, fuel-mix evolution |
| V#2 | Compute / AI | Foundation-model release timing, benchmark results, capacity buildouts, data-center power draw |
| V#3 | Healthcare | FDA approvals, clinical milestones, disease-incidence trajectories |
| V#4 | Climate | Hurricane landfalls, temperature records, extreme-weather event probabilities |
| V#5 | Regulatory | Legislation passage timing, agency decisions, court rulings |
| V#6 | Supply Chain | Macro indicators, trade-balance shifts, tariff outcomes |
| V#7 | Space Economy | Launch-success probabilities, mission timelines, commercial-milestone events |
| V#8 | Robotics | Adoption-timing curves, humanoid commercial deployment milestones |

Each vertical's forecasts are **emitted at industry-aggregate granularity** with calibration scorecard attestation and methodology-ledger transparency. Per-customer or per-asset forecasting is out of scope by design (Themis publish-gate enforces).

## How Phronesis differs from sibling partner-built plugins

- **LSEG**, **S&P Global**, and similar financial-data plugins answer *"what is true now"* from point-in-time data.
- Phronesis answers *"what is the calibrated probability distribution for this future event"* with an auditable accuracy track record.

The plugins are complementary. A pitch agent might pull current comparables from LSEG/S&P and forward-looking probability distributions from Phronesis to assemble a complete view.

## Status (Sprint 5.19, May 2026)

Plugin v0.2.0. Sprint 5.16 PR-Anthropic-Repo-1 landed the **plugin scaffold** (manifest, MCP connector at `https://phronesis-jrstinehour.replit.app/mcp`, agent-discovery surfaces). Sprint 5.19 PR-Anthropic-Repo-2 (this PR) adds **13 SKILL.md files**: eight per-vertical forecasting skills (V#1 Energy, V#2 Compute+AI, V#3 Healthcare, V#4 Climate, V#5 Regulatory, V#6 Supply Chain, V#7 Space, V#8 Robotics) and five cross-vertical capability skills (calibration-scorecard, methodology-ledger, forecast-distribution-comparison, scenario-attribution, evidence-chain-audit).

Skills land in `skills/<skill-name>/SKILL.md`. Each skill describes its tool-chaining workflow against the Phronesis MCP server, the canonical query shape, the calibration evidence it surfaces, and the disclaimer scope.

Roadmap (Sprint 5.20+):

- **PR-Anthropic-Repo-3**: Managed Agent cookbook entry under `managed-agent-cookbooks/phronesis-forecaster/` for direct deployment via the Claude Managed Agents API.
- **PR-Anthropic-Repo-4**: Worked examples, deployment patterns, and final validation refinements.

## How to use

### In Claude Cowork

1. Open Claude Desktop and navigate to the **Cowork** tab
2. Click **Customize with Plugins**
3. In Browse Plugins, select **Personal** (or your team marketplace once Phronesis is admitted)
4. Click the **plus sign "+"** to add the Phronesis plugin
5. The MCP server requires no per-user authentication for the public-tier endpoints; paid-tier access uses standard MCP credential handoff

Once installed, Phronesis tool surfaces become available automatically. Commands and skills land in PR-Anthropic-Repo-2..5.

### In Claude Code

Follow the instructions on the [Claude Code documentation](https://code.claude.com/docs/en/discover-plugins#add-from-github).

### Direct MCP integration

The MCP server is platform-agnostic. Any MCP-compatible client can connect directly:

```json
{
  "mcpServers": {
    "phronesis": {
      "type": "http",
      "url": "https://phronesis-jrstinehour.replit.app/mcp"
    }
  }
}
```

## Calibration evidence

Phronesis publishes a public calibration scorecard at `https://phronesis-jrstinehour.replit.app/scorecard` (live) and a methodology ledger at `https://phronesis-jrstinehour.replit.app/methodology-ledger` (Sprint 5.19+). Every forecast emission cites the methodology version, the evaluation horizon, and the Brier-score history of the relevant Pythia ring at the time of emission. Forecasts are **not** marketing claims; they are calibrated probability distributions with auditable accuracy.

## Pricing

Phronesis offers a six-tier pricing structure surfaced at `https://phronesis-jrstinehour.replit.app/pricing`:

| Tier | Audience | Surface |
|---|---|---|
| 1 | Discovery (free) | Aggregated forecast queries; rate-limited |
| 2-4 | Researchers, advisory firms, agent platforms | Self-serve subscription via Stripe |
| 5 | Enterprise | Sales-led; SOC 2 + DPA |
| 6 | Outcome-conditional | Custom; success-based pricing |

For agent customers, Phronesis is x402-compliant: paid endpoints respond to unauthenticated calls with a `402 Payment Required` payload that lists accepted rails (Stripe ACS, Circle Arc USDC, Coinbase Business). Agents pay via their preferred rail and retry with a payment-proof header.

## Feedback and roadmap

Phronesis is in active development. Issue tracking and roadmap discussion live at the upstream Phronesis repository: <https://github.com/sustainable-finance-partners/phronesis>.

## License

Licensed under the Apache 2.0 License. See `LICENSE` in this directory.

Copyright 2026-present Sustainable Finance Partners, LLC.
