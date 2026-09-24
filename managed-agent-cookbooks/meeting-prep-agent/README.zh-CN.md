# Meeting Prep Agent — managed-agent 模板

## 概览

每次客户会议前生成简报包。本目录与 Cowork 插件 [`meeting-prep-agent`](../../plugins/agent-plugins/meeting-prep-agent) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CRM_MCP_URL=... CAPIQ_MCP_URL=...
../../scripts/deploy-managed-agent.sh meeting-prep-agent
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。通常由你的工作流引擎从日历事件触发。

## 安全与 handoff

客户提供的文档与入站邮件均不可信（untrusted）。采用三层隔离：

| Tier | 会接触不可信文档？ | Tools | Connectors |
|---|---|---|---|
| `profiler` | 否 | `Read`, `Grep` | CRM、CapIQ（只读） |
| **`news-reader`** | **是** | 仅 `Read`, `Grep` | 无 |
| **`pack-writer`**（持有 Write） | 否 | `Read`, `Write`, `Edit` | 无 |

`pack-writer` 会产出 `./out/briefing-<client>.pptx`；它不会直接打开客户提供的内容。

**不保证：** 简报包面向顾问，而非客户。不会直接面向客户发送。
