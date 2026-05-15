# LSEG 金融分析插件

使用 LSEG 金融数据与分析能力对债券定价、分析收益率曲线、评估 FX carry 交易、期权估值，并构建宏观仪表盘。

## 本插件做什么

本插件将 LSEG 的金融分析 MCP 工具封装为 8 个高层工作流：每个命令会将多个工具调用串联起来，以完成常见金融分析任务。你无需逐个调用底层工具；每个命令会把 4–5 个工具编排成一个连贯的分析流程。

## Commands

| Command | 描述 |
|---------|-------------|
| `/analyze-bond-rv` | 分析债券相对价值：利差拆解与情景压力测试 |
| `/analyze-fx-carry` | 评估 FX carry 机会：现汇、远期、波动率曲面与历史背景 |
| `/research-equity` | 生成股票研究快照：一致预期、基本面与价格表现 |
| `/analyze-swap-curve` | 分析 swap curve：叠加国债与通胀曲线，产出曲线交易想法 |
| `/analyze-option-vol` | 分析期权波动率：波动率曲面、希腊值、隐含 vs 已实现对比 |
| `/review-fi-portfolio` | 审阅固收组合：定价、现金流与情景分析 |
| `/macro-rates` | 构建宏观与利率仪表盘：经济指标、收益率曲线与 swap 利差 |
| `/analyze-bond-basis` | 分析债券期货基差：CTD 识别与 implied repo rate |

## Skills

每个命令都由对应的 skill 支撑，提供深入的领域方法论：

| Skill | 领域知识 |
|-------|-----------------|
| `bond-relative-value` | 利差框架、G-spread/Z-spread/OAS、rich-cheap 分析 |
| `fx-carry-trade` | carry 机制、carry-to-vol 比率、G10 与新兴市场 carry 动态 |
| `equity-research` | IBES 一致预期解读、基本面分析、估值指标 |
| `swap-curve-strategy` | swap curve 构建、曲线交易、实际利率分析 |
| `option-vol-analysis` | 波动率曲面解读、SABR 模型、希腊值、隐含 vs 已实现波动率 |
| `fixed-income-portfolio` | 组合分析、关键期限久期、现金流分析、情景测试 |
| `macro-rates-monitor` | 宏观指标、收益率曲线形态、实际利率、金融条件 |
| `bond-futures-basis` | CTD 机制、基差计算、implied repo、交割期权 |

## Integrations

本插件连接到 **LFA MCP Server**，可访问 LSEG 在以下领域的金融数据与分析能力：

- **债券定价**：债券与债券期货估值
- **外汇定价**：即期与远期汇率
- **曲线**：利率、信用、通胀与 FX 远期曲线
- **掉期**：利率掉期定价
- **期权**：包含全部希腊值的期权估值
- **波动率**：FX 与股票隐含波动率曲面
- **量化分析**：分析师预期、公司基本面、股票价格、宏观数据
- **时间序列**：历史定价摘要
- **YieldBook**：固收参考数据、现金流、情景与风险分析

完整工具清单见 [CONNECTORS.md](CONNECTORS.md)。

## 安装

```
claude plugins add LSEG
```

## 要求

- 具备可用凭据的 LSEG MCP Server 访问权限
- 对应产品的 LSEG 数据授权（entitlements）
