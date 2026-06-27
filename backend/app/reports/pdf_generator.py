import io
from app.reports.schemas import FinalReportSchema
from app.reports.html_generator import HTMLGenerator
import logging

log = logging.getLogger("vedic_ai")

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    log.warning("WeasyPrint is not installed or missing OS dependencies. PDF generation will fallback to raw HTML bytes or fail.")

class PDFGenerator:
    """
    Consumes the rendered HTML string and converts it to a binary PDF Blob
    using WeasyPrint. 
    """
    def __init__(self):
        self.html_generator = HTMLGenerator()

    def generate(self, report_data: FinalReportSchema) -> bytes:
        """
        Renders the data to HTML, then converts the HTML to PDF bytes.
        """
        if not WEASYPRINT_AVAILABLE:
            raise RuntimeError("WeasyPrint OS dependencies are missing. Cannot generate PDF natively.")
            
        # 1. Generate the raw HTML string
        html_content = self.html_generator.generate(report_data)
        
        # 2. Render PDF bytes
        pdf_bytes = io.BytesIO()
        HTML(string=html_content).write_pdf(pdf_bytes)
        
        return pdf_bytes.getvalue()
