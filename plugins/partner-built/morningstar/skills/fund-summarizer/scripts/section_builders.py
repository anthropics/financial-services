"""Build derived HTML placeholders from structured fund summary data."""

from html import escape


_TRAILING_PERIODS = ["YTD", "1 Yr", "2 Yr", "3 Yr", "5 Yr", "10 Yr"]

_ISSUER_INITIATED_DISCLOSURE = (
    "In Australia and New Zealand only, starting from June 2026, Morningstar may receive a fee from product issuers "
    "for preparing Morningstar Medalist Rating on their financial product(s) domiciled in Australia or New Zealand "
    "(an \"Issuer Initiated Rating\"). An Issuer Initiated Rating will apply to a strategy and its associated share "
    "classes. "
    "Morningstar will clearly identify each Issuer Initiated Rating on the front page of the report and will provide "
    "disclosure relating to the party that has paid the associated fee. Fees for an Issuer Initiated Rating are not "
    "linked "
    "to the rating outcome, and the paying entity has no influence over the analytical process or rating outcome."
)

_TRACKS_MORNINGSTAR_INDEX_DISCLOSURE = (
    "Certain managed investments use indexes created by and licensed from Morningstar, Inc., and its subsidiaries as "
    "their tracking index. We mitigate any actual or potential conflicts of interest arising from these activities by "
    "maintaining and enforcing information barriers, including both technological and non-technological controls, and "
    "conducting ongoing monitoring through Morningstar's Compliance department. Morningstar will clearly identify "
    "manager "
    "research related to such indexes on the front page of the report. Morningstar does not provide qualitative "
    "ratings or "
    "opinions for investments managed by Morningstar or managed investments that track Morningstar indexes that "
    "incorporate "
    "discretionary inputs assigned by Morningstar employees on an ongoing basis, such as Morningstar Economic Moat "
    "Ratings, "
    "or ESG Ratings."
)


def _is_missing(value) -> bool:
    """Return True when a profile value should not make a section visible."""
    if value is None:
        return True
    if isinstance(value, str):
        normalized = value.strip().lower()
        return normalized in {"", "--", "-", "n/a", "na", "not available", "not returned", "none", "null"}
    return False


def _has_display_value(value) -> bool:
    """Return True for a non-empty, non-placeholder display value."""
    return not _is_missing(value)


def _fmt_pct(value) -> str:
    """Format a numeric percentage value for display."""
    if value is None:
        return "--"
    if isinstance(value, str):
        return value
    return f"{value:.1f}%"


def _fmt_value(value, fmt: str = "plain") -> str:
    """Format a value according to its format hint."""
    if value is None:
        return "--"
    if isinstance(value, str):
        return value
    if fmt == "pct":
        return f"{value:.1f}%"
    if fmt == "ratio":
        return f"{value:.2f}"
    if fmt == "compact":
        if abs(value) >= 1_000_000:
            return f"{value / 1_000_000:,.1f}M"
        return f"{value:,.1f}"
    return str(value)


def _escape_html(value) -> str:
    """Escape external text before embedding it in renderer-generated HTML."""
    return escape(str(value), quote=True)


def _fmt_return(value, signed: bool = False) -> str:
    """Format a table return value with two decimals and optional plus sign."""
    if value is None:
        return "--"
    if isinstance(value, str):
        return _escape_html(value)
    try:
        number = float(value)
    except (ValueError, TypeError):
        return "--"
    if signed and number > 0:
        return f"+{number:.2f}"
    return f"{number:.2f}"


def _number_or_none(value) -> float | None:
    """Parse a numeric input used for derived calculations."""
    if value is None:
        return None
    try:
        return float(str(value).strip().rstrip("%"))
    except (ValueError, TypeError):
        return None


def _has_positive_fund_value(rows: list) -> bool:
    """Return True when at least one row has positive fund exposure."""
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        value = row.get("fund")
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)) and value > 0:
            return True
        number = _number_or_none(value)
        if number is not None and number > 0:
            return True
    return False


def _has_meaningful_fund_value(rows: list) -> bool:
    """Return True when at least one row has a nonzero or textual fund value."""
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        value = row.get("fund")
        if _is_missing(value):
            continue
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            if value != 0:
                return True
            continue
        number = _number_or_none(value)
        if number is not None:
            if number != 0:
                return True
            continue
        return True
    return False


def _fmt_rank(value) -> str:
    """Format an annual return percentile rank."""
    if value is None:
        return "--"
    if isinstance(value, str):
        return _escape_html(value)
    try:
        return str(int(round(float(value))))
    except (ValueError, TypeError):
        return "--"


def _coerce_paragraphs(value) -> list[str]:
    """Normalize a string/list summary input into paragraph strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _paragraphs_html(value, fallback: str = "") -> str:
    """Build escaped paragraph HTML from structured plain-text summary input."""
    paragraphs = _coerce_paragraphs(value)
    if not paragraphs:
        paragraphs = _coerce_paragraphs(fallback)
    return "".join(f"<p>{_escape_html(paragraph)}</p>" for paragraph in paragraphs)


def _build_top_holdings_rows(rows: list[dict]) -> str:
    """Build top-holdings table rows from structured holding dictionaries."""
    output = []
    for row in rows[:10]:
        name = _escape_html(row.get("name") or row.get("holding") or row.get("label") or "--")
        weight = row.get("weight")
        weight_display = _fmt_pct(weight) if not isinstance(weight, str) else _escape_html(weight)
        output.append(f"<tr><td>{name}</td><td>{weight_display}</td></tr>")
    return "".join(output)


def _build_trailing_returns_rows(rows: list[dict], include_benchmark: bool = True) -> str:
    """Build trailing returns table body from structured period dictionaries."""
    by_period = {str(row.get("period", "")).strip(): row for row in rows}

    def values_for(key: str) -> list:
        return [by_period.get(period, {}).get(key) for period in _TRAILING_PERIODS]

    fund_values = values_for("fund")
    benchmark_values = values_for("benchmark")
    fund_cells = "".join(f"<td>{_fmt_return(value)}</td>" for value in fund_values)
    output = [f'<tr class="row-fund"><td>Fund</td>{fund_cells}</tr>']

    benchmark_available = include_benchmark and any(value is not None for value in benchmark_values)
    if benchmark_available:
        benchmark_cells = "".join(f"<td>{_fmt_return(value)}</td>" for value in benchmark_values)
        output.append(f"<tr><td>Benchmark</td>{benchmark_cells}</tr>")
        excess_cells = []
        for fund_value, benchmark_value in zip(fund_values, benchmark_values):
            fund_number = _number_or_none(fund_value)
            benchmark_number = _number_or_none(benchmark_value)
            if fund_number is None or benchmark_number is None:
                excess_cells.append("<td>--</td>")
                continue
            excess_cells.append(f"<td>{_fmt_return(fund_number - benchmark_number, signed=True)}</td>")
        output.append(f'<tr class="row-excess"><td>Excess</td>{"".join(excess_cells)}</tr>')
    return "".join(output)


def _build_annual_returns_parts(rows: list[dict], include_benchmark: bool = True) -> dict[str, str]:
    """Build annual returns headers and rows from structured year dictionaries."""
    sorted_rows = sorted(rows, key=lambda row: row.get("year") or 0)
    headers = "".join(f"<th>{_escape_html(row.get('year'))}</th>" for row in sorted_rows)

    fund_cells = "".join(f"<td>{_fmt_return(row.get('fund'))}</td>" for row in sorted_rows)
    output = [f'<tr class="row-fund"><td>Fund</td>{fund_cells}</tr>']

    benchmark_available = include_benchmark and any(row.get("benchmark") is not None for row in sorted_rows)
    if benchmark_available:
        benchmark_cells = "".join(f"<td>{_fmt_return(row.get('benchmark'))}</td>" for row in sorted_rows)
        output.append(f"<tr><td>Benchmark</td>{benchmark_cells}</tr>")
        excess_cells = []
        for row in sorted_rows:
            fund_number = _number_or_none(row.get("fund"))
            benchmark_number = _number_or_none(row.get("benchmark"))
            if fund_number is None or benchmark_number is None:
                excess_cells.append("<td>--</td>")
                continue
            excess_cells.append(f"<td>{_fmt_return(fund_number - benchmark_number, signed=True)}</td>")
        output.append(f'<tr class="row-excess"><td>Excess</td>{"".join(excess_cells)}</tr>')

    rank_cells = "".join(
        f"<td>{_fmt_rank(row.get('rank') if 'rank' in row else row.get('percentile_rank'))}</td>"
        for row in sorted_rows
    )
    if rank_cells:
        output.append(f"<tr><td>Percentile Rank</td>{rank_cells}</tr>")
    return {"headers": headers, "rows": "".join(output)}


def _populate_table_placeholders(data: dict) -> None:
    """Populate table and benchmark placeholders from structured inputs."""
    if data.get("TOP_HOLDINGS"):
        data["TOP_HOLDINGS_ROWS"] = _build_top_holdings_rows(data["TOP_HOLDINGS"])
        if not data.get("PCT_TOP_10"):
            total = sum(
                row.get("weight", 0)
                for row in data["TOP_HOLDINGS"][:10]
                if isinstance(row.get("weight"), (int, float))
            )
            data["PCT_TOP_10"] = f"{total:.1f}%" if total else "--"

    include_benchmark = not bool(data.get("BENCHMARK_CURRENCY_MISMATCH"))
    if data.get("TRAILING_RETURNS"):
        data["TRAILING_RETURNS_ROWS"] = _build_trailing_returns_rows(data["TRAILING_RETURNS"], include_benchmark)
    if data.get("ANNUAL_RETURNS"):
        annual_parts = _build_annual_returns_parts(data["ANNUAL_RETURNS"], include_benchmark)
        data["ANNUAL_RETURNS_HEADERS"] = annual_parts["headers"]
        data["ANNUAL_RETURNS_ROWS"] = annual_parts["rows"]

    if data.get("BENCHMARK_CURRENCY_MISMATCH"):
        data["BENCHMARK_LEGEND_ENTRY"] = ""
        if not data.get("BENCHMARK_CURRENCY_NOTE"):
            note = data.get("BENCHMARK_CURRENCY_NOTE_TEXT") or (
                "The benchmark is denominated in a different currency than the fund. "
                "Benchmark returns have been excluded from this report."
            )
            data["BENCHMARK_CURRENCY_NOTE"] = f'<p class="currency-note">{_escape_html(note)}</p>'
    elif "BENCHMARK_LEGEND_ENTRY" not in data:
        benchmark_name = data.get("BENCHMARK_NAME") or data.get("PROSPECTUS_BENCHMARK")
        if benchmark_name:
            data["BENCHMARK_LEGEND_ENTRY"] = (
                f'<span><i style="background:var(--c-bench);"></i>{_escape_html(benchmark_name)}</span>'
            )


def _populate_summary_placeholders(data: dict) -> None:
    """Populate escaped summary HTML placeholders from structured text inputs."""
    if data.get("ANALYST_SUMMARY_PARAGRAPHS"):
        data["ANALYST_SUMMARY"] = _paragraphs_html(data["ANALYST_SUMMARY_PARAGRAPHS"])

    pillar_summaries = data.get("PILLAR_SUMMARIES") if isinstance(data.get("PILLAR_SUMMARIES"), dict) else {}
    for key, legacy_key in (
        ("process", "PROCESS_SUMMARY"),
        ("people", "PEOPLE_SUMMARY"),
        ("parent", "PARENT_SUMMARY"),
        ("price", "PRICE_SUMMARY"),
    ):
        html_key = f"{legacy_key}_HTML"
        if html_key in data:
            continue
        data[html_key] = _paragraphs_html(pillar_summaries.get(key), data.get(legacy_key, ""))


def _normalize_disclosure_type(value) -> str:
    """Normalize the CNAXS disclosure label for matching and display."""
    if _is_missing(value):
        return ""
    text = str(value).strip()
    if text.lower() in {"no", "false"}:
        return ""
    return text


def _populate_medalist_disclosures(data: dict) -> None:
    """Populate CNAXS front-page label and bottom footnote placeholders."""
    disclosure_type = _normalize_disclosure_type(data.get("MEDALIST_DISCLOSURE_TYPE"))
    if not disclosure_type:
        data["MEDALIST_DISCLOSURE_TYPE_DISPLAY"] = ""
        data["MEDALIST_DISCLOSURE_FOOTNOTE"] = ""
        return

    data["MEDALIST_DISCLOSURE_TYPE_DISPLAY"] = (
        f'<div class="muted medalist-disclosure-type">{_escape_html(disclosure_type)}</div>'
    )

    normalized = disclosure_type.lower()
    if "issuer initiated" in normalized:
        disclosure_text = _ISSUER_INITIATED_DISCLOSURE
    elif "tracks morningstar index" in normalized or "morningstar index" in normalized:
        disclosure_text = _TRACKS_MORNINGSTAR_INDEX_DISCLOSURE
    else:
        data["MEDALIST_DISCLOSURE_FOOTNOTE"] = ""
        return

    data["MEDALIST_DISCLOSURE_FOOTNOTE"] = (
        f'<div class="footnote medalist-disclosure-footnote"><strong>{_escape_html(disclosure_type)}:</strong> '
        f'{_escape_html(disclosure_text)}</div>'
    )


def _has_benchmark(rows: list) -> bool:
    """Check if any row in a list has a non-null benchmark value."""
    return any(not _is_missing(row.get("benchmark")) for row in rows)


def _hide_class(visible: bool) -> str:
    """Return the template class used to hide empty optional sections."""
    return "" if visible else "is-empty"


def _note_html(notes: list[str]) -> str:
    """Wrap note text in the template's note class."""
    if not notes:
        return ""
    return f'<div class="section-note">{" ".join(notes)}</div>'


def _empty_comparison_parts() -> dict[str, str | bool]:
    """Return empty comparison table parts for hidden sections."""
    return {"header": "", "rows": "", "note": "", "visible": False}


def _sort_key(row: dict) -> float:
    value = row.get("fund")
    if value is None:
        return float("inf")
    if isinstance(value, (int, float)):
        return -value
    try:
        return -float(str(value).rstrip("%"))
    except (ValueError, TypeError):
        return float("inf")


def _comparison_parts(
    rows: list,
    col_header: str,
    fund_name: str,
    sort_desc: bool = True,
    use_bars: bool = True,
    fmt: str = "pct",
) -> dict[str, str | bool]:
    """Build table header/rows/note parts for an explicit template section."""
    if not rows:
        return _empty_comparison_parts()

    populated_rows = []
    for row in rows:
        fund_val = row.get("fund")
        benchmark_val = row.get("benchmark")
        if _is_missing(fund_val) and _is_missing(benchmark_val):
            continue
        populated_rows.append(row)

    if not populated_rows:
        return _empty_comparison_parts()

    if sort_desc:
        populated_rows.sort(key=_sort_key)

    benchmark_available = _has_benchmark(rows)
    if benchmark_available:
        header = f'<tr><th>{col_header}</th><th>Fund</th><th>Benchmark</th></tr>'
    else:
        header = f'<tr><th>{col_header}</th><th>Fund</th></tr>'

    row_html = []
    for row in populated_rows:
        row_fmt = row.get("format", fmt)
        fund_display = _fmt_pct(row.get("fund")) if row_fmt == "pct" else _fmt_value(row.get("fund"), row_fmt)
        if benchmark_available:
            row_html.append(_comparison_row_with_benchmark(row, row_fmt, fund_display, use_bars))
        else:
            row_html.append(_comparison_row_without_benchmark(row, row_fmt, fund_display, use_bars))

    notes = _comparison_notes(benchmark_available)
    return {
        "header": header,
        "rows": "\n".join(row_html),
        "note": _note_html(notes),
        "visible": True,
    }


def _comparison_row_with_benchmark(row: dict, row_fmt: str, fund_display: str, use_bars: bool) -> str:
    benchmark_val = row.get("benchmark")
    benchmark_display = _fmt_pct(benchmark_val) if row_fmt == "pct" else _fmt_value(benchmark_val, row_fmt)
    if use_bars and row_fmt == "pct":
        fund_width = row.get("fund") if isinstance(row.get("fund"), (int, float)) else 0
        benchmark_width = benchmark_val if isinstance(benchmark_val, (int, float)) else 0
        return (
            f'<tr><td>{row["label"]}</td>'
            f'<td><div class="region-cell"><span class="region-bar">'
            f'<span style="width:{fund_width:.1f}%"></span></span>'
            f'<span class="region-value">{fund_display}</span></div></td>'
            f'<td><div class="region-cell"><span class="region-bar bench">'
            f'<span style="width:{benchmark_width:.1f}%"></span></span>'
            f'<span class="region-value">{benchmark_display}</span></div></td></tr>'
        )
    return f'<tr><td>{row["label"]}</td><td>{fund_display}</td><td>{benchmark_display}</td></tr>'


def _comparison_row_without_benchmark(row: dict, row_fmt: str, fund_display: str, use_bars: bool) -> str:
    if use_bars and row_fmt == "pct":
        fund_width = row.get("fund") if isinstance(row.get("fund"), (int, float)) else 0
        return (
            f'<tr><td>{row["label"]}</td>'
            f'<td><div class="region-cell"><span class="region-bar">'
            f'<span style="width:{fund_width:.1f}%"></span></span>'
            f'<span class="region-value">{fund_display}</span></div></td></tr>'
        )
    return f'<tr><td>{row["label"]}</td><td>{fund_display}</td></tr>'


def _comparison_notes(benchmark_available: bool) -> list[str]:
    notes = []
    if not benchmark_available:
        notes.append("Benchmark portfolio detail was not available for this section.")
    return notes


def _style_box_rows(data: dict) -> str:
    """Build explicit style-box table rows from SKILL.md style box values."""
    rows = []
    if _has_display_value(data.get("STYLE_BOX_EQUITY")):
        rows.append(f'<tr><td>Equity Style Box</td><td>{data["STYLE_BOX_EQUITY"]}</td></tr>')
    if _has_display_value(data.get("STYLE_BOX_FIXED_INCOME")):
        rows.append(f'<tr><td>Fixed-Income Style Box</td><td>{data["STYLE_BOX_FIXED_INCOME"]}</td></tr>')
    return "\n".join(rows)


def populate_section_placeholders(data: dict) -> None:
    """Populate derived portfolio-detail placeholders in place."""
    _populate_table_placeholders(data)
    _populate_summary_placeholders(data)
    _populate_medalist_disclosures(data)

    fund_name = data.get("FUND_NAME", "This fund")

    style_rows = _style_box_rows(data)
    data["STYLE_BOX_ROWS"] = style_rows
    data["STYLE_BOX_SECTION_CLASS"] = _hide_class(bool(style_rows))

    fixed_income_region_rows = data.get("FIXED_INCOME_REGION_ROWS", [])
    if not (
        _has_display_value(data.get("FI_DURATION"))
        or _has_display_value(data.get("FI_CREDIT_QUALITY"))
        or _has_positive_fund_value(fixed_income_region_rows)
    ):
        fixed_income_region_rows = []

    fixed_income_parts = _comparison_parts(
        fixed_income_region_rows,
        "Region",
        fund_name,
        sort_desc=True,
        use_bars=True,
        fmt="pct",
    )
    fixed_income_stats_visible = bool(
        _has_display_value(data.get("FI_DURATION"))
        or _has_display_value(data.get("FI_CREDIT_QUALITY"))
    )
    fixed_income_visible = bool(fixed_income_stats_visible or fixed_income_parts["visible"])
    data["FIXED_INCOME_SECTION_CLASS"] = _hide_class(fixed_income_visible)
    data["FIXED_INCOME_STATS_SECTION_CLASS"] = _hide_class(fixed_income_stats_visible)
    data["FIXED_INCOME_REGION_SECTION_CLASS"] = _hide_class(bool(fixed_income_parts["visible"]))
    data["FIXED_INCOME_REGION_HEADER"] = fixed_income_parts["header"]
    data["FIXED_INCOME_REGION_ROWS_HTML"] = fixed_income_parts["rows"]
    data["FIXED_INCOME_SECTION_NOTE"] = fixed_income_parts["note"]
    if data.get("FI_DURATION") is None:
        data["FI_DURATION"] = "--"
    elif isinstance(data.get("FI_DURATION"), (int, float)):
        data["FI_DURATION"] = f'{data["FI_DURATION"]:.2f} yrs'
    if not data.get("FI_CREDIT_QUALITY"):
        data["FI_CREDIT_QUALITY"] = "--"

    regional_exposure_rows = data.get("REGIONAL_EXPOSURE_ROWS", [])
    if not _has_positive_fund_value(regional_exposure_rows):
        regional_exposure_rows = []

    regional_parts = _comparison_parts(
        regional_exposure_rows,
        "Region",
        fund_name,
        sort_desc=True,
        use_bars=True,
        fmt="pct",
    )
    data["REGIONAL_EXPOSURE_SECTION_CLASS"] = _hide_class(bool(regional_parts["visible"]))
    data["REGIONAL_EXPOSURE_HEADER"] = regional_parts["header"]
    data["REGIONAL_EXPOSURE_ROWS_HTML"] = regional_parts["rows"]
    data["REGIONAL_EXPOSURE_SECTION_NOTE"] = regional_parts["note"]

    market_cap_rows = data.get("MARKET_CAP_ROWS", [])
    if not _has_positive_fund_value(market_cap_rows):
        market_cap_rows = []

    market_cap_parts = _comparison_parts(
        market_cap_rows,
        "Market Cap",
        fund_name,
        sort_desc=True,
        use_bars=True,
        fmt="pct",
    )
    data["MARKET_CAP_SECTION_CLASS"] = _hide_class(bool(market_cap_parts["visible"]))
    data["MARKET_CAP_HEADER"] = market_cap_parts["header"]
    data["MARKET_CAP_ROWS_HTML"] = market_cap_parts["rows"]
    data["MARKET_CAP_SECTION_NOTE"] = market_cap_parts["note"]

    equity_portfolio_stats_rows = data.get("EQUITY_PORTFOLIO_STATS_ROWS", [])
    if not _has_meaningful_fund_value(equity_portfolio_stats_rows):
        equity_portfolio_stats_rows = []

    equity_stats_parts = _comparison_parts(
        equity_portfolio_stats_rows,
        "Statistic",
        fund_name,
        sort_desc=False,
        use_bars=False,
        fmt="plain",
    )
    data["EQUITY_PORTFOLIO_STATS_SECTION_CLASS"] = _hide_class(bool(equity_stats_parts["visible"]))
    data["EQUITY_PORTFOLIO_STATS_HEADER"] = equity_stats_parts["header"]
    data["EQUITY_PORTFOLIO_STATS_ROWS_HTML"] = equity_stats_parts["rows"]
    data["EQUITY_PORTFOLIO_STATS_SECTION_NOTE"] = equity_stats_parts["note"]

    equity_visible = bool(
        regional_parts["visible"]
        or market_cap_parts["visible"]
        or equity_stats_parts["visible"]
    )
    data["EQUITY_PROFILE_SECTION_CLASS"] = _hide_class(equity_visible)
