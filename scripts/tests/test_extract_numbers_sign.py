"""Signed financial figures must retain their sign without changing ranges."""
import importlib.util
from pathlib import Path
import sys
import unittest

SOURCE = Path(__file__).resolve().parents[2] / "plugins/vertical-plugins/financial-analysis/skills/ib-check-deck/scripts/extract_numbers.py"
spec = importlib.util.spec_from_file_location("signed_deck_numbers", SOURCE)
numbers = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = numbers
spec.loader.exec_module(numbers)


class SignedFigureTests(unittest.TestCase):
    def test_negative_amounts(self):
        for text in ["-$20M", "$-20M", "-20M", "-$20 million"]:
            with self.subTest(text=text):
                figures = numbers.extract_numbers("## Slide 2\nEBITDA was " + text + ".")
                self.assertEqual(len(figures), 1)
                self.assertEqual(figures[0].normalized, -20_000_000)
                self.assertIn("-", figures[0].value)
                self.assertEqual(figures[0].slide, 2)

    def test_negative_decimal_percentage_and_other_currency(self):
        for text, expected in [("-$1,234.50", -1234.5), ("-25.5%", -25.5), ("-€20M", -20_000_000), ("£-20M", -20_000_000)]:
            with self.subTest(text=text):
                figures = numbers.extract_numbers("Reported " + text + ".")
                self.assertEqual(len(figures), 1)
                self.assertEqual(figures[0].normalized, expected)

    def test_opposite_signs_are_not_the_same_figure(self):
        text = "## Slide 1\nEBITDA was -$20M.\n## Slide 2\nEBITDA was $20M.\n"
        findings = numbers.find_inconsistencies(numbers.extract_numbers(text))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "high")

    def test_positive_ranges_keep_positive_endpoints(self):
        for text in ["$10M-$20M", "$10M - $20M", "10M-20M", "10M - 20M"]:
            with self.subTest(text=text):
                figures = numbers.extract_numbers("Revenue range " + text + ".")
                self.assertEqual([n.normalized for n in figures], [10_000_000, 20_000_000])

    def test_repeated_losses_are_consistent(self):
        text = "## Slide 1\nEBITDA was -$20M.\n## Slide 2\nEBITDA was $-20 million.\n"
        self.assertEqual(numbers.find_inconsistencies(numbers.extract_numbers(text)), [])

    def test_loss_comparisons_use_the_existing_tolerance(self):
        for second, count in [("-$20.8M", 0), ("-$21M", 1)]:
            with self.subTest(second=second):
                text = "## Slide 1\nEBITDA was -$20M.\n## Slide 2\nEBITDA was " + second + ".\n"
                self.assertEqual(len(numbers.find_inconsistencies(numbers.extract_numbers(text))), count)

    def test_separate_negative_figures_keep_both_signs(self):
        figures = numbers.extract_numbers("EBITDA: -$20M, -$30M.")
        self.assertEqual([n.normalized for n in figures], [-20_000_000, -30_000_000])


if __name__ == "__main__":
    unittest.main()
