---
description: Find the controlling EU-regulation text for a question, returned as citable Article-paragraphs and recitals
argument-hint: "<question> [act e.g. MiCA / MiFID II] [article e.g. 20]"
---

# Regulation Lookup

> Uses the Aether `regulation_search` tool. See [CONNECTORS.md](../CONNECTORS.md) for parameters.

Find the controlling text in the EU financial-regulation corpus and return it as **citable**
units with breadcrumbs (e.g. `MiCA 2023/1114 · Art. 4 · para. 1`). See the
**eu-regulation-research** skill for the CELEX map and consolidated-vs-OJ guidance.

## Workflow

### 1. Gather Input
- Question (required).
- Optional: which act (map to CELEX), specific article, doc type, AML topic.

### 2. Search
Call `regulation_search` with:
- `query`: the question phrased naturally.
- `celex`: if the user named an act — e.g. `32023R1114` (MiCA), `32014L0065` (MiFID II),
  `32013R0575` (CRR), `32022R2554` (DORA), `32024R1624` (AMLR). See the skill for the full map.
- `article`: if they cited a specific article.
- `aml_topics`: for AML questions (e.g. `cdd`, `edd`, `pep`, `str_reporting`).
- `prefer_consolidated`: `true` when the user wants current in-force text rather than as-published.
- `limit`: 10.

### 3. Synthesize
- Quote the operative provision **verbatim**.
- Always include the breadcrumb citation returned with each unit.
- If consolidated and original text differ materially, note both.

## Output Format

Lead with a 1-2 sentence answer grounded in the provision, then:

| Provision (verbatim) | Citation | Type |
|----------------------|----------|------|
| "…" | MiCA 2023/1114 · Art. 4 · para. 1 | paragraph |

Close with a plain-language reading. Flag that this is the corpus text, not legal advice, and
note if the question spans acts not in the 29-act corpus.
