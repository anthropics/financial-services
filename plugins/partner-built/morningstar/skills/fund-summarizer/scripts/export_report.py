#!/usr/bin/env python3
"""Export a rendered Morningstar fund summary HTML report to PDF.

This wrapper keeps the skill entry point Python-friendly while using the
Codex-bundled Node runtime when it is available. The companion
export_report.mjs script uses Playwright for faithful HTML-to-PDF rendering.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
NODE_SCRIPT = SCRIPT_DIR / "export_report.mjs"
BUNDLED_NODE_ROOT = (
    Path.home()
    / ".cache"
    / "codex-runtimes"
    / "codex-primary-runtime"
    / "dependencies"
    / "node"
)


def default_node() -> str:
    bundled_node = BUNDLED_NODE_ROOT / "bin" / "node"
    return str(bundled_node) if bundled_node.exists() else "node"


def default_node_path() -> str | None:
    bundled_modules = BUNDLED_NODE_ROOT / "node_modules"
    return str(bundled_modules) if bundled_modules.exists() else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a rendered Morningstar HTML fund report to PDF.",
    )
    parser.add_argument("html", help="Path or file:// URL for the rendered HTML report")
    parser.add_argument(
        "--format",
        choices=["pdf"],
        default="pdf",
        help="Export format",
    )
    parser.add_argument("--output", help="Output PDF path")
    parser.add_argument("--output-dir", help="Output directory; defaults to the HTML file directory")
    parser.add_argument("--node", default=default_node(), help="Node.js executable")
    parser.add_argument(
        "--node-path",
        default=default_node_path(),
        help="NODE_PATH containing playwright",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    command = [
        args.node,
        str(NODE_SCRIPT),
        "--input",
        args.html,
        "--format",
        args.format,
    ]
    if args.output:
        command.extend(["--output", args.output])
    if args.output_dir:
        command.extend(["--output-dir", args.output_dir])

    env = os.environ.copy()
    if args.node_path:
        existing_node_path = env.get("NODE_PATH")
        env["NODE_PATH"] = (
            args.node_path
            if not existing_node_path
            else os.pathsep.join([args.node_path, existing_node_path])
        )

    try:
        completed = subprocess.run(command, check=False, env=env)
    except FileNotFoundError:
        print(f"Error: Node executable not found: {args.node}", file=sys.stderr)
        return 127
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
