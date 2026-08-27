"""Fixtures for subprocess tests of scripts/check.py."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest


REAL_CHECK_PY = Path(__file__).resolve().parents[1] / "check.py"


@pytest.fixture
def minimal_repo(tmp_path: Path) -> Path:
    """Build the smallest repository that satisfies every current check."""
    root = tmp_path / "repo"

    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    shutil.copy(REAL_CHECK_PY, scripts / "check.py")

    marketplace = root / ".claude-plugin"
    marketplace.mkdir()
    (marketplace / "marketplace.json").write_text(
        json.dumps(
            {
                "plugins": [
                    {
                        "name": "test-vertical",
                        "source": "./plugins/vertical-plugins/test-vertical",
                    },
                    {
                        "name": "test-agent",
                        "source": "./plugins/agent-plugins/test-agent",
                    },
                ]
            }
        )
    )

    vertical = root / "plugins" / "vertical-plugins" / "test-vertical"
    (vertical / ".claude-plugin").mkdir(parents=True)
    (vertical / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "test-vertical"})
    )
    skill_text = "---\nname: shared-skill\ndescription: Test skill\n---\n\nBody\n"
    source_skill = vertical / "skills" / "shared-skill"
    source_skill.mkdir(parents=True)
    (source_skill / "SKILL.md").write_text(skill_text)

    agent = root / "plugins" / "agent-plugins" / "test-agent"
    (agent / ".claude-plugin").mkdir(parents=True)
    (agent / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "test-agent"})
    )
    (agent / "agents").mkdir()
    (agent / "agents" / "test-agent.md").write_text(
        "---\nname: test-agent\ndescription: Test agent\n---\n\nBody\n"
    )
    bundled_skill = agent / "skills" / "shared-skill"
    bundled_skill.mkdir(parents=True)
    (bundled_skill / "SKILL.md").write_text(skill_text)

    cookbook = root / "managed-agent-cookbooks" / "test-agent"
    cookbook.mkdir(parents=True)
    (cookbook / "README.md").write_text("# Test agent\n")
    (cookbook / "steering-examples.json").write_text("[]\n")
    (cookbook / "agent.yaml").write_text(
        "name: test-agent\n"
        "system:\n"
        "  file: ../../plugins/agent-plugins/test-agent/agents/test-agent.md\n"
        "skills:\n"
        "  - from_plugin: ../../plugins/agent-plugins/test-agent\n"
    )

    return root


@pytest.fixture
def run_check() -> Callable[[Path], subprocess.CompletedProcess[str]]:
    """Run the copied checker exactly as contributors and CI invoke it."""

    def _run(repo: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(repo / "scripts" / "check.py")],
            capture_output=True,
            text=True,
            check=False,
        )

    return _run
