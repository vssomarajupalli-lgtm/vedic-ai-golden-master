import io
import html as html_lib
import asyncio
import sys
from app.reports.schemas import FinalReportSchema
from app.reports.html_generator import HTMLGenerator
import logging

log = logging.getLogger("vedic_ai")

# Try WeasyPrint first (preferred for quality)
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False
    log.warning("WeasyPrint is not installed or missing OS dependencies. Will use Playwright fallback.")

# Playwright fallback (works on Windows without GTK/Pango)
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


def _client_name(report_data) -> str:
    """Extract the client name from a report dict or FinalReportSchema."""
    try:
        if isinstance(report_data, dict):
            profile = report_data.get("client_profile", {}) or {}
            return str(profile.get("name") or "Vedic-AI Report")
        profile = getattr(report_data, "client_profile", None) or {}
        return str(getattr(profile, "name", None) or "Vedic-AI Report")
    except Exception:
        return "Vedic-AI Report"


def _header_template(client: str) -> str:
    """Running header for Playwright PDF (client name + report title)."""
    title = html_lib.escape("Vedic-AI Intelligence Report")
    client_esc = html_lib.escape(client)
    return (
        "<div style='font-size:9px; color:#6b7280; width:100%; padding:0 14mm; "
        "display:flex; justify-content:space-between;'>"
        f"<span>{client_esc}</span><span>{title}</span>"
        "</div>"
    )


def _footer_template() -> str:
    """Running footer for Playwright PDF (page X of Y)."""
    return (
        "<div style='font-size:9px; color:#6b7280; width:100%; padding:0 14mm; "
        "text-align:center;'>"
        "Page <span class='pageNumber'></span> of <span class='totalPages'></span>"
        "</div>"
    )


class PDFGenerator:
    """
    Consumes the rendered HTML string and converts it to a binary PDF Blob
    using WeasyPrint (preferred) or Playwright (fallback).
    """
    def __init__(self):
        self.html_generator = HTMLGenerator()

    def generate(self, report_data: FinalReportSchema) -> bytes:
        """
        Renders the data to HTML, then converts the HTML to PDF bytes.
        Tries WeasyPrint first (best quality), falls back to Playwright (Chromium).
        """
        # 1. Generate the raw HTML string
        html_content = self.html_generator.generate(report_data)

        # 1.5. PDF Parity: Forcibly expand all <details> tags so the Shadow DOM renders them
        html_content = html_content.replace("<details", "<details open")

        client = _client_name(report_data)

        # Try WeasyPrint first (best quality for printing)
        if WEASYPRINT_AVAILABLE:
            try:
                pdf_bytes = io.BytesIO()
                HTML(string=html_content).write_pdf(pdf_bytes)
                log.info("PDF generated via WeasyPrint")
                return pdf_bytes.getvalue()
            except Exception as e:
                log.warning(f"WeasyPrint failed: {e}. Falling back to Playwright.")

        # Fallback to Playwright (Chromium headless)
        if PLAYWRIGHT_AVAILABLE:
            try:
                # uvicorn with reload=True installs WindowsSelectorEventLoopPolicy,
                # whose event loop cannot spawn subprocesses. Playwright's sync
                # driver relies on asyncio subprocess support, so restore the
                # Proactor policy (subprocess-capable) before launching it.
                if sys.platform == "win32":
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                with sync_playwright() as p:
                    browser = p.chromium.launch()
                    page = browser.new_page()
                    page.set_content(html_content, wait_until="networkidle")
                    pdf_bytes = page.pdf(
                        format="A4",
                        print_background=True,
                        display_header_footer=True,
                        margin={"top": "18mm", "bottom": "18mm", "left": "14mm", "right": "14mm"},
                        header_template=_header_template(client),
                        footer_template=_footer_template(),
                    )
                    log.info("PDF generated via Playwright (Chromium)")
                    return pdf_bytes
            except Exception as e:
                log.error(f"Playwright PDF generation failed: {e}")

        raise RuntimeError("PDF generation unavailable: WeasyPrint (missing GTK/Pango) and Playwright (not installed) both failed.")
