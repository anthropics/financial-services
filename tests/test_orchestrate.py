import importlib.util
import sys
import types
from pathlib import Path


def _load_orchestrate():
    sys.modules.setdefault("anthropic", types.ModuleType("anthropic"))
    spec = importlib.util.spec_from_file_location(
        "orchestrate", Path(__file__).resolve().parents[1] / "scripts" / "orchestrate.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_handoff_with_object_payload_is_extracted():
    orchestrate = _load_orchestrate()
    text = (
        'assistant notes: {"type": "handoff_request", '
        '"target_agent": "pitch-agent", '
        '"payload": {"event": "Build deck", "context_ref": "deal/1"}} trailing text'
    )
    assert orchestrate.extract_handoff(text) == {
        "target_agent": "pitch-agent",
        "payload": {"event": "Build deck", "context_ref": "deal/1"},
    }
