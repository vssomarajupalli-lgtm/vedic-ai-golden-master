---
archive_title: "GOCHARA ARCHITECTURE AUDIT & DOSHA RE-EVALUATION"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "docs/knowledge/TRANSIT_ENGINE_KNOWLEDGE_PACKAGE.md"
---

# GOCHARA ARCHITECTURE AUDIT & DOSHA RE-EVALUATION

Based on the Domain Expert's clarification, the prior conclusions regarding the Dosha Engine and Transit Engine have been re-evaluated. This document audits the existing layers, source data, and missing proprietary logic to enforce the DR-003 Extraction-First mandate.

---

## 1. DOSHA ENGINE RE-EVALUATION

**Prior Conclusion**: "Dosha Engine is missing. We must calculate Kuja Dosha from raw planet placements."
**Revised Conclusion**: Incorrect. Kuja Dosha is already declared in the source PDF. Attempting to natively recalculate it violates the extraction-first architecture.

### Audit Findings:
*   **Existing Source Data**: Planet placements are already fully available. According to the domain expert, Kuja Dosha status is explicitly declared in the source PDF.
*   **Existing Implementation**: No `DoshaEngine` currently exists in `backend/app/engines/`.
*   **Missing Extraction**: The `HoroscopeCleaner_Final` parser needs to be updated to extract the explicit Kuja Dosha declaration (e.g., as a boolean or string value) from the PDF and map it into the `canonical_content.json` payload.
*   **Missing Calculations**: Rather than calculating the dosha from scratch using complex house/aspect rules, the `DoshaEngine` simply needs to read the extracted declaration and apply the appropriate probability penalties/modifiers to the relevant life domains (e.g., Marriage).

---

## 2. GOCHARA (TRANSIT) ENGINE RE-EVALUATION

**Prior Conclusion**: "Transit Engine is a standard gochara planetary house calculator that needs to be refactored to read generic transit text."
**Revised Conclusion**: Incorrect. The Gochara system is a multi-layered proprietary engine. It relies heavily on Nakshatra Pada logic, not just classical Rasi/House transits.

### Audit Findings:

#### A. Classical Transit Layer
*   **Existing Implementation**: `transit_engine.py` currently implements classical Parashari Gochara (House Quality, Conjunctions, Aspects) and Vedha Obstructions.
*   **Existing Source Data**: None directly mapped in the JSON, but `phalithalu` (Pages 85-87) is indexed in the PDF.
*   **Missing Extraction**: We need to parse the `phalithalu` pages to determine if classical transit predictions are already provided.

#### B. Samartha True Micro Gochara & Pada-Based Rules
*   **Existing Implementation**: Completely missing. `transit_engine.py` operates strictly on Rasi (Sign) and Bhava (House) mathematics.
*   **Missing Proprietary Rule Implementations**: Section 2 of `GOCHARA_ENGINE_MASTER.md` explicitly dictates that the engine MUST use "Moon nakshatra pada based logic rather than simple rasi-only logic." The center reference point must be the native's Moon pada, mapping surrounding zones across the 27-pada framework. This is entirely absent from the codebase.

#### C. Ashtakavarga Validation (BAV)
*   **Existing Implementation**: Present. `transit_engine.py` already checks transit planet positions against the `bav_charts` provided by `AshtakavargaEngine`.
*   **Existing Source Data**: Full SAV and BAV charts are successfully extracted in `canonical_content.json`.

#### D. Elinati Saturn (Sadesati) Logic
*   **Existing Implementation**: Partial/Stub. `transit_engine.py` only sets a `"saturn_sadesati"` confidence flag if Saturn transits houses 12, 1, or 2 from the natal Moon sign.
*   **Missing Proprietary Rule Implementations**: `GOCHARA_ENGINE_MASTER.md` demands an "Elinati Shani builder" (Section 10.7) capable of determining precise start/end dates and detailed phase mapping, rather than just a simplistic runtime flag.

#### E. Domain Trigger Logic (Dasha-Transit Sync)
*   **Existing Implementation**: Present. `transit_engine.py` aligns transit planets with active Mahadasha and Antardasha lords to generate bonus multipliers. It successfully maps final transit activation scores to the 8 Life Domains using primary/support house logic.

---

## 3. REQUIRED ACTION PATH

1.  **Halt Dosha Calculation**: Do not write mathematical rules for Kuja Dosha. Wait for or implement the extraction parser update to pull the declaration directly from the PDF.
2.  **Halt Classical Gochara Expansion**: Do not expand the Rasi-based transit engine.
3.  **Acknowledge Proprietary Gap**: The largest missing calculation is the **Pada-Based Micro Gochara Belt Mapping**. Since this logic does not exist in standard Rasi charts, the Transit Engine must be completely redesigned around the 27-Nakshatra Pada framework, using the natal Moon Pada as the anchor, as mandated by the `GOCHARA_ENGINE_MASTER.md`.
