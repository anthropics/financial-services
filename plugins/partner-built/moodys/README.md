# Moody's Skills

A collection of AI agent skills that leverage [Moody's MCP tools](https://www.moodys.com) to produce professional financial analysis and reports. Each skill is a self-contained prompt-driven workflow that an AI coding agent (Cursor, Claude Code, etc.) can follow end-to-end.

This plugin includes a [Claude Code](https://docs.claude.com/en/docs/claude-code) manifest (`.claude-plugin/plugin.json`). The skills, MCP config, and assets are driven by `SKILL.md` frontmatter and `.mcp.json`.

## Quick start

### Claude Code

1. Install the plugin by pointing Claude Code at this directory (or install from a marketplace if available).
2. Ensure MCP access — the plugin ships with `.mcp.json` for the required Moody's servers. Provide valid API credentials.
3. Trigger a skill — ask Claude naturally. Each `SKILL.md` defines trigger phrases in its frontmatter.

## Plugin structure

```
plugin/
├── .claude-plugin/
│   └── plugin.json          # Claude Code manifest
├── .mcp.json                # MCP server configuration
├── README.md                # This file
└── skills/
    └── <skill-name>/
        ├── SKILL.md          # Skill definition (trigger, steps, schema)
        └── assets/           # Templates, images, or other bundled files
```

## Available skills

| Skill | Description | MCP Server |
|-------|-------------|------------|
| [Earnings Brief](skills/earnings-brief/SKILL.md) | Generates a Moody's-styled HTML report comparing earnings call transcripts across 2–5 companies, enriched with credit ratings, sector outlook, and news. | `Moodys MCP server` |
| [Peer Analysis](skills/peer-analysis/SKILL.md) | Produces an HTML peer analysis report comparing a target company against up to 3 credit peers, with structured sub-tables and a ratings overview. | `Moodys MCP server` |
| [Issuer Brief](skills/issuer-brief/SKILL.md) | Generates a comprehensive Public Information Book (PIB) HTML report covering company overview, financials, peer comparison, industry, strategy, management, credit profile, risks, and ESG. | `Moodys MCP server` |
| [Rating Analysis](skills/rating-analysis/SKILL.md) | Builds a PowerPoint (.pptx) rating pitch deck combining sector analysis, company credit overview, SWOT, peer comparison, and ESG. | `Moodys MCP server` |
| [Sector Brief](skills/sector-brief/SKILL.md) | Produces a research-driven HTML sector brief report combining Moody's sector outlook with broader industry research. | `Moodys MCP server` |

## How skills work

Each skill is defined by a `SKILL.md` file with two parts:

- **YAML frontmatter** — `name`, `description`, and trigger phrases that tell the agent when to activate the skill.
- **Markdown body** — step-by-step instructions the agent follows: which MCP tools to call, how to synthesize the data, and what artifact to produce.

Skills can bundle supporting assets (HTML templates, schemas, images) in an `assets/` directory alongside the `SKILL.md`.

## Adding a new skill

1. Create a new directory under `skills/` with a short, kebab-case name (e.g. `skills/credit-monitor/`).
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`) and detailed step-by-step instructions.
3. Place any templates or static files in an `assets/` subdirectory.
4. Update the **Available skills** table in this README.

## MCP servers

The plugin's `.mcp.json` declares the MCP servers that skills depend on. Currently configured:

| Server | Type | Endpoint |
|--------|------|----------|
| `Moodys MCP server` | HTTP | `https://api.moodys.com/genai-ready-data/Credit/mcp` |

Individual skills list their required server and the specific tools they call in their `SKILL.md`.

## License

Proprietary — Moody's Corporation. See repository root for full license terms.
