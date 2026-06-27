# FORMULA REPOSITORY DESIGN

**Date:** 2026-06-19
**Version:** Phase 9 Step 3A Governance Package

## Governance Principle
**Question logic must never be hardcoded into the Python engines.** 

If a user asks about "Marriage," the Python code does not contain `if house == 7`. Instead, the system looks up the externalized formula for "Marriage" from the Formula Repository.

## Purpose
The Formula Repository allows:
1. Astrologers to update the logic without software developer intervention.
2. The system to scale to thousands of questions without engine bloat.
3. Easy auditing of the astrological rules used by the AI.

## Structure

Formulas are stored as discrete, machine-readable definition files (currently conceptualized as Markdown/JSON structures).

### Examples of Formula Files

1. **`FORMULA_MARRIAGE_PROMISE`**
   *   **Primary House:** 7
   *   **Secondary Houses:** 2, 11
   *   **Karakas:** Venus (Men), Jupiter (Women)
   *   **Varga:** D9 (Navamsha)
   *   **Evaluation Logic:** Sum(Bhava Bala 7) + Shadbala(7th Lord) + Benefic Aspects

2. **`FORMULA_MARRIAGE_TIMING`**
   *   **Dasha Triggers:** 7th Lord, planets in 7th, Venus/Jupiter, Dispositor of 7th Lord.

3. **`FORMULA_CAREER_PROMISE`**
   *   **Primary House:** 10
   *   **Secondary Houses:** 2, 6, 11
   *   **Karakas:** Sun, Mercury, Saturn
   *   **Varga:** D10 (Dashamsha)
   *   **Evaluation Logic:** Analyze 10th Lord placement, Amatyakaraka, and D10 Ascendant.

4. **`FORMULA_CAREER_TIMING`**
   *   **Dasha Triggers:** 10th Lord, 11th Lord (for promotion), 6th Lord (for job change).

## Dynamic Loading
During pipeline execution, the Question Router identifies the requested domain, and the Domain Resolver dynamically loads the relevant `FORMULA_*` files from this repository to execute the reasoning.
