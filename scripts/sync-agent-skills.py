#!/usr/bin/env python3
"""
Re-sync each agent plugin's bundled skills from the vertical-plugin source.

Agent plugins under plugins/agent-plugins/<slug>/skills/<name>/ are vendored
copies of plugins/vertical-plugins/*/skills/<name>/. The vertical copy is the
source of truth; run this after editing a skill there to propagate the change
into every agent that bundles it.

Usage: python3 scripts/sync-agent-skills.py
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "plugins" / "agent-plugins"
VERTICALS = ROOT / "plugins" / "vertical-plugins"

def sync_agent_skills(root: Path = ROOT) -> tuple[int, list[str]]:
    agents = root / "plugins" / "agent-plugins"
    verticals = root / "plugins" / "vertical-plugins"

    src_by_name: dict[str, Path] = {}
    for sk in verticals.glob("*/skills/*"):
        if sk.is_dir():
            src_by_name[sk.name] = sk

    synced = 0
    missing: list[str] = []
    for bundled in sorted(agents.glob("*/skills/*")):
        if not bundled.is_dir():
            continue
        src = src_by_name.get(bundled.name)
        if not src:
            missing.append(str(bundled.relative_to(root)))
            continue
        shutil.rmtree(bundled)
        shutil.copytree(src, bundled)
        synced += 1

    return synced, missing


def main() -> int:
    synced, missing = sync_agent_skills()
    print(f"synced {synced} bundled skill dir(s) from vertical-plugins/")
    if missing:
        print("WARN: no vertical source found for:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
