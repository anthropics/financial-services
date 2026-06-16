"""Fund Summary Report Renderer — fills {{PLACEHOLDER}} tokens in template.html.

CLI:
  python render.py --data data.json [--output report.html]
  python render.py --list-placeholders
"""

import base64
import json
import re
import sys
import warnings
from pathlib import Path

try:
    from .chart_builders import build_donut_chart_svg, build_line_chart_svg
    from .icon_embedder import embed_icons
    from .placeholder_defaults import PLACEHOLDERS
    from .utils import to_number
except ImportError:  # Supports running this file directly as a script.
    from chart_builders import build_donut_chart_svg, build_line_chart_svg
    from icon_embedder import embed_icons
    from placeholder_defaults import PLACEHOLDERS
    from utils import to_number

TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "template.html"
LOGO_PATH = (
    Path(__file__).parent.parent
    / "assets"
    / "logotype-usage-color-negative-white-red50.png"
)
ICONS_PATH = Path(__file__).parent.parent / "assets" / "icons"


def _parsed_json_list(value) -> list:
    """Return a list from an already-parsed list or a JSON list string."""
    if isinstance(value, list):
        return value
    if not isinstance(value, str):
        return []
    try:
        parsed = json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []
    return parsed if isinstance(parsed, list) else []


def _compute_cumulative_returns(raw_monthly: list[dict]) -> list[dict]:
    """
    Compute a Growth of $10,000 cumulative series from raw monthly HP010 returns.

    Input: [{"date": "YYYY-MM-DD", "fund_return": 1.23, "benchmark_return": 0.98}, ...]
    Output: [{"date": "YYYY-MM-DD", "fund": 10123.00, "benchmark": 10098.00}, ...]
    preceded by a $10,000 base observation at the same date as the first entry
    (used only for axis labelling).
    """
    if not raw_monthly:
        return []

    sorted_rows = sorted(raw_monthly, key=lambda r: r.get("date", ""))
    has_benchmark = any(r.get("benchmark_return") is not None for r in sorted_rows)

    base: dict = {"date": sorted_rows[0]["date"], "fund": 10000.0}
    if has_benchmark:
        base["benchmark"] = 10000.0
    result = [base]
    fund_val = 10000.0
    bench_val = 10000.0

    for row in sorted_rows:
        fr = to_number(row.get("fund_return"))
        br = to_number(row.get("benchmark_return"))
        if fr is not None:
            fund_val = round(fund_val * (1 + fr / 100), 2)
        if br is not None:
            bench_val = round(bench_val * (1 + br / 100), 2)
        entry: dict = {"date": row["date"], "fund": fund_val}
        if has_benchmark:
            entry["benchmark"] = bench_val
        result.append(entry)

    return result


def _coerce_chart_rows(rows: list, numeric_keys: tuple) -> list:
    """Return a copy of rows with specified keys coerced to float | None."""
    normalized = []
    for row in rows:
        copy = dict(row)
        for key in numeric_keys:
            if key in copy:
                copy[key] = to_number(copy[key])
        normalized.append(copy)
    return normalized


def _is_benchmark_mismatch(data: dict) -> bool:
    """Return True when BENCHMARK_CURRENCY_MISMATCH is set to true/True."""
    val = data.get("BENCHMARK_CURRENCY_MISMATCH")
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() == "true"


def _compute_benchmark_fields(data: dict) -> None:
    """Compute BENCHMARK_CURRENCY_MISMATCH and auto-generate BENCHMARK_LEGEND_ENTRY
    and BENCHMARK_CURRENCY_NOTE from BASE_CURRENCY and BENCHMARK_CURRENCY.

    The model provides raw currency values; the renderer owns all gate logic.
    Must be called before _apply_benchmark_currency_gate.
    """
    fund_currency = str(data.get("BASE_CURRENCY", "")).strip()
    bench_currency = str(data.get("BENCHMARK_CURRENCY", "")).strip()
    mismatch = bool(fund_currency and bench_currency and fund_currency != bench_currency)

    data["BENCHMARK_CURRENCY_MISMATCH"] = "true" if mismatch else "false"

    bench_name = str(data.get("BENCHMARK_NAME", "")).strip()
    if mismatch:
        data["BENCHMARK_LEGEND_ENTRY"] = ""
        data["BENCHMARK_CURRENCY_NOTE"] = (
            f'<p class="currency-note">Benchmark data is not shown because '
            f"{bench_name} is denominated in {bench_currency}, which differs "
            f"from the fund\u2019s base currency ({fund_currency}).</p>"
        )
    else:
        data["BENCHMARK_LEGEND_ENTRY"] = (
            f'<span><i style="background:var(--c-bench);"></i>{bench_name}</span>'
            if bench_name
            else ""
        )
        data["BENCHMARK_CURRENCY_NOTE"] = ""


def _apply_benchmark_currency_gate(data: dict) -> None:
    """Null out benchmark_return values in MONTHLY_RETURNS_JSON when currencies differ.

    _compute_benchmark_fields must run first to set BENCHMARK_CURRENCY_MISMATCH.
    The model may still pass raw benchmark values in MONTHLY_RETURNS_JSON even
    when currencies differ; this gate prevents them from reaching the chart.
    """
    if not _is_benchmark_mismatch(data):
        return

    monthly = _parsed_json_list(data.get("MONTHLY_RETURNS_JSON"))
    if monthly:
        for row in monthly:
            row["benchmark_return"] = None
        data["MONTHLY_RETURNS_JSON"] = monthly


def _add_chart_svgs(data: dict) -> None:
    """Populate RETURNS_CHART_SVG and DONUT_CHART_SVG from JSON chart data."""
    raw_monthly = _coerce_chart_rows(
        _parsed_json_list(data.get("MONTHLY_RETURNS_JSON")),
        ("fund_return", "benchmark_return"),
    )
    if raw_monthly:
        cumulative = _compute_cumulative_returns(raw_monthly)
        has_benchmark_line = any("benchmark" in r for r in cumulative)
        if not has_benchmark_line and not _is_benchmark_mismatch(data):
            warnings.warn(
                "BENCHMARK_LEGEND_ENTRY is set but MONTHLY_RETURNS_JSON contains no "
                "benchmark_return values — benchmark line will not appear in chart. "
                "Include benchmark HP010 monthly returns in MONTHLY_RETURNS_JSON.",
                stacklevel=2,
            )
        data["RETURNS_CHART_SVG"] = build_line_chart_svg(cumulative)

    alloc_data = _coerce_chart_rows(
        _parsed_json_list(data.get("ASSET_ALLOCATION_JSON")),
        ("value",),
    )
    if alloc_data:
        data["DONUT_CHART_SVG"] = build_donut_chart_svg(alloc_data)


def _processed_values(data: dict) -> dict[str, str]:
    """Serialize the model-provided data dict into string values for template substitution.

    The model is responsible for formatting all values (e.g. '88.20B', '0.75%')
    and building all HTML row strings before calling render_report. This function
    only handles type coercion: dicts/lists → JSON strings, None → empty string,
    everything else → str().

    Two derived fields are computed here because they require no MCP data —
    only values the model already passed:
      STAR_RATING_DISPLAY — star characters derived from STAR_RATING integer.
      MPRS               — rounded to a whole-number string for dial SVG selection.
    """
    processed = {}
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            processed[key] = json.dumps(value)
        elif value is None:
            processed[key] = ""
        else:
            processed[key] = str(value)

    star_count = data.get("STAR_RATING")
    if star_count is not None:
        try:
            stars = max(0, min(5, int(star_count)))
            processed["STAR_RATING_DISPLAY"] = "\u2605" * stars
        except (ValueError, TypeError):
            pass

    mprs = data.get("MPRS")
    if mprs is not None:
        try:
            processed["MPRS"] = str(int(round(float(mprs))))
        except (ValueError, TypeError):
            pass

    return processed


def _replace_placeholders(template: str, values: dict[str, str]) -> str:
    """Replace {{ PLACEHOLDER }} tokens with processed values."""

    def replacer(match):
        key = match.group(1).strip()
        return values.get(key, match.group(0))

    return re.sub(r"\{\{\s*([A-Z_0-9]+)\s*\}\}", replacer, template)


def _warn_unresolved_placeholders(result: str) -> None:
    unresolved = re.findall(r"\{\{\s*[A-Z_0-9]+\s*\}\}", result)
    if not unresolved:
        return
    unique = sorted(set(match.strip("{} ") for match in unresolved))
    warnings.warn(
        f"Unresolved template placeholders: {', '.join(unique)}",
        stacklevel=2,
    )


def render_report(
    data: dict,
    output_path: str | Path = "report.html",
) -> Path:
    """
    Render the fund summary HTML by replacing all {{ PLACEHOLDER }} tokens.

    The model is responsible for all value formatting and HTML row construction
    before calling this function (see references/full-workflow.md, Workflow B).
    This renderer embeds assets, builds SVG charts, substitutes tokens, and
    writes the output file.
    """
    report_data = dict(data)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    output_path = Path(output_path)

    # Derive BENCHMARK_CURRENCY_MISMATCH from the two raw currency values and
    # auto-generate BENCHMARK_LEGEND_ENTRY and BENCHMARK_CURRENCY_NOTE.
    # Must run before _apply_benchmark_currency_gate, which reads the mismatch flag.
    _compute_benchmark_fields(report_data)
    _apply_benchmark_currency_gate(report_data)

    if LOGO_PATH.exists():
        logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
        template = template.replace("{{LOGO_BASE64}}", logo_b64)

    template = embed_icons(template, report_data, ICONS_PATH)
    _add_chart_svgs(report_data)

    result = _replace_placeholders(template, _processed_values(report_data))
    _warn_unresolved_placeholders(result)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")
    return output_path.resolve()


def main():
    """CLI entry point: python render.py --data data.json [--output report.html]"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Render fund summary HTML from JSON data."
    )
    parser.add_argument("--data", help="Path to JSON file with placeholder values")
    parser.add_argument(
        "--output",
        default="report.html",
        help="Output HTML path (default: report.html)",
    )
    parser.add_argument(
        "--list-placeholders",
        action="store_true",
        help="Print all placeholders and exit",
    )
    args = parser.parse_args()

    if args.list_placeholders:
        print("Available placeholders:\n")
        for key, desc in PLACEHOLDERS.items():
            print(f"  {key:40s} {desc}")
        sys.exit(0)

    if not args.data:
        parser.error("--data is required")

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(data_path.read_text(encoding="utf-8"))
    out = render_report(data, args.output)
    print(f"Rendered: {out}")


if __name__ == "__main__":
    main()
