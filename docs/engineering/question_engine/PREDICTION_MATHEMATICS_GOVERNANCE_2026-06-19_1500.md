# PREDICTION MATHEMATICS GOVERNANCE

**Date:** 2026-06-19_1500
**Version:** Phase 9 Step 3E

## SECTION 1: PREDICTION ARCHITECTURE

The Prediction Engine relies on five distinct mathematical pillars. Each pillar contributes to the final evaluation independently, preventing a single failure point from causing a zeroed-out prediction (which occurs in simple multiplication models).

1.  **Natal Promise:** The foundational baseline potential of the domain. If this is zero, no dasha or yoga can manifest the event.
2.  **Activation:** The relevance and strength of the currently running time period (Dasha/Gochara). A strong promise requires activation to manifest.
3.  **Dosha Impact:** The specific frictions, karmic debts, or obstacles penalizing the domain.
4.  **Yoga Support:** The mitigating or accelerating planetary combinations that elevate the baseline promise.
5.  **Confidence:** The reliability metric indicating how consistently the Vargas and underlying factors agree with the primary D1 chart.

---

## SECTION 2: MASTER PREDICTION FORMULA

### Design Principle
The engine explicitly **rejects simple multiplication models** (e.g., `Score = Promise × Activation × Modifier`). A strict multiplication model creates a fragile system where a single zero (e.g., a missing yoga or weak current activation) incorrectly zeroes out a lifelong natal promise.

### The Weighted Normalized Model
The Final Prediction Score is calculated using a dynamic weighted distribution, normalized to a 100-point scale.

**Base Distribution:**
*   **Natal Promise:** 50% (The karmic baseline)
*   **Activation:** 20% (The current temporal trigger)
*   **Yoga Support:** 15% (The accelerating boosters)
*   **Dosha Impact:** -15% (The maximum allowed penalty deduction)
*   **Confidence:** Applied as a separate reliability metric, not as a direct score modifier.

**Formula Structure:**
`Final Prediction Score = (Natal Promise Score × 0.50) + (Activation Score × 0.20) + (Yoga Support Score × 0.15) - (Net Dosha Impact × 0.15)`

*Advantages:* This model prevents unrealistic score collapses. Even if a Dosha is at maximum severity, it can only deduct 15% from the total score, reflecting reality where people with Doshas still get married or find jobs, albeit with friction.

---

## SECTION 3: NATAL PROMISE CALCULATION

The Natal Promise is normalized on a 0-100 scale by synthesizing the following components:

1.  **Bhava Strength:** The Bhava Bala of the primary house (e.g., 7th house for marriage).
2.  **Bhava Lord Strength:** The Shadbala of the planet ruling the primary house.
3.  **Karaka Strength:** The Shadbala and Dignity of the universal significator (e.g., Venus for marriage).
4.  **Relevant Vargas:** The dignity of the Lord and Karaka in the relevant D-chart (e.g., D9).
5.  **Benefic Influence:** Positive aspects or conjunctions on the Bhava/Lord.
6.  **Malefic Influence:** Negative aspects or conjunctions.

*Normalization Methodology:* Each component is converted to a 0-100 score (e.g., 100% Shadbala = 50 points, 150% Shadbala = 100 points). The components are then weighted according to the Domain Weighting (Section 4).

---

## SECTION 4: DOMAIN WEIGHTING

Different domains prioritize different astrological elements. The weights below define how the 100 points of Natal Promise are constructed.

### Marriage
*   **Bhava Weights (7th):** 20%
*   **Lord Weights (7th Lord):** 30%
*   **Karaka Weights (Venus/Jupiter):** 30%
*   **Varga Weights (D9):** 20%

### Career
*   **Bhava Weights (10th):** 30%
*   **Lord Weights (10th Lord):** 30%
*   **Karaka Weights (Sun/Mercury/Saturn):** 10%
*   **Varga Weights (D10):** 30%

### Wealth
*   **Bhava Weights (2nd, 11th):** 40%
*   **Lord Weights (2nd/11th Lords):** 30%
*   **Karaka Weights (Jupiter):** 10%
*   **Varga Weights (D2, D9):** 20%

### Health
*   **Bhava Weights (6th, 1st):** 30%
*   **Lord Weights (Ascendant Lord):** 40%
*   **Karaka Weights (Sun):** 10%
*   **Varga Weights (D30, D6):** 20%

### Education
*   **Bhava Weights (4th, 5th, 9th):** 30%
*   **Lord Weights:** 30%
*   **Karaka Weights (Mercury, Jupiter):** 20%
*   **Varga Weights (D24):** 20%

### Children
*   **Bhava Weights (5th):** 30%
*   **Lord Weights (5th Lord):** 30%
*   **Karaka Weights (Jupiter):** 20%
*   **Varga Weights (D7):** 20%

### Property
*   **Bhava Weights (4th):** 30%
*   **Lord Weights (4th Lord):** 30%
*   **Karaka Weights (Mars):** 20%
*   **Varga Weights (D4, D16):** 20%

### Spirituality
*   **Bhava Weights (9th, 12th):** 30%
*   **Lord Weights (9th/12th Lords):** 20%
*   **Karaka Weights (Jupiter, Ketu):** 20%
*   **Varga Weights (D20, D9):** 30%

---

## SECTION 5: DOSHA IMPACT MODEL

Binary (Yes/No) doshas are forbidden. All doshas are calculated on a 0-100 severity scale. The maximum allowed penalty from all combined Doshas is capped at 15 points in the Final Prediction Score.

**Formula:**
`Net Impact Score = Max(0, Severity Score - Cancellation Score)`

### Examples
*   **Kuja Dosha:** Mars in 7th (Severity 80). Jupiter aspects Mars (Cancellation 50). Net Impact: 30.
*   **Kalasarpa Dosha:** All planets between nodes (Severity 100). Moon outside axis (Cancellation 40). Net Impact: 60.
*   **Guru Chandal:** Jupiter conjunct Rahu (Severity 90). Jupiter in own sign Sagittarius (Cancellation 70). Net Impact: 20.
*   **Papakartari:** 10th house hemmed (Severity 70). Venus aspects 10th (Cancellation 30). Net Impact: 40.
*   **Pitru Dosha:** Sun conjunct Rahu in 9th (Severity 95). No benefic aspects (Cancellation 0). Net Impact: 95.

---

## SECTION 6: YOGA SUPPORT MODEL

Yogas act as accelerators. They are scored and weighted to contribute up to 15% of the Final Prediction Score.

*   **Yoga Strength Score (0-100):** Based on the Shadbala of the participating planets and their dignity.
*   **Yoga Relevance Score (0-100):** Does this yoga directly impact the question? (A Dhana Yoga helps a Wealth question but is irrelevant to a Health question).
*   **Domain Relevance Score:** `Yoga Strength × Yoga Relevance`.

---

## SECTION 7: CONFLICT RESOLUTION GOVERNANCE

When Vargas conflict with the D1 chart, strict resolution precedence must be followed:

1.  **D1 Strong, D9 Weak:** Indicates a strong surface promise that degrades over time or lacks internal strength. Prediction Score is moderately reduced, and Confidence is lowered.
2.  **D1 Weak, D10 Strong:** Initial struggle in career, but eventual immense success through perseverance. Confidence is moderate, Timing engine delays the peak output.
3.  **D1 Moderate, D60 Strong:** D60 acts as the ultimate karmic tie-breaker. A strong D60 elevates the Natal Promise by 10-15 points and sets Confidence to High.

---

## SECTION 8: CONFIDENCE SCORE MODEL

Confidence is NOT the prediction itself. It measures how reliable and stable the prediction is. 

**Factors Evaluated:**
*   **Varga Agreement:** Do D1, D9, and specific D-charts tell the same story?
*   **Planetary Consistency:** Are the Lord and Karaka both strong, or is one supporting while the other destroys?
*   **Dosha Consistency:** Are there hidden Doshas in the Vargas that don't appear in D1?

**Confidence Tiers:**
*   **High Confidence (>85%):** Unified alignment across D1, Vargas, and Karakas.
*   **Medium Confidence (50-85%):** Mixed signals, typical of most charts. Prediction relies heavily on current Activation.
*   **Low Confidence (<50%):** Direct contradictions (e.g., Exalted in D1, Debilitated in D9 with heavy Dosha). The prediction is highly volatile.

---

## SECTION 9: TIMING GOVERNANCE

Timing Activation constitutes 20% of the Final Prediction Score.

### Current MVP
*   **MD (Mahadasha):** Provides the base activation floor (e.g., 10/20 points).
*   **AD (Antardasha):** Provides the specific trigger (e.g., +7 points).
*   **PD (Pratyantardasha):** Provides the micro-trigger (e.g., +3 points).

### Future Integrations
*   **Gochara:** Will act as a gating multiplier on the Activation score.
*   **Ashtakavarga:** Kakshya transits will fine-tune the PD activation.
*   **Mandali Transit:** Will alter the emotional perception of the timing event.

---

## SECTION 10: WORKED EXAMPLES

### Example 1: Marriage
*   **Promise:** 7th Lord strong, Venus average, D9 excellent. (Score: 82/100)
*   **Activation:** Currently in 7th Lord MD / Venus AD. (Score: 95/100)
*   **Dosha:** Mild Kuja dosha, mostly cancelled. (Net Impact: 15/100)
*   **Yoga:** Strong Malavya Yoga. (Score: 80/100)
*   **Final Score:** `(82 * 0.50) + (95 * 0.20) + (80 * 0.15) - (15 * 0.15) = 41 + 19 + 12 - 2.25 = 69.75` (Highly Favorable)
*   **Confidence:** High (Due to D9 agreement).

### Example 2: Career
*   **Promise:** 10th Lord debilitated, Sun strong, D10 average. (Score: 45/100)
*   **Activation:** 12th Lord MD / 8th Lord AD. (Score: 10/100)
*   **Dosha:** Papakartari on 10th. (Net Impact: 60/100)
*   **Yoga:** None relevant. (Score: 0/100)
*   **Final Score:** `(45 * 0.50) + (10 * 0.20) + (0 * 0.15) - (60 * 0.15) = 22.5 + 2 + 0 - 9 = 15.5` (Severe Struggle)
*   **Confidence:** Medium.

### Example 3: Wealth
*   **Promise:** 2nd Lord exalted, 11th Lord strong. (Score: 90/100)
*   **Activation:** Jupiter MD. (Score: 70/100)
*   **Dosha:** Kalasarpa fully cancelled. (Net Impact: 0/100)
*   **Yoga:** Massive Dhana Yoga. (Score: 95/100)
*   **Final Score:** `(90 * 0.50) + (70 * 0.20) + (95 * 0.15) - (0 * 0.15) = 45 + 14 + 14.25 - 0 = 73.25` (Excellent)
*   **Confidence:** High.

### Example 4: Health
*   **Promise:** Ascendant Lord weak, 6th Lord strong. (Score: 30/100)
*   **Activation:** 6th Lord MD. (Score: 80/100)
*   **Dosha:** None. (Net Impact: 0/100)
*   **Yoga:** Vipareeta Raja Yoga. (Score: 40/100)
*   **Final Score:** `(30 * 0.50) + (80 * 0.20) + (40 * 0.15) - (0) = 15 + 16 + 6 = 37` (Health Crisis, but survival indicated by Vipareeta).
*   **Confidence:** High.

---

## SECTION 11: FORMULA GOVERNANCE

All future formulas developed for the Formula Repository MUST inherit these mathematical rules. The Question Engine is strictly prohibited from creating independent, isolated scoring systems. Every prediction must map back to the `Final Prediction Score` weighted normalized architecture to ensure systemic stability.
