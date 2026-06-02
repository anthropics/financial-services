"""
SVG chart builders for fund summary reports.

The renderer passes parsed chart data into these functions and receives inline
SVG markup that can be substituted directly into the HTML template.
"""

import math
from datetime import datetime

# Chart color constants matching template CSS variables.
_C_FUND = "#2364B9"
_C_BENCH = "#B2013C"
_C_GRID = "#DAD9D8"
_C_TEXT = "#7F7D7A"
_C_BODY = "#3D3B39"
_C_AXIS = "#A6A4A1"
_ALLOC_COLORS = {
    "Equity": "#2364B9",
    "Fixed Income": "#F47206",
    "Bond": "#F47206",
    "Alternative": "#B2013C",
    "Cash": "#039649",
    "Other": "#F5C72C",
    "Not Classified": "#ECEBEA",
}


def _escape_xml(text: str) -> str:
    """Escape text for safe embedding in SVG/XML."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _format_growth_date(value) -> str:
    """Format month labels as abbreviated month plus two-digit year."""
    text = str(value)
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            return datetime.strptime(text, fmt).strftime("%b %y")
        except ValueError:
            continue
    return text


def _nice_ceiling(value: float) -> float:
    """Return a clean chart-axis ceiling greater than or equal to value."""
    if value <= 0:
        return 1
    exponent = 10 ** math.floor(math.log10(value))
    fraction = value / exponent
    for step in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if fraction <= step:
            return step * exponent
    return 10 * exponent


def build_line_chart_svg(data: list[dict]) -> str:
    """Build an inline SVG line chart from cumulative or calendar returns data.

    Accepts a list of dicts with keys:
    - 'date' or 'year' (label)
    - 'fund' (number)
    - 'benchmark' (number, optional)

    Returns SVG markup string.
    """
    if not data:
        return (
            '<div class="chart-wrap" '
            'style="display:flex;align-items:center;justify-content:center;'
            'color:#7F7D7A;font-size:12px;">No return data available</div>'
        )

    is_growth = "date" in data[0]
    label_key = "date" if is_growth else "year"

    w, h = 700, 248
    pad_top, pad_right, pad_bottom, pad_left = 12, 12, 32, 72 if is_growth else 54
    plot_w = w - pad_left - pad_right
    plot_h = h - pad_top - pad_bottom

    all_vals = []
    for item in data:
        if isinstance(item.get("fund"), (int, float)):
            all_vals.append(item["fund"])
        if isinstance(item.get("benchmark"), (int, float)):
            all_vals.append(item["benchmark"])
    if not all_vals:
        return ""

    y_min_raw, y_max_raw = min(all_vals), max(all_vals)
    if y_min_raw >= 0:
        y_min = 0
        y_max = _nice_ceiling(y_max_raw)
    else:
        y_pad = (y_max_raw - y_min_raw or abs(y_max_raw) or 1) * 0.08
        y_min = y_min_raw - y_pad
        y_max = y_max_raw + y_pad

    n = len(data)

    def x_for(index: int) -> float:
        if n == 1:
            return pad_left + plot_w / 2
        return pad_left + (index / (n - 1)) * plot_w

    def y_for(value: float) -> float:
        return pad_top + (1 - (value - y_min) / (y_max - y_min)) * plot_h

    def fmt_val(value: float) -> str:
        if is_growth:
            return f"{value:,.2f}"
        return f"{value:.2f}"

    def label_for(item: dict) -> str:
        value = item[label_key]
        return _format_growth_date(value) if is_growth else str(value)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'style="width:100%;height:auto;max-height:320px;" '
        f'font-family="MORN Intrinsic,Aptos,Calibri,sans-serif">'
        '<defs>'
        '<filter id="tip-shadow" x="-20%" y="-20%" width="140%" height="140%">'
        '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#3D3B39" flood-opacity="0.14"/>'
        '</filter>'
        '</defs>'
    ]

    tick_count = 5
    for index in range(tick_count):
        tick_val = y_min + (y_max - y_min) * index / (tick_count - 1)
        y = y_for(tick_val)
        is_zero = abs(tick_val) < 0.000001
        grid_style = f'stroke="{_C_AXIS if is_zero else _C_GRID}"'
        if not is_zero:
            grid_style += ' stroke-dasharray="2,4"'
        parts.append(
            f'<line x1="{pad_left}" y1="{y:.1f}" x2="{w - pad_right}" y2="{y:.1f}" '
            f'{grid_style} />'
        )
        parts.append(
            f'<text x="{pad_left - 8}" y="{y:.1f}" text-anchor="end" '
            f'dominant-baseline="middle" fill="{_C_BODY}" font-size="11">'
            f'{_escape_xml(fmt_val(tick_val))}</text>'
        )

    parts.append(
        f'<line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{pad_top + plot_h}" '
        f'stroke="{_C_AXIS}" stroke-width="1" />'
    )

    if is_growth:
        label_cy = pad_top + plot_h / 2
        parts.append(
            f'<text transform="rotate(-90)" x="{-label_cy:.1f}" y="12" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'fill="{_C_BODY}" font-size="10">Growth of 10,000</text>'
        )

    max_labels = min(8, n)
    label_every = max(1, math.ceil(n / max_labels))
    for index, item in enumerate(data):
        if index % label_every != 0 and index != n - 1:
            continue
        parts.append(
            f'<text x="{x_for(index):.1f}" y="{h - 12}" text-anchor="middle" '
            f'fill="{_C_BODY}" font-size="11">{_escape_xml(label_for(item))}</text>'
        )

    for index in range(n - 1):
        first, second = data[index], data[index + 1]
        first_fund, second_fund = first.get("fund"), second.get("fund")
        first_bench, second_bench = first.get("benchmark"), second.get("benchmark")
        if not all(isinstance(value, (int, float)) for value in [first_fund, second_fund, first_bench, second_bench]):
            continue
        above = (first_fund + second_fund) / 2 >= (first_bench + second_bench) / 2
        color = "rgba(3,150,73,0.10)" if above else "rgba(228,37,19,0.10)"
        path = (
            f'M{x_for(index):.1f},{y_for(first_fund):.1f} '
            f'L{x_for(index + 1):.1f},{y_for(second_fund):.1f} '
            f'L{x_for(index + 1):.1f},{y_for(second_bench):.1f} '
            f'L{x_for(index):.1f},{y_for(first_bench):.1f} Z'
        )
        parts.append(f'<path d="{path}" fill="{color}" />')

    fund_points = []
    for index, item in enumerate(data):
        if isinstance(item.get("fund"), (int, float)):
            fund_points.append(f"{x_for(index):.1f},{y_for(item['fund']):.1f}")
    if fund_points:
        parts.append(
            f'<polyline points="{" ".join(fund_points)}" '
            f'fill="none" stroke="{_C_FUND}" stroke-width="2.5" '
            f'stroke-linejoin="round" stroke-linecap="round" />'
        )

    bench_points = []
    for index, item in enumerate(data):
        if isinstance(item.get("benchmark"), (int, float)):
            bench_points.append(f"{x_for(index):.1f},{y_for(item['benchmark']):.1f}")
    if bench_points:
        parts.append(
            f'<polyline points="{" ".join(bench_points)}" '
            f'fill="none" stroke="{_C_BENCH}" stroke-width="2" '
            f'stroke-linejoin="round" stroke-linecap="round" />'
        )

    col_w = plot_w / max(n - 1, 1) if n > 1 else plot_w
    for index, item in enumerate(data):
        cx_pt = x_for(index)
        parts.append(f'<g class="chart-point" data-idx="{index}">')
        parts.append(
            f'<rect class="hover-target" x="{cx_pt - col_w / 2:.1f}" y="{pad_top}" '
            f'width="{col_w:.1f}" height="{plot_h}" fill="transparent" />'
        )
        parts.append(
            f'<line class="data-dot" x1="{cx_pt:.1f}" y1="{pad_top}" '
            f'x2="{cx_pt:.1f}" y2="{pad_top + plot_h}" '
            f'stroke="{_C_GRID}" stroke-dasharray="3,4" />'
        )
        for key, color in [("fund", _C_FUND), ("benchmark", _C_BENCH)]:
            if isinstance(item.get(key), (int, float)):
                cy_pt = y_for(item[key])
                parts.append(
                    f'<circle class="data-dot" cx="{cx_pt:.1f}" cy="{cy_pt:.1f}" '
                    f'r="4" fill="{color}" stroke="#fff" stroke-width="1.5" />'
                )

        series = []
        if isinstance(item.get("fund"), (int, float)):
            series.append(("Fund", _C_FUND, fmt_val(item["fund"])))
        if isinstance(item.get("benchmark"), (int, float)):
            series.append(("Benchmark", _C_BENCH, fmt_val(item["benchmark"])))
        if series:
            label_str = _escape_xml(label_for(item))
            longest_text = max(
                len(label_for(item)),
                max(len(name) + len(value) + 3 for name, _, value in series),
            )
            tip_w = max(110, min(200, longest_text * 7 + 24))
            row_h = 18
            tip_h = 26 + len(series) * row_h + 6
            anchor_right = cx_pt + tip_w + 16 > w - pad_right
            tip_x = cx_pt - tip_w - 12 if anchor_right else cx_pt + 12
            tooltip_value = item.get("fund") if isinstance(item.get("fund"), (int, float)) else item.get("benchmark")
            value_y = y_for(tooltip_value)
            tip_y = max(pad_top + 4, min(value_y - tip_h / 2, pad_top + plot_h - tip_h - 4))
            parts.append('<g class="chart-tooltip-box">')
            parts.append(
                f'<rect x="{tip_x:.1f}" y="{tip_y:.1f}" width="{tip_w:.1f}" height="{tip_h:.1f}" '
                f'rx="4" ry="4" fill="#fff" stroke="{_C_GRID}" stroke-width="1" filter="url(#tip-shadow)" />'
            )
            parts.append(
                f'<text x="{tip_x + 10:.1f}" y="{tip_y + 16:.1f}" fill="{_C_BODY}" '
                f'font-size="11" font-weight="700">{label_str}</text>'
            )
            for row_index, (name, color, value) in enumerate(series):
                row_y = tip_y + 30 + row_index * row_h
                parts.append(
                    f'<line x1="{tip_x + 10:.1f}" y1="{row_y - 3:.1f}" '
                    f'x2="{tip_x + 21:.1f}" y2="{row_y - 3:.1f}" stroke="{color}" stroke-width="2.5" '
                    f'stroke-linecap="round" />'
                )
                parts.append(
                    f'<text x="{tip_x + 27:.1f}" y="{row_y:.1f}" fill="{_C_BODY}" font-size="10">'
                    f'{_escape_xml(name)}</text>'
                )
                parts.append(
                    f'<text x="{tip_x + tip_w - 8:.1f}" y="{row_y:.1f}" '
                    f'text-anchor="end" fill="{_C_BODY}" font-size="10" font-variant-numeric="tabular-nums">'
                    f'{_escape_xml(value)}</text>'
                )
            parts.append('</g>')
        parts.append('</g>')

    parts.append('</svg>')
    return "\n".join(parts)


def build_donut_chart_svg(data: list[dict]) -> str:
    """Build an inline SVG donut chart from asset allocation data.

    Accepts a list of dicts with keys:
    - 'label' (string)
    - 'value' (number, percentage)

    Returns SVG markup string.
    """
    if not data:
        return ""

    total = sum(item.get("value", 0) for item in data if isinstance(item.get("value"), (int, float)))
    if not total:
        return ""

    w, h = 300, 280
    cx, cy = w / 2, 150
    outer_r = 90
    inner_r = outer_r * 0.56

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'style="width:100%;height:auto;max-height:280px;" '
        f'font-family="MORN Intrinsic,Aptos,Calibri,sans-serif">'
        '<defs>'
        '<filter id="tip-shadow" x="-20%" y="-20%" width="140%" height="140%">'
        '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#3D3B39" flood-opacity="0.14"/>'
        '</filter>'
        '</defs>'
    ]

    legend_x = 10
    legend_y = 18
    for item in data:
        color = _ALLOC_COLORS.get(item["label"], _ALLOC_COLORS["Other"])
        label = _escape_xml(item["label"])
        text_w = len(item["label"]) * 7
        if legend_x + text_w + 20 > w - 10:
            legend_x = 10
            legend_y += 20
        parts.append(f'<circle cx="{legend_x + 5}" cy="{legend_y}" r="4" fill="{color}" />')
        parts.append(
            f'<text x="{legend_x + 13}" y="{legend_y}" dominant-baseline="middle" '
            f'fill="{_C_TEXT}" font-size="11">{label}</text>'
        )
        legend_x += text_w + 28

    angle = -math.pi / 2
    for item in data:
        value = item.get("value", 0)
        if not isinstance(value, (int, float)) or value <= 0:
            continue
        slice_angle = (value / total) * 2 * math.pi
        start_angle = angle
        end_angle = angle + slice_angle
        mid_angle = (start_angle + end_angle) / 2
        color = _ALLOC_COLORS.get(item["label"], _ALLOC_COLORS["Other"])
        display_label = _escape_xml(item["label"])
        value_str = f"{value:.1f}%"

        x1_o = cx + outer_r * math.cos(start_angle)
        y1_o = cy + outer_r * math.sin(start_angle)
        x2_o = cx + outer_r * math.cos(end_angle)
        y2_o = cy + outer_r * math.sin(end_angle)
        x1_i = cx + inner_r * math.cos(end_angle)
        y1_i = cy + inner_r * math.sin(end_angle)
        x2_i = cx + inner_r * math.cos(start_angle)
        y2_i = cy + inner_r * math.sin(start_angle)

        large_arc = 1 if slice_angle > math.pi else 0

        path = (
            f'M{x1_o:.2f},{y1_o:.2f} '
            f'A{outer_r},{outer_r} 0 {large_arc},1 {x2_o:.2f},{y2_o:.2f} '
            f'L{x1_i:.2f},{y1_i:.2f} '
            f'A{inner_r},{inner_r} 0 {large_arc},0 {x2_i:.2f},{y2_i:.2f} Z'
        )

        # Card tooltip position: outside the ring in the direction of mid_angle
        tip_w = max(88, min(140, (len(item["label"]) + len(value_str)) * 6 + 36))
        tip_h = 28
        tip_margin = 14
        anchor_x = cx + (outer_r + tip_margin) * math.cos(mid_angle)
        anchor_y = cy + (outer_r + tip_margin) * math.sin(mid_angle)
        tip_x = anchor_x if math.cos(mid_angle) >= 0 else anchor_x - tip_w
        tip_y = anchor_y - tip_h / 2
        tip_x = max(2, min(w - tip_w - 2, tip_x))
        tip_y = max(2, min(h - tip_h - 2, tip_y))
        row_y = tip_y + 18

        parts.append('<g class="slice-group">')
        parts.append(
            f'<path class="slice-arc" d="{path}" fill="{color}" stroke="#fff" stroke-width="2"></path>'
        )
        parts.append('<g class="chart-tooltip-box">')
        parts.append(
            f'<rect x="{tip_x:.1f}" y="{tip_y:.1f}" width="{tip_w:.1f}" height="{tip_h:.1f}" '
            f'rx="4" ry="4" fill="#fff" stroke="{_C_GRID}" stroke-width="1" filter="url(#tip-shadow)" />'
        )
        parts.append(
            f'<line x1="{tip_x + 8:.1f}" y1="{row_y - 3:.1f}" '
            f'x2="{tip_x + 19:.1f}" y2="{row_y - 3:.1f}" '
            f'stroke="{color}" stroke-width="2.5" stroke-linecap="round" />'
        )
        parts.append(
            f'<text x="{tip_x + 25:.1f}" y="{row_y:.1f}" fill="{_C_BODY}" font-size="10">'
            f'{display_label}</text>'
        )
        parts.append(
            f'<text x="{tip_x + tip_w - 8:.1f}" y="{row_y:.1f}" text-anchor="end" '
            f'fill="{_C_BODY}" font-size="10" font-variant-numeric="tabular-nums">'
            f'{_escape_xml(value_str)}</text>'
        )
        parts.append('</g>')
        parts.append('</g>')
        angle = end_angle

    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{inner_r - 1:.1f}" fill="#fff" pointer-events="none" />')

    parts.append('</svg>')
    return "\n".join(parts)
