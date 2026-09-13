# KYC Screener — managed-agent 模板

## 概览

解析准入材料，运行规则引擎，筛查制裁/PEP，并标记缺口。本目录与 Cowork 插件 [`kyc-screener`](../../plugins/agent-plugins/kyc-screener) 使用同一套源文件——这里是用于 `POST /v1/agents` 的 Managed Agent cookbook。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export SCREENING_MCP_URL=...
../../scripts/deploy-managed-agent.sh kyc-screener
```

## Steering events

见 [`steering-examples.json`](./steering-examples.json)。

## 安全与 handoff

准入文档不可信（untrusted）。采用三层隔离：

| Tier | 会接触不可信文档？ | Tools | Connectors |
|---|---|---|---|
| **`doc-reader`** | **是** | 仅 `Read`, `Grep` | 无 |
| `rules-engine` / Orchestrator | 否 | `Read`, `Grep`, `Glob`, `Agent` | screening（只读） |
| **`escalator`**（持有 Write） | 否 | `Read`, `Write`, `Edit` | 无 |

`doc-reader` 只返回长度受限、并经 schema 校验的 JSON。`escalator` 会产出 `./out/escalation-<packet>.xlsx`。

**不保证：** 本代理只给出风险评级建议；最终由合规官决策。
