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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "plugins" / "agent-plugins"
VERTICALS = ROOT / "plugins" / "vertical-plugins"

# index every skill name -> source dir in verticals
src_by_name: dict[str, Path] = {}
for sk in VERTICALS.glob("*/skills/*"):
    if sk.is_dir():
        src_by_name[sk.name] = sk

synced = 0
agent_owned = 0
for bundled in sorted(AGENTS.glob("*/skills/*")):
    if not bundled.is_dir():
        continue
    src = src_by_name.get(bundled.name)
    if not src:
        # Agent-only skills are canonical in their bundle; there is nothing to
        # sync when no vertical plugin exposes a skill with the same name.
        agent_owned += 1
        continue
    shutil.rmtree(bundled)
    shutil.copytree(src, bundled)
    synced += 1

print(f"synced {synced} bundled skill dir(s) from vertical-plugins/")
if agent_owned:
    print(f"left {agent_owned} agent-only skill dir(s) unchanged")
