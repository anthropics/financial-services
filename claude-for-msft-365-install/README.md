# Claude for Office — Direct Cloud Setup

Admin tooling for configuring the Claude Office add-in to call your own cloud
(Vertex AI, Bedrock, or an LLM gateway) instead of Anthropic's API.

## Install

```bash
claude plugin marketplace add anthropics/financial-services
claude plugin install claude-for-msft-365-install@claude-for-financial-services
```

Then inside the session: `/claude-for-msft-365-install:setup`

## Update

Pull the latest version of the plugin:

```bash
claude plugin update claude-for-msft-365-install@claude-for-financial-services
```

Restart the session to apply. Re-run `/claude-for-msft-365-install:setup` only
if you need to regenerate the manifest with new options.

## Bootstrap

For per-user MCP servers, skills, or dynamic config, host a bootstrap endpoint
and point the add-in at it:

```bash
claude plugin marketplace add anthropics/financial-services   # if not already added
claude plugin install claude-for-msft-365-install@claude-for-financial-services
```

Then inside the session: `/claude-for-msft-365-install:bootstrap`

## Commands

| Command | What it does |
|---|---|
| `/claude-for-msft-365-install:setup` | Interactive wizard — provisions cloud resources, admin consent, writes manifest |
| `/claude-for-msft-365-install:manifest` | Generate the customized add-in manifest XML |
| `/claude-for-msft-365-install:consent` | Azure admin consent URL for the add-in's app registration |
| `/claude-for-msft-365-install:update-user-attrs` | Write per-user config via Microsoft Graph extension attributes |
| `/claude-for-msft-365-install:bootstrap` | Build the bootstrap endpoint — per-user MCP servers, skills, dynamic config |
| `/claude-for-msft-365-install:debug` | Diagnose deployment issues — stale config, connect failures, missing add-in |
