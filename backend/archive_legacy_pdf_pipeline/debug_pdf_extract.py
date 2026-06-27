
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

from app.parsers.pdf_text_extractor import PdfTextExtractor


def main():
    print("STEP 1")

    if len(sys.argv) < 2:
        print("Usage:")
        print("python debug_pdf_extract.py <path_to_pdf> [start_page] [end_page]")
        sys.exit(1)

    pdf_path = sys.argv[1]

    print("STEP 2")

    start_page = int(sys.argv[2]) if len(sys.argv) > 2 else None
    end_page = int(sys.argv[3]) if len(sys.argv) > 3 else None

    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    print("STEP 3")

    extractor = PdfTextExtractor()

    print("STEP 4")

    pages = extractor.extract_text(pdf_path)

    print("STEP 5")

    print(f"TOTAL PAGES EXTRACTED: {len(pages)}")

    for page_num, text in pages.items():

        if start_page is not None and page_num < start_page:
            continue

        if end_page is not None and page_num > end_page:
            continue

        print(f"\n--- PAGE {page_num} ---")

        for line in text.splitlines():
            print(repr(line))


if __name__ == "__main__":
    main()

