# Connectors — Fund Administration

This plugin works in **standalone mode** and is **supercharged with MCP connectors**.

## Core Feature Set (Standalone)

- Period-end accrual schedules and draft journal entry calculations
- GL-to-subledger position and trade reconciliation
- Reconciliation break root-cause tracing
- LP statement NAV tie-out calculations
- Balance sheet roll-forward and flux variance commentary

## Supercharged Features (with MCPs)

| MCP | Categories | Unlocks | Enhanced Skills |
|-----|------------|---------|-----------------|
| **Internal GL** | `fund-accounting` | General ledger query API for journal entries, account balances, and posting details | `gl-recon`, `break-trace`, `accrual-schedule`, `roll-forward`, `variance-commentary` |
| **Subledger** | `fund-accounting` | Subledger transaction feeds, trade records, and settlement feeds | `gl-recon`, `break-trace` |
| **NAV** | `fund-accounting` | Fund NAV calculation packs, capital account tables, and LP distribution statements | `nav-tieout` |
