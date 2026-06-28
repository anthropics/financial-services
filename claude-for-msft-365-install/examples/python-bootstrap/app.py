"""
Claude in Office — Bootstrap endpoint reference implementation.

The Office add-in calls GET /bootstrap with the user's Entra ID token.
This server validates the token, decides which skills and MCP servers
that employee is allowed to use, and returns them.

All customer-editable settings live in config.py — edit that, not this file.
"""
import re
import time

import jwt  # PyJWT
from config import (
    AUDIENCE,
    DEV_JWKS_PATH,
    HOST,
    ISSUER,
    JWKS_URL,
    MCP_SERVERS,
    PORT,
    RULES,
    SKILLS,
)
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from jwt import PyJWKClient

_UA_RE = re.compile(r"^claude-(word|excel|powerpoint)/", re.I)

def parse_app(user_agent: str | None) -> str:
    m = _UA_RE.match(user_agent or "")
    return m.group(1).lower() if m else ""

def resolve(oid: str, groups: set[str], app: str) -> dict:
    for r in RULES:
        w = r["when"]
        if "user" in w and w["user"] != oid:
            continue
        if "group" in w and w["group"] not in groups:
            continue
        if "app" in w and w["app"] != app:
            continue
        return {
            "skills":      [{"name": n, **SKILLS[n]} for n in r.get("skills", [])],
            "mcp_servers": [MCP_SERVERS[n] for n in r.get("mcp_servers", [])],
        }
    return {"skills": [], "mcp_servers": []}

# ─── Token validation ────────────────────────────────────────────────
_jwks = PyJWKClient(JWKS_URL) if not DEV_JWKS_PATH else None

def validate(auth_header: str) -> dict:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = auth_header.removeprefix("Bearer ").strip()
    if DEV_JWKS_PATH:
        import json
        with open(DEV_JWKS_PATH) as f:
            key = jwt.PyJWK(json.load(f)["keys"][0]).key
    else:
        key = _jwks.get_signing_key_from_jwt(token).key
    try:
        return jwt.decode(token, key, algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
    except jwt.InvalidTokenError as e:
        raise HTTPException(401, f"Invalid token: {e}")

# ─── HTTP ────────────────────────────────────────────────────────────
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pivot.claude.ai"],
    allow_methods=["GET"],
    allow_headers=["*"],  # FastAPI reflects the preflight's requested headers
)

@app.get("/bootstrap")
def bootstrap(
    authorization: str = Header(None),
    x_claude_user_agent: str = Header(None),
):
    claims = validate(authorization)
    oid = claims.get("oid", "")
    # NOTE: We assume group membership arrives in the token's `groups` claim.
    # If your tenant doesn't emit it (or you prefer your own RBAC), replace
    # this line with a lookup against your IdP / HRIS — e.g.
    #   groups = fetch_groups_from_graph(oid)  or  your_iam.groups_for(email)
    groups = set(claims.get("groups", []))
    config = resolve(oid, groups, parse_app(x_claude_user_agent))
    return {**config, "bootstrap_expires_at": int(time.time()) + 3600}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
