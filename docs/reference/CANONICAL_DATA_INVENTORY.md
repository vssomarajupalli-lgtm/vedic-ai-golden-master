# CANONICAL DATA INVENTORY

This document provides a complete inventory of the astrological data currently extracted and mapped from the source PDF into `machine_index.json` and `canonical_content.json`. 

Pursuant to **DR-003**, this inventory determines what must be strictly *extracted* rather than *recalculated*.

---

## 1. Data Category Status

| Category | Status | Details |
| :--- | :--- | :--- |
| **Dasha Data** | **Present** | Structured payload contains active `mahadasha`, `antardasha`, and `pratyantardasha`. Source PDF index confirms massive `dasha_phalithalu` section (Pages 55-84). |
| **Ashtakavarga Data** | **Present** | Structured payload contains full `sav_chart` (bindus per house) and `bav_charts` (bindus per planet). Source PDF index confirms calculation (Pages 20-22) and predictions (Pages 83-84). |
| **Bhava (House) Data** | **Present** | Structured payload maps all 12 houses including `house_type`, `lord`, `occupants`, `aspected_by`, and `sav_points`. Source PDF index confirms `bhava_bala` (Pages 16-19). |
| **Planet Strength Data** | **Partial** | Structured payload maps `sign`, `dignity`, `retrograde`, `combust`, and basic aspect counts. However, full *Shadbala* numeric scores are missing from the JSON despite being listed in the PDF index (`shadbala`, Pages 12-15). |
| **Varga Data** | **Partial** | Structured payload only contains `D9` and `D10`. Source PDF index confirms all 16 vargas (`shodasha_vargas`, Pages 23-50) are available for extraction. |
| **Dosha Data** | **Missing** | No structured dosha payload exists in JSON, nor is there an explicit dosha section identified in `machine_index.json`. |
| **Yoga Data** | **Missing** | No structured yoga payload exists in JSON, nor is there an explicit yoga section identified in `machine_index.json`. |
| **Transit (Gochara) Data**| **Missing** | No structured transit payload exists. The PDF index shows `phalithalu` (Pages 85-87), which may contain transit predictions, but they are not currently parsed. |

---

## 2. DR-003 Extraction Directives

Based on the PDF index (`machine_index.json`) and the "Extraction Over Recalculation" rule, the following calculations MUST be extracted from the canonical source text rather than rebuilt natively in Python:

1.  **Dasha Timings and Predictions**: Pages 55-84 contain exhaustive Dasha evaluation. The `DashaEngine` must NOT calculate Vimshottari temporal math. It must merely read the active periods from the JSON and map them to timing multipliers.
2.  **Shadbala (Planet Strength)**: Pages 12-15 contain exact Shadbala points. Once `HoroscopeCleaner_Final` updates the JSON schema to include these, the `PlanetStrengthEngine` must switch to extracting these raw scores instead of doing its own dignity arithmetic.
3.  **Bhava Bala (House Strength)**: Pages 16-19 contain exact Bhava Bala points. The `HouseStrengthEngine` must be ready to ingest these points directly.
4.  **Ashtakavarga Validation**: Pages 83-84 (`ashtakavarga_vibhagam`) contain predictions.
5.  **Shodasha Vargas**: Pages 23-50 contain all 16 divisional charts. The `VargaEngine` must not attempt to calculate planetary degrees to divisional assignments; it must strictly read the mapped outputs.

### Unresolved Engine Targets (Requires Calculation)

Because they are currently **Missing** from the source extraction mapping, the system *must* calculate the following logically until the canonical data payload provides them:
*   **Dosha Calculations** (Kuja, Kala Sarpa)
*   **Yoga Formations** (Gaja Kesari, etc.)
*   **Transit (Gochara) Scores** (Unless `phalithalu` on pages 85-87 proves to contain explicitly mapped transit values).
