#!/usr/bin/env python3
"""Regression checks: python test_extract_numbers.py  (no framework, no fixtures).

Each check pins ONE behaviour and fails on its own if that behaviour regresses.
"""
import importlib.util
import pathlib
import sys

here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("extract_numbers", here / "extract_numbers.py")
en = importlib.util.module_from_spec(spec)
spec.loader.exec_module(en)


def categories(text):
    return {n.value: n.category for n in en.extract_numbers(text)}


def flagged(text):
    """Pairs of values reported as inconsistent, as a set of frozensets."""
    out = set()
    for inc in en.find_inconsistencies(en.extract_numbers(text)):
        out.add(frozenset((inc["expected"]["value"], inc["found"]["value"])))
    return out


failures = []


def check(name, cond, detail=""):
    if not cond:
        failures.append(f"{name}: {detail}")


# 1. Tolerance. $500M vs $485M is 3% apart — two figures meant to be the same
#    number. A 5% window swallows it; 1% reports it.
deck = """## Slide 3
FY2025 revenue of $500M.

## Slide 8
Revenue reached $500MM in fiscal 2025.

## Slide 15
Revenue of $485M for FY2025.
"""
check("tolerance", frozenset(("$500M", "$485M")) in flagged(deck), flagged(deck))

# 2. Unit decides the category before context keywords: a percentage on a line
#    that says "revenue" is growth, not a revenue figure.
cats = categories("## Slide 1\nRevenue growth of 42% YoY on $500M of revenue.\n")
check("unit-first category", cats.get("42%") == "growth", cats)
check("unit-first keeps money", cats.get("$500M") == "revenue", cats)

# 3. A currency symbol glued to a ratio unit ("$22%" -> USD_%) must still read
#    as a ratio, not as money.
cats = categories("## Slide 1\nRevenue growth was $22% this year.\n")
check("currency-prefixed ratio", cats.get("$22%") == "growth", cats)

# 4. Grouping is by dimension, not by raw unit: the same figure written "$500M"
#    and "485M" must still be compared with each other.
deck = """## Slide 1
FY2025 revenue of $500M.

## Slide 2
Revenue reached 485M in fiscal 2025.
"""
check("dimension grouping", frozenset(("$500M", "485M")) in flagged(deck), flagged(deck))

# 5. Ratios and multiples are never compared against dollar figures.
deck = """## Slide 1
Revenue of $500M, EBITDA margin of 22%, trading at 12.0x revenue.
"""
pairs = flagged(deck)
check("no unit crossing", all("$500M" not in p or len(p - {"$500M"}) == 0 for p in pairs), pairs)

# 6. "bps" is not a magnitude — its "b" must not be read as billions.
bps = [n for n in en.extract_numbers("## Slide 1\nMargin improved 500bps.\n") if n.unit == "bps"]
check("bps not billions", bps and bps[0].normalized == 500, [n.normalized for n in bps])

if failures:
    print("FAIL")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("PASS")
