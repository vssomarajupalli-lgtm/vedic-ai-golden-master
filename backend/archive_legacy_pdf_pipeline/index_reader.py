import re
import pdfplumber
from typing import Dict, Any, List, Tuple

class IndexReader:
    """
    Deterministic parser for extracting the Table of Contents/Index from horoscope PDFs.
    Identifies sections and their page ranges to guide downstream extraction.
    Stateless and contains zero astrological calculations.
    """
    
    def __init__(self):
        # Matches strings like "Planetary Positions ........ 4" or "Dashas   12"
        # Groups: 1 = Title, 2 = Page Number
        self.index_line_pattern = re.compile(
            r'^(.*?)\s*(?:[\.\-\_]{2,}|\s{3,})\s*(?:\b(?:page|pg)\.?\s*)?(\d+)\s*$', 
            re.IGNORECASE
        )
        
        # Keywords indicating an index page (evaluated defensively)
        self.index_keywords = ["table of contents", "index", "contents"]

    def extract_index(self, pdf_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Main entry point. Opens the PDF, scans for index pages, and builds
        a deterministic map of sections and their page boundaries.
        """
        extracted_items: List[Tuple[str, int]] = []
        total_pages = 0
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            # Defensively scan only the first 15 pages to find the index
            scan_limit = min(15, total_pages)
            for page_num in range(scan_limit):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if not text:
                    continue
                    
                if self._is_index_page(text):
                    extracted_items.extend(self._parse_page_text(text))
        
        return self._calculate_page_ranges(extracted_items, total_pages)

    # --- Isolated Helper Methods ---

    def _is_index_page(self, text: str) -> bool:
        """Checks the top of the page text for known index headers."""
        header_text = text[:500].lower() 
        return any(keyword in header_text for keyword in self.index_keywords)

    def _parse_page_text(self, text: str) -> List[Tuple[str, int]]:
        """Regex-based line parser to extract raw title and page number pairs."""
        items = []
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            match = self.index_line_pattern.match(line)
            if match:
                raw_title = match.group(1)
                page_number = int(match.group(2))
                
                title = self._normalize_title(raw_title)
                if title:
                    items.append((title, page_number))
        return items

    def _normalize_title(self, title: str) -> str:
        """Safely cleans the extracted title to ensure dictionary key stability."""
        clean = re.sub(r'\s+', ' ', title.strip()).lower()
        
        # Defensively ignore purely numeric titles
        if clean.isnumeric():
            return ""

        # Accept known short patterns for Varga charts (e.g., 'd9', 'd10')
        if re.fullmatch(r'd\d{1,2}', clean):
            return clean

        # For all other titles, enforce a minimum length to filter junk
        if len(clean) < 6:
            return ""
            
        return clean

    def _calculate_page_ranges(self, items: List[Tuple[str, int]], total_pages: int) -> Dict[str, Dict[str, Any]]:
        """Transforms single start pages into start/end boundaries deterministically."""
        if not items:
            return {}
            
        # Remove duplicates (preferring the lowest page number if duplicated)
        unique_items = {}
        for title, page in items:
            if title not in unique_items or unique_items[title] > page:
                unique_items[title] = page
        
        # Sort strictly by page number to guarantee determinism
        sorted_items = sorted(unique_items.items(), key=lambda x: x[1])
        
        structured_index = {}
        for i, (title, start_page) in enumerate(sorted_items):
            # Safely clamp page numbers within document bounds
            safe_start = max(1, min(start_page, total_pages))
            
            if i < len(sorted_items) - 1:
                next_start = sorted_items[i+1][1]
                safe_end = max(safe_start, min(next_start - 1, total_pages))
            else:
                safe_end = total_pages
                
            structured_index[title] = {
                "start_page": safe_start,
                "end_page": safe_end
            }
            
        return structured_index