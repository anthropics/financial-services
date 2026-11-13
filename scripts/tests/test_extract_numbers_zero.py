"""Regression tests for repeated zero figures in deck consistency checks.

Run from the repository root:
    python3 -m unittest discover -s scripts/tests -p 'test_extract_numbers_zero.py' -v
"""
import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "plugins/vertical-plugins/financial-analysis/skills/ib-check-deck/scripts/extract_numbers.py"
spec = importlib.util.spec_from_file_location("deck_numbers", SOURCE)
deck_numbers = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = deck_numbers
spec.loader.exec_module(deck_numbers)


def deck(first, second):
    return f"## Slide 1\nRevenue was {first}.\n## Slide 2\nRevenue was {second}.\n"


class ZeroFigureRegressionTests(unittest.TestCase):
    def test_repeated_zero_figures_are_consistent(self):
        for first, second in [("$0M", "$0M"), ("0M", "0.0M"), ("$0M", "$0 million")]:
            with self.subTest(first=first, second=second):
                figures = deck_numbers.extract_numbers(deck(first, second))
                self.assertEqual(len(figures), 2)
                self.assertEqual([figure.normalized for figure in figures], [0, 0])
                self.assertEqual([figure.slide for figure in figures], [1, 2])
                self.assertEqual(deck_numbers.find_inconsistencies(figures), [])

    def test_zero_and_nonzero_are_inconsistent_in_either_order(self):
        for first, second in [("$0M", "$10M"), ("$10M", "$0M")]:
            with self.subTest(first=first, second=second):
                findings = deck_numbers.find_inconsistencies(deck_numbers.extract_numbers(deck(first, second)))
                self.assertEqual(len(findings), 1)
                self.assertEqual(findings[0]["severity"], "high")
                self.assertEqual({findings[0]["expected"]["value"], findings[0]["found"]["value"]}, {"$0M", "$10M"})

    def test_repeated_zero_group_keeps_a_real_contradiction(self):
        text = deck("$0M", "$0M") + "## Slide 3\nRevenue was $10M.\n"
        findings = deck_numbers.find_inconsistencies(deck_numbers.extract_numbers(text))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["expected"], {"value": "$0M", "slides": [1, 2], "count": 2})
        self.assertEqual(findings[0]["found"], {"value": "$10M", "slides": [3], "count": 1})

    def test_positive_figure_comparisons_still_detect_real_differences(self):
        for first, second, count in [("$100M", "$100M", 0), ("$100M", "$100 million", 0), ("$100M", "$110M", 1)]:
            with self.subTest(first=first, second=second):
                findings = deck_numbers.find_inconsistencies(deck_numbers.extract_numbers(deck(first, second)))
                self.assertEqual(len(findings), count)

if __name__ == "__main__":
    unittest.main()
