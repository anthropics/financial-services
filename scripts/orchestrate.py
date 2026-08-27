#!/usr/bin/env python3
"""Reference event loop for cross-agent handoffs between managed agents.

REFERENCE ONLY — replace with your firm's workflow engine (Temporal, Airflow,
Guidewire event bus). This script shows the shape of the loop, not a
production implementation.
"""
import json
import os
import re

import anthropic
import jsonschema

ALLOWED_TARGETS = {
    "pitch-agent", "market-researcher", "earnings-reviewer", "meeting-prep-agent",
    "model-builder", "gl-reconciler", "kyc-screener",
    "valuation-reviewer", "month-end-closer", "statement-auditor",
}

HANDOFF_PAYLOAD_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["event"],
    "properties": {
        "event": {"type": "string", "maxLength": 2000},
        "context_ref": {"type": "string", "maxLength": 256,
                        "pattern": r"^[A-Za-z0-9 ._/:#-]+$"},
    },
}

# Find the starting point of the handoff request
MARKER_RE = re.compile(r'"type"\s*:\s*"handoff_request"')

def _extract_json_object(text: str, start_index: int) -> str | None:
    """Extracts a complete JSON object handling nested braces and strings."""
    depth = 0
    in_string = False
    escaped = False
    
    for i in range(start_index, len(text)):
        char = text[i]
        
        if in_string:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                in_string = False
            continue
        
        if char == '"':
            in_string = True
        elif char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return text[start_index : i + 1]
    return None

def extract_handoff(text: str) -> dict | None:
    """Scans text for handoff requests and validates them."""
    for match in MARKER_RE.finditer(text):
        # Look back for the opening brace
        start_pos = text.rfind('{', 0, match.start())
        if start_pos == -1:
            continue
            
        json_str = _extract_json_object(text, start_pos)
        if not json_str:
            continue
            
        try:
            obj = json.loads(json_str)
        except json.JSONDecodeError:
            continue

        target = obj.get("target_agent")
        payload = obj.get("payload")

        if target not in ALLOWED_TARGETS:
            continue

        try:
            jsonschema.validate(instance=payload, schema=HANDOFF_PAYLOAD_SCHEMA)
        except (jsonschema.ValidationError, jsonschema.SchemaError):
            continue

        return {"target_agent": target, "payload": payload}
    
    return None

def run(source_session_id: str, agent_ids: dict[str, str]) -> None:
    """Main loop: listens to the stream and steers to target agents."""
    client = anthropic.Anthropic()
    with client.beta.agents.sessions.stream(session_id=source_session_id) as stream:
        for event in stream:
            if event.type != "message_delta" or not getattr(event, "text", None):
                continue
            
            handoff = extract_handoff(event.text)
            if not handoff:
                continue
                
            target_slug = handoff["target_agent"]
            target_id = agent_ids.get(target_slug)
            if not target_id:
                continue
                
            client.beta.agents.sessions.steer(
                agent_id=target_id,
                input=handoff["payload"]["event"],
            )

if __name__ == "__main__":
    run(
        source_session_id=os.environ["SOURCE_SESSION_ID"],
        agent_ids=json.loads(os.environ.get("AGENT_IDS", "{}")),
    )
