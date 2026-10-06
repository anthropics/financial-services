
# Claude 金融服务解决方案

面向金融服务业工作流（投资银行、股票研究、私募股权和财富管理）的参考智能体、技能和数据连接器。

这里的所有内容都来自同一源码，支持**两种使用方式**：作为 [Claude Cowork](https://claude.com/product/cowork) 插件安装，或通过 [Claude Managed Agents API](https://docs.claude.com/en/api/managed-agents) 部署到你自己的工作流引擎后端。相同的系统提示词，相同的技能——运行位置由你选择。

> [!IMPORTANT]
> 本仓库中的任何内容均不构成投资、法律、税务或会计建议。这些智能体起草的是分析师工作成果——模型、备忘录、研究笔记、对账文件——需由合资格专业人士审核。它们不会做出投资建议、执行交易、承担风险、记账或批准开户；所有输出都需经过人工审批。你有责任验证输出结果，并确保符合适用于你公司的法律法规。

仓库内容概览：

- **[智能体](#agents)** — 具名的端到端工作流智能体（Pitch 智能体、市场研究智能体、总账对账智能体等）。每个智能体既作为 Cowork 插件提供，也提供通过 `/v1/agents` 部署的 [Claude Managed Agent 模板](./managed-agent-cookbooks)。
- **[垂直领域插件](#vertical-plugins)** — 按 FSI 垂直领域打包的底层技能、斜杠命令和数据连接器。如果你只想要 `/comps`、`/dcf`、`/earnings` 和连接器，而不需要完整的智能体，可以单独安装这些插件。

## 智能体

每个智能体以其运行的工作流命名。它们是起点：安装与你工作匹配的智能体，然后根据你公司的具体方式调整提示词、技能和连接器。

每个智能体插件都是**自包含的**——它打包了其使用的技能，所以只需安装智能体即可。

| 功能 | 智能体 | 说明 |
|---|---|---|
| **覆盖与咨询** | **[Pitch 智能体](./plugins/agent-plugins/pitch-agent)** | 可比公司分析、先例案例、LBO → 品牌 pitch deck，端到端 |
| | **[会议准备智能体](./plugins/agent-plugins/meeting-prep-agent)** | 每次客户会议前的简报包 |
| **研究与建模** | **[市场研究智能体](./plugins/agent-plugins/market-researcher)** | 行业或主题 → 行业概览、竞争格局、可比公司、同ideas 候选列表 |
| | **[业绩回顾智能体](./plugins/agent-plugins/earnings-reviewer)** | 财报电话会议 + 文件 → 模型更新 → 笔记草稿 |
| | **[模型构建智能体](./plugins/agent-plugins/model-builder)** | DCF、LBO、三张报表、可比公司分析——实时在 Excel 中 |
| **基金管理与财务运营** | **[估值审核智能体](./plugins/agent-plugins/valuation-reviewer)** | 接收 GP 资料包，运行估值模板，准备 LP 报告 |
| | **[总账对账智能体](./plugins/agent-plugins/gl-reconciler)** | 查找差异，追溯根本原因，提交审批 |
| | **[月末结账智能体](./plugins/agent-plugins/month-end-closer)** | 应计项目、滚动forward、差异说明 |
| | **[报表审计智能体](./plugins/agent-plugins/statement-auditor)** | 发行前审计 LP 报表 |
| **运营与开户** | **[KYC 筛查智能体](./plugins/agent-plugins/kyc-screener)** | 解析开户文件，运行规则引擎，标记缺失项 |

关于 Managed Agent 部署——`agent.yaml`、叶子工作器子智能体、steering 事件示例以及每个智能体的安全说明——请参见 **[managed-agent-cookbooks/](./managed-agent-cookbooks)**。

## 仓库结构

```
plugins/
  agent-plugins/               # 具名智能体——每个插件自包含
  vertical-plugins/            # 按 FSI 垂直领域打包的技能 + 命令，以及 MCP 连接器
  partner-built/               # 合作伙伴编写的插件（LSEG、S&P Global）
managed-agent-cookbooks/       # Claude Managed Agent cookbook——每个智能体一个目录
claude-for-msft-365-install/   # 用于配置 Claude Microsoft 365 插件的管理工具
scripts/                       # deploy-managed-agent.sh · check.py · validate.py · orchestrate.py · sync-agent-skills.py
```

## 快速开始

### Cowork

在 Cowork 中，打开 **Settings → Plugins → Add plugin**，然后：

- **粘贴此仓库 URL** — `https://github.com/anthropics/claude-for-financial-services` — 然后从市场列表中选择你需要的智能体和垂直领域，或
- **上传 zip 文件** — 压缩 `plugins/` 下的任何目录（例如 `plugins/agent-plugins/pitch-agent/`）然后上传。

### Claude Code

```bash
# 添加市场
claude plugin marketplace add anthropics/claude-for-financial-services

# 核心技能 + 连接器（先安装）
claude plugin install financial-analysis@claude-for-financial-services

# 具名智能体——选择你需要的
claude plugin install pitch-agent@claude-for-financial-services
claude plugin install gl-reconciler@claude-for-financial-services
claude plugin install market-researcher@claude-for-financial-services

# 垂直领域技能包
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
```

安装后，智能体会出现在 Cowork 调度中，技能在相关时会自动触发，斜杠命令可在会话中使用（`/comps`、`/dcf`、`/earnings`、`/ic-memo` 等）。

### Claude Managed Agents

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

[`managed-agent-cookbooks/`](./managed-agent-cookbooks) 下的每个模板都引用与其插件对应版本相同的系统提示词和技能。部署脚本解析文件引用、上传技能、创建叶子工作器子智能体，并通过 `/v1/agents` POST 编排器。请参阅 [`scripts/orchestrate.py`](./scripts/orchestrate.py) 中的参考事件循环，该循环通过你自己的编排层在智能体之间路由 `handoff_request` 事件。

> **研究预览：** 子智能体委托（`callable_agents`）是一项预览功能。请参阅各智能体的 README 以了解安全和交接指导。

## 架构说明

| | 是什么 | 位置 |
|---|---|---|
| **智能体** | 自包含的插件，端到端拥有工作流——系统提示词加上其使用的技能。Cowork 和 Managed Agent 包装器都引用同一目录。 | `plugins/agent-plugins/<slug>/` |
| **技能** | Claude 在相关时自动使用的领域专业知识、惯例和逐步方法。在垂直领域插件中编写一次；每个智能体打包其需要的技能副本。 | `plugins/vertical-plugins/<vertical>/skills/`（源）· `plugins/agent-plugins/<slug>/skills/`（打包后） |
| **命令** | 显式触发的斜杠操作（`/comps`、`/earnings`、`/ic-memo`）。 | `plugins/vertical-plugins/<vertical>/commands/` |
| **连接器** | 将 Claude 连接到你的数据的 [MCP 服务器](https://modelcontextprotocol.io/)——终端、研究平台、文档存储。 | `plugins/vertical-plugins/financial-analysis/.mcp.json` |
| **Managed-agent 包装器** | `agent.yaml` + 深度1子智能体 + 无头部署的 steering 示例。 | `managed-agent-cookbooks/<slug>/` |

一切都是基于文件的——Markdown 和 JSON，无需构建步骤。

## 垂直领域插件

从 **financial-analysis** 开始——它包含共享的建模技能和所有数据连接器。根据需要添加垂直领域插件。

| 插件 | 功能 |
|---|---|
| **[financial-analysis](./plugins/vertical-plugins/financial-analysis)** *(核心)* | 可比公司分析、DCF、LBO、三张报表、deck QC、Excel 审计。全部 11 个数据连接器。 |
| **[investment-banking](./plugins/vertical-plugins/investment-banking)** | CIM、teaser、流程函件、买家名单、合并模型、交易跟踪。 |
| **[equity-research](./plugins/vertical-plugins/equity-research)** | 业绩笔记、首发覆盖、模型更新、thesis 和催化剂跟踪。 |
| **[private-equity](./plugins/vertical-plugins/private-equity)** | 项目来源、筛选、尽职调查清单、IC 备忘录、投资组合监控。 |
| **[wealth-management](./plugins/vertical-plugins/wealth-management)** | 客户回顾、财务计划、再平衡、报告、TLH。 |
| **[fund-admin](./plugins/vertical-plugins/fund-admin)** | 总账对账、差异追溯、应计项目、滚动forward、差异说明、NAV 核对。 |
| **[operations](./plugins/vertical-plugins/operations)** | KYC 文档解析和规则网格评估。 |
| **[lseg](./plugins/partner-built/lseg)** *(合作伙伴)* | 基于 LSEG 数据的债券 RV、互换曲线、FX carry、期权波动率、宏观利率监控。 |
| **[sp-global](./plugins/partner-built/spglobal)** *(合作伙伴)* | 基于 S&P Capital IQ 的摘要表、业绩预览、资金摘要。 |

## MCP 集成

所有连接器集中在 **financial-analysis** 核心插件中，并在其他插件间共享。

| 提供商 | URL |
|---|---|
| [Daloopa](https://www.daloopa.com/) | `https://mcp.daloopa.com/server/mcp` |
| [Morningstar](https://www.morningstar.com/) | `https://mcp.morningstar.com/mcp` |
| [S&P Global](https://www.spglobal.com/) | `https://kfinance.kensho.com/integrations/mcp` |
| [FactSet](https://www.factset.com/) | `https://mcp.factset.com/mcp` |
| [Moody's](https://www.moodys.com/) | `https://api.moodys.com/genai-ready-data/m1/mcp` |
| [MT Newswires](https://www.mtnewswires.com/) | `https://vast-mcp.blueskyapi.com/mtnewswires` |
| [Aiera](https://www.aiera.com/) | `https://mcp-pub.aiera.com` |
| [LSEG](https://www.lseg.com/) | `https://api.analytics.lseg.com/lfa/mcp` |
| [PitchBook](https://pitchbook.com/) | `https://premium.mcp.pitchbook.com/mcp` |
| [Chronograph](https://www.chronograph.pe/) | `https://ai.chronograph.pe/mcp` |
| [Egnyte](https://www.egnyte.com/) | `https://mcp-server.egnyte.com/mcp` |

> 访问 MCP 可能需要提供商订阅或 API 密钥。

## Claude for Microsoft 365 — 安装工具

如果你的公司通过 Microsoft 365 插件在 Excel、PowerPoint、Word 和 Outlook 中运行 Claude，[`claude-for-msft-365-install/`](./claude-for-msft-365-install) 是供 IT 管理员使用的配置工具，可将其配置为针对**你自己的云**——Vertex AI、Bedrock 或内部 LLM 网关——而不是 Anthropic 的 API。

这是一个 Claude Code 插件（非 Cowork 插件），引导 IT 管理员生成定制的插件清单、授予 Azure 管理员同意，以及通过 Microsoft Graph 编写每个用户的路由配置。安装方式：

```bash
claude plugin install claude-for-msft-365-install@claude-for-financial-services
/claude-for-msft-365-install:setup
```

这与上面的智能体和垂直领域插件是分开的——它是让插件在租户中部署的入口，之后智能体和技能将在其中运行。

## 定制化

这些都是参考模板——根据你公司的工作方式进行调整会变得更好。

- **更换连接器** — 将 `.mcp.json` 指向你的数据提供商和内部系统。
- **添加公司上下文** — 将你的术语、流程和格式标准添加到技能文件中。
- **使用你的模板** — `/ppt-template` 教 Claude 你的品牌 PowerPoint 布局。
- **调整智能体范围** — 编辑 `agents/<slug>.md` 以匹配你团队实际运行工作流的方式。
- **添加你自己的** — 复制我们尚未覆盖的工作流结构。

## 技能与命令参考

<details>
<summary><b>financial-analysis</b> — 核心建模、Excel、deck QC</summary>

| 技能 | 命令 | 说明 |
|---|---|---|
| comps-analysis | `/comps` | 使用交易倍数的可比公司分析 |
| dcf-model | `/dcf` | 带 WACC 和敏感性分析的 DCF 估值 |
| lbo-model | `/lbo` | 杠杆收购模型 |
| 3-statement-model | `/3-statement-model` | 填充三张报表财务模型模板 |
| audit-xls | `/debug-model` | Excel 模型审计——公式追踪、硬编码检测、平衡检查 |
| clean-data-xls | — | 规范化和清理 Excel 中的表格数据 |
| deck-refresh | — | 重新链接和刷新整个 deck 中的嵌入式图表/表格 |
| competitive-analysis | `/competitive-analysis` | 竞争格局和市场定位 |
| ib-check-deck | — | 演示文稿 QC——检查错误和一致性 |
| pptx-author | — | 无头生成 `.pptx` 文件（Managed Agent 模式） |
| xlsx-author | — | 无头生成 `.xlsx` 文件（Managed Agent 模式） |
| ppt-template-creator | `/ppt-template` | 创建可复用的 PPT 模板技能 |
| skill-creator | — | 创建新技能的指南 |

</details>

<details>
<summary><b>investment-banking</b> — 交易材料与执行</summary>

| 技能 | 命令 | 说明 |
|---|---|---|
| strip-profile | `/one-pager` | Pitch book 的一页公司概况 |
| pitch-deck | — | 用数据填充 pitch deck 模板 |
| datapack-builder | — | 从 CIM 和文件中构建数据包 |
| cim-builder | `/cim` | 起草保密信息备忘录 |
| teaser | `/teaser` | 匿名一页公司 teaser |
| buyer-list | `/buyer-list` | 战略和金融买家范围 |
| merger-model | `/merger-model` | 增厚/稀释 M&A 分析 |
| process-letter | `/process-letter` | 投标指令和流程信函 |
| deal-tracker | `/deal-tracker` | 跟踪进行中的交易、里程碑和待办事项 |

</details>

<details>
<summary><b>equity-research</b> — 覆盖与发布</summary>

| 技能 | 命令 | 说明 |
|---|---|---|
| earnings-analysis | `/earnings` | 业绩后季度更新报告 |
| earnings-preview | `/earnings-preview` | 业绩前情景分析和关键指标 |
| initiating-coverage | `/initiate` | 机构级首发覆盖报告 |
| model-update | `/model-update` | 用新数据更新财务模型 |
| morning-note | `/morning-note` | 晨会笔记和交易想法 |
| sector-overview | `/sector` | 行业格局和主题报告 |
| thesis-tracker | `/thesis` | 维护和更新投资 thesis |
| catalyst-calendar | `/catalysts` | 跟踪覆盖范围内的即将到来的催化剂 |
| idea-generation | `/screen` | 股票筛选和想法来源 |

</details>

<details>
<summary><b>private-equity</b> — 从项目来源到投资组合运营</summary>

| 技能 | 命令 | 说明 |
|---|---|---|
| deal-sourcing | `/source` | 发现公司、检查 CRM、起草创始人联系 |
| deal-screening | `/screen-deal` | 对收到的 CIM 和 teaser 快速做出通过/不通过决定 |
| dd-checklist | `/dd-checklist` | 按工作流分类的尽职调查清单 |
| dd-meeting-prep | `/dd-prep` | 为管理层演示和专家电话做准备 |
| unit-economics | `/unit-economics` | ARR 队列、LTV/CAC、净留存率、收入质量 |
| returns-analysis | `/returns` | IRR/MOIC 敏感性表 |
| ic-memo | `/ic-memo` | 投资委员会备忘录起草 |
| portfolio-monitoring | `/portfolio` | 跟踪投资组合公司 KPI 和差异 |
| value-creation-plan | `/value-creation` | 交割后 100 天计划和 EBITDA 桥接 |
| ai-readiness | `/ai-readiness` | 评估投资组合公司的 AI 准备情况 |

</details>

<details>
<summary><b>wealth-management</b> — 顾问工作流</summary>

| 技能 | 命令 | 说明 |
|---|---|---|
| client-review | `/client-review` | 为客户会议准备业绩和要点 |
| financial-plan | `/financial-plan` | 退休、教育、遗产和现金流预测 |
| portfolio-rebalance | `/rebalance` | 配置漂移分析和税收敏感型再平衡 |
| client-report | `/client-report` | 面向客户的业绩报告 |
| investment-proposal | `/proposal` | 为潜在客户准备的提案 |
| tax-loss-harvesting | `/tlh` | 识别 TLH 机会并管理洗售交易 |

</details>

## 贡献

一切都是 Markdown 和 YAML。欢迎 Fork、编辑、PR。对于新内容：

- 新技能 → 添加到 `plugins/vertical-plugins/<vertical>/skills/`，然后运行 `python3 scripts/sync-agent-skills.py` 同步到打包该技能的任何智能体。
- 新智能体 → `plugins/agent-plugins/<slug>/`（包含 `agents/<slug>.md` + `skills/`）以及对应的 `managed-agent-cookbooks/<slug>/`。
- 推送前运行 `python3 scripts/check.py`——它会检查每个清单、验证所有跨文件引用，并检测任何打包技能是否偏离了垂直领域源文件。

## 许可证

[Apache License 2.0](./LICENSE)