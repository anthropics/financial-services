"""
Fund Summary Report Renderer
============================
Fills {{ PLACEHOLDER }} tokens in template.html with supplied data and writes
the final HTML file.

Usage (programmatic):
    from render import render_report
    render_report(data_dict, output_path="output.html")

Usage (CLI):
    python render.py --data data.json --output report.html
"""

import base64
import json
import re
import subprocess
import sys
import warnings
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

try:
    from .chart_builders import build_donut_chart_svg, build_line_chart_svg
    from .icon_embedder import embed_icons
    from .placeholder_defaults import PLACEHOLDERS, default_for
    from .section_builders import populate_section_placeholders
except ImportError:  # Supports running this file directly as a script.
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))

    from chart_builders import build_donut_chart_svg, build_line_chart_svg
    from icon_embedder import embed_icons
    from placeholder_defaults import PLACEHOLDERS, default_for
    from section_builders import populate_section_placeholders

TEMPLATE_PATH = SKILL_DIR / "assets" / "template.html"
LOGO_PATH = SKILL_DIR / "assets" / "logotype-usage-color-negative-white-red50.png"
ICONS_PATH = SKILL_DIR / "assets" / "icons"


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


def _add_chart_svgs(data: dict) -> None:
    """Populate pre-rendered SVG chart placeholders from chart JSON data."""
    if "CALENDAR_RETURNS_JSON" in data and "CUMULATIVE_RETURNS_JSON" not in data:
        data["CUMULATIVE_RETURNS_JSON"] = data["CALENDAR_RETURNS_JSON"]

    line_data = _parsed_json_list(data.get("CUMULATIVE_RETURNS_JSON") or data.get("CALENDAR_RETURNS_JSON"))
    if line_data:
        data["RETURNS_CHART_SVG"] = build_line_chart_svg(line_data)

    alloc_data = _parsed_json_list(data.get("ASSET_ALLOCATION_JSON"))
    if alloc_data:
        data["DONUT_CHART_SVG"] = build_donut_chart_svg(alloc_data)


def _processed_values(data: dict) -> dict[str, str]:
    """Convert report data into string values ready for template replacement."""
    processed = {}
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            processed[key] = json.dumps(value)
        elif value is None:
            processed[key] = default_for(key)
        else:
            processed[key] = str(value)

    for key in PLACEHOLDERS:
        if key not in processed:
            processed[key] = default_for(key)

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


def default_pdf_path(html_path: str | Path) -> Path:
    """Return the sibling PDF path for a rendered report HTML path."""
    return Path(html_path).with_suffix(".pdf")


def _export_pdf_copy(html_path: Path, pdf_output_path: str | Path | None = None) -> Path:
    """Create a PDF copy of a rendered HTML report using the PDF export helper."""
    pdf_path = Path(pdf_output_path) if pdf_output_path else default_pdf_path(html_path)
    if pdf_path.exists():
        pdf_path.unlink()
    command = [
        sys.executable,
        str(SCRIPT_DIR / "export_report.py"),
        str(html_path),
        "--format",
        "pdf",
        "--output",
        str(pdf_path),
    ]
    completed = subprocess.run(command, capture_output=True, check=False, text=True)
    if completed.returncode != 0:
        details = "\n".join(part for part in [completed.stderr.strip(), completed.stdout.strip()] if part)
        raise RuntimeError(f"PDF export failed with exit code {completed.returncode}.\n{details}".strip())
    return pdf_path.resolve()


def render_report(
    data: dict,
    output_path: str | Path = "report.html",
    *,
    export_pdf: bool = True,
    pdf_output_path: str | Path | None = None,
    require_pdf: bool = False,
) -> Path:
    """
    Render the fund summary HTML by replacing all {{ PLACEHOLDER }} tokens.

    Structured row-list and summary inputs are consumed by section builders.
    Dict and list values are serialized automatically for JSON placeholders.
    By default, a sibling PDF copy is attempted after the HTML is written.
    PDF export failures do not block the HTML deliverable unless require_pdf=True.
    """
    report_data = dict(data)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    output_path = Path(output_path)
    resolved_output_path = output_path.resolve()

    if LOGO_PATH.exists():
        logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
        template = template.replace("{{LOGO_BASE64}}", logo_b64)

    template = embed_icons(template, report_data, ICONS_PATH)
    populate_section_placeholders(report_data)
    _add_chart_svgs(report_data)

    result = _replace_placeholders(template, _processed_values(report_data))
    _warn_unresolved_placeholders(result)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")
    if export_pdf:
        try:
            _export_pdf_copy(resolved_output_path, pdf_output_path)
        except RuntimeError:
            if require_pdf:
                raise
    return resolved_output_path


def main():
    """CLI entry point: python render.py --data data.json [--output report.html]"""
    import argparse

    parser = argparse.ArgumentParser(description="Render fund summary HTML from JSON data.")
    parser.add_argument("--data", help="Path to JSON file with placeholder values")
    parser.add_argument("--output", default="report.html", help="Output HTML path (default: report.html)")
    parser.add_argument("--pdf-output", help="Output PDF path; defaults to the HTML path with .pdf suffix")
    parser.add_argument("--no-pdf", action="store_true", help="Only render HTML; skip the automatic PDF copy")
    parser.add_argument("--require-pdf", action="store_true", help="Fail if the automatic PDF copy cannot be created")
    parser.add_argument("--list-placeholders", action="store_true", help="Print all placeholders and exit")
    args = parser.parse_args()

    if args.list_placeholders:
        print("Available placeholders:\n")
        for key, desc in PLACEHOLDERS.items():
            print(f"  {key:40s} {desc}")
        sys.exit(0)

    if not args.data:
        print("Error: --data is required unless --list-placeholders is used", file=sys.stderr)
        sys.exit(2)

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(data_path.read_text(encoding="utf-8"))
    out = render_report(
        data,
        args.output,
        export_pdf=not args.no_pdf,
        pdf_output_path=args.pdf_output,
        require_pdf=args.require_pdf,
    )
    print(f"Rendered: {out}")
    if not args.no_pdf:
        pdf_path = Path(args.pdf_output).resolve() if args.pdf_output else default_pdf_path(out)
        if pdf_path.exists():
            print(f"PDF: {pdf_path}")


if __name__ == "__main__":
    main()
