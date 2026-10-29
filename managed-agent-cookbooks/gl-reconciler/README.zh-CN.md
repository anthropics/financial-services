# GL Reconciler — managed-agent 模板

## 概览

针对某个交易日与资产类别集合，找出总账（general ledger）与分账（subledger）之间的差异，追踪根因，并生成供财务主管签字的异常报告。

本目录与 Cowork 插件 [`gl-reconciler`](../../plugins/agent-plugins/gl-reconciler) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export GL_MCP_URL=...           # 只读 GL MCP
export SUBLEDGER_MCP_URL=...    # 只读 subledger MCP
../../scripts/deploy-managed-agent.sh gl-reconciler
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。用交易日与资产类别列表启动会话；后续事件可用于重新追踪某一条差异。

## 安全与 handoff

本代理需要读取交易对手/托管方对账单等外部文档——这些由第三方撰写的文件可能包含对抗性指令。该模板通过结构化隔离，确保文档中的 payload 无法触达 shell、写工具或公司系统：

| Tier | 会接触不可信文档？ | Tools | Connectors |
|---|---|---|---|
| **`reader`** | **是** | 仅 `Read`, `Grep` | 无 |
| **Orchestrator** | 否 | `Read`, `Grep`, `Glob`, `Agent` | 只读 GL + subledger MCP |
| **`resolver`**（持有 Write） | 否 | `Read`, `Write`, `Edit` | 无 |

`reader` 仅返回长度受限、并经 schema 校验的 JSON（由 `scripts/validate.py` 校验）。`critic` 会基于可信来源独立复核每一条差异，编排器再将结果交给 `resolver`。`resolver` 会将异常报告写入 `./out/`；它不会打开任何外部文件。

**Handoff：** 若要把已验证的 breaks 交给 Month-End Closer，编排器会在最终输出中发出面向 `month-end-closer` 的 `handoff_request`；`scripts/orchestrate.py`（或你的 Temporal/Airflow worker）将其路由为新的 steering event。allowlist + payload 校验模式见脚本。

**不保证：** 本流程不会写入系统记录（system of record）。对总账的调整仍需代理之外的人工审批。
