#!/usr/bin/env python3
"""
Print your Entra (Azure AD) tenant ID.

Usage:
    python get_tenant_id.py alice@yourcompany.com
    python get_tenant_id.py yourcompany.com
    python get_tenant_id.py            # tries `az account show` if Azure CLI is logged in

Set the result as TENANT_ID before running app.py.
"""
import json
import subprocess
import sys
import urllib.request


def from_domain(domain: str) -> str:
    # Entra publishes per-tenant OIDC metadata at this well-known URL.
    # The `issuer` field is https://login.microsoftonline.com/<tenant_id>/v2.0
    url = f"https://login.microsoftonline.com/{domain}/v2.0/.well-known/openid-configuration"
    with urllib.request.urlopen(url, timeout=5) as r:
        issuer = json.load(r)["issuer"]
    return issuer.rstrip("/").split("/")[-2]


def from_az_cli() -> str:
    out = subprocess.run(
        ["az", "account", "show", "--query", "tenantId", "-o", "tsv"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        domain = arg.split("@", 1)[1] if "@" in arg else arg
        print(from_domain(domain))
    else:
        try:
            print(from_az_cli())
        except Exception as e:
            sys.exit(f"Pass an email/domain, or run `az login` first ({e})")
