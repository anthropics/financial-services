import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
RENDER_PATH = SCRIPT_DIR / "render.py"


def load_render_module():
    spec = importlib.util.spec_from_file_location("morningstar_render", RENDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RenderReportTests(unittest.TestCase):
    def test_render_report_writes_html(self):
        render = load_render_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.html"
            result_path = render.render_report(
                {
                    "FUND_NAME": "Test Growth Fund",
                    "TICKER": "TEST",
                    "STAR_RATING": 4,
                },
                output_path,
                export_pdf=False,
            )

            html = result_path.read_text(encoding="utf-8")
            self.assertIn("Test Growth Fund", html)
            self.assertIn("TEST", html)
            self.assertNotIn("export-pdf", html)
            self.assertNotIn("Save PDF", html)

    def test_render_report_exports_pdf_by_default(self):
        render = load_render_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.html"
            calls = []

            def fake_export_pdf(html_path, pdf_output_path=None):
                calls.append((html_path, pdf_output_path))
                pdf_path = render.default_pdf_path(html_path)
                pdf_path.write_bytes(b"%PDF-1.7\n")
                return pdf_path

            render._export_pdf_copy = fake_export_pdf
            result_path = render.render_report(
                {
                    "FUND_NAME": "Test Growth Fund",
                    "TICKER": "TEST",
                    "STAR_RATING": 4,
                },
                output_path,
            )

            self.assertEqual(calls, [(result_path, None)])
            self.assertTrue(result_path.with_suffix(".pdf").exists())

    def test_render_report_keeps_html_when_pdf_export_fails(self):
        render = load_render_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.html"

            def fail_export_pdf(html_path, pdf_output_path=None):
                raise RuntimeError("No browser available")

            render._export_pdf_copy = fail_export_pdf
            result_path = render.render_report(
                {
                    "FUND_NAME": "Test Growth Fund",
                    "TICKER": "TEST",
                    "STAR_RATING": 4,
                },
                output_path,
            )

            self.assertTrue(result_path.exists())
            self.assertFalse(result_path.with_suffix(".pdf").exists())

    def test_render_report_can_require_pdf(self):
        render = load_render_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.html"

            def fail_export_pdf(html_path, pdf_output_path=None):
                raise RuntimeError("No browser available")

            render._export_pdf_copy = fail_export_pdf
            with self.assertRaisesRegex(RuntimeError, "No browser available"):
                render.render_report(
                    {
                        "FUND_NAME": "Test Growth Fund",
                        "TICKER": "TEST",
                        "STAR_RATING": 4,
                    },
                    output_path,
                    require_pdf=True,
                )

    def test_list_placeholders_does_not_require_data_file(self):
        completed = subprocess.run(
            [sys.executable, str(RENDER_PATH), "--list-placeholders"],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Available placeholders", completed.stdout)

    def test_export_helper_has_cli_help(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "export_report.py"), "--help"],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--format", completed.stdout)


if __name__ == "__main__":
    unittest.main()
