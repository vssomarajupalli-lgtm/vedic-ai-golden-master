# ASHTAKAVARGA ARCHITECTURE RECOMMENDATION

**Date:** 2026-06-19_1800
**Context:** Phase 9 Astakavarga Governance Review

## Objective
To resolve the architectural placement of Ashtakavarga (SAV/BAV) within the Prediction Engine and determine whether it functions best as a baked-in component of Bhava Strength (Option A) or as an independent formula variable (Option B).

---

## 1. Which option avoids double counting?
**Option A.**
If Ashtakavarga is evaluated once to build the `Final Bhava Strength` and then evaluated *again* as an independent variable inside a specific `PROMISE_001` formula, the system mathematically double-counts the same astrological principle. Option A restricts the SAV/BAV modifier to a single point of calculation, preventing a house with low SAV from being redundantly penalized twice in the master prediction score.

## 2. Which option is astrologically more correct?
**Option A.**
Astrologically, Ashtakavarga represents the intrinsic, collective capacity of a specific sign/house to bear fruit, based on the planetary rays cast upon it. Therefore, it is fundamentally a structural characteristic of the Bhava itself. It belongs permanently inside the "Natal Promise" tier alongside raw Bhava Bala, not as a floating, domain-specific modifier like a temporary Dosha.

## 3. Which option produces cleaner architecture?
**Option A.**
Option A adheres to strict architectural decoupling. If SAV/BAV is merged into `Final Bhava Strength`, the Question Engine and Formula Repository remain completely agnostic to the underlying math. The `MAR_PROMISE_001` formula simply requests the "Strength of the 7th House." It does not need to know *how* that strength was computed. This isolates the complexity entirely within the core Bhava Evaluation Engine.

## 4. Which option is easier to maintain across 150+ questions and 20+ formula groups?
**Option A.**
If Option B is chosen, every single one of the 150+ formulas in the repository must manually define and configure an Ashtakavarga threshold modifier. If Option A is chosen, the repository remains completely clean. The underlying Bhava Engine applies the SAV modifier universally across the entire system with a single piece of code.

## 5. Classification
Ashtakavarga should be officially classified as a **Primary Bhava Component**. 

---

## 6. Resolving Future Gochara Timing (No Double Counting)
If Option A is implemented, Ashtakavarga will effectively exist in two distinct systemic layers: the *Static Promise* and the *Dynamic Activation*. Here is how the architecture avoids double counting:

1.  **The Promise Axis (Static SAV):** The Natal D1 SAV points are evaluated exactly once by the Bhava Engine to compute the lifelong `Final Bhava Strength`. This locks in the 50% "Natal Promise" baseline score.
2.  **The Activation Axis (Dynamic Kakshya):** During the execution of the `TIMING_001` formula, the system evaluates current transits (Gochara). The Gochara engine does *not* look at the natal SAV to determine promise. Instead, it looks at the SAV/BAV of the *sign the transiting planet is currently traveling through* to calculate the strength of the temporal trigger (Kakshya). 

Because the Natal Promise uses the *static natal placement*, and the Timing Engine uses the *dynamic transit placement*, they operate on entirely different mathematical axes. This ensures Gochara transit validations function perfectly without double-counting the baseline promise.
