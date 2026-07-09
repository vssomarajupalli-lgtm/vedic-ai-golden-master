# FORMULA FAMILY CATALOG v1

## 1. Overview
This catalog dictates the foundational architecture for the Formula Families required to support the entire canonical Question Registry. Each domain is rigidly structured according to Phase 14A inheritance and Phase 14B governance rules.

---

## 2. Domain: Marriage (Domain 7)
- **Master Category:** Marriage
- **Subcategories:** Timing, Quality/Promise, Delay, Divorce/Separation
- **Formula Families:** 
  - `MAR_TIMING_BASE`: Evaluates Dasha and Transit activation of 7th house/Venus.
  - `MAR_PROMISE_BASE`: Evaluates fundamental strength of 7th house, 7th lord, and Venus.
  - `MAR_RISK_BASE`: Evaluates afflictions (Saturn, Mars, Rahu, Ketu) to the 7th house and D9 chart.
- **Typical Variants:** `MAR_TIMING_EARLY`, `MAR_TIMING_DELAY`, `MAR_DIVORCE_RISK`
- **Required Engines:** NatalPromiseEngine, DashaEngine, TransitEngine (for Timing), YogaEngine
- **Required Confidence Layers:** `7th_house_strength`, `venus_dignity`, `dasha_lord_aspect_7th`, `transit_jupiter_aspect_7th`
- **Template Families:** `timing_assessment`, `multifactor_assessment`, `risk_assessment`

---

## 3. Domain: Career (Domain 10)
- **Master Category:** Career & Profession
- **Subcategories:** Growth, Job Change, Stability, Foreign Opportunities
- **Formula Families:**
  - `CAR_GROWTH_BASE`: Evaluates Dasha activation of 10th and 11th houses.
  - `CAR_CHANGE_BASE`: Evaluates Dasha/Transit connections between 10th and 8th/12th houses.
  - `CAR_STABILITY_BASE`: Evaluates fundamental strength of 10th house, 10th lord, Mercury, and Sun.
- **Typical Variants:** `CAR_PROMOTION_TIMING`, `CAR_SUDDEN_LOSS`, `CAR_FOREIGN_OPPORTUNITY` (adds 12th house check).
- **Required Engines:** NatalPromiseEngine, DashaEngine, TransitEngine, AshtakavargaEngine
- **Required Confidence Layers:** `10th_house_strength`, `sun_dignity`, `dasha_lord_activates_10th`
- **Template Families:** `timing_assessment`, `multifactor_assessment`, `strength_assessment`

---

## 4. Domain: Wealth (Domain 2 & 11)
- **Master Category:** Wealth & Finance
- **Subcategories:** Savings, Income, Sudden Gains, Debt
- **Formula Families:**
  - `WEA_INCOME_BASE`: Evaluates 11th house, 11th lord, and Jupiter.
  - `WEA_SAVINGS_BASE`: Evaluates 2nd house and 2nd lord.
  - `WEA_DEBT_BASE`: Evaluates 6th house afflictions overriding the 2nd/11th houses.
  - `WEA_SUDDEN_BASE`: Evaluates 8th house positive manifestations (e.g., Vipreet Raj Yoga).
- **Typical Variants:** `WEA_SUDDEN_GAIN`, `WEA_SUDDEN_LOSS`, `WEA_DEBT_RISK`
- **Required Engines:** NatalPromiseEngine, DashaEngine, YogaEngine
- **Required Confidence Layers:** `2nd_house_strength`, `11th_house_strength`, `jupiter_dignity`, `6th_house_affliction`
- **Template Families:** `multifactor_assessment`, `risk_assessment`

---

## 5. Domain: Health (Domain 6)
- **Master Category:** Health & Vitality
- **Subcategories:** General Vitality, Chronic Illness, Accidents, Recovery
- **Formula Families:**
  - `HLT_VITALITY_BASE`: Evaluates Lagna, Lagna lord, and Sun.
  - `HLT_ILLNESS_BASE`: Evaluates 6th house, 6th lord, and current Dasha lord relationship to 6th.
  - `HLT_ACCIDENT_BASE`: Evaluates 8th house and Mars/Rahu transits over sensitive points.
- **Typical Variants:** `HLT_SURGERY_TIMING`, `HLT_CHRONIC_RISK`, `HLT_RECOVERY_TIMING`
- **Required Engines:** NatalPromiseEngine, DashaEngine, TransitEngine
- **Required Confidence Layers:** `lagna_strength`, `sun_dignity`, `6th_lord_activation`
- **Template Families:** `timing_assessment`, `risk_assessment`, `strength_assessment`

---

## 6. Domain: Property & Vehicles (Domain 4)
- **Master Category:** Assets
- **Subcategories:** Property Purchase, Vehicle Purchase, Loss of Property
- **Formula Families:**
  - `AST_PURCHASE_BASE`: Evaluates 4th house, 4th lord, and Mars (Property) / Venus (Vehicles).
- **Typical Variants:** `AST_PROP_TIMING`, `AST_VEH_TIMING`, `AST_PROP_LOSS`
- **Required Engines:** NatalPromiseEngine, DashaEngine
- **Required Confidence Layers:** `4th_house_strength`, `mars_dignity` (for land)
- **Template Families:** `timing_assessment`, `multifactor_assessment`

---

## 7. Domain: Education (Domain 4 & 5 & 9)
- **Master Category:** Education
- **Subcategories:** Primary, Higher Education, Competitive Exams, Interruptions
- **Formula Families:**
  - `EDU_ACADEMIC_BASE`: Evaluates 4th (early) and 5th (intelligence) houses, plus Mercury and Jupiter.
  - `EDU_HIGHER_BASE`: Evaluates 9th house and 9th lord.
  - `EDU_COMPETITION_BASE`: Evaluates 6th house (competitions) relative to Lagna lord strength.
- **Typical Variants:** `EDU_EXAM_SUCCESS`, `EDU_FOREIGN_STUDY` (adds 12th house).
- **Required Engines:** NatalPromiseEngine, DashaEngine, YogaEngine
- **Required Confidence Layers:** `5th_house_strength`, `mercury_dignity`, `9th_house_strength`
- **Template Families:** `multifactor_assessment`, `timing_assessment`

---

## 8. Domain: Children (Domain 5)
- **Master Category:** Progeny
- **Subcategories:** Promise of Children, Timing of Birth, IVF/Complications
- **Formula Families:**
  - `PRO_PROMISE_BASE`: Evaluates 5th house, 5th lord, Jupiter, and Saptamsha (D7).
  - `PRO_TIMING_BASE`: Evaluates Dasha and Transit activation of the 5th house/lord.
- **Typical Variants:** `PRO_TIMING`, `PRO_DELAY_RISK`
- **Required Engines:** NatalPromiseEngine, DashaEngine, TransitEngine
- **Required Confidence Layers:** `5th_house_strength`, `jupiter_dignity`, `transit_jupiter_aspect_5th`
- **Template Families:** `timing_assessment`, `multifactor_assessment`

---

## 9. Domain: Relationships (Domain 7 & 11)
- **Master Category:** Interpersonal
- **Subcategories:** Friendships, Business Partnerships, Secret Enemies
- **Formula Families:**
  - `REL_PARTNERSHIP_BASE`: Evaluates 7th house (business) and 11th house (networking).
  - `REL_ENEMIES_BASE`: Evaluates 6th (open enemies) and 12th (hidden enemies).
- **Typical Variants:** `REL_BUSINESS_SUCCESS`, `REL_BETRAYAL_RISK`
- **Required Engines:** NatalPromiseEngine, AshtakavargaEngine
- **Required Confidence Layers:** `11th_house_strength`, `7th_house_bindus`
- **Template Families:** `multifactor_assessment`, `risk_assessment`

---

## 10. Domain: Travel (Domain 3, 9, 12)
- **Master Category:** Travel & Relocation
- **Subcategories:** Short Trips, Long Distance Travel, Foreign Settlement
- **Formula Families:**
  - `TRV_FOREIGN_BASE`: Evaluates 9th (long travel) and 12th (foreign settlement), plus Rahu.
- **Typical Variants:** `TRV_FOREIGN_SETTLEMENT`, `TRV_TIMING`
- **Required Engines:** NatalPromiseEngine, DashaEngine
- **Required Confidence Layers:** `12th_house_activation`, `rahu_activation`
- **Template Families:** `timing_assessment`, `multifactor_assessment`

---

## 11. Domain: Spirituality (Domain 9 & 12)
- **Master Category:** Spiritual Growth
- **Subcategories:** Moksha, Occult Studies, Guru/Guidance
- **Formula Families:**
  - `SPI_MOKSHA_BASE`: Evaluates 12th house, 12th lord, Ketu, and Jupiter.
  - `SPI_OCCULT_BASE`: Evaluates 8th house (hidden knowledge).
- **Typical Variants:** `SPI_AWAKENING_TIMING`, `SPI_OCCULT_POTENTIAL`
- **Required Engines:** NatalPromiseEngine, YogaEngine
- **Required Confidence Layers:** `12th_house_strength`, `ketu_dignity`, `jupiter_dignity`
- **Template Families:** `strength_assessment`
