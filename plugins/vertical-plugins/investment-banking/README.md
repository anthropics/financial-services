# Investment Banking Plugin

Investment banking productivity tools for equity research, valuation, presentations, and deal materials.

## Features

- **Deal Materials** - CIMs, teasers, process letters, and buyer lists
- **Presentations** - Strip profiles, pitch decks with branded templates
- **Transaction Support** - Merger models, deal tracking, and data packs

## Installation

```bash
claude --plugin-dir /path/to/investment-banking
```

Or copy to your project's `.claude-plugin/` directory.

## Commands

| Command | Description |
|---------|-------------|
| `/one-pager [company]` | One-page strip profile for pitch books |
| `/cim [company]` | Draft Confidential Information Memorandum |
| `/teaser [company]` | Anonymous one-page company teaser |
| `/buyer-list [company]` | Strategic and financial buyer universe |
| `/merger-model [deal]` | Accretion/dilution M&A analysis |
| `/process-letter [deal]` | Bid instructions and process correspondence |
| `/deal-tracker` | Track live deals, milestones, and action items |

## Skills

### Deal Materials
| Skill | Description |
|-------|-------------|
| **cim-builder** | Draft Confidential Information Memorandums |
| **teaser** | Anonymous one-page company teasers |
| **process-letter** | Bid instructions and process correspondence |
| **buyer-list** | Strategic and financial buyer universe |
| **datapack-builder** | Build data packs from CIMs and filings |

### Presentations
| Skill | Description |
|-------|-------------|
| **strip-profile** | Information-dense company profiles for pitch books |
| **pitch-deck** | Populate pitch deck templates with data |

### Transaction Support
| Skill | Description |
|-------|-------------|
| **merger-model** | Accretion/dilution M&A analysis |
| **deal-tracker** | Track live deals, milestones, and action items |

## Example Workflows

### One-Page Strip Profile
```
/one-pager Target

# Generates:
# - Single-slide company profile using PPT template
# - 4 quadrants: Overview, Business, Financials, Ownership
# - Respects template margins and branding
```

### CIM Drafting
```
/cim Target

# Generates:
# - Full CIM document with executive summary, business overview,
#   financial analysis, and market positioning
```

### Merger Model
```
/merger-model Acquirer acquiring Target

# Generates:
# - Accretion/dilution analysis
# - Sources and uses, pro forma financials
# - Sensitivity on purchase price and synergies
```
