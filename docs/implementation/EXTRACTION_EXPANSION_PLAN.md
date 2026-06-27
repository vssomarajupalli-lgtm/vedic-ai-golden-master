# EXTRACTION EXPANSION PLAN

**Goal:** Audit astrology data present in the canonical source material but missing from the current JSON extraction, focusing on Shadbala, Bhava Bala, and Shodasha Vargas.

---

## 1. Shadbala (Planetary Strength)

*   **Is Shadbala present in source?** Yes.
*   **Exact source location:** `machine_index.json` confirms "shadbala" is located on pages **12 to 15**.
*   **Current JSON availability:** Missing. `canonical_content.json` lacks any numeric Shadbala scores.
*   **Missing extraction fields:**
    *   Total numeric Shadbala points (Rupas / Virupas) for the 7 visible planets.
    *   Breakdown of the 6 sub-balas (Sthana, Dig, Kala, Cheshta, Naisargika, Drik) if needed for explainability.
*   **Cleaner changes required:** The PDF parser/cleaner must be updated to locate the Shadbala tables on pages 12-15, parse the numeric values, and inject a `"shadbala_score"` into each planet object within the JSON payload.

---

## 2. Bhava Bala (House Strength)

*   **Is Bhava Bala present in source?** Yes.
*   **Exact source location:** `machine_index.json` confirms "bhava_bala" is located on pages **16 to 19**.
*   **Current JSON availability:** Missing. `canonical_content.json` lacks any numeric Bhava Bala scores.
*   **Missing extraction fields:** Total numeric Bhava Bala points (Rupas / Virupas) or percentage strengths for all 12 houses.
*   **Cleaner changes required:** The parser must be updated to target the tables on pages 16-19 and inject a `"bhava_bala_score"` into each house object within the JSON payload.

---

## 3. Remaining Shodasha Vargas (Divisional Charts)

*   **Current extracted:** D9 (Navamsha), D10 (Dashamsha).
*   **Existing in source but not extracted:** D2, D3, D4, D7, D12, D16, D20, D24, D27, D30, D40, D45, D60.
*   **Source availability:** `machine_index.json` states "shodasha_vargas" (all 16 divisional charts) span from pages **23 to 50**.
*   **Extraction complexity:** Moderate to High. The parser must identify the headers for the 14 unmapped charts and accurately scrape 9 planetary placements (Sign, Dignity) for each across 27 pages of tables.
*   **JSON schema impact:** Low structural impact, high data volume. The schema already uses a `"vargas"` dictionary. We simply expand the keys from `["D9", "D10"]` to include the remaining divisions `["D2", "D3", "D4", "D7", ... "D60"]`.

---

## 4. Engine Impact Analysis

*   **PlanetStrengthEngine impact:** **Massive.** In strict adherence to **DR-003 (Extraction First)**, once Shadbala is extracted, this engine must immediately stop calculating its own arithmetic proxy score (dignity + house + state) and switch to passing through the raw extracted Shadbala value (normalized to a 0-100 scale).
*   **HouseStrengthEngine impact:** **Massive.** Similar to PlanetStrength, once Bhava Bala is extracted, this engine must cease its internal arithmetic (lord + occupants + SAV) and switch to the raw Bhava Bala score (normalized to 0-100).
*   **VargaEngine impact:** **Significant.** Expanding from 2 to 16 vargas allows the engine to score planetary strength dynamically depending on the life domain queried (e.g., scoring Jupiter in D7 for a children query, or Mercury in D24 for an education query).
*   **NatalPromiseEngine impact:** **Substantial.** Domain promise calculations rely heavily on Varga support. Providing exact D-charts for all 8 life domains will vastly increase precision and replace the current hardcoded D9/D10 fallback mechanisms.
*   **Future Gochara (Transit) impact:** **Moderate.** Transits utilize base planetary strength to determine transit efficacy. Moving to true Shadbala will make transit weighting much more accurate.

---

## 5. Recommended Implementation Order

To safely transition the architecture from arithmetic-proxy to extraction-driven without breaking the pipeline:

1.  **Cleaner Update - Vargas:** Update the PDF cleaner to parse pages 23-50 and populate `D2` through `D60` in the JSON. (Lowest risk, as the schema already supports this format).
2.  **Cleaner Update - Shadbala & Bhava Bala:** Build and test table extractors for pages 12-19. Add raw scores to the JSON.
3.  **JSON Migration Validation:** Verify the new `canonical_content.json` structure against the `PipelineRunner` to ensure no schema-parsing exceptions occur.
4.  **Engine Refactor - Varga & NatalPromise:** Update engines to consume the 14 new divisional charts and map them to their respective domains (Wealth -> D2, Property -> D4, etc.).
5.  **Engine Refactor - Strength Engines (DR-003 Compliance):** Modify `PlanetStrengthEngine` and `HouseStrengthEngine` to check for `shadbala_score`/`bhava_bala_score` in the payload. If present, use it. If missing (fallback), use the legacy arithmetic calculation.

---

## 6. Risk Assessment

*   **Source Ambiguity:** The PDF tables for Shadbala (pages 12-15) are notoriously complex and matrix-heavy. The OCR/parser may struggle to align columns to planets correctly, resulting in swapped or corrupted scores.
*   **Cleaner Risks:** Modifying the `HoroscopeCleaner_Final` regexes or page-targeting bounds could accidentally break the currently working D9/D10 or Ashtakavarga extraction.
*   **JSON Migration Risks:** If the new extraction injects `null` or improperly typed strings (e.g., `"12.5 Rupas"` instead of a `float`) for Shadbala, the `PlanetStrengthEngine` will throw TypeErrors and crash the entire PipelineRunner. *Mitigation:* Strict type coercion and a fallback arithmetic path must be implemented in the engines before the JSON is updated.

## User Review Required
> [!IMPORTANT]
> The audit is complete. Please review the implementation order and risk mitigation strategies (specifically the fallback calculation paths during JSON migration). Do you approve this audit plan?
