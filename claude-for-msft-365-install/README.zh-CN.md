# Claude for Office — 直连自有云的配置工具

用于配置 Claude Office 加载项的管理员工具，使其调用你自己的云端服务
（Vertex AI、Bedrock 或 LLM gateway），而不是 Anthropic 的 API。

## 安装

```bash
claude plugin marketplace add anthropics/financial-services-plugins
claude plugin install claude-for-msft-365-install@financial-services-plugins
```

然后在会话中运行：`/claude-for-msft-365-install:setup`

## Commands

| Command | 功能 |
|---|---|
| `/claude-for-msft-365-install:setup` | 交互式向导：创建云资源、完成管理员同意、写入 manifest |
| `/claude-for-msft-365-install:manifest` | 生成定制化加载项 manifest XML |
| `/claude-for-msft-365-install:consent` | 生成加载项应用注册所需的 Azure 管理员同意 URL |
| `/claude-for-msft-365-install:update-user-attrs` | 通过 Microsoft Graph extension attributes 写入按用户配置 |
| `/claude-for-msft-365-install:bootstrap` | 构建 bootstrap endpoint：按用户下发 MCP servers、skills 与动态配置 |
