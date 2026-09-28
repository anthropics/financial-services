#!/usr/bin/env python3
"""Read-only, opt-in structural checks for one selected AISOP/AISP input.

This is a bounded preflight, not an AISOP runtime, full protocol validator,
security review, or host-compatibility check. It reads JSON and explicitly
declared local resources only. Nothing in the selected package is executed.

Examples:
    python scripts/preflight_aisp.py path/to/aisp/reader_aisp
    python scripts/preflight_aisp.py path/to/aisop-program.aisop.json
    python scripts/preflight_aisp.py path/to/skill --allow-shared

The command writes a JSON report to stdout and never modifies the selection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


MAX_PROGRAM_BYTES = 2 * 1024 * 1024
MAX_RESOURCE_BYTES = 2 * 1024 * 1024
MAX_RESOURCES = 256
MAX_PACKAGES = 64
MAX_JSON_DEPTH = 48
MAX_FINDINGS = 200
RESOURCE_MODES = {"read_only", "execute_only", "read_and_execute"}
RISK_LEVELS = {"low", "medium", "high", "critical"}
STEP_BINDING = re.compile(
    r"^(?P<node>[A-Za-z_][A-Za-z0-9_-]*)\."
    r"(?P<step>step[1-9][0-9]*):(?P<mechanism>sys\.[A-Za-z][A-Za-z0-9_.]*)$"
)
BRIDGE_POINTER = re.compile(r"(?m)^\s+aisp_program:\s*([^\s#]+)")


class Report:
    def __init__(self, target: Path, allow_shared: bool) -> None:
        self.value: dict[str, Any] = {
            "selected_path": str(target),
            "format": "unknown",
            "version": None,
            "status": "PASS",
            "checks": [],
            "not_checked": [
                "complete JSON Schema validation of aisp_contract",
                "AISOP graph topology and runtime behavior",
                "host upload or discovery compatibility",
                "program execution (never attempted)",
                "financial correctness, authorization, and trust",
            ],
            "findings": [],
        }
        self.allow_shared = allow_shared

    def add(self, severity: str, code: str, message: str) -> None:
        findings = self.value["findings"]
        if len(findings) < MAX_FINDINGS:
            findings.append({"severity": severity, "code": code, "message": message})
        elif len(findings) == MAX_FINDINGS:
            findings.append({
                "severity": "error",
                "code": "output.limit",
                "message": "Finding limit reached; additional diagnostics were suppressed.",
            })

    def checked(self, name: str) -> None:
        self.value["checks"].append(name)

    def finish(self) -> dict[str, Any]:
        severities = {row["severity"] for row in self.value["findings"]}
        if "error" in severities:
            self.value["status"] = "FAIL"
        elif "incomplete" in severities:
            self.value["status"] = "INCOMPLETE"
        return self.value


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _depth_within_limit(value: Any) -> bool:
    stack = [(value, 1)]
    while stack:
        item, depth = stack.pop()
        if depth > MAX_JSON_DEPTH:
            return False
        if isinstance(item, dict):
            stack.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            stack.extend((child, depth + 1) for child in item)
    return True


def _read_json(path: Path, root: Path, limit: int, report: Report) -> Any | None:
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        report.add("error", "path.unreadable", f"Cannot resolve selected file: {exc}.")
        return None
    if not _is_within(resolved, root):
        report.add("error", "path.escape", "Selected file resolves outside the approved root.")
        return None
    if not resolved.is_file():
        report.add("error", "path.not_file", "Selected program is not a regular file.")
        return None
    try:
        size = resolved.stat().st_size
        if size > limit:
            report.add("error", "input.too_large", f"Selected file exceeds the {limit}-byte limit.")
            return None
        text = resolved.read_bytes().decode("utf-8-sig")
    except (OSError, UnicodeError) as exc:
        report.add("error", "input.unreadable", f"Cannot read UTF-8 JSON input: {exc}.")
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        report.add("error", "json.invalid", f"Invalid JSON at line {exc.lineno}, column {exc.colno}.")
        return None
    except RecursionError:
        report.add("error", "json.too_deep", "JSON nesting exceeds the parser limit.")
        return None
    if not _depth_within_limit(value):
        report.add("error", "json.too_deep", f"JSON nesting exceeds the {MAX_JSON_DEPTH}-level limit.")
        return None
    return value


def _selected_program(target: Path, report: Report) -> tuple[Path, Path] | None:
    """Return (program path, package root) from one explicit local selection."""
    if target.is_file():
        if not target.name.endswith(".aisop.json"):
            report.add("error", "selection.extension", "Select a local *.aisop.json file or package directory.")
            return None
        return target, target.parent

    if not target.is_dir():
        report.add("error", "selection.missing", "Selected path does not exist or is not a file/directory.")
        return None

    direct = target / "aisp.aisop.json"
    if target.name.endswith("_aisp"):
        return direct, target

    roots = []
    if target.name == "aisp":
        roots.append(target)
    aisp_dir = target / "aisp"
    if aisp_dir.is_dir() and not aisp_dir.is_symlink():
        roots.append(aisp_dir)
    if direct.exists():
        return direct, target

    candidates: list[tuple[Path, Path]] = []
    for root in roots:
        try:
            with os.scandir(root) as entries:
                for entry in entries:
                    if not entry.name.endswith("_aisp"):
                        continue
                    if entry.is_symlink():
                        report.add("error", "path.symlink", f"Package directory is a symlink: {entry.name}.")
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        candidates.append((Path(entry.path) / "aisp.aisop.json", Path(entry.path)))
                        if len(candidates) > MAX_PACKAGES:
                            report.add("error", "selection.too_many", f"Package discovery exceeds {MAX_PACKAGES} entries.")
                            return None
        except OSError as exc:
            report.add("error", "selection.unreadable", f"Cannot inspect selected package root: {exc}.")
            return None

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        report.add("error", "selection.ambiguous", "Select one *_aisp package instead of a directory containing several.")
        return None
    report.add("incomplete", "selection.no_package", "No AISP package was found at the selected path; select a standalone *.aisop.json file to inspect it as standalone AISOP.")
    return None


def _contract_checks(program: Any, package_root: Path, report: Report) -> None:
    if not isinstance(program, list) or len(program) != 2:
        report.add("error", "aisop.envelope", "AISP V1.0.0 requires a two-message JSON array.")
        return
    system, user = program
    if not isinstance(system, dict) or system.get("role") != "system" or not isinstance(system.get("content"), dict):
        report.add("error", "aisop.system", "First message must be a system message with an object content field.")
        return
    if not isinstance(user, dict) or user.get("role") != "user" or not isinstance(user.get("content"), dict):
        report.add("error", "aisop.user", "Second message must be a user message with an object content field.")
        return
    system_content = system["content"]
    user_content = user["content"]
    report.checked("two-message role/content envelope")

    for field in ("protocol", "axiom_0", "id", "name", "version", "flow_format", "loading_mode"):
        if not isinstance(system_content.get(field), str) or not system_content[field].strip():
            report.add("error", "aisop.required_field", f"system.content.{field} must be a non-empty string.")
    if system_content.get("protocol") != "AISP V1.0.0":
        report.add("error", "aisp.unsupported_version", "Only the AISP V1.0.0 package marker is supported.")
    if system_content.get("loading_mode") != "node":
        report.add("error", "aisp.loading_mode", "AISP V1.0.0 requires loading_mode to be 'node'.")
    if not package_root.name.endswith("_aisp") or package_root.parent.name != "aisp":
        report.add("error", "aisp.layout", "AISP package must be under aisp/<id>_aisp/.")
    if system_content.get("id") != package_root.name:
        report.add("error", "aisp.id_mismatch", "system.content.id must match the *_aisp package folder name.")

    if not isinstance(user_content.get("instruction"), str) or not user_content["instruction"].strip():
        report.add("error", "aisop.instruction", "user.content.instruction must be a non-empty string.")
    aisop = user_content.get("aisop")
    functions = user_content.get("functions")
    if not isinstance(aisop, dict) or not aisop.get("main"):
        report.add("error", "aisop.main", "user.content.aisop.main must be present and non-empty.")
    if not isinstance(functions, dict):
        report.add("error", "aisop.functions", "user.content.functions must be an object.")
        functions = {}
    else:
        report.checked("AISOP main and functions presence")

    contract = user_content.get("aisp_contract")
    if not isinstance(contract, dict):
        report.add("error", "aisp.contract", "user.content.aisp_contract must be a JSON object.")
        return
    profile = contract.get("profile")
    if not isinstance(profile, str) or not profile.startswith("aisp.skill."):
        report.add("error", "aisp.contract_profile", "aisp_contract.profile must start with 'aisp.skill.'.")
    invocation = contract.get("invocation")
    if not isinstance(invocation, dict):
        report.add("error", "aisp.invocation", "aisp_contract.invocation must be an object.")
    non_negotiable = contract.get("non_negotiable")
    if not isinstance(non_negotiable, list):
        report.add("error", "aisp.non_negotiable", "aisp_contract.non_negotiable must be an array.")
        non_negotiable = []
    risk_level = contract.get("risk_level")
    if risk_level is not None and (not isinstance(risk_level, str) or risk_level not in RISK_LEVELS):
        report.add("error", "aisp.risk_level", "aisp_contract.risk_level must be low, medium, high, or critical.")
    resources = contract.get("resources", [])
    if not isinstance(resources, list):
        report.add("error", "aisp.resources", "aisp_contract.resources must be an array when present.")
        resources = []
    if len(resources) > MAX_RESOURCES:
        report.add("error", "aisp.resource_limit", f"Resource count exceeds the {MAX_RESOURCES}-entry limit.")
        resources = resources[:MAX_RESOURCES]
    report.checked("partial contract required-field/type checks")

    for index, entry in enumerate(non_negotiable):
        if not isinstance(entry, dict) or not isinstance(entry.get("rule"), str) or not isinstance(entry.get("enforced_by"), str):
            report.add("error", "aisp.binding_shape", f"non_negotiable[{index}] requires string rule and enforced_by fields.")
            continue
        binding = entry["enforced_by"]
        match = STEP_BINDING.fullmatch(binding)
        if match:
            node = functions.get(match.group("node"))
            step_name = match.group("step")
            step = node.get(step_name) if isinstance(node, dict) else None
            mechanism = match.group("mechanism")
            if not isinstance(step, str):
                report.add("error", "aisp.binding_missing_step", f"Binding {binding!r} does not name a string functions step.")
            elif not step.startswith(mechanism):
                report.add("error", "aisp.binding_mechanism", f"Binding {binding!r} does not match the mechanism at its step.")
            else:
                report.checked(f"enforced_by path binding {binding}")
        elif binding == "aisop.main":
            if isinstance(aisop, dict) and aisop.get("main"):
                report.add("incomplete", "aisp.binding_topology", "aisop.main is present, but graph topology and required-node semantics are not checked.")
            else:
                report.add("error", "aisp.binding_missing_main", "aisop.main binding has no main graph.")
        elif binding == "tools":
            report.add("incomplete", "aisp.binding_tools", "tools binding depends on runtime permission enforcement, which static inspection cannot establish.")
        else:
            report.add("error", "aisp.binding_grammar", f"Unsupported or malformed enforced_by binding: {binding!r}.")

    shared_root = package_root.parent / "_shared"
    for index, resource in enumerate(resources):
        _resource_check(resource, index, package_root, shared_root, report)

    _bridge_check(package_root, report)
    report.add("incomplete", "aisp.schema_partial", "The installed upstream JSON Schema is not vendored; contract validation is intentionally limited to the listed field/type checks.")
    report.add("incomplete", "aisp.graph_partial", "Graph syntax, topology, reachable nodes, and runtime behavior are not checked.")


def _resource_check(resource: Any, index: int, package_root: Path, shared_root: Path, report: Report) -> None:
    if not isinstance(resource, dict):
        report.add("error", "aisp.resource_shape", f"resources[{index}] must be an object.")
        return
    resource_id = resource.get("id")
    raw_path = resource.get("path")
    mode = resource.get("mode")
    scope = resource.get("scope", "skill")
    if not isinstance(resource_id, str) or not resource_id.strip():
        report.add("error", "aisp.resource_id", f"resources[{index}].id must be a non-empty string.")
    if not isinstance(raw_path, str) or not raw_path.strip():
        report.add("error", "aisp.resource_path", f"resources[{index}].path must be a non-empty relative path.")
        return
    if not isinstance(mode, str) or mode not in RESOURCE_MODES:
        report.add("error", "aisp.resource_mode", f"resources[{index}].mode is not a supported AISP mode.")
    if not isinstance(scope, str) or scope not in {"skill", "shared"}:
        report.add("error", "aisp.resource_scope", f"resources[{index}].scope must be 'skill' or 'shared'.")
        return

    posix = PurePosixPath(raw_path)
    windows = PureWindowsPath(raw_path)
    if posix.is_absolute() or windows.is_absolute() or windows.drive or "\\" in raw_path or ".." in posix.parts:
        report.add("error", "aisp.resource_escape", f"Resource {resource_id!r} path is absolute or escapes its approved root.")
        return
    if any(part in {"", "."} for part in posix.parts):
        report.add("error", "aisp.resource_path", f"Resource {resource_id!r} path contains an empty or dot component.")
        return

    if scope == "shared":
        if not report.allow_shared:
            report.add("incomplete", "aisp.shared_unapproved", f"Shared resource {resource_id!r} was not read; pass --allow-shared to approve only aisp/_shared/.")
            return
        base = shared_root
    else:
        base = package_root

    path = base.joinpath(*posix.parts)
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        report.add("error", "aisp.resource_missing", f"Resource {resource_id!r} is missing or unreadable: {exc}.")
        return
    if not _is_within(resolved, base.resolve()):
        report.add("error", "aisp.resource_escape", f"Resource {resource_id!r} resolves outside its approved {scope} root.")
        return
    if not resolved.is_file():
        report.add("error", "aisp.resource_not_file", f"Resource {resource_id!r} does not resolve to a regular file.")
        return
    try:
        size = resolved.stat().st_size
        if size > MAX_RESOURCE_BYTES:
            report.add("error", "aisp.resource_too_large", f"Resource {resource_id!r} exceeds the {MAX_RESOURCE_BYTES}-byte limit.")
            return
        expected_hash = resource.get("sha256")
        if expected_hash is not None:
            if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash):
                report.add("error", "aisp.resource_hash", f"Resource {resource_id!r} has a malformed sha256 value.")
                return
            actual_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()
            if actual_hash.lower() != expected_hash.lower():
                report.add("error", "aisp.resource_hash", f"Resource {resource_id!r} does not match its declared sha256.")
                return
    except OSError as exc:
        report.add("error", "aisp.resource_unreadable", f"Resource {resource_id!r} cannot be read: {exc}.")
        return
    report.checked(f"resource path and existence: {resource_id}")


def _bridge_check(package_root: Path, report: Report) -> None:
    bridge = package_root / "SKILL.md"
    if bridge.is_symlink():
        report.add("error", "aisp.bridge_symlink", "SKILL.md may not be a symlink.")
        return
    if not bridge.exists():
        report.add("incomplete", "aisp.bridge_absent", "No same-folder SKILL.md bridge is present; native AISP inspection remains possible.")
        return
    try:
        resolved = bridge.resolve(strict=True)
        if not _is_within(resolved, package_root.resolve()):
            report.add("error", "aisp.bridge_escape", "SKILL.md resolves outside the selected AISP package.")
            return
        if resolved.stat().st_size > MAX_RESOURCE_BYTES:
            report.add("error", "aisp.bridge_too_large", "SKILL.md exceeds the input-size limit.")
            return
        text = resolved.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        report.add("error", "aisp.bridge_unreadable", f"Same-folder SKILL.md cannot be read: {exc}.")
        return
    frontmatter = re.match(r"\A---\s*\n(.*?)\n---(?:\s|$)", text, flags=re.DOTALL)
    if not frontmatter:
        report.add("incomplete", "aisp.bridge_frontmatter", "SKILL.md exists but its YAML frontmatter was not parsed.")
        return
    pointer = BRIDGE_POINTER.search(frontmatter.group(1))
    if pointer and pointer.group(1).strip("\"'") == "aisp.aisop.json":
        report.checked("same-folder SKILL.md bridge pointer")
    elif pointer:
        report.add("error", "aisp.bridge_pointer", "Bridge metadata.aisp_program must be the same-folder file aisp.aisop.json.")
    else:
        report.add("incomplete", "aisp.bridge_pointer_absent", "SKILL.md has no recognized metadata.aisp_program pointer.")


def preflight(selection: str | Path, allow_shared: bool = False) -> dict[str, Any]:
    raw = Path(selection).expanduser().absolute()
    report = Report(raw, allow_shared)
    if raw.is_symlink():
        report.add("error", "selection.symlink", "Selected root may not itself be a symlink.")
        return report.finish()
    try:
        target = raw.resolve(strict=True)
    except OSError as exc:
        report.add("error", "selection.missing", f"Selected path cannot be resolved: {exc}.")
        return report.finish()

    chosen = _selected_program(target, report)
    if chosen is None:
        return report.finish()
    program_path, package_root = chosen
    if not program_path.exists():
        report.add("error", "selection.program_missing", "Selected package does not contain aisp.aisop.json.")
        return report.finish()

    program = _read_json(program_path, package_root, MAX_PROGRAM_BYTES, report)
    if program is None:
        return report.finish()
    is_aisp = (
        program_path.name == "aisp.aisop.json"
        and package_root.name.endswith("_aisp")
    ) or (
        isinstance(program, list)
        and len(program) == 2
        and isinstance(program[0], dict)
        and isinstance(program[0].get("content"), dict)
        and str(program[0]["content"].get("protocol", "")).startswith("AISP")
    )
    if is_aisp:
        report.value["format"] = "AISP"
        report.value["version"] = "AISP V1.0.0"
        _contract_checks(program, package_root, report)
    else:
        report.value["format"] = "standalone AISOP"
        report.value["version"] = None
        report.checked("selected standalone AISOP file is readable JSON")
        report.add("incomplete", "aisop.standalone_limited", "Standalone AISOP is identified and parsed as JSON only; no AISP contract or package-layout requirements were applied.")
    return report.finish()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selection", help="explicit local *.aisop.json file or package directory")
    parser.add_argument(
        "--allow-shared",
        action="store_true",
        help="approve reads only from the selected package's sibling aisp/_shared directory",
    )
    args = parser.parse_args()
    report = preflight(args.selection, allow_shared=args.allow_shared)
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return {"PASS": 0, "INCOMPLETE": 2, "FAIL": 1}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
