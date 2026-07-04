"""
BODS UBO Validator — MCP server for Beneficial Ownership Data Standard v0.4.

Provides tools to validate UBO chains against BODS conceptual rules:
  - ubo-validate  : structural validation of a UBO declaration JSON
  - ubo-sample    : return a sample BODS-compliant UBO record

Stdlib-only — no external dependencies beyond the `mcp` package.
"""
import json
import sys
from typing import Any

# MCP server entry
# To run: pip install mcp && python server.py
# Or register with Claude: configure in .mcp.json


def validate_ubo_chain(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate a UBO chain declaration against BODS conceptual rules.
    Input: {applicant: {name, jurisdiction, applicant_type}, beneficial_owners: [...], controllers: [...]}
    Output: validation report with per-check results and opacity score.
    """
    checks = []
    flags = 0
    applicant = data.get("applicant", {})
    owners = data.get("beneficial_owners", [])
    controllers = data.get("controllers", [])

    # ── 1. Total ownership ──────────────────────────────────
    total_pct = sum(o.get("ownership_pct", 0) for o in owners)
    threshold = 10 if applicant.get("applicant_type") == "trust" else 25
    owner_names = [o.get("name", "?") for o in owners]

    if total_pct < threshold and applicant.get("applicant_type") != "public":
        checks.append({
            "check": "total_ownership",
            "result": "flag",
            "detail": f"Total declared = {total_pct}% < {threshold}% threshold for {applicant.get('applicant_type', 'entity')}",
            "evidence": f"UBOs: {', '.join(owner_names)}"
        })
        flags += 1
    else:
        checks.append({"check": "total_ownership", "result": "pass",
                       "detail": f"Sum = {total_pct}%"})

    # ── 2. Circular ownership ───────────────────────────────
    entities_in_chain = {applicant.get("legal_name", "").lower()}
    circular = False
    for o in owners:
        name = o.get("name", "").lower()
        if name in entities_in_chain:
            circular = True
            break
        entities_in_chain.add(name)
    if circular:
        checks.append({"check": "circular_ownership", "result": "flag",
                       "detail": "UBO chain contains a self-reference or cycle"})
        flags += 1
    else:
        checks.append({"check": "circular_ownership", "result": "pass",
                       "detail": "No cycle detected"})

    # ── 3. Control mismatch ─────────────────────────────────
    mismatch = False
    for o in owners:
        pct = o.get("ownership_pct", 0)
        basis = o.get("control_basis", "")
        if basis == "ownership" and pct < 25:
            mismatch = True
        if basis in ("voting", "board_control") and pct > 0:
            mismatch = True
    if mismatch:
        checks.append({"check": "control_mismatch", "result": "flag",
                       "detail": "Control basis conflicts with ownership percentage"})
        flags += 1
    else:
        checks.append({"check": "control_mismatch", "result": "pass"})

    # ── 4. Shell risk ────────────────────────────────────────
    high_risk = ["bvi", "cayman islands", "british virgin islands", "panama",
                 "belize", "seychelles", "marshall islands", "liechtenstein", "cyprus"]
    jurisdiction = applicant.get("nationality_or_jurisdiction", "").lower()
    has_address = bool(applicant.get("registered_address"))
    if jurisdiction in high_risk and not has_address:
        checks.append({"check": "shell_risk", "result": "flag",
                       "detail": f"High-risk jurisdiction ({jurisdiction}) with no registered address"})
        flags += 1
    elif jurisdiction in high_risk:
        checks.append({"check": "shell_risk", "result": "insufficient_data",
                       "detail": f"High-risk jurisdiction ({jurisdiction}) — address listed but not verified"})
    else:
        checks.append({"check": "shell_risk", "result": "pass"})

    # ── 5. PEP intersection ─────────────────────────────────
    pep_declared = data.get("pep_declared", False)
    if pep_declared and not any(o.get("pep_disclosed") for o in owners):
        checks.append({"check": "pep_intersection", "result": "flag",
                       "detail": "Applicant declared PEP but no individual UBO PEP disclosure"})
        flags += 1
    else:
        checks.append({"check": "pep_intersection", "result": "pass"})

    # ── 6. Bearer / nominee risk ────────────────────────────
    bearer = any(o.get("share_type") == "bearer" for o in owners)
    nominees = any(c.get("role") == "nominee" for c in controllers)
    if bearer or nominees:
        checks.append({"check": "bearer_nominee_risk", "result": "flag",
                       "detail": "Bearer shares or nominee directors detected"})
        flags += 1
    else:
        checks.append({"check": "bearer_nominee_risk", "result": "pass"})

    # ── Score ────────────────────────────────────────────────
    depth = len(owners)
    opacity = depth + flags + sum(1 for c in checks if c["result"] == "insufficient_data")
    rating = "low" if opacity <= 2 else "medium" if opacity <= 4 else "high"

    return {
        "ubo_count": len(owners),
        "chain_depth": depth,
        "opacity_score": opacity,
        "opacity_rating": rating,
        "flags": flags,
        "checks": checks,
        "bods_conformance": "full" if flags == 0 else "partial",
        "recommended_action": (
            f"Submit corrected UBO declaration addressing {flags} flagged item(s)"
            if flags > 0 else "Declaration passes structural validation"
        ),
        "statutory_basis": f"FATF Recommendation 24 — {threshold}% threshold for {applicant.get('applicant_type', 'entity')}"
    }


def get_sample_ubo() -> dict[str, Any]:
    """Return a sample BODS-compliant UBO declaration for testing."""
    return {
        "applicant": {
            "applicant_type": "entity",
            "legal_name": "Acme Global Holdings Ltd",
            "nationality_or_jurisdiction": "Singapore",
            "registered_address": "1 Raffles Place, #20-01, Singapore 048616",
            "dob_or_formation_date": "2015-03-15"
        },
        "beneficial_owners": [
            {"name": "Jane Smith", "ownership_pct": 60, "control_basis": "ownership",
             "nationality": "US", "dob": "1972-08-22"},
            {"name": "Robert Chen", "ownership_pct": 30, "control_basis": "ownership",
             "nationality": "SG", "dob": "1968-11-05"},
            {"name": "TrustCo Nominees Ltd", "ownership_pct": 10, "control_basis": "other",
             "nationality": "KY", "share_type": "bearer"}
        ],
        "controllers": [
            {"name": "Jane Smith", "role": "director"},
            {"name": "Robert Chen", "role": "director"}
        ],
        "pep_declared": False,
        "documents_received": [
            {"type": "Certificate of Incorporation", "ref": "ACME-INC-001", "date": "2015-03-15"},
            {"type": "UBO Declaration", "ref": "ACME-UBO-001", "date": "2025-01-10"}
        ]
    }


# ── MCP server ──────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="BODS UBO Validator MCP server")
    parser.add_argument("--validate", type=str, help="Validate a UBO JSON string")
    parser.add_argument("--sample", action="store_true", help="Return sample UBO record")
    parser.add_argument("--serve", action="store_true", help="Run as MCP stdio server")

    args = parser.parse_args()

    if args.sample:
        print(json.dumps(get_sample_ubo(), indent=2))
    elif args.validate:
        data = json.loads(args.validate)
        result = validate_ubo_chain(data)
        print(json.dumps(result, indent=2))
    elif args.serve:
        # MCP stdio loop — read JSON lines, respond
        print("BODS UBO Validator MCP server ready (stdio)", file=sys.stderr)
        for line in sys.stdin:
            try:
                req = json.loads(line.strip())
                method = req.get("method", "")
                req_id = req.get("id")
                if method == "tools/list":
                    resp = {
                        "jsonrpc": "2.0", "id": req_id, "result": {
                            "tools": [
                                {"name": "ubo-validate", "description": "Validate UBO chain against BODS v0.4",
                                 "inputSchema": {"type": "object", "properties": {"ubo_json": {"type": "string", "description": "UBO declaration JSON"}}, "required": ["ubo_json"]}},
                                {"name": "ubo-sample", "description": "Return sample BODS-compliant UBO record",
                                 "inputSchema": {"type": "object", "properties": {}}}
                            ]
                        }
                    }
                elif method == "tools/call":
                    tool_name = req.get("params", {}).get("name", "")
                    args2 = req.get("params", {}).get("arguments", {})
                    if tool_name == "ubo-validate":
                        data = json.loads(args2.get("ubo_json", "{}"))
                        result = validate_ubo_chain(data)
                        resp = {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}}
                    elif tool_name == "ubo-sample":
                        result = get_sample_ubo()
                        resp = {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}}
                    else:
                        resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}
                else:
                    resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}
                print(json.dumps(resp), flush=True)
            except Exception as e:
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}), flush=True)
    else:
        parser.print_help()
