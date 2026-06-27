import unittest
from unittest.mock import patch, MagicMock
from app.parsers.pdf_text_extractor import PdfTextExtractor

class MockPage:
    """Deterministic mock object to simulate pdfplumber Page behavior."""
    def __init__(self, text=None, exception=False):
        self.text = text
        self.exception = exception

    def extract_text(self):
        if self.exception:
            raise Exception("Mocked PDF extraction error simulating a corrupt page")
        return self.text

class TestPdfTextExtractor(unittest.TestCase):
    """
    Deterministic Tests for the PdfTextExtractor module.
    Validates correct page mapping, defensive error handling, 
    and extraction reproducibility using stateless mocked dependencies.
    """

    def setUp(self):
        self.extractor = PdfTextExtractor()

    @patch('app.parsers.pdf_text_extractor.pdfplumber.open')
    def test_deterministic_page_ordering_and_reproducibility(self, mock_pdfplumber_open):
        """1. & 3. Ensure pages are extracted and ordered deterministically (1-indexed)."""
        mock_pdf = MagicMock()
        mock_pdf.pages = [
            MockPage(text="Page 1 Text"),
            MockPage(text="Page 2 Text   "), # Extra whitespace to test stripping
            MockPage(text="Page 3 Text")
        ]
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

        result = self.extractor.extract_text("dummy_path.pdf")

        self.assertEqual(len(result), 3)
        self.assertEqual(result[1], "Page 1 Text")
        self.assertEqual(result[2], "Page 2 Text")
        self.assertEqual(result[3], "Page 3 Text")

    @patch('app.parsers.pdf_text_extractor.pdfplumber.open')
    def test_empty_page_handling(self, mock_pdfplumber_open):
        """2. Ensure completely blank pages are defensively ignored without misaligning indices."""
        mock_pdf = MagicMock()
        mock_pdf.pages = [
            MockPage(text="Page 1 Data"),
            MockPage(text=None),
            MockPage(text="   \n  "), # Whitespace-only page
            MockPage(text="Page 4 Data")
        ]
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

        result = self.extractor.extract_text("dummy_path.pdf")

        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertNotIn(2, result)
        self.assertNotIn(3, result)
        self.assertIn(4, result)

    @patch('app.parsers.pdf_text_extractor.pdfplumber.open')
    def test_malformed_page_defensive_handling(self, mock_pdfplumber_open):
        """4. Ensure a corrupt page throwing a structural exception does not crash the pipeline."""
        mock_pdf = MagicMock()
        mock_pdf.pages = [
            MockPage(text="Valid Page 1"),
            MockPage(exception=True),
            MockPage(text="Valid Page 3")
        ]
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

        result = self.extractor.extract_text("dummy_path.pdf")

        self.assertEqual(len(result), 2)
        self.assertNotIn(2, result)
        self.assertEqual(result[3], "Valid Page 3")

    def test_stable_dictionary_output_structure(self):
        """5. Ensure the internal helper enforces exact string outputs regardless of input type."""
        valid_page = MockPage(text="Standard text")
        none_page = MockPage(text=None)
        error_page = MockPage(exception=True)

        self.assertEqual(self.extractor._extract_page_text(valid_page), "Standard text")
        self.assertEqual(self.extractor._extract_page_text(none_page), "")
        self.assertEqual(self.extractor._extract_page_text(error_page), "")