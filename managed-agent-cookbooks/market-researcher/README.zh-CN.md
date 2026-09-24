# Market Researcher — managed-agent 模板

## 概览

行业/主题 → 行业概览 → 竞争格局 → 同业可比 → 想法清单 → 研究纪要。本目录与 Cowork 插件 [`market-researcher`](../../plugins/agent-plugins/market-researcher) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CAPIQ_MCP_URL=... FACTSET_MCP_URL=...
../../scripts/deploy-managed-agent.sh market-researcher
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。可由 research-queue 事件触发，或由覆盖地图扇出（fan out）并行运行。

## 安全与 handoff

第三方报告与发行人材料不可信（untrusted）。采用三层隔离：

| Tier | 会接触不可信文档？ | Tools | Connectors |
|---|---|---|---|
| **`sector-reader`** | **是** | 仅 `Read`, `Grep` | 无 |
| `comps-spreader` / Orchestrator | 否 | `Read`, `Grep`, `Glob`, `Agent` | CapIQ、FactSet（只读） |
| **`note-writer`**（持有 Write） | 否 | `Read`, `Write`, `Edit` | 无 |

`sector-reader` 只返回长度受限、并经 schema 校验的 JSON。`note-writer` 会产出 `./out/primer-<sector>.docx`（若请求 slides，也会生成 `.pptx`）。

**Handoff：** 若要对想法清单中的单一标的建模，可发出面向 `model-builder` 的 `handoff_request`；`scripts/orchestrate.py` 会将其路由为新的 steering event。
