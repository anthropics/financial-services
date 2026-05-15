# 金融服务的 Managed Agent 模板

本仓库中的每个代理都以**两种方式**发布：一种是分析师今天就能安装使用的 Cowork 插件（见仓库根目录下按垂直领域划分的目录），另一种是供平台团队在自有工作流引擎后部署的 Claude Managed Agent 模板。**同一个代理、同一套技能——由你选择接入面。**下表中的每个目录都是一个部署清单（deploy manifest），它引用与对应插件一致的“规范系统提示词”和技能文件，因此全仓库保持单一事实来源（single source of truth）。

运行 `../scripts/deploy-managed-agent.sh <slug>` 可上传技能、创建 leaf workers，并用解析后的配置 `POST /v1/agents`。每个模板都带有 [`steering-examples.json`](./pitch-agent/steering-examples.json) 以及对应代理的 README（包含安全分级与 handoff 说明）。

| Agent | Vertical plugin | Cowork tile | CMA steering event | Leaf workers |
|---|---|---|---|---|
| [`pitch-agent`](./pitch-agent/) | investment-banking | 可比公司、可比交易、LBO → 品牌化 pitch deck | `Build pitch book: <target> / <acquirer>, thesis: <text>` | researcher · modeler · **deck-writer** |
| [`market-researcher`](./market-researcher/) | equity-research | 行业/主题 → 概览、格局、同业可比、想法清单 | `Primer: <sector or theme>, angle: <text>` | sector-reader · comps-spreader · **note-writer** |
| [`earnings-reviewer`](./earnings-reviewer/) | equity-research | 电话会 + 披露文件 → 模型更新 → 纪要草稿 | `Process earnings: <ticker> <period>` | transcript-reader · model-updater · **note-writer** |
| [`meeting-prep-agent`](./meeting-prep-agent/) | wealth-management | 每次客户会议前生成简报包 | `Briefing pack for <client-id>, meeting <event-id>` | profiler · news-reader · **pack-writer** |
| [`model-builder`](./model-builder/) | financial-analysis | DCF、LBO、三表、可比——以文件产出 | `Build <dcf\|lbo\|3-stmt> for <ticker>, assumptions: {...}` | data-puller · **builder** · auditor |
| [`gl-reconciler`](./gl-reconciler/) | financial-analysis | 找出差异、追踪根因、提交签字确认 | `Reconcile GL vs subledger, trade date <D>, classes: <list>` | reader · critic · **resolver** |
| [`kyc-screener`](./kyc-screener/) | financial-analysis | 解析准入材料、运行规则、标记缺口 | `Screen onboarding packet <id>` | doc-reader · rules-engine · **escalator** |
| [`valuation-reviewer`](./valuation-reviewer/) | private-equity | 导入 GP 包，运行估值模板，准备 LP 报告 | `Review portco valuations for fund <X> as of <date>` | package-reader · valuation-runner · **publisher** |
| [`month-end-closer`](./month-end-closer/) | financial-analysis | 计提、滚动表、差异说明 | `Close <entity> for period <YYYY-MM>` | ledger-reader · rollforward · **poster** |
| [`statement-auditor`](./statement-auditor/) | private-equity | 在分发前审计 LP 对账单 | `Tie out statement batch <id> against <fund> NAV pack` | statement-reader · reconciler · **flagger** |

**加粗** leaf 表示它是唯一持有 `Write` 的 worker。

## Manifest 与 API 的关系

`agent.yaml` 文件使用真实的 `POST /v1/agents` 字段名，并加入少量部署脚本会解析的约定：

| Manifest 约定 | 解析后对应 |
|---|---|
| `system: {file: ../../plugins/agent-plugins/<slug>/agents/<slug>.md, append: "..."}` | `system: "<内联文件内容 + append>"` |
| `system: {text: "..."}` | `system: "<text>"` |
| `skills: [{from_plugin: ../../plugins/agent-plugins/<slug>}]` | 上传该目录下 `skills/*` → `[{type: custom, skill_id: ...}, ...]` |
| `skills: [{path: ../../...}]` | `skills: [{type: custom, skill_id: <uploaded-id>}]` |
| `callable_agents: [{manifest: ./subagents/x.yaml}]` | `callable_agents: [{type: agent, id: <created-id>, version: latest}]` |

> **研究预览：** `callable_agents`（多代理委派）仅支持**一层委派**。编排器可以调用 worker；worker 不能再调用更深层的子代理。

## 跨代理 handoff

具名代理不会彼此直接调用。当一个代理需要另一个代理时，会在输出中发出 `handoff_request`；[`../scripts/orchestrate.py`](../scripts/orchestrate.py)（或你的 Temporal/Airflow/Guidewire 事件总线）会将其路由为目标会话的新 steering event。参考脚本会对目标做强 allowlist，并对 payload 做 schema 校验——其 threat model 见脚本头部说明。
