# FORMULA REPOSITORY GOVERNANCE

**Date:** 2026-06-19_1600
**Version:** Phase 9 Step 3F

## SECTION 1: FORMULA REPOSITORY PURPOSE
The Formula Repository decouples astrological logic from engine execution. The Question Engine does not contain direct `if house == 7` logic. Instead, the logic flows rigidly as:
**Question → Question ID → Formula ID → Prediction Engine**
This architecture guarantees that astrologers can update parameters in the Formula Repository without requiring Python logic modifications to the Prediction Engine.

---

## SECTION 2: MARRIAGE FORMULAS
### `MAR_PROMISE_001` (Marriage Promise)
*   **Relevant Bhavas:** 7th (Primary), 2nd, 11th
*   **Relevant Lords:** 7th Lord, 2nd Lord, 11th Lord
*   **Relevant Karakas:** Venus (Men), Jupiter (Women)
*   **Relevant Vargas:** D1, D9, D60
*   **Relevant Yogas:** Malavya Yoga, Bheri Yoga
*   **Relevant Doshas:** Kuja Dosha, Kalasarpa

### `MAR_TIMING_001` (Marriage Timing)
*   **Relevant Bhavas:** 7th
*   **Relevant Lords:** 7th Lord
*   **Relevant Karakas:** Venus, Jupiter
*   **Relevant Vargas:** D1, D9
*   **Relevant Yogas:** Vivaha Yogas
*   **Relevant Doshas:** Kuja Dosha (Delay effects)

### `MAR_QUALITY_001` (Marital Harmony)
*   **Relevant Bhavas:** 7th, 4th, 12th
*   **Relevant Lords:** 7th Lord, 4th Lord
*   **Relevant Karakas:** Venus
*   **Relevant Vargas:** D9
*   **Relevant Yogas:** None
*   **Relevant Doshas:** Kuja Dosha, Papakartari on 7th

### `MAR_DELAY_001` (Marriage Delay Factors)
*   **Relevant Bhavas:** 7th
*   **Relevant Lords:** 7th Lord, Saturn (Significator of Delay)
*   **Relevant Karakas:** Saturn, Ketu
*   **Relevant Vargas:** D1, D9
*   **Relevant Yogas:** Daridra Yogas (impacting 7th)
*   **Relevant Doshas:** Kuja Dosha, Kalasarpa

### `MAR_SECOND_MARRIAGE_001` (Second Marriage Promise)
*   **Relevant Bhavas:** 9th, 2nd, 11th
*   **Relevant Lords:** 9th Lord, 2nd Lord
*   **Relevant Karakas:** Venus, Jupiter
*   **Relevant Vargas:** D9
*   **Relevant Yogas:** Multiple marriage yogas
*   **Relevant Doshas:** N/A

---

## SECTION 3: CAREER FORMULAS
### `CAR_PROMISE_001` (Career Prominence)
*   **Relevant Bhavas:** 10th, 1st
*   **Relevant Lords:** 10th Lord, Ascendant Lord
*   **Relevant Karakas:** Sun, Mercury, Saturn
*   **Relevant Vargas:** D1, D10, D60
*   **Relevant Yogas:** Ruchaka, Bhadra, Hamsa, Malavya, Shasha
*   **Relevant Doshas:** Kalasarpa

### `CAR_JOB_001` (Employment Promise)
*   **Relevant Bhavas:** 6th, 10th
*   **Relevant Lords:** 6th Lord, 10th Lord
*   **Relevant Karakas:** Saturn
*   **Relevant Vargas:** D10
*   **Relevant Yogas:** Service-oriented yogas
*   **Relevant Doshas:** Papakartari on 10th

### `CAR_BUSINESS_001` (Business Promise)
*   **Relevant Bhavas:** 7th, 10th, 11th
*   **Relevant Lords:** 7th Lord, 10th Lord
*   **Relevant Karakas:** Mercury
*   **Relevant Vargas:** D10
*   **Relevant Yogas:** Dhan Yogas, Lakshmi Yoga
*   **Relevant Doshas:** Kalasarpa

### `CAR_PROMOTION_001` (Promotion Timing)
*   **Relevant Bhavas:** 11th, 10th
*   **Relevant Lords:** 11th Lord, 10th Lord
*   **Relevant Karakas:** Sun, Jupiter
*   **Relevant Vargas:** D10
*   **Relevant Yogas:** Amala Yoga
*   **Relevant Doshas:** N/A

### `CAR_PROFESSION_SUITABILITY_001` (Field of Work)
*   **Relevant Bhavas:** 10th, 2nd, 11th
*   **Relevant Lords:** 10th Lord, planets placed in 10th
*   **Relevant Karakas:** Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn
*   **Relevant Vargas:** D10, D24
*   **Relevant Yogas:** Specific planetary yogas
*   **Relevant Doshas:** N/A

---

## SECTION 4: WEALTH FORMULAS
### `FIN_WEALTH_001` (Overall Wealth Promise)
*   **Relevant Bhavas:** 2nd, 11th, 9th, 5th
*   **Relevant Lords:** 2nd Lord, 11th Lord, 9th Lord
*   **Relevant Karakas:** Jupiter
*   **Relevant Vargas:** D1, D2, D9, D10
*   **Relevant Yogas:** Dhana Yogas, Lakshmi Yoga
*   **Relevant Doshas:** Kalasarpa, Guru Chandal, Daridra Yogas

### `FIN_INCOME_001` (Regular Income)
*   **Relevant Bhavas:** 11th
*   **Relevant Lords:** 11th Lord
*   **Relevant Karakas:** Jupiter, Venus
*   **Relevant Vargas:** D1, D2
*   **Relevant Yogas:** Dhana Yogas
*   **Relevant Doshas:** Papakartari on 11th

### `FIN_BUSINESS_GAIN_001` (Gains from Business)
*   **Relevant Bhavas:** 7th, 11th
*   **Relevant Lords:** 7th Lord, 11th Lord
*   **Relevant Karakas:** Mercury
*   **Relevant Vargas:** D1, D10, D2
*   **Relevant Yogas:** Vasumathi Yoga
*   **Relevant Doshas:** N/A

### `FIN_INVESTMENT_001` (Investment/Speculation)
*   **Relevant Bhavas:** 5th, 8th, 11th
*   **Relevant Lords:** 5th Lord, 8th Lord
*   **Relevant Karakas:** Rahu, Mercury
*   **Relevant Vargas:** D1, D2
*   **Relevant Yogas:** Dhana Yogas involving 5th
*   **Relevant Doshas:** Kalasarpa

---

## SECTION 5: HEALTH FORMULAS
### `HEA_HEALTH_001` (General Vitality)
*   **Relevant Bhavas:** 1st, 6th
*   **Relevant Lords:** 1st Lord
*   **Relevant Karakas:** Sun, Moon
*   **Relevant Vargas:** D1, D6, D30
*   **Relevant Yogas:** None
*   **Relevant Doshas:** Papakartari on Lagna

### `HEA_DISEASE_RISK_001` (Chronic Illness Risk)
*   **Relevant Bhavas:** 6th, 8th, 12th
*   **Relevant Lords:** 6th Lord, 8th Lord, 12th Lord
*   **Relevant Karakas:** Saturn, Rahu, Ketu
*   **Relevant Vargas:** D1, D30
*   **Relevant Yogas:** Balarishta (for early life)
*   **Relevant Doshas:** Kuja Dosha, Papakartari

### `HEA_RECOVERY_001` (Recovery Strength)
*   **Relevant Bhavas:** 1st, 5th, 9th, 11th
*   **Relevant Lords:** 1st Lord, 11th Lord
*   **Relevant Karakas:** Sun, Jupiter
*   **Relevant Vargas:** D1, D6
*   **Relevant Yogas:** Vipareeta Raja Yoga
*   **Relevant Doshas:** N/A

---

## SECTION 6: EDUCATION FORMULAS
### `EDU_PROMISE_001` (Higher Education)
*   **Relevant Bhavas:** 4th, 5th, 9th
*   **Relevant Lords:** 4th Lord, 5th Lord, 9th Lord
*   **Relevant Karakas:** Mercury, Jupiter
*   **Relevant Vargas:** D1, D24
*   **Relevant Yogas:** Saraswati Yoga, Kalanidhi Yoga
*   **Relevant Doshas:** Guru Chandal

---

## SECTION 7: CHILDREN FORMULAS
### `CHI_PROMISE_001` (Progeny Promise)
*   **Relevant Bhavas:** 5th, 9th
*   **Relevant Lords:** 5th Lord, 9th Lord
*   **Relevant Karakas:** Jupiter
*   **Relevant Vargas:** D1, D7
*   **Relevant Yogas:** None
*   **Relevant Doshas:** Pitru Dosha, Kalasarpa

---

## SECTION 8: PROPERTY FORMULAS
### `PRO_PROMISE_001` (Real Estate Promise)
*   **Relevant Bhavas:** 4th, 11th
*   **Relevant Lords:** 4th Lord, 11th Lord
*   **Relevant Karakas:** Mars (Land), Venus (Vehicles)
*   **Relevant Vargas:** D1, D4, D16
*   **Relevant Yogas:** Vahana Yoga
*   **Relevant Doshas:** Kuja Dosha

---

## SECTION 9: SPIRITUAL FORMULAS
### `SPI_PROMISE_001` (Spiritual Inclination)
*   **Relevant Bhavas:** 9th, 12th, 8th
*   **Relevant Lords:** 9th Lord, 12th Lord
*   **Relevant Karakas:** Jupiter, Ketu, Saturn
*   **Relevant Vargas:** D1, D9, D20, D60
*   **Relevant Yogas:** Sanyasa Yogas, Tapaswi Yoga
*   **Relevant Doshas:** Guru Chandal

---

## SECTION 10: DOSHA FORMULAS

### `DOS_KUJA_001` (Kuja Dosha)
*   **Severity Inputs:** Mars in 1st, 2nd, 4th, 7th, 8th, 12th from Ascendant, Moon, or Venus.
*   **Cancellation Inputs:** Mars in own sign/exaltation; Jupiter aspecting Mars; strong Ascendant lord.
*   **Affected Domains:** Marriage, Property, Health.

### `DOS_KALASARPA_001` (Kalasarpa Dosha)
*   **Severity Inputs:** All planets hemmed between Rahu and Ketu axis.
*   **Cancellation Inputs:** A strong benefic outside the axis; strong Ascendant and 9th Lord.
*   **Affected Domains:** Master Life Analysis, Wealth, Career.

### `DOS_GURU_CHANDAL_001` (Guru Chandal Dosha)
*   **Severity Inputs:** Jupiter conjunct or mutual aspect with Rahu/Ketu.
*   **Cancellation Inputs:** Jupiter retrograde, exalted, or aspected by strong benefic.
*   **Affected Domains:** Education, Wealth, Spirituality.

### `DOS_PAPAKARTARI_001` (Papakartari Dosha)
*   **Severity Inputs:** Any Bhava or Planet hemmed between two malefics (e.g., Saturn and Mars).
*   **Cancellation Inputs:** Benefic aspecting the hemmed planet/house.
*   **Affected Domains:** Depends on the specific Bhava/Planet affected.

### `DOS_PITRU_001` (Pitru Dosha)
*   **Severity Inputs:** Sun or 9th Lord afflicted by Rahu/Saturn in 9th House.
*   **Cancellation Inputs:** Jupiter aspecting the 9th House or Sun.
*   **Affected Domains:** Master Life Analysis, Children, Wealth.

---

## SECTION 11: FORMULA DEPENDENCY MATRIX

| Question ID | Formula ID | Required Engines | Required Vargas |
| :--- | :--- | :--- | :--- |
| **MAR_001** | `MAR_PROMISE_001`, `MAR_TIMING_001` | House Engine, Planet Engine, Dasha Engine | D1, D9, D60 |
| **CAR_001** | `CAR_PROMISE_001`, `CAR_TIMING_001` | House Engine, Planet Engine, Dasha Engine | D1, D10, D60 |
| **FIN_001** | `FIN_WEALTH_001`, `FIN_TIMING_001` | House Engine, Planet Engine, Dasha Engine | D1, D2, D9, D10 |
| **HEA_001** | `HEA_HEALTH_001`, `HEA_TIMING_001` | House Engine, Planet Engine, Dasha Engine | D1, D6, D30 |
| **EDU_001** | `EDU_PROMISE_001`, `EDU_TIMING_001` | House Engine, Planet Engine, Dasha Engine | D1, D24 |
| **CHI_001** | `CHI_PROMISE_001`, `CHI_TIMING_001` | House Engine, Planet Engine, Dasha Engine | D1, D7 |
| **PRO_001** | `PRO_PROMISE_001`, `PRO_TIMING_001` | House Engine, Planet Engine, Dasha Engine | D1, D4, D16 |

---

## SECTION 12: FUTURE EXTENSIONS

The Formula Repository is built to naturally accept the following future layers:

1.  **Gochara:** Adds transit conditions to the `TIMING_001` formulas.
2.  **Ashtakavarga:** Adds minimum SAV/BAV thresholds to `PROMISE_001` and `TIMING_001` formulas.
3.  **Mandali Transit Model:** Integrates emotional trigger conditions into the prediction narrative.
4.  **Compatibility Engine:** Will cross-reference two independent Formula Repositories for match-making.
5.  **AI Ranking Layer:** LLM-based prioritization of `PROMISE_001` outputs based on holistic chart synthesis.
