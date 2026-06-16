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


def load_module(name: str):
    path = SCRIPT_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_BASE_DATA = {
    "FUND_NAME": "Test Growth Fund",
    "TICKER": "TEST",
    "STAR_RATING": 4,
    "TURNOVER_RATIO": 35.2,
    "MONTHLY_RETURNS_JSON": [
        {"date": "2024-01-31", "fund_return": 1.23, "benchmark_return": 1.10},
        {"date": "2024-02-29", "fund_return": -0.50, "benchmark_return": -0.40},
    ],
    "RISK_DATA_JSON": {
        "fund": {
            "sharpe": [0.82, 0.91, 0.76, 0.88],
            "upside": [112.3, 108.5, 105.2, 107.1],
            "downside": [95.4, 88.2, 91.0, 89.5],
            "stddev": [None, 14.20, 15.10, 13.80],
            "alpha": [None, 1.25, 0.85, None],
            "beta": [None, 0.94, 0.96, 0.98],
            "rsquared": [None, 92.10, 91.40, None],
        },
        "benchmark": {"stddev": [None, 15.00, 16.20, 14.30]},
    },
}


class RenderReportTests(unittest.TestCase):
    def test_render_report_writes_html(self):
        render = load_render_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.html"
            result_path = render.render_report(
                _BASE_DATA,
                output_path,
            )

            html = result_path.read_text(encoding="utf-8")
            self.assertIn("Test Growth Fund", html)
            self.assertIn("TEST", html)

    def test_list_placeholders_does_not_require_data_file(self):
        completed = subprocess.run(
            [sys.executable, str(RENDER_PATH), "--list-placeholders"],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Available placeholders", completed.stdout)


if __name__ == "__main__":
    unittest.main()


class ToNumberTests(unittest.TestCase):
    """Tests for the shared to_number utility in utils.py."""

    def setUp(self):
        self.utils = load_module("utils")

    def _n(self, v):
        return self.utils.to_number(v)

    def test_int_and_float_passthrough(self):
        self.assertEqual(self._n(1), 1.0)
        self.assertEqual(self._n(3.14), 3.14)

    def test_numeric_string(self):
        self.assertEqual(self._n("1.23"), 1.23)

    def test_percent_string_stripped(self):
        self.assertEqual(self._n("65.2%"), 65.2)

    def test_comma_formatted_string(self):
        self.assertEqual(self._n("1,234.56"), 1234.56)

    def test_sentinel_strings_return_none(self):
        for s in ("", "--", "-", "N/A", "n/a", "none", "null", "not returned"):
            self.assertIsNone(self._n(s), msg=f"expected None for {s!r}")

    def test_bool_returns_none(self):
        self.assertIsNone(self._n(True))
        self.assertIsNone(self._n(False))

    def test_none_returns_none(self):
        self.assertIsNone(self._n(None))

    def test_non_numeric_string_returns_none(self):
        self.assertIsNone(self._n("Large Blend"))


class CumulativeReturnsTests(unittest.TestCase):
    """Tests for _compute_cumulative_returns in render.py."""

    def setUp(self):
        self.render = load_render_module()

    def test_empty_input_returns_empty(self):
        self.assertEqual(self.render._compute_cumulative_returns([]), [])

    def test_single_month_positive_return(self):
        result = self.render._compute_cumulative_returns(
            [
                {"date": "2024-01-31", "fund_return": 10.0},
            ]
        )
        # Base row + 1 data row
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[1]["fund"], 11000.0)

    def test_benchmark_present_in_output_when_supplied(self):
        result = self.render._compute_cumulative_returns(
            [
                {"date": "2024-01-31", "fund_return": 1.0, "benchmark_return": 0.5},
            ]
        )
        self.assertIn("benchmark", result[0])
        self.assertIn("benchmark", result[1])

    def test_benchmark_absent_when_all_null(self):
        result = self.render._compute_cumulative_returns(
            [
                {"date": "2024-01-31", "fund_return": 1.0, "benchmark_return": None},
            ]
        )
        self.assertNotIn("benchmark", result[0])

    def test_rows_sorted_by_date(self):
        result = self.render._compute_cumulative_returns(
            [
                {"date": "2024-02-29", "fund_return": -1.0},
                {"date": "2024-01-31", "fund_return": 2.0},
            ]
        )
        dates = [r["date"] for r in result[1:]]
        self.assertEqual(dates, sorted(dates))

    def test_base_row_shares_date_with_first_entry(self):
        result = self.render._compute_cumulative_returns(
            [
                {"date": "2024-01-31", "fund_return": 0.0},
            ]
        )
        self.assertEqual(result[0]["date"], "2024-01-31")


class BenchmarkCurrencyGateTests(unittest.TestCase):
    """Tests for _apply_benchmark_currency_gate in render.py."""

    def setUp(self):
        self.render = load_render_module()

    def test_no_op_when_mismatch_false(self):
        data = {
            "MONTHLY_RETURNS_JSON": [
                {"date": "2024-01-31", "fund_return": 1.0, "benchmark_return": 0.5}
            ]
        }
        self.render._apply_benchmark_currency_gate(data)
        self.assertEqual(data["MONTHLY_RETURNS_JSON"][0]["benchmark_return"], 0.5)

    def test_nulls_benchmark_return_when_mismatch_true(self):
        data = {
            "BENCHMARK_CURRENCY_MISMATCH": True,
            "MONTHLY_RETURNS_JSON": [
                {"date": "2024-01-31", "fund_return": 1.0, "benchmark_return": 0.5}
            ],
        }
        self.render._apply_benchmark_currency_gate(data)
        self.assertIsNone(data["MONTHLY_RETURNS_JSON"][0]["benchmark_return"])

    def test_fund_return_preserved_when_mismatch_true(self):
        data = {
            "BENCHMARK_CURRENCY_MISMATCH": True,
            "MONTHLY_RETURNS_JSON": [
                {"date": "2024-01-31", "fund_return": 2.5, "benchmark_return": 1.0}
            ],
        }
        self.render._apply_benchmark_currency_gate(data)
        self.assertEqual(data["MONTHLY_RETURNS_JSON"][0]["fund_return"], 2.5)

    def test_string_true_triggers_gate(self):
        data = {
            "BENCHMARK_CURRENCY_MISMATCH": "true",
            "MONTHLY_RETURNS_JSON": [
                {"date": "2024-01-31", "fund_return": 1.0, "benchmark_return": 0.5}
            ],
        }
        self.render._apply_benchmark_currency_gate(data)
        self.assertIsNone(data["MONTHLY_RETURNS_JSON"][0]["benchmark_return"])

    def test_string_false_does_not_trigger_gate(self):
        data = {
            "BENCHMARK_CURRENCY_MISMATCH": "false",
            "MONTHLY_RETURNS_JSON": [
                {"date": "2024-01-31", "fund_return": 1.0, "benchmark_return": 0.5}
            ],
        }
        self.render._apply_benchmark_currency_gate(data)
        self.assertEqual(data["MONTHLY_RETURNS_JSON"][0]["benchmark_return"], 0.5)


if __name__ == "__main__":
    unittest.main()
