"""Excel error cells must be distinguished from explanatory text."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
SOURCES = [
    ROOT / "plugins" / kind / plugin / "skills/dcf-model/scripts/validate_dcf.py"
    for kind, plugin in [
        ("vertical-plugins", "financial-analysis"),
        ("agent-plugins", "model-builder"),
        ("agent-plugins", "pitch-agent"),
    ]
]
ERRORS = ["#VALUE!", "#DIV/0!", "#REF!", "#NAME?", "#NULL!", "#NUM!", "#N/A"]


class FormulaErrorTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "model.xlsx"

    def save_cells(self, values, force_text=False):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "DCF"
        for row, value in enumerate(values, 1):
            cell = sheet.cell(row, 1, value)
            if force_text:
                cell.data_type = "s"
        workbook.save(self.path)
        workbook.close()

    def validators(self):
        for index, source in enumerate(SOURCES):
            spec = importlib.util.spec_from_file_location(f"dcf_errors_{index}", source)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            validator = module.DCFModelValidator(str(self.path))
            self.addCleanup(validator.workbook_formulas.close)
            self.addCleanup(validator.workbook_values.close)
            yield source, validator

    def test_notes_containing_error_names_are_not_errors(self):
        self.save_cells([f"Check for {error} before delivery" for error in ERRORS])
        for source, validator in self.validators():
            with self.subTest(source=source):
                details, count = validator.check_formula_errors()
                self.assertEqual(count, 0)
                self.assertEqual(validator.errors, [])
                self.assertTrue(all(not locations for locations in details.values()))

    def test_literal_text_error_names_are_not_error_cells(self):
        self.save_cells(ERRORS, force_text=True)
        for source, validator in self.validators():
            with self.subTest(source=source):
                self.assertEqual(validator.workbook_values["DCF"]["A1"].data_type, "s")
                self.assertEqual(validator.check_formula_errors()[1], 0)

    def test_real_excel_error_cells_keep_their_locations(self):
        self.save_cells(ERRORS)
        for source, validator in self.validators():
            with self.subTest(source=source):
                details, count = validator.check_formula_errors()
                self.assertEqual(count, len(ERRORS))
                for row, error in enumerate(ERRORS, 1):
                    self.assertEqual(details[error], [f"DCF!A{row}"])
                    self.assertIn(f"{error} at DCF!A{row}", validator.errors)

    def test_cached_formula_error_is_detected_and_formula_is_counted(self):
        self.save_cells(["=1/0", "Explain #DIV/0! here", 0, 42])
        # openpyxl does not calculate formulas. Supply an Excel-style error cache.
        with zipfile.ZipFile(self.path) as archive:
            entries = {name: archive.read(name) for name in archive.namelist()}
        namespace = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        sheet = ET.fromstring(entries["xl/worksheets/sheet1.xml"])
        cell = sheet.find(".//s:c[@r='A1']", namespace)
        cell.set("t", "e")
        cell.find("s:v", namespace).text = "#DIV/0!"
        entries["xl/worksheets/sheet1.xml"] = ET.tostring(sheet)
        with zipfile.ZipFile(self.path, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, contents in entries.items():
                archive.writestr(name, contents)
        for source, validator in self.validators():
            with self.subTest(source=source):
                details, count = validator.check_formula_errors()
                self.assertEqual(count, 1)
                self.assertEqual(details["#DIV/0!"], ["DCF!A1"])
                self.assertIn("Total formulas: 1", validator.info)


if __name__ == "__main__":
    unittest.main()
