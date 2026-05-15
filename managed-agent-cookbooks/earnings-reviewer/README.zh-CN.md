# Earnings Reviewer — managed-agent 模板

## 概览

电话会 + 披露文件 → 模型更新 → 纪要草稿。本目录与 Cowork 插件 [`earnings-reviewer`](../../plugins/agent-plugins/earnings-reviewer) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export FACTSET_MCP_URL=... DALOOPA_MCP_URL=...
../../scripts/deploy-managed-agent.sh earnings-reviewer
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。可由你的编排层基于覆盖列表进行扇出（fan out）：每个 ticker 启动一个会话。

## 安全与 handoff

电话会纪要与新闻稿不可信（untrusted）。采用三层隔离：

| Tier | 会接触不可信文档？ | Tools | Connectors |
|---|---|---|---|
| **`transcript-reader`** | **是** | 仅 `Read`, `Grep` | 无 |
| `model-updater` / Orchestrator | 否 | `Read`, `Grep`, `Glob`, `Agent` | FactSet、Daloopa（只读） |
| **`note-writer`**（持有 Write） | 否 | `Read`, `Write`, `Edit` | 无 |

`transcript-reader` 只返回长度受限、并经 schema 校验的 JSON。`note-writer` 会产出 `./out/note-<ticker>.docx`，并将更新后的模型写到 `./out/model-<ticker>.xlsx`。

**Handoff：** 若财报驱动 thesis 变化需要重建 DCF，可发出面向 `model-builder` 的 `handoff_request`；`scripts/orchestrate.py` 会将其路由为新的 steering event。
