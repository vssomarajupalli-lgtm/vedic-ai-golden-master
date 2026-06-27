# ASTROLOGICAL_PREDICTION_GOVERNANCE_v1

## Purpose
Define the permanent separation between:
1. Natal Promise
2. Dasha Activation
3. Mandali Transit Analysis

for the Vedic AI System.

---

## Core Principle
An event can only occur if the natal chart contains the promise.

Neither Dasha nor Transit can create an event that is absent from the natal promise.

---

## Layer 1: Natal Promise Engine (Truth Layer)

**Purpose:**
Determine whether an event is fundamentally supported in the horoscope.

**Inputs:**
1. Bhava Strength
2. Bhava Lord Strength
3. Karaka Strength
4. Relevant Yogas
5. Relevant Vargas
6. Functional Benefic/Malefic Impact
7. Affliction Strength

*(A strong Bhava or Karaka can still be weakened by severe afflictions. Affliction evaluation is an explicit promise component.)*

**Output:**
* Promise Strength
* Promise Percentage
* Promise Classification

---

## Layer 2: Dasha Activation Engine (Activation Layer)

**Purpose:**
Determine whether the natal promise is activated during the current period.

**Inputs:**
* Mahadasha
* Antardasha
* Pratyantardasha

**Output:**
* Activated
* Partially Activated
* Not Activated

**Governance Rule:**
* Dasha identifies activation periods.
* Dasha does not create promise.
* Dasha does not guarantee manifestation.
* Dasha indicates when the natal promise becomes operational.

---

## Layer 3: Mandali Transit Engine (Independent Advisory Layer)

**Purpose:**
Provide independent transit analysis.

**Inputs:**
* Moon-centered Mandali
* Jupiter, Saturn, Rahu, Ketu transits

**Output:**
* Transit Climate
* General Opportunities
* General Challenges

**Governance Hardening:**
Mandali is STRICTLY EXCLUDED from:
1. Promise Calculation
2. Promise Percentage
3. Dasha Activation Calculation
4. Final Question Probability
5. Formula Evaluator Logic
6. Formula Family Scoring

Mandali is PERMITTED ONLY in:
1. Independent Transit Reports
2. Monthly Transit Reports
3. Yearly Transit Reports
4. General Transit Climate Analysis
5. Independent Mandali Dashboard

*Mandali must never alter Question Engine conclusions.*

---

## Question Engine Formula

**Question Engine = Natal Promise + Dasha Activation**

*Mandali is excluded.*

---

## Question Result Model

Every Question Engine output must contain a mandatory reporting structure:

**A. Promise Assessment**
**B. Dasha Activation Assessment**
**C. Final Question Conclusion**

*Optional:*
**D. Independent Mandali Commentary**

**Governance Rule:**
The Final Question Conclusion must be generated before Mandali is consulted. Mandali commentary is optional and independent.

---

## Core System Governance Freeze

The following architecture is permanently frozen:
1. **Promise Engine** -> Truth Layer
2. **Dasha Engine** -> Activation Layer
3. **Question Engine** -> Promise + Dasha
4. **Mandali Engine** -> Independent Advisory Layer

Mandali shall never override, modify, increase, decrease, or recalculate any Question Engine probability.
