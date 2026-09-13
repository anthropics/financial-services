# Model Builder — managed-agent 模板

## 概览

DCF、LBO、三表、可比——以文件 artifact 形式产出。本目录与 Cowork 插件 [`model-builder`](../../plugins/agent-plugins/model-builder) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CAPIQ_MCP_URL=... DALOOPA_MCP_URL=...
../../scripts/deploy-managed-agent.sh model-builder
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。

## 安全与 handoff

任务拆分（task-decomposition）——输入来自可信 MCP，因此隔离重点在 artifact 边界与复核。只有一个 worker 持有 `Write`：

| Leaf | Tools | Connectors |
|---|---|---|
| `data-puller` | `Read`, `Grep` | CapIQ、Daloopa（只读） |
| **`builder`**（持有 Write） | `Read`, `Write`, `Edit`, `Bash`（沙箱） | 无 |
| `auditor` | `Read`, `Grep` | 无 |

`auditor` 会在 `builder` 写出 `./out/model.xlsx` 后重新检查勾稽与平衡。

**Handoff：** 当从 `earnings-reviewer` 或 `pitch-agent` 调用时，调用方输出中的 `handoff_request` 会由 `scripts/orchestrate.py` 路由到这里，作为新的 steering event。
