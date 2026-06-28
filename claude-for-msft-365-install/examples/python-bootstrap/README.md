# Bootstrap endpoint — Python reference

A minimal FastAPI implementation of the Claude in Office `/bootstrap` endpoint.
It validates the caller's Entra ID token and returns per-employee `skills` and
`mcp_servers` based on a simple first-match RBAC table.

## Run against your real Entra tenant

```bash
pip install -r requirements.txt
# Find your tenant ID:
python get_tenant_id.py you@yourcompany.com
export TENANT_ID=<your-tenant-guid>
python app.py
```

## Run locally with a fake token

```bash
pip install -r requirements.txt
export TENANT_ID=dev-tenant
TOKEN=$(python mint_dev_token.py --oid alice --group investment-banking)
DEV_JWKS_PATH=dev_jwks.json python app.py &
curl -H "Authorization: Bearer $TOKEN" \
     -H "X-Claude-User-Agent: claude-word/1.0.0" \
     http://127.0.0.1:8080/bootstrap
```

## Customize

Everything you need to change lives in **`config.py`** — `app.py` should not need edits.

- Edit `SKILLS` and `MCP_SERVERS` — the full catalog you can hand out.
- Edit `RULES` — first matching rule wins; the empty `when: {}` at the bottom is the default.
- Replace the placeholder group/user names in `RULES` with your real Entra Object IDs (GUIDs).
- Group membership is read from the token's `groups` claim. If your tenant
  doesn't emit it, swap the `groups = ...` line in `app.py` for a lookup against
  your internal directory.
- Rules can be scoped per Office host with `"app": "word" | "excel" | "powerpoint"`,
  parsed from the `X-Claude-User-Agent` header the add-in sends.
- The `groups` claim is **not** in Entra tokens by default. Enable it under
  *App registration → Token configuration → Add groups claim* for your app.
- Swap the in-memory `RULES` for your real source of truth (DB, config service, etc.).

## Security

`DEV_JWKS_PATH` lets the server trust a self-issued signing key instead of
Microsoft's. It refuses to start unless bound to `127.0.0.1`. **Never** set it
in a deployed environment.
