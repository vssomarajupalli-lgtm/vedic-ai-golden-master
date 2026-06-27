import pdfplumber
from typing import Dict, Any

class PdfTextExtractor:
    """
    Deterministic parser for extracting raw text from horoscope PDFs.
    Stateless, modular, and designed to preserve exact page ordering.
    Contains zero astrological calculations or OCR fallbacks.
    """

    def extract_text(self, pdf_path: str) -> Dict[int, str]:
        """
        Safely opens a PDF and extracts text page-by-page.
        
        Args:
            pdf_path (str): The absolute path to the PDF file.
            
        Returns:
            Dict[int, str]: A dictionary mapping page numbers (1-indexed) to their extracted text.
        """
        extracted_pages: Dict[int, str] = {}

        with pdfplumber.open(pdf_path) as pdf:
            for page_index, page in enumerate(pdf.pages):
                page_number = page_index + 1
                text = self._extract_page_text(page)
                
                # Only map pages that contain extractable deterministic text
                if text:
                    extracted_pages[page_number] = text

        return extracted_pages

    def _extract_page_text(self, page: Any) -> str:
        """
        Safely extracts text from a single page, handling empty or unreadable pages defensively.
        """
        try:
            text = page.extract_text()
            return text.strip() if text else ""
        except Exception:
            # Defensively catch unexpected PDF structural errors on a specific page
            return ""