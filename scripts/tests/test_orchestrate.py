"""Tests for extract_handoff in scripts/orchestrate.py.

The original regex-based extractor truncated at the first `}`, breaking any
handoff whose `payload.event` contained nested JSON or a brace inside a
quoted string. These tests pin that bug shut and cover the validation paths.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

# Import orchestrate as a module without executing __main__
ORCHESTRATE_PATH = Path(__file__).resolve().parents[1] / "orchestrate.py"
spec = importlib.util.spec_from_file_location("orchestrate", ORCHESTRATE_PATH)
orchestrate = importlib.util.module_from_spec(spec)
sys.modules["orchestrate"] = orchestrate
spec.loader.exec_module(orchestrate)
extract_handoff = orchestrate.extract_handoff


def _wrap(payload_event: str, target: str = "model-builder") -> str:
    """Build a handoff_request JSON blob with the given event string."""
    return json.dumps(
        {"type": "handoff_request", "target_agent": target,
         "payload": {"event": payload_event}}
    )


def test_simple_handoff_extracted() -> None:
    text = "preamble " + _wrap("Build dcf for MSFT") + " trailing"
    result = extract_handoff(text)
    assert result == {
        "target_agent": "model-builder",
        "payload": {"event": "Build dcf for MSFT"},
    }


def test_handoff_with_nested_json_in_payload_survives() -> None:
    """Regression — original non-greedy regex truncated at the first `}`."""
    nested = 'assumptions: {"wacc": 0.085, "tgr": 0.025, "horizon": 5}'
    text = _wrap(nested)
    result = extract_handoff(text)
    assert result is not None
    assert result["payload"]["event"] == nested


def test_handoff_with_brace_inside_quoted_string_survives() -> None:
    """A literal `}` inside a JSON string must not terminate the scan."""
    text = _wrap("note: closing brace } in narration")
    result = extract_handoff(text)
    assert result is not None
    assert "}" in result["payload"]["event"]


def test_invalid_target_agent_rejected() -> None:
    text = _wrap("doing things", target="unknown-agent")
    assert extract_handoff(text) is None


def test_schema_invalid_payload_rejected() -> None:
    text = json.dumps({
        "type": "handoff_request",
        "target_agent": "model-builder",
        "payload": {"event": "x", "context_ref": "bad ref with !@#$%"},
    })
    assert extract_handoff(text) is None


def test_no_handoff_returns_none() -> None:
    assert extract_handoff("just some streaming text, nothing to see") is None


def test_payload_missing_event_rejected() -> None:
    text = json.dumps({
        "type": "handoff_request",
        "target_agent": "model-builder",
        "payload": {},
    })
    assert extract_handoff(text) is None


def test_first_valid_handoff_wins_over_invalid() -> None:
    """If text contains multiple candidates, the first valid one is returned."""
    bad = json.dumps({
        "type": "handoff_request",
        "target_agent": "not-on-the-allowlist",
        "payload": {"event": "skip me"},
    })
    good = _wrap("use me")
    result = extract_handoff(f"{bad} ... {good}")
    assert result is not None
    assert result["payload"]["event"] == "use me"
