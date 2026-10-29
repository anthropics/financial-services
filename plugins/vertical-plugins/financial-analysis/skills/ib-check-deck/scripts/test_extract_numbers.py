import pytest
from extract_numbers import normalize_number

def test_normalize_number_invalid_input():
    """Test that normalize_number handles un-parseable strings by returning 0.0."""
    assert normalize_number("invalid", "none") == 0.0
    assert normalize_number("", "none") == 0.0
    assert normalize_number("abc", "M") == 0.0

def test_normalize_number_happy_path():
    """Test normalize_number with valid inputs and various units."""
    # Basic numbers
    assert normalize_number("100", "") == 100.0
    assert normalize_number("100.5", "") == 100.5

    # Commas and spaces
    assert normalize_number("1,000", "") == 1000.0
    assert normalize_number("1 000", "") == 1000.0

    # Unit multipliers
    assert normalize_number("1", "M") == 1e6
    assert normalize_number("1", "million") == 1e6
    assert normalize_number("1", "B") == 1e9
    assert normalize_number("1", "bn") == 1e9
    assert normalize_number("1", "K") == 1e3
    assert normalize_number("1", "T") == 1e12

    # Mixed case and substrings
    assert normalize_number("1", "Million") == 1e6
    assert normalize_number("1", "USD_M") == 1e6
