# Month-End Closer — managed-agent 模板

## 概览

计提、滚动表与差异说明。本目录与 Cowork 插件 [`month-end-closer`](../../plugins/agent-plugins/month-end-closer) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export GL_MCP_URL=...
../../scripts/deploy-managed-agent.sh month-end-closer
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。

## 安全与 handoff

支持性发票与供应商对账单均不可信（untrusted）。采用三层隔离：

| Tier | 会接触不可信文档？ | Tools | Connectors |
|---|---|---|---|
| **`ledger-reader`** | **是** | 仅 `Read`, `Grep` | 无 |
| `rollforward` / Orchestrator | 否 | `Read`, `Grep`, `Glob`, `Agent` | internal-gl（只读） |
| **`poster`**（持有 Write） | 否 | `Read`, `Write`, `Edit` | 无 |

`poster` 会产出 `./out/close-package-<entity>-<period>.xlsx`。JE 草稿仅用于暂存，不会直接入账到 GL。

**Handoff：** 接收来自 `gl-reconciler` 的 `handoff_request`（已验证的 breaks），并将其纳入月结差异说明。
