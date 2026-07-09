# FORMULA DOMAIN MAP v1

## 1. Overview
This document maps the projected scaling metrics of the Formula Library architecture. It provides statistical estimates of how the canonical Question Registry maps downward through the Formula Family inheritance model.

## 2. Question Mapping Strategy
The Question Registry handles the mapping of natural language user inputs (assigned unique `QuestionID`s) into the strict architectural pipeline.

### 2.1 The Many-to-One Convergence Rule
Because linguistic variations of questions far outnumber the core astrological mathematical evaluations, the system aggressively converges questions into shared Formula Variants.

**Example Convergence (Career Timing):**
- QID 10.1: "When will I get a promotion?"
- QID 10.2: "Is this a good time to ask for a raise?"
- QID 10.3: "When will my career take off?"
- **Mapping:** All three map to `CAR_GROWTH_TIMING` Formula Variant.

## 3. Projected Architectural Metrics

To support a projected Canonical Question Registry of ~500 common Vedic Astrology questions across all 10 major domains, the architecture enforces the following scaling bounds:

### 3.1 Estimated Formula Families (Bases)
- **Constraint:** ~3 to 4 Families per domain.
- **Projected Total:** **~35 Formula Families**.
- **Analysis:** By abstracting the core logic (e.g., Timing vs. Strength vs. Risk), the system only requires 35 fundamental mathematical pipelines to cover every area of human life.

### 3.2 Estimated Formula Variants (Children)
- **Constraint:** ~2 to 4 Variants per Family.
- **Projected Total:** **~100 Formula Variants**.
- **Analysis:** This provides enough granularity to differentiate between, for instance, a "Sudden Wealth Gain" and a "Slow Wealth Accumulation", while inheriting 80% of the mathematical logic from the Base Family.

### 3.3 Question Registry Mapping
- **Input:** ~500 Question IDs.
- **Convergence Ratio:** ~5:1.
- **Analysis:** On average, 5 uniquely phrased Question IDs will map to a single Formula Variant. This perfectly insulates the mathematical layer from semantic NLP bloat.

### 3.4 Answer Template Families
- **Constraint:** Global reuse.
- **Projected Total:** **< 10 Template Families** (e.g., Timing, Strength, Risk, Quality).
- **Analysis:** Because templates only dictate the structural formatting of the output payload and rely on the `evidence_block` for data, the system can render narrative answers for all 500 questions using fewer than 30 total `.txt` files (3 states per family).

## 4. Maintenance Risk Analysis
This mapping completely eliminates "Formula Explosion." By isolating logic into 35 Base Families and 100 Variants, a system update (e.g., refining the calculation of Ashtakavarga bindus) requires editing a single Base Family JSON file, instantly correcting the evaluation logic for dozens of downstream Question IDs simultaneously.
