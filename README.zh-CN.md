# 面向金融服务的 Claude

面向我们最常见金融服务工作流（投行、股票研究、私募股权与财富管理）的参考代理、技能与数据连接器。

这里的所有内容都以**同一套源文件提供两种使用方式**：你可以把它安装为 [Claude Cowork](https://claude.com/product/cowork) 插件，或通过 [Claude Managed Agents API](https://docs.claude.com/en/api/managed-agents) 在你自己的工作流引擎后端进行部署。系统提示词相同、技能相同——由你决定运行位置。

> [!IMPORTANT]
> 本仓库中的任何内容均不构成投资、法律、税务或会计建议。这些代理会起草分析师工作产出（模型、备忘录、研究笔记、对账结果等），供具备资质的专业人士审核。它们不会给出投资建议、执行交易、承担风险、记账入账或批准准入；所有输出都需要人工签字确认。你需要自行验证输出并确保遵守适用于贵机构的法律与监管要求。

仓库内容概览：

- **[Agents](#agents)** —— 具名的端到端工作流代理（Pitch Agent、Market Researcher、GL Reconciler 等）。每个代理同时以 Cowork 插件形式发布，且提供对应的 [Claude Managed Agent 模板](./managed-agent-cookbooks)，供你通过 `/v1/agents` 部署。
- **[Vertical plugins](#vertical-plugins)** —— 按金融垂直领域打包的底层技能、斜杠命令与数据连接器。如果你只想使用 `/comps`、`/dcf`、`/earnings` 以及连接器，而不需要完整代理，可以只安装这些垂直插件。

## Agents

每个代理以它所运行的工作流命名。它们是起点：先安装与你的工作相关的代理，再根据你所在机构的流程调整提示词、技能与连接器。

每个代理插件都是**自包含**的——它会打包自己使用到的技能，因此安装代理本身就足够。

| 职能 | 代理 | 功能 |
|---|---|---|
| **研究覆盖与投顾** | **[Pitch Agent](./plugins/agent-plugins/pitch-agent)** | 可比公司、可比交易、LBO → 品牌化 pitch deck，全流程端到端 |
|  | **[Meeting Prep Agent](./plugins/agent-plugins/meeting-prep-agent)** | 每次客户会议前生成简报包 |
| **研究与建模** | **[Market Researcher](./plugins/agent-plugins/market-researcher)** | 行业/主题 → 行业概览、竞争格局、同业可比、想法清单 |
|  | **[Earnings Reviewer](./plugins/agent-plugins/earnings-reviewer)** | 电话会 + 披露文件 → 更新模型 → 起草纪要 |
|  | **[Model Builder](./plugins/agent-plugins/model-builder)** | DCF、LBO、三表、可比——直接生成 Excel 文件 |
| **基金后台与财务运营** | **[Valuation Reviewer](./plugins/agent-plugins/valuation-reviewer)** | 导入 GP 包，运行估值模板，准备 LP 报告 |
|  | **[GL Reconciler](./plugins/agent-plugins/gl-reconciler)** | 找出差异、追踪根因、提交签字确认 |
|  | **[Month-End Closer](./plugins/agent-plugins/month-end-closer)** | 计提、滚动表、差异说明 |
|  | **[Statement Auditor](./plugins/agent-plugins/statement-auditor)** | 在分发前审计 LP 对账单 |
| **运营与准入** | **[KYC Screener](./plugins/agent-plugins/kyc-screener)** | 解析准入材料，运行规则引擎，标记缺口 |

如需 Managed Agent 部署用的 `agent.yaml`、叶子子代理（leaf-worker）、steering event 示例以及每个代理的安全说明，请查看 **[managed-agent-cookbooks/](./managed-agent-cookbooks)**。

## 仓库结构

```text
plugins/
  agent-plugins/               # 具名代理 — 每个目录是一个自包含插件
  vertical-plugins/            # 按金融垂直领域打包的技能 + 命令 + MCP 连接器
  partner-built/               # 合作伙伴编写的插件（LSEG、S&P Global）
managed-agent-cookbooks/       # Claude Managed Agent 配方 — 每个代理一个目录
claude-for-msft-365-install/   # 用于配置 Claude Microsoft 365 加载项的管理员工具
scripts/                       # deploy-managed-agent.sh · check.py · validate.py · orchestrate.py · sync-agent-skills.py
```

## 快速开始

### Cowork

在 Cowork 中，打开 **Settings → Plugins → Add plugin**，然后选择其一：

- **粘贴本仓库 URL**：`https://github.com/anthropics/claude-for-financial-services`，随后从市场列表中选择你想要的代理与垂直插件，或
- **上传 zip**：将 `plugins/` 下任一目录（例如 `plugins/agent-plugins/pitch-agent/`）打包成 zip 并上传。

### Claude Code

```bash
# 添加 marketplace
claude plugin marketplace add anthropics/claude-for-financial-services

# 核心技能 + 连接器（建议先装）
claude plugin install financial-analysis@claude-for-financial-services

# 具名代理 — 按需选择
claude plugin install pitch-agent@claude-for-financial-services
claude plugin install gl-reconciler@claude-for-financial-services
claude plugin install market-researcher@claude-for-financial-services

# 垂直领域技能包
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
```

安装后，代理会出现在 Cowork 的分发界面；当相关时技能会自动触发；斜杠命令可在会话中使用（`/comps`、`/dcf`、`/earnings`、`/ic-memo` 等）。

### Claude Managed Agents

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

[`managed-agent-cookbooks/`](./managed-agent-cookbooks) 下的每个模板都会引用与其插件版本一致的系统提示词与技能。部署脚本会解析文件引用、上传技能、创建 leaf-worker 子代理，并将编排器（orchestrator）POST 到 `/v1/agents`。可参考 [`scripts/orchestrate.py`](./scripts/orchestrate.py) 中的事件循环示例，它展示了如何通过你自己的编排层在代理之间路由 `handoff_request` 事件。

> **研究预览：** 子代理委派（`callable_agents`）是预览能力。安全与交接建议见各代理 README。

## 它们如何协同工作

| | 定义 | 所在位置 |
|---|---|---|
| **Agents** | 端到端工作流的自包含插件——系统提示词 + 它所使用的技能。Cowork 与 Managed Agent 外壳都引用同一目录。 | `plugins/agent-plugins/<slug>/` |
| **Skills** | Claude 在相关时会自动调用的领域知识、约定与分步方法。技能在垂直插件中只写一次；每个代理会同步一份自己需要的技能。 | `plugins/vertical-plugins/<vertical>/skills/`（源）· `plugins/agent-plugins/<slug>/skills/`（打包） |
| **Commands** | 你显式触发的斜杠动作（`/comps`、`/earnings`、`/ic-memo`）。 | `plugins/vertical-plugins/<vertical>/commands/` |
| **Connectors** | 将 Claude 连接到你的数据（终端、研究平台、文档库等）的 [MCP servers](https://modelcontextprotocol.io/)。 | `plugins/vertical-plugins/financial-analysis/.mcp.json` |
| **Managed-agent wrappers** | 用于无界面部署的 `agent.yaml` + 一级子代理 + steering 示例。 | `managed-agent-cookbooks/<slug>/` |

所有内容均为文件（Markdown 与 JSON），无需构建步骤。

## Vertical Plugins

建议从 **financial-analysis** 开始——它包含共享建模技能以及所有数据连接器。再按需叠加其它垂直插件。

| 插件 | 增加的能力 |
|---|---|
| **[financial-analysis](./plugins/vertical-plugins/financial-analysis)**（核心） | 可比、DCF、LBO、三表、deck 质检、Excel 审计；全部 11 个数据连接器。 |
| **[investment-banking](./plugins/vertical-plugins/investment-banking)** | CIM、teaser、process letter、buyer list、merger model、deal tracking。 |
| **[equity-research](./plugins/vertical-plugins/equity-research)** | 财报纪要、覆盖启动（initiation）、模型更新、投资主线与催化剂跟踪。 |
| **[private-equity](./plugins/vertical-plugins/private-equity)** | Sourcing、筛选、尽调清单、IC memo、投后监控。 |
| **[wealth-management](./plugins/vertical-plugins/wealth-management)** | 客户回顾、财务规划、再平衡、客户报告、TLH。 |
| **[fund-admin](./plugins/vertical-plugins/fund-admin)** | GL 对账、break tracing、计提、滚动表、差异说明、NAV tie-out。 |
| **[operations](./plugins/vertical-plugins/operations)** | KYC 文档解析与规则网格评估。 |
| **[lseg](./plugins/partner-built/lseg)**（合作伙伴） | 基于 LSEG 数据的债券 RV、swap curve、FX carry、期权波动率、宏观利率监控。 |
| **[sp-global](./plugins/partner-built/spglobal)**（合作伙伴） | 基于 S&P Capital IQ 的 tear sheet、财报预览、融资摘要。 |

## MCP 集成

所有连接器集中在 **financial-analysis** 核心插件中，并在其它插件间共享。

| 提供方 | URL |
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

> MCP 访问可能需要供应商订阅或 API key。

## Claude for Microsoft 365 — 安装工具

如果你的机构通过 Microsoft 365 加载项在 Excel、PowerPoint、Word 与 Outlook 中使用 Claude，那么 [`claude-for-msft-365-install/`](./claude-for-msft-365-install) 提供管理员工具，用于将其配置为调用**你自己的云**（Vertex AI、Bedrock 或内部 LLM gateway），而不是 Anthropic 的 API。

它是一个 Claude Code 插件（不是 Cowork 插件），会引导 IT 管理员生成定制的加载项清单、获取 Azure 管理员同意，并通过 Microsoft Graph 写入按用户的路由配置。安装方式：

```bash
claude plugin install claude-for-msft-365-install@claude-for-financial-services
/claude-for-msft-365-install:setup
```

这与上面的代理与垂直插件是分开的——它负责把加载项部署到租户中；部署完成后，运行在其中的才是本仓库的代理与技能。

## 个性化定制

这些是参考模板——当你按自身工作方式调优后会更强。

- **替换连接器**：把 `.mcp.json` 指向你的数据供应商与内部系统。
- **补充机构上下文**：将你的术语、流程、格式标准写入 skill 文件。
- **引入你的模板**：`/ppt-template` 可以教 Claude 学会你品牌化的 PowerPoint 版式。
- **调整代理边界**：编辑 `agents/<slug>.md` 以匹配团队真实工作流。
- **新增内容**：复制现有结构，覆盖仓库未包含的工作流。

## Skill & Command 参考

<details>
<summary><b>financial-analysis</b> — 核心建模、Excel、deck 质检</summary>

| Skill | Command | 描述 |
|---|---|---|
| comps-analysis | `/comps` | 可比公司分析（交易倍数） |
| dcf-model | `/dcf` | DCF 估值（WACC 与敏感性分析） |
| lbo-model | `/lbo` | 杠杆收购（LBO）模型 |
| 3-statement-model | `/3-statement-model` | 填充三表财务模型模板 |
| audit-xls | `/debug-model` | Excel 模型审计：公式追踪、硬编码检测、平衡校验 |
| clean-data-xls | — | 归一化并清洗 Excel 表格数据 |
| deck-refresh | — | 重新链接并刷新 deck 中嵌入的图表/表格 |
| competitive-analysis | `/competitive-analysis` | 竞争格局与市场定位 |
| ib-check-deck | — | 演示文稿错误与一致性质检 |
| pptx-author | — | 无界面生成 `.pptx` 文件（Managed Agent 模式） |
| xlsx-author | — | 无界面生成 `.xlsx` 文件（Managed Agent 模式） |
| ppt-template-creator | `/ppt-template` | 创建可复用的 PPT 模板技能 |
| skill-creator | — | 创建新技能的指南 |

</details>

<details>
<summary><b>investment-banking</b> — 交易材料与执行</summary>

| Skill | Command | 描述 |
|---|---|---|
| strip-profile | `/one-pager` | pitch book 用的一页公司 profile |
| pitch-deck | — | 以数据填充 pitch deck 模板 |
| datapack-builder | — | 从 CIM 与披露文件构建数据包 |
| cim-builder | `/cim` | 起草保密信息备忘录（CIM） |
| teaser | `/teaser` | 匿名的一页 teaser |
| buyer-list | `/buyer-list` | 战略/财务买家清单 |
| merger-model | `/merger-model` | 并购增厚/摊薄分析 |
| process-letter | `/process-letter` | 投标流程信与流程沟通材料 |
| deal-tracker | `/deal-tracker` | 跟踪在途交易与里程碑 |

</details>

<details>
<summary><b>equity-research</b> — 覆盖与发布</summary>

| Skill | Command | 描述 |
|---|---|---|
| earnings-analysis | `/earnings` | 财报后季度更新报告 |
| earnings-preview | `/earnings-preview` | 财报前情景分析与关键指标 |
| initiating-coverage | `/initiate` | 机构级 initiating 报告 |
| model-update | `/model-update` | 基于新数据更新财务模型 |
| morning-note | `/morning-note` | 早会要点与交易想法 |
| sector-overview | `/sector` | 行业格局与主题报告 |
| thesis-tracker | `/thesis` | 维护并更新投资主线 |
| catalyst-calendar | `/catalysts` | 跟踪覆盖标的催化剂 |
| idea-generation | `/screen` | 股票筛选与想法生成 |

</details>

<details>
<summary><b>private-equity</b> — 从 sourcing 到投后运营</summary>

| Skill | Command | 描述 |
|---|---|---|
| deal-sourcing | `/source` | 寻找公司、查 CRM、起草创始人外联 |
| deal-screening | `/screen-deal` | 对入站 CIM/teaser 的快速通过/拒绝 |
| dd-checklist | `/dd-checklist` | 按工作流分解的尽调清单 |
| dd-meeting-prep | `/dd-prep` | 管理层演示与专家访谈准备 |
| unit-economics | `/unit-economics` | ARR cohort、LTV/CAC、净留存、收入质量 |
| returns-analysis | `/returns` | IRR/MOIC 敏感性表 |
| ic-memo | `/ic-memo` | 起草投委会备忘录 |
| portfolio-monitoring | `/portfolio` | 跟踪投后 KPI 与偏差 |
| value-creation-plan | `/value-creation` | 交割后 100 天计划与 EBITDA bridge |
| ai-readiness | `/ai-readiness` | 评估被投公司的 AI readiness |

</details>

<details>
<summary><b>wealth-management</b> — 理财顾问工作流</summary>

| Skill | Command | 描述 |
|---|---|---|
| client-review | `/client-review` | 基于业绩与要点为客户会面做准备 |
| financial-plan | `/financial-plan` | 退休、教育、遗产与现金流预测 |
| portfolio-rebalance | `/rebalance` | 偏离分析与税务友好再平衡 |
| client-report | `/client-report` | 面向客户的业绩报告 |
| investment-proposal | `/proposal` | 面向潜在客户的提案 |
| tax-loss-harvesting | `/tlh` | TLH 机会识别与 wash sale 管理 |

</details>

## 贡献指南

所有内容都是 Markdown 与 YAML。Fork、编辑、提交 PR 即可。新增内容建议：

- 新增 skill：添加到 `plugins/vertical-plugins/<vertical>/skills/`，然后运行 `python3 scripts/sync-agent-skills.py` 同步到会打包它的代理。
- 新增 agent：创建 `plugins/agent-plugins/<slug>/`（含 `agents/<slug>.md` + `skills/`），并同步创建匹配的 `managed-agent-cookbooks/<slug>/`。
- 提交前运行 `python3 scripts/check.py`：它会 lint 所有 manifest，验证跨文件引用是否可解析，并在打包 skill 与其垂直源不一致时失败。

## 许可证

[Apache License 2.0](./LICENSE)
