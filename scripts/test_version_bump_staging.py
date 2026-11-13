"""Integration tests for version bumping with staged and unstaged manifest edits."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).with_name("version_bump.py")
HOOK = SOURCE.parent.parent / ".githooks" / "pre-commit"


class VersionBumpStagingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "scripts").mkdir()
        shutil.copy2(SOURCE, self.root / "scripts" / "version_bump.py")
        self.git("init", "-q")
        self.git("config", "user.name", "Test User")
        self.git("config", "user.email", "test@example.invalid")
        self.create_plugin("one")
        self.create_plugin("two")
        self.git("add", ".")
        self.git("commit", "-qm", "base")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), *args], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ).stdout

    def create_plugin(self, name):
        manifest = self.manifest(name)
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({"name": name, "version": "1.2.3", "description": "original"}) + "\n")
        (manifest.parent.parent / "skill.md").write_text("original\n")

    def manifest(self, name):
        return self.root / "plugins" / name / ".claude-plugin" / "plugin.json"

    def stage_skill(self, name):
        path = self.manifest(name).parent.parent / "skill.md"
        path.write_text("changed\n")
        self.git("add", str(path))

    def update_manifest(self, name, **changes):
        path = self.manifest(name)
        contents = json.loads(path.read_text())
        contents.update(changes)
        path.write_text(json.dumps(contents) + "\n")

    def indexed_manifest(self, name):
        path = self.manifest(name).relative_to(self.root).as_posix()
        return json.loads(self.git("show", f":{path}"))

    def apply(self):
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / "version_bump.py"), "--apply", "--base", "HEAD"],
            cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )

    def install_hook(self):
        directory = self.root / ".githooks"
        directory.mkdir()
        shutil.copy2(HOOK, directory / "pre-commit")
        (directory / "pre-commit").chmod(0o755)
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("config", "core.hooksPath", ".githooks")

    def test_real_commit_hook_rejects_unstaged_manifest(self):
        self.install_hook()
        self.stage_skill("one")
        self.update_manifest("one", description="unstaged edit")
        before = self.git("rev-parse", "HEAD")
        result = subprocess.run(
            ["git", "-C", str(self.root), "commit", "-m", "change plugin"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("unstaged", result.stderr.lower())
        self.assertEqual(self.git("rev-parse", "HEAD"), before)
        self.assertEqual(self.indexed_manifest("one")["description"], "original")

    def test_real_commit_hook_bumps_clean_manifest(self):
        self.install_hook()
        self.stage_skill("one")
        self.git("commit", "-qm", "change plugin")
        self.assertEqual(self.indexed_manifest("one")["version"], "1.2.4")
        path = self.manifest("one").relative_to(self.root).as_posix()
        self.assertEqual(json.loads(self.git("show", f"HEAD:{path}"))["version"], "1.2.4")

    def test_unstaged_metadata_does_not_get_staged(self):
        self.stage_skill("one")
        self.update_manifest("one", description="unstaged edit")
        before = self.manifest("one").read_bytes()
        result = self.apply()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("unstaged", result.stderr.lower())
        self.assertEqual(self.indexed_manifest("one")["description"], "original")
        self.assertEqual(self.manifest("one").read_bytes(), before)

    def test_unstaged_version_is_not_counted_as_a_staged_bump(self):
        self.stage_skill("one")
        self.update_manifest("one", version="1.2.4")
        result = self.apply()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.indexed_manifest("one")["version"], "1.2.3")

    def test_staged_version_with_unstaged_metadata_remains_untouched(self):
        self.stage_skill("one")
        self.update_manifest("one", version="1.2.4")
        self.git("add", str(self.manifest("one")))
        self.update_manifest("one", description="unstaged edit")
        before = self.manifest("one").read_bytes()
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.indexed_manifest("one")["description"], "original")
        self.assertEqual(self.manifest("one").read_bytes(), before)

    def test_ordinary_staged_change_is_bumped_once(self):
        self.stage_skill("one")
        for _ in range(2):
            result = self.apply()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.indexed_manifest("one")["version"], "1.2.4")
        self.assertEqual(json.loads(self.manifest("one").read_text())["version"], "1.2.4")

    def test_staged_manifest_edit_is_kept_with_the_bump(self):
        self.stage_skill("one")
        self.update_manifest("one", description="staged edit")
        self.git("add", str(self.manifest("one")))
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.indexed_manifest("one")["description"], "staged edit")
        self.assertEqual(self.indexed_manifest("one")["version"], "1.2.4")

    def test_non_ascii_staged_filename_still_triggers_bump(self):
        path = self.manifest("one").parent.parent / "研究.md"
        path.write_text("changed\n", encoding="utf-8")
        self.git("add", str(path))
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.indexed_manifest("one")["version"], "1.2.4")

    def test_check_detects_non_ascii_committed_filename(self):
        path = self.manifest("one").parent.parent / "研究.md"
        path.write_text("changed\n", encoding="utf-8")
        self.git("add", str(path))
        self.git("commit", "-qm", "change plugin without bump")
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts" / "version_bump.py"),
             "--check", "--base", "HEAD^"],
            cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("without a version bump", result.stderr)

    def test_unstaged_manifest_deletion_is_not_silently_skipped(self):
        self.stage_skill("one")
        self.manifest("one").unlink()
        result = self.apply()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.indexed_manifest("one")["version"], "1.2.3")
        self.assertFalse(self.manifest("one").exists())

    def test_dirty_manifest_fails_before_any_plugin_is_changed(self):
        self.stage_skill("one")
        self.stage_skill("two")
        self.update_manifest("two", description="unstaged edit")
        result = self.apply()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.indexed_manifest("one")["version"], "1.2.3")
        self.assertEqual(self.indexed_manifest("two")["version"], "1.2.3")


if __name__ == "__main__":
    unittest.main()
