# TIMING ARCHITECTURE ANALYSIS

## 1. Timing Variant Dependency Chains

### A. `MAR_TIMING_BASE` (Marriage)
1. **Promise:** `7th_house`, `7th_lord`, `venus`, `lagna_lord`
2. **Dasha Activation:** `dasha_lord_aspect_7th`, `dasha_lord_is_venus`
3. **Transit Dependency:** `jupiter_transit_7th_lagna`
4. **Can function without transit?** Yes.

### B. `CAR_CHANGE_TIMING` (Career)
1. **Promise:** `10th_house`, `11th_house`
2. **Dasha Activation:** `positive_dasha`, `dasha_lords_connect_5th_9th`
3. **Transit Dependency:** `transit_saturn_jupiter_activate_10th`
4. **Can function without transit?** Yes.

### C. `AST_PROP_TIMING` (Property)
1. **Promise:** `4th_house`, `2nd_house`, `11th_house`, `mars`
2. **Dasha Activation:** `dasha_activates_4th`, `2nd_11th_lord_activation`
3. **Transit Dependency:** `transit_jupiter_saturn_activate_4th`
4. **Can function without transit?** Yes.

### D. `HLT_RECOVERY_TIMING` (Health)
1. **Promise:** `lagna`, `lagna_lord`, `sun`
2. **Dasha Activation:** `positive_dasha`
3. **Transit Dependency:** `transit_jupiter_aspect_lagna`
4. **Can function without transit?** Yes.

### E. `FAM_CHILD_TIMING` (Progeny)
1. **Promise:** `5th_house`, `9th_house`, `jupiter`
2. **Dasha Activation:** `dasha_activates_5th_9th`
3. **Transit Dependency:** `transit_jupiter_aspect_5th_9th`
4. **Can function without transit?** Yes.

### F. Pure Dasha Variants (Already Transit-Free)
*   **`TRV_TIMING`** (Travel): Relies only on `dasha_activates_3rd_9th_12th`.
*   **`EDU_EXAM_SUCCESS_TIMING`** (Education): Relies only on `dasha_activates_5th_6th`.
*   **`LIT_CONFLICT_TIMING`** (Litigation): Relies only on `dasha_activates_6th`.

---

## 2. Removing Transit: Mathematical Feasibility

**Yes, the timing variants can mathematically function using ONLY Promise + Dasha (MD/AD/PD).**

In Vedic Astrology, the Vimshottari Dasha system dictates the timeline of one's life. 
*   **Mahadasha (MD):** Broad theme (6-20 years)
*   **Antardasha (AD):** Specific manifestation (1-3 years)
*   **Pratyantardasha (PD):** Granular trigger (1-6 months)

By traversing the MD -> AD -> PD sequence, the Question Engine can pinpoint the exact *season* an event is statistically likely to occur, relying solely on static natal calculations. 

**Unnecessary Layers to be Stripped:**
*   `jupiter_transit_7th_lagna`
*   `transit_saturn_jupiter_activate_10th`
*   `transit_jupiter_saturn_activate_4th`
*   `transit_jupiter_aspect_lagna`
*   `transit_jupiter_aspect_5th_9th`

---

## 3. Timing Architecture Comparison

### Option A: Timing = Promise + Dasha
*(Mandali completely decoupled from Question Engine probability)*

*   **Parashari Alignment:** Perfectly aligned with the core tenet: *"That which is promised in the chart is delivered by the Dasha."* If the Dasha does not support the event, no transit can force it to happen.
*   **Project Goals:** Highly performant. The Question Engine executes at lightning speed because it only calculates the 3 active Dasha lords rather than running ephemeris projections for 50 years of transiting planets.
*   **Drawback:** PD (Pratyantardasha) is extremely sensitive to birth time accuracy (a 4-minute error can shift a PD by weeks). 

### Option B: Timing = Promise + Dasha + Transit
*(Mandali integrated into Question Engine boolean logic)*

*   **Parashari Alignment:** Aligned with K.N. Rao's *Double Transit Theory*, which states an event only materializes when Jupiter and Saturn simultaneously aspect the relevant house during an active Dasha.
*   **Project Goals:** Fails system decoupling. It forces the boolean math engine to calculate real-time planetary positions (ephemeris), creating a massive bottleneck.
*   **Drawback:** Violates the separation of concerns. The mathematical probability of "Will this happen?" becomes permanently entangled with "Where is Saturn right now?"

## 4. Final Conclusion & Recommendation

**Option A is the correct architectural choice.**

The Question Engine must predict *Probability* based on Promise + Dasha. 

Mandali must be isolated into an Independent Advisory Module. Instead of being a boolean requirement (`True`/`False`) inside the math engine, Mandali should ingest the active Dasha window (e.g., "June 2028 - Oct 2029") and output a natural language array of transit triggers during that window. The LLM (Answer Composer) will synthesize them.

**Recommendation:** Proceed with the **Mandali Decoupling Refactor** to convert all variants to Option A.
