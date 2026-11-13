"""A tiny registry that maps a region code (e.g. "US") to its implementation.

When EU/AU modules are added, they register themselves here and immediately
become available to every tool — no other code changes.
"""
from __future__ import annotations

from .base import Region

_REGIONS: dict[str, Region] = {}


def register(region: Region) -> None:
    _REGIONS[region.code.upper()] = region


def get_region(code: str = "US") -> Region:
    code = (code or "US").upper()
    if code not in _REGIONS:
        raise ValueError(
            f"Region '{code}' is not available. Registered regions: {sorted(_REGIONS) or '[none]'}"
        )
    return _REGIONS[code]


def available_regions() -> list[str]:
    return sorted(_REGIONS)
