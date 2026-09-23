"""Regression tests for plugin version bumps; uses temporary Git repositories."""
import contextlib
import io
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import tempfile
import unittest
from unittest.mock import patch

import version_bump


class RelativePathTests(unittest.TestCase):
    def test_git_paths_use_forward_slashes_on_windows_and_posix(self):
        for root in (PureWindowsPath("C:/repo"), PurePosixPath("/repo")):
            with self.subTest(root=root), patch.object(version_bump, "ROOT", root):
                manifest = root / "plugins/sample/.claude-plugin/plugin.json"
                self.assertEqual(
                    version_bump.rel(manifest),
                    "plugins/sample/.claude-plugin/plugin.json",
                )


class VersionBumpTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="version bump ")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        root_patch = patch.object(version_bump, "ROOT", root)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        git_env = patch.dict(os.environ, {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
        })
        git_env.start()
        self.addCleanup(git_env.stop)

        version_bump.git("init", "--initial-branch=main")
        version_bump.git("config", "user.name", "Version bump test")
        version_bump.git("config", "user.email", "test@example.invalid")
        version_bump.git("config", "commit.gpgsign", "false")
        self.manifest_path = "plugins/sample/.claude-plugin/plugin.json"
        self.manifest = root / self.manifest_path
        self.manifest.parent.mkdir(parents=True)
        self.manifest.write_text(json.dumps({"name": "sample", "version": "1.2.3"}))
        self.skill = root / "plugins/sample/skills/example/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("Original skill\n")
        version_bump.git("add", ".")
        version_bump.git("commit", "-m", "Initial plugin")
        version_bump.git("switch", "-c", "update-skill")
        self.skill.write_text("Updated skill\n")
        version_bump.git("add", ".")

    def test_reads_existing_plugin_version_from_git(self):
        self.assertEqual(version_bump.base_version("main", self.manifest), "1.2.3")

    def test_apply_stages_one_patch_bump_and_is_idempotent(self):
        for _ in range(2):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(version_bump.cmd_apply("main"), 0)
            self.assertEqual(version_bump.working_version(self.manifest), "1.2.4")
            staged = json.loads(version_bump.git("show", f":{self.manifest_path}"))
            self.assertEqual(staged["version"], "1.2.4")

    def test_check_rejects_unchanged_version_and_accepts_bumped_version(self):
        version_bump.git("commit", "-m", "Update skill without bump")
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(version_bump.cmd_check("main"), 1)

        self.manifest.write_text(json.dumps({"name": "sample", "version": "1.2.4"}))
        version_bump.git("add", ".")
        version_bump.git("commit", "-m", "Bump plugin version")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(version_bump.cmd_check("main"), 0)


if __name__ == "__main__":
    unittest.main()
