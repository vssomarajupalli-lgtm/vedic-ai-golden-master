# FORMULA LIBRARY SCALING GOVERNANCE v1

## 1. Core Governance Directives
As the Formula Library expands to encompass the complete canonical Question Registry, the following immutable governance rules apply:

1. **Evaluate Once, Consume Many:** Formulas must only extract and evaluate deterministic signals. No downstream presentation layer (LLM Composer, PDF Report, UI) may perform astrological calculations.
2. **Strict Reuse:** A new formula variant may only be created if the mathematical logic (confidence layers) required to answer the question differs from an existing variant. 
3. **No Semantic Formulas:** Formulas must not be created purely to change the linguistic tone of an answer. Tone variations must be handled by mapping multiple questions to the same formula but mapping to different presentation templates via the Answer Composer.

## 2. Mitigation of Maintenance Risks
To prevent "formula explosion" and massive maintenance burdens, the system implements the following risk mitigations:

### 2.1 Duplicate Logic Risk
- **Mitigation:** Inheritance. Base formulas encapsulate 80% of the standard logic (e.g., standard planetary strength checks). Child variants only append the 20% niche logic (e.g., specific transit triggers). A bug in the foundational logic only needs to be fixed in the Base formula.

### 2.2 Template Sprawl Risk
- **Mitigation:** The Answer Composer architecture explicitly prevents template bloat. Templates are tied strictly to generalized categories (`timing_assessment`, `multifactor_assessment`, `strength_assessment`). We do not create a unique text template for every single formula. A generic `favorable`, `mixed`, and `unfavorable` template covers an entire class of formulas.

### 2.3 Evaluator Complexity Creep
- **Mitigation:** The Formula Evaluator must permanently remain mathematically blind. It is forbidden from substituting variables, resolving dynamic arrays, or executing custom python functions per formula. It is a pure boolean check engine against the JSON schema.

## 3. Registry Coverage Roadmap

Expansion will proceed in a phased, domain-driven sequence.

### Phase A: Core Relationship & Wealth (Current Focus)
- **Domains:** Marriage (Domain 7), Career (Domain 10), Wealth (Domain 2)
- **Goal:** Establish the foundational Base formulas for relationships and finances.

### Phase B: Health, Litigation, and Property
- **Domains:** Health (Domain 6), Property/Vehicles (Domain 4), Litigation/Enemies (Domain 6)
- **Goal:** Introduce multi-house synthesis formulas (e.g., 6th vs Lagna lord).

### Phase C: Education, Travel, and Spirituality
- **Domains:** Education (Domain 4/5/9), Travel (Domain 3/9/12), Spirituality (Domain 9/12)
- **Goal:** Expand YogaEngine extraction to map highly specific education/spiritual yogas into the formulas.

### Phase D: Mandali Gochara Integration
- **Goal:** Retrofit the Base formulas across all domains to trigger `future_gochara_required`, enabling Moon-centered timeline predictions.
