# Contributing

Thanks for contributing to Claude for Financial Services. This repo is a set of reference templates: real firms fork it and tune the prompts, skills, and connectors to how they actually work. Contributions that make the reference templates clearer, more correct, or broader in coverage are very welcome.

## What we accept

Three categories, with different bars.

### 1. Fixes and improvements to existing content

Bug fixes, typos, broken links, clearer wording, additional examples in an existing skill, better defaults. **Open a PR directly** — no preamble needed. Keep the diff focused (one fix per PR).

Before pushing:

- Run `python3 scripts/check.py` — it lints every manifest, verifies cross-file references resolve, and fails if any `agent-plugins/<slug>/skills/` copy has drifted from its `vertical-plugins/` source.
- If you edited a skill in `plugins/vertical-plugins/`, run `python3 scripts/sync-agent-skills.py` to propagate the change into the agent bundles that use it.
- If you edited any plugin's files, the local pre-commit hook (`.githooks/pre-commit`) patch-bumps that plugin's `.claude-plugin/plugin.json` `version` field automatically. The `version-bump` GitHub Action enforces this on PRs as a backstop.

### 2. New skills, commands, or agents

Adding coverage for a workflow we don't have yet. Open a PR; we'll review for fit and quality.

- **New skill** → add it under `plugins/vertical-plugins/<vertical>/skills/<skill-name>/SKILL.md` with valid frontmatter (`name`, `description`). Then run `python3 scripts/sync-agent-skills.py`.
- **New slash command** → `plugins/vertical-plugins/<vertical>/commands/<command-name>.md` with frontmatter (`description`, `argument-hint`, `allowed-tools`).
- **New agent** → `plugins/agent-plugins/<slug>/` (with `agents/<slug>.md` + bundled `skills/`) **and** a matching `managed-agent-cookbooks/<slug>/` (with `agent.yaml`, subagent yamls, `steering-examples.json`, `README.md`).

Each agent should ship both ways — Cowork plugin and Managed Agent cookbook — from one source. See `plugins/agent-plugins/pitch-agent/` and `managed-agent-cookbooks/pitch-agent/` as the canonical reference.

### 3. Partner submissions (MCP connectors and partner-built plugins)

Submissions from a third-party data, research, or workflow vendor that adds the vendor's product as an MCP connector or partner-built plugin. **Use the [Partner Submission](.github/PULL_REQUEST_TEMPLATE/partner-submission.md) PR template** — append `?template=partner-submission.md` to the new-PR URL, or copy the template into the PR description manually.

The bar is higher than for category 2 because partner submissions are public endorsements of the vendor's product.

## Partner submission acceptance criteria

We accept partner submissions that meet **all** of the following:

| Criterion | What it means |
|---|---|
| **Real product, real users** | A production vendor in financial data, research, workflow, or document tooling — not a personal project, side experiment, or whitepaper. Live website, public docs, real customers. |
| **Live MCP endpoint or supported connector** | If the submission adds an MCP connector, the endpoint URL must be reachable and the documented interface must match what's deployed. We will not merge MCP entries that 404, are gated on a private beta, or are aspirational. |
| **Auth pattern documented** | Environment variable, OAuth flow, or signed-in browser session — whichever the provider uses. No bundled credentials, ever. The README must clearly state how a customer of the provider authenticates from Claude. |
| **Skills reference the provider's public docs** | If the PR adds skills that use the connector, those skills must link to the provider's own public documentation for the tools they call — not to internal wikis or sales decks. |
| **License-compatible** | All content added by the PR is compatible with this repository's Apache 2.0 license. The PR description must affirm this. |
| **Manifests pass `check.py`** | `python3 scripts/check.py` exits 0 against the PR's branch. CI runs this on every PR. |
| **Scoped to financial services** | The product solves a workflow that fits the verticals we cover (investment banking, equity research, private equity, wealth management, fund admin, operations, risk/compliance) or extends them with adjacent finance workflows. General-purpose tools without a clear finance angle are usually a better fit elsewhere. |
| **For "partner-built" plugins specifically** | The vendor must be a signatory on the Anthropic partner agreement. Open a PR; if your organization is not yet a signatory, we'll route you to the right Anthropic contact before review. MCP-only submissions do not require a partner agreement. |

## What we don't accept

- **Aspirational / coming-soon** integrations — wait until the endpoint is live, then submit.
- **Plugins that wrap a non-financial product** with finance-themed copy. The Claude Code marketplace has broader categories for general-purpose tools.
- **Duplicate / competing submissions** of the same partner from different authors. We'll batch and ask the partner to pick one to maintain.
- **Personal investing tools targeting retail end-users.** This repo's audience is institutional — banks, asset managers, funds, advisors. Retail-focused tooling is a better fit for the consumer Claude marketplace.
- **Submissions that bundle credentials** in source — under any wrapper. Reject on sight.

## Review process

1. **CI must pass** — `check.py` lint and version-bump check both green.
2. **Reviewer assigned** within ~5 business days for partner submissions; less for fixes.
3. **Review focus**:
   - Manifest correctness (paths resolve, frontmatter valid, skills present)
   - Skill quality (clear instructions, realistic worked examples, references the actual provider docs)
   - Partner criteria above
   - Marketplace listing description fits in one line in the README table
4. **Iteration** — most reviews ask for at least one round of changes. Please respond to comments in-line; don't open a new PR for the same submission.
5. **Decision** — merge, request changes, or close with reason. Closure does not preclude resubmission after the underlying issue is addressed.

## What changes don't need a PR

- Forking the repo and editing freely in your own copy. That's the point of the templates.
- Internal customizations of skills, prompts, or connectors for your firm. Keep those in your own fork.
- One-off questions — open an issue.

## License

By contributing, you agree your contributions are licensed under the [Apache License 2.0](./LICENSE).
