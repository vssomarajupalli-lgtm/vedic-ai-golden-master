# NATAL PROMISE VALIDATION AUDIT

## 1. Executive Summary

This document presents a technical and astrological audit of the **NatalPromiseEngine** (`backend/app/engines/natal_promise_engine.py`) across all eight life domains. It evaluates the current formulas, highlights the expected classical Vedic factors, identifies critical omissions and oversimplifications, and grades the severity and prediction impact of these discrepancies.

---

## 2. Domain-by-Domain Audits

### 1. Marriage (`marriage`)

* **Current Implemented Formula**:
  $$\text{Score} = 0.30 \cdot \text{House 7} + 0.20 \cdot \text{avg(House 2, 11)} + 0.25 \cdot \text{avg(Venus, Jupiter)} + 0.15 \cdot \text{Lord 7} + 0.05 \cdot \text{D9} + 0.05 \cdot \text{SAV 7} + \text{Bonuses} + \text{Penalties}$$
  * *Afflictions*: Saturn, Mars, Rahu, or Ketu in 7; Venus combust (capped at -25).
  * *Bonuses*: Jupiter aspects 7 (+8); Venus exalted (+5).
* **Classical Vedic Factors Expected**:
  * 7th house (spouse/marriage), 7th lord, and Venus (universal significator of marriage/wife).
  * Jupiter (significator of husband in female charts).
  * 2nd house (family growth), 8th house (longevity of marriage/mangalya sthana), and 11th house (social desires).
  * **Upapada Lagna (UL)** and its lord (crucial for checking the longevity and status of marriage).
  * **Darakaraka** (Jaimini planet with the lowest degree representing the spouse).
  * **Kuja Dosha (Manglik Blemish)**: Placement of Mars in 1st, 2nd, 4th, 7th, 8th, or 12th houses.
* **Missing Factors**:
  * **Upapada Lagna (UL)**: Completely missing from the logic.
  * **Darakaraka**: Completely missing.
  * **8th House (Mangalya Sthana)**: Omitted. This house is critical for predicting divorce or marital longevity.
  * **Kuja Dosha**: Mars in the 7th is penalized (-10), but Mars in the 1st, 2nd, 4th, 8th, or 12th is not evaluated for marriage.
* **Oversimplified Factors**:
  * **Karaka Blending**: Venus and Jupiter are averaged statically. In Vedic astrology, Venus must be the primary karaka for male charts, while Jupiter must be the primary karaka for female charts.
  * **Navamsha D9**: Evaluated as a minor flat modifier (`0.05` weight) rather than looking at the 7th house or 7th lord in the D9 chart.
* **Severity**: **CRITICAL**
* **Estimated Impact on Prediction Accuracy**: **Very High**. Without Upapada Lagna and 8th house longevity checks, the system cannot reliably distinguish between a stable marriage with challenges and a marriage ending in divorce.

---

### 2. Career (`career`)

* **Current Implemented Formula**:
  $$\text{Score} = 0.30 \cdot \text{House 10} + 0.20 \cdot \text{avg(House 6, 11)} + 0.25 \cdot \text{avg(Saturn, Sun)} + 0.15 \cdot \text{Lord 10} + 0.05 \cdot \text{D10} + 0.05 \cdot \text{SAV 10} + \text{Bonuses} + \text{Penalties}$$
  * *Afflictions*: Rahu in 10; Saturn retrograde in 10; Lord 10 in Dusthana (capped at -25).
  * *Bonuses*: Raja Yoga (+15% of max strength); Neecha Bhanga Raja Yoga (+10% of max strength).
* **Classical Vedic Factors Expected**:
  * 10th house (karma sthana) and 10th lord from Lagna, Moon (Chandra Lagna), and Sun (Surya Lagna).
  * **Amatyakaraka (AmK)**: Jaimini planet with the second-highest degree representing career.
  * D10 (Dashamamsha) ascendant, 10th house, and 10th lord.
  * Differentiating houses: House 6 and 10 rule service/employment; House 3, 7, 10, and 11 rule business.
* **Missing Factors**:
  * **10th House from Moon/Sun**: Ignored in the current implementation.
  * **Amatyakaraka (AmK)**: Completely missing.
  * **D10 Structural Layout**: Only reads flat D10 planet dignity, ignoring the D10 lord's placement and D10 Kendra/Trikona houses.
* **Oversimplified Factors**:
  * **Support Houses**: Average of 6 and 11 assumes all careers are based on service. It fails to adjust weights for business-oriented natives (who require 3rd and 7th house validation).
  * **Karaka Blending**: Averaging Saturn (service/labor) and Sun (government/authority/leadership) dilutes their contrasting career indications.
* **Severity**: **HIGH**
* **Estimated Impact on Prediction Accuracy**: **High**. The engine cannot distinguish between corporate employment, government service, or independent entrepreneurship, leading to overly generic career assessments.

---

### 3. Wealth (`wealth`)

* **Current Implemented Formula**:
  $$\text{Score} = 0.30 \cdot \text{avg(House 2, 11)} + 0.20 \cdot \text{avg(House 5, 9)} + 0.25 \cdot \text{avg(Jupiter, Venus)} + 0.15 \cdot \text{Lord 2} + 0.05 \cdot \text{D2} + 0.05 \cdot \text{SAV 2} + \text{Bonuses} + \text{Penalties}$$
  * *Afflictions*: Saturn in 2; Rahu in 11 (capped at -20).
  * *Bonuses*: Conjoined 2nd and 11th lords (+8); Jupiter in 2, 5, 9, or 11 (+5); Venus in 2 (+5).
* **Classical Vedic Factors Expected**:
  * 2nd house (wealth accumulation/dhana sthana) and 11th house (gains/labha sthana).
  * 5th and 9th houses (trikonas representing speculative wealth and fortune).
  * **Indu Lagna** (the specialized ascendant for evaluating wealth potential).
  * Hora (D2) solar/lunar divisions (planets in Sun/Moon horas determine ease of earning).
  * Dhana Yogas (wealth yogas) and Daridra Yogas (poverty combinations).
* **Missing Factors**:
  * **Indu Lagna**: Omitted. This is the primary verification gate for financial status.
  * **Hora (D2) Solar/Lunar Divisions**: D2 is not calculated or structured beyond a flat, unused varga key (which defaults to baseline 50.0).
  * **Daridra Yogas**: Omitted (e.g., lords of 2 or 11 conjoining lords of 6, 8, or 12).
* **Oversimplified Factors**:
  * **Lord and SAV Selection**: The engine evaluates only the lord of the 2nd house and the SAV of the 2nd house in its weighted calculation, completely ignoring the lord and SAV of the 11th house.
* **Severity**: **HIGH**
* **Estimated Impact on Prediction Accuracy**: **High**. An chart with strong 11th house indicators but a weak 2nd house will get an artificially depressed score because the 11th lord's strength and the 11th house's SAV points are completely ignored.

---

### 4. Education (`education`)

* **Current Implemented Formula**:
  $$\text{Score} = 0.25 \cdot \text{House 5} + 0.25 \cdot \text{avg(House 4, 9)} + 0.25 \cdot \text{avg(Mercury, Jupiter)} + 0.15 \cdot \text{Lord 5} + 0.05 \cdot \text{D24} + 0.05 \cdot \text{SAV 5} + \text{Bonuses} + \text{Penalties}$$
  * *Afflictions*: Mercury combust; Rahu in 5; Saturn in 5; Lord 5 in Dusthana (capped at -25).
  * *Bonuses*: Gaja Kesari Yoga (+10% of max strength).
* **Classical Vedic Factors Expected**:
  * 4th house (schooling/intellect), 5th house (intelligence/memory/creativity), and 9th house (higher university studies/specialization).
  * Mercury (rational mind and learning speed) and Jupiter (wisdom and advanced comprehension).
  * Chaturvimshamsha (D24) chart for academic accomplishments and exams.
* **Missing Factors**:
  * **D24 Data**: D24 is not defined in `canonical_content.json`, causing the varga score to always default to the baseline `50.0`.
* **Oversimplified Factors**:
  * **Unified Formula**: Merges basic schooling (4th), graduation (5th), and advanced research degrees (9th) into a single average. This prevents detecting cases of high intelligence (strong 5th) with interrupted formal schooling (weak 4th).
* **Severity**: **MEDIUM**
* **Estimated Impact on Prediction Accuracy**: **Medium**. The model cannot distinguish between general intelligence/intellect and actual academic credentials.

---

### 5. Children (`children`)

* **Current Implemented Formula**:
  $$\text{Score} = 0.30 \cdot \text{House 5} + 0.20 \cdot \text{avg(House 9, 11)} + 0.25 \cdot \text{avg(Jupiter, Moon)} + 0.15 \cdot \text{Lord 5} + 0.05 \cdot \text{D7} + 0.05 \cdot \text{SAV 5} + \text{Bonuses} + \text{Penalties}$$
  * *Afflictions*: Rahu, Saturn, or Ketu in 5; Lord 5 in Dusthana; Lord 5 debilitated (capped at -30).
  * *Bonuses*: Jupiter conjoined or aspecting 5 (+5).
* **Classical Vedic Factors Expected**:
  * 5th house (putra sthana), 5th lord, and Jupiter (Putrakaraka/significator of children).
  * **Kshetra Sphuta** (for female charts) and **Beeja Sphuta** (for male charts) to evaluate biological fertility.
  * **Karako Bhava Nashaya Rule**: A classical rule where the karaka (Jupiter) placed directly in its corresponding house (5th) causes challenges or delays regarding children.
  * Saptamsha (D7) chart (lineage, child birth timing, and child well-being).
* **Missing Factors**:
  * **Beeja & Kshetra Sphuta**: Omitted. These calculations are mandatory in Vedic astrology for evaluating fertility.
  * **Karako Bhava Nashaya**: Omitted. The engine gives a `+5` bonus for Jupiter in the 5th, which contradicts the classical blemish.
* **Oversimplified Factors**:
  * **D7 evaluation**: Only checks D7 planetary dignity, ignoring the D7 ascendant, 5th house, and 5th lord in D7.
* **Severity**: **HIGH**
* **Estimated Impact on Prediction Accuracy**: **High**. The system will fail to identify child birth challenges resulting from biological blocks (Beeja/Kshetra Sphuta) or classical significator blemishes.

---

### 6. Property (`property`)

* **Current Implemented Formula**:
  $$\text{Score} = 0.30 \cdot \text{House 4} + 0.20 \cdot \text{avg(House 2, 11)} + 0.25 \cdot \text{avg(Mars, Moon)} + 0.15 \cdot \text{Lord 4} + 0.05 \cdot \text{D4} + 0.05 \cdot \text{SAV 4} + \text{Penalties}$$
  * *Afflictions*: Saturn in 4; Rahu in 4; Lord 4 in Dusthana; Mars debilitated (capped at -20).
  * *Bonuses*: none.
* **Classical Vedic Factors Expected**:
  * 4th house (land/vehicles/comforts) and 4th lord.
  * Mars (significator of landed property and real estate).
  * Venus (significator of luxury vehicles, comforts, and conveyances).
  * Chaturthansha (D4) division (fortunes from property and housing).
* **Missing Factors**:
  * **Venus as Vehicle Karaka**: Currently uses the Moon as a secondary karaka, which represents emotions and mother, rather than Venus, which rules physical vehicles.
* **Oversimplified Factors**:
  * **Combined Asset Score**: Landed property (Mars) and luxury conveyances/cars (Venus) are combined. A native with a weak D4 but a strong Venus might own luxury vehicles but no land, which this unified score cannot capture.
* **Severity**: **MEDIUM**
* **Estimated Impact on Prediction Accuracy**: **Medium**. Fails to distinguish between real estate gains and vehicle acquisitions.

---

### 7. Health (`health`)

* **Current Implemented Formula**:
  $$\text{Score} = 0.30 \cdot \text{House 1} + 0.20 \cdot \text{avg(House 6, 8, 12)}_{\text{INVERTED}} + 0.25 \cdot \text{avg(Sun, Moon)} + 0.15 \cdot \text{Lord 1} + 0.05 \cdot \text{D6} + 0.05 \cdot \text{SAV 1} + \text{Bonuses} + \text{Penalties}$$
  * *Afflictions*: Saturn aspects Lagna; Rahu in 1; Sun combust (capped at -25).
  * *Bonuses*: Arishta Yoga max strength $\times -0.15$ (penalty).
* **Classical Vedic Factors Expected**:
  * 1st house (body/vitality) and 1st lord.
  * 6th house (disease/roga), 8th house (longevity/ayu), and 12th house (hospitalization/loss).
  * **Trimshamsha (D30)**: The primary divisional chart for disease, accidents, and injuries.
  * **Maraka Houses (2 and 7)**: Houses that bring death or severe physical affliction.
  * **Badhaka Sthana** and **Badhakesh** (obstruction points).
* **Missing Factors**:
  * **D30 Trimshamsha**: Completely omitted (uses D6 instead, which is not a standard Parashari divisional chart).
  * **Maraka Houses & Badhaka Sthana**: Omitted.
* **Oversimplified Factors**:
  * **Inverted Support Houses (`6, 8, 12`)**: The engine averages the strengths of these houses and inverts the score (higher strength = worse health). Astrologically, a strong 8th house lord gives long life (longevity), and a strong 6th lord can give the capacity to fight off diseases. Inverting their strengths mathematically penalizes natives with long life and strong constitutions, which is a major conceptual error.
* **Severity**: **HIGH**
* **Estimated Impact on Prediction Accuracy**: **High**. The system will miscalculate physical constitution and longevity for charts with strong 8th house placements.

---

### 8. Spirituality (`spirituality`)

* **Current Implemented Formula**:
  $$\text{Score} = 0.30 \cdot \text{avg(House 9, 12)} + 0.20 \cdot \text{House 5} + 0.25 \cdot \text{avg(Jupiter, Ketu)} + 0.15 \cdot \text{Lord 9} + 0.05 \cdot \text{D20} + 0.05 \cdot \text{SAV 9} + \text{Bonuses} + \text{Penalties}$$
  * *Afflictions*: Jupiter debilitated; Lord 9 combust (capped at -20).
  * *Bonuses*: Jupiter in 9 (+8), 5 (+5); Ketu strong in Moksha (+10).
* **Classical Vedic Factors Expected**:
  * 9th house (dharma/guru), 12th house (moksha/renunciation), and 5th house (devotion/mantra).
  * Jupiter (spiritual wisdom), Ketu (mokshakaraka), and Saturn (asceticism/detachment).
  * **Atmakaraka (AK)**: Planet with the highest degree, and its position in the Navamsha (Karakamsha) to identify the Ishta Devata.
  * Vimshamsha (D20) chart for spiritual progress.
* **Missing Factors**:
  * **Atmakaraka & Karakamsha**: Completely omitted.
  * **Saturn as Karaka of Renunciation**: Omitted.
* **Oversimplified Factors**:
  * D20 Vimshamsha is defaulted to the `50.0` baseline.
* **Severity**: **MEDIUM**
* **Estimated Impact on Prediction Accuracy**: **Medium**. Cannot determine the specific path of spiritual devotion (Ishta Devata) or the degree of ascetic renunciation.

---

## 3. Summary of Findings & Audit Action Plan

| Domain | Severity | Prediction Impact | Primary Audited Gaps |
| :--- | :---: | :---: | :--- |
| **Marriage** | **CRITICAL** | **Very High** | Missing Upapada Lagna (UL), Manglik Blemish (Kuja Dosha), and 8th house longevity checks. |
| **Career** | **HIGH** | **High** | Missing Amatyakaraka (AmK) and 10th house checks from Chandra/Surya Lagna. |
| **Wealth** | **HIGH** | **High** | Missing Indu Lagna and 11th lord/SAV calculations in primary factors. |
| **Children** | **HIGH** | **High** | Missing Beeja/Kshetra Sphuta fertility checks; Jupiter in 5th *Karako Bhava Nashaya* blemish ignored. |
| **Health** | **HIGH** | **High** | Incorrect inversion of 8th house (penalizes longevity); missing D30 Trimshamsha and Maraka house checks. |
| **Property** | **MEDIUM** | **Medium** | Missing Venus as vehicle significator; combines real estate and luxury vehicles. |
| **Education** | **MEDIUM** | **Medium** | Unified formula merges 4th, 5th, and 9th house indicators, masking individual distinctions. |
| **Spirituality** | **MEDIUM** | **Medium** | Missing Atmakaraka, Karakamsha, and Ishta Devata evaluations. |
