"""Inline Morningstar rating icons into the fund summary template."""

import math
from pathlib import Path

_MEDALIST_ICON_MAP: dict[str, str] = {
    "Gold": "Gold-Lrg.svg",
    "Silver": "Silver-Lrg.svg",
    "Bronze": "Bronze-Lrg.svg",
    "Neutral": "Neutral-Lrg.svg",
    "Negative": "Negative-Lrg.svg",
    "Not Rated": "NR-Lrg.svg",
    "NR": "NR-Lrg.svg",
    "Under Review": "UR-Lrg.svg",
    "UR": "UR-Lrg.svg",
}

_PILLAR_SCALE_LABELS = ["Low", "Below Average", "Average", "Above Average", "High"]

_PILLAR_ICON_LABEL_MAP: dict[str, str] = {
    "High": "High",
    "Above Average": "Above Avg",
    "Above Avg": "Above Avg",
    "Average": "Average",
    "Below Average": "Below Avg",
    "Below Avg": "Below Avg",
    "Low": "Low",
}

_PILLAR_DISPLAY_LABEL_MAP: dict[str, str] = {
    "High": "High",
    "Above Average": "Above Average",
    "Above Avg": "Above Average",
    "Average": "Average",
    "Below Average": "Below Average",
    "Below Avg": "Below Average",
    "Low": "Low",
}

_PILLAR_SCALE_CLASS_MAP: dict[str, str] = {
    "High": "high",
    "Above Average": "above-average",
    "Average": "average",
    "Below Average": "below-average",
    "Low": "low",
}


def _parse_star_rating(data: dict) -> int | None:
    """Return a 1-5 Morningstar rating from numeric or display inputs."""
    raw_rating = data.get("STAR_RATING")
    if raw_rating is not None:
        try:
            rating = int(float(str(raw_rating).strip()))
            return max(1, min(5, rating))
        except (ValueError, TypeError):
            pass

    display = str(data.get("STAR_RATING_DISPLAY", ""))
    filled = display.count("★")
    return max(1, min(5, filled)) if filled else None


def _parse_score(value) -> float | None:
    """Parse a 0-100 score from report data."""
    try:
        score = float(str(value).strip().rstrip("%"))
    except (ValueError, TypeError):
        return None
    return max(0, min(100, score))


def _build_mprs_visual(score_value, icons_path: Path) -> str:
    """Inline the MPRS dial and add a score label plus pointer marker."""
    base_svg = _load_svg(icons_path / "MPRS.svg")
    score = _parse_score(score_value)
    if score is None:
        return '<span class="value-lg">--</span>'
    if not base_svg:
        score_text = str(int(score)) if score.is_integer() else f"{score:.1f}"
        return f'<span class="value-lg">{score_text}</span>'

    angle = math.radians(135 + score * 2.7)
    center_x = 150
    center_y = 150
    tip_radius = 78
    base_radius = 61
    half_width = 7
    ux = math.cos(angle)
    uy = math.sin(angle)
    tx = -uy
    ty = ux

    tip = (center_x + ux * tip_radius, center_y + uy * tip_radius)
    base_center = (center_x + ux * base_radius, center_y + uy * base_radius)
    base_a = (base_center[0] + tx * half_width, base_center[1] + ty * half_width)
    base_b = (base_center[0] - tx * half_width, base_center[1] - ty * half_width)
    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in (tip, base_a, base_b))
    score_text = str(int(score)) if score.is_integer() else f"{score:.1f}"
    overlay = (
        f'<g class="mprs-overlay">'
        f'<polygon points="{points}" fill="#3D3B39" stroke="#FFFFFF" stroke-width="1.5" />'
        f'<text x="150" y="159" text-anchor="middle" fill="#6F6D6A" '
        f'font-family="MORN Intrinsic,Aptos,Calibri,sans-serif" font-size="52" font-weight="300">{score_text}</text>'
        f'</g>'
    )
    return base_svg.replace("</svg>", overlay + "</svg>")


def _load_svg(path: Path) -> str:
    """Return the raw SVG XML content of *path*, or empty string if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _parse_pillar(rating_raw: str, score_type_raw: str) -> tuple[str, str]:
    """
    Parse a pillar rating value and its score type into (label, icon_type).

    Analyst-driven pillars return a plain label (e.g. "High", "Above Average").
    Quant-driven pillars append ^Q to the label (e.g. "Below Average^Q").
    The suffix is stripped before the label lookup.

    Resolution:
    - ^Q suffix present        → Quant
    - Score Type "Quantitative" → Quant
    - No suffix / "Not returned" / anything else → Analyst
    """
    rating = rating_raw.strip()
    if rating.endswith("^Q"):
        return rating[:-2].strip(), "Quant"

    score_type = score_type_raw.strip().lower()
    icon_type = "Quant" if "quantitative" in score_type else "Analyst"
    return rating, icon_type


def _build_pillar_score_scale(rating_raw: str, allow_unmatched: bool = True) -> str:
    """Build a compact five-segment pillar score scale for a normalized rating."""
    rating = rating_raw.strip()
    if rating.endswith("^Q"):
        rating = rating[:-2].strip()
    active_label = _PILLAR_DISPLAY_LABEL_MAP.get(rating, "")
    if not active_label and not allow_unmatched:
        return ""
    points = []
    for label in _PILLAR_SCALE_LABELS:
        active_class = " is-active" if label == active_label else ""
        rating_class = f" is-{_PILLAR_SCALE_CLASS_MAP[label]}" if label == active_label else ""
        points.append(
            f'<span class="pillar-scale-point{active_class}{rating_class}">'
            f'<span class="pillar-scale-segment"></span>'
            f'<span class="pillar-scale-label">{label}</span>'
            f'</span>'
        )
    return '<div class="pillar-score-scale"><div class="pillar-scale-track">' + "".join(points) + "</div></div>"


def embed_icons(template: str, data: dict, icons_path: Path) -> str:
    """
    Replace rating icon placeholders with inline SVG selected from report data.

    Process, People, and Parent pillar scores are represented by Morningstar
    SVG score icons plus compact score scales. Price keeps its numeric MMRGS
    value because it is not a qualitative pillar label in the normal data path.
    """
    medalist = str(data.get("MEDALIST_RATING", "")).strip()
    icon_file = _MEDALIST_ICON_MAP.get(medalist, "")
    template = template.replace("{{MEDALIST_ICON}}", _load_svg(icons_path / icon_file) if icon_file else "")

    star_rating = _parse_star_rating(data)
    star_icon = _load_svg(icons_path / f"{star_rating} Star.svg") if star_rating else ""
    template = template.replace("{{STAR_RATING_ICON}}", star_icon)
    template = template.replace("{{MPRS_VISUAL}}", _build_mprs_visual(data.get("MPRS"), icons_path))

    for data_key, score_type_key, icon_placeholder, scale_placeholder in (
        ("PROCESS_RATING", "PROCESS_SCORE_TYPE", "PROCESS_ICON", "PROCESS_SCORE_SCALE"),
        ("PEOPLE_RATING", "PEOPLE_SCORE_TYPE", "PEOPLE_ICON", "PEOPLE_SCORE_SCALE"),
        ("PARENT_RATING", "PARENT_SCORE_TYPE", "PARENT_ICON", "PARENT_SCORE_SCALE"),
    ):
        score_type_raw = str(data.get(score_type_key, ""))
        rating, icon_type = _parse_pillar(str(data.get(data_key, "")), score_type_raw)
        icon_label = _PILLAR_ICON_LABEL_MAP.get(rating, "")
        pillar_svg = _load_svg(icons_path / f"{icon_label} {icon_type}.svg") if icon_label else ""
        template = template.replace("{{" + icon_placeholder + "}}", pillar_svg)
        template = template.replace("{{" + scale_placeholder + "}}", _build_pillar_score_scale(rating))

    price_raw = str(data.get("PRICE_RATING", "")).strip()
    try:
        price_num = float(price_raw)
        price_display = str(int(price_num)) if price_num.is_integer() else f"{price_num:.1f}"
    except (ValueError, TypeError):
        price_display = price_raw
    price_html = f'<span class="price-score-num">{price_display}</span>' if price_display else ""
    template = template.replace("{{PRICE_SCORE}}", price_html)
    template = template.replace("{{PRICE_SCORE_SCALE}}", _build_pillar_score_scale(price_raw, allow_unmatched=False))

    return template