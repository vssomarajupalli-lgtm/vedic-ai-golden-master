import io
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
                with sync_playwright() as p:
                    browser = p.chromium.launch()
                    page = browser.new_page()
                    page.set_content(html_content, wait_until="networkidle")
                    pdf_bytes = page.pdf(format="A4", print_background=True)
                    log.info("PDF generated via Playwright (Chromium)")
                    return pdf_bytes
            except Exception as e:
                log.error(f"Playwright PDF generation failed: {e}")
        
        raise RuntimeError("PDF generation unavailable: WeasyPrint (missing GTK/Pango) and Playwright (not installed) both failed.")
