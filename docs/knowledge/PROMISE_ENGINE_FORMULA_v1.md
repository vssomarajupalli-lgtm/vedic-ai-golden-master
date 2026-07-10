# PROMISE_ENGINE_FORMULA_v1

## Status

Draft for Architectural Approval

## Purpose

This document defines the deterministic Promise Score architecture for Vedic AI.

The objective is to evaluate a life domain using four independent pillars:

1. Bhava Strength
2. Bhavadhipati Strength
3. Karaka Strength
4. Relevant Varga Validation

This architecture prevents double counting and preserves explainability.

---

# OUTER WEIGHTS

| Factor                    | Weight |
| ------------------------- | ------ |
| Bhava Strength            | 35%    |
| Bhavadhipati Strength     | 30%    |
| Karaka Strength           | 20%    |
| Relevant Varga Validation | 15%    |

Total = 100%

---

# 1. BHAVA STRENGTH (35%)

## Purpose

Determines the strength of the field of manifestation.

Example:

* Marriage → 7th House
* Career → 10th House
* Wealth → 2nd / 11th House
* Property → 4th House

---

## Internal Weights

| Factor                                 | Weight |
| -------------------------------------- | ------ |
| Sarvashtakavarga (SAV)                 | 30%    |
| Occupants                              | 20%    |
| Benefic Aspects                        | 15%    |
| Malefic Aspects                        | 15%    |
| House Nature (Kendra/Trikona/Dusthana) | 10%    |
| House Specific Yogas                   | 10%    |

Total = 100%

---

## Formula

Bhava Strength =

(SAV × 30%)
* (Occupants × 20%)
* (Benefic Aspects × 15%)
* (Malefic Aspects × 15%)
* (House Nature × 10%)
* (House Yogas × 10%)

---

# 2. BHAVADHIPATI STRENGTH (30%)

## Purpose

Determines the strength of the house controller.

Examples:

* Marriage → 7th Lord
* Career → 10th Lord
* Property → 4th Lord
* Children → 5th Lord

---

## Internal Weights

| Factor            | Weight |
| ----------------- | ------ |
| Dignity           | 25%    |
| House Placement   | 20%    |
| Planetary Aspects | 15%    |
| Conjunctions      | 10%    |
| Combustion        | 10%    |
| Retrogression     | 5%     |
| Shadbala          | 10%    |
| Varga Dignity     | 5%     |

Total = 100%

---

## Governance Rule

Planetary afflictions shall be evaluated here only.

Examples:

* Combustion
* Debilitation
* Retrogression
* Planetary Afflictions
* Planetary Blessings

These factors shall not be re-applied downstream.

---

# 3. KARAKA STRENGTH (20%)

## Purpose

Determines the strength of the natural significator.

Examples:

| Domain       | Karaka         |
| ------------ | -------------- |
| Marriage     | Venus          |
| Career       | Saturn / Sun   |
| Wealth       | Jupiter        |
| Children     | Jupiter        |
| Property     | Mars + Moon    |
| Health       | Sun + Moon     |
| Spirituality | Jupiter + Ketu |

---

## Method

Karaka Strength shall use the Final Planet Strength.

No additional penalties.

No additional bonuses.

No duplicate calculations.

Example:

Venus Final Strength = 60

Karaka Strength = 60

No further modification permitted.

---

# 4. RELEVANT VARGA VALIDATION (15%)

## Purpose

Confirms whether the promise survives divisional chart validation.

---

## Domain Mapping

| Domain             | Primary Varga |
| ------------------ | ------------- |
| Marriage           | D9            |
| Children           | D7            |
| Career             | D10           |
| Parents            | D12           |
| Property / Vehicle | D16           |
| Education          | D24           |
| Spirituality       | D20           |

---

## Internal Weights

| Factor               | Weight |
| -------------------- | ------ |
| Varga Lord Strength  | 40%    |
| Varga House Strength | 40%    |
| Special Varga Yogas  | 20%    |

Total = 100%

---

# FINAL PROMISE FORMULA

Promise Score =

(Bhava Strength × 35%)
+ (Bhavadhipati Strength × 30%)
+ (Karaka Strength × 20%)
+ (Relevant Varga Validation × 15%)

---

# GOVERNANCE RULE DR-XXX

## NO DOUBLE PENALTY RULE

A planetary condition shall be evaluated exactly once.

Examples:

* Combustion
* Debilitation
* Retrogression
* Planetary Affliction
* Planetary Blessing

These shall be calculated inside Planet/Bhavadhipati Strength only.

The resulting Final Planet Strength shall propagate downstream.

---

## Correct Example

Venus Raw Strength = 80
Combustion = -20
Final Venus Strength = 60

Then:
Bhavadhipati Contribution = 60
Karaka Contribution = 60

---

## Incorrect Example

Venus Raw Strength = 80
Combustion = -20
Final Venus = 60

Then:
Karaka = 60 - 20
Bhavadhipati = 60 - 20

This is prohibited.

---

# ARCHITECTURAL PRINCIPLE

Promise Evaluation shall follow:

Bhava
→ Bhavadhipati
→ Karaka
→ Relevant Varga

These are four independent pillars.

The architecture must remain:

* Deterministic
* Explainable
* Auditable
* Free from double counting
* Free from duplicate punishment

End of Document.
