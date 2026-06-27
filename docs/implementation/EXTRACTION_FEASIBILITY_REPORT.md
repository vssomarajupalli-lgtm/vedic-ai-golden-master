# EXTRACTION FEASIBILITY REPORT

**Verification Date:** 2026-06-12 IST  
**Target Repository:** `D:\HoroscopeCleaner_Final` (External Extraction System)  

Based on a physical source code audit of the external `HoroscopeCleaner_Final` repository (`cleaner_dom.py`, `dom_targeter.py`), the following answers your direct feasibility questions:

---

### 1. Are Shadbala pages already being parsed and discarded, or never parsed?
**Answer:** **Parsed and Discarded.**
*   `dom_targeter.py`'s `extract_canonical_content()` utilizes `page.find_tables()` across *all* pages of the PDF.
*   This means the Shadbala tables (pages 12-15) **are actively being physically extracted** into the intermediate output (`{"pages": [{"content_blocks": [{"type": "table", "rows": [...]}]}]}`).
*   However, they are effectively "discarded" because there is no semantic translation layer built to convert these raw table rows into the structured `canonical_content.json` payload consumed by the Vedic-AI backend.

### 2. Are Bhava Bala pages already being parsed and discarded, or never parsed?
**Answer:** **Parsed and Discarded.**
*   Exactly like Shadbala, the Bhava Bala tables (pages 16-19) are captured by the global table extractor and dumped into the intermediate JSON payload. 
*   They are discarded due to the lack of a semantic table mapper.

### 3. For D2-D60 Vargas: Are the tables available, or must new logic be built?
**Answer:** **The raw tables are already available in the intermediate output, but entirely new semantic mapping logic must be built.**
*   All Shodasha Varga tables (pages 23-50) are successfully captured as raw matrix rows by `dom_targeter.py`.
*   Currently, the Vedic-AI backend uses a hardcoded, mock `canonical_content.json` ("Representative sample") containing only D9 and D10. 
*   To extract D2-D60, you must build semantic table parsers that can look at a raw table block, identify its title (e.g., "Hora / D2"), and map the 9 planets to their respective signs.

---

### Feasibility Summary

| Component | Physical Extraction Status | Semantic Parsing Status | Estimated Complexity |
| :--- | :--- | :--- | :--- |
| **Shadbala** | ✅ Available in raw dump | ❌ Missing translation | High (Complex matrix tables) |
| **Bhava Bala** | ✅ Available in raw dump | ❌ Missing translation | High (Complex matrix tables) |
| **Vargas (D2-D60)**| ✅ Available in raw dump | ❌ Missing translation | Medium (Standard 3x4 grids) |

### Lowest-Risk Extraction Target
**Shodasha Vargas (D2-D60)** is the lowest-risk starting point. 
1. The grid structure for a Varga is identical to the D1/D9 charts already theoretically supported. 
2. Adding them involves writing a generic 3x4 grid parser that maps the Telugu/English planet abbreviations to the Zodiac signs, which is much simpler than parsing the multi-column, numeric-heavy Shadbala tables.

---

**Conclusion:** The physical OCR/PDF-extraction layer (`HoroscopeCleaner_Final`) is already doing its job perfectly. The roadblock is the *semantic mapping layer* — code must be written to read the raw `{"type": "table", "rows": [...]}` blocks and structure them into `canonical_content.json`.
