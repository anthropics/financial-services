# Valuation Reviewer — managed-agent 模板

## 概览

导入 GP 包，运行估值模板，准备 LP 报告。本目录与 Cowork 插件 [`valuation-reviewer`](../../plugins/agent-plugins/valuation-reviewer) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export PORTFOLIO_MCP_URL=...
../../scripts/deploy-managed-agent.sh valuation-reviewer
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。

## 安全与 handoff

GP 提供的估值材料不可信（untrusted）。采用三层隔离：

| Tier | 会接触不可信文档？ | Tools | Connectors |
|---|---|---|---|
| **`package-reader`** | **是** | 仅 `Read`, `Grep` | 无 |
| `valuation-runner` / Orchestrator | 否 | `Read`, `Grep`, `Glob`, `Agent` | portfolio（只读） |
| **`publisher`**（持有 Write） | 否 | `Read`, `Write`, `Edit` | 无 |

`package-reader` 只返回长度受限、并经 schema 校验的 JSON。`publisher` 会产出 `./out/lp-pack-<fund>.xlsx`。

**Handoff：** 若要将标记的被投公司（portcos）交给 GL Reconciler 进一步处理，可发出面向 `gl-reconciler` 的 `handoff_request`；`scripts/orchestrate.py` 会负责路由。

**不保证：** LP 报告在本代理之外仍需 IR 与 CCO 签字确认。
