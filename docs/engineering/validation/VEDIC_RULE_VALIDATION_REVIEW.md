# VEDIC RULE VALIDATION REVIEW

## 1. Executive Summary

This document reviews 22 proposed astrological enhancements for the Vedic-AI computational engines. Each rule is evaluated for classical source support, universal acceptance, deterministic suitability, implementation priority, and false-prediction risks.

---

## 2. Rule-by-Rule Evaluations

### 1. Upapada Lagna (UL)
* **Classical Source Support**: **Strong** (*Brihat Parashara Hora Shastra* - Upapada chapter).
* **Acceptance**: Universally accepted in both Parashari and Jaimini systems.
* **Suitable for Deterministic Software**: **YES** (strict mathematical Arudha calculation).
* **Recommended Phase**: **V1** (critical for Marriage domain accuracy).
* **Risk of False Predictions**: **HIGH** (incorrect calculation will cause false indicators of marriage delays or divorce).

### 2. Amatyakaraka (AmK)
* **Classical Source Support**: **Strong** (*Jaimini Sutras*).
* **Acceptance**: Universally accepted (primarily Jaimini school, widely used in Parashari).
* **Suitable for Deterministic Software**: **YES** (rank ordering planet longitudes).
* **Recommended Phase**: **V1** (essential for Career domain accuracy).
* **Risk of False Predictions**: **MEDIUM** (incorrect AmK shifts the career direction metrics).

### 3. Darakaraka (DK)
* **Classical Source Support**: **Strong** (*Jaimini Sutras*).
* **Acceptance**: Universally accepted (spouse significator).
* **Suitable for Deterministic Software**: **YES** (lowest degree planet among the 7 classical planets).
* **Recommended Phase**: **V1** (critical for Marriage domain accuracy).
* **Risk of False Predictions**: **MEDIUM** (incorrect spouse profile and relationship strength metrics).

### 4. Atmakaraka (AK)
* **Classical Source Support**: **Strong** (*Jaimini Sutras*).
* **Acceptance**: Universally accepted (self/soul significator).
* **Suitable for Deterministic Software**: **YES** (highest degree planet among the 7 classical planets).
* **Recommended Phase**: **V2** (essential for Spirituality and Self domains).
* **Risk of False Predictions**: **MEDIUM** (affects spiritual affinity calculations).

### 5. Kuja Dosha (Manglik Blemish)
* **Classical Source Support**: **Strong** (Standard classical texts: *Phaladeepika*, *Deva Keralam*).
* **Acceptance**: Universally accepted, though local cancellation exceptions vary by region.
* **Suitable for Deterministic Software**: **YES** (checking Mars in 1, 2, 4, 7, 8, 12, but cancellation rules must be coded precisely).
* **Recommended Phase**: **V1** (vital for Marriage domain).
* **Risk of False Predictions**: **HIGH** (causes false alarms of severe relationship distress if cancellations are ignored).

### 6. Functional Benefics
* **Classical Source Support**: **Strong** (*BPHS* - Sambandha chapter).
* **Acceptance**: Universally accepted in the Parashari system.
* **Suitable for Deterministic Software**: **YES** (strict conditional logic mapped directly to Lagna sign).
* **Recommended Phase**: **V1** (fundamental to `HouseStrengthEngine`).
* **Risk of False Predictions**: **CRITICAL** (affects every house and planet strength score; errors here distort the entire engine output).

### 7. Yogakaraka
* **Classical Source Support**: **Strong** (*BPHS*).
* **Acceptance**: Universally accepted (planet ruling both a Kendra and a Trikona).
* **Suitable for Deterministic Software**: **YES** (simple lookup mapping).
* **Recommended Phase**: **V1** (fundamental to `PlanetStrengthEngine`).
* **Risk of False Predictions**: **HIGH** (underestimates planetary strength for Taurus, Libra, Cancer, and Leo Ascendants).

### 8. Beeja Sphuta
* **Classical Source Support**: **Strong** (*Phaladeepika* - Chapter 12).
* **Acceptance**: Universally accepted for male fertility.
* **Suitable for Deterministic Software**: **YES** (mathematical longitude sum of Sun + Venus + Jupiter).
* **Recommended Phase**: **V2** (Children domain).
* **Risk of False Predictions**: **HIGH** (incorrectly predicting biological conceiving challenges).

### 9. Kshetra Sphuta
* **Classical Source Support**: **Strong** (*Phaladeepika* - Chapter 12).
* **Acceptance**: Universally accepted for female fertility.
* **Suitable for Deterministic Software**: **YES** (mathematical longitude sum of Moon + Mars + Jupiter).
* **Recommended Phase**: **V2** (Children domain).
* **Risk of False Predictions**: **HIGH** (incorrectly predicting biological conceiving challenges).

### 10. Karako Bhava Nashaya
* **Classical Source Support**: **Moderate** (*Bhavartha Ratnakara*).
* **Acceptance**: **School-dependent** (some schools apply this rule strictly; others apply it only to Jupiter in the 5th and Sun in the 9th).
* **Suitable for Deterministic Software**: **YES** (should be implemented as a soft penalty rather than a complete negation).
* **Recommended Phase**: **V2** (to refine Children and Wealth domains).
* **Risk of False Predictions**: **MEDIUM** (incorrect implementation over-penalizes positive planetary placements).

### 11. Indu Lagna
* **Classical Source Support**: **Strong** (*Brihat Jataka*, *Uttara Kalamrita*).
* **Acceptance**: Universally accepted for wealth potential.
* **Suitable for Deterministic Software**: **YES** (simple mathematical ray sum calculation).
* **Recommended Phase**: **V1** (vital for Wealth domain accuracy).
* **Risk of False Predictions**: **HIGH** (incorrectly assesses wealth limits and financial success).

### 12. Moolatrikona
* **Classical Source Support**: **Strong** (*BPHS*).
* **Acceptance**: Universally accepted.
* **Suitable for Deterministic Software**: **YES** (planet sign and degree boundary checks).
* **Recommended Phase**: **V1** (fundamental to `PlanetStrengthEngine`).
* **Risk of False Predictions**: **MEDIUM** (incorrectly calculates foundational planetary dignity scores).

### 13. Graha Yuddha (Planetary War)
* **Classical Source Support**: **Strong** (*Surya Siddhanta*, *Brihat Samhita*).
* **Acceptance**: **Controversial / School-dependent** (astrologers debate calculation methods: center-to-center longitude vs. declination, and the exact rules for determining the winner).
* **Suitable for Deterministic Software**: **YES** (if locked to the standard center-to-center longitude $< 1^\circ$ rule).
* **Recommended Phase**: **V3** (due to calculation disputes).
* **Risk of False Predictions**: **MEDIUM** (affects planetary war winner/loser strengths).

### 14. Combustion
* **Classical Source Support**: **Strong** (*Surya Siddhanta*).
* **Acceptance**: Universally accepted, with minor regional variations in exact degree boundaries.
* **Suitable for Deterministic Software**: **YES** (strict degree check).
* **Recommended Phase**: **V1** (fundamental to `PlanetStrengthEngine`).
* **Risk of False Predictions**: **HIGH** (falsely registers a planet as combustion-damaged).

### 15. Maraka
* **Classical Source Support**: **Strong** (*BPHS*).
* **Acceptance**: Universally accepted (Lords and occupants of 2nd and 7th houses).
* **Suitable for Deterministic Software**: **YES** (standard house-relationship lookup).
* **Recommended Phase**: **V2** (Health domain timing overlays).
* **Risk of False Predictions**: **HIGH** (can generate incorrect timing indications of severe illness).

### 16. Badhaka
* **Classical Source Support**: **Strong** (*Prashna Marga*).
* **Acceptance**: Universally accepted, though application rules differ between natal and query astrology.
* **Suitable for Deterministic Software**: **YES** (lookup based on Lagna sign mobility).
* **Recommended Phase**: **V2** (Health/Obstruction domain overlays).
* **Risk of False Predictions**: **MEDIUM** (incorrectly flags a positive dasha as blocked).

### 17. D2 (Hora - Wealth)
* **Classical Source Support**: **Strong** (*BPHS*).
* **Acceptance**: Universally accepted, but calculation methods (Parashari vs. Kashinath) differ.
* **Suitable for Deterministic Software**: **YES** (using the classical Parashari solar/lunar sign split).
* **Recommended Phase**: **V2** (Wealth validation).
* **Risk of False Predictions**: **MEDIUM** (distorts D2 wealth confirmation scores).

### 18. D4 (Chaturthansha - Property)
* **Classical Source Support**: **Strong** (*BPHS*).
* **Acceptance**: Universally accepted.
* **Suitable for Deterministic Software**: **YES**.
* **Recommended Phase**: **V2** (Property validation).
* **Risk of False Predictions**: **LOW**.

### 19. D7 (Saptamsha - Children)
* **Classical Source Support**: **Strong** (*BPHS*).
* **Acceptance**: Universally accepted.
* **Suitable for Deterministic Software**: **YES**.
* **Recommended Phase**: **V2** (Children validation).
* **Risk of False Predictions**: **HIGH** (incorrect child birth timeline predictions).

### 20. D20 (Vimshamsha - Spirituality)
* **Classical Source Support**: **Strong** (*BPHS*).
* **Acceptance**: Universally accepted.
* **Suitable for Deterministic Software**: **YES**.
* **Recommended Phase**: **V3** (Spirituality validation).
* **Risk of False Predictions**: **LOW**.

### 21. D24 (Chaturvimshamsha - Education)
* **Classical Source Support**: **Strong** (*BPHS*).
* **Acceptance**: Universally accepted.
* **Suitable for Deterministic Software**: **YES**.
* **Recommended Phase**: **V2** (Education validation).
* **Risk of False Predictions**: **LOW**.

### 22. D30 (Trimshamsha - Diseases)
* **Classical Source Support**: **Strong** (*BPHS*).
* **Acceptance**: Universally accepted (used for physical challenges, accidents, and diseases).
* **Suitable for Deterministic Software**: **YES** (requires special sign-to-ruler mapping).
* **Recommended Phase**: **V2** (Health/Disease validation).
* **Risk of False Predictions**: **HIGH** (incorrect disease diagnosis/timing assessments).

---

## 3. Recommended Implementation Strategy

1. **Prioritize V1 (High Impact, Safe Standards)**: Implement Upapada Lagna, Karaka (AmK/DK), Kuja Dosha, Functional Benefics, Yogakaraka, Indu Lagna, Moolatrikona, and Combustion first. These are universally accepted and mathematically solid.
2. **Handle V2 (Specialized Domains & Vargas)**: Implement Beeja/Kshetra Sphuta, D2, D4, D7, D24, D30, Maraka, and Badhaka after foundational engines are validated.
3. **Delay V3 (Controversial & Non-Critical)**: Implement Graha Yuddha and D20 last due to school-dependent calculation disputes and lower immediate prediction impact.
