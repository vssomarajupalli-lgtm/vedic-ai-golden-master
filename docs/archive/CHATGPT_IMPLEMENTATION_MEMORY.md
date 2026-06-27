# CHATGPT_IMPLEMENTATION_MEMORY

## PURPOSE OF THIS DOCUMENT
This document serves as the single-source-of-truth implementation memory for future AI coding assistants (ChatGPT, Gemini, Claude, Codex, etc.). It strictly defines the current, realistic implementation state of the Vedic Astrology Intelligence Framework. 

Do NOT hallucinate architecture. Do NOT invent speculative future systems. When resuming work, read this document to understand exactly where the project stands.

---

## Phase 16A Conclusion (Architecture Constitution Freeze)
- **Transparency:** Phase 15 Transparency and Formula Verification Console successfully completed.
- **Constitution:** Architecture Constitution fully approved. Governance is frozen.
- **Ownership:** Ownership Matrix and Formula Ownership Register strictly finalized.
- **Dependency Hierarchy:** Engine Dependency Hierarchy permanently frozen as a strict DAG.
- **Contracts:** Engine Output Contracts frozen.
- **Calibration Governance:** Calibration Version Governance and Migration Strategy frozen.
- **Gochara:** Moon-Centered Nine-Pada Mandali Governance frozen.
- **Next Phase:** Phase 16A.3 – Calibration Architecture.

---

## Phase 7 Conclusion (Mandali Gochara & Stabilization)
- **Mandali Gochara Migration:** Successful. Test fixtures updated. No production logic changes were required to mathematical boundaries.
- **Dasha Timeline Contract:** Standardized to a `timeline[]` array successfully.
- **Yoga Engine Contract:** Dignity schema correctly routed via `normalized_payload`.
- **Master Probability Engine Contract:** Varga legacy wrapper mismatches patched to standard `{"D9": {"planets": ...}}`.
- **Final Test Status:** All 613 test suites successfully pass. 0 failures. 0 errors.

---

## 1. Current Real Project Goal
The current practical goal is to build a **deterministic Vedic astrology calculation platform**. 
It must:
- Open and parse immutable astrology PDF reports.
- Extract data safely using an index-driven page boundary strategy.
- Normalize parsed data into strict JSON contracts.
- Calculate explainable planetary (Graha) and house (Bhava) strengths.
- Produce a deterministic, schema-validated JSON output report.

---

## 2. Current Stabilized Architecture
The backend operates as a **Unidirectional Directed Acyclic Graph (DAG)**:
1. **Extraction:** `IndexReader` + `PdfTextExtractor`
2. **Normalization:** `JsonNormalizer`
3. **Orchestration:** `PipelineRunner`
4. **Calculation Engines:** `PlanetStrengthEngine`, `HouseStrengthEngine`, `VargaEngine`

Data flows strictly forward. Engines are stateless. The `PipelineRunner` manages all dependency injection.

---

## 3. Deterministic Philosophy Rules
- **The Immutable D1 Rule:** The natal D1 chart is the foundation. Vargas, Dashas, and Transits are overlays. They must NEVER overwrite D1 base scores.
- **Zero Magic Numbers:** All scoring weights live exclusively in `app/config/astrology_constants.py`.
- **Stateless Engines:** Engines must not retain memory between requests.
- **Safe Math:** All final scores must be clamped (0-100) using `app/utils/astrology_math.py`.
- **No AI in Math:** Calculations are 100% deterministic Python logic. AI is strictly for future text interpretation.

---

## 4. Current Implemented Modules
The following modules are successfully implemented and stabilized:

**Orchestration & Data:**
- `app/pipeline_runner.py`: Sequential pipeline execution and safe dependency passing.
- `app/parsers/json_normalizer.py`: Firewall module enforcing Type, Schema, and Safe Defaults.

**Calculation Engines:**
- `app/engines/planet_strength_engine.py`: Evaluates dignity, state, house placement, and aspects.
- `app/engines/house_strength_engine.py`: Evaluates house type, lord contribution, and occupants.
- `app/engines/varga_engine.py`: Calculates structural capacity modifiers (D9/D10) without mutating D1.

**Extraction Layer:**
- `app/parsers/index_reader.py`: Regex-based parser to find Table of Contents and map deterministic page boundaries.
- `app/parsers/pdf_text_extractor.py`: Defensive, page-by-page raw text extraction tool handling malformed/empty pages.

**Config & Utils:**
- `app/config/astrology_constants.py`
- `app/utils/astrology_math.py`

---

## 5. Current Implemented Tests
Testing utilizes standard `unittest` with isolated, mocked payloads (no live PDF loading required for logic tests):
- `tests/test_pipeline_runner.py`: Verifies DAG execution, D1 Immutability, missing dependency fallbacks.
- `tests/test_index_reader.py`: Verifies Table of Contents regex, page bounds, and junk row rejection.
- `tests/test_pdf_text_extractor.py`: Verifies deterministic page ordering (1-indexed) and defensive crash handling.

---

## 6. Extraction Architecture Strategy
PDF extraction is highly staged to prevent parsing garbage:
1. **Index Mapping:** Find the Table of Contents and calculate `(start_page, end_page)` for all relevant sections.
2. **Targeted Extraction:** Use the calculated page boundaries to extract text ONLY from specific pages.
3. **Table Parsing:** (Pending) Extract structured data (e.g., planetary positions) from those targeted pages.
4. **JSON Structuring:** Convert raw tables into a nested Python dictionary.
5. **Normalization:** Pass to `JsonNormalizer`.

---

## 7. PDF Handling Philosophy
- **Immutable Source:** The source PDF is read-only.
- **Defensive Parsing:** PDF libraries (`pdfplumber`) occasionally fail. Wrappers must use `try/except` and safely ignore corrupt pages.
- **No OCR Yet:** The system relies strictly on digital text extraction. OCR is a future fallback and is out of scope.

---

## 8. Index-Driven Extraction Design
The `IndexReader` is the "map maker." 
Instead of blindly scanning an 80-page PDF for the word "Sun", the pipeline first scans the index. If "Planetary Positions" is mapped to pages 4-6, the downstream `TableParser` will exclusively scan pages 4, 5, and 6. This eliminates false positives and massively speeds up execution.

---

## 9. Current Pending Work
- **Table Extraction:** Implementing `table_parser.py` to convert PDF tables within the established page boundaries into raw dictionaries.
- **Extraction Integration:** Connecting the Extraction Layer (`pdfplumber` components) to the `JsonNormalizer` inside the `PipelineRunner`.

---

## 10. Strict Scope Boundaries
**WHAT WE ARE NOT DOING RIGHT NOW:**
- No UI, frontend, or web framework.
- No Databases (SQL, Mongo, etc.).
- [HISTORICAL] No Dasha (Vimshottari) timeline calculations. (Completed Phase 6)
- [HISTORICAL] No Transit (Gochara) evaluation systems. (Completed Phase 7)
- [HISTORICAL] No complex Event-Domain (Marriage, Career) probability synthesis. (Completed Phase 2 & 8)
- No Generative AI or LLM integration.

---

## 11. Immediate Next Implementation Steps
1. **`table_parser.py`**: Create a deterministic module that accepts page boundaries and extracts planetary alignment grids.
2. **Table Parser Tests**: Write mocked unit tests for table extraction.
3. **Pipeline Integration**: Modify `PipelineRunner` to accept a PDF file path, run extraction, pass the result to the normalizer, and execute engines.
4. **End-to-End Test**: Run a sample PDF through the entire pipeline.

---

## 12. Critical Rules To Prevent Overengineering
- **Build One Engine At A Time:** Finish the PDF extraction pipeline completely before looking at Dashas.
- **No Deep OOP:** Use flat functions, simple classes, and standard Python dictionaries. No complex inheritance chains.
- **Protect the JSON Contract:** Never alter top-level keys without updating global schemas. Engines expect exact keys.

---

## 13. Current Dependency List
Core dependencies (minimal footprint):
- `python 3.x`
- `pdfplumber` (for PDF text/layout extraction)
- `unittest` (standard library, for deterministic isolated testing)
- `re` (standard library, for regex parsing)

---

## 14. Current Known Risks
- **PDF Format Variations:** Different astrology software generates different table layouts. Table parsing logic might become fragile if not heavily regex-protected and abstracted.
- **Regex Corruption:** Complex regex patterns (like in `index_reader.py`) are susceptible to AI hallucination/merge conflicts. Always test regex changes defensively.
- **Schema Drift:** As extraction capabilities expand, the `raw_data` dictionary format may shift, breaking the `JsonNormalizer`.

---

## 15. Recommended Development Order
1. Complete `table_parser.py` (Planetary Grids). (COMPLETED)
2. Integrate Full Pipeline (PDF -> Index -> Extract -> Normalize -> Calculate -> JSON Output). (COMPLETED)
3. *[Milestone: Core System Stable]* (ACHIEVED)
4. Phase 6: Dasha Engine (Timing Multipliers). (COMPLETED - Timeline Array Schema)
5. Phase 7: Transit Engine (Snapshot Triggers). (COMPLETED - Mandali Gochara Implementation)
6. Phase 8: Probability Synthesis Engine (Event Domains). (COMPLETED)
7. Phase 9: AI Interpretation Layer. (PENDING ROADMAP)