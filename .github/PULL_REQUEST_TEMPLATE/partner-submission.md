<!--
Use this template if you're submitting a third-party MCP connector or a
partner-built plugin. See CONTRIBUTING.md for the acceptance criteria.

For everything else (bug fixes, doc updates, new skills, new agents),
just open a regular PR — you don't need this template.
-->

## Partner / submission summary

- **Vendor name:**
- **Vendor URL:**
- **Submission type:** ☐ MCP connector  ☐ Partner-built plugin  ☐ Both
- **Vertical(s) it primarily supports:** <!-- e.g. equity-research, fund-admin -->
- **One-line description (for the README table):**

## Acceptance criteria checklist

Confirm each item before requesting review.

### Vendor / product
- [ ] Production product with a live website and public docs (not a side project / whitepaper / coming-soon)
- [ ] Existing real customers (or at least public case studies / press)
- [ ] License of all content added by this PR is compatible with Apache 2.0
- [ ] Scoped to financial services — see CONTRIBUTING.md for which verticals fit

### MCP / connector (if applicable)
- [ ] Endpoint URL is reachable from a fresh terminal (not behind a private beta)
- [ ] Authentication is documented — environment variable, OAuth flow, or browser session
- [ ] No credentials are bundled in source (including in any example file under this PR)
- [ ] Skills using the connector reference the vendor's public docs, not internal wikis

### Manifest / repo hygiene
- [ ] `python3 scripts/check.py` passes locally
- [ ] If this adds a new plugin, it's under `plugins/partner-built/<slug>/` with `.claude-plugin/plugin.json`
- [ ] If this adds a new MCP entry, it's in `plugins/vertical-plugins/financial-analysis/.mcp.json`
- [ ] README entry added (if the submission introduces a new top-level plugin or connector)
- [ ] The plugin's `.claude-plugin/plugin.json` `version` is patch-bumped if this PR modifies an existing plugin

### Partner-built plugin (only if applicable)
- [ ] My organization is a signatory on the Anthropic partner agreement (or I've been routed to the right Anthropic contact and acknowledged)

## What this submission adds

<!-- Concrete description: which skills, what the connector exposes, what
     the partner-built plugin does end to end. Link the relevant files. -->

## How to test

<!-- Step-by-step a reviewer can follow:
     1. Set env var X
     2. Install plugin Y
     3. Run /command Z
     4. Confirm <expected behavior>
-->

## Why this fits

<!-- One paragraph: which existing workflow this extends or which gap it
     closes, and how a customer of yours would use it from inside Claude. -->
