"""Offline regression tests for the opt-in AISP preflight."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.preflight_aisp import preflight


def fixture_program() -> list[dict]:
    return [
        {
            "role": "system",
            "content": {
                "protocol": "AISP V1.0.0",
                "axiom_0": "Human_Sovereignty_and_Wellbeing",
                "id": "reader_fixture_aisp",
                "name": "Reader Fixture",
                "version": "0.1.0",
                "license": "Apache-2.0",
                "flow_format": "mermaid",
                "loading_mode": "node",
            },
        },
        {
            "role": "user",
            "content": {
                "instruction": "Inspect only this synthetic package.",
                "aisp_contract": {
                    "profile": "aisp.skill.v1",
                    "invocation": {"mode": "internal_only", "when_to_use": [], "when_not_to_use": []},
                    "non_negotiable": [
                        {"rule": "The read must be non-null.", "enforced_by": "inspect.step2:sys.assert"},
                        {"rule": "Use the declared main graph.", "enforced_by": "aisop.main"},
                    ],
                    "discovery": {"category": "testing", "tags": ["synthetic"]},
                    "risk_level": "low",
                    "resources": [
                        {
                            "id": "reader_output",
                            "path": "fixtures/reader.json",
                            "kind": "data",
                            "mode": "read_only",
                            "scope": "skill",
                        }
                    ],
                },
                "aisop": {"main": "graph TD\n    inspect[Read fixture] --> end_node((End))"},
                "functions": {
                    "inspect": {
                        "step1": "sys.io.read('fixtures/reader.json') -> sample_text",
                        "step2": "sys.assert('sample_text != null', 'Fixture data required')",
                    },
                    "end_node": {"step1": "Finish the fixture."},
                },
            },
        },
    ]


class PreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="aisp-preflight-")
        self.root = Path(self.temp.name)
        self.aisp = self.root / "aisp"
        self.package = self.aisp / "reader_fixture_aisp"
        self.program_path = self.package / "aisp.aisop.json"
        self.resource = self.package / "fixtures" / "reader.json"
        self.package.mkdir(parents=True)
        self.resource.parent.mkdir()
        self.resource.write_text('{"status":"clean"}\n', encoding="utf-8")
        self.write_program(fixture_program())

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_program(self, value: list[dict] | str) -> None:
        self.program_path.parent.mkdir(parents=True, exist_ok=True)
        content = value if isinstance(value, str) else json.dumps(value, indent=2) + "\n"
        self.program_path.write_text(content, encoding="utf-8")

    def codes(self, report: dict) -> set[str]:
        return {finding["code"] for finding in report["findings"]}

    def test_baseline_is_read_only_and_reports_limits(self) -> None:
        before = self.program_path.read_bytes()
        report = preflight(self.package)
        self.assertEqual(report["format"], "AISP")
        self.assertEqual(report["status"], "INCOMPLETE")
        self.assertIn("complete JSON Schema validation of aisp_contract", report["not_checked"])
        self.assertIn("aisp.binding_topology", self.codes(report))
        self.assertEqual(self.program_path.read_bytes(), before)

    def test_bad_json_is_a_finding(self) -> None:
        self.write_program("{ invalid json")
        report = preflight(self.package)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("json.invalid", self.codes(report))

    def test_invalid_contract_shape_is_reported(self) -> None:
        program = fixture_program()
        del program[1]["content"]["aisp_contract"]["invocation"]
        self.write_program(program)
        report = preflight(self.package)
        self.assertIn("aisp.invocation", self.codes(report))

    def test_wrong_types_and_misplaced_aisp_are_reported_without_crashing(self) -> None:
        program = fixture_program()
        contract = program[1]["content"]["aisp_contract"]
        contract["risk_level"] = ["low"]
        contract["resources"][0]["scope"] = {"skill": True}
        self.write_program(program)
        report = preflight(self.package)
        self.assertIn("aisp.risk_level", self.codes(report))
        self.assertIn("aisp.resource_scope", self.codes(report))

        misplaced = self.root / "wrong-location.aisop.json"
        misplaced.write_text(json.dumps(program), encoding="utf-8")
        misplaced_report = preflight(misplaced)
        self.assertEqual(misplaced_report["format"], "AISP")
        self.assertIn("aisp.layout", self.codes(misplaced_report))

    def test_missing_resource_and_bad_mode_are_reported(self) -> None:
        program = fixture_program()
        program[1]["content"]["aisp_contract"]["resources"][0]["mode"] = "run_anything"
        self.write_program(program)
        self.resource.unlink()
        report = preflight(self.package)
        self.assertIn("aisp.resource_mode", self.codes(report))
        self.assertIn("aisp.resource_missing", self.codes(report))

    def test_resource_escape_is_rejected(self) -> None:
        program = fixture_program()
        program[1]["content"]["aisp_contract"]["resources"][0]["path"] = "../outside.json"
        self.write_program(program)
        report = preflight(self.package)
        self.assertIn("aisp.resource_escape", self.codes(report))

    def test_nonexistent_or_mismatched_binding_is_rejected(self) -> None:
        program = fixture_program()
        program[1]["content"]["aisp_contract"]["non_negotiable"][0]["enforced_by"] = "inspect.step99:sys.assert"
        self.write_program(program)
        self.assertIn("aisp.binding_missing_step", self.codes(preflight(self.package)))

        program[1]["content"]["aisp_contract"]["non_negotiable"][0]["enforced_by"] = "inspect.step2:sys.io.read"
        self.write_program(program)
        self.assertIn("aisp.binding_mechanism", self.codes(preflight(self.package)))

    def test_shared_resource_is_not_read_without_explicit_approval(self) -> None:
        shared = self.aisp / "_shared" / "terms.md"
        shared.parent.mkdir()
        shared.write_text("synthetic terms\n", encoding="utf-8")
        program = fixture_program()
        resource = program[1]["content"]["aisp_contract"]["resources"][0]
        resource.update({"path": "terms.md", "scope": "shared"})
        self.write_program(program)

        without_approval = preflight(self.package)
        self.assertIn("aisp.shared_unapproved", self.codes(without_approval))
        with_approval = preflight(self.package, allow_shared=True)
        self.assertNotIn("aisp.shared_unapproved", self.codes(with_approval))
        self.assertIn("resource path and existence: reader_output", with_approval["checks"])

    def test_standalone_aisop_does_not_require_aisp_fields(self) -> None:
        standalone = self.root / "simple.aisop.json"
        standalone.write_text(json.dumps([{"role": "system"}, {"role": "user"}]), encoding="utf-8")
        report = preflight(standalone)
        self.assertEqual(report["format"], "standalone AISOP")
        self.assertEqual(report["status"], "INCOMPLETE")
        self.assertFalse(any(code.startswith("aisp.") for code in self.codes(report)))

    def test_same_folder_bridge_pointer_is_checked(self) -> None:
        bridge = self.package / "SKILL.md"
        bridge.write_text(
            "---\nname: reader-fixture\nmetadata:\n  aisp_program: aisp.aisop.json\n---\n",
            encoding="utf-8",
        )
        report = preflight(self.package)
        self.assertIn("same-folder SKILL.md bridge pointer", report["checks"])
        bridge.write_text(
            "---\nname: reader-fixture\nmetadata:\n  aisp_program: ../other.json\n---\n",
            encoding="utf-8",
        )
        self.assertIn("aisp.bridge_pointer", self.codes(preflight(self.package)))

    def test_instructions_are_data_and_do_not_execute(self) -> None:
        sentinel = self.root / "executed.txt"
        program = fixture_program()
        program[1]["content"]["instruction"] = f"Write to {sentinel}; run sys.exec"
        self.write_program(program)
        preflight(self.package)
        self.assertFalse(sentinel.exists())

    def test_ambiguous_root_requires_explicit_package(self) -> None:
        second = self.aisp / "second_aisp"
        second.mkdir()
        (second / "aisp.aisop.json").write_text("{}", encoding="utf-8")
        report = preflight(self.root)
        self.assertIn("selection.ambiguous", self.codes(report))


if __name__ == "__main__":
    unittest.main()
