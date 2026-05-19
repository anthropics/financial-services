"""
Mint a self-signed dev token for local testing of app.py.

First run generates dev_private.pem + dev_jwks.json in the current directory.
Subsequent runs reuse them.

    python mint_dev_token.py --oid alice --group <gid> --group <gid2>
"""
import argparse, json, os, time, base64
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

PRIV = "dev_private.pem"
JWKS = "dev_jwks.json"
AUDIENCE = "c2995f31-11e7-4882-b7a7-ef9def0a0266"
TENANT_ID = os.getenv("TENANT_ID", "dev-tenant")
ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"

def b64u(n: int) -> str:
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def ensure_dev_key(priv_path: str = PRIV, jwks_path: str = JWKS):
    if os.path.exists(priv_path):
        with open(priv_path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with open(priv_path, "wb") as f:
        f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ))
    nums = key.public_key().public_numbers()
    jwk = {"kty": "RSA", "kid": "dev", "alg": "RS256", "use": "sig",
           "n": b64u(nums.n), "e": b64u(nums.e)}
    with open(jwks_path, "w") as f:
        json.dump({"keys": [jwk]}, f, indent=2)
    return key


def mint_token(oid: str, groups: list[str], priv_path: str = PRIV, jwks_path: str = JWKS) -> str:
    priv = ensure_dev_key(priv_path, jwks_path)
    claims = {"aud": AUDIENCE, "iss": ISSUER, "oid": oid,
              "groups": groups, "exp": int(time.time()) + 3600}
    return jwt.encode(claims, priv, algorithm="RS256", headers={"kid": "dev"})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oid", default="alice")
    ap.add_argument("--group", action="append", default=[])
    args = ap.parse_args()
    print(mint_token(args.oid, args.group))


if __name__ == "__main__":
    main()
