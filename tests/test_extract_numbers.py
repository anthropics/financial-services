import importlib.util
from pathlib import Path

MODULE = (
    Path(__file__).resolve().parents[1]
    / "plugins/vertical-plugins/financial-analysis/skills/ib-check-deck/scripts/extract_numbers.py"
)
spec = importlib.util.spec_from_file_location("extract_numbers", MODULE)
extract_numbers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extract_numbers)


def test_basis_points_are_not_scaled_as_billions():
    assert extract_numbers.normalize_number("150", "bps") == 150.0
    assert extract_numbers.normalize_number("25.5", "bps") == 25.5


def test_real_multipliers_still_apply():
    assert extract_numbers.normalize_number("1.5", "B") == 1.5e9
    assert extract_numbers.normalize_number("500", "M") == 500e6
