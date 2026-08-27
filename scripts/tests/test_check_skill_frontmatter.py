"""Regression coverage for Claude skill frontmatter validation."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from subprocess import CompletedProcess

import pytest


def skill_files(repo: Path) -> tuple[Path, Path]:
    """Return the canonical skill and its synchronized agent copy."""
    source = (
        repo
        / "plugins"
        / "vertical-plugins"
        / "test-vertical"
        / "skills"
        / "shared-skill"
        / "SKILL.md"
    )
    bundled = (
        repo
        / "plugins"
        / "agent-plugins"
        / "test-agent"
        / "skills"
        / "shared-skill"
        / "SKILL.md"
    )
    return source, bundled


def write_both(repo: Path, content: str) -> None:
    """Keep source and bundled skill identical so drift cannot mask failures."""
    for skill in skill_files(repo):
        skill.write_text(content)


def test_valid_skill_frontmatter_passes(
    minimal_repo: Path,
    run_check: Callable[[Path], CompletedProcess[str]],
) -> None:
    result = run_check(minimal_repo)

    assert result.returncode == 0, result.stderr


def test_skill_without_frontmatter_fails(
    minimal_repo: Path,
    run_check: Callable[[Path], CompletedProcess[str]],
) -> None:
    write_both(minimal_repo, "# Shared skill\n\nBody\n")

    result = run_check(minimal_repo)

    assert result.returncode == 1
    assert "skill-frontmatter" in result.stderr
    assert "missing leading ---" in result.stderr


@pytest.mark.parametrize("missing_key", ["name", "description"])
def test_skill_frontmatter_requires_metadata(
    minimal_repo: Path,
    run_check: Callable[[Path], CompletedProcess[str]],
    missing_key: str,
) -> None:
    metadata = {
        "name": "shared-skill",
        "description": "Test skill",
    }
    metadata.pop(missing_key)
    body = "\n".join(f"{key}: {value}" for key, value in metadata.items())
    write_both(minimal_repo, f"---\n{body}\n---\n\nBody\n")

    result = run_check(minimal_repo)

    assert result.returncode == 1
    assert "skill-frontmatter" in result.stderr
    assert f"missing '{missing_key}'" in result.stderr
