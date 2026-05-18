"""Test fixtures for check.py.

Builds a minimal-valid repo skeleton in a tmpdir and copies `check.py` into it
so the script's `Path(__file__).resolve().parents[1]` correctly identifies the
fixture as ROOT. Tests then mutate one file at a time and assert check.py's
exit code + stderr.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REAL_CHECK_PY = Path(__file__).resolve().parents[1] / "check.py"


@pytest.fixture
def minimal_repo(tmp_path: Path) -> Path:
    """Build a minimal-valid repo skeleton; return its root path."""
    root = tmp_path / "repo"

    # scripts/check.py — copy, not symlink, so Path(__file__).resolve()
    # lands inside the fixture
    (root / "scripts").mkdir(parents=True)
    shutil.copy(REAL_CHECK_PY, root / "scripts" / "check.py")

    # .claude-plugin/marketplace.json
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps(
            {
                "name": "test-marketplace",
                "owner": {"name": "Test"},
                "plugins": [
                    {
                        "name": "test-vertical",
                        "source": "./plugins/vertical-plugins/test-vertical",
                        "description": "Test vertical",
                    },
                    {
                        "name": "test-agent",
                        "source": "./plugins/agent-plugins/test-agent",
                        "description": "Test agent",
                    },
                ],
            }
        )
    )

    # vertical plugin
    vp = root / "plugins" / "vertical-plugins" / "test-vertical"
    (vp / ".claude-plugin").mkdir(parents=True)
    (vp / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": "test-vertical",
                "version": "0.1.0",
                "description": "Test vertical",
                "author": {"name": "Test"},
            }
        )
    )
    (vp / "hooks").mkdir()
    (vp / "hooks" / "hooks.json").write_text(json.dumps({"hooks": {}}))
    (vp / "skills" / "shared-skill").mkdir(parents=True)
    (vp / "skills" / "shared-skill" / "SKILL.md").write_text(
        "---\nname: shared-skill\ndescription: Test\n---\n\nbody\n"
    )

    # agent plugin (bundles the shared-skill)
    ap = root / "plugins" / "agent-plugins" / "test-agent"
    (ap / ".claude-plugin").mkdir(parents=True)
    (ap / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": "test-agent",
                "version": "0.1.0",
                "description": "Test agent",
                "author": {"name": "Test"},
            }
        )
    )
    (ap / "agents").mkdir()
    (ap / "agents" / "test-agent.md").write_text(
        "---\nname: test-agent\ndescription: Test agent\n---\n\nbody\n"
    )
    # bundled copy of the skill — must match the source byte-for-byte
    (ap / "skills" / "shared-skill").mkdir(parents=True)
    (ap / "skills" / "shared-skill" / "SKILL.md").write_text(
        "---\nname: shared-skill\ndescription: Test\n---\n\nbody\n"
    )

    # managed-agent cookbook
    mac = root / "managed-agent-cookbooks" / "test-agent"
    mac.mkdir(parents=True)
    (mac / "README.md").write_text("# test-agent\n")
    (mac / "steering-examples.json").write_text(json.dumps([{"event": "x"}]))
    (mac / "agent.yaml").write_text(
        "name: test-agent\n"
        "system:\n"
        "  file: ../../plugins/agent-plugins/test-agent/agents/test-agent.md\n"
        "skills:\n"
        "  - from_plugin: ../../plugins/agent-plugins/test-agent\n"
    )

    return root


@pytest.fixture
def run_check():
    """Return a callable that runs check.py inside the given repo root."""
    def _run(repo: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(repo / "scripts" / "check.py")],
            capture_output=True,
            text=True,
        )
    return _run
