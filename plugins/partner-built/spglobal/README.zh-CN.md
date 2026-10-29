# S&P Global 插件

本插件通过一组预置技能，将 S&P Global 的金融数据与分析能力直接带入你的 AI 工作流。它面向希望基于权威 S&P Global 数据进行 AI 辅助研究、分析与文档生成的金融从业者。

这些技能构建在开放标准（MCP）之上，能够跨 AI 平台与 agent 框架工作。尽管本插件遵循 Claude Cowork 标准，但所有技能以及底层数据层均与平台无关。如果你希望在其它环境中使用这些技能，欢迎这样做。

我们理解每家机构都有独特需求。这里的技能是帮助你起步的起点，你可以根据本机构的流程、模板与数据需求，调整提示词、输出与工作流。

本插件内技能按“现状”提供。生成的输出与数据不保证正确。**请始终对 LLM 生成的结果进行校验。**

## 包含的技能

### Tearsheets
**需要**：订阅 [S&P Global LLM-ready API](https://www.marketplace.spglobal.com/en/solutions/kensho-llm-ready-api-%28a156fe9f-5564-4f60-a624-95d8645dc98f%29)

生成一到两页格式化的公司 tearsheet（Word 文档），并使用 S&P Capital IQ 的实时数据填充。支持四种受众类型，每种针对不同场景优化：
* 股票研究：为买方/卖方分析师生成投资主线快照
* 投资银行 / 并购：在交易语境下的公司 profile
* 企业发展（Corp Dev）：面向内部战略团队的收购标的 profile
* 销售 / 商务拓展：面向商业团队的客户会议准备

**示例提示词**："Generate a business development tearsheet for Palantir."

### 行业交易摘要（Industry Transaction Summaries）
**需要**：订阅 [S&P Global LLM-ready API](https://www.marketplace.spglobal.com/en/solutions/kensho-llm-ready-api-%28a156fe9f-5564-4f60-a624-95d8645dc98f%29)

基于 S&P Capital IQ 交易数据，总结某个行业（或某家公司）近期并购与交易活动。适用于市场映射、pitch 准备与竞争情报。

**示例提示词**："Summarize recent transactions in the data infrastructure space”

### 财报预览（Earnings Previews）
**需要**：订阅 [S&P Global LLM-ready API](https://www.marketplace.spglobal.com/en/solutions/kensho-llm-ready-api-%28a156fe9f-5564-4f60-a624-95d8645dc98f%29)

为即将发布的财报生成结构化预览，包括一致预期、近期指引、分析师情绪与关注要点——全部来源于 S&P Capital IQ。

**示例提示词**："Give me an earnings preview for Salesforce."

## 使用方式

插件与技能需要访问 S&P Global 数据方可工作，可使用 [Capital IQ Pro](https://www.spglobal.com/market-intelligence/en/solutions/products/sp-capital-iq-pro) 或订阅 [S&P Global LLM-ready API](https://www.marketplace.spglobal.com/en/solutions/kensho-llm-ready-api-%28a156fe9f-5564-4f60-a624-95d8645dc98f%29)。

LLM-ready API 可以通过其 MCP server 轻松集成到 Claude 或其它应用中。请按照 [这些步骤](docs.kensho.com/llmreadyapi/mcp/third-party/claude) 进行设置。

### 在 Cowork 中
你需要付费的 Claude 计划（Pro、Max、Team 或 Enterprise）以及 macOS 或 Windows 的 Claude Desktop 应用。

1. 打开 Claude Desktop 并进入 **Cowork** 标签页
1. 点击 **Customize with Plugins**
1. 在 Browse Plugins 中选择 **Personal**
1. 点击 **加号 “+”** 添加插件
1. 按提示使用你的 S&P Global 凭据完成认证

安装后，相关场景下技能会自动激活——用自然语言描述你的需求即可。你也可以在聊天里输入 `/` 查看可用命令并显式调用特定技能。

要将插件定制为适配你机构的工作流、模板或术语，请在已安装插件界面点击 **Customize**。我们鼓励你这样做；默认配置只是起点，而非标准答案。

### 在 Claude Desktop 中（单独安装技能）
如果你想在 Claude Desktop 中只安装单独技能，而不安装整个插件：

1. 打开 **Settings**
1. 进入 **Capabilities → Skills**
1. 点击 **Add**
1. 上传本仓库中的 skill 文件

上传后技能会立即可用。你可以按需安装一个或多个。

### 在 Claude Code 中（单独安装技能）

请参考 [Claude Code 文档](https://code.claude.com/docs/en/discover-plugins#add-from-github)。

### 其它平台
本仓库中的技能是 Markdown 文件。任何支持自定义指令、系统提示词或知识文件上传的 AI 平台都可以使用它们——具体机制随平台而异，但原则相同：将 skill 内容加载为持久上下文。

**ChatGPT**：把 skill 内容粘贴到自定义指令（Settings → Customize ChatGPT），作为 Project 的知识文件上传，或加入自定义 GPT 的配置。自定义指令对所有会话全局生效；Project 级文件将上下文限制在特定工作流内。

**Microsoft Copilot**：根据你的 Copilot 配置（M365 Copilot、Copilot Studio 等），将 skill 内容粘贴到自定义提示词或系统指令中。通过 Copilot Studio 的企业部署通常支持直接上传知识源。

**其它平台**：如果平台支持系统提示词或持久指令层，将 skill Markdown 粘贴到该处；如果支持文件式知识检索，则上传 skill 文件。技能是纯 Markdown，不需要任何特殊格式或工具。

## 后续计划

我们正在持续构建更多覆盖金融工作流的技能与插件。欢迎告诉我们你最希望看到什么能力！如有一般问题、反馈或合作咨询，请联系 [commercial@kensho.com](mailto:commercial@kensho.com) 或在本仓库中提 issue。

# 许可证

Licensed under the Apache 2.0 License. Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Copyright 2026-present Kensho Technologies, LLC. The present date is determined by the timestamp of the most recent commit in the repository.
