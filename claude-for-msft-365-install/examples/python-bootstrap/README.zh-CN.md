# Bootstrap endpoint — Python 参考实现

一个最小化的 FastAPI 实现，用于 Claude in Office 的 `/bootstrap` endpoint。
它会校验调用方的 Entra ID token，并基于一个简单的“首条匹配”RBAC 表，为每位员工返回对应的 `skills` 与 `mcp_servers`。

## 连接到你的真实 Entra 租户运行

```bash
pip install -r requirements.txt
# 查找你的 tenant ID：
python get_tenant_id.py you@yourcompany.com
export TENANT_ID=<your-tenant-guid>
python app.py
```

## 使用假 token 本地运行

```bash
pip install -r requirements.txt
export TENANT_ID=dev-tenant
TOKEN=$(python mint_dev_token.py --oid alice --group investment-banking)
DEV_JWKS_PATH=dev_jwks.json python app.py &
curl -H "Authorization: Bearer $TOKEN" \
     -H "X-Claude-User-Agent: claude-word/1.0.0" \
     http://127.0.0.1:8080/bootstrap
```

## 定制方式

你需要修改的内容都在 **`config.py`** ——通常无需编辑 `app.py`。

- 编辑 `SKILLS` 与 `MCP_SERVERS`：你可下发的完整目录（catalog）。
- 编辑 `RULES`：按“首条匹配即生效”的规则；底部空的 `when: {}` 是默认兜底。
- 将 `RULES` 中的占位 group/user 名替换为你真实的 Entra Object IDs（GUIDs）。
- token 的 `groups` claim 用于读取群组成员关系。如果你的租户不下发它，把 `app.py` 里 `groups = ...` 的逻辑替换为对内部目录的查询。
- 规则可按 Office host 限定：`"app": "word" | "excel" | "powerpoint"`，来源于加载项发送的 `X-Claude-User-Agent` header。
- Entra token 默认**不包含** `groups` claim。请在应用注册中启用：*App registration → Token configuration → Add groups claim*。
- 将内存中的 `RULES` 替换为你真实的事实来源（DB、配置服务等）。

## 安全

`DEV_JWKS_PATH` 允许服务端信任自签名密钥，而不是 Microsoft 的签名密钥。服务只会在绑定到 `127.0.0.1` 时允许启用该选项。**不要**在部署环境中设置它。
