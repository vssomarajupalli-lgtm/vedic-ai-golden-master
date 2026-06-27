# GOVERNANCE REFINEMENT REVIEW

## A. Parashari Methodology Review

**1. Promise Engine Refinement**
*   **Analysis:** Excellent. Adding Functional Nature and Affliction Strength correctly aligns with the Parashari concept of *Karako Bhava Nasaya* and functional malefics. A strong house lord that is functionally malefic (e.g., 6th lord) will destroy the house it sits in. Excluding afflictions previously meant the engine would blindly rate a house as "Strong" just because the lord was exalted, ignoring that it was sitting with Rahu/Ketu.
*   **Risk:** None. This mathematically hardens the Truth Layer.

**2. Dasha Governance Refinement**
*   **Analysis:** Highly accurate. Parashara states that Dasha brings the fruits of the natal chart. The exact same Jupiter Mahadasha can make one person a billionaire and another person bankrupt, depending entirely on the Dasha Lord's natal dignity. Shifting the definition from "creates promise" to "identifies activation periods" is perfectly aligned.

**3. Mandali Governance Hardening (The Major Risk)**
*   **Analysis:** The strict ban on Mandali altering probability scores is mathematically sound. However, there is a major Parashari risk regarding **Micro-Timing**.
*   **Risk:** Parashari timing relies on "Double Transit Theory" (e.g., Jupiter and Saturn both aspecting the 7th house) to trigger the *exact month* an event occurs within a broader 3-year Dasha window. If Mandali is totally excluded from the Question Engine's core formulas, the Question Engine can only predict "Event will happen between 2028-2031" (Dasha). It will lose the ability to say "Event will happen in March 2029" (Transit trigger).
*   **Recommendation Before Freeze:** Clarify the governance to state that Mandali cannot alter *probability* (Will it happen?), but it *can* be used to filter *active time-windows* (When exactly within the Dasha will it happen?).

---

## B. Long-Term Software Architecture Review

**1. Total Decoupling**
*   **Analysis:** The frozen four-layer architecture (Promise -> Dasha -> Question -> Mandali) is exceptionally scalable. By strictly isolating the `TransitEngine` from the `FormulaEvaluator`, we prevent circular dependencies and avoid massive performance bottlenecks where evaluating a question required calculating ephemeris data for the next 50 years.

**2. Question Result Model Integration**
*   **Analysis:** The A-B-C-D reporting structure creates a clean, deterministic pipeline for the Answer Composer (LLM). The LLM is fed the Promise data, the Dasha timeline, the frozen Conclusion, and *then* the Mandali JSON as supplementary flavor text.
*   **Risk:** Disjointed UX. If the Question Engine strictly concludes "High Probability of Career Success" based on Dasha, but the optional Mandali commentary notes a severe *Sade Sati* (Saturn transit) causing immense depression and delays during that exact window, the final response might sound contradictory to the user.
*   **Recommendation Before Freeze:** Ensure the Answer Composer is explicitly instructed in its system prompt to synthesize the deterministic Question Conclusion with the Mandali commentary smoothly (e.g., "You have a high probability of success this year, *but* the current transit indicates you will face severe delays before the breakthrough occurs"). The LLM handles the synthesis; the mathematical engines remain isolated.
