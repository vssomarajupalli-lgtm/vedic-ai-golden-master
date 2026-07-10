# FORMULA WEIGHTING GOVERNANCE
**Date:** 2026-06-19_1700
**Version:** Phase 9 Step 3G

## SECTION 1: WEIGHTING PHILOSOPHY
Astrological factors do not possess equal deterministic influence over an event. A strong Karaka cannot singlehandedly manifest a marriage if the 7th Bhava is completely destroyed. Therefore, a rigid, domain-specific weighting model is required to synthesize raw Shadbala, Bhava Bala, and Varga strength into a normalized Natal Promise score.
**Categorization:**
*   **Primary Factors:** The absolute core drivers (typically the primary Bhava and its Lord) carrying the heaviest weight.
*   **Secondary Factors:** Supporting elements (Karakas, supporting Bhavas) providing context and momentum.
*   **Modifiers:** Yogas (Accelerators) and Doshas (Brakes) applied after the base promise is calculated.

## SECTION 2: MARRIAGE WEIGHTING (MAR_PROMISE_001)
**Base Promise Weighting:**
*   **7th House (Bhava Bala):** 25%
*   **7th Lord (Shadbala & Dignity):** 25%
*   **Venus (Male) / Jupiter (Female) (Karaka):** 20%
*   **D9 (Navamsha Dignity of 7th Lord/Karaka):** 30%
*Total: 100%*

**Modifiers (Applied to Total Score):**
*   **Marriage Yogas (e.g., Malavya):** Up to +15%
*   **Marriage Doshas (e.g., Kuja Dosha):** Up to -15%
*   **Cancellation Rules:** Direct benefic aspects halve the Dosha penalty.

## SECTION 3: CAREER WEIGHTING (CAR_PROMISE_001)
**Base Promise Weighting:**
*   **10th House (Status):** 20%
*   **10th Lord:** 25%
*   **6th House (Service) / 2nd House (Income):** 10%
*   **Sun / Mercury / Saturn (Karakas):** 15%
*   **D10 (Dashamsha):** 25%
*   **D24 (Skills):** 5%
*Total: 100%*

**Modifiers:**
*   **Career Yogas (e.g., Bhadra, Ruchaka):** Up to +15%
*   **Career Doshas (e.g., Kalasarpa):** Up to -15%

## SECTION 4: WEALTH WEIGHTING (FIN_WEALTH_001)
**Base Promise Weighting:**
*   **2nd House (Accumulation):** 20%
*   **11th House (Gains):** 20%
*   **5th House (Speculation) / 9th House (Fortune):** 15%
*   **Jupiter / Venus / Mercury (Karakas):** 15%
*   **D2 (Hora):** 15%
*   **D10 / D9:** 15%
*Total: 100%*

**Modifiers:**
*   **Dhana Yogas:** Up to +15%
*   **Financial Doshas (e.g., Guru Chandal):** Up to -15%

## SECTION 5: HEALTH WEIGHTING (HEA_HEALTH_001)
**Base Promise Weighting:**
*   **1st House (Vitality):** 25%
*   **6th House (Disease) / 8th House (Longevity):** 25%
*   **Moon (Mind) / Sun (Body) / Saturn (Chronic):** 20%
*   **D6 (Shashthamsha):** 15%
*   **D30 (Trishamsha):** 15%
*Total: 100%*

**Modifiers:**
*   **Health Yogas (e.g., Vipareeta):** Up to +15% (Protective)
*   **Health Doshas (e.g., Papakartari on Lagna):** Up to -15%

## SECTION 6: EDUCATION WEIGHTING
**Base Promise Weighting:**
*   **4th House (Basic) / 5th House (Intellect):** 30%
*   **Mercury / Jupiter (Karakas):** 30%
*   **D24 (Chaturvimshamsha):** 40%
*Total: 100%*

## SECTION 7: CHILDREN WEIGHTING
**Base Promise Weighting:**
*   **5th House:** 30%
*   **5th Lord:** 25%
*   **Jupiter (Karaka):** 20%
*   **D7 (Saptamsha):** 25%
*Total: 100%*

## SECTION 8: PROPERTY WEIGHTING
**Base Promise Weighting:**
*   **4th House:** 35%
*   **4th Lord:** 25%
*   **Mars (Land):** 20%
*   **D4 (Chaturthamsha):** 20%
*Total: 100%*

## SECTION 9: SPIRITUALITY WEIGHTING
**Base Promise Weighting:**
*   **9th House (Dharma) / 12th House (Moksha):** 30%
*   **Jupiter / Ketu (Karakas):** 30%
*   **D9 (Navamsha) / D20 (Vimshamsha):** 30%
*   **D60 (Shashtiamsha):** 10%
*Total: 100%*

## SECTION 10: DOSHA PENALTY GOVERNANCE
Doshas are not boolean triggers. They execute along severity bands. The maximum allowable penalty from any combination of Doshas is capped at -15% of the total prediction score to prevent unrealistic mathematical collapse.

**Severity Bands (Post-Cancellation):**
*   **Very Low:** -1%
*   **Low:** -5%
*   **Moderate:** -8%
*   **High:** -12%
*   **Severe:** -15% (Hard Limit)

**Governed Doshas:** Kuja, Kalasarpa, Guru Chandal, Papakartari, Pitru.

## SECTION 11: YOGA BONUS GOVERNANCE
Yogas function as accelerators. To prevent unrealistic score inflation, their maximum allowable contribution is capped at +15%.

**Bonus Bands:**
*   **Weak Yoga:** +2%
*   **Moderate Yoga:** +5%
*   **Strong Yoga:** +10%
*   **Exceptional Yoga:** +15% (Hard Limit)

## SECTION 12: CONFLICT GOVERNANCE
Weighting adjustments for contradiction scenarios:
*   **Strong D1 + Weak D9:** Initial weight holds, but Confidence multiplier is reduced (-20%). Manifestation experiences decay over time.
*   **Strong D10 + Weak D1:** Base weight suffers, but D10 strength delays the positive outcome to later Dasha periods. (Delayed Success curve).
*   **Strong Yoga + Strong Dosha:** Accelerators and Brakes run simultaneously. The system adds Yoga (+X%) and subtracts Dosha (-Y%) creating high-volatility events (e.g., sudden massive wealth followed by sudden litigation).

## SECTION 13: NORMALIZATION GOVERNANCE
It is mathematically impossible for the Question Engine to output a score outside the **0–100** boundary.
*   If sum(Weights + Yogas - Doshas) > 100: Cap at 100.
*   If sum(Weights + Yogas - Doshas) < 0: Floor at 0.

## SECTION 14: DOMAIN COMPARISON TABLE
| Domain | Bhava Weight | Lord Weight | Karaka Weight | Varga Weight |
| :--- | :--- | :--- | :--- | :--- |
| **Marriage** | 25% | 25% | 20% | 30% |
| **Career** | 30% | 25% | 15% | 30% |
| **Wealth** | 55% | 0%* | 15% | 30% |
| **Health** | 50% | 0%* | 20% | 30% |
| **Education**| 30% | 0%* | 30% | 40% |
| **Children** | 30% | 25% | 20% | 25% |
| **Property** | 35% | 25% | 20% | 20% |
| **Spiritual**| 30% | 0%* | 30% | 40% |
*(Note: Lord weights are often merged into Bhava calculation for these specific base models).* 

## SECTION 15: FUTURE ADAPTABILITY
The weighting architecture is completely decoupled from execution. Future layers can modify the *modifiers* without breaking the baseline governance:
*   **Gochara:** Adds a multiplier (0.0 to 1.0) to the Activation timing block.
*   **Ashtakavarga:** Acts as a boolean gate (If SAV < 28, cap maximum activation score at 60%).
*   **Mandali Transit Model:** Acts as a modifier for the Dosha severity band.
*   **AI Ranking Layer:** Reweights the 14 Domains against each other based on holistic textual synthesis.

