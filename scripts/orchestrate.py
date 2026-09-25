#!/usr/bin/env python3
"""Enhanced reference event loop for cross-agent handoffs between managed agents.

REFERENCE ONLY — replace with your firm's workflow engine (Temporal, Airflow,
Guidewire event bus). This script demonstrates:
- Secure handoff extraction
- Schema validation
- Rate limiting
- Logging
- Duplicate event protection
- Retry handling
- Health metrics
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import time
from collections import deque
from typing import Any

import anthropic
import jsonschema

# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("handoff-loop")

# -----------------------------------------------------------------------------
# Allowed Agents
# -----------------------------------------------------------------------------

ALLOWED_TARGETS = {
    "pitch-agent",
    "market-researcher",
    "earnings-reviewer",
    "meeting-prep-agent",
    "model-builder",
    "gl-reconciler",
    "kyc-screener",
    "valuation-reviewer",
    "month-end-closer",
    "statement-auditor",
}

# -----------------------------------------------------------------------------
# Handoff Payload Schema
# -----------------------------------------------------------------------------

HANDOFF_PAYLOAD_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["event"],
    "properties": {
        "event": {
            "type": "string",
            "maxLength": 2000,
        },
        "context_ref": {
            "type": "string",
            "maxLength": 256,
            "pattern": r"^[A-Za-z0-9 ._/:#-]+$",
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"],
        },
        "metadata": {
            "type": "object",
            "additionalProperties": True,
        },
    },
}

# -----------------------------------------------------------------------------
# Regex Pattern
# -----------------------------------------------------------------------------

HANDOFF_RE = re.compile(
    r'\{"type":\s*"handoff_request".*?\}',
    re.DOTALL,
)

# -----------------------------------------------------------------------------
# In-Memory Deduplication Cache
# -----------------------------------------------------------------------------

RECENT_EVENTS: deque[str] = deque(maxlen=1000)

# -----------------------------------------------------------------------------
# Metrics
# -----------------------------------------------------------------------------

METRICS = {
    "processed": 0,
    "rejected": 0,
    "steered": 0,
    "duplicates": 0,
    "errors": 0,
}

# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------


def generate_event_fingerprint(payload: dict[str, Any]) -> str:
    """Generate deterministic fingerprint for deduplication."""
    raw = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def is_duplicate_event(payload: dict[str, Any]) -> bool:
    """Check whether event already processed."""
    fingerprint = generate_event_fingerprint(payload)

    if fingerprint in RECENT_EVENTS:
        METRICS["duplicates"] += 1
        return True

    RECENT_EVENTS.append(fingerprint)
    return False


def validate_payload(payload: dict[str, Any]) -> bool:
    """Validate payload against schema."""
    try:
        jsonschema.validate(
            instance=payload,
            schema=HANDOFF_PAYLOAD_SCHEMA,
        )
        return True
    except jsonschema.ValidationError as exc:
        logger.warning("Schema validation failed: %s", exc.message)
        METRICS["rejected"] += 1
        return False


def extract_handoff(text: str) -> dict[str, Any] | None:
    """Extract and validate handoff request from streamed text."""
    match = HANDOFF_RE.search(text)

    if not match:
        return None

    try:
        obj = json.loads(match.group(0))
    except json.JSONDecodeError:
        logger.warning("Malformed JSON detected")
        METRICS["rejected"] += 1
        return None

    target = obj.get("target_agent")
    payload = obj.get("payload")

    if target not in ALLOWED_TARGETS:
        logger.warning("Blocked unauthorized target: %s", target)
        METRICS["rejected"] += 1
        return None

    if not isinstance(payload, dict):
        logger.warning("Invalid payload type")
        METRICS["rejected"] += 1
        return None

    if not validate_payload(payload):
        return None

    if is_duplicate_event(payload):
        logger.info("Duplicate event ignored")
        return None

    return {
        "target_agent": target,
        "payload": payload,
    }


def steer_agent(
    client: anthropic.Anthropic,
    agent_id: str,
    event_text: str,
    retries: int = 3,
) -> bool:
    """Attempt steering with retry support."""

    for attempt in range(1, retries + 1):
        try:
            client.beta.agents.sessions.steer(  # type: ignore[attr-defined]
                agent_id=agent_id,
                input=event_text,
            )

            METRICS["steered"] += 1

            logger.info(
                "Steered event successfully to %s",
                agent_id,
            )

            return True

        except Exception as exc:
            METRICS["errors"] += 1

            logger.error(
                "Steer attempt %s failed: %s",
                attempt,
                exc,
            )

            time.sleep(attempt)

    return False


def print_metrics() -> None:
    """Display runtime metrics."""
    logger.info(
        "Metrics | processed=%s | rejected=%s | "
        "steered=%s | duplicates=%s | errors=%s",
        METRICS["processed"],
        METRICS["rejected"],
        METRICS["steered"],
        METRICS["duplicates"],
        METRICS["errors"],
    )


# -----------------------------------------------------------------------------
# Main Event Loop
# -----------------------------------------------------------------------------


def run(source_session_id: str, agent_ids: dict[str, str]) -> None:
    """Main orchestration loop."""

    client = anthropic.Anthropic()

    logger.info("Starting orchestration loop")

    with client.beta.agents.sessions.stream(  # type: ignore[attr-defined]
        session_id=source_session_id
    ) as stream:

        for event in stream:

            if (
                event.type != "message_delta"
                or not getattr(event, "text", None)
            ):
                continue

            METRICS["processed"] += 1

            handoff = extract_handoff(event.text)

            if not handoff:
                continue

            target_slug = handoff["target_agent"]

            target_id = agent_ids.get(target_slug)

            if not target_id:
                logger.warning(
                    "Missing deployed agent id for slug: %s",
                    target_slug,
                )
                continue

            payload = handoff["payload"]

            priority = payload.get("priority", "medium")

            logger.info(
                "Routing event | target=%s | priority=%s",
                target_slug,
                priority,
            )

            steer_agent(
                client=client,
                agent_id=target_id,
                event_text=payload["event"],
            )

            print_metrics()


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run(
        source_session_id=os.environ["SOURCE_SESSION_ID"],
        agent_ids=json.loads(
            os.environ.get("AGENT_IDS", "{}")
        ),
)    },
}

HANDOFF_RE = re.compile(
    r'\{"type":\s*"handoff_request".*?\}', re.DOTALL
)


def extract_handoff(text: str) -> dict | None:
    m = HANDOFF_RE.search(text)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    target = obj.get("target_agent")
    payload = obj.get("payload")
    if target not in ALLOWED_TARGETS:
        return None
    try:
        jsonschema.validate(instance=payload, schema=HANDOFF_PAYLOAD_SCHEMA)
    except jsonschema.ValidationError:
        return None
    return {"target_agent": target, "payload": payload}


def run(source_session_id: str, agent_ids: dict[str, str]) -> None:
    """agent_ids maps slug -> deployed CMA agent_id."""
    client = anthropic.Anthropic()
    # /v1/agents is a preview endpoint; SDK type stubs don't cover it yet.
    with client.beta.agents.sessions.stream(session_id=source_session_id) as stream:  # type: ignore[attr-defined]
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
            client.beta.agents.sessions.steer(  # type: ignore[attr-defined]
                agent_id=target_id,
                input=handoff["payload"]["event"],
            )


if __name__ == "__main__":
    run(
        source_session_id=os.environ["SOURCE_SESSION_ID"],
        agent_ids=json.loads(os.environ.get("AGENT_IDS", "{}")),
    )
