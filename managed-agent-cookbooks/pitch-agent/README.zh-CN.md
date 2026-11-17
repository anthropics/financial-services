# Pitch Agent — managed-agent 模板

## 概览

可比公司、可比交易、LBO → 品牌化 pitch deck，端到端完成。本目录与 Cowork 插件 [`pitch-agent`](../../plugins/agent-plugins/pitch-agent) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CAPIQ_MCP_URL=... DALOOPA_MCP_URL=...
../../scripts/deploy-managed-agent.sh pitch-agent
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。

## 安全与 handoff

任务拆分（task-decomposition）——与其说是处理不可信输入（数据来自 CapIQ/Daloopa MCP），不如说是为了并行与 artifact 隔离。只有一个 worker 持有 `Write`：

| Leaf | Tools | Connectors |
|---|---|---|
| `researcher` | `Read`, `Grep` | CapIQ、Daloopa（只读） |
| `modeler` | `Read`, `Bash`（沙箱） | CapIQ、Daloopa（只读） |
| **`deck-writer`**（持有 Write） | `Read`, `Write`, `Edit` | 无 |

通过 `pptx-author` / `xlsx-author` 产出文件到 `./out/pitch-<target>.pptx` 与 `./out/model.xlsx`。

**Handoff：** 若因 thesis 变更需要重建模型，编排器会发出面向 `model-builder` 的 `handoff_request`；`scripts/orchestrate.py`（或你的工作流引擎）将其路由为新的 steering event。allowlist + payload 校验模式见脚本。
