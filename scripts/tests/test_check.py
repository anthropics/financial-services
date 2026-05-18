"""End-to-end tests for scripts/check.py.

Each test mutates one file in the minimal-valid fixture repo and asserts
check.py's exit code + the specific error message. Subprocess-based so
the script is exercised as it actually runs in CI.
"""
from __future__ import annotations

import json
from pathlib import Path

def test_clean_tree_passes(minimal_repo: Path, run_check) -> None:
    result = run_check(minimal_repo)
    assert result.returncode == 0, result.stderr
    assert "OK" in result.stdout


# --- hooks.json validator (Phase 1 addition) -------------------------------

def test_hooks_json_as_array_fails(minimal_repo: Path, run_check) -> None:
    hjf = minimal_repo / "plugins" / "vertical-plugins" / "test-vertical" / "hooks" / "hooks.json"
    hjf.write_text("[]")
    result = run_check(minimal_repo)
    assert result.returncode == 1
    assert "must be" in result.stderr
    assert "got list" in result.stderr
    assert "hooks/hooks.json" in result.stderr


def test_hooks_json_missing_hooks_key_fails(minimal_repo: Path, run_check) -> None:
    hjf = minimal_repo / "plugins" / "vertical-plugins" / "test-vertical" / "hooks" / "hooks.json"
    hjf.write_text("{}")
    result = run_check(minimal_repo)
    assert result.returncode == 1
    assert "must be" in result.stderr


def test_hooks_json_malformed_fails(minimal_repo: Path, run_check) -> None:
    hjf = minimal_repo / "plugins" / "vertical-plugins" / "test-vertical" / "hooks" / "hooks.json"
    hjf.write_text("{not json")
    result = run_check(minimal_repo)
    assert result.returncode == 1
    assert "hooks.json parse" in result.stderr


# --- existing validators (regression coverage) -----------------------------

def test_missing_steering_examples_fails(minimal_repo: Path, run_check) -> None:
    (minimal_repo / "managed-agent-cookbooks" / "test-agent" / "steering-examples.json").unlink()
    result = run_check(minimal_repo)
    assert result.returncode == 1
    assert "missing" in result.stderr
    assert "steering-examples.json" in result.stderr


def test_agent_md_missing_frontmatter_fails(minimal_repo: Path, run_check) -> None:
    md = minimal_repo / "plugins" / "agent-plugins" / "test-agent" / "agents" / "test-agent.md"
    md.write_text("no frontmatter here\n")
    result = run_check(minimal_repo)
    assert result.returncode == 1
    assert "frontmatter" in result.stderr


def test_broken_system_file_ref_fails(minimal_repo: Path, run_check) -> None:
    yml = minimal_repo / "managed-agent-cookbooks" / "test-agent" / "agent.yaml"
    yml.write_text(
        "name: test-agent\n"
        "system:\n"
        "  file: ../../plugins/agent-plugins/test-agent/agents/does-not-exist.md\n"
    )
    result = run_check(minimal_repo)
    assert result.returncode == 1
    assert "system.file" in result.stderr
    assert "not found" in result.stderr


def test_bundled_skill_drift_fails(minimal_repo: Path, run_check) -> None:
    bundled = (
        minimal_repo
        / "plugins"
        / "agent-plugins"
        / "test-agent"
        / "skills"
        / "shared-skill"
        / "SKILL.md"
    )
    bundled.write_text("drifted content\n")
    result = run_check(minimal_repo)
    assert result.returncode == 1
    assert "drifted" in result.stderr
    assert "sync-agent-skills.py" in result.stderr


def test_marketplace_source_must_resolve(minimal_repo: Path, run_check) -> None:
    mp = minimal_repo / ".claude-plugin" / "marketplace.json"
    data = json.loads(mp.read_text())
    data["plugins"].append(
        {
            "name": "ghost",
            "source": "./plugins/vertical-plugins/does-not-exist",
            "description": "broken",
        }
    )
    mp.write_text(json.dumps(data))
    result = run_check(minimal_repo)
    assert result.returncode == 1
    assert "marketplace" in result.stderr
    assert "ghost" in result.stderr
