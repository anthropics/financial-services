#!/usr/bin/env python3
"""
Single source of truth for plugin version-bump enforcement.

A plugin's `.claude-plugin/plugin.json` `version` gates update delivery to
already-installed users (Claude Code only re-delivers a plugin when its
version changes). This script guarantees that any plugin modified on a
branch ends up exactly one patch ahead of `main` — bumped once, not once
per commit.

Modes
  --apply   Mutating. For every plugin with staged changes whose version is
            not yet ahead of the base ref, patch-bump it (base + 1) and
            `git add` the result. Idempotent: a plugin already ahead of base
            is left untouched, so repeated commits on a branch bump once.
            Used by .githooks/pre-commit.

  --check   Read-only. For every plugin changed between the base ref and
            HEAD, fail (exit 1) if its version is not strictly greater than
            the base ref's version. Used by .github/workflows/version-bump.yml
            as a backstop for contributors without the local hook.

Base ref resolution (in order): explicit --base, origin/main, main.
Exit 0 clean, 1 on a --check violation, 2 on an internal error.
Requires: git, python3 (stdlib only).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*args: str) -> str:
    """Run a git command, returning stdout (stripped). Raises on failure."""
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def git_ok(*args: str) -> str | None:
    """Run a git command, returning stdout or None if it fails."""
    try:
        return git(*args)
    except subprocess.CalledProcessError:
        return None


def resolve_base(explicit: str | None) -> str | None:
    for ref in (explicit, "origin/main", "main"):
        if ref and git_ok("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"):
            return ref
    return None


def all_plugin_jsons() -> list[Path]:
    """Every <plugin>/.claude-plugin/plugin.json in the repo."""
    return sorted(
        p for p in ROOT.glob("**/.claude-plugin/plugin.json")
        if ".git/" not in str(p)
    )


def plugin_root(plugin_json: Path) -> Path:
    # <root>/.claude-plugin/plugin.json -> <root>
    return plugin_json.parent.parent


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def parse_semver(v: str) -> tuple[int, int, int] | None:
    """Parse 'x.y.z' into a comparable tuple. None if not parseable."""
    parts = (v or "").split(".")
    if len(parts) != 3:
        return None
    try:
        return tuple(int(x) for x in parts)  # type: ignore[return-value]
    except ValueError:
        return None


def patch_bump(v: str) -> str:
    sv = parse_semver(v)
    if sv is None:
        # Unparseable base — start a clean patch series.
        return "0.0.1"
    return f"{sv[0]}.{sv[1]}.{sv[2] + 1}"


def base_version(base: str, plugin_json: Path) -> str | None:
    """The plugin's version at the base ref, or None if it didn't exist there."""
    raw = git_ok("show", f"{base}:{rel(plugin_json)}")
    if raw is None:
        return None
    try:
        return json.loads(raw).get("version")
    except json.JSONDecodeError:
        return None


def working_version(plugin_json: Path) -> str | None:
    try:
        return json.loads(plugin_json.read_text()).get("version")
    except (OSError, json.JSONDecodeError):
        return None


def is_ahead(work: str | None, base: str | None) -> bool:
    """True if the working version is strictly greater than the base version."""
    if base is None:
        # Plugin is new on this branch — nothing to be 'ahead' of.
        return True
    wv, bv = parse_semver(work or ""), parse_semver(base)
    if wv is None or bv is None:
        # Can't compare numerically — fall back to 'changed string == bump'.
        return (work or "") != base
    return wv > bv


def changed_plugins(base: str, staged_only: bool) -> list[Path]:
    """Plugin roots touched relative to base (staged set, or base...HEAD)."""
    if staged_only:
        files = git_ok("diff", "--cached", "--name-only") or ""
    else:
        files = git_ok("diff", "--name-only", f"{base}...HEAD") or ""
    changed = {Path(line) for line in files.splitlines() if line}

    hits: list[Path] = []
    for pj in all_plugin_jsons():
        root_rel = Path(rel(plugin_root(pj)))
        if any(
            c == root_rel or root_rel in c.parents or str(c).startswith(f"{root_rel}/")
            for c in changed
        ):
            hits.append(pj)
    return hits


def cmd_apply(base: str) -> int:
    bumped = []
    for pj in changed_plugins(base, staged_only=True):
        work = working_version(pj)
        bv = base_version(base, pj)
        if is_ahead(work, bv):
            continue  # already bumped on this branch — idempotent no-op
        new = patch_bump(bv or work or "0.0.0")
        data = json.loads(pj.read_text())
        data["version"] = new
        pj.write_text(json.dumps(data, indent=2) + "\n")
        git("add", rel(pj))
        bumped.append((rel(plugin_root(pj)), bv, new))

    for name, old, new in bumped:
        print(f"[version-bump] {name}: {old or '(new)'} -> {new}")
    return 0


def cmd_check(base: str) -> int:
    violations = []
    for pj in changed_plugins(base, staged_only=False):
        work = working_version(pj)
        bv = base_version(base, pj)
        if not is_ahead(work, bv):
            violations.append(
                f"{rel(plugin_root(pj))}: changed but version not bumped "
                f"({bv} -> {work}). Bump .claude-plugin/plugin.json version "
                f"(or run scripts/check.py once to install the pre-commit hook)."
            )
    if violations:
        print(
            f"FAIL — {len(violations)} plugin(s) changed without a version bump:\n",
            file=sys.stderr,
        )
        for v in violations:
            print(f"  ✗ {v}", file=sys.stderr)
        return 1
    print("OK — all changed plugins have a version bump.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Plugin version-bump enforcement.")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true", help="bump staged plugins (pre-commit)")
    mode.add_argument("--check", action="store_true", help="verify changed plugins are bumped (CI)")
    ap.add_argument("--base", help="base ref (default: origin/main, then main)")
    args = ap.parse_args()

    base = resolve_base(args.base)
    if base is None:
        # No base to compare against (e.g. fresh shallow clone offline).
        # Never block a commit over this; CI has full history as the backstop.
        print("[version-bump] no base ref found; skipping.", file=sys.stderr)
        return 0

    return cmd_apply(base) if args.apply else cmd_check(base)


if __name__ == "__main__":
    sys.exit(main())
