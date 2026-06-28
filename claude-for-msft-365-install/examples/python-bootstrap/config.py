"""
Edit this file to configure your bootstrap server. app.py should not need changes.
"""
import base64
import os

# ─── Config ──────────────────────────────────────────────────────────
TENANT_ID = os.environ["TENANT_ID"]                         # your Entra tenant
AUDIENCE  = "c2995f31-11e7-4882-b7a7-ef9def0a0266"          # Claude in Office add-in app ID
ISSUER    = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
JWKS_URL  = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
HOST      = os.getenv("HOST", "127.0.0.1")
PORT      = int(os.getenv("PORT", "8080"))

# Local-dev override: point at a self-issued JWKS instead of Entra.
# Signature verification still runs. Refuses to start on non-loopback.
DEV_JWKS_PATH = os.getenv("DEV_JWKS_PATH")
if DEV_JWKS_PATH and HOST != "127.0.0.1":
    raise SystemExit("DEV_JWKS_PATH may only be used when HOST=127.0.0.1")

# ─── Catalog: every skill / MCP server you might hand out ────────────
def b64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()

SKILLS = {
    "deal-memo": {
        "description": "Draft a deal memo from a term sheet",
        "url": "https://your-bucket.s3.amazonaws.com/skills/deal-memo.zip?X-Amz-Signature=...",
    },
    "compliance-check": {
        "description": "Review a document for compliance issues",
        "content": b64("# Compliance check\n\nReview the document for regulatory red flags..."),
    },
    "risk-dashboard": {
        "description": "Summarize positions from the risk dashboard",
        "url": "https://your-bucket.s3.amazonaws.com/skills/risk.zip?X-Amz-Signature=...",
    },
}

MCP_SERVERS = {
    "linear": {"url": "https://mcp.linear.app/sse", "label": "Linear"},
    "risk-api": {
        "url": "https://internal.example.com/mcp/risk",
        "label": "Risk Dashboard",
        "headers": {"Authorization": "Bearer {{gateway_token}}"},
    },
}

# ─── RBAC: first matching rule wins ──────────────────────────────────
# `when` conditions (all must match):
#   group — value from the Entra token's `groups` claim
#   user  — Entra user `oid`
#   app   — Office host: "word" | "excel" | "powerpoint"
# In production, group/user values are GUIDs — replace the names below
# with real Object IDs from Entra admin center.
RULES = [
    {"when": {"app": "word", "group": "investment-banking"},
     "skills": ["deal-memo", "compliance-check"], "mcp_servers": ["linear"]},

    {"when": {"group": "risk"},
     "skills": ["risk-dashboard", "compliance-check"], "mcp_servers": ["risk-api"]},

    {"when": {"user": "alice"},
     "skills": ["deal-memo"], "mcp_servers": []},

    {"when": {}, "skills": ["compliance-check"], "mcp_servers": []},  # default
]
