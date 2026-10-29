# Statement Auditor — managed-agent 模板

## 概览

在分发前审计预生成的 LP 对账单。本目录与 Cowork 插件 [`statement-auditor`](../../plugins/agent-plugins/statement-auditor) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export NAV_MCP_URL=...
../../scripts/deploy-managed-agent.sh statement-auditor
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。

## 安全与 handoff

生成的对账单被视为不可信（上游系统不在本代理范围内）。采用三层隔离：

| Tier | 会接触不可信文档？ | Tools | Connectors |
|---|---|---|---|
| **`statement-reader`** | **是** | 仅 `Read`, `Grep` | 无 |
| `reconciler` / Orchestrator | 否 | `Read`, `Grep`, `Glob`, `Agent` | nav（只读） |
| **`flagger`**（持有 Write） | 否 | `Read`, `Write`, `Edit` | 无 |

`flagger` 会产出 `./out/signoff-<batch>.xlsx`。

**不保证：** 本代理只给出通过/暂缓的建议；IR 在人工签字后再分发。
