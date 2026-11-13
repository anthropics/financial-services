"""Tests for bootstrap app and DEV_JWKS_PATH loopback guard."""

import json
import os
import sys
import tempfile
import time
from pathlib import Path
import unittest
from unittest.mock import patch

# Set required environment variables before importing config
os.environ["TENANT_ID"] = "dev-tenant"
BOOTSTRAP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BOOTSTRAP_DIR))

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
import jwt
import app
from app import _is_loopback, app as fastapi_app


def _generate_dev_keys(tmpdir: Path):
    priv_file = tmpdir / "dev_private.pem"
    jwks_file = tmpdir / "dev_jwks.json"

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv_pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    priv_file.write_bytes(priv_pem)

    nums = key.public_key().public_numbers()
    def b64u(n: int) -> str:
        import base64
        raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

    jwk = {
        "kty": "RSA",
        "kid": "dev",
        "alg": "RS256",
        "use": "sig",
        "n": b64u(nums.n),
        "e": b64u(nums.e),
    }
    jwks_file.write_text(json.dumps({"keys": [jwk]}))
    return priv_file, jwks_file, key


class TestLoopbackGuard(unittest.TestCase):
    """Test DEV_JWKS_PATH loopback protection and request handling."""

    def test_is_loopback_helper(self):
        self.assertTrue(_is_loopback("127.0.0.1"))
        self.assertTrue(_is_loopback("127.0.0.2"))
        self.assertTrue(_is_loopback("::1"))
        self.assertTrue(_is_loopback("localhost"))
        self.assertTrue(_is_loopback("testclient"))
        self.assertFalse(_is_loopback("192.168.1.50"))
        self.assertFalse(_is_loopback("10.0.0.1"))
        self.assertFalse(_is_loopback("203.0.113.1"))
        self.assertFalse(_is_loopback(None))
        self.assertFalse(_is_loopback(""))

    def test_dev_jwks_rejects_non_loopback_client(self):
        client = TestClient(fastapi_app, client=("192.168.1.100", 54321))

        with patch.object(app, "DEV_JWKS_PATH", "dev_jwks.json"):
            # Simulate a request from a non-loopback IP address
            response = client.get(
                "/bootstrap",
                headers={"Authorization": "Bearer dummy"},
            )
            self.assertEqual(response.status_code, 403)
            self.assertIn(
                "DEV_JWKS_PATH may only be used from loopback addresses",
                response.json()["detail"],
            )

    def test_dev_jwks_allows_loopback_client(self):
        client = TestClient(fastapi_app, client=("127.0.0.1", 54321))

        with patch.object(app, "DEV_JWKS_PATH", "dev_jwks.json"):
            # Request from loopback (127.0.0.1) should pass the loopback guard
            # and reach token validation (returns 401 for invalid/missing token rather than 403)
            response = client.get(
                "/bootstrap",
                headers={"Authorization": "Bearer invalid_token"},
            )
            self.assertEqual(response.status_code, 401)
            self.assertIn("Invalid token", response.json()["detail"])

    def test_production_mode_permits_external_requests(self):
        client = TestClient(fastapi_app, client=("192.168.1.100", 54321))

        with patch.object(app, "DEV_JWKS_PATH", None):
            # When DEV_JWKS_PATH is not set, external client IPs are not blocked by the loopback guard
            response = client.get(
                "/bootstrap",
                headers={"Authorization": "Bearer invalid_token"},
            )
            # Should reach validate() and return 401, not 403
            self.assertEqual(response.status_code, 401)

    def test_dev_jwks_end_to_end_loopback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            _, jwks_file, key = _generate_dev_keys(tmp_path)

            claims = {
                "aud": app.AUDIENCE,
                "iss": app.ISSUER,
                "oid": "alice",
                "groups": ["investment-banking"],
                "exp": int(time.time()) + 3600,
            }
            token = jwt.encode(claims, key, algorithm="RS256", headers={"kid": "dev"})

            with patch.object(app, "DEV_JWKS_PATH", str(jwks_file)):
                # 1. Non-loopback attempt must fail with 403
                remote_client = TestClient(fastapi_app, client=("192.168.1.50", 12345))
                resp_remote = remote_client.get(
                    "/bootstrap",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "X-Claude-User-Agent": "claude-word/1.0.0",
                    },
                )
                self.assertEqual(resp_remote.status_code, 403)

                # 2. Loopback request succeeds and resolves RBAC
                local_client = TestClient(fastapi_app, client=("127.0.0.1", 12345))
                resp_local = local_client.get(
                    "/bootstrap",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "X-Claude-User-Agent": "claude-word/1.0.0",
                    },
                )
                self.assertEqual(resp_local.status_code, 200)
                data = resp_local.json()
                self.assertIn("skills", data)
                self.assertIn("mcp_servers", data)
                skill_names = [s["name"] for s in data["skills"]]
                self.assertIn("deal-memo", skill_names)
                self.assertIn("compliance-check", skill_names)


if __name__ == "__main__":
    unittest.main()
